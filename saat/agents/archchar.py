"""Architecture Characteristics Analysis Agent.

Analyzes C4 models against specified architecture characteristics and provides
recommendations based on "Fundamentals of Software Architecture" by Mark Richards and Neal Ford.
"""

import asyncio
from pathlib import Path
from typing import Any, Optional

from pydantic_ai import Agent, RunContext

from saat.agents.base import BaseAgentWithChecklist
from saat.models import C4Model, ChecklistItem, AgentChecklist
from saat.models_archchar import (
    ArchCharInput,
    ArchCharacteristic,
    CharacteristicAnalysis,
    CharacteristicGap,
    CharacteristicRecommendation,
    ArchCharAnalysisResult,
    STANDARD_CHARACTERISTICS,
)


# ============================================================================
# Dependencies
# ============================================================================


class ArchCharDependencies:
    """Dependencies for Architecture Characteristics Analysis Agent."""

    def __init__(self, c4_model: C4Model, archchar_input: ArchCharInput):
        """Initialize dependencies.

        Args:
            c4_model: C4 architecture model to analyze
            archchar_input: Architecture characteristics from ArchCharCapture
        """
        self.c4_model = c4_model
        self.archchar_input = archchar_input
        self.selected_characteristics = [
            c for c in archchar_input.characteristics if c.selected
        ]
        self.top_characteristics = archchar_input.topCharacteristics

        # Create lookup dict for quick access
        self.characteristics_by_name = {
            c.name: c for c in archchar_input.characteristics
        }


# ============================================================================
# System Prompt
# ============================================================================


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
- **Specificity**: Reference actual systems, containers, components, and relationships
- **Patterns**: Recommend proven architectural patterns from the book
- **Technologies**: Suggest specific technologies that support the characteristic
- **Pragmatism**: Balance ideal solutions with practical constraints
- **Trade-offs**: Explicitly state what you're trading off

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


# ============================================================================
# Helper Functions
# ============================================================================


def calculate_score(gaps: list[CharacteristicGap], rating: str) -> int:
    """Calculate compliance score based on gaps and characteristic rating.

    Args:
        gaps: List of identified gaps
        rating: Importance rating of the characteristic

    Returns:
        Score from 0-100
    """
    base_score = 100

    severity_weights = {
        "critical": 30,
        "high": 20,
        "medium": 10,
        "low": 5,
    }

    for gap in gaps:
        penalty = severity_weights.get(gap.severity, 10)
        base_score -= penalty

    # Cap at 0
    score = max(0, base_score)

    # Adjust for characteristic importance
    if rating == "critical" and score < 70:
        # Critical characteristics need higher standards
        score = max(0, score - 10)

    return score


def determine_status(score: int) -> str:
    """Determine compliance status from score.

    Args:
        score: Compliance score (0-100)

    Returns:
        Status: compliant, partial, or non-compliant
    """
    if score >= 80:
        return "compliant"
    elif score >= 50:
        return "partial"
    else:
        return "non-compliant"


# ============================================================================
# Agent Creation
# ============================================================================


def create_archchar_agent(
    model_name: str = "anthropic:claude-sonnet-4",
) -> Agent[ArchCharDependencies, str]:
    """Create Architecture Characteristics Analysis agent.

    Args:
        model_name: Model identifier

    Returns:
        Configured PydanticAI agent
    """
    agent: Agent[ArchCharDependencies, str] = Agent(
        model_name,
        deps_type=ArchCharDependencies,
        result_type=str,
        system_prompt=SYSTEM_PROMPT,
    )

    # ========================================================================
    # Analysis Tools - Operational Characteristics
    # ========================================================================

    @agent.tool
    async def analyze_availability(
        ctx: RunContext[ArchCharDependencies],
    ) -> dict[str, Any]:
        """Analyze Availability characteristic against C4 model.

        Evaluates:
        - Redundancy patterns
        - Failover mechanisms
        - Multi-AZ/region deployment
        - Load balancing
        - Health checks
        - Single points of failure

        Args:
            ctx: Agent context with C4 model and architecture characteristics

        Returns:
            Dictionary with gaps and initial recommendations
        """
        model = ctx.deps.c4_model
        char = ctx.deps.characteristics_by_name.get("Availability")

        if not char:
            return {"gaps": [], "recommendations": []}

        gaps = []
        recommendations = []

        # Check 1: Critical containers without redundancy indicators
        critical_containers = [
            c
            for c in model.containers
            if c.criticality in ["CS1", "CS2"]  # High criticality
        ]

        # Look for single-instance indicators
        single_instance_critical = []
        for container in critical_containers:
            # Check if technology or description indicates single instance
            tech_str = " ".join(container.technology).lower()
            if "single" in tech_str or len(container.technology) == 0:
                single_instance_critical.append(container)

        if single_instance_critical and char.rating in ["critical", "high"]:
            gaps.append({
                "area": "Critical Containers - Redundancy",
                "issue": f"{len(single_instance_critical)} critical containers may lack redundancy: {', '.join(c.name for c in single_instance_critical[:3])}",
                "severity": "critical" if char.rating == "critical" else "high",
                "impact": "Service unavailability if single instance fails. Violates high availability requirements.",
                "current_state": "Critical containers potentially running as single instances",
                "desired_state": "Active-Active or Active-Passive clustering with load balancing"
            })

            recommendations.append({
                "title": "Implement redundancy for critical containers",
                "description": f"Deploy multiple instances of critical containers ({', '.join(c.name for c in single_instance_critical[:3])}) across availability zones with load balancing.",
                "pattern": "Active-Active Clustering",
                "technologies": ["Load Balancer (ALB/NLB)", "Auto Scaling Groups", "Multi-AZ Deployment", "Health Checks"],
                "implementation_effort": "medium",
                "priority": char.rating,
                "rationale": f"Critical containers require redundancy to meet {char.rating.upper()} availability requirements. Single points of failure risk complete service outage.",
                "tradeoffs": "Increased infrastructure cost, added complexity in state management",
                "implementation_steps": [
                    "Configure auto-scaling groups with min 2 instances",
                    "Deploy load balancer with health checks",
                    "Ensure stateless design or implement session replication",
                    "Test failover scenarios"
                ]
            })

        # Check 2: Load balancing
        has_load_balancer = any(
            "load balancer" in " ".join(c.technology).lower() or "lb" in c.name.lower()
            for c in model.containers
        )

        if not has_load_balancer and critical_containers:
            gaps.append({
                "area": "Load Balancing",
                "issue": "No load balancer detected in architecture",
                "severity": "high" if char.rating in ["critical", "high"] else "medium",
                "impact": "Cannot distribute traffic across redundant instances. No automatic failover.",
                "current_state": "Direct connections to containers without load distribution",
                "desired_state": "Load balancer distributing traffic with health checks"
            })

            recommendations.append({
                "title": "Add load balancer for traffic distribution",
                "description": "Implement application load balancer to distribute traffic and provide automatic failover.",
                "pattern": "Load Balancing",
                "technologies": ["AWS ALB/NLB", "Azure Load Balancer", "NGINX", "HAProxy"],
                "implementation_effort": "low",
                "priority": char.rating,
                "rationale": "Load balancers enable high availability by distributing load and detecting failed instances.",
                "tradeoffs": "Additional component to manage, slight latency increase",
                "implementation_steps": [
                    "Deploy load balancer in front of critical services",
                    "Configure health check endpoints",
                    "Set up SSL termination at load balancer",
                    "Configure target groups and routing rules"
                ]
            })

        # Check 3: Database availability
        database_containers = [
            c for c in model.containers
            if any(db in " ".join(c.technology).lower() for db in ["database", "postgres", "mysql", "mongo", "sql"])
        ]

        for db in database_containers:
            if db.criticality in ["CS1", "CS2"]:
                tech_str = " ".join(db.technology).lower()
                if "replica" not in tech_str and "cluster" not in tech_str:
                    gaps.append({
                        "area": f"Database: {db.name}",
                        "issue": "No database replication or clustering detected",
                        "severity": "critical" if char.rating == "critical" else "high",
                        "impact": "Database single point of failure. Data unavailability during outages.",
                        "current_state": "Single database instance",
                        "desired_state": "Multi-AZ database with read replicas or clustering"
                    })

                    recommendations.append({
                        "title": f"Implement database high availability for {db.name}",
                        "description": "Configure database replication or clustering for high availability.",
                        "pattern": "Active-Passive Database Replication",
                        "technologies": ["Multi-AZ RDS", "PostgreSQL Streaming Replication", "MongoDB Replica Sets"],
                        "implementation_effort": "medium",
                        "priority": char.rating,
                        "rationale": "Database is critical component requiring high availability to prevent data access outages.",
                        "tradeoffs": "Increased cost, replication lag considerations, complexity in failover",
                        "implementation_steps": [
                            "Enable Multi-AZ deployment or configure replication",
                            "Set up automated failover",
                            "Configure backup strategy",
                            "Test failover procedures"
                        ]
                    })

        return {"gaps": gaps, "recommendations": recommendations}

    @agent.tool
    async def analyze_scalability(
        ctx: RunContext[ArchCharDependencies],
    ) -> dict[str, Any]:
        """Analyze Scalability characteristic against C4 model.

        Evaluates:
        - Horizontal scaling capability
        - Auto-scaling configuration
        - Stateless design
        - Database scalability
        - Caching strategy
        - Load distribution

        Args:
            ctx: Agent context

        Returns:
            Dictionary with gaps and recommendations
        """
        model = ctx.deps.c4_model
        char = ctx.deps.characteristics_by_name.get("Scalability")

        if not char:
            return {"gaps": [], "recommendations": []}

        gaps = []
        recommendations = []

        # Check 1: Auto-scaling capability
        has_autoscaling = any(
            "auto" in " ".join(c.technology).lower() and "scal" in " ".join(c.technology).lower()
            for c in model.containers
        )

        if not has_autoscaling and char.rating in ["critical", "high"]:
            gaps.append({
                "area": "Auto-Scaling",
                "issue": "No auto-scaling detected in architecture",
                "severity": "high" if char.rating == "critical" else "medium",
                "impact": "Cannot automatically handle traffic spikes. Manual intervention required for scaling.",
                "current_state": "Fixed capacity deployment",
                "desired_state": "Auto-scaling groups that respond to load metrics"
            })

            recommendations.append({
                "title": "Implement auto-scaling for dynamic capacity",
                "description": "Configure auto-scaling groups for all stateless containers to automatically scale based on load.",
                "pattern": "Elasticity Pattern",
                "technologies": ["AWS Auto Scaling", "Kubernetes HPA", "Azure VMSS"],
                "implementation_effort": "medium",
                "priority": char.rating,
                "rationale": "Auto-scaling enables system to handle variable load without over-provisioning resources.",
                "tradeoffs": "Scaling delays (warm-up time), potential cost increases during high load",
                "implementation_steps": [
                    "Configure auto-scaling groups with appropriate metrics (CPU, request count)",
                    "Set scaling policies (target tracking or step scaling)",
                    "Define min/max instance counts based on criticality",
                    "Test scaling behavior under load"
                ]
            })

        # Check 2: Caching layer
        has_cache = any(
            any(cache in tech.lower() for cache in ["redis", "memcached", "cache"])
            for c in model.containers
            for tech in c.technology
        )

        if not has_cache and char.rating in ["critical", "high"]:
            gaps.append({
                "area": "Caching Strategy",
                "issue": "No caching layer detected",
                "severity": "medium",
                "impact": "Higher database load, slower response times, reduced scalability.",
                "current_state": "Direct database queries for all requests",
                "desired_state": "Distributed caching layer reducing database load"
            })

            recommendations.append({
                "title": "Add distributed caching layer",
                "description": "Implement caching for frequently accessed data to reduce database load and improve scalability.",
                "pattern": "Cache-Aside Pattern",
                "technologies": ["Redis", "Memcached", "AWS ElastiCache"],
                "implementation_effort": "medium",
                "priority": char.rating,
                "rationale": "Caching dramatically reduces database load, enabling higher scalability and better performance.",
                "tradeoffs": "Cache invalidation complexity, eventual consistency, additional infrastructure",
                "implementation_steps": [
                    "Identify frequently accessed, rarely changing data",
                    "Deploy distributed cache cluster",
                    "Implement cache-aside or write-through pattern",
                    "Configure TTL and eviction policies",
                    "Monitor cache hit rates"
                ]
            })

        # Check 3: Database scalability
        database_containers = [
            c for c in model.containers
            if any(db in " ".join(c.technology).lower() for db in ["database", "postgres", "mysql", "mongo"])
        ]

        for db in database_containers:
            tech_str = " ".join(db.technology).lower()
            if "read replica" not in tech_str and "shard" not in tech_str and char.rating in ["critical", "high"]:
                gaps.append({
                    "area": f"Database Scalability: {db.name}",
                    "issue": "No database scaling strategy detected (read replicas or sharding)",
                    "severity": "high" if char.rating == "critical" else "medium",
                    "impact": "Database becomes bottleneck under high load. Limited read scalability.",
                    "current_state": "Single database instance handling all read/write operations",
                    "desired_state": "Read replicas for read scaling or sharding for horizontal scaling"
                })

                recommendations.append({
                    "title": f"Implement database scaling for {db.name}",
                    "description": "Add read replicas to scale read operations or implement sharding for horizontal scaling.",
                    "pattern": "Database Replication / Sharding",
                    "technologies": ["RDS Read Replicas", "PostgreSQL Replication", "Database Sharding"],
                    "implementation_effort": "high",
                    "priority": char.rating,
                    "rationale": "Database scalability is critical for overall system scalability. Read replicas provide immediate read scaling.",
                    "tradeoffs": "Replication lag, increased complexity, sharding requires application changes",
                    "implementation_steps": [
                        "Start with read replicas for read-heavy workloads",
                        "Route read queries to replicas",
                        "Monitor replication lag",
                        "Consider sharding if write scaling needed",
                        "Plan sharding key carefully if implementing sharding"
                    ]
                })

        # Check 4: Message queues for async processing
        has_queue = any(
            any(q in tech.lower() for q in ["queue", "kafka", "rabbitmq", "sqs", "servicebus"])
            for c in model.containers
            for tech in c.technology
        )

        if not has_queue and len(model.containers) > 3:
            gaps.append({
                "area": "Asynchronous Processing",
                "issue": "No message queue or async processing detected",
                "severity": "medium",
                "impact": "Synchronous processing limits scalability. Longer response times under load.",
                "current_state": "Synchronous request/response for all operations",
                "desired_state": "Async processing with message queues for non-critical operations"
            })

            recommendations.append({
                "title": "Implement message queue for async processing",
                "description": "Add message queue to decouple services and enable asynchronous processing of non-time-sensitive operations.",
                "pattern": "Event-Driven Architecture",
                "technologies": ["RabbitMQ", "Apache Kafka", "AWS SQS", "Azure Service Bus"],
                "implementation_effort": "medium",
                "priority": char.rating,
                "rationale": "Async processing improves scalability by decoupling services and reducing blocking operations.",
                "tradeoffs": "Increased complexity, eventual consistency, message delivery guarantees to consider",
                "implementation_steps": [
                    "Identify operations that can be processed asynchronously",
                    "Deploy message broker",
                    "Implement producer/consumer patterns",
                    "Handle message failures and retries",
                    "Monitor queue depths"
                ]
            })

        return {"gaps": gaps, "recommendations": recommendations}

    @agent.tool
    async def analyze_performance(
        ctx: RunContext[ArchCharDependencies],
    ) -> dict[str, Any]:
        """Analyze Performance characteristic against C4 model.

        Evaluates:
        - Response time optimization
        - CDN usage
        - Caching strategy
        - Database query optimization
        - Async processing
        - Resource efficiency

        Args:
            ctx: Agent context

        Returns:
            Dictionary with gaps and recommendations
        """
        model = ctx.deps.c4_model
        char = ctx.deps.characteristics_by_name.get("Performance")

        if not char:
            return {"gaps": [], "recommendations": []}

        gaps = []
        recommendations = []

        # Check 1: CDN for static content
        has_cdn = any(
            "cdn" in " ".join(c.technology).lower() or "cloudfront" in " ".join(c.technology).lower()
            for c in model.containers
        )

        # Look for web/frontend containers
        has_frontend = any(
            any(fe in c.name.lower() or fe in " ".join(c.technology).lower() for fe in ["web", "frontend", "ui", "react", "angular", "vue"])
            for c in model.containers
        )

        if not has_cdn and has_frontend and char.rating in ["critical", "high"]:
            gaps.append({
                "area": "Content Delivery",
                "issue": "No CDN detected for static content delivery",
                "severity": "medium",
                "impact": "Slower page load times, higher latency for geographically distant users, increased origin server load.",
                "current_state": "Static content served directly from origin servers",
                "desired_state": "CDN distributing static content globally"
            })

            recommendations.append({
                "title": "Implement CDN for static content",
                "description": "Deploy CDN to cache and serve static assets (images, CSS, JavaScript) from edge locations close to users.",
                "pattern": "CDN Pattern",
                "technologies": ["AWS CloudFront", "Cloudflare", "Azure CDN", "Akamai"],
                "implementation_effort": "low",
                "priority": char.rating,
                "rationale": "CDN significantly reduces latency and improves page load times by serving content from edge locations.",
                "tradeoffs": "Additional cost, cache invalidation complexity, potential stale content",
                "implementation_steps": [
                    "Configure CDN distribution pointing to origin",
                    "Set appropriate cache headers on static assets",
                    "Implement cache invalidation strategy",
                    "Configure SSL/TLS at CDN edge",
                    "Monitor cache hit rates"
                ]
            })

        # Check 2: Caching (critical for performance)
        has_cache = any(
            any(cache in tech.lower() for cache in ["redis", "memcached", "cache"])
            for c in model.containers
            for tech in c.technology
        )

        if not has_cache and char.rating in ["critical", "high"]:
            gaps.append({
                "area": "Application Caching",
                "issue": "No application-level caching detected",
                "severity": "high" if char.rating == "critical" else "medium",
                "impact": "Every request hits database. Slow response times, high database load.",
                "current_state": "No caching layer between application and database",
                "desired_state": "Distributed cache reducing database queries"
            })

            recommendations.append({
                "title": "Add application caching layer",
                "description": "Implement caching for database query results and frequently accessed data.",
                "pattern": "Cache-Aside Pattern",
                "technologies": ["Redis", "Memcached", "AWS ElastiCache"],
                "implementation_effort": "medium",
                "priority": char.rating,
                "rationale": "Caching is one of the most effective performance optimizations, dramatically reducing response times.",
                "tradeoffs": "Cache invalidation complexity, memory cost, eventual consistency",
                "implementation_steps": [
                    "Identify slow queries and frequently accessed data",
                    "Deploy distributed cache",
                    "Implement caching in application code",
                    "Set appropriate TTLs",
                    "Monitor cache hit rates and adjust strategy"
                ]
            })

        # Check 3: Database indexing (inferred)
        database_containers = [
            c for c in model.containers
            if any(db in " ".join(c.technology).lower() for db in ["database", "postgres", "mysql", "mongo"])
        ]

        if database_containers and char.rating in ["critical", "high"]:
            gaps.append({
                "area": "Database Performance",
                "issue": "Database query optimization should be verified",
                "severity": "medium",
                "impact": "Slow queries can degrade overall system performance.",
                "current_state": "Database configuration and indexing strategy unknown",
                "desired_state": "Optimized indexes, query optimization, connection pooling"
            })

            recommendations.append({
                "title": "Optimize database performance",
                "description": "Ensure proper indexing, query optimization, and connection pooling are in place.",
                "pattern": "Database Optimization",
                "technologies": ["Database Indexes", "Connection Pooling", "Query Optimization"],
                "implementation_effort": "medium",
                "priority": char.rating,
                "rationale": "Database is often the performance bottleneck. Proper optimization is essential.",
                "tradeoffs": "Index maintenance overhead, requires ongoing monitoring",
                "implementation_steps": [
                    "Analyze slow query logs",
                    "Create indexes for frequently queried fields",
                    "Implement connection pooling",
                    "Optimize N+1 query problems",
                    "Consider read replicas for read-heavy workloads",
                    "Monitor query performance continuously"
                ]
            })

        # Check 4: Async processing for long-running tasks
        has_queue = any(
            any(q in tech.lower() for q in ["queue", "kafka", "rabbitmq", "sqs"])
            for c in model.containers
            for tech in c.technology
        )

        if not has_queue and len(model.containers) > 3:
            gaps.append({
                "area": "Asynchronous Processing",
                "issue": "No async processing detected for long-running operations",
                "severity": "medium",
                "impact": "Long-running operations block request threads, causing slow response times.",
                "current_state": "Synchronous processing for all operations",
                "desired_state": "Long-running operations processed asynchronously"
            })

            recommendations.append({
                "title": "Implement async processing for long operations",
                "description": "Move long-running operations (reports, emails, batch processing) to async processing.",
                "pattern": "Async Request-Reply",
                "technologies": ["Message Queue", "Background Workers", "AWS Lambda"],
                "implementation_effort": "medium",
                "priority": char.rating,
                "rationale": "Async processing frees up request threads, improving response times for user-facing operations.",
                "tradeoffs": "Increased complexity, eventual consistency, need for status tracking",
                "implementation_steps": [
                    "Identify long-running operations",
                    "Implement message queue",
                    "Create background workers",
                    "Implement status tracking for async jobs",
                    "Handle job failures and retries"
                ]
            })

        return {"gaps": gaps, "recommendations": recommendations}

    @agent.tool
    async def analyze_security(
        ctx: RunContext[ArchCharDependencies],
    ) -> dict[str, Any]:
        """Analyze Security characteristic against C4 model.

        Evaluates:
        - Authentication mechanisms
        - Authorization controls
        - Encryption (at rest and in transit)
        - API security
        - Secrets management
        - Compliance requirements

        Args:
            ctx: Agent context

        Returns:
            Dictionary with gaps and recommendations
        """
        model = ctx.deps.c4_model
        char = ctx.deps.characteristics_by_name.get("Security")

        if not char:
            return {"gaps": [], "recommendations": []}

        gaps = []
        recommendations = []

        # Check 1: HTTPS/TLS encryption
        http_interfaces = []
        for container in model.containers:
            for interface in container.interfaces:
                if interface.protocol and "http" in interface.protocol.lower() and "https" not in interface.protocol.lower():
                    http_interfaces.append((container.name, interface.port))

        if http_interfaces:
            gaps.append({
                "area": "Encryption in Transit",
                "issue": f"Unencrypted HTTP detected on {len(http_interfaces)} interfaces",
                "severity": "critical" if char.rating == "critical" else "high",
                "impact": "Data transmitted in cleartext can be intercepted. Security and compliance risk.",
                "current_state": f"HTTP protocol on ports: {', '.join(str(p) for _, p in http_interfaces[:3])}",
                "desired_state": "HTTPS/TLS for all external communication"
            })

            recommendations.append({
                "title": "Enforce HTTPS/TLS for all communication",
                "description": "Configure TLS/SSL certificates and enforce HTTPS for all external interfaces.",
                "pattern": "TLS Everywhere",
                "technologies": ["TLS/SSL Certificates", "Let's Encrypt", "AWS ACM", "Load Balancer SSL Termination"],
                "implementation_effort": "low",
                "priority": char.rating,
                "rationale": "Encryption in transit is fundamental for security. Required for compliance (PCI-DSS, HIPAA, GDPR).",
                "tradeoffs": "Minimal - slight performance overhead, certificate management",
                "implementation_steps": [
                    "Obtain SSL/TLS certificates",
                    "Configure HTTPS on load balancers/ingress",
                    "Redirect HTTP to HTTPS",
                    "Enforce HTTPS in application",
                    "Set up certificate renewal automation"
                ]
            })

        # Check 2: API Gateway / Authentication layer
        has_api_gateway = any(
            "api gateway" in c.name.lower() or "gateway" in " ".join(c.technology).lower()
            for c in model.containers
        )

        has_auth_service = any(
            any(auth in c.name.lower() or auth in " ".join(c.technology).lower() for auth in ["auth", "identity", "cognito", "oauth"])
            for c in model.containers
        )

        if not has_api_gateway and not has_auth_service and len(model.containers) > 2:
            gaps.append({
                "area": "Authentication & Authorization",
                "issue": "No centralized authentication/API gateway detected",
                "severity": "critical" if char.rating == "critical" else "high",
                "impact": "Each service must implement own authentication. Inconsistent security controls.",
                "current_state": "No centralized auth mechanism visible",
                "desired_state": "API Gateway with centralized authentication"
            })

            recommendations.append({
                "title": "Implement API Gateway with authentication",
                "description": "Deploy API Gateway to centralize authentication, authorization, and API security controls.",
                "pattern": "API Gateway Pattern",
                "technologies": ["AWS API Gateway", "Kong", "Azure API Management", "OAuth2/OIDC"],
                "implementation_effort": "medium",
                "priority": char.rating,
                "rationale": "API Gateway provides single point for security controls, reducing attack surface and ensuring consistency.",
                "tradeoffs": "Additional component, potential single point of failure (mitigate with HA)",
                "implementation_steps": [
                    "Deploy API Gateway in front of services",
                    "Integrate with identity provider (OAuth2/OIDC)",
                    "Configure authentication policies",
                    "Implement rate limiting and throttling",
                    "Set up API keys and access controls",
                    "Configure WAF rules"
                ]
            })

        # Check 3: Secrets management
        has_secrets_mgmt = any(
            any(sm in " ".join(c.technology).lower() for sm in ["vault", "secrets manager", "key vault"])
            for c in model.containers
        )

        if not has_secrets_mgmt and char.rating in ["critical", "high"]:
            gaps.append({
                "area": "Secrets Management",
                "issue": "No secrets management system detected",
                "severity": "high",
                "impact": "Secrets may be stored in code, config files, or environment variables. Security risk.",
                "current_state": "Secrets management approach unclear",
                "desired_state": "Centralized secrets management with encryption and rotation"
            })

            recommendations.append({
                "title": "Implement secrets management system",
                "description": "Deploy secrets management to securely store and rotate credentials, API keys, and certificates.",
                "pattern": "Secrets Management",
                "technologies": ["HashiCorp Vault", "AWS Secrets Manager", "Azure Key Vault", "GCP Secret Manager"],
                "implementation_effort": "medium",
                "priority": char.rating,
                "rationale": "Proper secrets management prevents credential exposure and enables rotation without code changes.",
                "tradeoffs": "Additional infrastructure, application changes needed",
                "implementation_steps": [
                    "Deploy secrets management service",
                    "Migrate secrets from code/config to secrets store",
                    "Integrate applications with secrets API",
                    "Implement secret rotation policies",
                    "Set up audit logging for secret access"
                ]
            })

        # Check 4: Database encryption
        database_containers = [
            c for c in model.containers
            if any(db in " ".join(c.technology).lower() for db in ["database", "postgres", "mysql", "mongo"])
        ]

        for db in database_containers:
            if db.criticality in ["CS1", "CS2"]:
                tech_str = " ".join(db.technology).lower()
                if "encrypt" not in tech_str:
                    gaps.append({
                        "area": f"Database Encryption: {db.name}",
                        "issue": "Database encryption at rest not explicitly configured",
                        "severity": "high" if char.rating == "critical" else "medium",
                        "impact": "Data at rest vulnerable if physical storage compromised. Compliance risk.",
                        "current_state": "Encryption status unknown",
                        "desired_state": "Encryption at rest enabled for all critical databases"
                    })

        if any("encrypt" not in " ".join(db.technology).lower() for db in database_containers if db.criticality in ["CS1", "CS2"]):
            recommendations.append({
                "title": "Enable database encryption at rest",
                "description": "Enable encryption at rest for all critical databases to protect data at storage level.",
                "pattern": "Encryption at Rest",
                "technologies": ["AWS RDS Encryption", "Azure SQL TDE", "MongoDB Encryption"],
                "implementation_effort": "low",
                "priority": char.rating,
                "rationale": "Encryption at rest is compliance requirement (PCI-DSS, HIPAA) and protects against physical theft.",
                "tradeoffs": "Minimal performance impact, slight storage overhead",
                "implementation_steps": [
                    "Enable encryption for new databases",
                    "Plan migration for existing databases",
                    "Manage encryption keys properly",
                    "Document encryption implementation"
                ]
            })

        return {"gaps": gaps, "recommendations": recommendations}

    @agent.tool
    async def analyze_reliability(
        ctx: RunContext[ArchCharDependencies],
    ) -> dict[str, Any]:
        """Analyze Reliability characteristic against C4 model.

        Evaluates:
        - Error handling
        - Retry logic
        - Transaction management
        - Data consistency
        - Monitoring and alerting

        Args:
            ctx: Agent context

        Returns:
            Dictionary with gaps and recommendations
        """
        model = ctx.deps.c4_model
        char = ctx.deps.characteristics_by_name.get("Reliability")

        if not char:
            return {"gaps": [], "recommendations": []}

        gaps = []
        recommendations = []

        # Check 1: Monitoring and observability
        has_monitoring = any(
            any(mon in " ".join(c.technology).lower() for mon in ["monitor", "prometheus", "datadog", "cloudwatch", "grafana"])
            for c in model.containers
        )

        if not has_monitoring:
            gaps.append({
                "area": "Monitoring & Observability",
                "issue": "No monitoring system detected",
                "severity": "high" if char.rating in ["critical", "high"] else "medium",
                "impact": "Cannot detect failures or performance issues. Poor visibility into system health.",
                "current_state": "No centralized monitoring",
                "desired_state": "Comprehensive monitoring with metrics, logs, and traces"
            })

            recommendations.append({
                "title": "Implement comprehensive monitoring",
                "description": "Deploy monitoring solution to track metrics, logs, and traces across all services.",
                "pattern": "Observability Pattern",
                "technologies": ["Prometheus + Grafana", "Datadog", "AWS CloudWatch", "Azure Monitor"],
                "implementation_effort": "medium",
                "priority": char.rating,
                "rationale": "Monitoring is essential for detecting and resolving reliability issues quickly.",
                "tradeoffs": "Additional infrastructure cost, requires instrumentation",
                "implementation_steps": [
                    "Deploy monitoring infrastructure",
                    "Instrument applications with metrics",
                    "Set up log aggregation",
                    "Implement distributed tracing",
                    "Create dashboards for key metrics",
                    "Configure alerts for critical issues"
                ]
            })

        # Check 2: Message queues for reliable async processing
        has_queue = any(
            any(q in " ".join(c.technology).lower() for q in ["queue", "kafka", "rabbitmq", "sqs"])
            for c in model.containers
        )

        if not has_queue and len(model.containers) > 3:
            gaps.append({
                "area": "Reliable Messaging",
                "issue": "No message queue detected for reliable async processing",
                "severity": "medium",
                "impact": "Risk of message loss in async operations. No guaranteed delivery.",
                "current_state": "No reliable messaging infrastructure",
                "desired_state": "Message queue with delivery guarantees and retry logic"
            })

            recommendations.append({
                "title": "Add message queue for reliable async processing",
                "description": "Implement message queue to ensure reliable delivery of async operations.",
                "pattern": "Reliable Messaging",
                "technologies": ["RabbitMQ", "Apache Kafka", "AWS SQS", "Azure Service Bus"],
                "implementation_effort": "medium",
                "priority": char.rating,
                "rationale": "Message queues provide reliable async communication with delivery guarantees and retry capabilities.",
                "tradeoffs": "Additional complexity, requires message handling logic",
                "implementation_steps": [
                    "Deploy message broker with HA configuration",
                    "Implement message producers and consumers",
                    "Configure dead letter queues for failed messages",
                    "Set up retry policies with exponential backoff",
                    "Monitor queue depths and processing rates"
                ]
            })

        # Check 3: Database transactions
        database_containers = [
            c for c in model.containers
            if any(db in " ".join(c.technology).lower() for db in ["database", "postgres", "mysql", "sql"])
        ]

        if database_containers:
            gaps.append({
                "area": "Data Consistency",
                "issue": "Transaction management and data consistency patterns should be verified",
                "severity": "medium",
                "impact": "Risk of data inconsistency in failure scenarios.",
                "current_state": "Transaction handling approach unclear",
                "desired_state": "ACID transactions or compensating transactions for distributed systems"
            })

            recommendations.append({
                "title": "Ensure proper transaction management",
                "description": "Verify ACID transactions for databases and consider Saga pattern for distributed transactions.",
                "pattern": "Transaction Management / Saga Pattern",
                "technologies": ["Database Transactions", "Saga Pattern", "Event Sourcing"],
                "implementation_effort": "medium",
                "priority": char.rating,
                "rationale": "Proper transaction management ensures data consistency and system reliability.",
                "tradeoffs": "Saga pattern adds complexity, eventual consistency considerations",
                "implementation_steps": [
                    "Use database transactions for single-database operations",
                    "Implement Saga pattern for distributed transactions",
                    "Add compensating transactions for rollback",
                    "Ensure idempotency in operations",
                    "Test failure scenarios thoroughly"
                ]
            })

        return {"gaps": gaps, "recommendations": recommendations}

    @agent.tool
    async def analyze_fault_tolerance(
        ctx: RunContext[ArchCharDependencies],
    ) -> dict[str, Any]:
        """Analyze Fault Tolerance characteristic against C4 model.

        Evaluates:
        - Circuit breakers
        - Bulkheads
        - Timeouts
        - Graceful degradation
        - Failure isolation

        Args:
            ctx: Agent context

        Returns:
            Dictionary with gaps and recommendations
        """
        model = ctx.deps.c4_model
        char = ctx.deps.characteristics_by_name.get("Fault Tolerance")

        if not char:
            return {"gaps": [], "recommendations": []}

        gaps = []
        recommendations = []

        # Check 1: Service mesh or resilience library
        has_service_mesh = any(
            any(sm in " ".join(c.technology).lower() for sm in ["istio", "linkerd", "consul", "service mesh"])
            for c in model.containers
        )

        has_resilience_lib = any(
            any(rl in " ".join(c.technology).lower() for rl in ["hystrix", "resilience4j", "polly"])
            for c in model.containers
        )

        if not has_service_mesh and not has_resilience_lib and len(model.containers) > 2:
            gaps.append({
                "area": "Circuit Breakers & Resilience",
                "issue": "No service mesh or resilience library detected",
                "severity": "high" if char.rating in ["critical", "high"] else "medium",
                "impact": "Cascading failures can bring down entire system. No automatic fault isolation.",
                "current_state": "No circuit breaker or resilience patterns visible",
                "desired_state": "Circuit breakers, timeouts, and retry logic for all service-to-service calls"
            })

            recommendations.append({
                "title": "Implement circuit breaker pattern",
                "description": "Add circuit breakers to prevent cascading failures and isolate faults.",
                "pattern": "Circuit Breaker Pattern",
                "technologies": ["Service Mesh (Istio, Linkerd)", "Resilience4j", "Netflix Hystrix", "Polly"],
                "implementation_effort": "medium",
                "priority": char.rating,
                "rationale": "Circuit breakers prevent cascading failures by stopping calls to failing services, allowing them to recover.",
                "tradeoffs": "Requires careful configuration of thresholds and timeouts",
                "implementation_steps": [
                    "Deploy service mesh OR integrate resilience library",
                    "Configure circuit breaker thresholds",
                    "Implement timeout policies for all external calls",
                    "Add retry logic with exponential backoff",
                    "Monitor circuit breaker states",
                    "Test failure scenarios"
                ]
            })

        # Check 2: Bulkhead pattern (resource isolation)
        critical_containers = [c for c in model.containers if c.criticality in ["CS1", "CS2"]]

        if critical_containers and not has_service_mesh:
            gaps.append({
                "area": "Failure Isolation (Bulkheads)",
                "issue": "No bulkhead pattern detected for resource isolation",
                "severity": "medium",
                "impact": "Failure in one service can exhaust shared resources, affecting all services.",
                "current_state": "Shared resources without isolation",
                "desired_state": "Resource pools isolated per service or client"
            })

            recommendations.append({
                "title": "Implement bulkhead pattern for resource isolation",
                "description": "Isolate thread pools, connections, and resources to prevent one failure from affecting others.",
                "pattern": "Bulkhead Pattern",
                "technologies": ["Thread Pool Isolation", "Connection Pool per Service", "Container Resource Limits"],
                "implementation_effort": "medium",
                "priority": char.rating,
                "rationale": "Bulkheads prevent resource exhaustion in one area from affecting the entire system.",
                "tradeoffs": "Resource overhead from multiple isolated pools",
                "implementation_steps": [
                    "Create separate thread pools for different operations",
                    "Isolate connection pools per downstream service",
                    "Set container resource limits (CPU, memory)",
                    "Configure queue depths and timeouts",
                    "Monitor resource utilization per pool"
                ]
            })

        # Check 3: Health checks
        gaps.append({
            "area": "Health Monitoring",
            "issue": "Health check endpoints should be verified",
            "severity": "medium",
            "impact": "Cannot detect service health automatically for traffic routing.",
            "current_state": "Health check implementation unclear",
            "desired_state": "Health check endpoints on all services for automated monitoring"
        })

        recommendations.append({
            "title": "Implement comprehensive health checks",
            "description": "Add health check endpoints to all services for monitoring and load balancer integration.",
            "pattern": "Health Check Pattern",
            "technologies": ["HTTP Health Endpoints", "Kubernetes Liveness/Readiness Probes"],
            "implementation_effort": "low",
            "priority": char.rating,
            "rationale": "Health checks enable automatic detection and routing away from unhealthy instances.",
            "tradeoffs": "Minimal - slight overhead from health check requests",
            "implementation_steps": [
                "Implement /health endpoint on all services",
                "Check critical dependencies (database, cache)",
                "Configure load balancer health checks",
                "Set up Kubernetes probes if applicable",
                "Monitor health check failures"
            ]
        })

        return {"gaps": gaps, "recommendations": recommendations}

    @agent.tool
    async def analyze_recoverability(
        ctx: RunContext[ArchCharDependencies],
    ) -> dict[str, Any]:
        """Analyze Recoverability characteristic against C4 model.

        Evaluates:
        - Backup strategy
        - RTO (Recovery Time Objective)
        - RPO (Recovery Point Objective)
        - Disaster recovery
        - Data replication

        Args:
            ctx: Agent context

        Returns:
            Dictionary with gaps and recommendations
        """
        model = ctx.deps.c4_model
        char = ctx.deps.characteristics_by_name.get("Recoverability")

        if not char:
            return {"gaps": [], "recommendations": []}

        gaps = []
        recommendations = []

        # Check 1: Database backups
        database_containers = [
            c for c in model.containers
            if any(db in " ".join(c.technology).lower() for db in ["database", "postgres", "mysql", "mongo"])
        ]

        critical_databases = [db for db in database_containers if db.criticality in ["CS1", "CS2"]]

        if critical_databases:
            gaps.append({
                "area": "Database Backup Strategy",
                "issue": f"{len(critical_databases)} critical databases - backup strategy should be verified",
                "severity": "high" if char.rating in ["critical", "high"] else "medium",
                "impact": "Risk of data loss if disaster occurs without proper backups.",
                "current_state": "Backup configuration unclear",
                "desired_state": "Automated backups with appropriate retention based on RPO requirements"
            })

            # Parse RTO/RPO from notes if available
            rto_rpo_info = ""
            if char.notes and ("rto" in char.notes.lower() or "rpo" in char.notes.lower()):
                rto_rpo_info = f" Requirements from notes: {char.notes}"

            recommendations.append({
                "title": "Implement automated database backups",
                "description": f"Configure automated backups for all critical databases with appropriate retention.{rto_rpo_info}",
                "pattern": "Backup and Restore",
                "technologies": ["AWS Backup", "RDS Automated Backups", "Point-in-Time Recovery", "Azure Backup"],
                "implementation_effort": "low",
                "priority": char.rating,
                "rationale": "Regular automated backups are essential for data recovery. Retention should match RPO requirements.",
                "tradeoffs": "Storage costs for backups, backup windows may impact performance",
                "implementation_steps": [
                    "Enable automated backups for all databases",
                    "Configure backup retention (CS1: 35d, CS2: 7d per SAAT standards)",
                    "Set up point-in-time recovery if required",
                    "Store backups in separate region/AZ",
                    "Test backup restoration regularly",
                    "Document recovery procedures"
                ]
            })

        # Check 2: Multi-region deployment for DR
        # Infer from technology mentions
        has_multi_region = any(
            any(mr in " ".join(c.technology).lower() for mr in ["multi-region", "cross-region", "global"])
            for c in model.containers
        )

        if not has_multi_region and char.rating == "critical":
            gaps.append({
                "area": "Disaster Recovery",
                "issue": "No multi-region deployment detected for disaster recovery",
                "severity": "high",
                "impact": "Regional failure would cause complete service outage. Extended RTO.",
                "current_state": "Single region deployment",
                "desired_state": "Multi-region deployment with automated failover"
            })

            recommendations.append({
                "title": "Implement multi-region disaster recovery",
                "description": "Deploy critical services across multiple regions for disaster recovery capability.",
                "pattern": "Multi-Region Active-Passive",
                "technologies": ["Multi-Region Deployment", "Route53 Failover", "Database Replication", "Global Load Balancer"],
                "implementation_effort": "high",
                "priority": char.rating,
                "rationale": "Multi-region deployment protects against regional failures, significantly reducing RTO.",
                "tradeoffs": "Significant cost increase, complexity in data replication and consistency",
                "implementation_steps": [
                    "Identify critical services for multi-region deployment",
                    "Deploy secondary region infrastructure",
                    "Configure cross-region database replication",
                    "Set up global load balancer with health checks",
                    "Implement automated failover procedures",
                    "Test DR failover regularly"
                ]
            })

        # Check 3: Backup restoration testing
        gaps.append({
            "area": "Recovery Testing",
            "issue": "Backup restoration testing should be verified",
            "severity": "medium",
            "impact": "Untested backups may fail during actual recovery, extending RTO.",
            "current_state": "Recovery testing procedures unknown",
            "desired_state": "Regular DR drills and backup restoration tests"
        })

        recommendations.append({
            "title": "Establish regular recovery testing",
            "description": "Schedule regular DR drills and backup restoration tests to verify recovery procedures.",
            "pattern": "DR Testing",
            "technologies": ["DR Runbooks", "Automated Testing", "Chaos Engineering"],
            "implementation_effort": "low",
            "priority": char.rating,
            "rationale": "Untested recovery procedures often fail when needed. Regular testing ensures confidence and reduces RTO.",
            "tradeoffs": "Time investment, potential for disruption if not done carefully",
            "implementation_steps": [
                "Create detailed recovery runbooks",
                "Schedule quarterly DR drills",
                "Test backup restoration in non-production",
                "Measure actual RTO/RPO in tests",
                "Update procedures based on learnings",
                "Consider chaos engineering for resilience testing"
            ]
        })

        return {"gaps": gaps, "recommendations": recommendations}

    # More tools will be added below...
    # (Maintainability, Testability, Deployability,
    #  Interoperability, Configurability, Extensibility, Usability)

    return agent


# ============================================================================
# Agent Class
# ============================================================================


class ArchCharAnalysisAgent(BaseAgentWithChecklist):
    """Architecture Characteristics Analysis Agent.

    Analyzes C4 models against architecture characteristics and provides
    gap analysis with recommendations.
    """

    def __init__(self, model: str = "anthropic:claude-sonnet-4"):
        """Initialize Architecture Characteristics Analysis Agent.

        Args:
            model: Model identifier
        """
        super().__init__("ArchCharAnalysisAgent", model)
        self.agent = create_archchar_agent(model)

    async def create_checklist(
        self, task_description: str, context: Optional[dict[str, Any]] = None
    ) -> AgentChecklist:
        """Generate checklist for architecture characteristics analysis.

        Args:
            task_description: Task description
            context: Context with 'characteristics_count'

        Returns:
            AgentChecklist
        """
        char_count = context.get("characteristics_count", 7) if context else 7

        items = [
            ChecklistItem(
                id="1",
                description="Load architecture characteristics from ArchCharCapture JSON",
                estimated_duration="5s",
            ),
            ChecklistItem(
                id="2",
                description="Load C4 architecture model",
                estimated_duration="5s",
            ),
            ChecklistItem(
                id="3",
                description=f"Analyze {char_count} selected characteristics",
                estimated_duration=f"{char_count * 15}s",
                dependencies=["1", "2"],
            ),
            ChecklistItem(
                id="4",
                description="Calculate compliance scores and identify gaps",
                estimated_duration="10s",
                dependencies=["3"],
            ),
            ChecklistItem(
                id="5",
                description="Generate prioritized recommendations",
                estimated_duration="15s",
                dependencies=["4"],
            ),
            ChecklistItem(
                id="6",
                description="Create executive summary and reports",
                estimated_duration="10s",
                dependencies=["5"],
            ),
        ]

        total_time = 50 + (char_count * 15)
        return AgentChecklist(
            agent_name=self.agent_name,
            task_description=task_description,
            items=items,
            estimated_total_duration=f"{total_time}s (~{total_time//60}m)",
            requires_approval=True,
        )

    async def analyze(
        self,
        c4_model: C4Model,
        archchar_input: ArchCharInput,
        auto_approve: bool = False,
    ) -> ArchCharAnalysisResult:
        """Analyze architecture against characteristics.

        Args:
            c4_model: C4 architecture model
            archchar_input: Architecture characteristics from ArchCharCapture
            auto_approve: Skip approval prompts

        Returns:
            ArchCharAnalysisResult with analysis and recommendations
        """
        selected_chars = [c for c in archchar_input.characteristics if c.selected]

        context = {"characteristics_count": len(selected_chars)}

        # Execute with checklist
        result = await self.execute_with_checklist(
            task_description=f"Analyze architecture against {len(selected_chars)} characteristics",
            auto_approve=auto_approve,
            context=context,
        )

        if result["cancelled"]:
            # Return empty result if cancelled
            return ArchCharAnalysisResult(
                project_name=archchar_input.projectName,
                architect=archchar_input.architect,
                characteristics_analyzed=0,
                overall_score=0,
                executive_summary="Analysis was cancelled by user.",
            )

        # Perform actual analysis
        deps = ArchCharDependencies(c4_model, archchar_input)

        # For now, return a basic result (full implementation will analyze each characteristic)
        # This is a skeleton that will be filled in with actual analysis
        analyses = []
        # TODO: Implement actual analysis for each characteristic

        return ArchCharAnalysisResult(
            project_name=archchar_input.projectName,
            architect=archchar_input.architect,
            characteristics_analyzed=len(selected_chars),
            overall_score=75,  # Placeholder
            analyses=analyses,
            critical_gaps=[],
            high_priority_gaps=[],
            top_recommendations=[],
            executive_summary="Analysis in progress...",
            architecture_patterns_recommended=[],
            technologies_recommended=[],
        )


# ============================================================================
# Convenience Functions
# ============================================================================


async def analyze_architecture_characteristics(
    c4_model: C4Model,
    archchar_input: ArchCharInput,
    model_name: str = "anthropic:claude-sonnet-4",
    auto_approve: bool = False,
) -> ArchCharAnalysisResult:
    """Convenience function to analyze architecture characteristics.

    Args:
        c4_model: C4 model
        archchar_input: Architecture characteristics
        model_name: Model to use
        auto_approve: Skip approval prompts

    Returns:
        ArchCharAnalysisResult
    """
    agent = ArchCharAnalysisAgent(model_name)
    return await agent.analyze(c4_model, archchar_input, auto_approve)
