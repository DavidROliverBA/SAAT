"""Generator Agent - Converts discovery results into C4 models using PydanticAI."""

from datetime import datetime
from typing import Optional

from pydantic_ai import Agent, RunContext

from saat.models import (
    BusinessContext,
    C4Model,
    CriticalityLevel,
    DiscoveryResult,
    ModelMetadata,
)


# ============================================================================
# Dependencies for Generator Agent
# ============================================================================


class GeneratorDependencies:
    """Dependencies for C4 model generation."""

    def __init__(
        self,
        discovery: DiscoveryResult,
        business_context: Optional[BusinessContext] = None,
        project_name: Optional[str] = None,
    ):
        self.discovery = discovery
        self.business_context = business_context
        self.project_name = project_name or discovery.repository
        self.id_counters: dict[str, int] = {}

    def generate_id(self, prefix: str, suffix: str) -> str:
        """Generate unique ID for elements.

        Args:
            prefix: ID prefix (SYS, CON, COM, EXT, REL)
            suffix: Context-specific suffix

        Returns:
            Unique ID like "SYS-API-001"
        """
        key = f"{prefix}-{suffix}"
        current = self.id_counters.get(key, 0)
        self.id_counters[key] = current + 1
        return f"{prefix}-{suffix.upper()}-{current + 1:03d}"


# ============================================================================
# Create Generator Agent
# ============================================================================


def create_generator_agent(model: str = "anthropic:claude-sonnet-4") -> Agent[
    GeneratorDependencies, C4Model
]:
    """Create a Generator Agent using PydanticAI.

    Args:
        model: Model identifier

    Returns:
        Configured PydanticAI Agent
    """
    agent: Agent[GeneratorDependencies, C4Model] = Agent(
        model,
        deps_type=GeneratorDependencies,
        result_type=C4Model,
        system_prompt="""You are an expert solution architect specializing in creating C4 architecture models.

Your role is to:
1. Convert discovery results into structured C4 models
2. Identify systems, containers, components, and external dependencies
3. Create meaningful relationships between elements
4. Assign appropriate criticality levels based on business context
5. Generate complete, valid C4 models following best practices

C4 Model Structure:
- Level 1 (System Context): High-level systems and external dependencies
- Level 2 (Containers): Applications, databases, services within systems
- Level 3 (Components): Internal modules and classes within containers
- Relationships: Connections with protocols, data flows, and descriptions

Criticality Levels:
- CS1: Critical (99.99% uptime) - Payment, security, core business
- CS2: High (99.9% uptime) - Important services
- SL1: Standard (99.5% uptime) - Regular services
- SL2: Medium (99% uptime) - Supporting services
- STANDARD: Basic (best effort) - Non-critical services

Generate comprehensive, production-ready C4 models.""",
    )

    @agent.tool
    async def analyze_criticality(
        ctx: RunContext[GeneratorDependencies],
    ) -> dict[str, str]:
        """Analyze and suggest criticality levels based on context.

        Args:
            ctx: Agent context

        Returns:
            Criticality suggestions
        """
        suggestions: dict[str, str] = {}

        # Check for critical keywords in technologies and patterns
        discovery = ctx.deps.discovery
        technologies_lower = [t.lower() for t in discovery.technologies]

        # Payment/financial = CS1
        if any(
            keyword in " ".join(technologies_lower)
            for keyword in ["payment", "stripe", "paypal", "financial", "banking"]
        ):
            suggestions["payment_services"] = "CS1"

        # Authentication/security = CS2
        if any(
            keyword in " ".join(technologies_lower)
            for keyword in ["auth", "oauth", "jwt", "security", "keycloak"]
        ):
            suggestions["auth_services"] = "CS2"

        # Database = Based on business context
        if any(
            keyword in " ".join(technologies_lower)
            for keyword in ["postgres", "mysql", "mongodb", "database"]
        ):
            if ctx.deps.business_context:
                # Check compliance requirements
                has_compliance = bool(ctx.deps.business_context.compliance)
                suggestions["database"] = "CS1" if has_compliance else "CS2"
            else:
                suggestions["database"] = "CS2"

        # API services = SL1 by default
        if any(
            keyword in " ".join(technologies_lower)
            for keyword in ["api", "rest", "graphql", "grpc"]
        ):
            suggestions["api_services"] = "SL1"

        return suggestions

    @agent.tool
    async def infer_relationships(
        ctx: RunContext[GeneratorDependencies],
    ) -> list[dict[str, str]]:
        """Infer relationships between components based on patterns.

        Args:
            ctx: Agent context

        Returns:
            List of suggested relationships
        """
        relationships = []
        discovery = ctx.deps.discovery
        patterns = [p.pattern.lower() for p in discovery.patterns]

        # Microservices pattern suggests service-to-service communication
        if "microservices" in patterns or "microservice" in patterns:
            relationships.append(
                {
                    "type": "uses",
                    "protocol": "HTTP/REST",
                    "description": "Microservices communicate via REST APIs",
                }
            )

        # Event-driven suggests message queue relationships
        if "event-driven" in patterns or "event driven" in patterns:
            relationships.append(
                {
                    "type": "uses",
                    "protocol": "Message Queue",
                    "description": "Services communicate asynchronously via events",
                }
            )

        # Database patterns
        technologies_lower = [t.lower() for t in discovery.technologies]
        if any("database" in tech or "db" in tech for tech in technologies_lower):
            relationships.append(
                {"type": "uses", "protocol": "SQL/NoSQL", "description": "Data persistence"}
            )

        return relationships

    return agent


# ============================================================================
# High-level Generator Agent wrapper
# ============================================================================


class GeneratorAgent:
    """High-level wrapper for the generator agent."""

    def __init__(self, model: str = "anthropic:claude-sonnet-4"):
        """Initialize Generator Agent.

        Args:
            model: Model identifier
        """
        self.agent = create_generator_agent(model)
        self.model = model

    async def generate_model(
        self,
        discovery: DiscoveryResult,
        business_context: Optional[BusinessContext] = None,
        project_name: Optional[str] = None,
        author: str = "SAAT",
    ) -> C4Model:
        """Generate C4 model from discovery results.

        Args:
            discovery: Discovery results from repository analysis
            business_context: Optional business context for better model generation
            project_name: Optional project name override
            author: Model author

        Returns:
            Complete C4 model
        """
        deps = GeneratorDependencies(discovery, business_context, project_name)

        # Build context message
        context_msg = f"""Generate a complete C4 architecture model from this discovery:

**Discovery Results:**
- Repository: {discovery.repository}
- Technologies: {', '.join(discovery.technologies)}
- Patterns: {', '.join([p.pattern for p in discovery.patterns])}
- Entry Points: {', '.join(discovery.entry_points)}
- Confidence: {discovery.confidence:.2f}
"""

        if business_context:
            context_msg += f"""
**Business Context:**
- Purpose: {business_context.purpose}
- Stakeholders: {len(business_context.stakeholders)}
- Capabilities: {', '.join(business_context.capabilities)}
- Compliance: {', '.join([c.framework for c in business_context.compliance])}
"""

        context_msg += """
Create a comprehensive C4 model with:
1. System Context (Level 1) - Main systems
2. Containers (Level 2) - Services, databases, applications
3. Components (Level 3) - Internal modules (if patterns suggest specific components)
4. External Systems - Third-party dependencies
5. Relationships - Connections between all elements

Use the tools to analyze criticality and infer relationships. Generate meaningful IDs, descriptions, and metadata."""

        result = await self.agent.run(context_msg, deps=deps)

        # Ensure metadata is set correctly
        model = result.data
        if not model.metadata:
            model.metadata = ModelMetadata(
                project=project_name or discovery.repository,
                author=author,
                created=datetime.now(),
                last_modified=datetime.now(),
                description=f"Architecture model for {discovery.repository}",
                version="1.0.0",
                tags=[p.pattern for p in discovery.patterns],
            )

        return model

    async def refine_model(self, model: C4Model, feedback: str) -> C4Model:
        """Refine an existing C4 model based on feedback.

        Args:
            model: Existing C4 model
            feedback: Feedback or refinement instructions

        Returns:
            Refined C4 model
        """
        # Create a minimal discovery result for context
        discovery = DiscoveryResult(
            repository=model.metadata.project,
            technologies=[],
            patterns=[],
            entry_points=[],
            confidence=1.0,
        )

        deps = GeneratorDependencies(discovery)

        result = await self.agent.run(
            f"""Refine this existing C4 model based on the following feedback:

**Feedback:** {feedback}

**Current Model:**
- Systems: {len(model.systems)}
- Containers: {len(model.containers)}
- Components: {len(model.components)}
- Externals: {len(model.externals)}
- Relationships: {len(model.relationships)}

Apply the requested changes while maintaining model validity and consistency.""",
            deps=deps,
        )

        refined = result.data
        refined.metadata.last_modified = datetime.now()

        return refined


# ============================================================================
# Convenience functions
# ============================================================================


async def generate_c4_model(
    discovery: DiscoveryResult,
    business_context: Optional[BusinessContext] = None,
    model: str = "anthropic:claude-sonnet-4",
) -> C4Model:
    """Convenience function to generate a C4 model.

    Args:
        discovery: Discovery results
        business_context: Optional business context
        model: Model to use

    Returns:
        C4 model
    """
    agent = GeneratorAgent(model)
    return await agent.generate_model(discovery, business_context)
