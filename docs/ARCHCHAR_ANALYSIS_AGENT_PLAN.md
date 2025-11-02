# Architecture Characteristics Analysis Agent - Implementation Plan

**Version**: 1.0
**Date**: 2025-10-31
**Status**: Planning Phase

---

## Executive Summary

This document outlines the implementation plan for an **Architecture Characteristics Analysis Agent** that will analyze C4 architecture models against specified architecture characteristics from ArchCharCapture, provide gap analysis, and generate actionable recommendations.

### Goals

1. **Analyze** C4 models against architecture characteristics
2. **Identify** gaps between current architecture and required characteristics
3. **Recommend** specific architectural changes, patterns, and technologies
4. **Prioritize** recommendations based on characteristic importance
5. **Generate** comprehensive reports with rationale

### Key Features

- Import ArchCharCapture JSON format
- Deep analysis of C4 models (systems, containers, components, relationships)
- Knowledge base from "Fundamentals of Software Architecture"
- Pattern matching and anti-pattern detection
- Actionable, prioritized recommendations
- Compliance scoring per characteristic

---

## Agent Overview

### Name
`ArchCharAnalysisAgent` (or `CharacteristicsAgent`)

### Purpose
Evaluate architecture designs against specified characteristics and provide expert recommendations for compliance.

### Input

1. **Architecture Characteristics** (from ArchCharCapture)
   - JSON format with selected characteristics
   - Top 7 driving characteristics
   - Importance ratings
   - Specific notes and requirements

2. **C4 Architecture Model** (from SAAT)
   - Systems, containers, components
   - Relationships and interfaces
   - Technologies and patterns
   - Criticality levels (CS1, CS2, SL1, SL2, STANDARD)

### Output

1. **Analysis Report**
   - Compliance score per characteristic
   - Overall architecture assessment
   - Gap analysis
   - Pattern recommendations
   - Technology recommendations
   - Specific implementation guidance

2. **Prioritized Recommendations**
   - Ordered by characteristic importance
   - Categorized by impact (high/medium/low)
   - With implementation effort estimates
   - With rationale and trade-offs

---

## Architecture

### Agent Structure

```
ArchCharAnalysisAgent
├── Core Agent (PydanticAI)
│   ├── System Prompt (Architecture expert persona)
│   ├── Result Type (ArchCharAnalysisResult)
│   └── Dependencies (ArchCharDependencies)
├── Tools
│   ├── analyze_availability
│   ├── analyze_scalability
│   ├── analyze_performance
│   ├── analyze_security
│   ├── analyze_reliability
│   ├── analyze_maintainability
│   ├── analyze_testability
│   ├── analyze_deployability
│   ├── analyze_fault_tolerance
│   ├── analyze_recoverability
│   ├── analyze_interoperability
│   ├── analyze_configurability
│   ├── analyze_extensibility
│   └── analyze_usability
├── Knowledge Base
│   └── ARCHITECTURE_CHARACTERISTICS_REFERENCE.md
└── Integration
    ├── ArchCharCapture JSON import
    └── C4 Model analysis
```

### Data Flow

```
1. Load ArchCharCapture JSON
   ↓
2. Load C4 Model JSON
   ↓
3. Create ArchCharDependencies
   ↓
4. Initialize ArchCharAnalysisAgent
   ↓
5. For each selected characteristic:
   → Invoke characteristic-specific tool
   → Analyze C4 model
   → Score compliance (0-100)
   → Identify gaps
   → Generate recommendations
   ↓
6. Aggregate results
   ↓
7. Prioritize by importance rating
   ↓
8. Generate comprehensive report
   ↓
9. Output ArchCharAnalysisResult
```

---

## Data Models

### ArchCharInput (from ArchCharCapture)

```python
class ArchCharacteristic(BaseModel):
    """Single architecture characteristic."""
    id: str
    name: str
    description: str
    selected: bool
    isTop: bool
    rating: Literal["critical", "high", "medium", "low"]
    notes: str
    isCustom: bool

class ArchCharInput(BaseModel):
    """Input from ArchCharCapture tool."""
    projectName: str
    architect: str
    date: str
    notes: str
    characteristics: list[ArchCharacteristic]
    topCharacteristics: list[ArchCharacteristic]
```

### CharacteristicAnalysis (Output per Characteristic)

```python
class CharacteristicGap(BaseModel):
    """A specific gap in the architecture."""
    area: str  # e.g., "Container: Payment Service"
    issue: str  # What's wrong
    severity: Literal["critical", "high", "medium", "low"]
    impact: str  # Impact if not addressed

class CharacteristicRecommendation(BaseModel):
    """A specific recommendation."""
    title: str
    description: str
    pattern: Optional[str] = None  # Architectural pattern
    technologies: list[str] = Field(default_factory=list)
    implementation_effort: Literal["low", "medium", "high"]
    priority: Literal["critical", "high", "medium", "low"]
    rationale: str
    tradeoffs: str

class CharacteristicAnalysis(BaseModel):
    """Analysis result for one characteristic."""
    characteristic_name: str
    characteristic_rating: str
    compliance_score: int = Field(ge=0, le=100)
    status: Literal["compliant", "partial", "non-compliant"]
    summary: str
    gaps: list[CharacteristicGap]
    recommendations: list[CharacteristicRecommendation]
```

### ArchCharAnalysisResult (Final Output)

```python
class ArchCharAnalysisResult(BaseModel):
    """Complete analysis result."""
    project_name: str
    analysis_date: str
    characteristics_analyzed: int
    overall_score: int = Field(ge=0, le=100)

    # Analysis per characteristic
    analyses: list[CharacteristicAnalysis]

    # Top findings
    critical_gaps: list[CharacteristicGap]
    top_recommendations: list[CharacteristicRecommendation]

    # Summary
    executive_summary: str
    architecture_patterns_recommended: list[str]
    technologies_recommended: list[str]
```

### ArchCharDependencies

```python
class ArchCharDependencies:
    """Dependencies for the agent."""
    def __init__(
        self,
        archchar_input: ArchCharInput,
        c4_model: C4Model
    ):
        self.archchar_input = archchar_input
        self.c4_model = c4_model
        self.selected_characteristics = [
            c for c in archchar_input.characteristics if c.selected
        ]
        self.top_characteristics = archchar_input.topCharacteristics
```

---

## Agent Tools

Each architecture characteristic gets a dedicated analysis tool. Here's the pattern:

### Tool Template: analyze_[characteristic]

```python
@agent.tool
async def analyze_availability(
    ctx: RunContext[ArchCharDependencies],
) -> dict[str, Any]:
    """Analyze availability characteristic against C4 model.

    Evaluates:
    - Redundancy patterns
    - Failover mechanisms
    - Multi-AZ/region deployment
    - Load balancing
    - Health checks
    - Circuit breakers

    Args:
        ctx: Agent context with ArchCharCapture input and C4 model

    Returns:
        Dictionary with analysis results including score, gaps, and recommendations
    """
    model = ctx.deps.c4_model
    char = next(c for c in ctx.deps.selected_characteristics if c.name == "Availability")

    analysis = {
        "score": 0,
        "gaps": [],
        "recommendations": []
    }

    # Check for redundancy
    single_instance_containers = [
        c for c in model.containers
        if c.criticality in ["CS1", "CS2"]  # High criticality
        # TODO: Check if only one instance
    ]

    if single_instance_containers:
        analysis["gaps"].append({
            "area": "High-criticality containers without redundancy",
            "issue": f"{len(single_instance_containers)} critical containers may have single points of failure",
            "severity": "critical" if char.rating == "critical" else "high"
        })
        analysis["score"] -= 30

    # Check for load balancing
    # Check for health monitoring
    # Check for geographic distribution (if required)
    # etc.

    # Generate recommendations based on gaps
    if single_instance_containers:
        analysis["recommendations"].append({
            "title": "Implement redundancy for critical containers",
            "pattern": "Active-Active Clustering",
            "technologies": ["Load Balancer", "Auto Scaling Group", "Health Checks"],
            "priority": char.rating,
            # ...
        })

    return analysis
```

### Tool List

Each tool follows the same pattern but with characteristic-specific analysis logic:

1. **analyze_availability** - Redundancy, failover, uptime
2. **analyze_scalability** - Horizontal scaling, elasticity, load handling
3. **analyze_performance** - Response time, throughput, caching
4. **analyze_security** - Authentication, encryption, compliance
5. **analyze_reliability** - Error handling, consistency, MTBF
6. **analyze_maintainability** - Code structure, modularity, documentation
7. **analyze_testability** - Test coverage, isolation, automation
8. **analyze_deployability** - CI/CD, deployment frequency, automation
9. **analyze_fault_tolerance** - Circuit breakers, bulkheads, graceful degradation
10. **analyze_recoverability** - Backups, RTO/RPO, disaster recovery
11. **analyze_interoperability** - APIs, standards, integration patterns
12. **analyze_configurability** - Configuration management, feature flags
13. **analyze_extensibility** - Plugin architecture, extension points
14. **analyze_usability** - UI/UX, accessibility, user experience

---

## System Prompt

```python
SYSTEM_PROMPT = """You are an expert software architect specializing in evaluating
architecture designs against specified architecture characteristics based on the
book "Fundamentals of Software Architecture" by Mark Richards and Neal Ford.

Your role is to:
1. Analyze C4 architecture models against specified architecture characteristics
2. Identify specific gaps and issues in the current architecture
3. Provide concrete, actionable recommendations with patterns and technologies
4. Prioritize recommendations based on characteristic importance
5. Explain trade-offs and rationale for each recommendation

For each characteristic, you will:
- Use the provided analysis tools to evaluate the architecture
- Score compliance from 0-100
- Identify specific gaps with severity levels
- Recommend patterns, technologies, and implementation approaches
- Prioritize by the characteristic's importance rating (critical, high, medium, low)

Focus on:
- **Specificity**: Reference actual containers, components, and relationships
- **Patterns**: Recommend proven architectural patterns from the book
- **Technologies**: Suggest specific technologies that support the characteristic
- **Pragmatism**: Balance ideal solutions with practical constraints
- **Tradeoffs**: Explicitly state what you're trading off

Knowledge base:
- You have access to comprehensive architecture characteristics reference
- You understand operational, structural, and cross-cutting characteristics
- You know which patterns support which characteristics
- You understand trade-offs between competing characteristics

Output format:
- Clear, structured analysis per characteristic
- Concrete recommendations with implementation details
- Prioritized action items
- Executive summary for stakeholders
"""
```

---

## Implementation Phases

### Phase 1: Core Infrastructure (Week 1)

**Tasks**:
1. Create data models (ArchCharInput, CharacteristicAnalysis, ArchCharAnalysisResult)
2. Implement ArchCharCapture JSON import
3. Create ArchCharDependencies class
4. Set up agent skeleton with PydanticAI
5. Implement basic checklist workflow

**Deliverables**:
- `saat/models_archchar.py` - Data models
- `saat/agents/archchar.py` - Agent skeleton
- `saat/converters_archchar.py` - JSON import
- Unit tests

### Phase 2: Analysis Tools (Week 2)

**Tasks**:
1. Implement analyze_availability tool (template)
2. Implement analyze_scalability tool
3. Implement analyze_performance tool
4. Implement analyze_security tool
5. Test and refine tool outputs

**Deliverables**:
- 4 working analysis tools
- Tool testing suite
- Refinement of output format

### Phase 3: Complete Characteristics (Week 3)

**Tasks**:
1. Implement remaining 10 analysis tools
2. Add support for custom characteristics
3. Implement scoring algorithm
4. Create recommendation prioritization logic

**Deliverables**:
- All 14 standard characteristic tools
- Custom characteristic support
- Complete analysis pipeline

### Phase 4: Aggregation & Reporting (Week 4)

**Tasks**:
1. Implement result aggregation
2. Create executive summary generation
3. Implement recommendation prioritization
4. Add markdown report generation
5. Add JSON export

**Deliverables**:
- Complete analysis result generation
- Report generation
- Export functionality

### Phase 5: CLI & Integration (Week 5)

**Tasks**:
1. Add CLI command: `saat analyze-characteristics`
2. Integrate with existing SAAT workflow
3. Add MCP tool for Claude Code
4. Create examples and documentation

**Deliverables**:
- `saat analyze-characteristics -m model.json -a archchar.json`
- MCP tool: `analyze_architecture_characteristics`
- Documentation and examples

### Phase 6: Refinement & Testing (Week 6)

**Tasks**:
1. End-to-end testing with real examples
2. Refinement of recommendations
3. Performance optimization
4. User feedback incorporation

**Deliverables**:
- Production-ready agent
- Comprehensive test suite
- User documentation

---

## CLI Command Design

### Command: analyze-characteristics

```bash
saat analyze-characteristics \
  --model-file architecture.json \
  --archchar-file archchar-capture.json \
  --output archchar-analysis.json \
  --report-format markdown \
  --auto-approve
```

**Options**:
- `--model-file`, `-m`: C4 model JSON file (required)
- `--archchar-file`, `-a`: ArchCharCapture JSON file (required)
- `--output`, `-o`: Output file (default: `archchar-analysis.json`)
- `--report-format`, `-f`: Report format (json, markdown, both) (default: both)
- `--auto-approve`, `-y`: Skip approval prompts
- `--focus`: Analyze only specific characteristics (comma-separated)

**Example**:
```bash
# Full analysis
saat analyze-characteristics -m arch.json -a chars.json

# Focus on top 7 only
saat analyze-characteristics -m arch.json -a chars.json --focus top7

# Auto-approve for CI/CD
saat -y analyze-characteristics -m arch.json -a chars.json
```

---

## MCP Tool Design

### Tool: analyze_architecture_characteristics

```json
{
  "name": "analyze_architecture_characteristics",
  "description": "Analyze C4 architecture model against specified architecture characteristics, identify gaps, and provide recommendations",
  "inputSchema": {
    "type": "object",
    "properties": {
      "model_file": {
        "type": "string",
        "description": "Path to C4 model JSON file"
      },
      "archchar_file": {
        "type": "string",
        "description": "Path to ArchCharCapture JSON file"
      }
    },
    "required": ["model_file", "archchar_file"]
  }
}
```

**Integration**:
```python
@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    if name == "analyze_architecture_characteristics":
        model_file = arguments["model_file"]
        archchar_file = arguments["archchar_file"]

        # Load files
        c4_model = C4Model(**json.loads(Path(model_file).read_text()))
        archchar_input = ArchCharInput(**json.loads(Path(archchar_file).read_text()))

        # Run analysis
        agent = ArchCharAnalysisAgent(DEFAULT_MODEL)
        result = await agent.analyze(c4_model, archchar_input, auto_approve=True)

        # Format output
        return [TextContent(type="text", text=format_analysis_result(result))]
```

---

## Analysis Logic Details

### Scoring Algorithm

Each characteristic gets a score from 0-100:

```python
def calculate_score(gaps: list[CharacteristicGap], rating: str) -> int:
    """Calculate compliance score based on gaps and rating."""
    base_score = 100

    severity_weights = {
        "critical": 30,
        "high": 20,
        "medium": 10,
        "low": 5
    }

    for gap in gaps:
        penalty = severity_weights[gap.severity]
        base_score -= penalty

    # Cap at 0
    score = max(0, base_score)

    # Adjust for characteristic importance
    if rating == "critical" and score < 70:
        # Critical characteristics need higher scores
        return score - 10

    return score
```

### Status Determination

```python
def determine_status(score: int) -> str:
    """Determine compliance status."""
    if score >= 80:
        return "compliant"
    elif score >= 50:
        return "partial"
    else:
        return "non-compliant"
```

### Gap Detection Strategies

For each characteristic, analyze different aspects:

**Availability Example**:
```python
def detect_availability_gaps(model: C4Model, char: ArchCharacteristic) -> list[Gap]:
    gaps = []

    # Check 1: Single points of failure
    critical_containers = [c for c in model.containers if c.criticality in ["CS1", "CS2"]]
    # Analyze if these have redundancy

    # Check 2: Load balancing
    # Check if critical containers have load balancers

    # Check 3: Health checks
    # Verify monitoring is in place

    # Check 4: Geographic distribution
    # For critical systems, check multi-region setup

    # Check 5: Database availability
    # Check for DB replication, failover

    return gaps
```

---

## Recommendation Engine

### Pattern Matching

Map characteristics to architectural patterns:

```python
CHARACTERISTIC_PATTERNS = {
    "Availability": [
        "Active-Active Clustering",
        "Active-Passive Failover",
        "Load Balancing",
        "Geographic Distribution",
        "Health Check Pattern"
    ],
    "Scalability": [
        "Microservices",
        "Event-Driven Architecture",
        "CQRS",
        "Database Sharding",
        "Caching",
        "CDN"
    ],
    "Performance": [
        "Caching Strategy",
        "CDN",
        "Asynchronous Processing",
        "Database Optimization",
        "Connection Pooling"
    ],
    # ... more mappings
}
```

### Technology Recommendations

Map characteristics to technologies:

```python
CHARACTERISTIC_TECHNOLOGIES = {
    "Availability": {
        "load_balancers": ["AWS ALB/NLB", "Azure Load Balancer", "NGINX", "HAProxy"],
        "orchestration": ["Kubernetes", "Docker Swarm", "ECS"],
        "monitoring": ["Prometheus", "Datadog", "CloudWatch"]
    },
    "Scalability": {
        "container_orchestration": ["Kubernetes", "ECS", "AKS"],
        "auto_scaling": ["AWS Auto Scaling", "Azure VMSS", "GCP Autoscaler"],
        "message_queues": ["RabbitMQ", "Kafka", "SQS", "Service Bus"]
    },
    # ... more mappings
}
```

### Prioritization Logic

```python
def prioritize_recommendations(
    recommendations: list[CharacteristicRecommendation],
    characteristic_rating: str
) -> list[CharacteristicRecommendation]:
    """Prioritize recommendations."""

    # Priority order
    priority_order = ["critical", "high", "medium", "low"]

    # Sort by:
    # 1. Characteristic importance rating
    # 2. Recommendation priority
    # 3. Implementation effort (prefer lower effort)

    def sort_key(rec: CharacteristicRecommendation):
        char_priority = priority_order.index(characteristic_rating)
        rec_priority = priority_order.index(rec.priority)
        effort_order = {"low": 0, "medium": 1, "high": 2}
        effort = effort_order[rec.implementation_effort]

        return (char_priority, rec_priority, effort)

    return sorted(recommendations, key=sort_key)
```

---

## Example Usage

### Python API

```python
from saat.agents.archchar import ArchCharAnalysisAgent
from saat.models import C4Model
from saat.models_archchar import ArchCharInput
import json

# Load inputs
c4_model = C4Model(**json.loads(Path("architecture.json").read_text()))
archchar_input = ArchCharInput(**json.loads(Path("archchar-capture.json").read_text()))

# Create and run agent
agent = ArchCharAnalysisAgent(model="anthropic:claude-sonnet-4")
result = await agent.analyze(
    c4_model=c4_model,
    archchar_input=archchar_input,
    auto_approve=False  # Interactive mode
)

# Access results
print(f"Overall Score: {result.overall_score}/100")
print(f"\nTop Recommendations:")
for rec in result.top_recommendations[:5]:
    print(f"  - {rec.title} (Priority: {rec.priority})")

# Save report
Path("archchar-analysis.json").write_text(result.model_dump_json(indent=2))
```

### CLI

```bash
# Basic analysis
saat analyze-characteristics \
  -m examples/ecommerce/architecture.json \
  -a examples/ecommerce/archchar-capture.json \
  -o ecommerce-analysis.json

# Output:
# 🔍 Analyzing architecture characteristics...
#
#    Analyzing Availability (CRITICAL)... ✓ Score: 65/100
#    Analyzing Scalability (CRITICAL)... ✓ Score: 70/100
#    Analyzing Performance (HIGH)... ✓ Score: 80/100
#    Analyzing Security (CRITICAL)... ✓ Score: 55/100
#    Analyzing Testability (HIGH)... ✓ Score: 85/100
#    Analyzing Deployability (HIGH)... ✓ Score: 90/100
#    Analyzing Fault Tolerance (CRITICAL)... ✓ Score: 60/100
#
# ✅ Analysis complete!
#    Overall Score: 72/100
#    Critical Gaps: 8
#    Total Recommendations: 24
#
#    Output: ecommerce-analysis.json
#    Report: ecommerce-analysis.md
```

---

## Testing Strategy

### Unit Tests

```python
def test_availability_analysis():
    """Test availability characteristic analysis."""
    # Create mock C4 model
    model = create_test_model_with_single_instance()

    # Create availability characteristic
    char = ArchCharacteristic(
        id="char_1",
        name="Availability",
        rating="critical",
        selected=True,
        isTop=True,
        # ...
    )

    # Analyze
    result = await analyze_availability(model, char)

    # Assert
    assert result["score"] < 70  # Should detect issues
    assert len(result["gaps"]) > 0
    assert any("single point of failure" in gap["issue"].lower()
               for gap in result["gaps"])
```

### Integration Tests

```python
def test_full_analysis_ecommerce():
    """Test complete analysis of e-commerce system."""
    model = load_ecommerce_model()
    archchar = load_ecommerce_archchar()

    agent = ArchCharAnalysisAgent()
    result = await agent.analyze(model, archchar, auto_approve=True)

    # Verify results
    assert result.overall_score > 0
    assert len(result.analyses) == 7  # Top 7 characteristics
    assert result.critical_gaps is not None
    assert len(result.top_recommendations) > 0
```

### End-to-End Tests

```python
def test_cli_analyze_characteristics():
    """Test CLI command."""
    result = subprocess.run([
        "saat", "analyze-characteristics",
        "-m", "tests/fixtures/model.json",
        "-a", "tests/fixtures/archchar.json",
        "-o", "/tmp/output.json",
        "-y"
    ], capture_output=True)

    assert result.returncode == 0
    assert Path("/tmp/output.json").exists()

    output = json.loads(Path("/tmp/output.json").read_text())
    assert "overall_score" in output
```

---

## Success Metrics

### Functional Metrics

- ✅ Successfully imports ArchCharCapture JSON
- ✅ Analyzes all 14 standard characteristics
- ✅ Supports custom characteristics
- ✅ Generates actionable recommendations
- ✅ Produces compliance scores
- ✅ Respects characteristic priorities

### Quality Metrics

- ✅ Recommendations are specific and actionable
- ✅ Patterns match architecture characteristics
- ✅ Technology suggestions are current and relevant
- ✅ Trade-offs are explicitly stated
- ✅ Rationale is clear and educational

### Performance Metrics

- Analysis completes in < 2 minutes for typical system
- Handles large models (100+ containers)
- Supports all SAAT model sizes

---

## Future Enhancements

### Version 1.1
- Support for architecture fitness functions
- Continuous monitoring integration
- Historical trend analysis
- Before/after comparison

### Version 1.2
- Cost estimation per recommendation
- Implementation roadmap generation
- Risk assessment per gap
- Alternative pattern suggestions

### Version 1.3
- Machine learning for pattern detection
- Custom characteristic templates
- Industry-specific characteristic sets
- Team collaboration features

---

## Conclusion

The Architecture Characteristics Analysis Agent will provide:

1. **Systematic Analysis**: Evaluate architectures against 14+ characteristics
2. **Expert Recommendations**: Pattern and technology suggestions based on the book
3. **Prioritized Action Items**: Focus on what matters most
4. **Educational Value**: Explain rationale and trade-offs
5. **Integration**: Seamless fit with existing SAAT workflow

**Next Steps**:
1. Review and approve this plan
2. Choose implementation approach (see Build Options)
3. Begin Phase 1: Core Infrastructure

---

**Questions for Decision**:

1. **Scope**: Start with top 3-5 characteristics or all 14?
2. **Depth**: How detailed should recommendations be?
3. **Integration**: Priority on CLI, MCP, or Python API?
4. **Timeline**: 6-week phased approach or faster MVP?

---

**Document Version**: 1.0
**Last Updated**: 2025-10-31
**Status**: Ready for Review
