# SAAT - Solution Architecture Agent Toolkit

<p align="center">
  <strong>🤖 AI-Powered C4 Architecture Discovery, Analysis & Infrastructure Generation</strong>
</p>

<p align="center">
  Complete architecture toolkit: Analyze existing code, extract requirements, validate compliance, analyze security, generate documentation, and create infrastructure-as-code using specialized AI agents powered by PydanticAI
</p>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Core Concepts](#-core-concepts)
- [Workflows](#-workflows)
  - [Brownfield (Existing Code)](#brownfield-existing-code-analysis)
  - [Greenfield (From Scratch)](#greenfield-from-scratch-design)
- [Available Agents](#-available-agents)
- [CLI Commands](#-cli-commands)
- [bac4-standalone Integration](#-bac4-standalone-visual-editor-integration)
- [Claude Code Integration](#-claude-code-integration-mcp)
- [Model Support](#-model-support)
- [Examples](#-examples)
- [Architecture](#-architecture)

---

## 🎯 Overview

SAAT is a **complete architecture toolkit** powered by PydanticAI that supports the entire software architecture lifecycle:

- **Discover** architecture from existing codebases (brownfield)
- **Extract** requirements from documents (greenfield)
- **Generate** C4 models automatically
- **Validate** against compliance frameworks (PCI-DSS, HIPAA, GDPR, SOC2)
- **Analyze** security posture and generate threat models
- **Generate** comprehensive documentation (Markdown, PlantUML, Mermaid, ADRs)
- **Create** production-ready infrastructure-as-code (Terraform for AWS/Azure/GCP)
- **Visualize** with bac4-standalone C4 editor integration

### Key Features

✅ **6 Specialized AI Agents** - Each with checklist workflow and approval system
✅ **Brownfield & Greenfield** - Analyze existing code OR design from requirements
✅ **Structurizr JSON Standard** - Industry-standard format for C4 models
✅ **bac4-standalone Integration** - Visual editing with round-trip conversion
✅ **Human-in-the-Loop** - Interactive approval with auto-approve mode
✅ **Multi-Model Support** - Claude, GPT-4, Gemini, Ollama
✅ **Claude Code MCP** - Seamless integration with Claude Code
✅ **Production Ready** - Retry logic, streaming, error handling
✅ **Type-Safe** - Pydantic models ensure correctness

### Why SAAT?

Traditional architecture tools require manual diagram creation and maintenance. SAAT **automates** the entire process:

```
Traditional:                           SAAT:
┌─────────────────┐                   ┌─────────────────┐
│ Manual Analysis │                   │ AI Analyzes     │
│ (days/weeks)    │                   │ (minutes)       │
└─────────────────┘                   └─────────────────┘
         ↓                                      ↓
┌─────────────────┐                   ┌─────────────────┐
│ Draw Diagrams   │                   │ Auto-Generate   │
│ (hours)         │                   │ C4 Models       │
└─────────────────┘                   └─────────────────┘
         ↓                                      ↓
┌─────────────────┐                   ┌─────────────────┐
│ Write Docs      │                   │ Validate &      │
│ (days)          │                   │ Document        │
└─────────────────┘                   └─────────────────┘
         ↓                                      ↓
┌─────────────────┐                   ┌─────────────────┐
│ Manual Updates  │                   │ Generate        │
│ (ongoing pain)  │                   │ Infrastructure  │
└─────────────────┘                   └─────────────────┘
```

---

## 🚀 Quick Start

### Brownfield: Analyze Existing Code

```bash
# 1. Install SAAT
pip install -e .

# 2. Set API key
export ANTHROPIC_API_KEY="your-key"

# 3. Analyze your codebase
saat analyze --path /path/to/your/code -o architecture.json

# 4. Validate against PCI-DSS
saat validate-model -m architecture.json -f PCI-DSS

# 5. Generate AWS infrastructure
saat generate-terraform -m architecture.json -p aws -o infrastructure/

# 6. Generate documentation
saat generate-docs -m architecture.json -f markdown -f plantuml -o docs/
```

### Greenfield: Design from Requirements

```bash
# 1. Extract requirements from PRD
saat discover-requirements -f docs/requirements.md -n "Payment Platform" -o requirements.json

# 2. Generate architecture (manual or from template)
# TODO: saat generate-from-requirements --requirements requirements.json -o architecture.json

# 3. Export for visual editing
saat export-structurizr -m architecture.json -o structurizr.json

# 4. Open bac4-standalone → Import → Edit → Export

# 5. Import refined model
saat import-structurizr -s structurizr.json -o architecture-final.json

# 6. Generate everything
saat validate-model -m architecture-final.json -f HIPAA
saat security-scan -m architecture-final.json --threat-model
saat generate-terraform -m architecture-final.json -p aws
```

---

## 📦 Installation

### Prerequisites

- Python 3.11+
- API key for Claude, GPT-4, or other supported models

### Option 1: pip (Recommended)

```bash
git clone https://github.com/DavidROliverBA/SAAT.git
cd SAAT
pip install -e .

# Or with all extras
pip install -e ".[all]"  # Logfire, OpenAI, Gemini support
```

### Option 2: Poetry

```bash
git clone https://github.com/DavidROliverBA/SAAT.git
cd SAAT
poetry install
```

### Environment Setup

```bash
# Create .env file
cp .env.example .env

# Add your API keys
echo "ANTHROPIC_API_KEY=your-key-here" >> .env

# Optional: Choose default model
echo "SAAT_MODEL=anthropic:claude-sonnet-4" >> .env
```

### Verify Installation

```bash
saat --version
saat info
```

---

## 🧠 Core Concepts

### C4 Model

SAAT uses the [C4 model](https://c4model.com) for software architecture:

- **Level 1 - System Context**: High-level systems and external dependencies
- **Level 2 - Container**: Applications, databases, microservices
- **Level 3 - Component**: Code-level modules and services
- **Level 4 - Code**: Classes and functions (future)

### Criticality Levels

SAAT assigns criticality to guide infrastructure decisions:

| Level | Uptime | Infrastructure | Use Case |
|-------|--------|---------------|----------|
| **CS1** | 99.99% | Multi-AZ, auto-scaling 2-10, 35d backups | Mission critical (payments, auth) |
| **CS2** | 99.9% | Multi-AZ, auto-scaling 2-5, 7d backups | Business critical (APIs, databases) |
| **SL1** | 99.5% | Single-AZ, basic monitoring, 3d backups | Standard services |
| **SL2** | 99% | Single-AZ, minimal config, 3d backups | Internal tools |
| **STANDARD** | Best effort | Minimal, no backups | Development, testing |

### Checklist Workflow

All agents follow a consistent workflow:

```
1. Generate Checklist → 2. Show to User → 3. Request Approval → 4. Execute Tasks
```

**Interactive Mode** (default):
```bash
saat validate-model -m architecture.json

📋 ValidationAgent Checklist:
  [ ] Load and parse C4 model
  [ ] Check structural integrity
  [ ] Validate relationships
  [ ] Check completeness
  [ ] Verify criticality assignments

Proceed? [y/N]: y
```

**Auto-Approve Mode**:
```bash
saat -y validate-model -m architecture.json
# or
saat --auto-approve validate-model -m architecture.json
```

---

## 🔄 Workflows

### Brownfield: Existing Code Analysis

Analyze an existing codebase to generate architecture models:

```bash
# Step 1: Discovery
saat discover --path /my-app --output discovery.json

# Step 2: Generate C4 Model
saat generate --discovery discovery.json --output architecture.json

# Or do both in one command:
saat analyze --path /my-app --output architecture.json

# Step 3: Validate
saat validate-model -m architecture.json -f PCI-DSS -o validation.json

# Step 4: Security Analysis
saat security-scan -m architecture.json --threat-model -o security.json

# Step 5: Generate Documentation
saat generate-docs -m architecture.json -f markdown -f plantuml -o docs/

# Step 6: Generate Infrastructure
saat generate-terraform -m architecture.json -p aws -r us-east-1 -o infrastructure/
```

### Greenfield: From-Scratch Design

Design a new system from requirements:

```bash
# Step 1: Extract Requirements
saat discover-requirements \\
  -f docs/PRD.md \\
  -f docs/tech-requirements.md \\
  -n "Payment Processing Platform" \\
  -o requirements.json

# Output: requirements.json with:
# - Functional requirements (REQ-F-001, REQ-F-002, ...)
# - Non-functional requirements (REQ-NF-001: 99.9% uptime, ...)
# - User stories (US-001: As a customer, I want...)
# - Technical constraints (CONST-001: PCI-DSS, ...)
# - Stakeholders

# Step 2: Design Architecture
# TODO: Implement generate-from-requirements
# For now: Manually create or use templates

# Step 3: Validate & Refine (same as brownfield)
saat validate-model -m architecture.json -f PCI-DSS
saat security-scan -m architecture.json
saat generate-terraform -m architecture.json -p aws
```

### Round-Trip with bac4-standalone

Combine AI analysis with visual editing:

```bash
# 1. Generate with SAAT
saat analyze --path /my-app -o architecture.json

# 2. Export to Structurizr format
saat export-structurizr -m architecture.json -o structurizr.json

# 3. Edit visually in bac4-standalone
# - Import structurizr.json
# - Drag & drop to refine layout
# - Add missing elements
# - Clarify relationships
# - Export as structurizr-refined.json

# 4. Import back to SAAT
saat import-structurizr -s structurizr-refined.json -o architecture-refined.json

# 5. Generate infrastructure from refined model
saat generate-terraform -m architecture-refined.json -p aws
```

---

## 🤖 Available Agents

### 1. Discovery Agent (Brownfield)
**Purpose**: Analyze existing codebases to discover architecture

```python
from saat.agents import DiscoveryAgent

agent = DiscoveryAgent()
discovery = await agent.analyze_repository("/path/to/repo", max_depth=3)

# Discovers:
# - Technologies used
# - Architectural patterns (microservices, MVC, etc.)
# - Services and components
# - Dependencies
```

### 2. Generator Agent
**Purpose**: Generate C4 models from discovery results

```python
from saat.agents import GeneratorAgent

agent = GeneratorAgent()
model = await agent.generate_model(discovery, business_context)

# Generates:
# - System Context diagrams
# - Container diagrams
# - Component diagrams
# - Relationships
```

### 3. Requirements Agent (Greenfield)
**Purpose**: Extract requirements from documents

```python
from saat.agents import RequirementsAgent

agent = RequirementsAgent()
result = await agent.discover_requirements(
    file_paths=["docs/PRD.md", "docs/tech-spec.md"],
    project_name="Payment Platform",
    auto_approve=False  # Interactive mode
)

# Extracts:
# - Functional requirements (REQ-F-001, ...)
# - Non-functional requirements (performance, security, ...)
# - User stories (As a... I want... So that...)
# - Technical constraints (compliance, technology choices, ...)
# - Stakeholders
```

### 4. Validation Agent
**Purpose**: Validate C4 models against standards

```python
from saat.agents import ValidationAgent

agent = ValidationAgent()
result = await agent.validate_model(
    model=c4_model,
    framework="PCI-DSS",  # or HIPAA, GDPR, SOC2
    auto_approve=True
)

# Validates:
# - Structural integrity (no orphaned elements)
# - Relationship consistency
# - Completeness
# - Compliance with frameworks
# - Best practices
```

### 5. Documentation Agent
**Purpose**: Generate comprehensive documentation

```python
from saat.agents import DocumentationAgent

agent = DocumentationAgent()
result = await agent.generate_documentation(
    model=c4_model,
    output_dir="docs/",
    formats=["markdown", "plantuml", "mermaid", "adr"],
    auto_approve=False
)

# Generates:
# - Markdown overview
# - PlantUML C4 diagrams
# - Mermaid diagrams
# - Architecture Decision Records (ADRs)
```

### 6. Security Agent
**Purpose**: Analyze security posture

```python
from saat.agents import SecurityAgent

agent = SecurityAgent()
result = await agent.analyze_security(
    model=c4_model,
    threat_model=True,
    output_file="security-report.json",
    auto_approve=False
)

# Analyzes:
# - Unencrypted communications
# - Missing authentication
# - Sensitive data exposure
# - Access controls
# - Compliance violations
# - Threat modeling (STRIDE)
```

### 7. Terraform Agent
**Purpose**: Generate infrastructure-as-code

```python
from saat.agents import TerraformAgent

agent = TerraformAgent()
result = await agent.generate_terraform(
    model=c4_model,
    provider="aws",  # or azure, gcp
    region="us-east-1",
    output_dir="infrastructure/",
    auto_approve=False
)

# Generates:
# - main.tf (resources based on criticality)
# - variables.tf
# - outputs.tf
# - terraform.tfvars.example
# - Multi-AZ for CS1/CS2
# - Auto-scaling based on criticality
# - Backups (35d for CS1, 7d for CS2, 3d for SL1/SL2)
```

---

## 🖥️ CLI Commands

### Analysis Commands

```bash
# Discover architecture from code
saat discover --path /repo --output discovery.json [--max-depth 3]

# Generate C4 model from discovery
saat generate --discovery discovery.json --output architecture.json

# Full analysis (discover + generate)
saat analyze --path /repo --output architecture.json [--business-context context.json]
```

### Requirements (Greenfield)

```bash
# Extract requirements from documents
saat discover-requirements \\
  -f docs/PRD.md \\
  -f docs/constraints.md \\
  -n "Project Name" \\
  -o requirements.json
```

### Validation

```bash
# Validate C4 model
saat validate-model -m architecture.json -o validation-report.json

# Validate with compliance framework
saat validate-model -m architecture.json -f PCI-DSS
saat validate-model -m architecture.json -f HIPAA
saat validate-model -m architecture.json -f GDPR
```

### Security

```bash
# Security analysis
saat security-scan -m architecture.json -o security-report.json

# Include threat modeling
saat security-scan -m architecture.json --threat-model
```

### Documentation

```bash
# Generate documentation (multiple formats)
saat generate-docs -m architecture.json -f markdown -f plantuml -o docs/

# All formats
saat generate-docs -m architecture.json \\
  -f markdown \\
  -f plantuml \\
  -f mermaid \\
  -f adr \\
  -o docs/
```

### Infrastructure

```bash
# Generate Terraform for AWS
saat generate-terraform -m architecture.json -p aws -r us-east-1 -o infrastructure/

# Generate for Azure
saat generate-terraform -m architecture.json -p azure -r eastus -o infrastructure/

# Generate for GCP
saat generate-terraform -m architecture.json -p gcp -r us-central1 -o infrastructure/
```

### Structurizr Integration

```bash
# Export to Structurizr JSON
saat export-structurizr -m architecture.json -o structurizr.json

# Import from Structurizr JSON
saat import-structurizr -s structurizr.json -o architecture.json
```

### Global Options

```bash
# Auto-approve mode (skip all prompts)
saat -y validate-model -m architecture.json
saat --auto-approve generate-docs -m architecture.json

# Use different model
saat --model openai:gpt-4 analyze --path /repo

# Set model via environment
export SAAT_MODEL="openai:gpt-4"
saat analyze --path /repo
```

### Utility Commands

```bash
# Show version and configuration
saat info

# Get help
saat --help
saat analyze --help
```

---

## 🎨 bac4-standalone Visual Editor Integration

SAAT integrates with [bac4-standalone](https://github.com/DavidROliverBA/bac4-standalone) using the industry-standard **Structurizr JSON** format.

### Why Integrate?

- **SAAT**: AI-powered analysis, validation, security, infrastructure generation
- **bac4-standalone**: Interactive visual editing, drag-and-drop, real-time layout
- **Together**: Best of both worlds - AI + human refinement

### Complete Workflow

```
┌──────────────┐                    ┌─────────────────┐                    ┌──────────────┐
│              │  Structurizr JSON  │                 │  Structurizr JSON  │              │
│     SAAT     │ ───────────────►   │  bac4-standalone│ ───────────────►   │     SAAT     │
│  (Analysis)  │                    │   (Visual Edit) │                    │ (Infra Gen)  │
└──────────────┘                    └─────────────────┘                    └──────────────┘
```

### Example

```bash
# 1. Analyze code with SAAT
saat analyze --path /my-payment-app -o architecture.json

# 2. Export to Structurizr
saat export-structurizr -m architecture.json -o structurizr.json

# 3. Open bac4-standalone (web browser)
#    → Import structurizr.json
#    → Visually refine diagram
#    → Export as structurizr-refined.json

# 4. Import refined model
saat import-structurizr -s structurizr-refined.json -o architecture-refined.json

# 5. Generate infrastructure from refined model
saat generate-terraform -m architecture-refined.json -p aws -o infrastructure/

# 6. Deploy!
cd infrastructure/
terraform init
terraform plan
terraform apply
```

### Data Preservation

SAAT's rich metadata (criticality levels, interfaces, responsibilities) is preserved in the `properties` field during round-trip conversion.

**See**: [BAC4_INTEGRATION.md](BAC4_INTEGRATION.md) for complete guide.

---

## 🔌 Claude Code Integration (MCP)

SAAT provides a Model Context Protocol (MCP) server for seamless Claude Code integration.

### Setup

1. **Add to Claude Code config** (`~/.config/claude/config.json`):

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

2. **Restart Claude Code**

3. **Use SAAT tools in Claude Code**:

```
You: I have a PRD in docs/requirements.md. Design the complete architecture.

Claude: I'll use SAAT to analyze your requirements and generate the architecture.
[Uses discover_requirements tool]
[Uses generate_c4_model tool]
[Uses validate_model tool with PCI-DSS]
[Uses security_scan tool]
[Uses generate_terraform tool for AWS]

I've created:
- Complete C4 architecture model (3 systems, 8 containers, 15 components)
- Validation report: 98/100 (2 minor warnings)
- Security analysis: 3 recommendations
- AWS Terraform configuration (ready to deploy)

Would you like me to show you any specific part?
```

### Available MCP Tools

- `discover_architecture` - Analyze repository
- `discover_requirements` - Extract requirements from documents
- `generate_c4_model` - Generate architecture model
- `validate_model` - Validate against standards
- `analyze_security` - Security analysis
- `generate_documentation` - Create docs
- `generate_terraform` - Infrastructure-as-code
- `full_analysis` - Complete end-to-end workflow

All tools use `auto_approve=True` for seamless integration.

---

## 🎛️ Model Support

SAAT supports multiple AI models via PydanticAI:

### Anthropic Claude (Default)

```bash
export ANTHROPIC_API_KEY="your-key"
saat --model anthropic:claude-sonnet-4 analyze --path /repo
# or
saat --model anthropic:claude-opus-4 analyze --path /repo
```

### OpenAI

```bash
export OPENAI_API_KEY="your-key"
saat --model openai:gpt-4 analyze --path /repo
# or
saat --model openai:gpt-4-turbo analyze --path /repo
```

### Google Gemini

```bash
export GEMINI_API_KEY="your-key"
saat --model gemini:gemini-1.5-pro analyze --path /repo
```

### Local Models (Ollama)

```bash
# Start Ollama
ollama serve

# Pull model
ollama pull llama3.1

# Use with SAAT
saat --model ollama:llama3.1 analyze --path /repo
```

### Set Default Model

```bash
# Via environment variable
export SAAT_MODEL="anthropic:claude-sonnet-4"

# Via .env file
echo "SAAT_MODEL=anthropic:claude-sonnet-4" >> .env
```

---

## 💡 Examples

### Example 1: Brownfield - Analyze Payment App

```bash
cd /my-payment-app

# Analyze
saat analyze --path . -o architecture.json

# Validate PCI-DSS compliance
saat validate-model -m architecture.json -f PCI-DSS -o validation.json

# Security scan
saat security-scan -m architecture.json --threat-model -o security.json

# Generate AWS infrastructure with compliance
saat generate-terraform -m architecture.json -p aws -o infrastructure/

# Output:
# ✅ architecture.json (C4 model)
# ✅ validation.json (PCI-DSS compliance report)
# ✅ security.json (Security issues + threat model)
# ✅ infrastructure/ (Terraform with proper encryption, network isolation)
```

### Example 2: Greenfield - Design E-Commerce Platform

```bash
# Extract requirements
saat discover-requirements \\
  -f docs/product-requirements.md \\
  -f docs/technical-constraints.md \\
  -n "E-Commerce Platform" \\
  -o requirements.json

# Review extracted requirements
cat requirements.json | python -m json.tool

# Export for visual design (manual creation for now)
# TODO: saat generate-from-requirements

# Validate
saat validate-model -m architecture.json -f GDPR

# Generate complete stack
saat generate-docs -m architecture.json -f markdown -f plantuml -o docs/
saat generate-terraform -m architecture.json -p aws -o infrastructure/
```

### Example 3: Round-Trip with Visual Editor

```bash
# Start with code analysis
saat analyze --path /my-microservices -o architecture.json

# Export to Structurizr
saat export-structurizr -m architecture.json -o structurizr.json

# Edit in bac4-standalone
# (Visual refinement, add missing systems, clarify relationships)

# Import refined model
saat import-structurizr -s structurizr-refined.json -o architecture-v2.json

# Validate changes
saat validate-model -m architecture-v2.json

# Regenerate infrastructure with changes
saat generate-terraform -m architecture-v2.json -p aws -o infrastructure-v2/
```

### Example 4: Full Automation

```bash
# Complete automated workflow
saat -y analyze --path /repo -o architecture.json
saat -y validate-model -m architecture.json -f PCI-DSS
saat -y security-scan -m architecture.json --threat-model
saat -y generate-docs -m architecture.json -f markdown -f plantuml
saat -y generate-terraform -m architecture.json -p aws

# All tasks run without prompts
```

---

## 🏛️ Architecture

```
SAAT/
├── saat/
│   ├── models.py              # Pydantic models (C4, Requirements, Checklists)
│   ├── structurizr.py         # Structurizr JSON models
│   ├── converters.py          # SAAT ↔ Structurizr conversion
│   ├── cli.py                 # Click CLI (12 commands)
│   ├── client.py              # High-level API
│   ├── broker.py              # Agent orchestration
│   ├── agents/
│   │   ├── base.py            # BaseAgentWithChecklist
│   │   ├── discovery.py       # Code analysis (brownfield)
│   │   ├── generator.py       # C4 model generation
│   │   ├── requirements.py    # Requirements extraction (greenfield)
│   │   ├── validation.py      # Compliance validation
│   │   ├── documentation.py   # Multi-format documentation
│   │   ├── security.py        # Security analysis & threat modeling
│   │   └── terraform.py       # Infrastructure-as-code generation
├── saat_mcp_server.py         # Claude Code MCP server
├── examples/
│   ├── quick_start.py         # Brownfield example
│   ├── greenfield_project.py  # Greenfield example
│   └── requirements.md        # Sample PRD
├── BAC4_INTEGRATION.md        # bac4-standalone integration guide
└── README.md                  # This file
```

---

## 📚 Documentation

- **[BAC4_INTEGRATION.md](BAC4_INTEGRATION.md)** - Complete guide for bac4-standalone integration
- **[IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md)** - Development roadmap
- **[NEXT_STEPS.md](NEXT_STEPS.md)** - Future enhancements
- **Examples**: See `examples/` directory

---

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) (TODO).

### Development Setup

```bash
git clone https://github.com/DavidROliverBA/SAAT.git
cd SAAT
poetry install
poetry run pytest  # Run tests (TODO)
```

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file

---

## 🙏 Acknowledgments

- **PydanticAI** - Agent framework
- **C4 Model** - Architecture visualization methodology
- **Structurizr** - JSON schema for C4 models
- **bac4-standalone** - Visual C4 editor

---

## 📞 Support

- **Issues**: https://github.com/DavidROliverBA/SAAT/issues
- **Discussions**: https://github.com/DavidROliverBA/SAAT/discussions

---

**Built with ❤️ using PydanticAI**
