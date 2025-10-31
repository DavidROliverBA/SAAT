# SAAT ↔ bac4-standalone Integration Guide

This document explains how SAAT (Solution Architecture Agent Toolkit) integrates with the bac4-standalone C4 model editor using the industry-standard Structurizr JSON format.

## Overview

**SAAT** generates C4 architecture models from code (brownfield) or requirements (greenfield).
**bac4-standalone** provides interactive visual editing of C4 diagrams.
**Structurizr JSON** is the common interchange format between them.

```
┌─────────────────┐                    ┌──────────────────┐
│                 │   Structurizr      │                  │
│      SAAT       │  ◄──── JSON ────►  │  bac4-standalone │
│  (Analysis &    │                    │   (Visual        │
│   Generation)   │                    │    Editor)       │
└─────────────────┘                    └──────────────────┘
```

---

## Workflow 1: Brownfield (Existing Code → Visual Editor)

### Step 1: Analyze Existing Codebase with SAAT
```bash
# Analyze your existing repository
cd /path/to/your/project
saat analyze --path . -o architecture.json

# This creates SAAT's internal format with rich metadata:
# - Criticality levels (CS1, CS2, SL1, SL2)
# - Interface specifications (protocols, ports, authentication)
# - Responsibilities
# - Technology stacks
```

### Step 2: Export to Structurizr Format
```bash
# Convert SAAT model to Structurizr JSON
saat export-structurizr -m architecture.json -o structurizr.json

# Output: structurizr.json (Structurizr workspace format)
```

### Step 3: Edit Visually in bac4-standalone
```bash
# Open bac4-standalone editor (web-based)
# Import structurizr.json
# Visually refine the diagram:
#   - Adjust element positions
#   - Add/remove systems or containers
#   - Modify relationships
#   - Enhance descriptions
# Export back to structurizr.json
```

### Step 4: Import Back into SAAT
```bash
# Import the refined model
saat import-structurizr -s structurizr.json -o architecture-refined.json

# Now run SAAT's analysis tools on the refined model:
saat validate-model -m architecture-refined.json -f PCI-DSS
saat security-scan -m architecture-refined.json --threat-model
saat generate-terraform -m architecture-refined.json -p aws
saat generate-docs -m architecture-refined.json -f markdown -f plantuml
```

---

## Workflow 2: Greenfield (Requirements → Visual Editor)

### Step 1: Extract Requirements with SAAT
```bash
# Analyze requirements documents
saat discover-requirements -f docs/requirements.md -n "Payment Platform" -o requirements.json

# Extract:
# - Functional requirements
# - Non-functional requirements
# - User stories
# - Technical constraints
# - Stakeholders
```

### Step 2: Generate Initial Architecture
```bash
# TODO: Implement generate-from-requirements
# saat generate-from-requirements --requirements requirements.json -o architecture.json

# For now, manually create architecture based on requirements
# OR use discovery from similar projects
```

### Step 3: Export → Edit → Import (Same as Brownfield)
```bash
# Export to Structurizr
saat export-structurizr -m architecture.json -o structurizr.json

# Edit in bac4-standalone
# (Visual refinement)

# Import back
saat import-structurizr -s structurizr.json -o architecture-final.json
```

### Step 4: Generate Infrastructure
```bash
# Validate architecture against constraints
saat validate-model -m architecture-final.json -f HIPAA

# Generate production infrastructure
saat generate-terraform -m architecture-final.json -p aws -o infrastructure/

# Generate documentation
saat generate-docs -m architecture-final.json -f markdown -f plantuml -o docs/
```

---

## Workflow 3: Round-Trip Editing

You can iterate between SAAT and bac4-standalone multiple times:

```bash
# 1. Initial analysis
saat analyze --path . -o architecture.json

# 2. Export to Structurizr
saat export-structurizr -m architecture.json -o structurizr.json

# 3. Edit in bac4-standalone → Export → structurizr-v2.json

# 4. Import back
saat import-structurizr -s structurizr-v2.json -o architecture-v2.json

# 5. Run validation
saat validate-model -m architecture-v2.json

# 6. Fix issues in bac4-standalone

# 7. Repeat until architecture is correct
```

---

## Data Mapping: SAAT ↔ Structurizr

### SAAT → Structurizr

| SAAT Concept | Structurizr Equivalent | Notes |
|--------------|------------------------|-------|
| `SystemContext` | `SoftwareSystem` (Internal) | |
| `ExternalSystem` | `SoftwareSystem` (External) | |
| `Container` | `Container` | |
| `Component` | `Component` | |
| `Relationship` | `Relationship` | |
| `criticality` (CS1, CS2, etc.) | `properties.criticality` | Custom property |
| `interfaces` | `properties.interface_*` | Serialized to properties |
| `responsibilities` | `properties.responsibilities` | Semicolon-separated |
| `technology` (list) | `technology` (comma-separated) | |
| `tags` (list) | `tags` (comma-separated) | |

### Structurizr → SAAT

| Structurizr Concept | SAAT Equivalent | Notes |
|---------------------|-----------------|-------|
| `SoftwareSystem` (Internal) | `SystemContext` | |
| `SoftwareSystem` (External) | `ExternalSystem` | |
| `Person` | *Not imported* | SAAT focuses on systems |
| `DeploymentNode` | *Not imported* | Use TerraformAgent instead |
| `properties.*` | Reconstructed to SAAT fields | Custom properties preserved |

---

## Structurizr JSON Schema

SAAT uses the official [Structurizr JSON schema](https://github.com/structurizr/json) for maximum compatibility.

### Key Schema Elements

```json
{
  "name": "My Architecture",
  "description": "System architecture",
  "model": {
    "softwareSystems": [
      {
        "id": "1",
        "name": "Payment System",
        "description": "Handles payments",
        "location": "Internal",
        "containers": [
          {
            "id": "2",
            "name": "API",
            "description": "REST API",
            "technology": "Node.js, Express",
            "components": []
          }
        ]
      }
    ]
  },
  "views": {
    "systemContextViews": [],
    "containerViews": [],
    "componentViews": []
  }
}
```

---

## CLI Commands Reference

### Export to Structurizr
```bash
saat export-structurizr -m architecture.json -o structurizr.json
```

**Options**:
- `-m, --model-file`: SAAT C4 model JSON file (required)
- `-o, --output`: Output Structurizr JSON file (default: structurizr.json)

**Output**: Structurizr workspace JSON file compatible with bac4-standalone, Structurizr Lite, and other tools.

### Import from Structurizr
```bash
saat import-structurizr -s structurizr.json -o architecture.json
```

**Options**:
- `-s, --structurizr-file`: Structurizr JSON file (required)
- `-o, --output`: Output SAAT model JSON file (default: architecture.json)

**Output**: SAAT C4 model JSON with reconstructed SAAT-specific fields from properties.

---

## Preserving SAAT-Specific Data

SAAT has richer metadata than standard Structurizr. This data is preserved during round-trip via the `properties` field:

### Criticality Levels
```json
{
  "id": "1",
  "name": "Payment API",
  "properties": {
    "criticality": "CS1"
  }
}
```

**SAAT Criticality Levels**:
- `CS1`: Mission Critical (99.99% uptime) → Multi-AZ, auto-scaling, 35-day backups
- `CS2`: Business Critical (99.9% uptime) → Multi-AZ, auto-scaling, 7-day backups
- `SL1`/`SL2`: Standard (99.5%/99% uptime) → Single-AZ, basic monitoring
- `STANDARD`: Best effort → Minimal configuration

### Interfaces
```json
{
  "id": "2",
  "name": "REST API",
  "properties": {
    "interface_0_protocol": "HTTPS",
    "interface_0_port": "443",
    "interface_0_auth": "OAuth2",
    "interface_0_encrypted": "True"
  }
}
```

### Responsibilities
```json
{
  "id": "3",
  "name": "Auth Service",
  "properties": {
    "responsibilities": "User authentication; Token generation; Session management"
  }
}
```

---

## Example: Complete Workflow

```bash
# Start with requirements
echo "# Payment Platform Requirements
## Functional Requirements
### REQ-F-001: Process Payments
Support credit card payments with PCI-DSS compliance.
" > requirements.md

# Discover requirements
saat discover-requirements -f requirements.md -n "Payment Platform" -o requirements.json

# Analyze existing code (brownfield)
saat analyze --path /my-payment-app -o architecture.json

# Export for visual editing
saat export-structurizr -m architecture.json -o structurizr.json

# Open bac4-standalone
# → Import structurizr.json
# → Edit visually
# → Export as structurizr-refined.json

# Import refined model
saat import-structurizr -s structurizr-refined.json -o architecture-refined.json

# Validate against PCI-DSS
saat validate-model -m architecture-refined.json -f PCI-DSS -o validation.json

# Security analysis
saat security-scan -m architecture-refined.json --threat-model -o security-report.json

# Generate AWS infrastructure
saat generate-terraform -m architecture-refined.json -p aws -r us-east-1 -o infrastructure/

# Generate documentation
saat generate-docs -m architecture-refined.json -f markdown -f plantuml -o docs/

# Review outputs:
ls -la
# architecture.json              (SAAT internal format)
# structurizr.json               (Exported for editing)
# structurizr-refined.json       (Edited in bac4-standalone)
# architecture-refined.json      (Imported back to SAAT)
# validation.json                (Validation report)
# security-report.json           (Security analysis)
# infrastructure/                (Terraform files)
# docs/                          (Architecture documentation)
```

---

## Troubleshooting

### Issue: Lost criticality levels after import
**Cause**: bac4-standalone may not preserve custom properties.
**Solution**: Check that bac4-standalone preserves the `properties` field in JSON. If not, manually merge properties after export.

### Issue: Relationships missing after round-trip
**Cause**: Structurizr stores relationships within source elements, not at the model level.
**Solution**: The converter extracts relationships from all elements. Verify relationships are nested under elements in the Structurizr JSON.

### Issue: Component nesting incorrect
**Cause**: SAAT uses flat lists with IDs; Structurizr uses nested objects.
**Solution**: The converter uses `system_id` and `container_id` to reconstruct nesting. Ensure IDs are consistent.

---

## Best Practices

1. **Always validate after import**
   ```bash
   saat validate-model -m architecture.json
   ```

2. **Use version control for all JSON files**
   ```bash
   git add architecture.json structurizr.json
   git commit -m "Update architecture model"
   ```

3. **Document changes made in bac4-standalone**
   - Keep a CHANGELOG.md
   - Note why visual changes were made
   - Track which version is source of truth

4. **Automate the workflow**
   ```bash
   # script: sync-architecture.sh
   saat export-structurizr -m architecture.json -o structurizr.json
   # (Manual edit in bac4-standalone)
   saat import-structurizr -s structurizr.json -o architecture.json
   saat validate-model -m architecture.json
   ```

5. **Use SAAT as source of truth for metadata**
   - Criticality levels
   - Interfaces and protocols
   - Technical constraints
   - Use bac4-standalone for layout and visual refinement

---

## Future Enhancements

- [ ] Direct API integration (no file exchange)
- [ ] Real-time sync between SAAT and bac4-standalone
- [ ] Collaborative editing support
- [ ] Diff viewer for model changes
- [ ] Automatic conflict resolution

---

## References

- **SAAT**: https://github.com/DavidROliverBA/SAAT
- **bac4-standalone**: https://github.com/DavidROliverBA/bac4-standalone
- **Structurizr JSON Schema**: https://github.com/structurizr/json
- **C4 Model**: https://c4model.com
- **Structurizr**: https://structurizr.com

---

**Last Updated**: 2025-10-31
**Version**: 1.0.0
