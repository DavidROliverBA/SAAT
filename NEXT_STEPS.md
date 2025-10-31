# SAAT - Next Steps for Completion

## ✅ What's Been Completed

### Phase 1: Core Framework (100%)
- ✅ Python/PydanticAI migration
- ✅ Pydantic models for C4 architecture
- ✅ Discovery Agent (brownfield)
- ✅ Generator Agent
- ✅ Context Broker
- ✅ CLI (5 commands)
- ✅ SAATClient API

### Phase 2: Greenfield & Checklist System (75%)
- ✅ Requirements models (ProjectRequirements, Requirement, UserStory, etc.)
- ✅ Checklist models (AgentChecklist, ChecklistItem, ApprovalRequest/Response)
- ✅ **BaseAgentWithChecklist** class (213 lines)
  - Checklist generation
  - Interactive approval with auto-approve
  - Progress tracking and display
  - Template for all agents
- ✅ **RequirementsAgent** (308 lines)
  - Reads markdown/text requirement docs
  - Extracts functional/non-functional requirements
  - Parses user stories and constraints
  - Generates structured ProjectRequirements.json
- ✅ **ValidationAgent** (260 lines)
  - Structural integrity validation
  - Compliance checking (PCI-DSS, HIPAA, GDPR)
  - Best practices enforcement
  - Generates ValidationResult with actionable suggestions

---

## 🚧 Remaining Work

### 1. Documentation Agent (saat/agents/documentation.py)

```python
class DocumentationAgent(BaseAgentWithChecklist):
    """Generate documentation from C4 models."""

    async def generate_documentation(
        self,
        model: C4Model,
        output_dir: str,
        formats: list[str] = ["markdown"],  # markdown, plantum, mermaid, confluence
        auto_approve: bool = False
    ) -> dict:
        """Generate comprehensive documentation.

        Checklist items:
        1. Load C4 model
        2. Generate markdown overview
        3. Create system context diagrams (PlantUML/Mermaid)
        4. Create container diagrams
        5. Create component diagrams
        6. Generate ADRs (Architecture Decision Records)
        7. Create deployment documentation
        8. (Optional) Publish to Confluence
        """
```

**Tools needed**:
- Markdown template generation
- PlantUML/Mermaid diagram generation
- ADR template generation

---

### 2. Security Agent (saat/agents/security.py)

```python
class SecurityAgent(BaseAgentWithChecklist):
    """Analyze security posture from C4 models."""

    async def analyze_security(
        self,
        model: C4Model,
        threat_model: bool = True,
        auto_approve: bool = False
    ) -> dict:
        """Analyze security posture.

        Checklist items:
        1. Load C4 model
        2. Identify unencrypted communications
        3. Check authentication mechanisms
        4. Analyze data flows for sensitive data
        5. Identify missing security controls
        6. Check compliance with security frameworks
        7. Generate threat model (if requested)
        8. Create security report with recommendations
        """
```

**Checks**:
- Unencrypted interfaces
- Missing authentication
- Sensitive data flows
- Access controls
- Logging and monitoring

---

### 3. Terraform Agent (saat/agents/terraform.py)

```python
class TerraformAgent(BaseAgentWithChecklist):
    """Generate infrastructure-as-code from C4 models."""

    async def generate_terraform(
        self,
        model: C4Model,
        provider: str = "aws",  # aws, azure, gcp
        output_dir: str = "infrastructure/",
        auto_approve: bool = False
    ) -> dict:
        """Generate Terraform configuration.

        Checklist items:
        1. Load C4 model
        2. Map containers to cloud resources
        3. Generate VPC/network configuration
        4. Create database resources (based on criticality)
        5. Set up load balancers
        6. Configure auto-scaling (CS1/CS2 get auto-scaling)
        7. Set up monitoring and alerting
        8. Generate backup configurations (CS1 = 35 days, CS2 = 7 days)
        9. Create IAM roles and policies
        10. Generate terraform files (main.tf, variables.tf, outputs.tf)
        """
```

**Criticality-based configs**:
- CS1: Multi-AZ, auto-scaling, 35-day backups, monitoring
- CS2: Multi-AZ, 7-day backups, monitoring
- SL1/SL2: Single-AZ, basic monitoring
- STANDARD: Minimal config

---

### 4. Update CLI (saat/cli.py)

Add `--auto-approve` flag to all commands:

```python
@click.group()
@click.option('--auto-approve', '-y', is_flag=True, help='Skip approval prompts')
@click.option('--model', default="anthropic:claude-sonnet-4", envvar='SAAT_MODEL')
@click.pass_context
def main(ctx, auto_approve, model):
    ctx.obj['auto_approve'] = auto_approve
    ctx.obj['model'] = model

# Add new commands:

@main.command()
@click.option('--files', '-f', multiple=True, required=True)
@click.option('--project-name', '-n')
@click.option('--output', '-o', default='requirements.json')
@click.pass_context
def discover_requirements(ctx, files, project_name, output):
    """Discover requirements from documents (greenfield)."""
    auto_approve = ctx.obj.get('auto_approve', False)
    # Use RequirementsAgent

@main.command()
@click.option('--model-file', '-m', required=True)
@click.option('--framework', '-f', help='Compliance framework')
@click.option('--output', '-o', default='validation-report.json')
@click.pass_context
def validate_model(ctx, model_file, framework, output):
    """Validate C4 model against standards."""
    auto_approve = ctx.obj.get('auto_approve', False)
    # Use ValidationAgent

@main.command()
@click.option('--model-file', '-m', required=True)
@click.option('--output-dir', '-o', default='docs/')
@click.option('--format', '-f', multiple=True, default=['markdown'])
@click.pass_context
def generate_docs(ctx, model_file, output_dir, format):
    """Generate documentation from C4 model."""
    # Use DocumentationAgent

@main.command()
@click.option('--model-file', '-m', required=True)
@click.option('--output', '-o', default='security-report.json')
@click.pass_context
def security_scan(ctx, model_file, output):
    """Analyze security posture."""
    # Use SecurityAgent

@main.command()
@click.option('--model-file', '-m', required=True)
@click.option('--provider', '-p', default='aws', type=click.Choice(['aws', 'azure', 'gcp']))
@click.option('--output-dir', '-o', default='infrastructure/')
@click.pass_context
def generate_terraform(ctx, model_file, provider, output_dir):
    """Generate Terraform infrastructure."""
    # Use TerraformAgent
```

---

### 5. Update Agents Init (saat/agents/__init__.py)

```python
from saat.agents.base import BaseAgentWithChecklist
from saat.agents.discovery import DiscoveryAgent, create_discovery_agent
from saat.agents.generator import GeneratorAgent, create_generator_agent
from saat.agents.requirements import RequirementsAgent, discover_requirements
from saat.agents.validation import ValidationAgent, validate_c4_model
# from saat.agents.documentation import DocumentationAgent
# from saat.agents.security import SecurityAgent
# from saat.agents.terraform import TerraformAgent

__all__ = [
    "BaseAgentWithChecklist",
    "DiscoveryAgent",
    "create_discovery_agent",
    "GeneratorAgent",
    "create_generator_agent",
    "RequirementsAgent",
    "discover_requirements",
    "ValidationAgent",
    "validate_c4_model",
    # Add others as implemented
]
```

---

### 6. MCP Server (saat_mcp_server.py)

Create in root directory:

```python
#!/usr/bin/env python3
"""MCP Server for SAAT - Integrates with Claude Code."""

import asyncio
import json
import sys
from pathlib import Path

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from saat import SAATClient
from saat.agents.requirements import RequirementsAgent
from saat.agents.validation import ValidationAgent

server = Server("saat-architecture")
saat_client = SAATClient()

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="discover_architecture",
            description="Analyze repository to discover architecture",
            inputSchema={
                "type": "object",
                "properties": {
                    "repo_path": {"type": "string"},
                    "max_depth": {"type": "integer", "default": 3}
                },
                "required": ["repo_path"]
            }
        ),
        Tool(
            name="discover_requirements",
            description="Extract requirements from documents for greenfield projects",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_paths": {"type": "array", "items": {"type": "string"}},
                    "project_name": {"type": "string"}
                },
                "required": ["file_paths"]
            }
        ),
        Tool(
            name="generate_c4_model",
            description="Generate C4 architecture model",
            inputSchema={
                "type": "object",
                "properties": {
                    "repo_path": {"type": "string"},
                    "requirements_file": {"type": "string"}
                }
            }
        ),
        Tool(
            name="validate_model",
            description="Validate C4 model against standards",
            inputSchema={
                "type": "object",
                "properties": {
                    "model_file": {"type": "string"},
                    "framework": {"type": "string"}
                },
                "required": ["model_file"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    # All tools use auto_approve=True for MCP integration

    if name == "discover_architecture":
        discovery, model = await saat_client.analyze(
            arguments["repo_path"],
            # Note: auto_approve not yet in SAATClient, needs update
        )
        return [TextContent(
            type="text",
            text=f"""Architecture discovered:

Technologies: {', '.join(discovery.technologies)}
Patterns: {', '.join([p.pattern for p in discovery.patterns])}
Systems: {len(model.systems)}
Containers: {len(model.containers)}
"""
        )]

    # Implement other tools...

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
```

**Claude Code Config** (~/.config/claude/config.json):
```json
{
  "mcpServers": {
    "saat": {
      "command": "python",
      "args": ["/path/to/SAAT/saat_mcp_server.py"],
      "env": {
        "ANTHROPIC_API_KEY": "${env:ANTHROPIC_API_KEY}"
      }
    }
  }
}
```

---

### 7. Example: Greenfield Project (examples/greenfield_project.py)

```python
#!/usr/bin/env python3
"""Example: Greenfield project from requirements to infrastructure."""

import asyncio
from pathlib import Path

from saat.agents.requirements import RequirementsAgent
from saat.agents.generator import GeneratorAgent
from saat.agents.validation import ValidationAgent
# from saat.agents.terraform import TerraformAgent

async def main():
    """Complete greenfield workflow."""

    print("🏗️  SAAT Greenfield Project Example\n")

    # Step 1: Discover requirements
    print("Step 1: Discovering requirements from PRD...")
    req_agent = RequirementsAgent()
    req_result = await req_agent.discover_requirements(
        file_paths=["docs/PRD.md", "docs/tech-constraints.md"],
        project_name="Payment Platform",
        auto_approve=True  # For demo
    )
    requirements = req_result["requirements"]
    print(f"✅ Found {len(requirements.requirements)} requirements")

    # Save
    Path("requirements.json").write_text(requirements.model_dump_json(indent=2))

    # Step 2: Generate architecture from requirements
    print("\nStep 2: Generating architecture from requirements...")
    # This would use a new method in GeneratorAgent
    # model = await gen_agent.generate_from_requirements(requirements)

    # Step 3: Validate
    print("\nStep 3: Validating architecture...")
    val_agent = ValidationAgent()
    val_result = await val_agent.validate_model(
        model=model,
        framework="PCI-DSS",
        auto_approve=True
    )
    print(f"✅ Validation score: {val_result['validation'].score}/100")

    # Step 4: Generate infrastructure
    print("\nStep 4: Generating Terraform...")
    # tf_agent = TerraformAgent()
    # await tf_agent.generate_terraform(model, "aws", auto_approve=True)

    print("\n✨ Greenfield project complete!")

if __name__ == "__main__":
    asyncio.run(main())
```

---

### 8. Sample Requirements Doc (examples/requirements.md)

```markdown
# Payment Processing Platform - Requirements

## Functional Requirements

### REQ-F-001: Process Payments
The system must process credit card payments securely using PCI-DSS compliant methods.

**Acceptance Criteria**:
- Support Visa, Mastercard, Amex
- Process payments within 3 seconds
- Return transaction ID to user

### REQ-F-002: Fraud Detection
The system must detect and block fraudulent transactions in real-time.

**Acceptance Criteria**:
- ML-based fraud scoring
- Block transactions with risk score > 0.8
- Log all decisions for audit

## Non-Functional Requirements

### REQ-NF-001: Availability
The system must maintain 99.9% uptime.

### REQ-NF-002: Performance
API response time must be < 200ms (95th percentile).

### REQ-NF-003: Security
All payment data must be encrypted in transit and at rest.

## User Stories

### US-001: Process Payment
**As a** customer
**I want** to pay with my credit card securely
**So that** I can complete my purchase quickly

**Acceptance Criteria**:
- Payment form loads in < 1 second
- Card number is masked
- Success/failure message shown immediately

## Technical Constraints

### CONST-001: Compliance
Must comply with PCI-DSS Level 1 requirements.

### CONST-002: Technology Stack
Must use Python and PostgreSQL for compatibility with existing systems.

### CONST-003: Cloud Provider
Must deploy on AWS for cost optimization.

## Stakeholders

- **Product Manager**: Needs fast feature delivery
- **Security Team**: Requires PCI-DSS compliance
- **Customers**: Need reliable, fast payments
- **Operations**: Need easy deployment and monitoring
```

---

## 🎯 Implementation Order

1. ✅ Base agent with checklist support
2. ✅ Requirements agent
3. ✅ Validation agent
4. ⏳ Documentation agent (2-3 hours)
5. ⏳ Security agent (2-3 hours)
6. ⏳ Terraform agent (3-4 hours)
7. ⏳ Update CLI with new commands (1-2 hours)
8. ⏳ MCP server (2-3 hours)
9. ⏳ Examples and testing (1-2 hours)

**Total remaining**: ~15-20 hours of development

---

## 🚀 Quick Commands After Completion

### Brownfield (Existing Code)
```bash
# Interactive
saat analyze --path /repo
# Auto mode
saat analyze --path /repo --auto-approve
```

### Greenfield (From Scratch)
```bash
# Step 1: Extract requirements
saat discover-requirements -f docs/PRD.md -n "Payment Platform" -o requirements.json

# Step 2: Generate architecture
saat generate-from-requirements --requirements requirements.json -o architecture.json

# Step 3: Validate
saat validate-model -m architecture.json -f PCI-DSS

# Step 4: Generate docs
saat generate-docs -m architecture.json -o docs/ -f markdown -f plantuml

# Step 5: Generate infrastructure
saat generate-terraform -m architecture.json -p aws -o infrastructure/

# All in one (auto mode)
saat greenfield-pipeline -f docs/PRD.md -n "Payment Platform" --auto-approve
```

### In Claude Code
```
You: I have a PRD in docs/requirements.md. Design the complete architecture.

Claude: [Uses SAAT MCP tools with auto-approve]

I've analyzed your requirements and generated:
1. Complete C4 model (3 systems, 8 containers)
2. Validation report (98/100 score, 2 warnings)
3. Security analysis (3 recommendations)
4. AWS Terraform configuration

Would you like me to show you any specific part?
```

---

## 📝 Testing Checklist

- [ ] Base agent checklist workflow
- [ ] Requirements discovery from markdown
- [ ] Validation with PCI-DSS/HIPAA
- [ ] Documentation generation
- [ ] Security analysis
- [ ] Terraform generation (AWS)
- [ ] CLI with --auto-approve
- [ ] MCP server integration
- [ ] End-to-end greenfield workflow
- [ ] End-to-end brownfield workflow

---

**Last Updated**: 2025-10-31
**Status**: 3/6 agents complete, CLI updates and MCP server pending
