---
description: Validate C4 model against structural standards and best practices
---

I'll help you validate your C4 architecture model for structural correctness and best practices.

**What I'll do:**
1. Check structural integrity:
   - All relationship IDs are valid
   - Containers reference valid systems
   - Components reference valid containers
   - No orphaned elements
2. Validate completeness:
   - All elements have descriptions
   - Critical systems have owners
   - Criticality levels assigned appropriately
   - Interfaces specified for containers
3. Enforce best practices:
   - Clear naming conventions
   - Proper criticality assignment
   - External dependencies documented
   - Relationships have protocols
4. (Optional) Check compliance:
   - PCI-DSS: Encryption, audit logs, access controls
   - HIPAA: PHI protection, encryption, audit trails
   - GDPR: Data privacy, right to deletion, consent
   - SOC2: Security controls, monitoring, access management

**What I need from you:**
1. Path to your C4 model JSON file (e.g., `architecture.json`)
2. (Optional) Compliance framework: PCI-DSS, HIPAA, GDPR, or SOC2

**Output includes:**
- Validation score (0-100)
- Issues by severity:
  - **Error**: Must be fixed (breaks model integrity)
  - **Warning**: Should be fixed (missing best practices)
  - **Info**: Consider fixing (suggestions for improvement)
- Actionable suggestions for each issue
- Report saved to `validation-report.json`

Please provide the path to your C4 model file.

**After validation**, I can help you:
- Fix identified issues
- Analyze architecture characteristics (`/saat-analyze-characteristics`)
- Run security analysis (`/saat-security`)
