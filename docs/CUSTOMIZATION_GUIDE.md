# Customization Guide: Tailoring SAAT to Your Needs

**Learn how to customize SAAT agents, add your own rules, and extend functionality**

---

## 📋 Table of Contents

- [Overview](#overview)
- [Customizing Agents](#customizing-agents)
- [Adding Custom Architecture Characteristics](#adding-custom-architecture-characteristics)
- [Custom Validation Rules](#custom-validation-rules)
- [Custom Security Rules](#custom-security-rules)
- [Creating Custom Agents](#creating-custom-agents)
- [Customizing Prompts](#customizing-prompts)
- [Configuration Files](#configuration-files)
- [Examples](#examples)

---

## Overview

SAAT is designed to be customizable. You can:

✅ **Customize agent behavior** - Adjust how agents analyze your code
✅ **Add custom characteristics** - Define your own quality metrics
✅ **Add validation rules** - Enforce your organization's standards
✅ **Create custom security rules** - Check for company-specific vulnerabilities
✅ **Build custom agents** - Add entirely new capabilities
✅ **Modify prompts** - Change how agents communicate
✅ **Configure defaults** - Set organizational preferences

---

## Customizing Agents

###  Configuration File

Create a `.saat/config.yaml` in your project or home directory:

```yaml
# .saat/config.yaml

# Global settings
settings:
  default_model: "anthropic:claude-sonnet-4"
  auto_approve: false
  max_depth: 5  # How deep to analyze directories

# Agent-specific customization
agents:
  discovery:
    ignore_patterns:
      - "*.test.js"
      - "*.spec.ts"
      - "node_modules/*"
      - "vendor/*"
      - ".git/*"

    focus_patterns:
      - "src/**/*.java"
      - "lib/**/*.rb"

    max_file_size: 1000000  # Skip files > 1MB

  generator:
    default_criticality: "CS2"
    prefer_microservices: true

  archchar:
    # Custom weighting for characteristics
    weights:
      availability: 5      # Extra important (default: 4)
      scalability: 5       # Extra important
      security: 5          # Extra important
      maintainability: 3
      testability: 3

    # Custom thresholds
    thresholds:
      critical_gap: 40     # Score <40 = critical
      high_gap: 60         # Score <60 = high priority
      medium_gap: 75       # Score <75 = medium

  validation:
    frameworks:
      - "PCI-DSS"
      - "HIPAA"
      - "SOC2"
      - "GDPR"
      - "CUSTOM-COMPANY-STANDARD"  # Your own!

  security:
    severity_threshold: "medium"  # Report medium and above
    include_low_priority: false

  documentation:
    default_formats:
      - "markdown"
      - "plantuml"

    include_adr: true
    adr_template: ".saat/templates/adr.md"
```

### Environment Variables

```bash
# Model configuration
export SAAT_MODEL="anthropic:claude-sonnet-4"
export ANTHROPIC_API_KEY="your-key"

# Behavior
export SAAT_AUTO_APPROVE="false"
export SAAT_MAX_DEPTH="5"

# Output
export SAAT_OUTPUT_DIR="./saat-output"
export SAAT_LOG_LEVEL="INFO"  # DEBUG, INFO, WARNING, ERROR
```

---

## Adding Custom Architecture Characteristics

### Create Custom Characteristic

Create `.saat/characteristics/cost-efficiency.yaml`:

```yaml
# Custom characteristic: Cost Efficiency
name: "Cost Efficiency"
category: "operational"
weight: 3  # Medium importance
description: "How well the architecture minimizes operational costs"

# What to look for
indicators:
  positive:
    - "Using serverless/Lambda functions"
    - "Auto-scaling configured"
    - "Using spot instances"
    - "Caching implemented"
    - "Database connection pooling"
    - "CDN for static assets"
    - "Appropriate instance sizing"

  negative:
    - "Always-on expensive instances"
    - "No auto-scaling"
    - "Over-provisioned resources"
    - "Redundant data processing"
    - "Inefficient queries"
    - "No caching"

# Scoring guidance
scoring:
  fully_compliant: "90-100"
  criteria:
    - "Serverless where appropriate"
    - "Auto-scaling on all services"
    - "Cost monitoring configured"
    - "Resource right-sized"

  mostly_compliant: "70-89"
  criteria:
    - "Some auto-scaling"
    - "Some cost optimization"

  partially_compliant: "40-69"
  criteria:
    - "Minimal cost optimization"
    - "Over-provisioned"

  non_compliant: "0-39"
  criteria:
    - "No cost optimization"
    - "Wasteful resource usage"

# Recommendations by score range
recommendations:
  low_score:  # <60
    - pattern: "Auto-Scaling"
      description: "Implement auto-scaling to match demand"
      effort: "3 days"
      impact: "30-50% cost reduction during low traffic"

    - pattern: "Serverless"
      description: "Move infrequent workloads to Lambda"
      effort: "5 days"
      impact: "Pay only for actual usage"

    - pattern: "Spot Instances"
      description: "Use spot instances for non-critical workloads"
      effort: "2 days"
      impact: "Up to 90% savings on compute"

  medium_score:  # 60-80
    - pattern: "CDN"
      description: "Add CloudFront for static assets"
      effort: "1 day"
      impact: "Reduce bandwidth costs 40-60%"
```

### Use Custom Characteristic

```bash
# Via CLI
saat analyze-characteristics \
  -m architecture.json \
  -c .saat/characteristics/cost-efficiency.yaml \
  -o analysis.json

# Via Orchestrator
/saat-orchestrate

You: Also analyze cost efficiency using my custom characteristic

Orchestrator: I see you have a custom "Cost Efficiency" characteristic.
              I'll include that in the analysis...
```

### Create Characteristic Set

For multiple custom characteristics, create a set:

`.saat/characteristic-sets/fintech.yaml`:

```yaml
# Characteristic set for financial services
name: "FinTech Quality Standards"
description: "Quality characteristics for financial technology systems"

# Include standard characteristics
include_standard:
  - availability
  - security
  - reliability
  - recoverability
  - maintainability
  - testability

# Include custom characteristics
include_custom:
  - cost-efficiency      # From above
  - audit-readiness     # Another custom one
  - regulatory-compliance
  - data-accuracy
  - transaction-integrity

# Adjust weights for fintech priorities
weights:
  security: 5            # Critical
  reliability: 5         # Critical
  audit-readiness: 4
  transaction-integrity: 4
  availability: 4
  cost-efficiency: 2     # Less important than security/reliability
```

---

## Custom Validation Rules

### Create Company Standard

`.saat/validation/company-standard.yaml`:

```yaml
name: "Acme Corp Architecture Standards"
version: "2.0"
category: "internal"

requirements:

  - id: "ACME-001"
    name: "All services must use company logging framework"
    category: "observability"
    severity: "high"
    description: |
      All microservices must integrate with our centralized
      logging system (ELK stack).

    check:
      type: "dependency"
      looks_for:
        - "acme-logging-sdk"
        - "acme-logger"

    pass_criteria: "Logging SDK found in dependencies"
    fail_criteria: "No logging SDK found"

    remediation: |
      Add to pom.xml:
      <dependency>
        <groupId>com.acme</groupId>
        <artifactId>acme-logging-sdk</artifactId>
        <version>2.1.0</version>
      </dependency>

  - id: "ACME-002"
    name: "Databases must be in private subnets"
    category: "security"
    severity: "critical"
    description: "Databases cannot be publicly accessible"

    check:
      type: "infrastructure"
      looks_for:
        database_public: false
        subnet_type: "private"

  - id: "ACME-003"
    name: "All APIs must have rate limiting"
    category: "security"
    severity: "high"

    check:
      type: "code_pattern"
      looks_for:
        - "@RateLimit"
        - "RateLimiter"
        - "throttle"

  - id: "ACME-004"
    name: "Services must have health check endpoint"
    category: "operations"
    severity: "high"

    check:
      type: "api"
      endpoint: "/health"
      required: true

  - id: "ACME-005"
    name: "Minimum test coverage: 70%"
    category: "quality"
    severity: "medium"

    check:
      type: "metric"
      metric: "test_coverage"
      threshold: 70
      operator: ">="
```

### Use Custom Validation

```bash
# Via CLI
saat validate-model \
  -m architecture.json \
  -f ACME-CORP-STANDARD \
  --custom-rules .saat/validation/company-standard.yaml

# Via Orchestrator
/saat-orchestrate

You: Validate against our company standards

Orchestrator: [Loads .saat/validation/company-standard.yaml]
              Checking against Acme Corp Architecture Standards v2.0...

              Results:
              ✅ ACME-001: Logging framework present
              ❌ ACME-002: Database in public subnet (CRITICAL)
              ✅ ACME-003: Rate limiting configured
              ⚠️  ACME-004: Health endpoint missing on 2/5 services
              ❌ ACME-005: Test coverage only 45% (need 70%)

              Overall: 3/5 passed, 2 critical issues
```

---

## Custom Security Rules

### Create Security Rules

`.saat/security/custom-rules.yaml`:

```yaml
name: "Acme Corp Security Rules"
description: "Company-specific security requirements"

rules:

  - id: "SEC-ACME-001"
    name: "No hardcoded API keys from our partners"
    severity: "critical"
    category: "secrets"

    patterns:
      # Regex patterns to detect
      - 'acme_api_key\s*=\s*["\'][\w-]+'
      - 'ACME_SECRET\s*=\s*["\'][\w-]+'
      - 'partner_key_\d+\s*=\s*["\'][\w-]+'

    remediation: |
      Move API keys to AWS Secrets Manager or environment variables.
      Never commit API keys to source control.

  - id: "SEC-ACME-002"
    name: "Must use company SSO for authentication"
    severity: "high"
    category: "authentication"

    check:
      type: "dependency"
      required:
        - "acme-sso-client"
        - "okta-spring-boot-starter"  # We use Okta

  - id: "SEC-ACME-003"
    name: "Sensitive data must be encrypted at rest"
    severity: "critical"
    category: "data-protection"

    applies_to:
      - "User"
      - "Payment"
      - "Customer"
      - "Account"

    check:
      type: "annotation"
      looks_for:
        - "@Encrypted"
        - "@EncryptedField"

  - id: "SEC-ACME-004"
    name: "Admin endpoints must require MFA"
    severity: "high"
    category: "authorization"

    check:
      type: "annotation"
      on_paths: ["/admin/*", "/api/admin/*"]
      requires:
        - "@RequiresMFA"
        - "@MFAProtected"
```

---

## Creating Custom Agents

### Build a Custom Agent

Create `.saat/agents/cost_analyzer.py`:

```python
"""
Custom Agent: Cost Analyzer
Analyzes architecture and estimates cloud costs
"""

from pydantic_ai import Agent
from saat.agents.base import BaseAgentWithChecklist
from saat.models import C4Model
from pydantic import BaseModel
from typing import List

class CostEstimate(BaseModel):
    """Cost estimate for a service"""
    service_name: str
    service_type: str  # "compute", "database", "storage", etc.
    monthly_cost_min: float
    monthly_cost_max: float
    assumptions: List[str]
    optimization_opportunities: List[str]

class CostAnalysisResult(BaseModel):
    """Overall cost analysis result"""
    total_monthly_min: float
    total_monthly_max: float
    breakdown: List[CostEstimate]
    recommendations: List[str]
    roi_analysis: str

class CostAnalyzerAgent(BaseAgentWithChecklist):
    """Agent that analyzes and estimates infrastructure costs"""

    def __init__(self, model_name: str = "anthropic:claude-sonnet-4"):
        super().__init__(
            name="CostAnalyzer",
            model_name=model_name,
            result_type=CostAnalysisResult
        )

    async def analyze_costs(
        self,
        model: C4Model,
        cloud_provider: str = "aws",
        region: str = "us-east-1",
        auto_approve: bool = False
    ) -> CostAnalysisResult:
        """
        Analyze architecture and estimate monthly costs

        Args:
            model: C4 architecture model
            cloud_provider: Cloud provider (aws, azure, gcp)
            region: Cloud region
            auto_approve: Skip checklist approval

        Returns:
            CostAnalysisResult with estimates and recommendations
        """

        # Generate checklist
        checklist_items = [
            f"Analyze each container in {model.name}",
            f"Estimate costs for {cloud_provider} in {region}",
            "Calculate compute costs (instances, serverless)",
            "Calculate database costs",
            "Calculate storage costs",
            "Calculate data transfer costs",
            "Identify cost optimization opportunities",
            "Provide ROI analysis"
        ]

        # Show checklist and get approval
        if not auto_approve:
            approved = await self._show_checklist_and_approve(
                checklist_items,
                f"Cost analysis for {model.name}"
            )
            if not approved:
                raise ValueError("Cost analysis cancelled by user")

        # Run analysis
        prompt = f"""
        Analyze this architecture and estimate monthly cloud costs.

        Architecture: {model.model_dump_json()}
        Cloud Provider: {cloud_provider}
        Region: {region}

        For each container (service), estimate:
        1. Compute costs (EC2, ECS, Lambda, etc.)
        2. Database costs (RDS, DynamoDB, etc.)
        3. Storage costs (S3, EBS, etc.)
        4. Data transfer costs
        5. Other services (load balancers, API Gateway, etc.)

        Consider:
        - Container criticality (CS1 = more expensive, needs HA)
        - Estimated traffic/load
        - Storage requirements
        - Backup retention

        Provide:
        - Min/max cost range (accounts for variable traffic)
        - Cost optimization opportunities
        - ROI analysis comparing costs to business value

        Use actual {cloud_provider} pricing for {region}.
        """

        result = await self.agent.run(prompt)

        return result.data

# Register the custom agent
__all__ = ['CostAnalyzerAgent']
```

### Use Custom Agent

```python
# In your code
from saat.agents.cost_analyzer import CostAnalyzerAgent
from saat.models import C4Model
import json

# Load architecture
with open('architecture.json') as f:
    model_dict = json.load(f)
    model = C4Model(**model_dict)

# Analyze costs
cost_agent = CostAnalyzerAgent()
result = await cost_agent.analyze_costs(
    model=model,
    cloud_provider="aws",
    region="us-east-1",
    auto_approve=False
)

print(f"Estimated monthly cost: ${result.total_monthly_min} - ${result.total_monthly_max}")
print(f"\nRecommendations:")
for rec in result.recommendations:
    print(f"  - {rec}")
```

### Register with CLI

Add to `saat/cli.py`:

```python
from saat.agents.cost_analyzer import CostAnalyzerAgent

@cli.command()
@click.option('--model-file', '-m', required=True, help='C4 model JSON file')
@click.option('--provider', '-p', default='aws', help='Cloud provider')
@click.option('--region', '-r', default='us-east-1', help='Cloud region')
@click.option('--output', '-o', help='Output file for cost analysis')
@click.pass_context
async def analyze_costs(ctx, model_file, provider, region, output):
    """Analyze architecture and estimate cloud costs"""

    # Load model
    with open(model_file) as f:
        model_dict = json.load(f)
        model = C4Model(**model_dict)

    # Run cost analysis
    agent = CostAnalyzerAgent(model_name=ctx.obj['model'])
    result = await agent.analyze_costs(
        model=model,
        cloud_provider=provider,
        region=region,
        auto_approve=ctx.obj['auto_approve']
    )

    # Output
    click.echo(f"\n💰 Cost Analysis for {model.name}")
    click.echo(f"   Estimated Monthly Cost: ${result.total_monthly_min:,.2f} - ${result.total_monthly_max:,.2f}")

    # Save to file
    if output:
        with open(output, 'w') as f:
            f.write(result.model_dump_json(indent=2))
        click.echo(f"   Saved to: {output}")
```

Now you can use:

```bash
saat analyze-costs -m architecture.json -p aws -r us-east-1 -o costs.json
```

---

## Customizing Prompts

### Override Agent Prompts

Create `.saat/prompts/discovery-agent.txt`:

```
You are analyzing a codebase for {company_name}.

Focus on:
1. Finding services and components
2. Understanding data flows
3. Identifying {company_tech_stack} patterns
4. Looking for {company_specific_patterns}

Special attention to:
- {compliance_requirements}
- Integration with {company_systems}

Please discover the architecture and provide a detailed analysis.
```

### Use Custom Prompts

```python
# saat/agents/discovery.py

class DiscoveryAgent(BaseAgentWithChecklist):
    def __init__(self, model_name: str = "anthropic:claude-sonnet-4"):
        # Load custom prompt if exists
        custom_prompt_path = Path(".saat/prompts/discovery-agent.txt")
        if custom_prompt_path.exists():
            self.prompt_template = custom_prompt_path.read_text()
        else:
            self.prompt_template = self.DEFAULT_PROMPT

        super().__init__(...)

    def _build_prompt(self, **kwargs):
        # Fill in template
        return self.prompt_template.format(
            company_name=kwargs.get('company_name', 'Your Organization'),
            company_tech_stack=kwargs.get('tech_stack', 'standard'),
            # ... etc
        )
```

---

## Configuration Files

### Project-Level Config

Create `.saat/config.yaml` in your project:

```yaml
# Project-specific configuration
project:
  name: "PaymentProcessor"
  version: "2.0"
  team: "Platform Engineering"

settings:
  # Override global settings for this project
  auto_approve: false
  max_depth: 10  # Deeper analysis for this project

characteristics:
  # This project prioritizes these
  focus:
    - security
    - reliability
    - compliance

  weights:
    security: 5
    reliability: 5
    availability: 4
    compliance: 4

validation:
  # Always check these frameworks
  required_frameworks:
    - "PCI-DSS"
    - "SOC2"
    - "ACME-CORP-STANDARD"

documentation:
  # Custom templates for this project
  templates:
    adr: ".saat/templates/adr-template.md"
    readme: ".saat/templates/readme-template.md"
```

### Global Config

Create `~/.saat/config.yaml` for all projects:

```yaml
# Global SAAT configuration
settings:
  default_model: "anthropic:claude-sonnet-4"
  auto_approve: false

  # Your organization's defaults
  company:
    name: "Acme Corp"
    tech_stack:
      - "Java"
      - "Spring Boot"
      - "PostgreSQL"
      - "Redis"
      - "AWS"

  # Paths to organization-wide customizations
  custom:
    characteristics: "~/.saat/characteristics/"
    validation: "~/.saat/validation/"
    security: "~/.saat/security/"
    agents: "~/.saat/agents/"
```

---

## Examples

### Example 1: Custom "Data Quality" Characteristic

`.saat/characteristics/data-quality.yaml`:

```yaml
name: "Data Quality"
category: "operational"
weight: 3
description: "How well the architecture ensures data accuracy and consistency"

indicators:
  positive:
    - "Input validation on all APIs"
    - "Database constraints (NOT NULL, UNIQUE, FK)"
    - "Data quality monitoring"
    - "Automated data validation pipelines"
    - "Referential integrity enforced"
    - "Data lineage tracking"

  negative:
    - "No input validation"
    - "Weak database constraints"
    - "Data inconsistencies possible"
    - "No data quality monitoring"

recommendations:
  low_score:
    - pattern: "API Input Validation"
      description: "Add comprehensive input validation"
      effort: "3 days"

    - pattern: "Database Constraints"
      description: "Add NOT NULL, UNIQUE, and FK constraints"
      effort: "2 days"
```

### Example 2: Custom "Mobile App" Validation

`.saat/validation/mobile-standards.yaml`:

```yaml
name: "Mobile App Backend Standards"
version: "1.0"

requirements:
  - id: "MOBILE-001"
    name: "APIs must support pagination"
    severity: "high"
    description: "Mobile apps need pagination for large datasets"

  - id: "MOBILE-002"
    name: "Response payload must be < 100KB"
    severity: "medium"
    description: "Keep responses small for mobile bandwidth"

  - id: "MOBILE-003"
    name: "Must support offline-first architecture"
    severity: "high"
    description: "Mobile apps need to work offline"

    check:
      looks_for:
        - "Sync endpoint"
        - "Conflict resolution"
        - "Local cache"
```

### Example 3: Custom "ML Model" Agent

```python
# .saat/agents/ml_model_analyzer.py

class MLModelAnalyzerAgent(BaseAgentWithChecklist):
    """Analyzes ML models in the architecture"""

    async def analyze_ml_models(self, model: C4Model):
        """
        Find ML models in architecture and analyze:
        - Model versioning
        - A/B testing capability
        - Model monitoring
        - Retraining pipelines
        - Inference performance
        """
        # Implementation...
```

### Example 4: Industry-Specific Characteristic Set

`.saat/characteristic-sets/healthcare.yaml`:

```yaml
name: "Healthcare Systems Quality"

include_standard:
  - security
  - reliability
  - availability
  - recoverability
  - maintainability

include_custom:
  - hipaa-readiness
  - data-privacy
  - audit-trail
  - patient-safety
  - interoperability

# Healthcare systems prioritize compliance and safety
weights:
  security: 5
  patient-safety: 5
  hipaa-readiness: 5
  data-privacy: 5
  reliability: 4
  availability: 4
```

---

## Best Practices

### 1. Start Simple

Don't customize everything at once:
1. Start with config.yaml (simple settings)
2. Add 1-2 custom characteristics
3. Add company validation rules
4. Build custom agents only when needed

### 2. Version Your Customizations

```bash
# Keep customizations in git
saat-customizations/
├── .saat/
│   ├── config.yaml
│   ├── characteristics/
│   ├── validation/
│   └── security/
└── README.md  # Document your customizations
```

### 3. Share Across Team

```bash
# Clone org customizations
git clone git@github.com:acme/saat-config.git ~/.saat

# Or symlink per-project
ln -s ~/saat-customizations/acme-corp/.saat .saat
```

### 4. Test Customizations

```bash
# Test custom characteristic
saat analyze-characteristics \
  -m test-architecture.json \
  -c .saat/characteristics/your-custom.yaml

# Verify it works before sharing with team
```

### 5. Document Your Customizations

```markdown
# Acme Corp SAAT Customizations

## Custom Characteristics
- **cost-efficiency**: Analyzes cloud cost optimization
- **data-quality**: Checks data validation and consistency

## Custom Validation
- **acme-corp-standard**: Our internal architecture standards

## Usage
```bash
# Use with orchestrator
/saat-orchestrate
"Use our company standards"
```
```

---

## Related Guides

- **[Greenfield Guide](GREENFIELD_GUIDE.md)** - Designing new systems
- **[Brownfield Guide](BROWNFIELD_GUIDE.md)** - Analyzing existing code
- **[Architecture Characteristics Guide](ARCHITECTURE_CHARACTERISTICS_USAGE.md)** - Quality analysis

---

**Happy Customizing! 🎨🔧**
