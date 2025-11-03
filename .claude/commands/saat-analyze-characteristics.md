---
description: Analyze architecture quality against specified characteristics
---

I'll help you analyze your architecture against specified characteristics using Mark Richards' methodology.

**What I'll do:**
1. Load your C4 architecture model
2. Load your architecture characteristics (from ArchCharCapture or custom)
3. Analyze against 14 standard characteristics:
   - **Operational**: Availability, Scalability, Performance, Security, Reliability, Fault Tolerance, Recoverability
   - **Structural**: Maintainability, Testability, Deployability, Configurability, Extensibility
   - **Cross-Cutting**: Interoperability, Usability
4. Identify gaps with severity levels (critical, high, medium, low)
5. Provide pattern-based recommendations with implementation steps
6. Generate compliance scores (0-100, weighted by importance)
7. Create detailed reports (Markdown + JSON)

**What I need from you:**
1. Path to your C4 model JSON file (e.g., `architecture.json`)
2. Path to your architecture characteristics JSON file (e.g., `characteristics.json`)

**If you don't have characteristics yet**, I can help you:
- Use the example from `examples/archchar-ecommerce.json`
- Create characteristics from your requirements
- Use the ArchCharCapture web tool: https://github.com/DavidROliverBA/ArchCharCapture

**Output includes:**
- Overall compliance score (weighted)
- Per-characteristic scores and status
- Critical and high-priority gaps requiring attention
- Top 10 recommendations with:
  - Pattern names
  - Technology suggestions
  - Implementation steps (detailed)
  - Trade-offs and rationale
  - Effort estimates
- Architecture patterns recommended
- Complete analysis saved to `archchar-analysis.md` and `archchar-analysis.json`

Please provide the paths to your C4 model and characteristics files, or let me know if you need help creating the characteristics file first.
