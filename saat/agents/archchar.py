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

    # ========================================================================
    # STRUCTURAL CHARACTERISTICS ANALYSIS TOOLS
    # ========================================================================

    @agent.tool
    async def analyze_maintainability(ctx: RunContext[ArchCharDependencies]) -> dict[str, Any]:
        """Analyze Maintainability against C4 model.

        Evaluates:
        - Code organization and modularity
        - Documentation and naming conventions
        - Technical debt indicators
        - Coupling and cohesion

        Returns:
            Dict with 'gaps' and 'recommendations'
        """
        model = ctx.deps.c4_model
        char = ctx.deps.characteristics_by_name.get("Maintainability")

        if not char:
            return {"gaps": [], "recommendations": []}

        gaps = []
        recommendations = []

        # Check 1: Documentation containers
        doc_containers = [c for c in model.containers if "doc" in c.name.lower() or "wiki" in c.name.lower()]

        if not doc_containers and char.rating in ["critical", "high"]:
            gaps.append({
                "area": "Documentation Infrastructure",
                "issue": "No documentation infrastructure detected",
                "severity": "medium",
                "impact": "Lack of documentation slows onboarding and increases maintenance time.",
                "current_state": "No dedicated documentation containers found",
                "desired_state": "Documentation system with API docs, architecture diagrams, and runbooks"
            })

            recommendations.append({
                "title": "Implement documentation infrastructure",
                "description": "Set up automated API documentation and architecture documentation system.",
                "pattern": "Documentation as Code",
                "technologies": ["Swagger/OpenAPI", "Docusaurus", "Confluence", "MkDocs"],
                "implementation_effort": "low",
                "priority": "medium",
                "rationale": "Good documentation significantly reduces maintenance time and improves team productivity.",
                "tradeoffs": "Initial time investment, ongoing maintenance effort",
                "implementation_steps": [
                    "Set up API documentation with OpenAPI/Swagger",
                    "Create architecture documentation repository",
                    "Integrate docs generation into CI/CD pipeline",
                    "Document deployment and operational procedures",
                    "Establish documentation standards and templates"
                ]
            })

        # Check 2: Modularity - excessive container dependencies
        high_coupling_containers = []
        for container in model.containers:
            dependency_count = len([rel for rel in model.relationships
                                  if rel.source == container.name])
            if dependency_count > 5:  # Arbitrary threshold for high coupling
                high_coupling_containers.append((container.name, dependency_count))

        if high_coupling_containers and char.rating in ["critical", "high"]:
            container_list = ", ".join([f"{name} ({count} deps)" for name, count in high_coupling_containers[:3]])
            gaps.append({
                "area": "Modularity and Coupling",
                "issue": f"{len(high_coupling_containers)} containers have high coupling",
                "severity": "medium" if char.rating == "high" else "high",
                "impact": "High coupling makes changes risky and time-consuming, reducing maintainability.",
                "current_state": f"Containers with high dependencies: {container_list}",
                "desired_state": "Loosely coupled containers with clear, minimal dependencies"
            })

            recommendations.append({
                "title": "Reduce coupling through interface segregation",
                "description": "Apply Interface Segregation Principle and introduce abstraction layers to reduce coupling.",
                "pattern": "Interface Segregation, Dependency Inversion",
                "technologies": ["API Gateway", "Event Bus", "Service Mesh"],
                "implementation_effort": "high",
                "priority": char.rating,
                "rationale": "Reducing coupling improves maintainability by allowing independent evolution of components.",
                "tradeoffs": "Increased initial complexity, potential performance overhead from indirection",
                "implementation_steps": [
                    "Identify high-coupling containers",
                    "Analyze dependencies and identify core vs peripheral",
                    "Introduce abstraction layers (interfaces, events)",
                    "Refactor direct dependencies to use abstractions",
                    "Monitor coupling metrics over time"
                ]
            })

        # Check 3: Monolithic containers
        large_monolith = [c for c in model.containers
                         if "monolith" in c.name.lower() or "legacy" in c.name.lower()]

        if large_monolith and char.rating in ["critical", "high"]:
            gaps.append({
                "area": "Monolithic Architecture",
                "issue": f"Monolithic containers detected: {', '.join([c.name for c in large_monolith])}",
                "severity": "high" if char.rating == "critical" else "medium",
                "impact": "Monoliths are harder to maintain, test, and evolve compared to modular architectures.",
                "current_state": "Monolithic architecture pattern",
                "desired_state": "Modular architecture with well-defined boundaries"
            })

            recommendations.append({
                "title": "Consider gradual decomposition of monoliths",
                "description": "Apply Strangler Fig pattern to gradually extract functionality from monoliths.",
                "pattern": "Strangler Fig, Domain-Driven Design",
                "technologies": ["API Gateway", "Service Mesh", "Domain Modeling"],
                "implementation_effort": "high",
                "priority": char.rating,
                "rationale": "Modular architectures are easier to maintain, test, and evolve. Gradual approach reduces risk.",
                "tradeoffs": "Long-term effort, temporary increase in complexity, dual maintenance",
                "implementation_steps": [
                    "Identify bounded contexts within monolith",
                    "Select least-coupled context for extraction",
                    "Create new service with well-defined API",
                    "Route traffic through API gateway",
                    "Gradually migrate functionality",
                    "Monitor and iterate"
                ]
            })

        return {"gaps": gaps, "recommendations": recommendations}

    @agent.tool
    async def analyze_testability(ctx: RunContext[ArchCharDependencies]) -> dict[str, Any]:
        """Analyze Testability against C4 model.

        Evaluates:
        - Test infrastructure and automation
        - Component isolation for testing
        - Mock-friendly architecture
        - Test environments

        Returns:
            Dict with 'gaps' and 'recommendations'
        """
        model = ctx.deps.c4_model
        char = ctx.deps.characteristics_by_name.get("Testability")

        if not char:
            return {"gaps": [], "recommendations": []}

        gaps = []
        recommendations = []

        # Check 1: CI/CD and test automation infrastructure
        ci_cd_containers = [c for c in model.containers
                           if any(keyword in c.name.lower()
                                 for keyword in ["jenkins", "gitlab", "github actions", "ci", "cd", "pipeline"])]

        if not ci_cd_containers and char.rating in ["critical", "high"]:
            gaps.append({
                "area": "Test Automation Infrastructure",
                "issue": "No CI/CD or test automation infrastructure detected",
                "severity": "critical" if char.rating == "critical" else "high",
                "impact": "Manual testing is slow, error-prone, and doesn't scale. Automated testing is essential for testability.",
                "current_state": "No visible CI/CD infrastructure",
                "desired_state": "Automated CI/CD pipeline with comprehensive test suites"
            })

            recommendations.append({
                "title": "Implement CI/CD pipeline with automated testing",
                "description": "Set up continuous integration with automated unit, integration, and E2E tests.",
                "pattern": "Continuous Integration/Continuous Deployment",
                "technologies": ["GitHub Actions", "GitLab CI", "Jenkins", "CircleCI"],
                "implementation_effort": "medium",
                "priority": char.rating,
                "rationale": "Automated testing is fundamental to testability. CI/CD ensures tests run consistently.",
                "tradeoffs": "Initial setup time, ongoing maintenance of test suites",
                "implementation_steps": [
                    "Select CI/CD platform",
                    "Create pipeline configuration",
                    "Set up test stages (unit, integration, E2E)",
                    "Configure test reporting and coverage",
                    "Implement quality gates",
                    "Train team on pipeline usage"
                ]
            })

        # Check 2: Database dependencies - tight coupling
        database_containers = [c for c in model.containers
                              if c.technology and "database" in c.technology.lower()]

        tightly_coupled_to_db = []
        for container in model.containers:
            db_dependencies = [rel for rel in model.relationships
                             if rel.source == container.name and
                             any(db.name == rel.target for db in database_containers)]
            if len(db_dependencies) > 0:
                tightly_coupled_to_db.append(container.name)

        if len(tightly_coupled_to_db) > 3 and char.rating in ["critical", "high"]:
            gaps.append({
                "area": "Database Coupling",
                "issue": f"{len(tightly_coupled_to_db)} containers directly coupled to databases",
                "severity": "medium",
                "impact": "Tight database coupling makes testing difficult. Tests require database setup and are slow.",
                "current_state": "Multiple containers with direct database dependencies",
                "desired_state": "Repository pattern with testable interfaces, in-memory test databases"
            })

            recommendations.append({
                "title": "Introduce repository pattern for testability",
                "description": "Abstract database access behind interfaces to enable mocking and in-memory testing.",
                "pattern": "Repository Pattern, Dependency Injection",
                "technologies": ["Testcontainers", "H2 Database", "SQLite", "Mocking Frameworks"],
                "implementation_effort": "medium",
                "priority": char.rating,
                "rationale": "Repository pattern enables fast, isolated unit tests without real database dependencies.",
                "tradeoffs": "Additional abstraction layer, learning curve for team",
                "implementation_steps": [
                    "Define repository interfaces for data access",
                    "Implement production repositories using real databases",
                    "Implement test repositories using in-memory databases",
                    "Use dependency injection to swap implementations",
                    "Write tests using test repositories",
                    "Consider Testcontainers for integration tests"
                ]
            })

        # Check 3: External service dependencies
        external_systems = [c for c in model.containers if c.external]

        if len(external_systems) > 2 and char.rating in ["critical", "high"]:
            gaps.append({
                "area": "External Dependencies",
                "issue": f"{len(external_systems)} external system dependencies may hinder testing",
                "severity": "medium",
                "impact": "External dependencies make tests slow, flaky, and dependent on external availability.",
                "current_state": f"External systems: {', '.join([s.name for s in external_systems[:5]])}",
                "desired_state": "Mocked external dependencies, contract testing, service virtualization"
            })

            recommendations.append({
                "title": "Implement service virtualization and contract testing",
                "description": "Use mocks, stubs, and contract testing to isolate tests from external dependencies.",
                "pattern": "Contract Testing, Service Virtualization",
                "technologies": ["WireMock", "Pact", "Mountebank", "MockServer"],
                "implementation_effort": "medium",
                "priority": char.rating,
                "rationale": "Service virtualization enables fast, reliable testing without external dependencies.",
                "tradeoffs": "Effort to maintain mocks, risk of mock drift from real services",
                "implementation_steps": [
                    "Identify critical external service dependencies",
                    "Set up service virtualization tool (WireMock, Pact)",
                    "Create mock responses for common scenarios",
                    "Implement contract tests to verify mocks",
                    "Use mocks in development and testing environments",
                    "Keep mocks synchronized with real services"
                ]
            })

        return {"gaps": gaps, "recommendations": recommendations}

    @agent.tool
    async def analyze_deployability(ctx: RunContext[ArchCharDependencies]) -> dict[str, Any]:
        """Analyze Deployability against C4 model.

        Evaluates:
        - CI/CD pipeline automation
        - Containerization and orchestration
        - Deployment frequency and risk
        - Rollback capabilities

        Returns:
            Dict with 'gaps' and 'recommendations'
        """
        model = ctx.deps.c4_model
        char = ctx.deps.characteristics_by_name.get("Deployability")

        if not char:
            return {"gaps": [], "recommendations": []}

        gaps = []
        recommendations = []

        # Check 1: CI/CD infrastructure
        ci_cd_containers = [c for c in model.containers
                           if any(keyword in c.name.lower()
                                 for keyword in ["jenkins", "gitlab", "github actions", "ci", "cd", "pipeline", "argocd", "spinnaker"])]

        if not ci_cd_containers and char.rating in ["critical", "high"]:
            gaps.append({
                "area": "CI/CD Automation",
                "issue": "No CI/CD pipeline infrastructure detected",
                "severity": "critical" if char.rating == "critical" else "high",
                "impact": "Manual deployments are slow, error-prone, and limit deployment frequency.",
                "current_state": "No visible deployment automation",
                "desired_state": "Fully automated CI/CD pipeline with quality gates"
            })

            recommendations.append({
                "title": "Implement comprehensive CI/CD pipeline",
                "description": "Build automated deployment pipeline with build, test, and deployment stages.",
                "pattern": "Continuous Deployment, GitOps",
                "technologies": ["GitHub Actions", "ArgoCD", "GitLab CI", "Jenkins", "Spinnaker"],
                "implementation_effort": "medium",
                "priority": char.rating,
                "rationale": "Deployment automation is essential for frequent, reliable deployments.",
                "tradeoffs": "Initial setup effort, learning curve for team",
                "implementation_steps": [
                    "Select CI/CD platform",
                    "Define deployment pipeline stages",
                    "Implement automated builds and tests",
                    "Set up deployment to staging and production",
                    "Configure approval gates for production",
                    "Implement deployment notifications"
                ]
            })

        # Check 2: Containerization and orchestration
        orchestration_containers = [c for c in model.containers
                                   if any(keyword in c.name.lower() or (c.technology and keyword in c.technology.lower())
                                         for keyword in ["kubernetes", "k8s", "docker", "container", "ecs", "fargate"])]

        if not orchestration_containers and char.rating in ["critical", "high"]:
            gaps.append({
                "area": "Containerization and Orchestration",
                "issue": "No container orchestration platform detected",
                "severity": "high",
                "impact": "Without containerization, deployments are harder to automate and less consistent across environments.",
                "current_state": "No visible container orchestration",
                "desired_state": "Containerized applications with orchestration (Kubernetes, ECS)"
            })

            recommendations.append({
                "title": "Containerize applications with orchestration",
                "description": "Package applications as containers and deploy with orchestration platform.",
                "pattern": "Container Orchestration, Infrastructure as Code",
                "technologies": ["Docker", "Kubernetes", "AWS ECS", "Google GKE", "Helm"],
                "implementation_effort": "high",
                "priority": char.rating,
                "rationale": "Containerization enables consistent deployments, easy scaling, and better resource utilization.",
                "tradeoffs": "Complexity increase, learning curve, operational overhead",
                "implementation_steps": [
                    "Create Dockerfiles for all services",
                    "Set up container registry",
                    "Select orchestration platform (K8s, ECS)",
                    "Define deployment manifests/Helm charts",
                    "Implement rolling deployment strategy",
                    "Set up monitoring and logging for containers"
                ]
            })

        # Check 3: Blue-green or canary deployment capability
        # Look for load balancers or API gateways that could support advanced deployment
        load_balancers = [c for c in model.containers
                         if any(keyword in c.name.lower()
                               for keyword in ["load balancer", "alb", "nginx", "traefik", "ingress"])]

        if load_balancers and char.rating == "critical":
            # Recommend advanced deployment strategies for critical deployability
            recommendations.append({
                "title": "Implement blue-green or canary deployments",
                "description": "Use advanced deployment strategies to reduce deployment risk and enable easy rollback.",
                "pattern": "Blue-Green Deployment, Canary Release",
                "technologies": ["Kubernetes", "Istio", "AWS CodeDeploy", "Flagger", "Argo Rollouts"],
                "implementation_effort": "medium",
                "priority": char.rating,
                "rationale": "Advanced deployment strategies minimize downtime and enable fast rollback if issues occur.",
                "tradeoffs": "Increased complexity, requires twice the resources during deployment",
                "implementation_steps": [
                    "Set up multiple deployment slots (blue/green)",
                    "Configure load balancer to route traffic",
                    "Implement health checks and validation",
                    "Automate traffic switching",
                    "Define rollback procedures",
                    "Consider progressive canary deployments"
                ]
            })

        # Check 4: Feature flags for deployment decoupling
        feature_flag_containers = [c for c in model.containers
                                  if any(keyword in c.name.lower()
                                        for keyword in ["feature flag", "launchdarkly", "split", "unleash", "flagsmith"])]

        if not feature_flag_containers and char.rating in ["critical", "high"]:
            recommendations.append({
                "title": "Implement feature flag system",
                "description": "Decouple deployment from release using feature flags to enable safer, more frequent deployments.",
                "pattern": "Feature Toggles, Trunk-Based Development",
                "technologies": ["LaunchDarkly", "Unleash", "Flagsmith", "Split.io"],
                "implementation_effort": "low",
                "priority": "medium",
                "rationale": "Feature flags enable deploying code without activating features, reducing deployment risk.",
                "tradeoffs": "Additional complexity in code, flag management overhead",
                "implementation_steps": [
                    "Select feature flag platform",
                    "Integrate SDK into applications",
                    "Define flag management processes",
                    "Wrap new features in flags",
                    "Implement gradual rollout capabilities",
                    "Establish flag cleanup procedures"
                ]
            })

        return {"gaps": gaps, "recommendations": recommendations}

    @agent.tool
    async def analyze_configurability(ctx: RunContext[ArchCharDependencies]) -> dict[str, Any]:
        """Analyze Configurability against C4 model.

        Evaluates:
        - Configuration management systems
        - Environment-specific configuration
        - Feature flag infrastructure
        - Secrets management

        Returns:
            Dict with 'gaps' and 'recommendations'
        """
        model = ctx.deps.c4_model
        char = ctx.deps.characteristics_by_name.get("Configurability")

        if not char:
            return {"gaps": [], "recommendations": []}

        gaps = []
        recommendations = []

        # Check 1: Configuration management infrastructure
        config_containers = [c for c in model.containers
                           if any(keyword in c.name.lower()
                                 for keyword in ["config", "consul", "etcd", "spring cloud config", "zookeeper"])]

        if not config_containers and char.rating in ["critical", "high"]:
            gaps.append({
                "area": "Configuration Management",
                "issue": "No centralized configuration management system detected",
                "severity": "medium" if char.rating == "high" else "high",
                "impact": "Without centralized config, environment-specific changes require redeployment.",
                "current_state": "No visible configuration management infrastructure",
                "desired_state": "Centralized configuration with environment-specific overrides"
            })

            recommendations.append({
                "title": "Implement centralized configuration management",
                "description": "Set up configuration server to externalize and centralize application configuration.",
                "pattern": "Externalized Configuration, Configuration Server",
                "technologies": ["Spring Cloud Config", "Consul", "etcd", "AWS Parameter Store", "Azure App Configuration"],
                "implementation_effort": "medium",
                "priority": char.rating,
                "rationale": "Centralized configuration enables runtime changes without redeployment and simplifies environment management.",
                "tradeoffs": "Additional infrastructure component, potential single point of failure",
                "implementation_steps": [
                    "Select configuration management solution",
                    "Set up configuration server",
                    "Migrate configuration from code to config server",
                    "Implement environment-specific overrides",
                    "Add configuration refresh capability",
                    "Secure sensitive configuration values"
                ]
            })

        # Check 2: Secrets management
        secrets_containers = [c for c in model.containers
                             if any(keyword in c.name.lower()
                                   for keyword in ["vault", "secrets", "key management", "kms", "secrets manager"])]

        if not secrets_containers and char.rating in ["critical", "high"]:
            gaps.append({
                "area": "Secrets Management",
                "issue": "No dedicated secrets management system detected",
                "severity": "high",
                "impact": "Secrets in configuration files or code pose security risks and limit configurability.",
                "current_state": "No visible secrets management infrastructure",
                "desired_state": "Secure secrets management with rotation capabilities"
            })

            recommendations.append({
                "title": "Implement secrets management system",
                "description": "Use dedicated secrets management to securely store and rotate sensitive configuration.",
                "pattern": "Secrets Management, Vault Pattern",
                "technologies": ["HashiCorp Vault", "AWS Secrets Manager", "Azure Key Vault", "Google Secret Manager"],
                "implementation_effort": "medium",
                "priority": "high",
                "rationale": "Proper secrets management is essential for security and enables configuration without code changes.",
                "tradeoffs": "Additional infrastructure, complexity in secret rotation",
                "implementation_steps": [
                    "Select secrets management solution",
                    "Set up secrets vault",
                    "Migrate secrets from config files to vault",
                    "Integrate applications with vault SDK",
                    "Implement secret rotation policies",
                    "Audit secret access"
                ]
            })

        # Check 3: Feature flag system
        feature_flag_containers = [c for c in model.containers
                                  if any(keyword in c.name.lower()
                                        for keyword in ["feature flag", "launchdarkly", "split", "unleash", "flagsmith"])]

        if not feature_flag_containers and char.rating in ["critical", "high"]:
            gaps.append({
                "area": "Feature Management",
                "issue": "No feature flag system for runtime feature control",
                "severity": "low" if char.rating == "high" else "medium",
                "impact": "Feature changes require redeployment instead of runtime configuration.",
                "current_state": "No feature flag infrastructure",
                "desired_state": "Feature flag system with runtime control and gradual rollout"
            })

            recommendations.append({
                "title": "Add feature flag system for runtime control",
                "description": "Implement feature flags to control feature availability without code deployment.",
                "pattern": "Feature Toggles, Feature Management",
                "technologies": ["LaunchDarkly", "Unleash", "Flagsmith", "Split.io", "ConfigCat"],
                "implementation_effort": "low",
                "priority": "medium",
                "rationale": "Feature flags enable runtime feature control, A/B testing, and gradual rollouts.",
                "tradeoffs": "Code complexity, flag management overhead, technical debt if not cleaned up",
                "implementation_steps": [
                    "Select feature flag platform",
                    "Integrate SDK into applications",
                    "Define flag naming conventions",
                    "Implement flags for key features",
                    "Set up user segmentation for targeting",
                    "Establish flag retirement process"
                ]
            })

        # Check 4: Environment awareness
        # Infer from notes about multiple environments
        if char.notes and ("environment" in char.notes.lower() or "dev" in char.notes.lower() or "staging" in char.notes.lower()):
            recommendations.append({
                "title": "Implement environment-aware configuration",
                "description": "Ensure configuration system supports multiple environments with clear separation.",
                "pattern": "Environment-Specific Configuration",
                "technologies": ["Environment Variables", "Config Profiles", "Helm Values"],
                "implementation_effort": "low",
                "priority": char.rating,
                "rationale": "Environment-specific configuration ensures proper separation and reduces deployment errors.",
                "tradeoffs": "Complexity in managing multiple configurations",
                "implementation_steps": [
                    "Define environment naming conventions (dev, staging, prod)",
                    "Create environment-specific configuration files",
                    "Use environment variables for environment selection",
                    "Validate configurations per environment",
                    "Document configuration differences"
                ]
            })

        return {"gaps": gaps, "recommendations": recommendations}

    @agent.tool
    async def analyze_extensibility(ctx: RunContext[ArchCharDependencies]) -> dict[str, Any]:
        """Analyze Extensibility against C4 model.

        Evaluates:
        - Plugin architecture support
        - API extensibility points
        - Loose coupling for extensions
        - Open/Closed principle adherence

        Returns:
            Dict with 'gaps' and 'recommendations'
        """
        model = ctx.deps.c4_model
        char = ctx.deps.characteristics_by_name.get("Extensibility")

        if not char:
            return {"gaps": [], "recommendations": []}

        gaps = []
        recommendations = []

        # Check 1: API Gateway for extensibility
        api_gateways = [c for c in model.containers
                       if any(keyword in c.name.lower()
                             for keyword in ["api gateway", "gateway", "kong", "apigee", "ambassador"])]

        if not api_gateways and char.rating in ["critical", "high"]:
            gaps.append({
                "area": "API Extensibility",
                "issue": "No API Gateway for managing extensibility points",
                "severity": "medium",
                "impact": "Without API Gateway, extending functionality and adding plugins is harder.",
                "current_state": "No visible API Gateway infrastructure",
                "desired_state": "API Gateway with plugin support and extension points"
            })

            recommendations.append({
                "title": "Implement API Gateway with plugin support",
                "description": "Use API Gateway to provide extensibility through plugins and custom filters.",
                "pattern": "API Gateway, Plugin Architecture",
                "technologies": ["Kong", "AWS API Gateway", "Apigee", "Tyk", "Ambassador"],
                "implementation_effort": "medium",
                "priority": char.rating,
                "rationale": "API Gateway provides central extensibility point for authentication, routing, and custom logic.",
                "tradeoffs": "Additional infrastructure component, potential bottleneck",
                "implementation_steps": [
                    "Select API Gateway solution",
                    "Deploy and configure gateway",
                    "Define plugin architecture",
                    "Migrate API routing to gateway",
                    "Implement custom plugins as needed",
                    "Document extension points for developers"
                ]
            })

        # Check 2: Event-driven architecture for extensibility
        message_brokers = [c for c in model.containers
                          if any(keyword in c.name.lower() or (c.technology and keyword in c.technology.lower())
                                for keyword in ["kafka", "rabbitmq", "event", "message", "pubsub", "sns", "sqs", "eventbridge"])]

        if not message_brokers and char.rating in ["critical", "high"]:
            gaps.append({
                "area": "Event-Driven Extensibility",
                "issue": "No event-driven infrastructure for loose coupling and extension",
                "severity": "medium" if char.rating == "high" else "high",
                "impact": "Tight coupling limits ability to add new functionality without modifying existing code.",
                "current_state": "No event bus or message broker detected",
                "desired_state": "Event-driven architecture with publish/subscribe for extensibility"
            })

            recommendations.append({
                "title": "Introduce event-driven architecture for extensibility",
                "description": "Use event bus to enable loose coupling and allow new functionality via event subscribers.",
                "pattern": "Event-Driven Architecture, Publish-Subscribe",
                "technologies": ["Apache Kafka", "RabbitMQ", "AWS SNS/SQS", "Google Pub/Sub", "Azure Event Grid"],
                "implementation_effort": "high",
                "priority": char.rating,
                "rationale": "Event-driven architecture enables adding new functionality without modifying existing services.",
                "tradeoffs": "Increased complexity, eventual consistency, debugging challenges",
                "implementation_steps": [
                    "Select message broker/event bus",
                    "Design event schema and versioning strategy",
                    "Identify events to publish from existing services",
                    "Implement event publishers",
                    "Create extension services as event subscribers",
                    "Implement dead letter queues and error handling"
                ]
            })

        # Check 3: Microservices for modularity
        service_count = len([c for c in model.containers if not c.external])

        if service_count < 3 and char.rating in ["critical", "high"]:
            gaps.append({
                "area": "Modular Architecture",
                "issue": "Limited modularity may hinder extensibility",
                "severity": "medium",
                "impact": "Monolithic architecture makes it harder to add functionality independently.",
                "current_state": f"Only {service_count} internal containers/services",
                "desired_state": "Modular architecture with clear service boundaries"
            })

            recommendations.append({
                "title": "Consider modular architecture for extensibility",
                "description": "Break down monolith into services with clear boundaries to enable independent extensions.",
                "pattern": "Microservices, Domain-Driven Design",
                "technologies": ["Service Mesh", "API Gateway", "Domain Modeling"],
                "implementation_effort": "high",
                "priority": char.rating,
                "rationale": "Modular architecture allows adding new services/features without modifying existing code.",
                "tradeoffs": "Increased operational complexity, distributed system challenges",
                "implementation_steps": [
                    "Identify bounded contexts using DDD",
                    "Define service boundaries and APIs",
                    "Extract services gradually (Strangler Fig)",
                    "Ensure loose coupling between services",
                    "Document extension patterns for new services"
                ]
            })

        # Check 4: Webhook or callback support
        if char.notes and ("webhook" in char.notes.lower() or "plugin" in char.notes.lower() or "integration" in char.notes.lower()):
            recommendations.append({
                "title": "Implement webhook system for extensibility",
                "description": "Provide webhook endpoints to allow external systems to extend functionality.",
                "pattern": "Webhook Pattern, Observer Pattern",
                "technologies": ["Webhook Management", "API Callbacks", "Event Notifications"],
                "implementation_effort": "medium",
                "priority": char.rating,
                "rationale": "Webhooks enable external systems and users to extend functionality without modifying core system.",
                "tradeoffs": "Security considerations, retry logic complexity, monitoring overhead",
                "implementation_steps": [
                    "Design webhook event types",
                    "Implement webhook registration API",
                    "Build webhook delivery system with retries",
                    "Add webhook authentication (signatures)",
                    "Provide webhook testing tools",
                    "Document webhook API and events"
                ]
            })

        return {"gaps": gaps, "recommendations": recommendations}

    # ========================================================================
    # CROSS-CUTTING CHARACTERISTICS ANALYSIS TOOLS
    # (Security already implemented above with operational characteristics)
    # ========================================================================

    @agent.tool
    async def analyze_interoperability(ctx: RunContext[ArchCharDependencies]) -> dict[str, Any]:
        """Analyze Interoperability against C4 model.

        Evaluates:
        - External system integrations
        - API standards and protocols
        - Data format compatibility
        - Message brokers for integration

        Returns:
            Dict with 'gaps' and 'recommendations'
        """
        model = ctx.deps.c4_model
        char = ctx.deps.characteristics_by_name.get("Interoperability")

        if not char:
            return {"gaps": [], "recommendations": []}

        gaps = []
        recommendations = []

        # Check 1: External system integrations
        external_systems = [c for c in model.containers if c.external]

        if len(external_systems) > 0:
            # Good - system has integrations, check for API Gateway
            api_gateways = [c for c in model.containers
                           if any(keyword in c.name.lower()
                                 for keyword in ["api gateway", "gateway", "kong", "apigee"])]

            if not api_gateways and len(external_systems) > 2:
                gaps.append({
                    "area": "Integration Management",
                    "issue": f"{len(external_systems)} external integrations without centralized gateway",
                    "severity": "medium",
                    "impact": "Decentralized integrations are harder to monitor, secure, and manage.",
                    "current_state": f"Multiple direct integrations: {', '.join([s.name for s in external_systems[:5]])}",
                    "desired_state": "Centralized API Gateway managing external integrations"
                })

                recommendations.append({
                    "title": "Centralize external integrations through API Gateway",
                    "description": "Route external integrations through API Gateway for consistent security, monitoring, and transformation.",
                    "pattern": "API Gateway, Integration Hub",
                    "technologies": ["Kong", "Apigee", "AWS API Gateway", "MuleSoft"],
                    "implementation_effort": "medium",
                    "priority": char.rating,
                    "rationale": "Centralized gateway provides consistent integration patterns, security, and observability.",
                    "tradeoffs": "Additional infrastructure, potential bottleneck",
                    "implementation_steps": [
                        "Select API Gateway solution",
                        "Define integration patterns and standards",
                        "Migrate external integrations to gateway",
                        "Implement rate limiting and security",
                        "Add monitoring and logging",
                        "Document integration guidelines"
                    ]
                })

        # Check 2: Message broker for async integration
        message_brokers = [c for c in model.containers
                          if any(keyword in c.name.lower() or (c.technology and keyword in c.technology.lower())
                                for keyword in ["kafka", "rabbitmq", "message", "event", "pubsub"])]

        if len(external_systems) > 1 and not message_brokers and char.rating in ["critical", "high"]:
            gaps.append({
                "area": "Asynchronous Integration",
                "issue": "No message broker for asynchronous integration patterns",
                "severity": "medium",
                "impact": "Synchronous-only integration limits flexibility and creates tight coupling with external systems.",
                "current_state": "No message broker detected",
                "desired_state": "Message broker enabling asynchronous, decoupled integration"
            })

            recommendations.append({
                "title": "Implement message broker for async integration",
                "description": "Use message broker to enable asynchronous, resilient integration patterns.",
                "pattern": "Message-Oriented Middleware, Event-Driven Integration",
                "technologies": ["Apache Kafka", "RabbitMQ", "AWS SNS/SQS", "Azure Service Bus"],
                "implementation_effort": "medium",
                "priority": char.rating,
                "rationale": "Asynchronous integration improves resilience, scalability, and decoupling from external systems.",
                "tradeoffs": "Complexity, eventual consistency, message ordering challenges",
                "implementation_steps": [
                    "Select message broker technology",
                    "Design message schemas and topics",
                    "Implement publishers for outbound integration",
                    "Implement consumers for inbound integration",
                    "Add error handling and dead letter queues",
                    "Monitor message flow and lag"
                ]
            })

        # Check 3: API documentation and standards
        # Look for OpenAPI/Swagger documentation
        doc_indicators = any("swagger" in c.name.lower() or "openapi" in c.name.lower()
                            for c in model.containers)

        if not doc_indicators and len(external_systems) > 0:
            recommendations.append({
                "title": "Implement API documentation with OpenAPI/Swagger",
                "description": "Use OpenAPI specification to document APIs for better interoperability.",
                "pattern": "API Documentation, Contract-First Design",
                "technologies": ["OpenAPI/Swagger", "Postman", "Stoplight", "Redoc"],
                "implementation_effort": "low",
                "priority": "medium",
                "rationale": "Well-documented APIs improve interoperability by making integration easier for external systems.",
                "tradeoffs": "Effort to maintain documentation in sync with code",
                "implementation_steps": [
                    "Define OpenAPI specification for all APIs",
                    "Generate API documentation from spec",
                    "Publish documentation to API portal",
                    "Implement contract testing",
                    "Keep documentation updated with changes"
                ]
            })

        # Check 4: Data transformation and mapping
        if len(external_systems) > 2 and char.rating in ["critical", "high"]:
            recommendations.append({
                "title": "Implement data transformation layer",
                "description": "Use transformation layer to handle different data formats from external systems.",
                "pattern": "Adapter Pattern, Data Transformation",
                "technologies": ["Apache Camel", "Spring Integration", "MuleSoft", "ETL Tools"],
                "implementation_effort": "medium",
                "priority": char.rating,
                "rationale": "Data transformation layer enables interoperability with diverse external systems using different formats.",
                "tradeoffs": "Additional complexity, transformation overhead",
                "implementation_steps": [
                    "Identify data format requirements per integration",
                    "Design canonical data model",
                    "Implement adapters for each external system",
                    "Add transformation logic (JSON, XML, CSV, etc.)",
                    "Validate transformed data",
                    "Monitor transformation errors"
                ]
            })

        return {"gaps": gaps, "recommendations": recommendations}

    @agent.tool
    async def analyze_usability(ctx: RunContext[ArchCharDependencies]) -> dict[str, Any]:
        """Analyze Usability against C4 model.

        Evaluates:
        - Frontend architecture
        - CDN for performance
        - Mobile support
        - Accessibility considerations

        Returns:
            Dict with 'gaps' and 'recommendations'
        """
        model = ctx.deps.c4_model
        char = ctx.deps.characteristics_by_name.get("Usability")

        if not char:
            return {"gaps": [], "recommendations": []}

        gaps = []
        recommendations = []

        # Check 1: Frontend/UI containers
        frontend_containers = [c for c in model.containers
                              if any(keyword in c.name.lower()
                                    for keyword in ["frontend", "ui", "web", "portal", "app", "client"])]

        if not frontend_containers:
            gaps.append({
                "area": "User Interface",
                "issue": "No frontend/UI containers detected",
                "severity": "high" if char.rating in ["critical", "high"] else "medium",
                "impact": "Without proper frontend architecture, usability will suffer.",
                "current_state": "No visible frontend containers",
                "desired_state": "Well-architected frontend with modern UX patterns"
            })

            recommendations.append({
                "title": "Implement modern frontend architecture",
                "description": "Build responsive, accessible frontend using modern frameworks and patterns.",
                "pattern": "Single Page Application, Progressive Web App",
                "technologies": ["React", "Vue", "Angular", "Next.js", "Svelte"],
                "implementation_effort": "high",
                "priority": char.rating,
                "rationale": "Modern frontend architecture is essential for good usability and user experience.",
                "tradeoffs": "Complexity, learning curve, build tooling overhead",
                "implementation_steps": [
                    "Select frontend framework",
                    "Design component architecture",
                    "Implement responsive layouts",
                    "Add accessibility features (ARIA, keyboard nav)",
                    "Implement progressive enhancement",
                    "Optimize for performance (lazy loading, code splitting)"
                ]
            })

        # Check 2: CDN for static content
        cdn_containers = [c for c in model.containers
                         if any(keyword in c.name.lower()
                               for keyword in ["cdn", "cloudfront", "cloudflare", "akamai", "fastly"])]

        if not cdn_containers and frontend_containers and char.rating in ["critical", "high"]:
            gaps.append({
                "area": "Content Delivery",
                "issue": "No CDN detected for frontend static assets",
                "severity": "medium",
                "impact": "Without CDN, page load times will be slower, especially for global users, hurting usability.",
                "current_state": "No CDN infrastructure",
                "desired_state": "CDN serving static assets with edge caching"
            })

            recommendations.append({
                "title": "Implement CDN for static content delivery",
                "description": "Use CDN to serve static assets closer to users for faster page loads.",
                "pattern": "Content Delivery Network, Edge Caching",
                "technologies": ["CloudFront", "Cloudflare", "Akamai", "Fastly", "Azure CDN"],
                "implementation_effort": "low",
                "priority": "high",
                "rationale": "CDN dramatically improves page load times, a key usability metric.",
                "tradeoffs": "Additional cost, cache invalidation complexity",
                "implementation_steps": [
                    "Select CDN provider",
                    "Configure CDN distribution",
                    "Update asset URLs to CDN endpoints",
                    "Set appropriate cache headers",
                    "Implement cache invalidation strategy",
                    "Monitor CDN performance and hit rates"
                ]
            })

        # Check 3: Mobile considerations
        mobile_containers = [c for c in model.containers
                            if any(keyword in c.name.lower()
                                  for keyword in ["mobile", "ios", "android", "react native", "flutter"])]

        if not mobile_containers and char.notes and "mobile" in char.notes.lower():
            gaps.append({
                "area": "Mobile Support",
                "issue": "Mobile support mentioned in notes but no mobile architecture detected",
                "severity": "medium" if char.rating == "high" else "high",
                "impact": "Growing mobile usage demands mobile-optimized experience.",
                "current_state": "No mobile-specific containers detected",
                "desired_state": "Responsive web or native mobile apps"
            })

            recommendations.append({
                "title": "Implement mobile-first responsive design or native apps",
                "description": "Ensure excellent mobile experience through responsive web or native mobile apps.",
                "pattern": "Mobile-First Design, Progressive Web App",
                "technologies": ["React Native", "Flutter", "PWA", "Responsive CSS", "Mobile-First Frameworks"],
                "implementation_effort": "high",
                "priority": char.rating,
                "rationale": "Mobile users expect optimized experiences. Mobile-first design improves usability for all users.",
                "tradeoffs": "Development effort, testing complexity across devices",
                "implementation_steps": [
                    "Analyze mobile usage patterns",
                    "Choose approach (responsive web vs native)",
                    "Design mobile-first UI/UX",
                    "Implement responsive breakpoints",
                    "Test across devices and screen sizes",
                    "Optimize for touch interactions and mobile performance"
                ]
            })

        # Check 4: Accessibility
        if char.notes and ("accessibility" in char.notes.lower() or "wcag" in char.notes.lower() or "a11y" in char.notes.lower()):
            recommendations.append({
                "title": "Ensure accessibility compliance (WCAG 2.1)",
                "description": "Implement accessibility best practices to ensure usability for all users.",
                "pattern": "Accessible Design, WCAG Compliance",
                "technologies": ["ARIA", "Accessibility Testing Tools", "Screen Readers", "axe-core"],
                "implementation_effort": "medium",
                "priority": char.rating,
                "rationale": "Accessibility improves usability for everyone and is often legally required.",
                "tradeoffs": "Additional development and testing effort",
                "implementation_steps": [
                    "Audit current accessibility status",
                    "Implement semantic HTML",
                    "Add ARIA labels and roles",
                    "Ensure keyboard navigation support",
                    "Test with screen readers",
                    "Implement automated accessibility testing in CI/CD",
                    "Achieve WCAG 2.1 AA compliance minimum"
                ]
            })

        # Check 5: Performance monitoring for UX
        monitoring_containers = [c for c in model.containers
                                if any(keyword in c.name.lower()
                                      for keyword in ["monitoring", "observability", "rum", "analytics"])]

        if frontend_containers and not any("rum" in c.name.lower() or "analytics" in c.name.lower()
                                          for c in monitoring_containers):
            recommendations.append({
                "title": "Implement Real User Monitoring (RUM)",
                "description": "Add RUM to track actual user experience metrics like page load time and interactivity.",
                "pattern": "Real User Monitoring, Performance Monitoring",
                "technologies": ["New Relic Browser", "Datadog RUM", "Google Analytics", "Sentry Performance"],
                "implementation_effort": "low",
                "priority": "medium",
                "rationale": "RUM provides actual user experience data to identify and fix usability issues.",
                "tradeoffs": "Small performance overhead, privacy considerations",
                "implementation_steps": [
                    "Select RUM solution",
                    "Integrate JavaScript agent",
                    "Configure key metrics (Core Web Vitals)",
                    "Set up alerts for poor performance",
                    "Create dashboards for UX metrics",
                    "Regularly review and act on insights"
                ]
            })

        return {"gaps": gaps, "recommendations": recommendations}

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

        # Map characteristic names to tool prompts
        tool_map = {
            "Availability": "analyze the architecture for Availability",
            "Scalability": "analyze the architecture for Scalability",
            "Performance": "analyze the architecture for Performance",
            "Security": "analyze the architecture for Security",
            "Reliability": "analyze the architecture for Reliability",
            "Fault Tolerance": "analyze the architecture for Fault Tolerance",
            "Recoverability": "analyze the architecture for Recoverability",
            "Maintainability": "analyze the architecture for Maintainability",
            "Testability": "analyze the architecture for Testability",
            "Deployability": "analyze the architecture for Deployability",
            "Configurability": "analyze the architecture for Configurability",
            "Extensibility": "analyze the architecture for Extensibility",
            "Interoperability": "analyze the architecture for Interoperability",
            "Usability": "analyze the architecture for Usability",
        }

        # Run analysis for each selected characteristic
        analyses: list[CharacteristicAnalysis] = []
        all_gaps: list[CharacteristicGap] = []
        all_recommendations: list[CharacteristicRecommendation] = []

        for char in selected_chars:
            if char.name not in tool_map:
                # Skip custom characteristics or unsupported ones
                continue

            try:
                # Run the agent with the characteristic-specific prompt
                result = await self.agent.run(
                    tool_map[char.name],
                    deps=deps,
                )

                # Extract gaps and recommendations from result
                # The result.data should be the return value from the tool
                analysis_data = result.data if hasattr(result, 'data') else {}

                gaps_data = analysis_data.get("gaps", [])
                recs_data = analysis_data.get("recommendations", [])

                # Convert to model objects
                gaps = [CharacteristicGap(**gap) for gap in gaps_data]
                recommendations = [CharacteristicRecommendation(**rec) for rec in recs_data]

                # Calculate score for this characteristic
                score = calculate_score(gaps, char.rating)

                # Create analysis result
                analysis = CharacteristicAnalysis(
                    characteristic_name=char.name,
                    characteristic_rating=char.rating,
                    is_top_characteristic=char.isTop,
                    notes=char.notes,
                    score=score,
                    gaps=gaps,
                    recommendations=recommendations,
                    compliance_status="compliant" if score >= 90 else
                                    "mostly_compliant" if score >= 70 else
                                    "partially_compliant" if score >= 50 else
                                    "non_compliant",
                )

                analyses.append(analysis)
                all_gaps.extend(gaps)
                all_recommendations.extend(recommendations)

            except Exception as e:
                # Log error but continue with other characteristics
                print(f"Warning: Failed to analyze {char.name}: {e}")
                continue

        # Calculate overall score (weighted by rating)
        if analyses:
            total_weight = 0
            weighted_score = 0
            for analysis in analyses:
                weight = {"critical": 4, "high": 3, "medium": 2, "low": 1}.get(
                    analysis.characteristic_rating, 2
                )
                weighted_score += analysis.score * weight
                total_weight += weight

            overall_score = int(weighted_score / total_weight) if total_weight > 0 else 0
        else:
            overall_score = 0

        # Identify critical and high priority gaps
        critical_gaps = [g for g in all_gaps if g.severity == "critical"]
        high_priority_gaps = [g for g in all_gaps if g.severity == "high"]

        # Prioritize recommendations (critical and high priority, top 10)
        priority_recs = [
            r for r in all_recommendations
            if r.priority in ["critical", "high"]
        ]
        priority_recs.sort(
            key=lambda r: (0 if r.priority == "critical" else 1, r.implementation_effort),
            reverse=False
        )
        top_recommendations = priority_recs[:10]

        # Extract recommended patterns and technologies
        patterns_set = set()
        technologies_set = set()

        for rec in all_recommendations:
            if rec.pattern:
                patterns_set.add(rec.pattern)
            technologies_set.update(rec.technologies)

        architecture_patterns_recommended = sorted(patterns_set)
        technologies_recommended = sorted(technologies_set)

        # Generate executive summary
        critical_count = len(critical_gaps)
        high_count = len(high_priority_gaps)
        compliant_count = len([a for a in analyses if a.score >= 70])

        summary_parts = [
            f"Architecture analysis completed for {len(analyses)} characteristics.",
            f"Overall compliance score: {overall_score}/100.",
        ]

        if overall_score >= 80:
            summary_parts.append(
                f"The architecture is well-aligned with the specified characteristics ({compliant_count}/{len(analyses)} compliant)."
            )
        elif overall_score >= 60:
            summary_parts.append(
                f"The architecture is partially aligned ({compliant_count}/{len(analyses)} compliant) with room for improvement."
            )
        else:
            summary_parts.append(
                f"The architecture needs significant improvements ({compliant_count}/{len(analyses)} compliant)."
            )

        if critical_count > 0:
            summary_parts.append(
                f"⚠️ {critical_count} critical gap{'s' if critical_count != 1 else ''} identified requiring immediate attention."
            )

        if high_count > 0:
            summary_parts.append(
                f"{high_count} high-priority gap{'s' if high_count != 1 else ''} should be addressed soon."
            )

        if top_recommendations:
            summary_parts.append(
                f"Top {len(top_recommendations)} recommendations provided with implementation guidance."
            )

        executive_summary = " ".join(summary_parts)

        # Identify top characteristics with issues
        top_char_analyses = [a for a in analyses if a.is_top_characteristic]
        top_char_issues = [a for a in top_char_analyses if a.score < 70]

        if top_char_issues:
            summary_parts.append(
                f"\n\nTop characteristics needing attention: {', '.join([a.characteristic_name for a in top_char_issues])}."
            )
            executive_summary = " ".join(summary_parts)

        return ArchCharAnalysisResult(
            project_name=archchar_input.projectName,
            architect=archchar_input.architect,
            analysis_date=archchar_input.date,
            notes=archchar_input.notes,
            characteristics_analyzed=len(analyses),
            overall_score=overall_score,
            analyses=analyses,
            critical_gaps=critical_gaps,
            high_priority_gaps=high_priority_gaps,
            top_recommendations=top_recommendations,
            executive_summary=executive_summary,
            architecture_patterns_recommended=architecture_patterns_recommended,
            technologies_recommended=technologies_recommended,
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


# ============================================================================
# Report Generation Functions
# ============================================================================


def generate_markdown_report(result: ArchCharAnalysisResult) -> str:
    """Generate detailed Markdown report from analysis result.

    Args:
        result: ArchCharAnalysisResult

    Returns:
        Markdown formatted report
    """
    lines = []

    # Header
    lines.append("# Architecture Characteristics Analysis Report")
    lines.append("")
    lines.append(f"**Project:** {result.project_name}")
    lines.append(f"**Architect:** {result.architect}")
    lines.append(f"**Analysis Date:** {result.analysis_date}")
    lines.append("")

    # Executive Summary
    lines.append("## Executive Summary")
    lines.append("")
    lines.append(result.executive_summary)
    lines.append("")

    # Overall Score
    lines.append("## Overall Compliance Score")
    lines.append("")
    score_bar = "█" * (result.overall_score // 5) + "░" * (20 - result.overall_score // 5)
    lines.append(f"**{result.overall_score}/100** {score_bar}")
    lines.append("")

    # Critical Gaps
    if result.critical_gaps:
        lines.append(f"## ⚠️ Critical Gaps ({len(result.critical_gaps)})")
        lines.append("")
        for gap in result.critical_gaps:
            lines.append(f"### {gap.area}")
            lines.append(f"- **Issue:** {gap.issue}")
            lines.append(f"- **Impact:** {gap.impact}")
            if gap.current_state:
                lines.append(f"- **Current State:** {gap.current_state}")
            if gap.desired_state:
                lines.append(f"- **Desired State:** {gap.desired_state}")
            lines.append("")

    # High Priority Gaps
    if result.high_priority_gaps:
        lines.append(f"## High Priority Gaps ({len(result.high_priority_gaps)})")
        lines.append("")
        for gap in result.high_priority_gaps:
            lines.append(f"### {gap.area}")
            lines.append(f"- **Issue:** {gap.issue}")
            lines.append(f"- **Impact:** {gap.impact}")
            lines.append("")

    # Top Recommendations
    if result.top_recommendations:
        lines.append(f"## Top Recommendations ({len(result.top_recommendations)})")
        lines.append("")
        for i, rec in enumerate(result.top_recommendations, 1):
            lines.append(f"### {i}. {rec.title}")
            lines.append("")
            lines.append(f"**Priority:** {rec.priority.upper()} | **Effort:** {rec.implementation_effort}")
            lines.append("")
            lines.append(f"**Description:** {rec.description}")
            lines.append("")
            if rec.pattern:
                lines.append(f"**Pattern:** {rec.pattern}")
            lines.append(f"**Technologies:** {', '.join(rec.technologies)}")
            lines.append("")
            lines.append(f"**Rationale:** {rec.rationale}")
            lines.append("")
            lines.append(f"**Trade-offs:** {rec.tradeoffs}")
            lines.append("")
            lines.append("**Implementation Steps:**")
            for step in rec.implementation_steps:
                lines.append(f"1. {step}")
            lines.append("")

    # Detailed Analysis by Characteristic
    lines.append("## Detailed Analysis by Characteristic")
    lines.append("")

    # Sort analyses: top characteristics first, then by score
    top_analyses = [a for a in result.analyses if a.is_top_characteristic]
    other_analyses = [a for a in result.analyses if not a.is_top_characteristic]

    top_analyses.sort(key=lambda a: a.score)
    other_analyses.sort(key=lambda a: a.score)

    all_analyses = top_analyses + other_analyses

    for analysis in all_analyses:
        top_badge = " 🌟 **[TOP 7]**" if analysis.is_top_characteristic else ""
        lines.append(f"### {analysis.characteristic_name}{top_badge}")
        lines.append("")
        lines.append(f"**Rating:** {analysis.characteristic_rating.upper()} | "
                    f"**Score:** {analysis.score}/100 | "
                    f"**Status:** {analysis.compliance_status.replace('_', ' ').title()}")
        lines.append("")

        if analysis.notes:
            lines.append(f"**Notes:** {analysis.notes}")
            lines.append("")

        if analysis.gaps:
            lines.append(f"**Gaps Identified ({len(analysis.gaps)}):**")
            lines.append("")
            for gap in analysis.gaps:
                lines.append(f"- **[{gap.severity.upper()}]** {gap.area}: {gap.issue}")
            lines.append("")

        if analysis.recommendations:
            lines.append(f"**Recommendations ({len(analysis.recommendations)}):**")
            lines.append("")
            for rec in analysis.recommendations:
                lines.append(f"- **{rec.title}** ({rec.priority} priority, {rec.implementation_effort} effort)")
                lines.append(f"  - {rec.description}")
            lines.append("")

    # Architecture Patterns Recommended
    if result.architecture_patterns_recommended:
        lines.append("## Architecture Patterns Recommended")
        lines.append("")
        for pattern in result.architecture_patterns_recommended:
            lines.append(f"- {pattern}")
        lines.append("")

    # Technologies Recommended
    if result.technologies_recommended:
        lines.append("## Technologies Recommended")
        lines.append("")
        # Group by category if possible, otherwise just list
        for tech in result.technologies_recommended[:20]:  # Limit to top 20
            lines.append(f"- {tech}")
        if len(result.technologies_recommended) > 20:
            lines.append(f"- ... and {len(result.technologies_recommended) - 20} more")
        lines.append("")

    # Footer
    lines.append("---")
    lines.append("")
    lines.append("*Generated by SAAT Architecture Characteristics Analysis Agent*")
    lines.append("*Based on Mark Richards' Architecture Characteristics Methodology*")

    return "\n".join(lines)


def export_json_report(result: ArchCharAnalysisResult) -> str:
    """Export analysis result as JSON.

    Args:
        result: ArchCharAnalysisResult

    Returns:
        JSON string
    """
    return result.model_dump_json(indent=2)


def save_report(
    result: ArchCharAnalysisResult,
    output_path: str | Path,
    format: str = "markdown"
) -> None:
    """Save analysis report to file.

    Args:
        result: ArchCharAnalysisResult
        output_path: Output file path
        format: Report format ('markdown' or 'json')

    Raises:
        ValueError: If format is not supported
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if format.lower() == "markdown":
        content = generate_markdown_report(result)
        path.write_text(content)
    elif format.lower() == "json":
        content = export_json_report(result)
        path.write_text(content)
    else:
        raise ValueError(f"Unsupported format: {format}. Use 'markdown' or 'json'.")
