# Solution Architecture Agent Toolkit (SAAT)
## Context-Engineered AI Agents for C4 Model Automation

> **Note:** SAAT has been rewritten using **PydanticAI** for production-grade agent development.
> See [README.md](README.md) for current implementation details, installation, and usage examples.

---

### Overview

SAAT is a collection of specialized AI agents designed to assist solution architects in creating, validating, and maintaining C4 architecture models. Built on **PydanticAI**, each agent has specific expertise and works through a context broker to provide comprehensive architectural support.

### Key Technologies

- **Framework**: PydanticAI (Python-based agent framework)
- **Language**: Python 3.9+
- **Validation**: Pydantic v2 (type-safe models)
- **Models**: Multi-provider support (Anthropic Claude, OpenAI, Google Gemini, Ollama, etc.)
- **Observability**: Pydantic Logfire integration
- **CLI**: Click-based command interface

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interfaces                           │
│              CLI | Python API | Future: REST API             │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     Context Broker                           │
│            (Pipeline Orchestration & Context Management)     │
└─────┬──────────────┬────────────────┬─────────────┬─────────┘
      │              │                │             │
      ▼              ▼                ▼             ▼
┌──────────┐  ┌──────────┐    ┌──────────┐  ┌──────────────┐
│Discovery │  │Generator │    │Validation│  │  Advisory    │
│  Agent   │  │  Agent   │    │  Agent   │  │   Agents     │
│(Pydantic │  │(Pydantic │    │(Pydantic │  │  (Pydantic   │
│   AI)    │  │   AI)    │    │   AI)    │  │     AI)      │
└──────────┘  └──────────┘    └──────────┘  └──────────────┘
```

---

## Agent Roles & Capabilities

### 1. Discovery Agent ✅ *Implemented*

**Purpose**: Analyze codebases to discover existing architecture

**Capabilities**:
- Technology stack detection (languages, frameworks, databases)
- Architectural pattern recognition (microservices, monolithic, event-driven)
- Entry point identification (main files, APIs, CLIs)
- Confidence scoring with evidence collection

**Implementation**:
- Uses PydanticAI tool calling to explore repository structure
- File system analysis with configurable depth limits
- Pattern matching against known architectural styles
- Returns structured `DiscoveryResult` with Pydantic validation

**Usage**:
```bash
saat discover --path /path/to/repo --output discovery.json
```

---

### 2. Generator Agent ✅ *Implemented*

**Purpose**: Convert discovery results into valid C4 architecture models

**Capabilities**:
- Generate C4 Level 1-3 models (Systems, Containers, Components)
- Infer relationships and data flows
- Assign criticality levels based on business context
- Apply compliance and security requirements

**Implementation**:
- Uses PydanticAI with structured output (returns `C4Model`)
- Automatic ID generation with configurable formats
- Business context integration for criticality assignment
- Relationship inference based on detected patterns

**Usage**:
```bash
saat generate --discovery discovery.json --output c4-model.json
```

---

### 3. Validation Agent 🔜 *Ready to Implement*

**Purpose**: Validate C4 models against enterprise standards

**Planned Capabilities**:
- Structural validation (orphaned elements, missing relationships)
- Compliance checking (PCI-DSS, HIPAA, GDPR, SOC2)
- Best practice enforcement
- Security posture validation

**Suggested Implementation**:
```python
from pydantic_ai import Agent
from saat.models import C4Model, ValidationResult

agent = Agent(
    "anthropic:claude-sonnet-4",
    result_type=ValidationResult,
    system_prompt="Validate C4 models against enterprise standards..."
)

@agent.tool
async def check_compliance(model: C4Model, framework: str) -> dict:
    """Check model against compliance framework."""
    # Implementation
```

---

### 4. Documentation Agent 🔜 *Ready to Implement*

**Purpose**: Generate documentation artifacts from C4 models

**Planned Capabilities**:
- Markdown documentation generation
- Architecture Decision Records (ADRs)
- PlantUML / Mermaid diagram generation
- Confluence integration
- PDF report generation

**Suggested Tools**:
- Markdown templates with Jinja2
- PlantUML for C4 diagrams
- Confluence REST API for publishing
- PDF generation with ReportLab or WeasyPrint

---

### 5. Security Agent 🔜 *Ready to Implement*

**Purpose**: Analyze security posture from architecture models

**Planned Capabilities**:
- Identify unencrypted communications
- Check authentication mechanisms
- Analyze data flow for sensitive information
- Generate security reports
- Threat modeling

---

### 6. Terraform Agent 🔜 *Ready to Implement*

**Purpose**: Generate infrastructure-as-code from C4 models

**Planned Capabilities**:
- AWS/Azure/GCP resource generation
- Criticality-based configurations (multi-AZ, backups, etc.)
- Network topology from relationships
- Monitoring and alerting setup
- Cost estimation

---

## Context Broker

The **Context Broker** orchestrates agent interactions and maintains shared context:

**Responsibilities**:
- Pipeline execution and orchestration
- Dependency management between agents
- Context sharing and persistence
- Error handling and recovery
- Performance tracking

**Implementation** (`saat/broker.py`):
```python
from saat.broker import ContextBroker

broker = ContextBroker(model="anthropic:claude-sonnet-4")

# Execute full pipeline
discovery, model = await broker.discover_and_generate(
    repo_path="/path/to/repo",
    business_context=business_ctx
)
```

---

## Design Principles

### 1. **Type Safety First**
- All models use Pydantic v2 for validation
- Agents return typed results (no unstructured data)
- Automatic retries on validation failures

### 2. **Multi-Model Support**
- Not locked to single provider
- Easy switching between Claude, GPT-4, Gemini, local models
- Provider-specific optimizations

### 3. **Observable by Default**
- Optional Logfire integration for monitoring
- Track token usage, latency, errors
- Debug agent decisions in real-time

### 4. **Production Ready**
- Durable execution (survives API failures)
- Retry logic with exponential backoff
- Streaming support for long-running tasks
- Comprehensive error handling

### 5. **Extensible Architecture**
- Easy to add new agents
- Custom tools via decorators
- Override default behaviors
- Plugin system for providers

---

## Data Models

### Core C4 Models

All architectural elements are Pydantic models in `saat/models.py`:

- `C4Model` - Complete architecture model
- `SystemContext` - C4 Level 1 (systems)
- `Container` - C4 Level 2 (services, databases)
- `Component` - C4 Level 3 (modules, classes)
- `ExternalSystem` - Third-party dependencies
- `Relationship` - Connections between elements

### Supporting Models

- `DiscoveryResult` - Repository analysis results
- `BusinessContext` - Stakeholders, capabilities, compliance
- `ValidationResult` - Model validation outcomes
- `Pipeline` - Agent workflow definitions

---

## Usage Patterns

### Pattern 1: Brownfield Discovery

```python
from saat import SAATClient

client = SAATClient()

# Discover existing architecture
discovery, model = await client.analyze("/path/to/existing/code")

# Model now contains Systems, Containers, and Relationships
```

### Pattern 2: Greenfield Design-First

```python
from saat.models import C4Model, SystemContext, Container

# Design architecture before coding
design = C4Model(
    systems=[
        SystemContext(id="SYS-001", name="Payment Platform", ...)
    ],
    containers=[
        Container(id="CON-001", name="API", technology=["Python", "FastAPI"], ...)
    ]
)

# Validate design
results = await validator.validate(design)

# Generate infrastructure
terraform = await terraform_agent.generate(design)
```

### Pattern 3: Continuous Validation

```python
# CI/CD integration
discovery_new = await client.discover("/path/to/code")
model_new = await client.generate_model(discovery_new)

# Compare with previous version
drift = await client.compare(model_baseline, model_new)

if drift.has_breaking_changes:
    raise Exception("Architecture drift detected!")
```

---

## Future Enhancements

### Short Term (Next 3 Months)
- Implement Validation Agent
- Implement Documentation Agent
- Add streaming support for large repositories
- Enhanced observability dashboard

### Medium Term (3-6 Months)
- Implement Security Agent
- Implement Terraform Agent
- REST API server
- Web UI for visualization
- Model versioning and diff tools

### Long Term (6-12 Months)
- Fitness Function Agent for continuous monitoring
- Architecture Advisor with ML-based recommendations
- Integration with popular architecture tools (Structurizr, Archimate)
- Collaborative features (team workspaces, reviews)
- Real-time architecture compliance monitoring

---

## Best Practices

### For Discovery
1. Run on clean repositories (no build artifacts)
2. Provide business context for better results
3. Use `--max-depth` to control analysis scope
4. Review confidence scores before proceeding

### For Generation
1. Always validate generated models
2. Provide business context for criticality assignment
3. Review and refine relationship inferences
4. Version control your C4 models

### For Production Use
1. Enable Logfire for observability
2. Set up alerts for low-confidence discoveries
3. Automate discovery in CI/CD pipelines
4. Maintain architecture decision records (ADRs)
5. Regular drift detection runs

---

## Contributing

See [README.md](README.md) for contribution guidelines.

Key areas for contribution:
- Implementing remaining agents (Validation, Documentation, Security, Terraform)
- Adding new model providers
- Enhancing observability
- Creating visualization tools
- Improving test coverage

---

## References

- **PydanticAI**: https://ai.pydantic.dev/
- **C4 Model**: https://c4model.com/
- **Pydantic**: https://docs.pydantic.dev/
- **SAAT Repository**: https://github.com/DavidROliverBA/SAAT

---

**Built with ❤️ using PydanticAI**
