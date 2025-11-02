# SAAT Agents - Quick Reference

**Last Updated**: 2025-11-02

---

## Overview

SAAT includes **9 specialized agents** that work together to provide complete architecture lifecycle support. Each agent is built with PydanticAI and follows consistent patterns for reliability and ease of use.

---

## Agent List

### 1. 🔍 Discovery Agent
**File**: `saat/agents/discovery.py`
**Purpose**: Analyze existing codebases to discover architecture (brownfield)

**What it does**:
- Scans repository structure and files
- Identifies technologies, frameworks, languages
- Detects architectural patterns
- Finds entry points and services

**Input**: Repository path
**Output**: `DiscoveryResult` with technologies, patterns, services, confidence scores

**CLI**: `saat discover -p <repo-path>`

---

### 2. 📋 Requirements Agent
**File**: `saat/agents/requirements.py`
**Purpose**: Extract requirements from documents (greenfield)

**What it does**:
- Parses requirements documents (markdown, text)
- Extracts functional requirements (REQ-F-*)
- Extracts non-functional requirements (REQ-NF-*)
- Creates user stories (US-*)
- Identifies constraints and stakeholders

**Input**: Requirements document paths
**Output**: `ProjectRequirements` with all structured requirements

**CLI**: `saat discover-requirements -f <files>`

---

### 3. 🏗️ Generator Agent
**File**: `saat/agents/generator.py`
**Purpose**: Convert discovery/requirements into C4 models

**What it does**:
- Transforms discovery results or requirements into C4 models
- Creates systems, containers, components
- Generates relationships
- Assigns criticality levels (CS1, CS2, SL1, SL2, STANDARD)

**Input**: `DiscoveryResult` or `ProjectRequirements`
**Output**: `C4Model` with complete architecture

**CLI**: `saat generate -d <discovery.json>` or `saat generate -r <requirements.json>`

---

### 4. ✅ Validation Agent
**File**: `saat/agents/validation.py`
**Purpose**: Validate C4 models against structural standards

**What it does**:
- Checks structural integrity (valid IDs, references)
- Validates completeness (descriptions, owners)
- Enforces best practices
- Compliance checking (PCI-DSS, HIPAA, GDPR, SOC2)

**Input**: `C4Model`, optional compliance framework
**Output**: `ValidationResult` with issues, severity, score (0-100)

**CLI**: `saat validate-model -m <model.json> -f <framework>`

---

### 5. 🔒 Security Agent
**File**: `saat/agents/security.py`
**Purpose**: Analyze security posture from architecture

**What it does**:
- Identifies security vulnerabilities
- Checks encryption (transit and at rest)
- Validates authentication/authorization
- Analyzes data flow security
- Assesses infrastructure security

**Input**: `C4Model`, optional threat modeling flag
**Output**: `SecurityReport` with issues by severity, score, recommendations

**CLI**: `saat security-scan -m <model.json> --threat-model`

---

### 6. 📊 Architecture Characteristics Agent (NEW)
**File**: `saat/agents/archchar.py`
**Purpose**: Evaluate architecture quality against requirements

**What it does**:
- Analyzes 14 standard architecture characteristics
- Identifies gaps with severity levels
- Provides pattern-based recommendations
- Generates weighted compliance scores
- Creates actionable implementation steps

**Characteristics**:
- **Operational**: Availability, Scalability, Performance, Security, Reliability, Fault Tolerance, Recoverability
- **Structural**: Maintainability, Testability, Deployability, Configurability, Extensibility
- **Cross-Cutting**: Interoperability, Usability

**Input**: `C4Model`, `ArchCharInput` (from ArchCharCapture)
**Output**: `ArchCharAnalysisResult` with scores, gaps, recommendations

**CLI**: `saat analyze-characteristics -m <model.json> -c <archchar.json>`

---

### 7. 📖 Documentation Agent
**File**: `saat/agents/documentation.py`
**Purpose**: Generate comprehensive documentation

**What it does**:
- Creates markdown overviews
- Generates C4 diagrams (PlantUML, Mermaid)
- Produces Architecture Decision Records (ADRs)
- Documents components and deployment

**Input**: `C4Model`, output directory, formats
**Output**: Multiple documentation files (markdown, diagrams, ADRs)

**CLI**: `saat document -m <model.json> -o <output-dir> -f markdown,plantuml,mermaid`

---

### 8. 🏗️ Terraform Agent
**File**: `saat/agents/terraform.py`
**Purpose**: Generate infrastructure-as-code

**What it does**:
- Maps C4 containers to cloud resources
- Applies criticality-based configurations
- Generates provider-specific Terraform
- Includes auto-scaling, monitoring, backups

**Providers**: AWS, Azure, GCP

**Input**: `C4Model`, provider, region
**Output**: `TerraformConfiguration` with resources, modules, variables

**CLI**: `saat generate-terraform -m <model.json> -p <provider> -r <region>`

---

### 9. 🔧 Base Agent
**File**: `saat/agents/base.py`
**Purpose**: Common functionality for all agents

**What it provides**:
- Checklist generation
- Human-in-the-loop approval workflow
- Auto-approve mode for automation
- Progress tracking

**Used by**: All agents inherit from `BaseAgentWithChecklist`

---

## Agent Workflow Patterns

### Pattern 1: Brownfield (Existing Codebase)
```
Discovery → Generator → ArchChar → Validation → Security → Documentation → Terraform
     ↓           ↓           ↓          ↓           ↓             ↓            ↓
  Analyze    Create C4   Evaluate   Validate   Security    Generate      Generate
   repo       model      quality     model      audit        docs          IaC
```

**CLI Workflow**:
```bash
saat discover -p ./my-app -o discovery.json
saat generate -d discovery.json -o model.json
saat analyze-characteristics -m model.json -c characteristics.json
saat validate-model -m model.json
saat security-scan -m model.json
saat document -m model.json -o docs/
saat generate-terraform -m model.json -p aws -o infrastructure/
```

---

### Pattern 2: Greenfield (New Project)
```
Requirements → Generator → ArchChar → Validation → Documentation → Terraform
      ↓            ↓           ↓          ↓              ↓             ↓
   Extract      Create C4   Evaluate   Validate      Generate      Generate
requirements    model      quality     model          docs          IaC
```

**CLI Workflow**:
```bash
saat discover-requirements -f requirements.md -o requirements.json
saat generate -r requirements.json -o model.json
# Create characteristics.json from NFRs
saat analyze-characteristics -m model.json -c characteristics.json
saat validate-model -m model.json
saat document -m model.json -o docs/
saat generate-terraform -m model.json -p aws -o infrastructure/
```

---

### Pattern 3: Quality Assurance Focus
```
(Any Source) → Generator → ArchChar → Fix Gaps → Re-analyze → Deploy
                   ↓           ↓          ↓           ↓           ↓
              Create C4   Find gaps  Update C4  Verify fixed  Continue
                model                  model
```

**Iterative Improvement**:
```bash
# Initial analysis
saat generate -d discovery.json -o model.json
saat analyze-characteristics -m model.json -c characteristics.json -o report1.json

# Score: 60/100 - Critical gaps in Availability and Scalability

# Add load balancer, auto-scaling to model
# (Manual or automated enhancement)

# Re-analyze
saat analyze-characteristics -m model-v2.json -c characteristics.json -o report2.json

# Score: 85/100 - Much better!
```

---

## Agent Integration Points

### Data Flow Between Agents

```
Discovery/Requirements
         ↓
    Generator
         ↓
     C4 Model ←──────────┐
         ↓               │
    ┌────┴────┬─────┬───┴───┐
    ↓         ↓     ↓       ↓
ArchChar  Validation Security Documentation
    ↓         ↓     ↓       ↓
  Gaps    Issues  Vulns   Docs
    ↓         ↓     ↓       ↓
    └─────────┴─────┴───────┘
              ↓
         Terraform
              ↓
        Infrastructure
```

### Common Output: C4Model

All downstream agents use the **C4Model** as their primary input:
- **ArchChar**: Evaluates against characteristics
- **Validation**: Checks structural correctness
- **Security**: Analyzes security posture
- **Documentation**: Generates docs
- **Terraform**: Produces IaC

---

## Agent Characteristics Comparison

| Agent | Input Type | Output Type | Analysis Type | Score? | Recommendations? |
|-------|-----------|-------------|---------------|--------|------------------|
| Discovery | Repository | DiscoveryResult | Pattern Detection | ✅ (Confidence) | ❌ |
| Requirements | Documents | ProjectRequirements | Text Extraction | ❌ | ❌ |
| Generator | Discovery/Reqs | C4Model | Synthesis | ❌ | ❌ |
| Validation | C4Model | ValidationResult | Structural | ✅ (0-100) | ✅ |
| Security | C4Model | SecurityReport | Threat-Based | ✅ (0-100) | ✅ |
| **ArchChar** | C4Model + Chars | AnalysisResult | **Quality-Based** | ✅ **(Weighted)** | ✅ **(Detailed)** |
| Documentation | C4Model | Files | Generation | ❌ | ❌ |
| Terraform | C4Model | TF Config | Translation | ❌ | ❌ |

---

## Key Differentiators: ArchChar Agent

**Unique Capabilities**:
1. **Multi-Dimensional**: Analyzes 14 different characteristics simultaneously
2. **Weighted Scoring**: Ratings (critical/high/medium/low) affect scores
3. **Pattern-Based**: Recommendations tied to established architectural patterns
4. **Implementation Steps**: Detailed steps for each recommendation
5. **Technology Agnostic**: Suggests patterns first, then technologies
6. **Business-Aligned**: Maps technical gaps to business impact
7. **Comprehensive**: Covers operational, structural, and cross-cutting concerns

**Complements Other Agents**:
- **vs. Validation**: Functional adequacy vs. structural correctness
- **vs. Security**: Strategic security vs. tactical vulnerabilities
- **+Documentation**: Adds quality assessment to docs
- **+Terraform**: Informs what infrastructure to add

---

## When to Use Which Agent

### Start New Project
1. **Requirements Agent**: Extract requirements from docs
2. **Generator Agent**: Create initial C4 model
3. **ArchChar Agent**: Evaluate against NFRs/characteristics
4. **Validation Agent**: Ensure structural correctness

### Modernize Existing System
1. **Discovery Agent**: Understand current architecture
2. **Generator Agent**: Create C4 model
3. **ArchChar Agent**: Find gaps vs. target characteristics
4. **Security Agent**: Identify security issues
5. **Documentation Agent**: Document current state and roadmap

### Review Architecture
1. **Validation Agent**: Check structural integrity
2. **ArchChar Agent**: Evaluate quality vs. requirements
3. **Security Agent**: Deep security audit
4. **Documentation Agent**: Update docs with findings

### Deploy Architecture
1. **Terraform Agent**: Generate infrastructure
2. **Documentation Agent**: Create deployment guides
3. **Validation Agent**: Final check before deployment

---

## CLI Quick Reference

```bash
# Discovery
saat discover -p <repo> -o discovery.json
saat discover-requirements -f <docs> -o requirements.json

# Generation
saat generate -d discovery.json -o model.json
saat generate -r requirements.json -o model.json

# Analysis
saat validate-model -m model.json -f <framework>
saat security-scan -m model.json --threat-model
saat analyze-characteristics -m model.json -c characteristics.json

# Output
saat document -m model.json -o docs/ -f markdown,plantuml
saat generate-terraform -m model.json -p aws -o infrastructure/

# Full Pipeline
saat analyze -p <repo> --save-discovery -o architecture.json
```

---

## Python API Quick Reference

```python
from saat.agents import (
    DiscoveryAgent,
    RequirementsAgent,
    GeneratorAgent,
    ValidationAgent,
    SecurityAgent,
    ArchCharAnalysisAgent,
    DocumentationAgent,
    TerraformAgent
)

# Discovery
discovery_agent = DiscoveryAgent()
discovery = await discovery_agent.analyze_repository(repo_path)

# Requirements
req_agent = RequirementsAgent()
requirements = await req_agent.discover_requirements(file_paths)

# Generation
gen_agent = GeneratorAgent()
model = await gen_agent.generate_model(discovery)

# Analysis
val_agent = ValidationAgent()
validation = await val_agent.validate_model(model=model)

sec_agent = SecurityAgent()
security = await sec_agent.analyze_security(model=model)

archchar_agent = ArchCharAnalysisAgent()
analysis = await archchar_agent.analyze(model, archchar_input)

# Output
doc_agent = DocumentationAgent()
docs = await doc_agent.generate_documentation(model=model)

tf_agent = TerraformAgent()
terraform = await tf_agent.generate_terraform(model=model, provider="aws")
```

---

## MCP Tools (Claude Code Integration)

All agents available as MCP tools:
- `discover_architecture`
- `discover_requirements`
- `generate_c4_model`
- `validate_model`
- `analyze_security`
- **`analyze_architecture_characteristics`** (NEW)
- `generate_documentation`
- `generate_terraform`
- `full_analysis`

**Usage in Claude Code**:
```
"Analyze my architecture characteristics using the model.json and characteristics.json"
"Find security issues in my architecture"
"Generate documentation for my C4 model"
```

---

## Future Enhancements

### Planned Agent Improvements

**ArchChar Agent**:
- Custom characteristic support
- Trend tracking database
- Interactive HTML reports
- Cost-benefit analysis
- Auto-enhancement mode

**All Agents**:
- Parallel execution where possible
- Enhanced error recovery
- Better progress reporting
- Richer output formats

### New Agents Under Consideration

1. **Cost Estimation Agent**: Calculate infrastructure costs
2. **Performance Testing Agent**: Generate load test scenarios
3. **Migration Planning Agent**: Create migration roadmaps
4. **Compliance Audit Agent**: Comprehensive compliance checking
5. **Architecture Comparison Agent**: Compare multiple designs

---

## Support and Resources

**Documentation**:
- Full usage guides in `docs/`
- Examples in `examples/`
- API reference in source files

**Getting Help**:
- GitHub Issues: https://github.com/DavidROliverBA/SAAT/issues
- Documentation: https://github.com/DavidROliverBA/SAAT/tree/main/docs

**Contributing**:
- All agents follow `BaseAgentWithChecklist` pattern
- Use PydanticAI for consistency
- Include checklist generation
- Support auto-approve mode
- Comprehensive docstrings

---

**Last Updated**: 2025-11-02
**Total Agents**: 9 (8 existing + 1 new ArchChar)
**SAAT Version**: 2.0 (with ArchChar)
