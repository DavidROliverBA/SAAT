"""SAAT Client - High-level API for programmatic usage."""

from typing import Optional

from saat.agents.discovery import DiscoveryAgent
from saat.agents.generator import GeneratorAgent
from saat.broker import ContextBroker
from saat.models import BusinessContext, C4Model, DiscoveryResult


class SAATClient:
    """High-level client for SAAT operations.

    Example:
        ```python
        from saat import SAATClient

        client = SAATClient(model="anthropic:claude-sonnet-4")

        # Discover architecture
        discovery = await client.discover("/path/to/repo")

        # Generate C4 model
        model = await client.generate_model(discovery)

        # Or do both at once
        discovery, model = await client.analyze("/path/to/repo")
        ```
    """

    def __init__(self, model: str = "anthropic:claude-sonnet-4"):
        """Initialize SAAT client.

        Args:
            model: Model identifier (e.g., "anthropic:claude-sonnet-4", "openai:gpt-4")
        """
        self.model = model
        self.discovery_agent = DiscoveryAgent(model)
        self.generator_agent = GeneratorAgent(model)
        self.broker = ContextBroker(model)

    async def discover(
        self, repo_path: str, max_depth: int = 3, context: Optional[str] = None
    ) -> DiscoveryResult:
        """Discover architecture from repository.

        Args:
            repo_path: Path to repository to analyze
            max_depth: Maximum directory depth to explore
            context: Optional additional context or focus areas

        Returns:
            Discovery results

        Example:
            ```python
            discovery = await client.discover(
                "/path/to/repo",
                context="Focus on API architecture"
            )
            print(f"Found: {discovery.technologies}")
            ```
        """
        if context:
            return await self.discovery_agent.analyze_repository_with_context(
                repo_path, context, max_depth
            )
        return await self.discovery_agent.analyze_repository(repo_path, max_depth)

    async def generate_model(
        self,
        discovery: DiscoveryResult,
        business_context: Optional[BusinessContext] = None,
        project_name: Optional[str] = None,
    ) -> C4Model:
        """Generate C4 model from discovery results.

        Args:
            discovery: Discovery results
            business_context: Optional business context for better generation
            project_name: Optional project name override

        Returns:
            C4 model

        Example:
            ```python
            business = BusinessContext(
                purpose="E-commerce platform",
                capabilities=["Orders", "Payments", "Inventory"]
            )
            model = await client.generate_model(discovery, business)
            ```
        """
        return await self.generator_agent.generate_model(
            discovery, business_context, project_name
        )

    async def refine_model(self, model: C4Model, feedback: str) -> C4Model:
        """Refine existing model based on feedback.

        Args:
            model: Existing C4 model
            feedback: Refinement instructions

        Returns:
            Refined model

        Example:
            ```python
            refined = await client.refine_model(
                model,
                "Add Redis cache container and update relationships"
            )
            ```
        """
        return await self.generator_agent.refine_model(model, feedback)

    async def analyze(
        self,
        repo_path: str,
        business_context: Optional[BusinessContext] = None,
        max_depth: int = 3,
    ) -> tuple[DiscoveryResult, C4Model]:
        """Complete analysis: discover and generate in one call.

        Args:
            repo_path: Repository path to analyze
            business_context: Optional business context
            max_depth: Maximum directory depth

        Returns:
            Tuple of (discovery_result, c4_model)

        Example:
            ```python
            discovery, model = await client.analyze("/path/to/repo")

            # Save results
            with open("model.json", "w") as f:
                f.write(model.model_dump_json(indent=2))
            ```
        """
        return await self.broker.discover_and_generate(repo_path, business_context)
