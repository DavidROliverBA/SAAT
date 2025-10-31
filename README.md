# SAAT - Solution Architecture Agent Toolkit

<p align="center">
  <strong>🤖 AI-Powered C4 Architecture Discovery & Documentation with PydanticAI</strong>
</p>

<p align="center">
  Automate architecture discovery, C4 model generation, and documentation using specialized AI agents powered by PydanticAI
</p>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Available Agents](#-available-agents)
- [CLI Usage](#-cli-usage)
- [Programmatic Usage](#-programmatic-usage)
- [Building from Scratch (Greenfield Projects)](#-building-from-scratch-greenfield-projects)
- [Refining & Improving Agents](#-refining--improving-agents)
- [Model Support](#-model-support)
- [Best Practices](#-best-practices)
- [Examples](#-examples)
- [Architecture](#-architecture)
- [Contributing](#-contributing)

---

## 🎯 Overview

SAAT is a **PydanticAI-powered** agent toolkit that automates the creation, validation, and documentation of C4 architecture models. Built with production-grade features including multi-model support, observability, and type-safe validation.

### Key Features

- 🔍 **Automated Discovery** - Analyze codebases to extract architecture
- 🏗️ **C4 Model Generation** - Create valid C4 models automatically
- ✅ **Type-Safe Validation** - Pydantic models ensure correctness
- 🤖 **Multi-Model Support** - Use Claude, GPT-4, Gemini, or local models
- 📊 **Built-in Observability** - Pydantic Logfire integration
- 🔄 **Durable Execution** - Survive API failures and restarts
- 🎯 **Production Ready** - Retry logic, streaming, error handling

### Powered by PydanticAI

SAAT leverages [PydanticAI](https://ai.pydantic.dev/) for:
- **Type-safe agents** with automatic validation
- **Multi-model support** across providers
- **Structured outputs** with Pydantic models
- **Tool calling** for repository analysis
- **Observability** and monitoring

---

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/DavidROliverBA/SAAT.git
cd SAAT

# 2. Install with pip
pip install -e .

# Or with Poetry
poetry install

# 3. Set up environment
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# 4. Run analysis
saat analyze --path /path/to/your/code --output architecture.json

# 5. View results
cat architecture.json | python -m json.tool
```

---

## 📦 Installation

### Option 1: pip (Recommended)

```bash
# Install from source
git clone https://github.com/DavidROliverBA/SAAT.git
cd SAAT
pip install -e .

# Or install specific extras
pip install -e ".[all]"  # All features (Logfire, OpenAI, Gemini)
pip install -e ".[logfire]"  # Just observability
pip install -e ".[openai]"  # Add OpenAI support
```

### Option 2: Poetry

```bash
git clone https://github.com/DavidROliverBA/SAAT.git
cd SAAT
poetry install

# With extras
poetry install -E all
```

### Requirements

- Python 3.9+
- API key for at least one model provider:
  - **Anthropic Claude** (recommended): Get key at [console.anthropic.com](https://console.anthropic.com)
  - **OpenAI**: Get key at [platform.openai.com](https://platform.openai.com)
  - **Google Gemini**: Get key at [makersuite.google.com](https://makersuite.google.com)

### Environment Setup

```bash
# Required: Set your API key
export ANTHROPIC_API_KEY="sk-ant-api03-your-key-here"

# Optional: Choose default model
export SAAT_MODEL="anthropic:claude-sonnet-4"

# Optional: Enable observability
export LOGFIRE_TOKEN="your-logfire-token"
```

---

## 🤖 Available Agents

### Implemented Agents

#### 1. **Discovery Agent** ✅
- **Purpose**: Analyze repositories to discover architecture
- **Capabilities**:
  - Technology detection (languages, frameworks, databases)
  - Pattern recognition (microservices, event-driven, etc.)
  - Entry point identification
  - Confidence scoring with evidence
- **Model**: Uses PydanticAI with tool calling for repository exploration
- **Output**: `DiscoveryResult` with technologies, patterns, and metadata

#### 2. **Generator Agent** ✅
- **Purpose**: Convert discovery results into C4 models
- **Capabilities**:
  - Generate Systems, Containers, Components
  - Infer relationships and data flows
  - Assign criticality levels (CS1, CS2, SL1, etc.)
  - Apply business context rules
- **Model**: Uses PydanticAI with structured output validation
- **Output**: Complete `C4Model` with all elements and relationships

### Agents Ready to Implement

#### 3. **Validation Agent** 🔜
- Validate C4 models against enterprise standards
- Check compliance requirements (PCI-DSS, GDPR, SOC2)
- Identify missing relationships or incomplete descriptions
- Suggest improvements

#### 4. **Documentation Agent** 🔜
- Generate markdown documentation from C4 models
- Create architecture decision records (ADRs)
- Publish to Confluence or wikis
- Generate diagrams (PlantUML, Mermaid)

#### 5. **Security Agent** 🔜
- Analyze security posture from C4 models
- Identify unencrypted communications
- Check authentication mechanisms
- Generate security reports

#### 6. **Terraform Agent** 🔜
- Generate infrastructure-as-code from C4 models
- Support AWS, Azure, GCP
- Apply criticality-based configurations
- Create monitoring and alerting

---

## 💻 CLI Usage

### Discover Architecture

```bash
# Analyze a repository
saat discover --path /path/to/repo --output discovery.json

# With maximum depth control
saat discover --path /path/to/repo --max-depth 5 --output discovery.json
```

**Output**: `discovery.json` with technologies, patterns, entry points, and confidence scores.

### Generate C4 Model

```bash
# Generate from discovery
saat generate --discovery discovery.json --output c4-model.json

# With business context
saat generate \
  --discovery discovery.json \
  --business-context business.json \
  --output c4-model.json
```

### Full Analysis (Recommended)

```bash
# Discover and generate in one command
saat analyze --path /path/to/repo --output architecture.json

# Save intermediate discovery
saat analyze \
  --path /path/to/repo \
  --output architecture.json \
  --save-discovery

# With business context
saat analyze \
  --path /path/to/repo \
  --business-context business.json \
  --output architecture.json
```

### Validate Model

```bash
# Check model for issues
saat validate --model-file c4-model.json
```

### Change Model

```bash
# Use GPT-4
saat --model openai:gpt-4 analyze --path /path/to/repo

# Use Gemini
saat --model gemini-1.5-pro analyze --path /path/to/repo

# Use local Ollama
saat --model ollama:llama2 analyze --path /path/to/repo
```

### Get Info

```bash
# Show version and configuration
saat info
```

---

## 🐍 Programmatic Usage

### Simple Analysis

```python
import asyncio
from saat import SAATClient

async def main():
    # Initialize client
    client = SAATClient(model="anthropic:claude-sonnet-4")

    # Analyze repository
    discovery, model = await client.analyze("/path/to/repo")

    # Access results
    print(f"Technologies: {discovery.technologies}")
    print(f"Systems: {len(model.systems)}")
    print(f"Containers: {len(model.containers)}")

    # Save model
    with open("architecture.json", "w") as f:
        f.write(model.model_dump_json(indent=2))

asyncio.run(main())
```

### Step-by-Step Analysis

```python
from saat import SAATClient
from saat.models import BusinessContext, Stakeholder

async def detailed_analysis():
    client = SAATClient()

    # Step 1: Discovery
    discovery = await client.discover(
        "/path/to/repo",
        context="Focus on microservices architecture"
    )

    # Step 2: Create business context
    business = BusinessContext(
        purpose="E-commerce platform for B2B sales",
        stakeholders=[
            Stakeholder(
                name="Sales Team",
                role="Primary Users",
                needs=["Fast order processing", "Customer insights"]
            )
        ],
        capabilities=["Order Management", "Inventory", "Payments"]
    )

    # Step 3: Generate model
    model = await client.generate_model(discovery, business)

    # Step 4: Refine if needed
    refined = await client.refine_model(
        model,
        "Add Redis cache container and update relationships"
    )

    return refined
```

### Using Individual Agents

```python
from saat.agents import DiscoveryAgent, GeneratorAgent

async def use_agents():
    # Discovery Agent
    discovery_agent = DiscoveryAgent(model="anthropic:claude-sonnet-4")
    discovery = await discovery_agent.analyze_repository("/path/to/repo")

    # Generator Agent
    generator_agent = GeneratorAgent(model="anthropic:claude-sonnet-4")
    model = await generator_agent.generate_model(discovery)

    return model
```

### Context Broker for Pipelines

```python
from saat.broker import ContextBroker
from saat.models import Pipeline, PipelineStep

async def run_pipeline():
    broker = ContextBroker(model="anthropic:claude-sonnet-4")

    # Define pipeline
    pipeline = Pipeline(
        name="full-analysis",
        description="Discover and generate C4 model",
        steps=[
            PipelineStep(
                name="discover",
                agent="discovery",
                task="analyze_repository",
                required=True
            ),
            PipelineStep(
                name="generate",
                agent="generator",
                task="generate_model",
                depends_on=["discover"],
                required=True
            )
        ]
    )

    # Execute pipeline
    results = await broker.execute_pipeline(
        pipeline,
        initial_context={"repo_path": "/path/to/repo"}
    )

    return results
```

---

## 🏗️ Building from Scratch (Greenfield Projects)

When starting a **new project from scratch**, SAAT becomes a powerful **design-first architecture tool**. Instead of discovering existing code, you design your ideal architecture upfront, validate it, and then implement following that validated design.

### Why Design-First with SAAT?

- ✅ **Validate Before You Build** - Catch architectural issues before writing code
- ✅ **Generate Infrastructure** - Auto-create Terraform, docs, and ADRs from your design
- ✅ **Enforce Standards** - Ensure compliance from day one
- ✅ **Guide Implementation** - Developers follow a validated architecture blueprint
- ✅ **Continuous Validation** - Verify implementation matches design as you build

### Greenfield Workflow

#### Phase 1: Design Your Architecture

```python
from saat.models import (
    C4Model, SystemContext, Container, ExternalSystem,
    Relationship, ModelMetadata, Interface, CriticalityLevel
)
from datetime import datetime

# Create your architecture design
architecture = C4Model(
    version="1.0.0",
    metadata=ModelMetadata(
        project="Payment Processing Platform",
        author="Architecture Team",
        created=datetime.now(),
        last_modified=datetime.now(),
        description="Secure, scalable payment processing for B2B transactions",
        tags=["fintech", "payments", "microservices"]
    ),
    systems=[
        SystemContext(
            id="SYS-PAYMENT-001",
            name="Payment Processing Platform",
            description="Handles all payment transactions and fraud detection",
            criticality=CriticalityLevel.CS1,
            responsibilities=[
                "Process payment transactions",
                "Detect fraudulent activity",
                "Generate financial reports"
            ],
            owner="payments-team@company.com"
        )
    ],
    containers=[
        Container(
            id="CON-API-001",
            name="Payment API",
            description="REST API for payment processing",
            type="Container",
            technology=["Python", "FastAPI", "Pydantic"],
            system_id="SYS-PAYMENT-001",
            criticality=CriticalityLevel.CS1,
            interfaces=[
                Interface(
                    protocol="HTTPS",
                    port=443,
                    authentication="OAuth2 + mTLS",
                    rate_limit="1000 req/min",
                    encrypted=True
                )
            ],
            responsibilities=[
                "Accept payment requests",
                "Validate payment data",
                "Return transaction status"
            ]
        ),
        Container(
            id="CON-DB-001",
            name="Transaction Database",
            description="Primary transactional data store",
            type="Database",
            technology=["PostgreSQL 15"],
            system_id="SYS-PAYMENT-001",
            criticality=CriticalityLevel.CS1
        )
    ],
    externals=[
        ExternalSystem(
            id="EXT-STRIPE-001",
            name="Stripe Payment Gateway",
            description="Third-party payment processing",
            vendor="Stripe Inc.",
            sla="99.99%"
        )
    ],
    relationships=[
        Relationship(
            id="REL-001",
            source="CON-API-001",
            target="CON-DB-001",
            description="Stores transaction data",
            type="uses",
            protocol="PostgreSQL",
            synchronous=True
        ),
        Relationship(
            id="REL-002",
            source="CON-API-001",
            target="EXT-STRIPE-001",
            description="Processes payment",
            type="uses",
            protocol="HTTPS",
            synchronous=True
        )
    ]
)

# Save design
with open("payment-platform-design.json", "w") as f:
    f.write(architecture.model_dump_json(indent=2))
```

#### Phase 2: Validate Your Design

```bash
# Validate design for correctness
saat validate --model-file payment-platform-design.json
```

#### Phase 3: Implement Following Design

Implement each container according to specifications:

```python
# services/payment-api/main.py
# Built following CON-API-001 specification

from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI(title="Payment API")

# From C4: Interface specification (HTTPS, port 443, OAuth2 + mTLS)
@app.post("/transactions")
async def create_transaction(transaction: TransactionRequest):
    # Responsibility 1: Validate payment data
    if not transaction.validate():
        raise HTTPException(400, "Invalid transaction data")

    # REL-001: Store in CON-DB-001 (PostgreSQL)
    await db.transactions.create(transaction)

    # REL-002: Process via EXT-STRIPE-001 (Stripe)
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.stripe.com/v1/charges",
            headers={"Authorization": f"Bearer {STRIPE_KEY}"}
        )

    # Responsibility 3: Return transaction status
    return {"id": transaction.id, "status": "processed"}

# From C4: criticality CS1 requires health checks
@app.get("/health")
async def health():
    return {"status": "healthy"}
```

#### Phase 4: Continuous Validation

```bash
# Discover actual implementation
saat discover --path ./services --output actual.json

# Compare with design (future feature)
# saat compare --expected design.json --actual actual.json
```

---

## 🔧 Refining & Improving Agents

### Extending Discovery Agent

Add support for new technologies:

```python
from saat.agents.discovery import DiscoveryAgent, DiscoveryDependencies
from pydantic_ai import Agent, RunContext

class CustomDiscoveryAgent(DiscoveryAgent):
    """Extended discovery with Rust support."""

    def __init__(self, model: str = "anthropic:claude-sonnet-4"):
        super().__init__(model)

        # Add custom tool
        @self.agent.tool
        async def discover_rust(ctx: RunContext[DiscoveryDependencies]) -> dict:
            """Detect Rust projects."""
            cargo_files = await ctx.deps.list_files("Cargo.toml")
            if cargo_files:
                return {"rust_detected": True, "cargo_files": cargo_files}
            return {"rust_detected": False}
```

### Extending Generator Agent

Customize ID generation:

```python
from saat.agents.generator import GeneratorAgent, GeneratorDependencies

class CustomGeneratorAgent(GeneratorAgent):
    """Generator with custom ID format."""

    async def generate_model(self, discovery, business_context=None):
        model = await super().generate_model(discovery, business_context)

        # Apply custom ID format: PROJ-TYPE-001
        for i, system in enumerate(model.systems, 1):
            system.id = f"PROJ-SYS-{i:03d}"

        for i, container in enumerate(model.containers, 1):
            container.id = f"PROJ-CON-{i:03d}"

        return model
```

### Creating Custom Agents

```python
from pydantic_ai import Agent
from saat.models import C4Model, ValidationResult

def create_custom_validator() -> Agent[None, ValidationResult]:
    """Create custom validation agent."""

    agent = Agent(
        "anthropic:claude-sonnet-4",
        result_type=ValidationResult,
        system_prompt="""You are a security-focused architecture validator.

        Check for:
        1. All external communications use HTTPS
        2. Databases have encryption at rest
        3. Authentication is properly configured
        4. No hardcoded secrets in descriptions
        """
    )

    @agent.tool
    async def check_encryption(model: C4Model) -> dict:
        """Check encryption settings."""
        issues = []
        for container in model.containers:
            for interface in container.interfaces:
                if not interface.encrypted:
                    issues.append(f"{container.name} has unencrypted interface")
        return {"encryption_issues": issues}

    return agent
```

---

## 🌐 Model Support

SAAT supports **all models via PydanticAI**:

### Anthropic Claude (Recommended)
```bash
export ANTHROPIC_API_KEY="your-key"
saat --model anthropic:claude-sonnet-4 analyze --path /repo
saat --model anthropic:claude-opus-4 analyze --path /repo
```

### OpenAI
```bash
pip install -e ".[openai]"
export OPENAI_API_KEY="your-key"
saat --model openai:gpt-4 analyze --path /repo
saat --model openai:gpt-4-turbo analyze --path /repo
```

### Google Gemini
```bash
pip install -e ".[gemini]"
export GOOGLE_API_KEY="your-key"
saat --model gemini-1.5-pro analyze --path /repo
```

### Local Models (Ollama)
```bash
# Start Ollama server
ollama serve

# Use local model
saat --model ollama:llama2 analyze --path /repo
saat --model ollama:codellama analyze --path /repo
```

### Other Providers
PydanticAI supports: DeepSeek, Grok, Mistral, Cohere, Azure, AWS Bedrock, and more.

---

## 📖 Best Practices

### 1. Discovery Best Practices

**DO:**
- ✅ Run discovery on clean repositories (no build artifacts)
- ✅ Provide business context for better results
- ✅ Use `--max-depth` to limit exploration time
- ✅ Review discovery results before generating models

**DON'T:**
- ❌ Analyze repositories with secrets or credentials
- ❌ Skip the discovery step for accurate models
- ❌ Ignore low confidence scores (< 0.7)

### 2. Model Generation Best Practices

**DO:**
- ✅ Always provide business context when available
- ✅ Review generated models for accuracy
- ✅ Assign appropriate criticality levels
- ✅ Validate models before using in production

**DON'T:**
- ❌ Accept models without validation
- ❌ Ignore missing relationships
- ❌ Skip criticality level assignment

### 3. Multi-Model Best Practices

**DO:**
- ✅ Use Claude Sonnet-4 for balanced performance
- ✅ Use Claude Opus-4 for complex architectures
- ✅ Try different models if results are unsatisfactory
- ✅ Use local models for sensitive codebases

**DON'T:**
- ❌ Use smaller models for large, complex systems
- ❌ Forget to set appropriate API keys
- ❌ Mix models mid-analysis (use same model throughout)

### 4. Production Best Practices

**DO:**
- ✅ Enable Logfire for observability
- ✅ Set up monitoring and alerting
- ✅ Version control your C4 models
- ✅ Automate discovery in CI/CD
- ✅ Document architectural decisions (ADRs)

**DON'T:**
- ❌ Run in production without error handling
- ❌ Ignore API rate limits
- ❌ Skip validation in pipelines

---

## 📚 Examples

### Example 1: Microservices Platform

```python
from saat import SAATClient

client = SAATClient()

# Analyze microservices
discovery, model = await client.analyze("/path/to/microservices")

# Check results
print(f"Found {len(model.containers)} services")
for container in model.containers:
    print(f"  - {container.name} ({', '.join(container.technology)})")
```

### Example 2: With Business Context

```python
from saat import SAATClient
from saat.models import BusinessContext, ComplianceRequirement

business = BusinessContext(
    purpose="Healthcare patient management system",
    capabilities=["Patient Records", "Appointments", "Billing"],
    compliance=[
        ComplianceRequirement(
            framework="HIPAA",
            requirements=["Data encryption", "Audit logs", "Access controls"],
            applicable=True
        )
    ]
)

client = SAATClient()
discovery, model = await client.analyze("/path/to/repo", business_context=business)

# Model will include HIPAA-aware criticality levels
for container in model.containers:
    print(f"{container.name}: {container.criticality}")
```

### Example 3: Model Refinement

```python
from saat import SAATClient

client = SAATClient()

# Initial generation
discovery, model = await client.analyze("/path/to/repo")

# Refine based on feedback
refined = await client.refine_model(
    model,
    """
    Add these improvements:
    1. Add Redis cache container (CS2 criticality)
    2. Create relationship from API to Redis
    3. Add monitoring container for observability
    4. Update API container to include health check endpoint
    """
)

# Save refined model
with open("architecture-v2.json", "w") as f:
    f.write(refined.model_dump_json(indent=2))
```

---

## 🏛️ Architecture

SAAT uses a **multi-agent architecture** powered by PydanticAI:

```
┌─────────────────────────────────────────────────────────────┐
│                         SAAT CLI                             │
│                    (Click-based interface)                   │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                      SAAT Client                             │
│              (High-level programmatic API)                   │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    Context Broker                            │
│              (Pipeline orchestration layer)                  │
└─────────┬────────────────────────────────────┬──────────────┘
          │                                    │
          ▼                                    ▼
┌──────────────────────┐           ┌──────────────────────────┐
│  Discovery Agent     │           │  Generator Agent         │
│  (PydanticAI)        │           │  (PydanticAI)            │
│                      │           │                          │
│  - Analyze repos     │           │  - Create C4 models      │
│  - Detect tech       │           │  - Assign criticality    │
│  - Find patterns     │           │  - Infer relationships   │
└──────────────────────┘           └──────────────────────────┘
```

### Technology Stack

- **Framework**: PydanticAI
- **Language**: Python 3.9+
- **Validation**: Pydantic v2
- **CLI**: Click
- **Models**: Anthropic, OpenAI, Google, Ollama, etc.
- **Observability**: Logfire (optional)
- **Type Checking**: mypy
- **Testing**: pytest

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

```bash
# 1. Clone and install
git clone https://github.com/DavidROliverBA/SAAT.git
cd SAAT
poetry install

# 2. Install dev dependencies
poetry install --with dev

# 3. Run tests
poetry run pytest

# 4. Format code
poetry run black saat/
poetry run ruff check saat/

# 5. Type check
poetry run mypy saat/
```

### Areas for Contribution

- 🔧 Implement remaining agents (Validation, Documentation, Security, Terraform)
- 🌐 Add support for more model providers
- 📊 Enhance observability and monitoring
- 🧪 Increase test coverage
- 📚 Improve documentation
- 🎨 Create visualization tools for C4 models

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built with [PydanticAI](https://ai.pydantic.dev/) by the Pydantic team
- Inspired by the [C4 Model](https://c4model.com/) by Simon Brown
- Powered by [Anthropic Claude](https://anthropic.com/), [OpenAI](https://openai.com/), and other LLM providers

---

**Made with ❤️  by the SAAT team**
