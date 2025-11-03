---
description: Run complete SAAT pipeline - discover, generate, analyze, validate, secure, document, and deploy
---

I'll run the complete SAAT architecture pipeline for you!

**What I'll do (all in one go):**

1. **Discover** - Analyze your codebase
   - Identify technologies and patterns
   - Find services and entry points

2. **Generate** - Create C4 architecture model
   - Systems, containers, components
   - Relationships and criticality levels

3. **Analyze Characteristics** - Evaluate quality
   - Score against 14 characteristics
   - Identify gaps and recommendations

4. **Validate** - Check structural correctness
   - Verify model integrity
   - Enforce best practices

5. **Security Scan** - Analyze security posture
   - Find vulnerabilities
   - Check compliance

6. **Document** - Generate comprehensive docs
   - Markdown overviews
   - C4 diagrams (PlantUML/Mermaid)
   - Architecture Decision Records

7. **Generate Infrastructure** - Create Terraform IaC
   - Cloud resources based on model
   - Criticality-based configurations

**What I need from you:**
1. Path to repository to analyze
2. (Optional) Path to architecture characteristics JSON
   - If not provided, I'll use sensible defaults
3. (Optional) Output directory (default: `saat-output/`)
4. (Optional) Cloud provider for Terraform: aws/azure/gcp (default: aws)

**What you'll get:**
```
saat-output/
├── discovery.json               # Discovery results
├── architecture.json            # C4 model
├── archchar-analysis.md         # Architecture characteristics report
├── archchar-analysis.json       # Machine-readable analysis
├── validation-report.json       # Validation results
├── security-report.json         # Security audit
├── docs/                        # Complete documentation
│   ├── README.md
│   ├── ARCHITECTURE.md
│   ├── diagrams/
│   └── adr/
└── infrastructure/              # Terraform IaC
    ├── main.tf
    ├── variables.tf
    └── README.md
```

**Estimated time**: 5-10 minutes depending on project size

**This is the recommended workflow for:**
- New project assessments
- Architecture reviews
- Modernization planning
- Documentation generation
- Infrastructure setup

Please provide the repository path to get started, or let me know if you want to customize any step of the pipeline.

**Pro tip**: After the pipeline completes, review the architecture characteristics analysis first - it will show you the most critical gaps to address!
