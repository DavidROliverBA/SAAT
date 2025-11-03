---
description: Extract requirements from documents for greenfield projects
---

I'll help you extract and structure requirements from your documents for a greenfield project.

**What I'll do:**
1. Parse your requirements documents (markdown, text, Word docs)
2. Extract and structure:
   - **Functional Requirements** (REQ-F-001, REQ-F-002, ...):
     - What the system must do
     - Clear, testable requirements
     - Acceptance criteria
   - **Non-Functional Requirements** (REQ-NF-001, REQ-NF-002, ...):
     - Quality attributes (performance, security, scalability)
     - Measurable criteria
     - Performance targets
   - **User Stories** (US-001, US-002, ...):
     - "As a [role], I want [feature], so that [benefit]"
     - Acceptance criteria
   - **Technical Constraints** (CONST-001, CONST-002, ...):
     - Technology choices
     - Compliance requirements
     - Budget and timeline constraints
   - **Stakeholders**:
     - Names and roles
     - Needs and concerns
3. Generate unique IDs consistently
4. Save structured requirements to `requirements.json`

**What I need from you:**
1. Paths to your requirements documents (can be multiple files)
2. (Optional) Project name

**Supported formats:**
- Markdown (.md)
- Text files (.txt)
- Word documents (.docx) - if accessible
- Any text-based format

**Output includes:**
- Complete `requirements.json` with all structured requirements
- Summary showing counts of each requirement type
- Quality check report

Please provide the paths to your requirements documents.

**After extraction**, I can help you:
- Convert NFRs to architecture characteristics
- Generate a C4 model (`/saat-generate`)
- Create the full architecture (`/saat-full-pipeline`)

**Pro tip**: I can automatically convert your Non-Functional Requirements (REQ-NF-*) into Architecture Characteristics for analysis!
