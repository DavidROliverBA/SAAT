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

    # More tools will be added below...
    # (Security, Reliability, Maintainability, Testability, Deployability,
    #  Fault Tolerance, Recoverability, Interoperability, Configurability,
    #  Extensibility, Usability)

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
