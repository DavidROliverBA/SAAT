# SAAT - Solution Architecture Agent Toolkit

<p align="center">
  <img src="https://img.shields.io/badge/version-2.0.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/python-3.11+-green.svg" alt="Python">
  <img src="https://img.shields.io/badge/agents-9-brightgreen.svg" alt="Agents">
  <img src="https://img.shields.io/badge/license-MIT-orange.svg" alt="License">
  <img src="https://img.shields.io/badge/status-production%20ready-success.svg" alt="Status">
</p>

<p align="center">
  <strong>🤖 AI-Powered Software Architecture Analysis & Quality Assurance Platform</strong>
</p>

---

## 📋 Table of Contents

- [What is SAAT?](#-what-is-saat)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Usage Guides](#-usage-guides)
- [Core Concepts](#-core-concepts)
- [Available Agents](#-available-agents)
- [Documentation](#-documentation)
- [Examples](#-examples)
- [Contributing](#-contributing)
- [Appendix](#-appendix)

---

## 🎯 What is SAAT?

SAAT is an **AI-powered architecture quality assurance platform** that helps you:

1. **Analyze existing codebases** (brownfield) - Discover architecture automatically
2. **Design new systems** (greenfield) - Extract requirements and generate architecture
3. **Evaluate quality** - Score architecture against 14 standard characteristics
4. **Validate compliance** - Check against PCI-DSS, HIPAA, GDPR, SOC2
5. **Analyze security** - Identify vulnerabilities and generate threat models
6. **Generate documentation** - Create comprehensive docs in multiple formats
7. **Create infrastructure** - Generate production-ready Terraform for AWS/Azure/GCP

### Why SAAT?

Traditional architecture work is manual and time-consuming. SAAT **automates the entire process**:

```
Traditional Approach:          SAAT Approach:
┌─────────────────┐           ┌─────────────────┐
│ Manual Analysis │           │ /saat-discover  │
│ (days/weeks)    │           │ (minutes)       │
└─────────────────┘           └─────────────────┘
         ↓                             ↓
┌─────────────────┐           ┌─────────────────┐
│ Draw Diagrams   │           │ /saat-generate  │
│ (hours)         │           │ (automatic)     │
└─────────────────┘           └─────────────────┘
         ↓                             ↓
┌─────────────────┐           ┌─────────────────┐
│ Write Docs      │           │ /saat-analyze   │
│ (days)          │           │ (with scores)   │
└─────────────────┘           └─────────────────┘
```

### Key Features

✅ **9 Specialized AI Agents** - Discovery, Generation, Requirements, Quality Analysis, Validation, Security, Documentation, Infrastructure, Orchestration
✅ **Architecture Quality Analysis** - Evaluate against 14 characteristics (Mark Richards methodology)
✅ **Conversational Slash Commands** - Type `/saat-` in Claude Code for guided workflows
✅ **C4 Model Standard** - Industry-standard architecture diagrams
✅ **Multi-Model Support** - Claude, GPT-4, Gemini, Ollama
✅ **Human-in-the-Loop** - Interactive approval with auto-approve mode
✅ **Production Ready** - Retry logic, streaming, error handling

---

## 🚀 Quick Start

### The Easy Way: Claude Code Slash Commands (Recommended)

1. **Install SAAT and configure Claude Code**:
```bash
# Clone and install SAAT
git clone https://github.com/DavidROliverBA/SAAT.git
cd SAAT
pip install -e .

# Install Claude Code slash commands
./install-claude-commands.sh

# Set API key
export ANTHROPIC_API_KEY="your-key"
```

2. **Analyze an existing project** (Brownfield):
```
Open Claude Code in your project directory, then:

You: /saat-orchestrate

Claude: I'll help you analyze your architecture!
        What would you like to do?
        1. Analyze existing codebase (brownfield)
        2. Design new system (greenfield)
        3. Review specific architecture aspect

You: Analyze my existing codebase

Claude: [Runs discovery, generates C4 model, analyzes quality,
        validates compliance, checks security, generates docs]

        ✅ Complete analysis finished!

        📊 Results Summary:
        - Architecture Model: 5 systems, 12 containers, 28 components
        - Quality Score: 68/100 (Needs Improvement)
        - Compliance: 85/100 (PCI-DSS)
        - Security: 3 critical issues found
        - Documentation: Generated in docs/

        🚨 Top Priorities:
        1. Fix critical security issue: Unencrypted database connection
        2. Add load balancer for availability (currently 55/100)
        3. Implement auto-scaling for scalability

        Next: Would you like me to generate Terraform to deploy fixes?
```

3. **Design a new system** (Greenfield):
```
You: /saat-orchestrate

Claude: What would you like to do?

You: Design a new payment processing system

Claude: I'll guide you through designing your architecture.

        Do you have requirements documents? If so, please provide paths.
        Otherwise, I can help you capture requirements conversationally.

You: I have docs/requirements.md

Claude: [Extracts requirements, generates architecture, analyzes quality,
        validates, checks security, generates infrastructure]

        ✅ Architecture design complete!

        📊 Your New System:
        - 3 systems, 8 containers, 15 components
        - Quality Score: 82/100 (Good)
        - Compliance: PCI-DSS ready (98/100)
        - Security: All checks passed
        - Infrastructure: AWS Terraform ready to deploy

        Files created:
        - architecture.json (C4 model)
        - docs/ (comprehensive documentation)
        - infrastructure/ (Terraform IaC)

        You can now: terraform apply to deploy!
```

### Individual Commands

All commands are conversational and guide you step-by-step:

- `/saat-orchestrate` - **Start here!** Recommends what to do based on your needs
- `/saat-discover` - Analyze existing codebase
- `/saat-requirements` - Extract requirements from documents
- `/saat-generate` - Create architecture model
- `/saat-analyze-characteristics` - Evaluate architecture quality
- `/saat-validate` - Check compliance
- `/saat-security` - Analyze security
- `/saat-document` - Generate documentation
- `/saat-terraform` - Create infrastructure code
- `/saat-help` - Show all commands

**See**: [Complete Usage Guides](#-usage-guides) for detailed walkthroughs.

---

## 📦 Installation

### Step 1: Install SAAT

```bash
# Clone repository
git clone https://github.com/DavidROliverBA/SAAT.git
cd SAAT

# Install with pip
pip install -e .

# Or with all extras (Logfire, OpenAI, Gemini)
pip install -e ".[all]"

# Or with Poetry
poetry install
```

### Step 2: Set API Key

```bash
# Create .env file
cp .env.example .env

# Add your API key
echo "ANTHROPIC_API_KEY=your-key-here" >> .env

# Optional: Choose default model
echo "SAAT_MODEL=anthropic:claude-sonnet-4" >> .env
```

### Step 3: Configure Claude Code (Recommended)

**Option A: Install Slash Commands Globally** (Available in all projects)
```bash
./install-claude-commands.sh
```

**Option B: Per-Project** (Already available when you run Claude Code from SAAT directory)
```bash
# Commands are in .claude/commands/ - no installation needed!
```

**Configure MCP Server** (Required for slash commands to work):

Add to `~/.config/claude/config.json`:
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

Then restart Claude Code.

### Step 4: Verify Installation

```bash
# Check SAAT CLI
saat --version
saat info

# In Claude Code, type:
# /saat-help
# You should see all available commands
```

---

## 📖 Usage Guides

### For New Users: Start Here!

**The Orchestrator** (`/saat-orchestrate`) is your starting point. It will:
- Ask you what you want to do
- Recommend which agents to run
- Guide you through the entire process
- Keep you updated on progress
- Ask for help when it needs information

### Detailed Step-by-Step Guides

📘 **[Greenfield Guide](docs/GREENFIELD_GUIDE.md)** - Designing a new system from scratch
- Extract requirements from documents
- Generate architecture automatically
- Evaluate quality before building
- Generate deployment infrastructure
- Complete walkthrough with examples

📗 **[Brownfield Guide](docs/BROWNFIELD_GUIDE.md)** - Analyzing existing codebases
- Discover architecture from code
- Identify quality issues
- Check compliance and security
- Generate missing documentation
- Create infrastructure-as-code
- Complete walkthrough with examples

📙 **[Customization Guide](docs/CUSTOMIZATION_GUIDE.md)** - Tailor SAAT to your needs
- Customize agent behavior
- Add custom validation rules
- Create custom architecture characteristics
- Extend with your own patterns
- Build custom agents

---

## 🧠 Core Concepts

### The 9 Agents

SAAT uses specialized AI agents, each expert in one area:

1. **🎯 Orchestrator Agent** ⭐ **NEW** - Coordinates all other agents, creates plans, guides users
2. **🔍 Discovery Agent** - Analyzes codebases to discover architecture
3. **📋 Requirements Agent** - Extracts requirements from documents
4. **🏗️ Generator Agent** - Creates C4 architecture models
5. **📊 Architecture Characteristics Agent** - Evaluates quality against 14 standards
6. **✅ Validation Agent** - Validates compliance (PCI-DSS, HIPAA, GDPR, SOC2)
7. **🔒 Security Agent** - Analyzes security and creates threat models
8. **📚 Documentation Agent** - Generates docs (Markdown, PlantUML, Mermaid, ADRs)
9. **🏗️ Terraform Agent** - Creates infrastructure-as-code

### The C4 Model

SAAT uses the [C4 model](https://c4model.com) for architecture:

- **Level 1 - System Context**: High-level view of systems and external dependencies
- **Level 2 - Container**: Applications, databases, microservices
- **Level 3 - Component**: Code-level modules and services

### Architecture Characteristics

SAAT evaluates architecture against 14 standard characteristics from Mark Richards:

**Operational (7)**: Availability, Scalability, Performance, Security, Reliability, Fault Tolerance, Recoverability

**Structural (5)**: Maintainability, Testability, Deployability, Configurability, Extensibility

**Cross-Cutting (2)**: Interoperability, Usability

Each characteristic gets:
- **Score** (0-100)
- **Status** (Fully Compliant, Mostly Compliant, Partially Compliant, Non-Compliant)
- **Gap Analysis** with severity levels (critical, high, medium, low)
- **Recommendations** with implementation steps

### Criticality Levels

SAAT assigns criticality to guide infrastructure decisions:

| Level | Uptime | Infrastructure | Use Case |
|-------|--------|---------------|----------|
| **CS1** | 99.99% | Multi-AZ, auto-scaling 2-10, 35d backups | Mission critical (payments, auth) |
| **CS2** | 99.9% | Multi-AZ, auto-scaling 2-5, 7d backups | Business critical (APIs, databases) |
| **SL1** | 99.5% | Single-AZ, basic monitoring, 3d backups | Standard services |
| **SL2** | 99% | Single-AZ, minimal config, 3d backups | Internal tools |
| **STANDARD** | Best effort | Minimal, no backups | Development, testing |

---

## 🤖 Available Agents

### 1. 🎯 Orchestrator Agent ⭐ **NEW**

**Purpose**: Your AI architecture consultant that coordinates all other agents

The Orchestrator Agent is your primary interface to SAAT. It:
- **Understands your goals** through conversation
- **Recommends what to do** based on your situation
- **Creates a plan** and gets your approval
- **Coordinates agents** to execute the plan
- **Keeps you updated** with progress reports
- **Asks for help** when it needs documentation or clarification

**Usage**:
```
/saat-orchestrate
```

**Example Conversation**:
```
You: /saat-orchestrate

Orchestrator: Hello! I'm your SAAT architecture consultant.
              I'll help you with architecture discovery, design,
              quality analysis, validation, and infrastructure.

              What brings you here today?
              1. I have an existing codebase I want to analyze
              2. I want to design a new system
              3. I have an architecture I want to review
              4. I'm not sure - help me figure it out

You: I want to analyze my existing payment processing application

Orchestrator: Great! I'll help you analyze your payment app.

              First, let me understand your situation:
              - Where is the codebase? (path)
              - Do you have any existing architecture docs?
              - What are your main concerns? (security, performance, etc.)
              - Any compliance requirements? (PCI-DSS, etc.)

You: The code is in /app/payment-system, no existing docs,
     I'm concerned about PCI-DSS compliance and security

Orchestrator: Perfect! Based on what you've told me, here's my plan:

              📋 Analysis Plan:
              1. ✅ Discover architecture from /app/payment-system
              2. ✅ Generate C4 model
              3. ✅ Analyze architecture quality (14 characteristics)
              4. ✅ Validate PCI-DSS compliance
              5. ✅ Deep security analysis with threat modeling
              6. ✅ Generate comprehensive documentation
              7. ✅ Create infrastructure-as-code (if needed)

              Estimated time: 5-10 minutes

              Does this plan look good? (y/n)

You: yes

Orchestrator: Excellent! Starting analysis...

              [1/7] 🔍 Discovering architecture...
              Found: 3 services (payment-api, auth-service, notification-service)
              Technologies: Node.js, PostgreSQL, Redis, RabbitMQ
              Pattern: Microservices with event-driven communication
              ✅ Discovery complete!

              [2/7] 🏗️ Generating C4 model...
              Created: 3 systems, 8 containers, 15 components
              ✅ Model generated!

              [3/7] 📊 Analyzing architecture quality...
              Overall Score: 68/100 (Needs Improvement)
              Critical Issues: 2 (Availability, Security)
              ✅ Analysis complete!

              [4/7] ✅ Validating PCI-DSS compliance...
              Compliance Score: 72/100
              ⚠️ Found 5 compliance issues
              ✅ Validation complete!

              [5/7] 🔒 Running security analysis...
              🚨 CRITICAL: Unencrypted database connections
              🚨 CRITICAL: Missing authentication on admin endpoints
              ⚠️ HIGH: Weak password hashing (MD5)
              ✅ Security scan complete!

              [6/7] 📚 Generating documentation...
              Created: README.md, architecture diagrams, ADRs
              ✅ Documentation complete!

              [7/7] 🏗️ Creating infrastructure code...
              Generated: AWS Terraform with PCI-DSS configuration
              ✅ Infrastructure code ready!


              🎉 Analysis Complete!

              📊 Summary:
              - Quality: 68/100 (Needs Improvement)
              - Compliance: 72/100 (PCI-DSS)
              - Security: 🚨 2 CRITICAL, 1 HIGH, 3 MEDIUM issues

              🚨 TOP PRIORITIES:
              1. Fix unencrypted database connections (CRITICAL)
              2. Add authentication to admin endpoints (CRITICAL)
              3. Upgrade password hashing to bcrypt (HIGH)
              4. Add load balancer for high availability
              5. Implement auto-scaling

              📁 Generated Files:
              - architecture.json (C4 model)
              - archchar-analysis.md (quality report)
              - validation-report.json (PCI-DSS)
              - security-report.json (threat model)
              - docs/ (comprehensive documentation)
              - infrastructure/ (Terraform)

              What would you like to do next?
              1. Review the security issues in detail
              2. See recommendations for fixing availability
              3. Deploy the infrastructure
              4. Something else
```

**See**: [docs/ORCHESTRATOR_GUIDE.md](docs/ORCHESTRATOR_GUIDE.md) for complete guide.

### 2-9. Specialized Agents

The Orchestrator coordinates these specialized agents as needed:

- **🔍 Discovery Agent** - Analyzes codebases (brownfield)
- **📋 Requirements Agent** - Extracts requirements (greenfield)
- **🏗️ Generator Agent** - Creates C4 models
- **📊 Architecture Characteristics Agent** - Evaluates quality
- **✅ Validation Agent** - Checks compliance
- **🔒 Security Agent** - Analyzes security
- **📚 Documentation Agent** - Generates docs
- **🏗️ Terraform Agent** - Creates infrastructure

Each agent has its own slash command if you want to use it directly:
- `/saat-discover`
- `/saat-requirements`
- `/saat-generate`
- `/saat-analyze-characteristics`
- `/saat-validate`
- `/saat-security`
- `/saat-document`
- `/saat-terraform`

**For detailed documentation on each agent**, see:
- [docs/AGENTS_QUICK_REFERENCE.md](docs/AGENTS_QUICK_REFERENCE.md) - All agents overview
- [Appendix: Agent API Reference](#appendix-agent-api-reference) - Python API for each agent

---

## 📚 Documentation

### Main Guides
- **[README.md](README.md)** - This document (overview and quick start)
- **[GREENFIELD_GUIDE.md](docs/GREENFIELD_GUIDE.md)** - Complete greenfield workflow
- **[BROWNFIELD_GUIDE.md](docs/BROWNFIELD_GUIDE.md)** - Complete brownfield workflow
- **[CUSTOMIZATION_GUIDE.md](docs/CUSTOMIZATION_GUIDE.md)** - How to customize SAAT

### Agent Documentation
- **[ORCHESTRATOR_GUIDE.md](docs/ORCHESTRATOR_GUIDE.md)** - Complete orchestrator guide
- **[AGENTS_QUICK_REFERENCE.md](docs/AGENTS_QUICK_REFERENCE.md)** - All agents overview
- **[ARCHITECTURE_CHARACTERISTICS_USAGE.md](docs/ARCHITECTURE_CHARACTERISTICS_USAGE.md)** - Quality analysis guide
- **[ARCHCHAR_INTEGRATION_ANALYSIS.md](docs/ARCHCHAR_INTEGRATION_ANALYSIS.md)** - Integration patterns

### Integration Guides
- **[BAC4_INTEGRATION.md](BAC4_INTEGRATION.md)** - Visual editor integration
- **[.claude/README.md](.claude/README.md)** - Slash commands reference

### Technical Documentation
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - SAAT system architecture
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and roadmap
- **[RELEASE_NOTES.md](RELEASE_NOTES.md)** - Release information

---

## 💡 Examples

### Example 1: Quick Architecture Review

```
You: /saat-orchestrate

Orchestrator: What would you like to do?

You: Quick review of my microservices app in ./services

Orchestrator: [Runs discovery → generate → analyze → validate → security]

              ✅ Quick Review Complete!

              Quality: 75/100 (Good)
              Top Issues:
              1. No load balancer (availability: 60/100)
              2. Missing auto-scaling (scalability: 65/100)
              3. No caching layer (performance: 70/100)

              Recommendation: Add these to improve to 90/100
```

### Example 2: Design Payment System

```
You: /saat-orchestrate

You: Design a PCI-DSS compliant payment system

Orchestrator: Do you have requirements docs?

You: Yes, in docs/requirements.md

Orchestrator: [Extracts requirements → generates architecture →
              analyzes quality → validates PCI-DSS →
              checks security → generates infrastructure]

              ✅ Design Complete!

              Your system:
              - 3 systems, 8 containers, 15 components
              - Quality: 88/100 (Excellent)
              - PCI-DSS: 98/100 (Ready for certification)
              - Infrastructure: AWS Terraform ready

              You can deploy with: cd infrastructure && terraform apply
```

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request

### Development Setup

```bash
git clone https://github.com/DavidROliverBA/SAAT.git
cd SAAT
pip install -e ".[dev]"
```

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file

---

## 🙏 Acknowledgments

- **PydanticAI** - Agent framework
- **C4 Model** - Architecture visualization methodology
- **Mark Richards** - Architecture characteristics methodology
- **Structurizr** - JSON schema for C4 models

---

**Built with ❤️ using PydanticAI**

---

## 📎 Appendix

### Appendix A: CLI Reference

For users who prefer command-line interface over conversational commands.

#### Discovery & Generation
```bash
saat discover --path /repo --output discovery.json
saat generate --discovery discovery.json --output architecture.json
saat analyze --path /repo --output architecture.json  # Combined
```

#### Requirements (Greenfield)
```bash
saat discover-requirements \
  -f docs/PRD.md \
  -n "Project Name" \
  -o requirements.json
```

#### Quality Analysis
```bash
saat analyze-characteristics \
  -m architecture.json \
  -c characteristics.json \
  -o archchar-analysis
```

#### Validation
```bash
saat validate-model -m architecture.json -f PCI-DSS
saat validate-model -m architecture.json -f HIPAA
```

#### Security
```bash
saat security-scan -m architecture.json --threat-model
```

#### Documentation
```bash
saat generate-docs \
  -m architecture.json \
  -f markdown -f plantuml -f mermaid \
  -o docs/
```

#### Infrastructure
```bash
saat generate-terraform -m architecture.json -p aws -r us-east-1 -o infrastructure/
```

#### Global Options
```bash
# Auto-approve (skip prompts)
saat -y validate-model -m architecture.json

# Use different model
saat --model openai:gpt-4 analyze --path /repo
```

**Full CLI documentation**: Run `saat --help` or `saat <command> --help`

### Appendix B: MCP Tools Reference

For developers integrating SAAT into other applications.

Available MCP tools:
- `orchestrate` - Start orchestrated workflow
- `discover_architecture` - Analyze repository
- `discover_requirements` - Extract requirements
- `generate_c4_model` - Generate model
- `analyze_architecture_characteristics` - Evaluate quality
- `validate_model` - Validate compliance
- `analyze_security` - Security analysis
- `generate_documentation` - Create docs
- `generate_terraform` - Infrastructure code
- `full_analysis` - Complete workflow

All tools use `auto_approve=True` for seamless integration.

### Appendix C: Agent API Reference

For Python developers using SAAT programmatically.

#### Orchestrator Agent
```python
from saat.agents import OrchestratorAgent

agent = OrchestratorAgent()
result = await agent.orchestrate(
    user_goal="Analyze my payment system",
    context={
        "codebase_path": "/app/payment",
        "compliance": ["PCI-DSS"],
        "concerns": ["security"]
    },
    auto_approve=False
)
```

#### Discovery Agent
```python
from saat.agents import DiscoveryAgent

agent = DiscoveryAgent()
discovery = await agent.analyze_repository(
    path="/path/to/repo",
    max_depth=3,
    auto_approve=False
)
```

#### Generator Agent
```python
from saat.agents import GeneratorAgent

agent = GeneratorAgent()
model = await agent.generate_model(
    discovery=discovery,
    business_context=context,
    auto_approve=False
)
```

#### Requirements Agent
```python
from saat.agents import RequirementsAgent

agent = RequirementsAgent()
result = await agent.discover_requirements(
    file_paths=["docs/PRD.md"],
    project_name="Payment Platform",
    auto_approve=False
)
```

#### Architecture Characteristics Agent
```python
from saat.agents import ArchCharAgent

agent = ArchCharAgent()
result = await agent.analyze_architecture(
    model=c4_model,
    characteristics_input=archchar_input,
    auto_approve=False
)
```

#### Validation Agent
```python
from saat.agents import ValidationAgent

agent = ValidationAgent()
result = await agent.validate_model(
    model=c4_model,
    framework="PCI-DSS",
    auto_approve=False
)
```

#### Security Agent
```python
from saat.agents import SecurityAgent

agent = SecurityAgent()
result = await agent.analyze_security(
    model=c4_model,
    threat_model=True,
    auto_approve=False
)
```

#### Documentation Agent
```python
from saat.agents import DocumentationAgent

agent = DocumentationAgent()
result = await agent.generate_documentation(
    model=c4_model,
    output_dir="docs/",
    formats=["markdown", "plantuml", "mermaid"],
    auto_approve=False
)
```

#### Terraform Agent
```python
from saat.agents import TerraformAgent

agent = TerraformAgent()
result = await agent.generate_terraform(
    model=c4_model,
    provider="aws",
    region="us-east-1",
    output_dir="infrastructure/",
    auto_approve=False
)
```

### Appendix D: Model Support

SAAT supports multiple AI models:

**Anthropic Claude** (Default)
```bash
export ANTHROPIC_API_KEY="your-key"
saat --model anthropic:claude-sonnet-4 analyze --path /repo
```

**OpenAI**
```bash
export OPENAI_API_KEY="your-key"
saat --model openai:gpt-4 analyze --path /repo
```

**Google Gemini**
```bash
export GEMINI_API_KEY="your-key"
saat --model gemini:gemini-1.5-pro analyze --path /repo
```

**Local (Ollama)**
```bash
ollama serve
ollama pull llama3.1
saat --model ollama:llama3.1 analyze --path /repo
```

### Appendix E: Structurizr Integration

SAAT integrates with [bac4-standalone](https://github.com/DavidROliverBA/bac4-standalone) for visual editing.

```bash
# Export to Structurizr format
saat export-structurizr -m architecture.json -o structurizr.json

# Import from Structurizr
saat import-structurizr -s structurizr.json -o architecture.json
```

**See**: [BAC4_INTEGRATION.md](BAC4_INTEGRATION.md) for complete guide.

### Appendix F: Future Roadmap - Agent Learning

**🔮 Coming in v2.1+**: Agents that learn and improve over time

#### Vision

Each SAAT agent will gain experience from every analysis, building organizational knowledge:

- **Pattern Recognition**: Learn common patterns in your codebases
- **Recommendation Quality**: Improve suggestions based on what worked
- **Domain Knowledge**: Build expertise in your specific industry/domain
- **Team Preferences**: Learn your team's architecture preferences
- **Historical Context**: Remember past decisions and their outcomes

#### Research Areas

We're researching best practices in agent learning:

1. **Memory Systems**
   - Vector databases for semantic memory (Pinecone, Weaviate)
   - Graph databases for relationship memory (Neo4j)
   - Time-series for evolution tracking

2. **Feedback Loops**
   - User feedback on recommendations (👍/👎)
   - Outcome tracking (did the fix work?)
   - A/B testing different approaches

3. **Knowledge Transfer**
   - Cross-project learning
   - Industry best practices database
   - Community-contributed patterns

4. **Privacy-Preserving Learning**
   - Local-only learning mode
   - Federated learning for team knowledge
   - Opt-in cloud knowledge sharing

#### Implementation Plan

**Phase 1**: Memory Storage (v2.1)
- Store analysis history in local SQLite
- Track patterns and decisions
- Basic recommendation improvement

**Phase 2**: Learning from Feedback (v2.2)
- User feedback mechanism
- Outcome tracking
- Recommendation scoring

**Phase 3**: Advanced Learning (v2.3)
- Vector embeddings for pattern matching
- Cross-project knowledge transfer
- Community knowledge base (opt-in)

**Phase 4**: Adaptive Agents (v3.0)
- Agents that adapt to your organization
- Personalized recommendations
- Predictive architecture guidance

#### Relevant Research

- [MemGPT](https://arxiv.org/abs/2310.08560) - Virtual context management for LLMs
- [Voyager](https://arxiv.org/abs/2305.16291) - Lifelong learning agents
- [Reflexion](https://arxiv.org/abs/2303.11366) - Self-reflection for agents
- [RAG Systems](https://arxiv.org/abs/2005.11401) - Retrieval-augmented generation

**See**: [docs/AGENT_LEARNING.md](docs/AGENT_LEARNING.md) for detailed research and design (coming soon)

---

**📞 Support**

- **Issues**: https://github.com/DavidROliverBA/SAAT/issues
- **Discussions**: https://github.com/DavidROliverBA/SAAT/discussions
