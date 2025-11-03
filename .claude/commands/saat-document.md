---
description: Generate comprehensive architecture documentation
---

I'll help you generate comprehensive documentation from your C4 architecture model.

**What I'll do:**
1. Create markdown overview:
   - Project summary
   - System context description
   - Technology stack
   - Key architectural decisions
2. Generate C4 diagrams:
   - System Context diagram (Level 1) - PlantUML/Mermaid
   - Container diagram (Level 2) - PlantUML/Mermaid
   - Component diagrams (Level 3) - PlantUML/Mermaid
   - Deployment diagram
3. Produce Architecture Decision Records (ADRs):
   - For each major architectural decision
   - Context, Decision, Consequences format
   - Numbered sequentially (ADR-001, ADR-002, etc.)
4. Document each component:
   - Purpose and responsibilities
   - Interfaces and APIs
   - Technology choices and rationale
5. Create deployment documentation:
   - Infrastructure requirements
   - Scaling considerations
   - Monitoring and alerting setup

**What I need from you:**
1. Path to your C4 model JSON file (e.g., `architecture.json`)
2. Output directory (default: `docs/`)
3. Formats to generate (default: markdown, plantuml, mermaid, adr):
   - **markdown**: Overview and component docs
   - **plantuml**: C4 diagrams as PlantUML
   - **mermaid**: C4 diagrams as Mermaid
   - **adr**: Architecture Decision Records

**Output includes:**
- `README.md` - Project overview
- `ARCHITECTURE.md` - Detailed architecture documentation
- `diagrams/` - C4 diagrams in selected formats
- `adr/` - Architecture Decision Records (ADR-001, ADR-002, ...)
- `components/` - Per-component documentation
- `deployment/` - Deployment guides

Please provide the path to your C4 model file and preferred output directory.

**Pro tip**: If you've run architecture characteristics analysis (`/saat-analyze-characteristics`), I can include quality scores and recommendations in the documentation!
