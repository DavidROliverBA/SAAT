# SAAT Slash Commands for Claude Code

This directory contains slash commands that make SAAT agents incredibly easy to use in Claude Code CLI!

## 🚀 Quick Start

### Installation (Automatic)

From the SAAT repository root:
```bash
# Copy commands to your home directory
./install-claude-commands.sh
```

Or manually:
```bash
# Copy to Claude Code's global commands directory
cp -r .claude/commands/* ~/.claude/commands/
```

### Installation (Per-Project)

If you want these commands only for this project:
```bash
# They're already here in .claude/commands/
# Claude Code will automatically find them when you're in this directory
```

## 📋 Available Commands

Once installed, just type `/` in Claude Code to see all commands, or type `/saat` to see SAAT-specific commands:

### Discovery & Requirements
- `/saat-discover` - Analyze existing codebase
- `/saat-requirements` - Extract requirements from documents

### Generation & Analysis
- `/saat-generate` - Create C4 architecture model
- `/saat-analyze-characteristics` - **NEW!** Evaluate architecture quality
- `/saat-validate` - Validate model structure
- `/saat-security` - Security analysis

### Documentation & Infrastructure
- `/saat-document` - Generate comprehensive docs
- `/saat-terraform` - Generate Terraform IaC

### Complete Workflows
- `/saat-full-pipeline` - Run everything at once
- `/saat-help` - Show all SAAT commands

## 💡 How It Works

1. **Type the command**: Just type `/saat-` and Claude Code will autocomplete
2. **Follow the prompts**: Each command explains what it needs
3. **Provide inputs**: Give file paths or configuration when asked
4. **Get results**: Commands automatically call the right MCP tools and format results

## 🎯 Example Usage

### Analyze Your Architecture

```
You: /saat-analyze-characteristics

Claude: I'll help you analyze your architecture against specified characteristics...
        What I need from you:
        1. Path to your C4 model JSON file
        2. Path to your architecture characteristics JSON file

You: The model is in architecture.json and characteristics are in characteristics.json

Claude: [Runs analysis using MCP tool]
        ✅ Analysis complete!
        Overall Score: 72/100 (Mostly Compliant)

        Critical Gaps (2):
        - Availability: No load balancer for critical services
        - Scalability: Missing auto-scaling configuration

        Top Recommendations (showing 3 of 8):
        1. Implement active-active clustering with load balancing
        2. Configure Kubernetes HPA for auto-scaling
        3. Add Redis caching layer for performance

        Full reports saved to:
        - archchar-analysis.md
        - archchar-analysis.json
```

### Run Full Pipeline

```
You: /saat-full-pipeline

Claude: I'll run the complete SAAT architecture pipeline!
        What I need: Path to repository to analyze

You: Analyze the current directory

Claude: [Runs discover → generate → analyze → validate → secure → document → deploy]
        ✅ Complete analysis finished!

        All outputs saved to: saat-output/
        - discovery.json
        - architecture.json
        - archchar-analysis.md (Score: 68/100)
        - validation-report.json (Score: 85/100)
        - security-report.json (Score: 71/100)
        - docs/ (comprehensive documentation)
        - infrastructure/ (Terraform IaC)

        🎯 Next Steps:
        1. Review archchar-analysis.md for critical gaps
        2. Fix the 3 critical security issues
        3. Run terraform apply to deploy
```

## 🔧 Customization

You can edit any command file in `.claude/commands/` to customize:
- The prompts and explanations
- Default values
- Output formats
- Workflow steps

## 📚 Command Details

### `/saat-discover`
Analyzes existing codebase to discover architecture.

**Inputs**: Repository path, max depth
**Outputs**: `discovery.json` with technologies, patterns, confidence scores
**Next**: `/saat-generate`, `/saat-full-pipeline`

### `/saat-requirements`
Extracts structured requirements from documents.

**Inputs**: Document paths, project name
**Outputs**: `requirements.json` with functional/non-functional requirements, user stories
**Next**: `/saat-generate` with requirements

### `/saat-generate`
Creates C4 architecture model from discovery or requirements.

**Inputs**: `discovery.json` or `requirements.json`
**Outputs**: `architecture.json` with complete C4 model
**Next**: `/saat-analyze-characteristics`, `/saat-validate`, `/saat-security`

### `/saat-analyze-characteristics` ⭐ NEW
Evaluates architecture quality against 14 standard characteristics.

**Inputs**:
- C4 model JSON (`architecture.json`)
- Architecture characteristics JSON (`characteristics.json`)

**Outputs**:
- `archchar-analysis.md` - Detailed report with gaps and recommendations
- `archchar-analysis.json` - Machine-readable results

**Analyzes**:
- **Operational** (7): Availability, Scalability, Performance, Security, Reliability, Fault Tolerance, Recoverability
- **Structural** (5): Maintainability, Testability, Deployability, Configurability, Extensibility
- **Cross-Cutting** (2): Interoperability, Usability

**Provides**:
- Overall quality score (0-100, weighted by importance)
- Per-characteristic scores and compliance status
- Critical and high-priority gaps
- Pattern-based recommendations with implementation steps
- Technology suggestions
- Trade-offs and effort estimates

**Next**: Fix critical gaps, update model, re-analyze

### `/saat-validate`
Validates C4 model structural correctness.

**Inputs**: C4 model JSON, optional compliance framework
**Outputs**: `validation-report.json` with issues and score
**Next**: Fix errors, `/saat-security`, `/saat-document`

### `/saat-security`
Analyzes security posture and finds vulnerabilities.

**Inputs**: C4 model JSON, optional threat modeling
**Outputs**: `security-report.json` with issues by severity
**Next**: Fix critical issues, update model

### `/saat-document`
Generates comprehensive architecture documentation.

**Inputs**: C4 model JSON, output directory, formats
**Outputs**: Multiple files in `docs/`:
- Markdown overviews
- C4 diagrams (PlantUML/Mermaid)
- Architecture Decision Records (ADRs)
- Component documentation

**Next**: Review and publish docs

### `/saat-terraform`
Generates Terraform infrastructure-as-code.

**Inputs**: C4 model JSON, cloud provider, region
**Outputs**: Terraform files in `infrastructure/`:
- `main.tf` with all resources
- `variables.tf`, `outputs.tf`
- Networking and monitoring configs

**Next**: `terraform init`, `terraform plan`, `terraform apply`

### `/saat-full-pipeline`
Runs complete workflow: discover → generate → analyze → validate → secure → document → deploy.

**Inputs**: Repository path, optional characteristics, output directory
**Outputs**: Everything in `saat-output/`:
- All analysis results
- Complete documentation
- Terraform infrastructure

**Best for**: New project assessments, architecture reviews, complete audits

### `/saat-help`
Shows all available SAAT commands with examples.

**No inputs needed** - just shows the command list and workflows

## 🎓 Tips for Best Results

1. **Start with the right command**:
   - Existing project? `/saat-discover`
   - New project? `/saat-requirements`
   - Quick review? `/saat-full-pipeline`

2. **Use characteristics analysis early**:
   - Run `/saat-analyze-characteristics` after generating model
   - Fix critical gaps before implementation
   - Re-analyze to confirm improvements

3. **Create characteristics from requirements**:
   - Extract Non-Functional Requirements
   - Map to standard characteristics
   - Set ratings (critical/high/medium/low) based on priority

4. **Iterate**:
   - Generate → Analyze → Fix → Re-analyze
   - Track score improvements over time
   - Use recommendations as roadmap

5. **Combine with other commands**:
   - After `/saat-analyze-characteristics`, run `/saat-terraform` to get infrastructure with recommended components
   - Include analysis results in `/saat-document` output

## 🔗 Integration with MCP Tools

These slash commands are friendly wrappers around SAAT's MCP tools. They:
- Provide context and guidance
- Ask for inputs conversationally
- Call the appropriate MCP tool
- Format results nicely
- Suggest next steps

**MCP tools used**:
- `discover_architecture`
- `discover_requirements`
- `generate_c4_model`
- `validate_model`
- `analyze_security`
- `analyze_architecture_characteristics` ⭐ NEW
- `generate_documentation`
- `generate_terraform`
- `full_analysis`

## 📖 Further Reading

- `docs/AGENTS_QUICK_REFERENCE.md` - All SAAT agents overview
- `docs/ARCHITECTURE_CHARACTERISTICS_USAGE.md` - Detailed ArchChar guide
- `docs/ARCHCHAR_INTEGRATION_ANALYSIS.md` - How ArchChar integrates with other agents
- `examples/` - Working examples to try

## 🆘 Getting Help

If a command isn't working:
1. Check that SAAT MCP server is running
2. Verify file paths are correct
3. Look at the command file in `.claude/commands/` to see what it expects
4. Ask Claude: "What do I need to provide for /saat-analyze-characteristics?"

**Report issues**: https://github.com/DavidROliverBA/SAAT/issues

---

**Enjoy effortless architecture analysis with SAAT + Claude Code!** 🚀
