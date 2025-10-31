"""Context Broker - Orchestrates multi-agent pipelines."""

import asyncio
from datetime import datetime
from typing import Any, Optional

from saat.agents.discovery import DiscoveryAgent
from saat.agents.generator import GeneratorAgent
from saat.models import BusinessContext, C4Model, DiscoveryResult, Pipeline, PipelineStep


class ContextBroker:
    """Orchestrates execution of agent pipelines."""

    def __init__(self, model: str = "anthropic:claude-sonnet-4"):
        """Initialize context broker.

        Args:
            model: Default model to use for agents
        """
        self.model = model
        self.discovery_agent = DiscoveryAgent(model)
        self.generator_agent = GeneratorAgent(model)
        self.context: dict[str, Any] = {}

    async def execute_pipeline(
        self, pipeline: Pipeline, initial_context: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        """Execute an agent pipeline.

        Args:
            pipeline: Pipeline configuration
            initial_context: Initial context data

        Returns:
            Results from all pipeline steps
        """
        if initial_context:
            self.context.update(initial_context)

        results: dict[str, Any] = {}
        start_time = datetime.now()

        for step in pipeline.steps:
            # Check dependencies
            if step.depends_on:
                missing_deps = [dep for dep in step.depends_on if dep not in results]
                if missing_deps:
                    if step.required:
                        raise ValueError(
                            f"Step '{step.name}' missing required dependencies: {missing_deps}"
                        )
                    else:
                        continue

            # Execute step
            try:
                result = await self._execute_step(step, results)
                results[step.name] = {"success": True, "data": result, "error": None}
                self.context[step.name] = result
            except Exception as e:
                results[step.name] = {"success": False, "data": None, "error": str(e)}
                if step.required:
                    break

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        return {
            "pipeline": pipeline.name,
            "results": results,
            "duration": duration,
            "success": all(r.get("success", False) for r in results.values()),
        }

    async def _execute_step(self, step: PipelineStep, previous_results: dict[str, Any]) -> Any:
        """Execute a single pipeline step.

        Args:
            step: Step configuration
            previous_results: Results from previous steps

        Returns:
            Step result
        """
        # Execute based on agent type
        if step.agent == "discovery":
            repo_path = self.context.get("repo_path") or previous_results.get("repo_path")
            return await self.discovery_agent.analyze_repository(repo_path)

        elif step.agent == "generator":
            # Get discovery from previous step or context
            discovery = None
            for dep in step.depends_on:
                if dep in previous_results and previous_results[dep].get("success"):
                    data = previous_results[dep]["data"]
                    if isinstance(data, DiscoveryResult):
                        discovery = data
                        break

            if not discovery:
                discovery = self.context.get("discovery")

            if not discovery:
                raise ValueError("Generator requires discovery result")

            business_context = self.context.get("business_context")
            return await self.generator_agent.generate_model(discovery, business_context)

        else:
            raise ValueError(f"Unknown agent type: {step.agent}")

    async def discover_and_generate(
        self,
        repo_path: str,
        business_context: Optional[BusinessContext] = None,
    ) -> tuple[DiscoveryResult, C4Model]:
        """Convenience method to discover and generate in one call.

        Args:
            repo_path: Repository path to analyze
            business_context: Optional business context

        Returns:
            Tuple of (discovery_result, c4_model)
        """
        # Store in context
        self.context["repo_path"] = repo_path
        if business_context:
            self.context["business_context"] = business_context

        # Run discovery
        discovery = await self.discovery_agent.analyze_repository(repo_path)
        self.context["discovery"] = discovery

        # Generate model
        model = await self.generator_agent.generate_model(discovery, business_context)

        return discovery, model
