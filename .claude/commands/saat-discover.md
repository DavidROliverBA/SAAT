---
description: Discover architecture from an existing codebase (brownfield)
---

I'll help you discover the architecture from an existing codebase.

**What I'll do:**
1. Analyze the repository structure and files
2. Identify technologies, frameworks, and languages
3. Detect architectural patterns (microservices, monolith, etc.)
4. Find services and entry points
5. Generate a discovery report with confidence scores

**What I need from you:**
- Path to the repository you want to analyze
- (Optional) Maximum directory depth to explore (default: 3)

Please provide the repository path, or if you're already in a repository directory, I'll use the current directory.

Once I have the path, I'll use the `discover_architecture` MCP tool to analyze it and show you:
- Technologies found
- Architectural patterns detected
- Services identified
- Confidence score
- Full discovery report saved to `discovery.json`

**After discovery**, I can help you:
- Generate a C4 model (`/saat-generate`)
- Analyze architecture characteristics (`/saat-analyze-characteristics`)
- Run the full pipeline (`/saat-full-pipeline`)
