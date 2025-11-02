# Architecture Characteristics Analysis - Usage Guide

**Author**: SAAT (Solution Architecture Agent Toolkit)
**Version**: 1.0.0
**Last Updated**: 2025-11-02

---

## Overview

The Architecture Characteristics Analysis Agent evaluates C4 architecture models against specified architecture characteristics using Mark Richards' methodology from "Fundamentals of Software Architecture." It identifies gaps, provides recommendations, and generates compliance scores.

### What are Architecture Characteristics?

Architecture characteristics (also called "non-functional requirements" or "-ilities") define **how well** a system performs its functions under real-world conditions. They include:

- **Operational**: Availability, Scalability, Performance, Reliability, Fault Tolerance, Recoverability
- **Structural**: Maintainability, Testability, Deployability, Configurability, Extensibility
- **Cross-cutting**: Security, Interoperability, Usability

### Key Principle: The Rule of 7

Mark Richards recommends identifying **no more than 7 driving characteristics** to focus architectural decisions. Too many characteristics lead to conflicts and dilute focus.

---

## Features

✅ **14 Standard Characteristics**: Complete analysis for all characteristics from Mark Richards' framework
✅ **Custom Characteristics Support**: Analyze domain-specific characteristics beyond the standard 14
✅ **Gap Analysis**: Identify missing infrastructure, patterns, and configurations
✅ **Pattern Recommendations**: Get specific architectural patterns to address gaps
✅ **Technology Suggestions**: Concrete technology recommendations with implementation steps
✅ **Compliance Scoring**: Weighted scoring based on characteristic importance (critical, high, medium, low)
✅ **Multiple Output Formats**: Markdown reports and JSON for automation
✅ **CLI Integration**: Command-line tool for easy use
✅ **MCP Integration**: Seamless integration with Claude Code

---

## Quick Start

### Prerequisites

1. **C4 Model**: Your architecture model in SAAT's C4 JSON format
2. **ArchCharCapture JSON**: Architecture characteristics from [ArchCharCapture](https://github.com/DavidROliverBA/ArchCharCapture)
3. **API Key**: Anthropic API key for Claude

```bash
export ANTHROPIC_API_KEY=your-api-key
```

### Using CLI

```bash
# Analyze with both markdown and JSON output
saat analyze-characteristics \
  -m architecture.json \
  -c archchar.json \
  -o analysis-report

# Markdown only
saat analyze-characteristics \
  -m architecture.json \
  -c archchar.json \
  -f markdown \
  -o report.md

# Auto-approve mode (skip prompts)
saat -y analyze-characteristics \
  -m architecture.json \
  -c archchar.json
```

### Using Python API

```python
import asyncio
from pathlib import Path
from saat.converters_archchar import import_archchar_json
from saat.agents.archchar import analyze_architecture_characteristics, save_report
from saat.models import C4Model

async def analyze():
    # Load models
    c4_model = C4Model(**json.loads(Path("model.json").read_text()))
    archchar = import_archchar_json("archchar.json")

    # Run analysis
    result = await analyze_architecture_characteristics(
        c4_model=c4_model,
        archchar_input=archchar,
        auto_approve=True
    )

    # Save reports
    save_report(result, "report.md", format="markdown")
    save_report(result, "report.json", format="json")

    # Access results programmatically
    print(f"Score: {result.overall_score}/100")
    print(f"Critical Gaps: {len(result.critical_gaps)}")

    for rec in result.top_recommendations[:5]:
        print(f"- {rec.title} ({rec.priority} priority)")

asyncio.run(analyze())
```

### Using MCP with Claude Code

The analysis tool is available as an MCP tool in Claude Code:

```
Analyze the architecture characteristics in my-model.json against archchar.json
```

Claude will automatically:
1. Load both files
2. Run the analysis
3. Save reports to your workspace
4. Display summary with key findings

---

## Creating ArchCharCapture JSON

### Option 1: Use ArchCharCapture Web Tool

1. Visit [ArchCharCapture](https://github.com/DavidROliverBA/ArchCharCapture)
2. Select relevant characteristics for your system
3. Choose your top 7 driving characteristics
4. Add ratings (critical, high, medium, low) and notes
5. Export to JSON

### Option 2: Create Manually

```json
{
  "projectName": "My System",
  "architect": "Your Name",
  "date": "2025-11-02",
  "notes": "System notes and context",
  "characteristics": [
    {
      "id": "char_001",
      "name": "Availability",
      "description": "System uptime and accessibility",
      "selected": true,
      "isTop": true,
      "rating": "critical",
      "notes": "99.99% uptime required",
      "isCustom": false
    }
    // ... more characteristics
  ],
  "topCharacteristics": [
    // Top 7 characteristics (subset of above with isTop: true)
  ]
}
```

### Option 3: Use Example Function

```python
from saat.converters_archchar import create_example_archchar, export_archchar_json

# Create example with typical e-commerce characteristics
example = create_example_archchar()

# Customize as needed
example.projectName = "My Project"
example.notes = "Custom notes"

# Export
export_archchar_json(example, "my-archchar.json")
```

---

## Understanding the Analysis

### Analysis Process

The agent performs these steps for each selected characteristic:

1. **Container Analysis**: Examines C4 containers for relevant infrastructure
2. **Relationship Analysis**: Checks dependencies and integrations
3. **Pattern Detection**: Identifies missing architectural patterns
4. **Gap Identification**: Documents specific gaps with severity levels
5. **Recommendation Generation**: Provides pattern-based solutions with technologies
6. **Scoring**: Calculates compliance score based on gaps and rating

### Scoring System

**Score Calculation**:
- Starts at 100 points per characteristic
- Deducts points based on gap severity:
  - Critical gap: -30 points
  - High gap: -20 points
  - Medium gap: -10 points
  - Low gap: -5 points
- Extra penalty for critical-rated characteristics below 70 points

**Overall Score**:
- Weighted average based on characteristic ratings:
  - Critical: 4x weight
  - High: 3x weight
  - Medium: 2x weight
  - Low: 1x weight

**Compliance Status**:
- 90-100: **Compliant** ✅
- 70-89: **Mostly Compliant** ⚠️
- 50-69: **Partially Compliant** 🟡
- 0-49: **Non-Compliant** ❌

### Gap Severity Levels

- **Critical**: Immediate attention required, system success at risk
- **High**: Should be addressed soon, significant impact
- **Medium**: Should be improved, moderate impact
- **Low**: Nice to have, minimal impact

---

## Report Output

### Markdown Report Structure

```markdown
# Architecture Characteristics Analysis Report

## Executive Summary
Overall score and high-level findings

## Overall Compliance Score
Visual score bar and percentage

## ⚠️ Critical Gaps
Detailed critical issues requiring immediate attention

## High Priority Gaps
Important issues to address soon

## Top Recommendations
Top 10 actionable recommendations with:
- Pattern names
- Technologies
- Implementation steps
- Trade-offs
- Effort estimates

## Detailed Analysis by Characteristic
Per-characteristic breakdown with:
- Score and status
- All gaps identified
- All recommendations

## Architecture Patterns Recommended
List of all recommended patterns

## Technologies Recommended
List of all suggested technologies
```

### JSON Report Structure

```json
{
  "project_name": "string",
  "architect": "string",
  "overall_score": 85,
  "characteristics_analyzed": 14,
  "analyses": [
    {
      "characteristic_name": "Availability",
      "score": 75,
      "compliance_status": "mostly_compliant",
      "gaps": [...],
      "recommendations": [...]
    }
  ],
  "critical_gaps": [...],
  "top_recommendations": [...],
  "architecture_patterns_recommended": [...],
  "technologies_recommended": [...]
}
```

---

## Examples

See the `examples/` directory for:

1. **archchar-ecommerce.json**: Example characteristics for e-commerce platform
2. **c4-ecommerce.json**: Example C4 model of e-commerce architecture
3. **analyze_archchar.py**: Complete Python example with detailed output

Run the example:

```bash
cd examples
./analyze_archchar.py
```

---

## Best Practices

### When to Use

✅ **Architecture Reviews**: Validate designs against business requirements
✅ **Greenfield Projects**: Ensure critical characteristics are addressed from the start
✅ **Modernization**: Identify gaps when migrating to new architectures
✅ **Compliance**: Verify adherence to architectural standards
✅ **Decision Support**: Compare architectural options objectively

### Tips for Effective Analysis

1. **Be Specific in Notes**: Add concrete requirements in characteristic notes
   - ❌ "High availability needed"
   - ✅ "99.99% uptime (52 min downtime/year), RTO < 5 min"

2. **Limit to 7 Top Characteristics**: Focus on what truly matters
   - Too many characteristics lead to conflicting recommendations

3. **Use Correct Ratings**: Be honest about importance
   - **Critical**: System fails without it
   - **High**: Significant business impact
   - **Medium**: Important but not critical
   - **Low**: Nice to have

4. **Iterate**: Run analysis multiple times as architecture evolves
   - Track score improvements over time
   - Use JSON output for trend analysis

5. **Act on Critical Gaps First**: Prioritize by severity
   - Critical gaps require immediate action
   - High-priority gaps should be in next sprint
   - Medium/Low can be backlog items

---

## Characteristic Analysis Details

### Availability
**Checks for**:
- Redundancy in critical containers
- Load balancing infrastructure
- Database clustering/replication
- Multi-region deployment

**Common Recommendations**:
- Active-Active or Active-Passive clustering
- Cloud Load Balancers (ALB, NLB)
- Database replication (RDS Multi-AZ, PostgreSQL replication)

### Scalability
**Checks for**:
- Auto-scaling capabilities
- Caching infrastructure (Redis, Memcached)
- Database scalability (read replicas, sharding)
- Message queues for async processing

**Common Recommendations**:
- Kubernetes HPA, AWS Auto Scaling
- ElastiCache, Redis Cluster
- Database read replicas, CQRS pattern
- Kafka, RabbitMQ, SQS

### Performance
**Checks for**:
- CDN for static content
- Application caching
- Database optimization
- Async processing for long operations

**Common Recommendations**:
- CloudFront, Cloudflare, Akamai
- Redis, Memcached for app caching
- Database indexing, query optimization
- Background job processors

### Security
**Checks for**:
- HTTPS/TLS encryption
- API Gateway with authentication
- Secrets management
- Database encryption at rest

**Common Recommendations**:
- API Gateway with OAuth/JWT
- HashiCorp Vault, AWS Secrets Manager
- TLS everywhere, encryption at rest
- WAF, DDoS protection

### (... and 10 more characteristics)

See [ARCHITECTURE_CHARACTERISTICS_REFERENCE.md](./ARCHITECTURE_CHARACTERISTICS_REFERENCE.md) for complete details on all 14 characteristics.

---

## Troubleshooting

### "No analysis tools found for characteristic X"

**Cause**: Custom characteristic not in the standard 14

**Solution**: Standard characteristics are:
- Availability, Scalability, Performance, Security, Reliability
- Fault Tolerance, Recoverability, Maintainability, Testability
- Deployability, Configurability, Extensibility, Interoperability, Usability

Custom characteristics are skipped in analysis. Rename to match standard names if possible.

### "Analysis taking too long"

**Cause**: Analyzing many characteristics or large models

**Solution**:
- Use `--auto-approve` / `-y` flag to skip prompts
- Reduce number of selected characteristics
- Ensure good network connection to Anthropic API

### "Low scores across all characteristics"

**Cause**: C4 model may lack implementation details

**Solution**:
- Add container technologies (databases, caches, load balancers)
- Add relationships between containers
- Add interfaces with protocols (HTTPS, PostgreSQL, etc.)
- Use sizing hints (CS1, SL1, etc.) for critical containers

---

## Integration with Other SAAT Tools

### Complete Workflow

```bash
# 1. Discover architecture
saat discover -p ./my-app -o discovery.json

# 2. Generate C4 model
saat generate -d discovery.json -o model.json

# 3. Validate model
saat validate-model -m model.json

# 4. Security analysis
saat security-scan -m model.json

# 5. Architecture characteristics analysis
saat analyze-characteristics -m model.json -c archchar.json

# 6. Generate documentation
saat document -m model.json

# 7. Generate infrastructure
saat generate-terraform -m model.json -p aws
```

---

## API Reference

See [archchar.py](../saat/agents/archchar.py) for complete API documentation.

### Key Functions

- `analyze_architecture_characteristics()`: Main analysis function
- `generate_markdown_report()`: Create markdown report
- `export_json_report()`: Create JSON report
- `save_report()`: Save report to file
- `import_archchar_json()`: Load ArchCharCapture file
- `create_example_archchar()`: Generate example characteristics

### Key Models

- `ArchCharInput`: Input characteristics from ArchCharCapture
- `ArchCharAnalysisResult`: Complete analysis results
- `CharacteristicAnalysis`: Per-characteristic analysis
- `CharacteristicGap`: Identified gap
- `CharacteristicRecommendation`: Actionable recommendation

---

## References

- **Fundamentals of Software Architecture** (2nd Edition, 2024) - Mark Richards, Neal Ford
- [ArchCharCapture](https://github.com/DavidROliverBA/ArchCharCapture) - Web tool for capturing characteristics
- [Mark Richards' Architecture Characteristics Worksheet](https://www.developertoarchitect.com)
- [ARCHITECTURE_CHARACTERISTICS_REFERENCE.md](./ARCHITECTURE_CHARACTERISTICS_REFERENCE.md) - Detailed reference
- [ARCHCHAR_JSON_FORMAT.md](./ARCHCHAR_JSON_FORMAT.md) - JSON format specification

---

## Support

For issues or questions:
- GitHub Issues: https://github.com/DavidROliverBA/SAAT/issues
- Documentation: https://github.com/DavidROliverBA/SAAT/tree/main/docs

---

**Last Updated**: 2025-11-02
**Version**: 1.0.0
