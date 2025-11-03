# SAAT Agents Guide

Complete reference guide for all SAAT (Software Architecture Analysis Toolkit) agents and commands.

---

## Table of Contents

1. [Orchestrator Agent](#1-orchestrator-agent)
2. [Discovery Agent](#2-discovery-agent)
3. [Requirements Agent](#3-requirements-agent)
4. [Generation Agent](#4-generation-agent)
5. [Architecture Characteristics Analysis Agent](#5-architecture-characteristics-analysis-agent)
6. [Validation Agent](#6-validation-agent)
7. [Security Analysis Agent](#7-security-analysis-agent)
8. [Documentation Agent](#8-documentation-agent)
9. [Terraform Infrastructure Agent](#9-terraform-infrastructure-agent)
10. [Full Pipeline Agent](#10-full-pipeline-agent)
11. [Help Agent](#11-help-agent)
12. [Workflow Patterns](#workflow-patterns)

---

## 1. Orchestrator Agent

### Command
```
/saat-orchestrate
```

### What It Does
Your AI architecture consultant that acts as an intelligent entry point to the SAAT toolkit. It:
- **Understands your situation** through conversational interaction
- **Analyzes your needs** (brownfield vs greenfield, performance concerns, security, compliance, modernization)
- **Creates personalized plans** based on your specific requirements
- **Orchestrates other agents** to execute the complete workflow
- **Provides transparent updates** as each step executes
- **Delivers comprehensive results** with actionable recommendations

### When to Use
- **START HERE** if you're new to SAAT or unsure which command to use
- When you want a guided, conversational experience
- When your needs span multiple analysis types
- When you want a customized workflow based on your situation

### Inputs
- Description of your situation (analyzing existing system, designing new system, reviewing architecture)
- Specific concerns (performance, security, compliance, modernization, cost optimization)
- Optional: paths to code repositories, requirements documents, or existing models

### Result
- **Personalized execution plan** tailored to your needs
- **Progress updates** as each step completes
- **Comprehensive final report** including:
  - Architecture analysis results
  - Quality assessment scores
  - Security findings
  - Validation results
  - Actionable recommendations prioritized by impact

### Example Usage
```
/saat-orchestrate

Then respond to prompts like:
"I'm analyzing an existing e-commerce platform for security and performance issues"
"I need to design a new microservices architecture for a healthcare application"
```

---

## 2. Discovery Agent

### Command
```
/saat-discover <path-to-repository> [max-depth]
```

### What It Does
Automatically analyzes existing codebases (brownfield projects) to understand their architecture:
- **Scans repository structure** and file systems
- **Identifies technologies** (programming languages, frameworks, libraries, databases)
- **Detects architectural patterns** (microservices, monolith, layered, event-driven, etc.)
- **Finds services and entry points** (APIs, web apps, background jobs)
- **Generates confidence scores** for all findings
- **Creates comprehensive discovery report**

### When to Use
- Analyzing **existing codebases** (brownfield)
- Understanding architecture of inherited projects
- Documenting legacy systems
- Starting point for modernization projects
- Before generating C4 models from existing code

### Inputs
1. **Path to repository** (required) - absolute or relative path to codebase
2. **Maximum directory depth** (optional, default: 3) - how deep to scan

### Result
**Output File**: `discovery.json`

Contains:
- **Technologies found**: Programming languages, frameworks, databases, cloud services
- **Architectural patterns**: Detected patterns with confidence scores
- **Services identified**: Service names, types, entry points, dependencies
- **Confidence scores**: Reliability indicators for each finding
- **Complete discovery report**: Detailed analysis of repository structure

### Example Usage
```
/saat-discover /path/to/my-project 4
```

**Next Steps After Discovery**:
- `/saat-generate` - Create C4 model from discovery results
- `/saat-analyze-characteristics` - Analyze architecture quality
- `/saat-full-pipeline` - Run complete analysis workflow

---

## 3. Requirements Agent

### Command
```
/saat-requirements <path-to-documents> [project-name]
```

### What It Does
Extracts and structures requirements from documents for greenfield (new) projects:
- **Parses requirements documents** (markdown, text, Word, PDFs)
- **Extracts functional requirements** (REQ-F-001, REQ-F-002, ...)
- **Extracts non-functional requirements** (REQ-NF-001, REQ-NF-002, ...)
- **Creates user stories** (US-001, US-002, ...)
- **Identifies technical constraints** (CONST-001, CONST-002, ...)
- **Captures stakeholder information**
- **Performs quality checks** on extracted requirements

### When to Use
- Starting **new projects** (greenfield)
- Converting requirements documents to structured format
- Preparing inputs for architecture generation
- Creating architecture from business requirements

### Inputs
1. **Paths to requirements documents** (required) - can specify multiple files
2. **Project name** (optional) - defaults to filename

**Supported Formats**: Markdown (.md), Text (.txt), Word (.doc, .docx), any text-based format

### Result
**Output File**: `requirements.json`

Contains:
- **Functional Requirements** (REQ-F-001, REQ-F-002, ...) - what the system must do
- **Non-Functional Requirements** (REQ-NF-001, REQ-NF-002, ...) - quality attributes, performance, security
- **User Stories** (US-001, US-002, ...) - user-centric descriptions
- **Technical Constraints** (CONST-001, CONST-002, ...) - technology limitations, compliance needs
- **Stakeholders** - roles, concerns, priorities
- **Quality check report** - completeness and clarity assessment

**Pro Tip**: Non-functional requirements can be automatically converted to Architecture Characteristics for analysis.

### Example Usage
```
/saat-requirements ./requirements/business-requirements.md ./requirements/technical-spec.doc
```

**Next Steps After Requirements**:
- `/saat-generate` - Create C4 model from requirements
- `/saat-analyze-characteristics` - Analyze against quality attributes
- `/saat-document` - Generate architecture documentation

---

## 4. Generation Agent

### Command
```
/saat-generate <input-file>
```

### What It Does
Transforms discovery results or requirements into standardized C4 architecture models:
- **Loads input** from discovery (brownfield) or requirements (greenfield)
- **Creates C4 model** with multiple levels:
  - **Level 1 - Systems**: High-level system context, external dependencies
  - **Level 2 - Containers**: Applications, databases, message queues, services
  - **Level 3 - Components**: Internal modules, classes, packages within containers
  - **Relationships**: Connections between all elements with protocols
- **Assigns criticality levels** based on business impact and availability needs
- **Structures model** in standardized JSON format for downstream tools

### When to Use
- After running `/saat-discover` (brownfield)
- After running `/saat-requirements` (greenfield)
- When you need a standardized C4 model
- Before validation, security analysis, or documentation

### Inputs
**Either**:
- Path to `discovery.json` (from `/saat-discover`)

**Or**:
- Path to `requirements.json` (from `/saat-requirements`)

### Criticality Levels Assigned

| Level | Name | Uptime | Use Cases |
|-------|------|--------|-----------|
| **CS1** | Mission Critical | 99.99% | Payment processing, authentication, core business logic |
| **CS2** | Business Critical | 99.9% | Important customer-facing services, revenue-impacting features |
| **SL1** | Standard | 99.5% | Regular services, typical business operations |
| **SL2** | Medium | 99% | Supporting services, internal tools |
| **STANDARD** | Best Effort | - | Non-critical services, experimental features |

### Result
**Output File**: `architecture.json`

Contains complete C4 model:
- **Systems** array with external systems and dependencies
- **Containers** array with applications, databases, services
- **Components** array with internal modules and packages
- **Relationships** array with connections, protocols, purposes
- **Metadata** including project name, version, generation timestamp

### Example Usage
```
# From discovery (brownfield)
/saat-generate discovery.json

# From requirements (greenfield)
/saat-generate requirements.json
```

**Next Steps After Generation**:
- `/saat-analyze-characteristics` - Evaluate architecture quality
- `/saat-validate` - Check model correctness
- `/saat-security` - Analyze security posture
- `/saat-document` - Generate documentation
- `/saat-terraform` - Create infrastructure code

---

## 5. Architecture Characteristics Analysis Agent

### Command
```
/saat-analyze-characteristics <architecture-file> <characteristics-file>
```

### What It Does
Evaluates architecture quality against 14 standard architecture characteristics using Mark Richards' methodology:
- **Analyzes 14 characteristics** across 3 dimensions:
  - **Operational (7)**: Availability, Scalability, Performance, Security, Reliability, Fault Tolerance, Recoverability
  - **Structural (5)**: Maintainability, Testability, Deployability, Configurability, Extensibility
  - **Cross-Cutting (2)**: Interoperability, Usability
- **Identifies gaps** with severity levels (critical, high, medium, low)
- **Provides pattern-based recommendations** with concrete implementation steps
- **Generates weighted compliance scores** based on characteristic importance
- **Maps findings to affected components** for targeted improvements

### When to Use
- **Quality assessment** of architecture designs
- **Gap analysis** before implementation
- **Architecture reviews** and audits
- **Modernization planning** to identify improvement areas
- **Trade-off analysis** between different characteristics

### The 14 Architecture Characteristics

#### Operational Characteristics (7)
1. **Availability** - System uptime and accessibility
2. **Scalability** - Ability to handle growth
3. **Performance** - Response time and throughput
4. **Security** - Protection against threats
5. **Reliability** - Consistent correct behavior
6. **Fault Tolerance** - Continue operating despite failures
7. **Recoverability** - Restore after failures

#### Structural Characteristics (5)
8. **Maintainability** - Ease of making changes
9. **Testability** - Ease of testing
10. **Deployability** - Ease of deployment
11. **Configurability** - Ease of configuration changes
12. **Extensibility** - Ease of adding features

#### Cross-Cutting Characteristics (2)
13. **Interoperability** - Integration with other systems
14. **Usability** - User experience and ease of use

### Inputs
1. **Path to C4 model JSON** (required) - typically `architecture.json` from `/saat-generate`
2. **Path to characteristics JSON** (required) - defines target characteristics and importance

**Example characteristics file**: `examples/archchar-ecommerce.json`
**Characteristics capture tool**: https://github.com/DavidROliverBA/ArchCharCapture

### Result
**Output Files**:
- `archchar-analysis.md` - Human-readable report
- `archchar-analysis.json` - Machine-readable results

Contains:
- **Overall compliance score** (0-100, weighted by characteristic importance)
- **Per-characteristic scores** with status (met/not-met/partial)
- **Critical and high-priority gaps** requiring immediate attention
- **Top 10 recommendations** with:
  - Pattern name (e.g., "Circuit Breaker", "CQRS", "API Gateway")
  - Technology suggestions (specific tools and frameworks)
  - Detailed implementation steps
  - Trade-offs and rationale
  - Effort estimates (hours/days)
- **Architecture patterns recommended** for your context
- **Affected components** mapped to each finding

### Example Usage
```
/saat-analyze-characteristics architecture.json examples/archchar-ecommerce.json
```

**Sample Output**:
```
Overall Score: 72/100

Critical Gaps:
- Availability: No redundancy for payment service (CS1 criticality)
- Performance: Database not optimized for read-heavy workload
- Security: Missing authentication on admin API

Top Recommendations:
1. Implement Active-Active deployment for payment service
   Technologies: Kubernetes, AWS ELB, Database replication
   Steps: [detailed implementation guide]
   Effort: 3-5 days
```

---

## 6. Validation Agent

### Command
```
/saat-validate <architecture-file> [compliance-framework]
```

### What It Does
Validates C4 architecture models against structural standards and best practices:
- **Checks structural integrity**:
  - All relationship IDs reference valid elements
  - Containers reference valid systems
  - Components reference valid containers
  - No orphaned or unreachable elements
- **Validates completeness**:
  - All elements have descriptions
  - Critical systems (CS1/CS2) have assigned owners
  - Criticality levels appropriately assigned
  - Interfaces specified for all containers
- **Enforces best practices**:
  - Clear and consistent naming conventions
  - Proper criticality assignment based on function
  - External dependencies properly documented
  - Relationships specify protocols and purposes
- **Optional compliance checking** (PCI-DSS, HIPAA, GDPR, SOC2)

### When to Use
- **After generating** C4 models to ensure correctness
- **Before documentation** to catch errors early
- **Before infrastructure generation** to prevent misconfigurations
- **Architecture reviews** to verify completeness
- **Compliance audits** for regulatory requirements

### Inputs
1. **Path to C4 model JSON** (required) - typically `architecture.json`
2. **Compliance framework** (optional) - one of: `PCI-DSS`, `HIPAA`, `GDPR`, `SOC2`

### Result
**Output File**: `validation-report.json`

Contains:
- **Validation score** (0-100) - overall model quality
- **Issues by severity**:
  - **ERROR** - Must fix (breaks model integrity, prevents downstream tools from working)
  - **WARNING** - Should fix (missing best practices, reduces quality)
  - **INFO** - Consider fixing (suggestions for improvement)
- **Actionable suggestions** for each issue with:
  - Element affected
  - Specific problem description
  - How to fix
  - Why it matters
- **Compliance results** (if framework specified):
  - Requirements met/not met
  - Gaps with regulatory impact
  - Remediation guidance

### Example Issues Detected
- **ERROR**: Container "PaymentAPI" references non-existent system "PaymentGateway"
- **WARNING**: Critical container "AuthService" (CS1) has no owner assigned
- **INFO**: Relationship between "WebApp" and "Database" missing protocol specification

### Example Usage
```
# Basic validation
/saat-validate architecture.json

# With compliance check
/saat-validate architecture.json PCI-DSS
```

**Sample Output**:
```
Validation Score: 87/100

Errors: 2
- Container "PaymentAPI" references invalid system ID
- Component "UserAuth" orphaned (container doesn't exist)

Warnings: 5
- 3 CS1 containers missing owners
- 2 containers missing interface specifications

Info: 8
- 8 relationships missing protocol details
```

---

## 7. Security Analysis Agent

### Command
```
/saat-security <architecture-file> [--threat-modeling]
```

### What It Does
Deep security analysis to identify vulnerabilities and compliance gaps in architecture:

#### Security Checks Performed

**1. Encryption & Data Protection**
- Unencrypted communications (HTTP vs HTTPS, plain TCP)
- Unencrypted data at rest (databases, file storage)
- Missing encryption for sensitive data (PII, payment info, health records)
- Weak encryption algorithms (MD5, SHA1, outdated ciphers)

**2. Authentication & Authorization**
- Missing authentication on services
- Weak authentication (basic auth, no MFA)
- Missing authorization checks (RBAC, ABAC)
- Overly permissive access policies
- Default credentials or hardcoded secrets

**3. Data Flow Security**
- Sensitive data through insecure channels
- Logs containing sensitive data
- Data exfiltration risks
- Missing input validation
- SQL injection, XSS vulnerabilities

**4. Infrastructure Security**
- Public internet access to sensitive systems
- Missing network segmentation
- No firewalls or Web Application Firewall (WAF)
- Missing intrusion detection/prevention
- Unpatched components or outdated dependencies

**5. Compliance Requirements**
- PCI-DSS (payment data)
- HIPAA (health data)
- GDPR (personal data)
- SOC2 requirements

**6. Threat Modeling** (optional)
- Attack scenarios mapped to architecture
- Attack vectors and entry points
- Blast radius analysis
- Mitigation strategies

### When to Use
- **Security reviews** of architecture designs
- **Before production deployment** to catch vulnerabilities
- **Compliance audits** for regulatory requirements
- **Penetration test preparation** to identify attack surfaces
- **Security incident post-mortems** to prevent recurrence

### Inputs
1. **Path to C4 model JSON** (required) - typically `architecture.json`
2. **Threat modeling flag** (optional) - `--threat-modeling` for detailed attack scenarios

### Result
**Output File**: `security-report.json`

Contains:
- **Security score** (0-100) - overall security posture
- **Issues by severity**:
  - **CRITICAL** - Immediate risk, exploitable vulnerabilities
  - **HIGH** - Significant risk, should fix before production
  - **MEDIUM** - Moderate risk, fix in next sprint
  - **LOW** - Minor risk, improvement opportunity
- **Affected elements** for each issue (which systems/containers/components)
- **Detailed recommendations** with:
  - Specific vulnerability description
  - Attack scenarios (how it could be exploited)
  - Remediation steps (how to fix)
  - Technology suggestions (tools, frameworks, services)
  - Compliance impact (which regulations affected)
- **Threat model** (if enabled):
  - Attack trees
  - STRIDE analysis
  - Attack surface mapping

### Example Issues Detected
- **CRITICAL**: Payment API (CS1) accessible over HTTP - credit card data at risk
- **HIGH**: Database has public internet access - data breach risk
- **MEDIUM**: No rate limiting on login endpoint - brute force attack risk
- **LOW**: Security headers missing on web app - clickjacking risk

### Example Usage
```
# Basic security analysis
/saat-security architecture.json

# With threat modeling
/saat-security architecture.json --threat-modeling
```

**Sample Output**:
```
Security Score: 68/100

Critical Issues: 3
- PaymentAPI using HTTP (affects: payment-service, database)
- Database publicly accessible (affects: customer-db)
- No encryption at rest for PII (affects: user-data-store)

High Issues: 7
- Missing authentication on admin endpoints
- No Web Application Firewall
- Logs contain sensitive data
...

Recommendations:
1. Enable HTTPS/TLS 1.3 for PaymentAPI
   - Use AWS ACM or Let's Encrypt certificates
   - Configure TLS termination at load balancer
   - Redirect HTTP to HTTPS
   - Compliance Impact: PCI-DSS 4.1, GDPR Article 32
```

---

## 8. Documentation Agent

### Command
```
/saat-document <architecture-file> [output-dir] [formats]
```

### What It Does
Generates comprehensive architecture documentation suite from C4 models:

#### Documentation Generated

**1. Markdown Overviews**
- Project summary and goals
- System context description
- Technology stack with rationale
- Key architectural decisions
- Deployment overview

**2. C4 Diagrams**
- **System Context diagram** (Level 1) - actors, external systems, system boundaries
- **Container diagram** (Level 2) - applications, databases, services, communication
- **Component diagrams** (Level 3) - internal modules, packages, classes
- **Deployment diagram** - infrastructure, environments, network topology
- Available in PlantUML and Mermaid formats

**3. Architecture Decision Records (ADRs)**
- One ADR per major architectural decision
- Standard format: Context, Decision, Consequences
- Numbered sequentially (ADR-001, ADR-002, ...)
- Captures rationale and trade-offs

**4. Component Documentation**
- Per-component details:
  - Purpose and responsibilities
  - Interfaces and APIs
  - Technology choices and rationale
  - Dependencies
  - Configuration

**5. Deployment Documentation**
- Infrastructure requirements
- Scaling considerations
- Monitoring and alerting setup
- Disaster recovery procedures

### When to Use
- **After architecture generation** to create comprehensive docs
- **For onboarding** new team members
- **For stakeholder communication** (technical and non-technical)
- **For compliance documentation** requirements
- **For knowledge transfer** and handoff

### Inputs
1. **Path to C4 model JSON** (required) - typically `architecture.json`
2. **Output directory** (optional, default: `docs/`) - where to create documentation
3. **Formats** (optional, default: all) - comma-separated list:
   - `markdown` - Overview and component docs
   - `plantuml` - C4 diagrams as PlantUML
   - `mermaid` - C4 diagrams as Mermaid
   - `adr` - Architecture Decision Records

### Result
**Output Directory Structure**:
```
docs/
├── README.md                    # Project overview
├── ARCHITECTURE.md              # Detailed architecture documentation
├── diagrams/                    # C4 diagrams
│   ├── system-context.puml      # PlantUML system context
│   ├── system-context.mmd       # Mermaid system context
│   ├── container.puml           # PlantUML container diagram
│   ├── container.mmd            # Mermaid container diagram
│   ├── component-*.puml         # Component diagrams
│   └── deployment.puml          # Deployment diagram
├── adr/                         # Architecture Decision Records
│   ├── ADR-001-technology-stack.md
│   ├── ADR-002-microservices-pattern.md
│   └── ADR-003-database-choice.md
├── components/                  # Per-component documentation
│   ├── payment-service.md
│   ├── user-service.md
│   └── notification-service.md
└── deployment/                  # Deployment guides
    ├── infrastructure.md
    ├── monitoring.md
    └── scaling.md
```

### Example Usage
```
# Generate all documentation formats
/saat-document architecture.json

# Custom output directory
/saat-document architecture.json ./project-docs

# Only markdown and mermaid
/saat-document architecture.json ./docs markdown,mermaid
```

### Viewing Diagrams
- **PlantUML (.puml)**: Use PlantUML extension in VS Code, or https://www.plantuml.com/plantuml/
- **Mermaid (.mmd)**: View in GitHub, VS Code with Mermaid extension, or https://mermaid.live/

---

## 9. Terraform Infrastructure Agent

### Command
```
/saat-terraform <architecture-file> [cloud-provider] [region] [output-dir]
```

### What It Does
Generates production-ready Terraform infrastructure-as-code from C4 architecture models:

#### Infrastructure Generated

**1. Compute Resources**
- Maps containers to cloud compute:
  - **AWS**: EC2 instances, ECS, Lambda
  - **Azure**: App Service, Container Instances, Functions
  - **GCP**: Compute Engine, Cloud Run, Cloud Functions
- Auto-scaling configurations based on criticality
- Load balancers and target groups

**2. Data Resources**
- Managed databases:
  - **AWS**: RDS (PostgreSQL, MySQL, SQL Server)
  - **Azure**: Azure SQL Database, Cosmos DB
  - **GCP**: Cloud SQL, Firestore
- Object storage:
  - **AWS**: S3 buckets
  - **Azure**: Blob Storage
  - **GCP**: Cloud Storage
- Caching layers (Redis, Memcached)

**3. Messaging & Queues**
- Message queues:
  - **AWS**: SQS, SNS
  - **Azure**: Service Bus, Event Grid
  - **GCP**: Pub/Sub
- Event streaming (Kafka, Kinesis)

**4. Networking**
- VPC/VNet with subnets (public, private, data)
- Security groups / Network Security Groups
- NAT gateways for private subnet internet access
- Load balancers (ALB, NLB, Application Gateway)
- DNS and domain configuration

**5. Monitoring & Logging**
- CloudWatch / Application Insights / Cloud Monitoring
- Log aggregation and retention
- Alarms based on criticality:
  - **CS1**: CPU > 70%, latency > 200ms, error rate > 0.1%
  - **CS2**: CPU > 80%, latency > 500ms, error rate > 1%
  - **SL1/SL2**: CPU > 90%, basic health checks

**6. Security**
- IAM roles and policies
- Encryption at rest and in transit
- Secret management (AWS Secrets Manager, Azure Key Vault, GCP Secret Manager)
- Security group rules (least privilege)

#### Criticality-Based Configurations

| Criticality | Deployment | Auto-Scaling | Backups | Alarms |
|-------------|-----------|--------------|---------|---------|
| **CS1** (Mission Critical) | Multi-AZ | min=2, max=10 | 35 days | Tight thresholds (CPU>70%, latency>200ms) |
| **CS2** (Business Critical) | Multi-AZ | min=2, max=5 | 7 days | Moderate thresholds (CPU>80%, latency>500ms) |
| **SL1** (Standard) | Single-AZ | min=1, max=3 | 3 days | Basic health checks |
| **SL2** (Medium) | Single-AZ | Fixed (1-2) | 1 day | Basic monitoring |
| **STANDARD** | Best effort | Fixed (1) | None | Optional monitoring |

### When to Use
- **Infrastructure provisioning** for new projects
- **Infrastructure as Code (IaC)** modernization
- **Multi-environment deployment** (dev, staging, prod)
- **Disaster recovery** setup
- **Cloud migration** planning

### Inputs
1. **Path to C4 model JSON** (required) - typically `architecture.json`
2. **Cloud provider** (optional, default: `aws`) - one of: `aws`, `azure`, `gcp`
3. **Region** (optional, default: `us-east-1`) - cloud region for deployment
4. **Output directory** (optional, default: `infrastructure/`) - where to create Terraform files

### Result
**Output Directory Structure**:
```
infrastructure/
├── main.tf           # Main Terraform configuration with all resources
├── variables.tf      # Configurable variables (region, environment, instance types)
├── outputs.tf        # Resource outputs (endpoints, IDs, connection strings)
├── provider.tf       # Provider configuration (AWS/Azure/GCP)
├── networking.tf     # VPC, subnets, security groups, load balancers
├── monitoring.tf     # CloudWatch/monitoring resources, alarms, dashboards
├── backend.tf        # Terraform state backend configuration
└── README.md         # Deployment instructions and prerequisites
```

### Deployment Steps
```bash
cd infrastructure/

# Initialize Terraform
terraform init

# Review planned changes
terraform plan

# Apply infrastructure
terraform apply

# (Later) Destroy infrastructure
terraform destroy
```

### Example Usage
```
# AWS deployment (default)
/saat-terraform architecture.json

# Azure deployment in West Europe
/saat-terraform architecture.json azure westeurope

# GCP deployment with custom output directory
/saat-terraform architecture.json gcp us-central1 ./infra
```

**Prerequisites**:
- Cloud provider CLI installed and configured (AWS CLI, Azure CLI, gcloud)
- Terraform installed (version 1.0+)
- Appropriate cloud credentials and permissions

---

## 10. Full Pipeline Agent

### Command
```
/saat-full-pipeline <repository-path> [characteristics-file] [output-dir] [cloud-provider]
```

### What It Does
Runs the complete SAAT analysis workflow in a single command - ideal for comprehensive architecture assessments:

#### Pipeline Stages

**1. Discovery** (Brownfield Analysis)
- Analyzes codebase structure
- Identifies technologies and patterns
- Detects services and dependencies
- Output: `discovery.json`

**2. C4 Model Generation**
- Creates standardized architecture model
- Maps systems, containers, components
- Assigns criticality levels
- Output: `architecture.json`

**3. Architecture Characteristics Analysis**
- Evaluates 14 quality characteristics
- Identifies gaps and recommendations
- Generates compliance scores
- Output: `archchar-analysis.md`, `archchar-analysis.json`

**4. Validation**
- Checks model structural integrity
- Validates completeness
- Enforces best practices
- Output: `validation-report.json`

**5. Security Analysis**
- Identifies vulnerabilities
- Checks compliance (PCI-DSS, HIPAA, GDPR, SOC2)
- Provides remediation guidance
- Output: `security-report.json`

**6. Documentation Generation**
- Creates markdown docs
- Generates C4 diagrams (PlantUML, Mermaid)
- Writes Architecture Decision Records
- Output: `docs/` directory

**7. Infrastructure as Code**
- Generates Terraform configurations
- Maps to cloud resources
- Applies criticality-based settings
- Output: `infrastructure/` directory

### When to Use
- **New project assessments** - comprehensive analysis from scratch
- **Architecture reviews** - complete evaluation of existing systems
- **Modernization planning** - understand current state, plan future state
- **Compliance audits** - full security and compliance assessment
- **Documentation generation** - create complete documentation suite
- **Quick comprehensive analysis** - one command to do everything

### Inputs
1. **Repository path** (required) - path to codebase to analyze
2. **Architecture characteristics file** (optional) - define quality targets
   - If not provided, uses sensible defaults for all 14 characteristics
   - Example file: `examples/archchar-ecommerce.json`
3. **Output directory** (optional, default: `saat-output/`) - where to create all outputs
4. **Cloud provider** (optional, default: `aws`) - for Terraform generation: `aws`, `azure`, `gcp`

### Result
**Output Directory Structure**:
```
saat-output/
├── discovery.json                  # Discovery results
├── architecture.json               # C4 model
├── archchar-analysis.md            # Architecture characteristics report (human-readable)
├── archchar-analysis.json          # Architecture characteristics (machine-readable)
├── validation-report.json          # Validation results
├── security-report.json            # Security audit
├── docs/                           # Complete documentation
│   ├── README.md                   # Project overview
│   ├── ARCHITECTURE.md             # Architecture details
│   ├── diagrams/                   # C4 diagrams (PlantUML, Mermaid)
│   │   ├── system-context.puml
│   │   ├── container.puml
│   │   └── component-*.puml
│   ├── adr/                        # Architecture Decision Records
│   │   ├── ADR-001-*.md
│   │   └── ADR-002-*.md
│   └── components/                 # Component documentation
│       └── *.md
└── infrastructure/                 # Terraform IaC
    ├── main.tf
    ├── variables.tf
    ├── networking.tf
    ├── monitoring.tf
    └── README.md
```

### Execution Time
- **Small projects** (< 100 files): 2-3 minutes
- **Medium projects** (100-1000 files): 5-7 minutes
- **Large projects** (> 1000 files): 10-15 minutes

### Example Usage
```
# Basic full pipeline with defaults
/saat-full-pipeline /path/to/my-project

# With custom characteristics and output directory
/saat-full-pipeline /path/to/my-project ./my-characteristics.json ./analysis-results

# Azure deployment
/saat-full-pipeline /path/to/my-project ./characteristics.json ./output azure
```

### Best For
- Complete architecture assessments
- Initial project analysis
- Architecture review meetings
- Compliance documentation
- Modernization kickoffs

---

## 11. Help Agent

### Command
```
/saat-help
```

### What It Does
Interactive help system providing:
- **List of all SAAT commands** with descriptions
- **Typical workflow patterns** (brownfield, greenfield, quick assessment, architecture review)
- **Links to detailed documentation**
- **Architecture characteristics explanation**
- **Command usage examples**
- **Getting started guide**

### When to Use
- **First time using SAAT** - understand available commands
- **Forgot command syntax** - quick reference
- **Want to see workflows** - understand how commands fit together
- **Need examples** - see usage patterns

### Result
Displays:
- Command reference with syntax
- Workflow diagrams
- Links to guides
- Example commands

### Example Usage
```
/saat-help
```

---

## Workflow Patterns

### Brownfield Workflow (Existing Project)

For analyzing and documenting **existing codebases**:

```
1. /saat-discover <repo-path>
      ↓
   Generates: discovery.json
      ↓
2. /saat-generate discovery.json
      ↓
   Generates: architecture.json
      ↓
3. /saat-analyze-characteristics architecture.json characteristics.json
      ↓
   Generates: archchar-analysis.md, archchar-analysis.json
      ↓
4. /saat-validate architecture.json
      ↓
   Generates: validation-report.json
      ↓
5. /saat-security architecture.json
      ↓
   Generates: security-report.json
      ↓
6. /saat-document architecture.json
      ↓
   Generates: docs/ directory
      ↓
7. /saat-terraform architecture.json aws
      ↓
   Generates: infrastructure/ directory
```

**Use Cases**:
- Legacy system documentation
- Architecture reviews
- Modernization planning
- Technical debt assessment

---

### Greenfield Workflow (New Project)

For designing **new systems** from requirements:

```
1. /saat-requirements <requirements-docs>
      ↓
   Generates: requirements.json
      ↓
2. /saat-generate requirements.json
      ↓
   Generates: architecture.json
      ↓
3. /saat-analyze-characteristics architecture.json characteristics.json
      ↓
   Generates: archchar-analysis.md, archchar-analysis.json
      ↓
4. /saat-validate architecture.json
      ↓
   Generates: validation-report.json
      ↓
5. /saat-document architecture.json
      ↓
   Generates: docs/ directory
      ↓
6. /saat-terraform architecture.json aws
      ↓
   Generates: infrastructure/ directory
```

**Use Cases**:
- New project design
- RFP responses
- Proof of concepts
- Architecture proposals

---

### Quick Assessment Workflow

For **rapid comprehensive analysis**:

```
/saat-full-pipeline <repo-path> [characteristics.json]
   ↓
Generates: Complete analysis in saat-output/
- discovery.json
- architecture.json
- archchar-analysis.md & .json
- validation-report.json
- security-report.json
- docs/
- infrastructure/
```

**Use Cases**:
- Initial project assessment
- Time-constrained reviews
- Executive briefings
- Vendor evaluation

---

### Architecture Review Workflow

For **quality and security assessment** of existing models:

```
Start with: architecture.json (existing C4 model)
   ↓
1. /saat-analyze-characteristics architecture.json characteristics.json
   ↓
2. /saat-validate architecture.json [PCI-DSS|HIPAA|GDPR|SOC2]
   ↓
3. /saat-security architecture.json --threat-modeling
   ↓
Review: All analysis reports for issues and recommendations
```

**Use Cases**:
- Pre-deployment reviews
- Compliance audits
- Security assessments
- Quality gate validation

---

### Orchestrated Workflow (Guided)

For **conversational, personalized** experience:

```
/saat-orchestrate
   ↓
Answer questions about:
- Your situation (analyzing/designing/reviewing)
- Project type (brownfield/greenfield)
- Concerns (performance/security/compliance/cost)
- Specific goals
   ↓
Orchestrator creates custom plan
   ↓
Executes appropriate commands automatically
   ↓
Provides comprehensive results
```

**Use Cases**:
- First-time SAAT users
- Complex scenarios
- Multiple stakeholder concerns
- Unclear starting point

---

## Key Features Summary

### Architecture Characteristics (14 Total)

**Operational (7)**
- Availability, Scalability, Performance, Security, Reliability, Fault Tolerance, Recoverability

**Structural (5)**
- Maintainability, Testability, Deployability, Configurability, Extensibility

**Cross-Cutting (2)**
- Interoperability, Usability

### Compliance Frameworks Supported
- **PCI-DSS** - Payment Card Industry Data Security Standard
- **HIPAA** - Health Insurance Portability and Accountability Act
- **GDPR** - General Data Protection Regulation
- **SOC2** - Service Organization Control 2

### Multi-Cloud Support
- **AWS** - Amazon Web Services
- **Azure** - Microsoft Azure
- **GCP** - Google Cloud Platform

### Documentation Formats
- **Markdown** - Human-readable documentation
- **PlantUML** - Diagram as code (industry standard)
- **Mermaid** - Markdown-native diagrams (GitHub-friendly)
- **ADR** - Architecture Decision Records (standard format)

### Criticality Levels
| Level | Uptime | Use Case |
|-------|--------|----------|
| CS1 | 99.99% | Mission critical (payment, auth) |
| CS2 | 99.9% | Business critical (customer-facing) |
| SL1 | 99.5% | Standard services |
| SL2 | 99% | Supporting services |
| STANDARD | Best effort | Non-critical |

---

## Quick Start Guide

### For Existing Projects (Brownfield)
```bash
# Option 1: Guided experience
/saat-orchestrate

# Option 2: Full automated pipeline
/saat-full-pipeline /path/to/your/project

# Option 3: Step-by-step control
/saat-discover /path/to/your/project
/saat-generate discovery.json
/saat-analyze-characteristics architecture.json examples/archchar-ecommerce.json
/saat-validate architecture.json
/saat-security architecture.json
/saat-document architecture.json
/saat-terraform architecture.json aws
```

### For New Projects (Greenfield)
```bash
# Option 1: Guided experience
/saat-orchestrate

# Option 2: From requirements
/saat-requirements ./requirements/business-requirements.md
/saat-generate requirements.json
/saat-analyze-characteristics architecture.json characteristics.json
/saat-validate architecture.json
/saat-document architecture.json
/saat-terraform architecture.json azure
```

### For Architecture Reviews
```bash
# Assuming you have architecture.json already
/saat-analyze-characteristics architecture.json characteristics.json
/saat-validate architecture.json PCI-DSS
/saat-security architecture.json --threat-modeling
```

---

## Getting Help

- **In-tool help**: `/saat-help`
- **Command-specific help**: Each command provides guidance when run
- **Examples**: Check `examples/` directory for sample files
- **Architecture Characteristics Tool**: https://github.com/DavidROliverBA/ArchCharCapture

---

## Tips and Best Practices

1. **Start with `/saat-orchestrate`** if you're unsure which command to use
2. **Use `/saat-full-pipeline`** for quick comprehensive assessments
3. **Always run `/saat-validate`** before generating documentation or infrastructure
4. **Run `/saat-security`** before production deployments
5. **Use architecture characteristics** to set quality targets early
6. **Version control** all generated JSON files for tracking changes
7. **Review recommendations** from characteristics analysis - they provide concrete implementation guidance
8. **Check validation reports** - fix errors before proceeding
9. **Customize** characteristics.json to match your specific quality targets
10. **Iterate** - update architecture.json based on analysis findings and re-run

---

*Generated by SAAT (Software Architecture Analysis Toolkit)*
