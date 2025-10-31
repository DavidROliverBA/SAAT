"""Base agent class with checklist and approval support."""

import sys
from typing import Any, Optional

from pydantic_ai import Agent

from saat.models import AgentChecklist, ApprovalRequest, ApprovalResponse, ChecklistItem


class BaseAgentWithChecklist:
    """Base class for agents with checklist and approval support.

    All agents should inherit from this to get:
    - Automatic checklist generation
    - Human-in-the-loop approval workflow
    - Auto-approve mode for automation
    - Progress tracking
    """

    def __init__(self, agent_name: str, model: str = "anthropic:claude-sonnet-4"):
        """Initialize base agent.

        Args:
            agent_name: Name of the agent (e.g., "ValidationAgent")
            model: Model to use for LLM calls
        """
        self.agent_name = agent_name
        self.model = model
        self.current_checklist: Optional[AgentChecklist] = None

    async def create_checklist(
        self,
        task_description: str,
        context: Optional[dict[str, Any]] = None
    ) -> AgentChecklist:
        """Generate a checklist for the task.

        This should be overridden by subclasses to provide specific checklists.

        Args:
            task_description: Description of the task to perform
            context: Additional context for checklist generation

        Returns:
            AgentChecklist with items to execute
        """
        # Default implementation - subclasses should override
        return AgentChecklist(
            agent_name=self.agent_name,
            task_description=task_description,
            items=[
                ChecklistItem(
                    id="1",
                    description="Execute task",
                    estimated_duration="Unknown"
                )
            ],
            estimated_total_duration="Unknown",
            requires_approval=True
        )

    def display_checklist(self, checklist: AgentChecklist) -> None:
        """Display checklist to user in CLI.

        Args:
            checklist: Checklist to display
        """
        print(f"\n📋 {checklist.agent_name} Checklist:")
        print(f"Task: {checklist.task_description}")

        if checklist.estimated_total_duration:
            print(f"Estimated Duration: {checklist.estimated_total_duration}")

        print("\nTasks:")
        for item in checklist.items:
            status = "✓" if item.completed else " "
            duration = f" (est: {item.estimated_duration})" if item.estimated_duration else ""
            print(f"  [{status}] {item.description}{duration}")

        print()

    async def request_approval(
        self,
        checklist: AgentChecklist,
        auto_approve: bool = False
    ) -> ApprovalResponse:
        """Request human approval for checklist.

        Args:
            checklist: Checklist to approve
            auto_approve: If True, automatically approve without prompting

        Returns:
            ApprovalResponse with approval status
        """
        if auto_approve:
            checklist.approved = True
            checklist.approved_by = "auto-approved"
            print("✅ Auto-approved")
            return ApprovalResponse(
                approved=True,
                feedback="Auto-approved in automation mode"
            )

        # Interactive approval
        try:
            response = input("Proceed? [y/N]: ").strip().lower()
            approved = response in ['y', 'yes']

            checklist.approved = approved
            if approved:
                checklist.approved_by = "user"
                print("✅ Approved")
            else:
                print("❌ Cancelled")

            return ApprovalResponse(
                approved=approved,
                feedback="User approval" if approved else "User cancelled"
            )
        except (KeyboardInterrupt, EOFError):
            print("\n❌ Cancelled")
            return ApprovalResponse(
                approved=False,
                feedback="Interrupted by user"
            )

    async def execute_checklist_item(
        self,
        item: ChecklistItem,
        context: Optional[dict[str, Any]] = None
    ) -> str:
        """Execute a single checklist item.

        This should be overridden by subclasses to provide actual execution.

        Args:
            item: Checklist item to execute
            context: Execution context

        Returns:
            Result string
        """
        # Default implementation - subclasses should override
        return f"Executed: {item.description}"

    async def execute_with_checklist(
        self,
        task_description: str,
        auto_approve: bool = False,
        context: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        """Execute task with checklist approval workflow.

        Args:
            task_description: Task to execute
            auto_approve: Skip approval prompts
            context: Additional context

        Returns:
            Dictionary with execution results and checklist
        """
        # 1. Generate checklist
        checklist = await self.create_checklist(task_description, context)
        self.current_checklist = checklist

        # 2. Display checklist
        self.display_checklist(checklist)

        # 3. Request approval
        approval = await self.request_approval(checklist, auto_approve)

        if not approval.approved:
            return {
                "success": False,
                "cancelled": True,
                "checklist": checklist,
                "feedback": approval.feedback
            }

        # 4. Execute tasks
        print("\n🔄 Executing tasks...\n")
        results = []

        for item in checklist.items:
            try:
                print(f"⏳ {item.description}...", end="", flush=True)

                result = await self.execute_checklist_item(item, context)
                item.completed = True
                item.result = result
                results.append(result)

                print(f" ✅")

            except Exception as e:
                print(f" ❌")
                print(f"   Error: {e}")
                item.result = f"Error: {e}"
                results.append(None)

        print("\n✨ Complete!")

        return {
            "success": True,
            "cancelled": False,
            "checklist": checklist,
            "results": results
        }

    def update_progress(self, item_id: str, result: str) -> None:
        """Update progress for a checklist item.

        Args:
            item_id: ID of item to update
            result: Result to store
        """
        if not self.current_checklist:
            return

        for item in self.current_checklist.items:
            if item.id == item_id:
                item.completed = True
                item.result = result
                break
