"""Documentation Agent - Generates comprehensive documentation from C4 models."""

from pathlib import Path
from typing import Any, Optional

from pydantic_ai import Agent, RunContext

from saat.agents.base import BaseAgentWithChecklist
from saat.models import AgentChecklist, C4Model, ChecklistItem


class DocumentationDependencies:
    """Dependencies for documentation generation."""

    def __init__(self, model: C4Model, output_dir: str, formats: list[str]):
        self.model = model
        self.output_dir = Path(output_dir)
        self.formats = formats  # ["markdown", "plantuml", "mermaid", "adr"]
        self.generated_files: list[str] = []


def create_documentation_agent(model_name: str = "anthropic:claude-sonnet-4") -> Agent[
    DocumentationDependencies, dict[str, Any]
]:
    """Create documentation generation agent.

    Args:
        model_name: Model identifier

    Returns:
        Configured PydanticAI agent
    """
    agent: Agent[DocumentationDependencies, dict[str, Any]] = Agent(
        model_name,
        deps_type=DocumentationDependencies,
        result_type=dict,
        system_prompt="""You are an expert technical writer specializing in software architecture documentation.

Generate comprehensive, clear documentation from C4 architecture models:

1. **Markdown Overview**
   - Project summary
   - System context description
   - Technology stack
   - Key architectural decisions

2. **C4 Diagrams** (PlantUML/Mermaid)
   - System Context diagram (Level 1)
   - Container diagram (Level 2)
   - Component diagrams (Level 3)
   - Deployment diagram

3. **Architecture Decision Records (ADRs)**
   - For each major architectural decision
   - Context, Decision, Consequences
   - Numbered sequentially (ADR-001, ADR-002, etc.)

4. **Component Documentation**
   - Each system, container, component
   - Purpose, responsibilities, interfaces
   - Technology choices and rationale

5. **Deployment Documentation**
   - Infrastructure requirements
   - Scaling considerations
   - Monitoring and alerting

Use clear, professional language. Include diagrams as code (PlantUML/Mermaid).
""",
    )

    @agent.tool
    async def generate_overview(ctx: RunContext[DocumentationDependencies]) -> str:
        """Generate markdown overview document.

        Args:
            ctx: Agent context

        Returns:
            Markdown content
        """
        model = ctx.deps.model

        # Generate overview markdown
        overview = f"""# {model.metadata.project} - Architecture Documentation

**Author**: {model.metadata.author}
**Version**: {model.version}
**Last Updated**: {model.metadata.last_modified.strftime('%Y-%m-%d')}

## Overview

{model.metadata.description}

## Systems

"""
        for system in model.systems:
            overview += f"### {system.name}\n\n"
            overview += f"{system.description}\n\n"
            overview += f"- **ID**: `{system.id}`\n"
            overview += f"- **Criticality**: {system.criticality}\n"
            if system.owner:
                overview += f"- **Owner**: {system.owner}\n"
            overview += "\n"

        overview += "## Containers\n\n"
        for container in model.containers:
            overview += f"### {container.name}\n\n"
            overview += f"{container.description}\n\n"
            overview += f"- **Technology**: {', '.join(container.technology)}\n"
            overview += f"- **Criticality**: {container.criticality}\n"
            overview += "\n"

        return overview

    @agent.tool
    async def generate_plantuml_diagram(
        ctx: RunContext[DocumentationDependencies],
        diagram_type: str
    ) -> str:
        """Generate PlantUML diagram.

        Args:
            ctx: Agent context
            diagram_type: "context", "container", or "component"

        Returns:
            PlantUML code
        """
        model = ctx.deps.model

        if diagram_type == "context":
            # System context diagram
            puml = "@startuml\n!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Context.puml\n\n"
            puml += f"LAYOUT_WITH_LEGEND()\ntitle System Context - {model.metadata.project}\n\n"

            for system in model.systems:
                puml += f"System({system.id}, \"{system.name}\", \"{system.description}\")\n"

            for external in model.externals:
                puml += f"System_Ext({external.id}, \"{external.name}\", \"{external.description}\")\n"

            for rel in model.relationships:
                if any(rel.source == s.id or rel.target == s.id for s in model.systems):
                    puml += f"Rel({rel.source}, {rel.target}, \"{rel.description}\")\n"

            puml += "\n@enduml"
            return puml

        return "@startuml\n' Diagram generation not implemented yet\n@enduml"

    return agent


class DocumentationAgent(BaseAgentWithChecklist):
    """Documentation Agent for generating architecture documentation."""

    def __init__(self, model: str = "anthropic:claude-sonnet-4"):
        """Initialize documentation agent.

        Args:
            model: Model identifier
        """
        super().__init__("DocumentationAgent", model)
        self.agent = create_documentation_agent(model)

    async def create_checklist(
        self,
        task_description: str,
        context: Optional[dict[str, Any]] = None
    ) -> AgentChecklist:
        """Generate documentation checklist.

        Args:
            task_description: Task description
            context: Should contain 'formats' list

        Returns:
            AgentChecklist
        """
        formats = context.get("formats", ["markdown"]) if context else ["markdown"]

        items = [
            ChecklistItem(
                id="1",
                description="Load and analyze C4 model",
                estimated_duration="5s"
            ),
            ChecklistItem(
                id="2",
                description="Generate markdown overview document",
                estimated_duration="15s",
                dependencies=["1"]
            )
        ]

        item_id = 3
        if "plantuml" in formats:
            items.append(
                ChecklistItem(
                    id=str(item_id),
                    description="Create PlantUML system context diagram",
                    estimated_duration="10s",
                    dependencies=["1"]
                )
            )
            item_id += 1
            items.append(
                ChecklistItem(
                    id=str(item_id),
                    description="Create PlantUML container diagram",
                    estimated_duration="10s",
                    dependencies=["1"]
                )
            )
            item_id += 1

        if "mermaid" in formats:
            items.append(
                ChecklistItem(
                    id=str(item_id),
                    description="Create Mermaid diagrams",
                    estimated_duration="10s",
                    dependencies=["1"]
                )
            )
            item_id += 1

        if "adr" in formats:
            items.append(
                ChecklistItem(
                    id=str(item_id),
                    description="Generate Architecture Decision Records (ADRs)",
                    estimated_duration="20s",
                    dependencies=["1"]
                )
            )
            item_id += 1

        items.append(
            ChecklistItem(
                id=str(item_id),
                description="Create component documentation",
                estimated_duration="15s",
                dependencies=["1"]
            )
        )
        item_id += 1

        items.append(
            ChecklistItem(
                id=str(item_id),
                description="Generate deployment documentation",
                estimated_duration="10s",
                dependencies=["1"]
            )
        )

        return AgentChecklist(
            agent_name=self.agent_name,
            task_description=task_description,
            items=items,
            estimated_total_duration="1-2 minutes",
            requires_approval=True
        )

    async def generate_documentation(
        self,
        model: C4Model,
        output_dir: str = "docs/",
        formats: list[str] = None,
        auto_approve: bool = False
    ) -> dict[str, Any]:
        """Generate documentation from C4 model.

        Args:
            model: C4 model to document
            output_dir: Output directory
            formats: List of formats ["markdown", "plantuml", "mermaid", "adr"]
            auto_approve: Skip approval prompts

        Returns:
            Dictionary with generated files and status
        """
        if formats is None:
            formats = ["markdown"]

        context = {
            "model": model,
            "output_dir": output_dir,
            "formats": formats
        }

        # Execute with checklist
        result = await self.execute_with_checklist(
            task_description=f"Generate documentation ({', '.join(formats)})",
            auto_approve=auto_approve,
            context=context
        )

        if result["cancelled"]:
            return result

        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        deps = DocumentationDependencies(model, output_dir, formats)

        # Generate overview
        overview = await self.agent.tools["generate_overview"](
            RunContext(deps=deps, retry=0, tool_name="generate_overview")
        )
        overview_file = output_path / "architecture-overview.md"
        overview_file.write_text(overview)
        deps.generated_files.append(str(overview_file))

        # Generate PlantUML diagrams if requested
        if "plantuml" in formats:
            context_diagram = await self.agent.tools["generate_plantuml_diagram"](
                RunContext(deps=deps, retry=0, tool_name="generate_plantuml_diagram"),
                diagram_type="context"
            )
            context_file = output_path / "system-context.puml"
            context_file.write_text(context_diagram)
            deps.generated_files.append(str(context_file))

        result["generated_files"] = deps.generated_files
        result["output_dir"] = output_dir
        result["summary"] = {
            "total_files": len(deps.generated_files),
            "formats": formats
        }

        return result


async def generate_documentation(
    model: C4Model,
    output_dir: str = "docs/",
    formats: list[str] = None,
    model_name: str = "anthropic:claude-sonnet-4",
    auto_approve: bool = False
) -> dict[str, Any]:
    """Convenience function to generate documentation.

    Args:
        model: C4 model
        output_dir: Output directory
        formats: Documentation formats
        model_name: Model to use
        auto_approve: Skip approval prompts

    Returns:
        Dictionary with results
    """
    agent = DocumentationAgent(model_name)
    result = await agent.generate_documentation(model, output_dir, formats, auto_approve)

    if result.get("cancelled"):
        raise ValueError("Documentation generation was cancelled")

    return result
