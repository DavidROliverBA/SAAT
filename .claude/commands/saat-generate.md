---
description: Generate a C4 architecture model from discovery results or requirements
---

I'll help you generate a C4 architecture model.

**What I'll do:**
1. Load your discovery results (brownfield) or requirements (greenfield)
2. Create a structured C4 model with:
   - Systems (Level 1)
   - Containers (Level 2)
   - Components (Level 3)
   - Relationships between elements
   - Criticality levels (CS1, CS2, SL1, SL2, STANDARD)
3. Save the complete model to `architecture.json`

**What I need from you:**
Choose one:
- **Brownfield**: Path to `discovery.json` file (from `/saat-discover`)
- **Greenfield**: Path to `requirements.json` file (from `/saat-requirements`)

**Criticality Levels** I'll assign:
- **CS1** (Mission Critical): 99.99% uptime - payment, auth, core business
- **CS2** (Business Critical): 99.9% uptime - important services
- **SL1** (Standard): 99.5% uptime - regular services
- **SL2** (Medium): 99% uptime - supporting services
- **STANDARD**: Best effort - non-critical services

Please provide the discovery or requirements file path.

**After generation**, I can help you:
- Analyze architecture characteristics (`/saat-analyze-characteristics`)
- Validate the model (`/saat-validate`)
- Run security analysis (`/saat-security`)
- Generate documentation (`/saat-document`)
- Create Terraform infrastructure (`/saat-terraform`)
