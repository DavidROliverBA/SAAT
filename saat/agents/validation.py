"""Validation Agent - Validates C4 models against standards and best practices."""

from pathlib import Path
from typing import Any, Optional

from pydantic_ai import Agent, RunContext

from saat.agents.base import BaseAgentWithChecklist
from saat.models import (
    AgentChecklist,
    C4Model,
    ChecklistItem,
    ValidationIssue,
    ValidationResult,
)


class ValidationDependencies:
    """Dependencies for validation."""

    def __init__(self, model: C4Model, framework: Optional[str] = None):
        self.model = model
        self.framework = framework  # e.g., "PCI-DSS", "HIPAA", "GDPR"


def create_validation_agent(model_name: str = "anthropic:claude-sonnet-4") -> Agent[
    ValidationDependencies, ValidationResult
]:
    """Create validation agent.

    Args:
        model_name: Model identifier

    Returns:
        Configured PydanticAI agent
    """
    agent: Agent[ValidationDependencies, ValidationResult] = Agent(
        model_name,
        deps_type=ValidationDependencies,
        result_type=ValidationResult,
        system_prompt="""You are an expert architecture validator.

Validate C4 architecture models for:

1. **Structural Integrity**
   - All relationships have valid source and target IDs
   - Containers reference valid systems
   - Components reference valid containers
   - No orphaned elements

2. **Completeness**
   - All elements have descriptions
   - Critical systems have owners
   - Criticality levels assigned appropriately
   - Interfaces specified for containers

3. **Best Practices**
   - Clear naming conventions
   - Proper criticality assignment (CS1 for critical systems)
   - External dependencies documented
   - Relationships have protocols specified

4. **Compliance** (if framework specified)
   - PCI-DSS: Encryption, audit logs, access controls
   - HIPAA: PHI protection, encryption, audit trails
   - GDPR: Data privacy, right to deletion, consent
   - SOC2: Security controls, monitoring, access management

Rate severity:
- **error**: Must be fixed (breaks model integrity)
- **warning**: Should be fixed (missing best practices)
- **info**: Consider fixing (suggestions for improvement)

Provide actionable suggestions for each issue.
""",
    )

    @agent.tool
    async def check_structure(ctx: RunContext[ValidationDependencies]) -> dict[str, Any]:
        """Check structural integrity of C4 model.

        Args:
            ctx: Agent context

        Returns:
            Dictionary with structural issues
        """
        model = ctx.deps.model
        issues = []

        # Collect all IDs
        all_ids = set()
        all_ids.update(s.id for s in model.systems)
        all_ids.update(c.id for c in model.containers)
        all_ids.update(comp.id for comp in model.components)
        all_ids.update(e.id for e in model.externals)

        # Check relationships
        for rel in model.relationships:
            if rel.source not in all_ids:
                issues.append(f"Relationship {rel.id}: source '{rel.source}' not found")
            if rel.target not in all_ids:
                issues.append(f"Relationship {rel.id}: target '{rel.target}' not found")

        # Check container references
        system_ids = {s.id for s in model.systems}
        for container in model.containers:
            if container.system_id not in system_ids:
                issues.append(f"Container {container.name}: references unknown system '{container.system_id}'")

        # Check component references
        container_ids = {c.id for c in model.containers}
        for component in model.components:
            if component.container_id not in container_ids:
                issues.append(f"Component {component.name}: references unknown container '{component.container_id}'")

        return {
            "issues": issues,
            "total_elements": len(all_ids),
            "relationships": len(model.relationships)
        }

    @agent.tool
    async def check_compliance(
        ctx: RunContext[ValidationDependencies],
        framework: str
    ) -> dict[str, Any]:
        """Check compliance with specific framework.

        Args:
            ctx: Agent context
            framework: Compliance framework (PCI-DSS, HIPAA, etc.)

        Returns:
            Dictionary with compliance issues
        """
        model = ctx.deps.model
        issues = []

        if framework == "PCI-DSS":
            # Check payment systems have encryption
            for container in model.containers:
                if any("payment" in tag.lower() for tag in container.tags):
                    if not any(i.encrypted for i in container.interfaces):
                        issues.append(f"{container.name}: Payment container must use encryption")

        elif framework == "HIPAA":
            # Check health data systems have proper security
            for container in model.containers:
                if any("health" in tag.lower() or "patient" in tag.lower() for tag in container.tags):
                    if container.criticality not in ["CS1", "CS2"]:
                        issues.append(f"{container.name}: Health data container should be CS1/CS2")

        return {
            "framework": framework,
            "issues": issues
        }

    return agent


class ValidationAgent(BaseAgentWithChecklist):
    """Validation Agent for C4 models."""

    def __init__(self, model: str = "anthropic:claude-sonnet-4"):
        """Initialize validation agent.

        Args:
            model: Model identifier
        """
        super().__init__("ValidationAgent", model)
        self.agent = create_validation_agent(model)

    async def create_checklist(
        self,
        task_description: str,
        context: Optional[dict[str, Any]] = None
    ) -> AgentChecklist:
        """Generate validation checklist.

        Args:
            task_description: Task description
            context: Should contain 'model' and optional 'framework'

        Returns:
            AgentChecklist
        """
        framework = context.get("framework") if context else None

        items = [
            ChecklistItem(
                id="1",
                description="Load and parse C4 model",
                estimated_duration="5s"
            ),
            ChecklistItem(
                id="2",
                description="Check structural integrity",
                estimated_duration="10s",
                dependencies=["1"]
            ),
            ChecklistItem(
                id="3",
                description="Validate relationships",
                estimated_duration="10s",
                dependencies=["1"]
            ),
            ChecklistItem(
                id="4",
                description="Check completeness (descriptions, owners, etc.)",
                estimated_duration="10s",
                dependencies=["1"]
            ),
            ChecklistItem(
                id="5",
                description="Verify criticality assignments",
                estimated_duration="10s",
                dependencies=["1"]
            ),
            ChecklistItem(
                id="6",
                description="Check best practices",
                estimated_duration="10s",
                dependencies=["1"]
            )
        ]

        if framework:
            items.append(
                ChecklistItem(
                    id="7",
                    description=f"Validate {framework} compliance requirements",
                    estimated_duration="15s",
                    dependencies=["1"]
                )
            )

        items.append(
            ChecklistItem(
                id="8" if framework else "7",
                description="Generate validation report",
                estimated_duration="5s",
                dependencies=["2", "3", "4", "5", "6"] + (["7"] if framework else [])
            )
        )

        return AgentChecklist(
            agent_name=self.agent_name,
            task_description=task_description,
            items=items,
            estimated_total_duration="1-2 minutes",
            requires_approval=True
        )

    async def validate_model(
        self,
        model: C4Model,
        framework: Optional[str] = None,
        auto_approve: bool = False
    ) -> dict[str, Any]:
        """Validate C4 model.

        Args:
            model: C4 model to validate
            framework: Optional compliance framework
            auto_approve: Skip approval prompts

        Returns:
            Dictionary with validation results
        """
        context = {
            "model": model,
            "framework": framework
        }

        # Execute with checklist
        result = await self.execute_with_checklist(
            task_description=f"Validate C4 model{f' against {framework}' if framework else ''}",
            auto_approve=auto_approve,
            context=context
        )

        if result["cancelled"]:
            return result

        # Perform validation
        deps = ValidationDependencies(model, framework)

        prompt = f"""Validate this C4 architecture model:

**Model**: {model.metadata.project}
**Systems**: {len(model.systems)}
**Containers**: {len(model.containers)}
**Components**: {len(model.components)}
**Relationships**: {len(model.relationships)}
{f"**Compliance Framework**: {framework}" if framework else ""}

Use the tools to:
1. Check structural integrity
2. Check compliance (if framework specified)
3. Identify all issues with severity and suggestions

Provide a complete validation report."""

        agent_result = await self.agent.run(prompt, deps=deps)
        validation = agent_result.data

        result["validation"] = validation
        result["summary"] = {
            "valid": validation.valid,
            "score": validation.score,
            "total_issues": len(validation.issues),
            "errors": len([i for i in validation.issues if i.severity == "error"]),
            "warnings": len([i for i in validation.issues if i.severity == "warning"]),
            "info": len([i for i in validation.issues if i.severity == "info"])
        }

        return result


async def validate_c4_model(
    model: C4Model,
    framework: Optional[str] = None,
    model_name: str = "anthropic:claude-sonnet-4",
    auto_approve: bool = False
) -> ValidationResult:
    """Convenience function to validate C4 model.

    Args:
        model: C4 model to validate
        framework: Optional compliance framework
        model_name: Model to use
        auto_approve: Skip approval prompts

    Returns:
        ValidationResult
    """
    agent = ValidationAgent(model_name)
    result = await agent.validate_model(model, framework, auto_approve)

    if result.get("cancelled"):
        raise ValueError("Validation was cancelled")

    return result["validation"]
