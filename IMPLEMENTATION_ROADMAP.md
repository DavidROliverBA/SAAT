# SAAT Implementation Roadmap

## ✅ Completed (Phase 1)

### Core Foundation
- ✅ Complete migration from TypeScript to Python/PydanticAI
- ✅ Pydantic models for C4 architecture (308 lines)
- ✅ Discovery Agent with tool calling (204 lines)
- ✅ Generator Agent with structured outputs (244 lines)
- ✅ Context Broker for orchestration (116 lines)
- ✅ CLI with 5 commands (263 lines)
- ✅ High-level SAATClient API (127 lines)
- ✅ Comprehensive README (913 lines)

### Greenfield Support (Phase 2 - In Progress)
- ✅ **ProjectRequirements model** - Complete requirements structure
- ✅ **Requirement, UserStory, TechnicalConstraint models** - Detailed requirements
- ✅ **AgentChecklist & ChecklistItem models** - Task tracking
- ✅ **ApprovalRequest/Response models** - Human-in-the-loop

---

## 🚧 In Progress (Phase 2)

### 1. Requirements Discovery Agent
**Purpose**: Read markdown/text files to extract requirements for greenfield projects

**File**: `saat/agents/requirements.py`

```python
from pydantic_ai import Agent, RunContext
from saat.models import ProjectRequirements, Requirement, UserStory

class RequirementsAgent:
    """Discovers requirements from markdown/text files."""

    def __init__(self, model: str = "anthropic:claude-sonnet-4"):
        self.agent = Agent(
            model,
            result_type=ProjectRequirements,
            system_prompt="""You are a requirements analyst.

            Extract requirements from documents:
            1. Functional requirements (what system must do)
            2. Non-functional requirements (performance, security, etc.)
            3. User stories (As a... I want... So that...)
            4. Technical constraints
            5. Stakeholders and their needs

            Parse markdown sections, bullet points, and natural language.
            Generate unique IDs (REQ-001, US-001, etc.).
            """
        )

    async def discover_requirements(
        self,
        requirement_files: list[str],
        project_name: str
    ) -> ProjectRequirements:
        """Read and parse requirement documents."""
        # Implementation needed
```

**Tools Needed**:
- `read_requirement_file(file_path: str) -> str`
- `parse_user_stories(content: str) -> list[UserStory]`
- `identify_constraints(content: str) -> list[TechnicalConstraint]`

---

### 2. Checklist Support in All Agents

**File**: `saat/agents/base.py`

```python
from saat.models import AgentChecklist, ChecklistItem, ApprovalRequest

class BaseAgentWithChecklist:
    """Base class for agents with checklist support."""

    async def create_checklist(
        self,
        task_description: str
    ) -> AgentChecklist:
        """Generate checklist before executing."""
        # Use LLM to generate checklist items
        pass

    async def request_approval(
        self,
        checklist: AgentChecklist,
        auto_approve: bool = False
    ) -> bool:
        """Request human approval or auto-approve."""
        if auto_approve:
            checklist.approved = True
            return True

        # Interactive approval in CLI
        # In Claude Code: use MCP approval workflow
        pass

    async def execute_with_checklist(
        self,
        task: str,
        auto_approve: bool = False
    ):
        """Execute task with checklist approval."""
        # 1. Generate checklist
        checklist = await self.create_checklist(task)

        # 2. Display checklist
        self.display_checklist(checklist)

        # 3. Request approval
        approved = await self.request_approval(checklist, auto_approve)

        if not approved:
            return {"cancelled": True}

        # 4. Execute tasks
        for item in checklist.items:
            result = await self.execute_item(item)
            item.completed = True
            item.result = result

        return checklist
```

---

## 📋 TODO (Phase 3): Complete Remaining Agents

### 3. Validation Agent
**File**: `saat/agents/validation.py`

**Purpose**: Validate C4 models against standards

**Checklist Items**:
1. Load C4 model from file
2. Check structural integrity (orphaned elements)
3. Validate relationships
4. Check criticality assignments
5. Verify compliance requirements (PCI-DSS, HIPAA, etc.)
6. Check security configurations
7. Generate validation report

**Usage**:
```bash
saat validate --model-file architecture.json --framework HIPAA
# Shows checklist, asks for approval, runs validation
```

---

### 4. Documentation Agent
**File**: `saat/agents/documentation.py`

**Purpose**: Generate documentation from C4 models

**Checklist Items**:
1. Load C4 model
2. Generate markdown overview
3. Create system context diagrams (PlantUML)
4. Create container diagrams
5. Create component diagrams
6. Generate ADRs (Architecture Decision Records)
7. Create deployment documentation
8. Publish to Confluence (optional)

**Usage**:
```bash
saat document --model-file architecture.json --output docs/
# Shows checklist of docs to generate, asks approval
```

---

### 5. Security Agent
**File**: `saat/agents/security.py`

**Purpose**: Analyze security posture

**Checklist Items**:
1. Load C4 model
2. Identify unencrypted communications
3. Check authentication mechanisms
4. Analyze data flows for sensitive data
5. Identify missing security controls
6. Check compliance with security frameworks
7. Generate threat model
8. Create security report

**Usage**:
```bash
saat security-scan --model-file architecture.json
```

---

### 6. Terraform Agent
**File**: `saat/agents/terraform.py`

**Purpose**: Generate infrastructure-as-code

**Checklist Items**:
1. Load C4 model
2. Map containers to cloud resources
3. Generate VPC/network configuration
4. Create database resources
5. Set up load balancers
6. Configure auto-scaling (based on criticality)
7. Set up monitoring and alerting
8. Generate backup configurations
9. Create IAM roles and policies
10. Generate terraform files

**Usage**:
```bash
saat generate-terraform --model-file architecture.json --provider aws --output infrastructure/
# Shows full checklist, asks approval before generating
```

---

## 🔌 Phase 4: MCP Server for Claude Code

### MCP Server Implementation
**File**: `saat_mcp_server.py` (root of repo)

```python
#!/usr/bin/env python3
"""MCP Server for SAAT - Integrates with Claude Code."""

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from saat import SAATClient
from saat.agents.requirements import RequirementsAgent

server = Server("saat-architecture")

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(name="discover_architecture", ...),
        Tool(name="generate_c4_model", ...),
        Tool(name="discover_requirements", ...),  # NEW
        Tool(name="validate_model", ...),  # NEW
        Tool(name="generate_documentation", ...),  # NEW
        Tool(name="security_scan", ...),  # NEW
        Tool(name="generate_terraform", ...),  # NEW
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    # Route to appropriate agent
    # All agents use checklist system
    # Auto-approve mode for MCP
    pass
```

**Claude Code Config**:
```json
{
  "mcpServers": {
    "saat": {
      "command": "python",
      "args": ["./saat_mcp_server.py"],
      "env": {
        "ANTHROPIC_API_KEY": "${env:ANTHROPIC_API_KEY}"
      }
    }
  }
}
```

---

## 🎯 Phase 5: CLI Enhancements

### Add --auto-approve Flag

**Update**: `saat/cli.py`

```python
@click.group()
@click.option('--auto-approve', is_flag=True, help='Skip approval prompts')
@click.option('--yes', '-y', is_flag=True, help='Alias for --auto-approve')
@click.pass_context
def main(ctx, auto_approve, yes):
    ctx.obj['auto_approve'] = auto_approve or yes

# Usage in commands:
@main.command()
@click.pass_context
def validate(ctx, model_file):
    auto_approve = ctx.obj.get('auto_approve', False)

    # Agent generates checklist
    checklist = await agent.create_checklist()

    if not auto_approve:
        # Show checklist and ask
        click.echo("Validation tasks:")
        for item in checklist.items:
            click.echo(f"  [ ] {item.description}")

        if not click.confirm("Proceed?"):
            return

    # Execute with auto_approve flag
    result = await agent.execute(auto_approve=auto_approve)
```

---

## 📁 File Structure After Completion

```
SAAT/
├── saat/
│   ├── __init__.py
│   ├── models.py (✅ Updated with requirements & checklists)
│   ├── cli.py (🔄 Add --auto-approve)
│   ├── client.py
│   ├── broker.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base.py (📋 NEW: Base class with checklist support)
│   │   ├── discovery.py (✅ Existing)
│   │   ├── generator.py (✅ Existing)
│   │   ├── requirements.py (📋 NEW: Read markdown requirements)
│   │   ├── validation.py (📋 NEW: Validate C4 models)
│   │   ├── documentation.py (📋 NEW: Generate docs)
│   │   ├── security.py (📋 NEW: Security analysis)
│   │   └── terraform.py (📋 NEW: Generate IaC)
├── saat_mcp_server.py (📋 NEW: Claude Code integration)
├── examples/
│   ├── quick_start.py (✅ Existing)
│   ├── greenfield_project.py (📋 NEW: From-scratch example)
│   └── requirements.md (📋 NEW: Sample requirements doc)
├── README.md (✅ Updated)
├── IMPLEMENTATION_ROADMAP.md (✅ This file)
└── pyproject.toml (✅ Existing)
```

---

## 🎬 Usage Examples After Completion

### Brownfield (Existing Code)
```bash
# Interactive mode (default)
saat analyze --path /path/to/repo

# Shows checklist:
# [ ] Discover technologies
# [ ] Identify patterns
# [ ] Generate C4 model
# [ ] Validate model
# Proceed? [y/N]: y

# Auto mode
saat analyze --path /path/to/repo --auto-approve
# Executes all tasks without prompts
```

### Greenfield (From Scratch)
```bash
# 1. Discover requirements from docs
saat discover-requirements --path docs/requirements.md --output requirements.json

# Shows checklist:
# [ ] Read requirement documents
# [ ] Extract functional requirements
# [ ] Extract user stories
# [ ] Identify constraints
# [ ] Generate requirements.json
# Proceed? [y/N]: y

# 2. Generate architecture from requirements
saat generate-from-requirements --requirements requirements.json --output architecture.json

# Shows checklist:
# [ ] Analyze requirements
# [ ] Identify systems needed
# [ ] Design containers
# [ ] Define relationships
# [ ] Assign criticality levels
# [ ] Generate C4 model
# Proceed? [y/N]: y

# 3. Generate infrastructure
saat generate-terraform --model architecture.json --provider aws --auto-approve
```

### In Claude Code
```
You: I have a requirements doc in docs/PRD.md. Help me design the architecture.

Claude: I'll use SAAT to analyze your requirements.
[Uses discover_requirements tool]

Found:
- 12 functional requirements
- 5 user stories
- 3 technical constraints (99.9% uptime, GDPR compliance, < 200ms latency)

Based on this, I recommend:
- Microservices architecture (3 services)
- PostgreSQL database (encrypted)
- Redis cache (for performance)
- API Gateway pattern

Would you like me to:
1. Generate the complete C4 model?
2. Validate against your constraints?
3. Generate Terraform for AWS?
```

---

## 🚀 Implementation Priority

### Immediate (Next Session)
1. ✅ Requirements models (DONE)
2. ✅ Checklist models (DONE)
3. 📋 Base agent with checklist support
4. 📋 Requirements discovery agent
5. 📋 Update CLI with --auto-approve
6. 📋 Validation agent

### Next Week
7. Documentation agent
8. Security agent
9. Terraform agent (AWS first)
10. MCP server

### Future
11. Terraform agent (Azure, GCP)
12. Fitness function agent
13. Architecture advisor agent
14. Web UI

---

## 🧪 Testing Strategy

Each agent should have:
1. Unit tests for checklist generation
2. Integration tests with approval system
3. End-to-end tests with sample projects
4. MCP integration tests

Example test:
```python
async def test_validation_agent_with_checklist():
    agent = ValidationAgent()

    # Should generate checklist
    checklist = await agent.create_checklist(model)
    assert len(checklist.items) > 0

    # Should execute with auto-approve
    result = await agent.execute(model, auto_approve=True)
    assert all(item.completed for item in result.checklist.items)
```

---

## 📝 Notes

- All agents follow the same pattern: checklist → approval → execution
- Checklists are saved to JSON for auditability
- Auto-approve mode essential for CI/CD integration
- MCP server enables seamless Claude Code experience
- Equal focus on greenfield (requirements → design) and brownfield (code → discovery)

---

**Last Updated**: 2025-10-31
**Status**: Phase 2 in progress, Phase 3-5 ready for implementation
