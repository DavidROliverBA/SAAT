---
description: Show all available SAAT commands and workflows
---

# SAAT (Solution Architecture Agent Toolkit) - Available Commands

I can help you with architecture discovery, generation, analysis, validation, security, documentation, and infrastructure-as-code!

## 🔍 Discovery & Requirements

- `/saat-discover` - Discover architecture from existing codebase (brownfield)
- `/saat-requirements` - Extract requirements from documents (greenfield)

## 🏗️ Generation & Analysis

- `/saat-generate` - Generate C4 architecture model
- `/saat-analyze-characteristics` - **NEW!** Analyze architecture quality against 14 characteristics
- `/saat-validate` - Validate model structural correctness
- `/saat-security` - Analyze security posture and vulnerabilities

## 📖 Documentation & Infrastructure

- `/saat-document` - Generate comprehensive documentation
- `/saat-terraform` - Generate Terraform infrastructure-as-code

## 🚀 Complete Workflows

- `/saat-full-pipeline` - Run everything: discover → generate → analyze → validate → secure → document → deploy

## 📋 Typical Workflows

### Brownfield (Existing Project)
```
/saat-discover              # Analyze existing code
/saat-generate              # Create C4 model
/saat-analyze-characteristics  # Evaluate quality
/saat-validate              # Check correctness
/saat-security              # Security audit
/saat-document              # Generate docs
/saat-terraform             # Create IaC
```

### Greenfield (New Project)
```
/saat-requirements          # Extract requirements
/saat-generate              # Create C4 model from requirements
/saat-analyze-characteristics  # Validate against NFRs
/saat-validate              # Check model
/saat-document              # Generate docs
/saat-terraform             # Create infrastructure
```

### Quick Assessment
```
/saat-full-pipeline         # Do everything at once!
```

### Architecture Review
```
/saat-analyze-characteristics  # Quality analysis
/saat-validate              # Structural check
/saat-security              # Security review
```

## 🎯 NEW: Architecture Characteristics Analysis

The `/saat-analyze-characteristics` command evaluates your architecture against:

**Operational (7)**: Availability, Scalability, Performance, Security, Reliability, Fault Tolerance, Recoverability

**Structural (5)**: Maintainability, Testability, Deployability, Configurability, Extensibility

**Cross-Cutting (2)**: Interoperability, Usability

**You get:**
- Overall quality score (0-100, weighted)
- Per-characteristic scores and compliance status
- Critical gaps requiring immediate attention
- Pattern-based recommendations with implementation steps
- Technology suggestions
- Detailed reports (Markdown + JSON)

## 📚 Documentation

All commands are documented with examples in:
- `docs/AGENTS_QUICK_REFERENCE.md` - All agents overview
- `docs/ARCHITECTURE_CHARACTERISTICS_USAGE.md` - ArchChar detailed guide
- `docs/ARCHCHAR_INTEGRATION_ANALYSIS.md` - Integration patterns
- `examples/` - Working examples

## 🎓 Need Help?

Just type any command and I'll guide you through it! I'll ask for any required information and explain what I'm doing at each step.

**Examples:**
- "Run a full SAAT analysis on this repository"
- "Analyze my architecture characteristics"
- "Generate documentation for my C4 model"
- "What's wrong with my architecture security?"

**Which command would you like to try first?**
