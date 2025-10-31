"""Requirements Discovery Agent - Extracts requirements from documents for greenfield projects."""

from pathlib import Path
from typing import Any, Optional

from pydantic_ai import Agent, RunContext

from saat.agents.base import BaseAgentWithChecklist
from saat.models import (
    AgentChecklist,
    ChecklistItem,
    ProjectRequirements,
    Requirement,
    TechnicalConstraint,
    UserStory,
)


class RequirementsDependencies:
    """Dependencies for requirements discovery."""

    def __init__(self, file_paths: list[str]):
        self.file_paths = file_paths
        self.file_contents: dict[str, str] = {}

    async def read_file(self, file_path: str) -> str:
        """Read file contents."""
        if file_path in self.file_contents:
            return self.file_contents[file_path]

        path = Path(file_path)
        if path.exists():
            content = path.read_text(encoding="utf-8", errors="ignore")
            self.file_contents[file_path] = content
            return content

        return ""


def create_requirements_agent(model: str = "anthropic:claude-sonnet-4") -> Agent[
    RequirementsDependencies, ProjectRequirements
]:
    """Create requirements discovery agent.

    Args:
        model: Model identifier

    Returns:
        Configured PydanticAI agent
    """
    agent: Agent[RequirementsDependencies, ProjectRequirements] = Agent(
        model,
        deps_type=RequirementsDependencies,
        result_type=ProjectRequirements,
        system_prompt="""You are an expert requirements analyst for software projects.

Your role is to extract and structure requirements from documents:

1. **Functional Requirements**: What the system must do
   - Format: REQ-F-001, REQ-F-002, etc.
   - Clear, testable requirements
   - Include acceptance criteria

2. **Non-Functional Requirements**: Quality attributes
   - Format: REQ-NF-001, REQ-NF-002, etc.
   - Performance, security, scalability, etc.
   - Measurable criteria

3. **User Stories**: Agile format
   - Format: US-001, US-002, etc.
   - "As a [role], I want [feature], so that [benefit]"
   - Include acceptance criteria

4. **Technical Constraints**: Limitations
   - Format: CONST-001, CONST-002, etc.
   - Technology choices, compliance, budget, timeline
   - Explain rationale

5. **Stakeholders**: Identify all stakeholders and their needs

Parse markdown sections, bullet points, and natural language.
Extract all relevant information and structure it properly.
Generate unique IDs consistently.
""",
    )

    @agent.tool
    async def read_document(
        ctx: RunContext[RequirementsDependencies], file_path: str
    ) -> dict[str, str]:
        """Read a requirements document.

        Args:
            ctx: Agent context
            file_path: Path to document

        Returns:
            Dictionary with file path and contents
        """
        content = await ctx.deps.read_file(file_path)
        return {
            "file_path": file_path,
            "content": content[:10000],  # Limit to 10k chars per file
            "length": len(content)
        }

    return agent


class RequirementsAgent(BaseAgentWithChecklist):
    """Requirements Discovery Agent for greenfield projects."""

    def __init__(self, model: str = "anthropic:claude-sonnet-4"):
        """Initialize requirements agent.

        Args:
            model: Model identifier
        """
        super().__init__("RequirementsAgent", model)
        self.agent = create_requirements_agent(model)

    async def create_checklist(
        self,
        task_description: str,
        context: Optional[dict[str, Any]] = None
    ) -> AgentChecklist:
        """Generate checklist for requirements discovery.

        Args:
            task_description: Task description
            context: Should contain 'file_paths' list

        Returns:
            AgentChecklist
        """
        file_paths = context.get("file_paths", []) if context else []
        num_files = len(file_paths)

        items = [
            ChecklistItem(
                id="1",
                description=f"Read {num_files} requirements document(s)",
                estimated_duration="10-30s"
            ),
            ChecklistItem(
                id="2",
                description="Extract functional requirements",
                estimated_duration="20-40s",
                dependencies=["1"]
            ),
            ChecklistItem(
                id="3",
                description="Extract non-functional requirements",
                estimated_duration="15-30s",
                dependencies=["1"]
            ),
            ChecklistItem(
                id="4",
                description="Parse user stories",
                estimated_duration="15-30s",
                dependencies=["1"]
            ),
            ChecklistItem(
                id="5",
                description="Identify technical constraints",
                estimated_duration="10-20s",
                dependencies=["1"]
            ),
            ChecklistItem(
                id="6",
                description="Identify stakeholders",
                estimated_duration="10-20s",
                dependencies=["1"]
            ),
            ChecklistItem(
                id="7",
                description="Generate structured ProjectRequirements",
                estimated_duration="10s",
                dependencies=["2", "3", "4", "5", "6"]
            )
        ]

        return AgentChecklist(
            agent_name=self.agent_name,
            task_description=task_description,
            items=items,
            estimated_total_duration="2-3 minutes",
            requires_approval=True
        )

    async def execute_checklist_item(
        self,
        item: ChecklistItem,
        context: Optional[dict[str, Any]] = None
    ) -> str:
        """Execute checklist item.

        Args:
            item: Item to execute
            context: Execution context

        Returns:
            Result string
        """
        # All items executed together in discover_requirements
        return f"Completed: {item.description}"

    async def discover_requirements(
        self,
        file_paths: list[str],
        project_name: Optional[str] = None,
        auto_approve: bool = False
    ) -> dict[str, Any]:
        """Discover requirements from documents.

        Args:
            file_paths: List of file paths to analyze
            project_name: Optional project name
            auto_approve: Skip approval prompts

        Returns:
            Dictionary with requirements and execution info
        """
        # Prepare context
        context = {
            "file_paths": file_paths,
            "project_name": project_name
        }

        # Execute with checklist workflow
        result = await self.execute_with_checklist(
            task_description=f"Discover requirements from {len(file_paths)} file(s)",
            auto_approve=auto_approve,
            context=context
        )

        if result["cancelled"]:
            return result

        # Actually perform discovery
        deps = RequirementsDependencies(file_paths)

        # Build prompt
        files_info = []
        for fp in file_paths:
            content = await deps.read_file(fp)
            files_info.append(f"File: {fp}\nLength: {len(content)} chars")

        prompt = f"""Analyze the following requirements documents and extract all requirements.

Project Name: {project_name or "Unknown"}

Documents to analyze:
{chr(10).join(files_info)}

Please read each document and extract:
1. Functional requirements
2. Non-functional requirements
3. User stories
4. Technical constraints
5. Stakeholders

Generate unique IDs and structure everything properly."""

        # Run agent
        agent_result = await self.agent.run(prompt, deps=deps)
        requirements = agent_result.data

        # Override project name if provided
        if project_name:
            requirements.project_name = project_name

        # Set source documents
        requirements.source_documents = file_paths

        result["requirements"] = requirements
        result["summary"] = {
            "functional_requirements": len([r for r in requirements.requirements if r.type == "functional"]),
            "non_functional_requirements": len([r for r in requirements.requirements if r.type == "non-functional"]),
            "user_stories": len(requirements.user_stories),
            "constraints": len(requirements.constraints),
            "stakeholders": len(requirements.stakeholders)
        }

        return result


async def discover_requirements(
    file_paths: list[str],
    project_name: Optional[str] = None,
    model: str = "anthropic:claude-sonnet-4",
    auto_approve: bool = False
) -> ProjectRequirements:
    """Convenience function to discover requirements.

    Args:
        file_paths: Paths to requirement documents
        project_name: Optional project name
        model: Model to use
        auto_approve: Skip approval prompts

    Returns:
        ProjectRequirements
    """
    agent = RequirementsAgent(model)
    result = await agent.discover_requirements(file_paths, project_name, auto_approve)

    if result.get("cancelled"):
        raise ValueError("Requirements discovery was cancelled")

    return result["requirements"]
