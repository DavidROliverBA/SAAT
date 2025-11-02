# ArchCharCapture JSON Format Specification

**Source**: https://github.com/DavidROliverBA/ArchCharCapture
**Purpose**: Understanding the architecture characteristics data format for SAAT integration

---

## Overview

ArchCharCapture is a web-based tool that captures architecture characteristics using Mark Richards' Architecture Characteristics Worksheet methodology. It stores data in browser localStorage and exports to Markdown/JPEG formats.

**Key Insight**: While the tool doesn't directly expose JSON for programmatic access, it uses a well-structured internal JSON format for localStorage that can be adapted for API consumption.

---

## JSON Data Structure

### Root Object

```json
{
  "projectName": "string",
  "architect": "string",
  "date": "string (ISO date format)",
  "notes": "string",
  "characteristics": [/* Array of Characteristic objects */],
  "topCharacteristics": [/* Array of top 7 selected Characteristic objects */]
}
```

### Characteristic Object

Each characteristic (whether common or custom) has the following structure:

```json
{
  "id": "string (format: 'char_' + random)",
  "name": "string",
  "description": "string",
  "selected": boolean,
  "isTop": boolean,
  "rating": "string (enum: 'critical', 'high', 'medium', 'low')",
  "notes": "string",
  "isCustom": boolean
}
```

---

## Complete Example

```json
{
  "projectName": "E-Commerce Platform",
  "architect": "John Smith / Architecture Team",
  "date": "2025-10-31",
  "notes": "This is a greenfield e-commerce platform with high scalability requirements due to expected traffic spikes during sales events.",
  "characteristics": [
    {
      "id": "char_abc123",
      "name": "Availability",
      "description": "The ability of a system to be accessible and operational when required.",
      "selected": true,
      "isTop": true,
      "rating": "critical",
      "notes": "99.99% uptime required per SLA. Must handle planned maintenance without downtime.",
      "isCustom": false
    },
    {
      "id": "char_def456",
      "name": "Scalability",
      "description": "The ability to handle increased workload by adding resources.",
      "selected": true,
      "isTop": true,
      "rating": "critical",
      "notes": "Must handle 10x traffic during Black Friday. Auto-scaling required.",
      "isCustom": false
    },
    {
      "id": "char_ghi789",
      "name": "Performance",
      "description": "The speed and efficiency of the system in executing tasks.",
      "selected": true,
      "isTop": true,
      "rating": "high",
      "notes": "Page load under 2s, checkout under 3s. P95 response time < 500ms.",
      "isCustom": false
    },
    {
      "id": "char_jkl012",
      "name": "Security",
      "description": "The ability to protect data and functionality from unauthorized access.",
      "selected": true,
      "isTop": true,
      "rating": "critical",
      "notes": "PCI-DSS compliance required for payment processing. GDPR for EU customers.",
      "isCustom": false
    },
    {
      "id": "char_mno345",
      "name": "Maintainability",
      "description": "The ease with which a system can be modified, updated, or repaired.",
      "selected": true,
      "isTop": false,
      "rating": "high",
      "notes": "Need to support rapid feature development. Code quality is priority.",
      "isCustom": false
    },
    {
      "id": "char_pqr678",
      "name": "Testability",
      "description": "The ease with which the system can be tested for defects.",
      "selected": true,
      "isTop": true,
      "rating": "high",
      "notes": "Automated testing required. 80% code coverage target.",
      "isCustom": false
    },
    {
      "id": "char_stu901",
      "name": "Deployability",
      "description": "The ease and frequency with which the system can be deployed.",
      "selected": true,
      "isTop": true,
      "rating": "high",
      "notes": "Multiple deployments per day. CI/CD pipeline essential.",
      "isCustom": false
    },
    {
      "id": "char_vwx234",
      "name": "Fault Tolerance",
      "description": "The ability to continue operating despite failures in components.",
      "selected": true,
      "isTop": true,
      "rating": "critical",
      "notes": "Single component failure should not bring down system. Circuit breakers needed.",
      "isCustom": false
    },
    {
      "id": "char_custom_1",
      "name": "Cost Efficiency",
      "description": "Ability to minimize cloud infrastructure costs while maintaining performance",
      "selected": true,
      "isTop": false,
      "rating": "medium",
      "notes": "Budget constraints. Need to optimize cloud resource usage.",
      "isCustom": true
    }
  ],
  "topCharacteristics": [
    /* References to the 7 characteristics with isTop: true */
    /* In actual data, these would be the full objects, not references */
  ]
}
```

---

## Standard Characteristics

The ArchCharCapture tool provides 14 pre-loaded characteristics:

### 1. Availability
- **Category**: Operational
- **Description**: The ability of a system to be accessible and operational when required.

### 2. Scalability
- **Category**: Operational
- **Description**: The ability to handle increased workload by adding resources.

### 3. Performance
- **Category**: Operational
- **Description**: The speed and efficiency of the system in executing tasks.

### 4. Security
- **Category**: Cross-Cutting
- **Description**: The ability to protect data and functionality from unauthorized access.

### 5. Reliability
- **Category**: Operational
- **Description**: The ability to function correctly and consistently over time.

### 6. Maintainability
- **Category**: Structural
- **Description**: The ease with which a system can be modified, updated, or repaired.

### 7. Testability
- **Category**: Structural
- **Description**: The ease with which the system can be tested for defects.

### 8. Deployability
- **Category**: Structural
- **Description**: The ease and frequency with which the system can be deployed.

### 9. Fault Tolerance
- **Category**: Operational
- **Description**: The ability to continue operating despite failures in components.

### 10. Recoverability
- **Category**: Operational
- **Description**: The ability to restore functionality after a failure.

### 11. Interoperability
- **Category**: Cross-Cutting
- **Description**: The ability to exchange data and interact with other systems.

### 12. Configurability
- **Category**: Structural
- **Description**: The ease with which system behavior can be changed through configuration.

### 13. Extensibility
- **Category**: Structural
- **Description**: The ease with which new functionality can be added.

### 14. Usability
- **Category**: Cross-Cutting
- **Description**: The ease of use and user experience of the system.

---

## Field Definitions

### projectName
- **Type**: String
- **Required**: No (defaults to "Untitled Project")
- **Purpose**: Identifies the system or project being analyzed

### architect
- **Type**: String
- **Required**: No (defaults to "Not specified")
- **Purpose**: Identifies who created the worksheet (individual or team)

### date
- **Type**: String (ISO 8601 date format: YYYY-MM-DD)
- **Required**: No (defaults to current date)
- **Purpose**: Timestamp for when the analysis was created

### notes
- **Type**: String
- **Required**: No (can be empty)
- **Purpose**: Additional context, constraints, or observations about the system

### characteristics
- **Type**: Array of Characteristic objects
- **Required**: Yes
- **Purpose**: Complete list of all characteristics (selected and unselected)
- **Note**: Includes both standard (14) and custom characteristics

### topCharacteristics
- **Type**: Array of Characteristic objects
- **Required**: Yes (can be empty)
- **Purpose**: The prioritized list of top 7 driving characteristics
- **Constraint**: Maximum of 7 items
- **Note**: These are references/copies of characteristics where `isTop: true`

---

## Characteristic Field Definitions

### id
- **Type**: String
- **Format**: `'char_' + random9Characters`
- **Example**: `"char_abc123xyz"`
- **Purpose**: Unique identifier for the characteristic

### name
- **Type**: String
- **Required**: Yes
- **Examples**: `"Availability"`, `"Scalability"`, `"Cost Efficiency"`
- **Purpose**: Display name of the characteristic

### description
- **Type**: String
- **Required**: Yes
- **Purpose**: Brief explanation of what the characteristic means

### selected
- **Type**: Boolean
- **Default**: false
- **Purpose**: Whether this characteristic is a candidate for the system
- **Note**: Only selected characteristics appear in analysis

### isTop
- **Type**: Boolean
- **Default**: false
- **Purpose**: Whether this is one of the top 7 driving characteristics
- **Constraint**: Maximum of 7 characteristics can have `isTop: true`
- **Note**: A characteristic must be `selected: true` to be eligible for `isTop: true`

### rating
- **Type**: String (enum)
- **Values**: `"critical"`, `"high"`, `"medium"`, `"low"`
- **Default**: `"medium"`
- **Purpose**: Importance level of the characteristic to system success

**Rating Definitions**:
- **critical**: Absolutely essential; system fails without it
- **high**: Very important; significant impact on success
- **medium**: Moderately important; should be considered
- **low**: Nice to have; minimal impact on core success

### notes
- **Type**: String
- **Default**: Empty string
- **Purpose**: Specific context, requirements, or constraints for this characteristic
- **Examples**:
  - `"99.99% uptime required per SLA"`
  - `"Must handle 10x traffic during Black Friday"`
  - `"PCI-DSS compliance required"`

### isCustom
- **Type**: Boolean
- **Default**: false
- **Purpose**: Distinguishes custom characteristics from the standard 14
- **Note**: Custom characteristics can be removed; standard ones cannot

---

## Usage Patterns

### Candidate Selection
1. User reviews all characteristics
2. Selects relevant ones as candidates (`selected: true`)
3. Rates each selected characteristic
4. Adds notes with specific requirements

### Top 7 Prioritization
1. From selected candidates, user chooses up to 7 as "driving" characteristics
2. These represent the most critical architecture characteristics
3. Order matters (priority #1 through #7)
4. Following Mark Richards' advice to limit characteristics

### Custom Characteristics
1. User can add domain-specific characteristics not in the standard 14
2. Examples: `"Cost Efficiency"`, `"Compliance"`, `"Data Sovereignty"`
3. Custom characteristics follow the same structure
4. Marked with `isCustom: true`

---

## Data Flow

```
User Input (Web Form)
    ↓
JavaScript State Management
    ↓
localStorage (JSON)
    ↓
Export Options:
  → Markdown File
  → JPEG Image
```

**For SAAT Integration**:

```
ArchCharCapture (localStorage JSON)
    ↓
Extract/Export JSON
    ↓
SAAT Analysis Agent
    ↓
C4 Model Analysis
    ↓
Architecture Recommendations
```

---

## Integration Considerations

### For SAAT Implementation

1. **Import Format**: Accept JSON in the documented format
2. **Validation**: Ensure characteristics match expected schema
3. **Top 7 Logic**: Verify no more than 7 `isTop: true` characteristics
4. **Custom Characteristics**: Support both standard and custom characteristics
5. **Rating Mapping**: Map ratings to priority levels for analysis

### Proposed SAAT Extension

```json
{
  "projectName": "string",
  "architect": "string",
  "date": "string",
  "notes": "string",
  "characteristics": [/* ... */],
  "topCharacteristics": [/* ... */],

  // SAAT-specific additions for analysis
  "analysis": {
    "c4ModelPath": "string",
    "analysisDate": "string",
    "findings": [/* ... */],
    "recommendations": [/* ... */],
    "complianceScore": number
  }
}
```

---

## Example Queries for Analysis

### Get All Critical Characteristics
```javascript
data.characteristics.filter(c => c.selected && c.rating === 'critical')
```

### Get Top 7 Ordered by Priority
```javascript
data.topCharacteristics
// Already ordered by priority (index 0 = highest)
```

### Get Operational Characteristics
```javascript
const operationalNames = ['Availability', 'Scalability', 'Performance',
                          'Reliability', 'Fault Tolerance', 'Recoverability'];
data.characteristics.filter(c =>
  c.selected && operationalNames.includes(c.name)
)
```

### Get Characteristics with Notes
```javascript
data.characteristics.filter(c => c.selected && c.notes.length > 0)
```

---

## Markdown Export Format

The tool exports to Markdown with this structure:

```markdown
# Architecture Characteristics Worksheet

**System/Project:** [projectName]
**Architect/Team:** [architect]
**Date:** [date]

---

## Top 7 Driving Characteristics

### 1. [Characteristic Name]

- **Description:** [description]
- **Importance Level:** [RATING]
- **Notes:** [notes]

[... repeat for all top 7 ...]

## All Candidate Characteristics ([count])

### [Characteristic Name]

- **Description:** [description]
- **Importance Level:** [RATING]
- **Top 7:** [Yes/No]
- **Notes:** [notes]

[... repeat for all selected ...]

## Additional Notes

[general notes]

---

*Generated by Architecture Characteristics Worksheet App*
*Based on the worksheet by Mark Richards - DeveloperToArchitect.com*
```

---

## API Design Proposal

For programmatic access to ArchCharCapture data in SAAT:

### Input Endpoint
```
POST /api/archchar/import
Content-Type: application/json

{
  "projectName": "...",
  "architect": "...",
  // ... full JSON structure
}
```

### Output Endpoint
```
GET /api/archchar/export/{projectId}
Returns: JSON in documented format
```

### Analysis Trigger
```
POST /api/archchar/analyze
{
  "archCharDataPath": "path/to/archchar.json",
  "c4ModelPath": "path/to/c4model.json"
}
```

---

## Summary

**Key Takeaways**:
1. ArchCharCapture uses a well-structured JSON format internally
2. Maximum of 7 "top" driving characteristics (Mark Richards' recommendation)
3. 14 standard characteristics covering operational, structural, and cross-cutting concerns
4. Support for custom characteristics
5. Four importance levels: critical, high, medium, low
6. Notes field allows specific requirements and context

**For SAAT Integration**:
- Use the documented JSON structure as input format
- Map characteristics to C4 model analysis
- Provide recommendations based on characteristic requirements
- Support both standard and custom characteristics
- Respect the "top 7" prioritization

---

**Last Updated**: 2025-10-31
**For**: SAAT (Solution Architecture Agent Toolkit)
**Purpose**: JSON format specification for architecture characteristics analysis
