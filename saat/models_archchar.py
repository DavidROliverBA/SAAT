"""Data models for Architecture Characteristics Analysis.

Based on ArchCharCapture format and Fundamentals of Software Architecture.
"""

from datetime import datetime
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


# ============================================================================
# Input Models (from ArchCharCapture)
# ============================================================================


class ArchCharacteristic(BaseModel):
    """Single architecture characteristic from ArchCharCapture."""

    id: str = Field(..., description="Unique identifier for the characteristic")
    name: str = Field(..., description="Name of the characteristic")
    description: str = Field(..., description="Brief description")
    selected: bool = Field(
        default=False, description="Whether this characteristic is a candidate"
    )
    isTop: bool = Field(
        default=False, description="Whether this is one of the top 7 driving characteristics"
    )
    rating: Literal["critical", "high", "medium", "low"] = Field(
        default="medium", description="Importance level"
    )
    notes: str = Field(default="", description="Specific requirements or context")
    isCustom: bool = Field(
        default=False, description="Whether this is a custom characteristic"
    )


class ArchCharInput(BaseModel):
    """Input from ArchCharCapture tool.

    This represents the architecture characteristics worksheet filled out
    by architects using Mark Richards' methodology.
    """

    projectName: str = Field(..., description="Project or system name")
    architect: str = Field(..., description="Architect name or team")
    date: str = Field(..., description="Date of analysis (ISO format)")
    notes: str = Field(default="", description="Additional context or notes")
    characteristics: list[ArchCharacteristic] = Field(
        default_factory=list, description="All characteristics (selected and unselected)"
    )
    topCharacteristics: list[ArchCharacteristic] = Field(
        default_factory=list, description="Top 7 driving characteristics (prioritized)"
    )


# ============================================================================
# Analysis Output Models
# ============================================================================


class CharacteristicGap(BaseModel):
    """A specific gap identified in the architecture."""

    area: str = Field(
        ...,
        description="Area where gap exists (e.g., 'Container: Payment Service')",
    )
    issue: str = Field(..., description="Description of the issue")
    severity: Literal["critical", "high", "medium", "low"] = Field(
        ..., description="Severity of the gap"
    )
    impact: str = Field(..., description="Impact if not addressed")
    current_state: Optional[str] = Field(
        None, description="Current state of the architecture"
    )
    desired_state: Optional[str] = Field(
        None, description="Desired state for compliance"
    )


class CharacteristicRecommendation(BaseModel):
    """A specific recommendation to address gaps."""

    title: str = Field(..., description="Short title for the recommendation")
    description: str = Field(..., description="Detailed description")
    pattern: Optional[str] = Field(
        None, description="Architectural pattern to apply"
    )
    technologies: list[str] = Field(
        default_factory=list, description="Suggested technologies"
    )
    implementation_effort: Literal["low", "medium", "high"] = Field(
        ..., description="Estimated effort to implement"
    )
    priority: Literal["critical", "high", "medium", "low"] = Field(
        ..., description="Priority based on characteristic importance"
    )
    rationale: str = Field(
        ..., description="Why this recommendation is important"
    )
    tradeoffs: str = Field(
        ..., description="Trade-offs and considerations"
    )
    implementation_steps: list[str] = Field(
        default_factory=list, description="High-level implementation steps"
    )


class CharacteristicAnalysis(BaseModel):
    """Analysis result for a single architecture characteristic."""

    characteristic_id: str = Field(..., description="ID of the characteristic")
    characteristic_name: str = Field(..., description="Name of the characteristic")
    characteristic_rating: Literal["critical", "high", "medium", "low"] = Field(
        ..., description="Importance rating from input"
    )
    category: Literal["operational", "structural", "cross-cutting"] = Field(
        ..., description="Category of the characteristic"
    )

    # Scoring
    compliance_score: int = Field(
        ..., ge=0, le=100, description="Compliance score (0-100)"
    )
    status: Literal["compliant", "partial", "non-compliant"] = Field(
        ..., description="Overall compliance status"
    )

    # Analysis
    summary: str = Field(..., description="Executive summary of the analysis")
    strengths: list[str] = Field(
        default_factory=list, description="Areas where architecture is strong"
    )
    gaps: list[CharacteristicGap] = Field(
        default_factory=list, description="Identified gaps"
    )
    recommendations: list[CharacteristicRecommendation] = Field(
        default_factory=list, description="Prioritized recommendations"
    )

    # Context
    requirements: Optional[str] = Field(
        None, description="Specific requirements from characteristic notes"
    )


class ArchCharAnalysisResult(BaseModel):
    """Complete analysis result for all characteristics."""

    # Metadata
    project_name: str = Field(..., description="Project name from input")
    architect: str = Field(..., description="Architect/team from input")
    analysis_date: str = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="Date of analysis",
    )
    model_metadata: dict[str, Any] = Field(
        default_factory=dict, description="C4 model metadata"
    )

    # Analysis results
    characteristics_analyzed: int = Field(
        ..., description="Number of characteristics analyzed"
    )
    overall_score: int = Field(
        ..., ge=0, le=100, description="Weighted overall compliance score"
    )
    analyses: list[CharacteristicAnalysis] = Field(
        default_factory=list, description="Analysis per characteristic"
    )

    # Top findings (aggregated across all characteristics)
    critical_gaps: list[CharacteristicGap] = Field(
        default_factory=list, description="All critical gaps across characteristics"
    )
    high_priority_gaps: list[CharacteristicGap] = Field(
        default_factory=list, description="All high priority gaps"
    )
    top_recommendations: list[CharacteristicRecommendation] = Field(
        default_factory=list, description="Top prioritized recommendations"
    )

    # Summary
    executive_summary: str = Field(
        ..., description="High-level summary for stakeholders"
    )
    architecture_patterns_recommended: list[str] = Field(
        default_factory=list, description="List of recommended patterns"
    )
    technologies_recommended: list[str] = Field(
        default_factory=list, description="List of recommended technologies"
    )

    # Scoring breakdown
    score_by_category: dict[str, int] = Field(
        default_factory=dict,
        description="Average score by category (operational, structural, cross-cutting)",
    )
    score_by_rating: dict[str, int] = Field(
        default_factory=dict,
        description="Average score by importance rating (critical, high, medium, low)",
    )


# ============================================================================
# Helper Models
# ============================================================================


class CharacteristicMetadata(BaseModel):
    """Metadata about a standard architecture characteristic."""

    name: str
    category: Literal["operational", "structural", "cross-cutting"]
    description: str
    key_concerns: list[str] = Field(
        default_factory=list, description="Key concerns to evaluate"
    )
    common_patterns: list[str] = Field(
        default_factory=list, description="Common patterns that support this"
    )
    common_technologies: list[str] = Field(
        default_factory=list, description="Common technologies"
    )
    measurement_approach: str = Field(
        default="", description="How to measure this characteristic"
    )


# Standard characteristics metadata for reference
STANDARD_CHARACTERISTICS: dict[str, CharacteristicMetadata] = {
    "Availability": CharacteristicMetadata(
        name="Availability",
        category="operational",
        description="The ability of a system to be accessible and operational when required.",
        key_concerns=[
            "Uptime requirements",
            "Redundancy",
            "Failover mechanisms",
            "Single points of failure",
            "Health monitoring",
        ],
        common_patterns=[
            "Active-Active Clustering",
            "Active-Passive Failover",
            "Load Balancing",
            "Geographic Distribution",
        ],
        common_technologies=[
            "Load Balancers (ALB, NLB, HAProxy, NGINX)",
            "Container Orchestration (Kubernetes, ECS)",
            "Health Check Systems",
            "Multi-AZ Deployment",
        ],
        measurement_approach="Uptime percentage, Mean Time Between Failures (MTBF)",
    ),
    "Scalability": CharacteristicMetadata(
        name="Scalability",
        category="operational",
        description="The ability to handle increased workload by adding resources.",
        key_concerns=[
            "Horizontal vs vertical scaling",
            "Auto-scaling capability",
            "Database scalability",
            "Stateless design",
            "Load distribution",
        ],
        common_patterns=[
            "Microservices",
            "Event-Driven Architecture",
            "CQRS",
            "Database Sharding",
            "Caching",
        ],
        common_technologies=[
            "Auto Scaling Groups",
            "Container Orchestration",
            "Message Queues (SQS, Kafka, RabbitMQ)",
            "Caching (Redis, Memcached)",
            "CDN",
        ],
        measurement_approach="Requests per second capacity, user concurrency, data volume",
    ),
    "Performance": CharacteristicMetadata(
        name="Performance",
        category="operational",
        description="The speed and efficiency of the system in executing tasks.",
        key_concerns=[
            "Response time requirements",
            "Throughput targets",
            "Resource utilization",
            "Database query optimization",
            "Network latency",
        ],
        common_patterns=[
            "Caching Strategy",
            "CDN",
            "Asynchronous Processing",
            "Database Optimization",
            "Connection Pooling",
        ],
        common_technologies=[
            "CDN (CloudFront, Akamai)",
            "Caching (Redis, Memcached, Varnish)",
            "Message Queues",
            "Database Indexes",
            "Load Balancers",
        ],
        measurement_approach="Response time (p50, p95, p99), throughput (TPS, RPS), latency",
    ),
    "Security": CharacteristicMetadata(
        name="Security",
        category="cross-cutting",
        description="The ability to protect data and functionality from unauthorized access.",
        key_concerns=[
            "Authentication mechanisms",
            "Authorization controls",
            "Encryption (at rest and in transit)",
            "Compliance requirements",
            "API security",
        ],
        common_patterns=[
            "Defense in Depth",
            "Least Privilege",
            "Zero Trust Architecture",
            "API Gateway Pattern",
            "OAuth2/OIDC",
        ],
        common_technologies=[
            "WAF (Web Application Firewall)",
            "Identity Providers (Auth0, Cognito, Azure AD)",
            "Secrets Management (Vault, Secrets Manager)",
            "TLS/SSL Certificates",
            "Security Groups/Network Policies",
        ],
        measurement_approach="Vulnerability count, compliance audit results, penetration test findings",
    ),
    "Reliability": CharacteristicMetadata(
        name="Reliability",
        category="operational",
        description="The ability to function correctly and consistently over time.",
        key_concerns=[
            "Error handling",
            "Data consistency",
            "Transaction management",
            "Retry logic",
            "Idempotency",
        ],
        common_patterns=[
            "Circuit Breaker",
            "Retry with Exponential Backoff",
            "Saga Pattern",
            "Event Sourcing",
            "Compensating Transactions",
        ],
        common_technologies=[
            "Service Mesh (Istio, Linkerd)",
            "Message Queues",
            "Distributed Tracing",
            "Chaos Engineering Tools",
        ],
        measurement_approach="Error rate, MTBF, MTTR, data consistency checks",
    ),
    "Maintainability": CharacteristicMetadata(
        name="Maintainability",
        category="structural",
        description="The ease with which a system can be modified, updated, or repaired.",
        key_concerns=[
            "Code quality",
            "Modularity",
            "Documentation",
            "Technical debt",
            "Code coupling",
        ],
        common_patterns=[
            "Clean Architecture",
            "Hexagonal Architecture",
            "Domain-Driven Design",
            "SOLID Principles",
            "Microservices",
        ],
        common_technologies=[
            "Code Quality Tools (SonarQube)",
            "Documentation (Swagger, API docs)",
            "Version Control (Git)",
            "Code Review Tools",
        ],
        measurement_approach="Cyclomatic complexity, code coverage, technical debt ratio",
    ),
    "Testability": CharacteristicMetadata(
        name="Testability",
        category="structural",
        description="The ease with which the system can be tested for defects.",
        key_concerns=[
            "Unit test coverage",
            "Integration testing",
            "Test isolation",
            "Mocking capability",
            "Test automation",
        ],
        common_patterns=[
            "Dependency Injection",
            "Hexagonal Architecture",
            "Test Pyramid",
            "Contract Testing",
            "Mocking/Stubbing",
        ],
        common_technologies=[
            "Test Frameworks (JUnit, pytest, Jest)",
            "Mocking Libraries",
            "Test Containers",
            "CI/CD Pipelines",
            "Contract Testing Tools (Pact)",
        ],
        measurement_approach="Test coverage percentage, test execution time, defect detection rate",
    ),
    "Deployability": CharacteristicMetadata(
        name="Deployability",
        category="structural",
        description="The ease and frequency with which the system can be deployed.",
        key_concerns=[
            "Deployment frequency",
            "Deployment automation",
            "Rollback capability",
            "Zero-downtime deployment",
            "Environment parity",
        ],
        common_patterns=[
            "CI/CD Pipeline",
            "Blue-Green Deployment",
            "Canary Releases",
            "Feature Flags",
            "Infrastructure as Code",
        ],
        common_technologies=[
            "CI/CD (Jenkins, GitHub Actions, GitLab CI)",
            "Container Orchestration (Kubernetes, ECS)",
            "Infrastructure as Code (Terraform, CloudFormation)",
            "Feature Flags (LaunchDarkly, Split)",
        ],
        measurement_approach="Deployment frequency, lead time, deployment failure rate, MTTR",
    ),
    "Fault Tolerance": CharacteristicMetadata(
        name="Fault Tolerance",
        category="operational",
        description="The ability to continue operating despite failures in components.",
        key_concerns=[
            "Graceful degradation",
            "Circuit breakers",
            "Bulkheads",
            "Timeout handling",
            "Failure isolation",
        ],
        common_patterns=[
            "Circuit Breaker",
            "Bulkhead Pattern",
            "Timeout Pattern",
            "Retry Pattern",
            "Graceful Degradation",
        ],
        common_technologies=[
            "Service Mesh (Istio, Linkerd)",
            "Circuit Breaker Libraries (Hystrix, Resilience4j)",
            "Health Checks",
            "Monitoring & Alerting",
        ],
        measurement_approach="Failure detection time, degradation impact, recovery time",
    ),
    "Recoverability": CharacteristicMetadata(
        name="Recoverability",
        category="operational",
        description="The ability to restore functionality after a failure.",
        key_concerns=[
            "Backup strategy",
            "RTO (Recovery Time Objective)",
            "RPO (Recovery Point Objective)",
            "Disaster recovery plan",
            "Data replication",
        ],
        common_patterns=[
            "Backup and Restore",
            "Active-Passive Replication",
            "Point-in-Time Recovery",
            "Disaster Recovery Sites",
        ],
        common_technologies=[
            "Backup Services (AWS Backup, Azure Backup)",
            "Database Replication",
            "Snapshot Mechanisms",
            "Disaster Recovery Tools",
        ],
        measurement_approach="RTO, RPO, backup frequency, restoration time, data loss",
    ),
    "Interoperability": CharacteristicMetadata(
        name="Interoperability",
        category="cross-cutting",
        description="The ability to exchange data and interact with other systems.",
        key_concerns=[
            "API standards",
            "Data format compatibility",
            "Protocol support",
            "Integration patterns",
            "Versioning strategy",
        ],
        common_patterns=[
            "RESTful APIs",
            "GraphQL",
            "Message Queues",
            "Event-Driven Architecture",
            "API Gateway",
        ],
        common_technologies=[
            "API Gateways",
            "Message Brokers (Kafka, RabbitMQ)",
            "API Standards (REST, GraphQL, gRPC)",
            "Data Formats (JSON, XML, Protocol Buffers)",
        ],
        measurement_approach="Integration points, API versioning, data format support",
    ),
    "Configurability": CharacteristicMetadata(
        name="Configurability",
        category="structural",
        description="The ease with which system behavior can be changed through configuration.",
        key_concerns=[
            "Environment-specific configuration",
            "Feature flags",
            "Runtime configuration changes",
            "Configuration management",
            "Secrets management",
        ],
        common_patterns=[
            "Externalized Configuration",
            "Feature Flags",
            "Configuration Server",
            "Environment Variables",
        ],
        common_technologies=[
            "Configuration Management (Spring Cloud Config, Consul)",
            "Feature Flags (LaunchDarkly)",
            "Secrets Management (Vault, AWS Secrets Manager)",
            "Environment Variables",
        ],
        measurement_approach="Configuration change frequency, configuration complexity",
    ),
    "Extensibility": CharacteristicMetadata(
        name="Extensibility",
        category="structural",
        description="The ease with which new functionality can be added.",
        key_concerns=[
            "Plugin architecture",
            "Extension points",
            "API design",
            "Backward compatibility",
            "Modularity",
        ],
        common_patterns=[
            "Plugin Architecture",
            "Strategy Pattern",
            "Decorator Pattern",
            "Dependency Injection",
            "Microservices",
        ],
        common_technologies=[
            "API Frameworks",
            "Plugin Systems",
            "Dependency Injection Containers",
            "Microservices Frameworks",
        ],
        measurement_approach="Extension points available, time to add features, backward compatibility",
    ),
    "Usability": CharacteristicMetadata(
        name="Usability",
        category="cross-cutting",
        description="The ease of use and user experience of the system.",
        key_concerns=[
            "User interface design",
            "Accessibility",
            "User onboarding",
            "Error messaging",
            "Documentation",
        ],
        common_patterns=[
            "User-Centered Design",
            "Progressive Disclosure",
            "Accessibility Standards",
            "Responsive Design",
        ],
        common_technologies=[
            "UI Frameworks",
            "Accessibility Tools (WCAG compliance)",
            "User Analytics",
            "A/B Testing Tools",
        ],
        measurement_approach="User satisfaction scores, task completion time, error rates",
    ),
}
