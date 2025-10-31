"""Security Agent - Analyzes security posture from C4 architecture models."""

from pathlib import Path
from typing import Any, Optional

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext

from saat.agents.base import BaseAgentWithChecklist
from saat.models import AgentChecklist, C4Model, ChecklistItem


class SecurityIssue(BaseModel):
    """Security issue found in architecture."""

    id: str = Field(..., description="Issue ID")
    severity: str = Field(..., description="critical, high, medium, low")
    category: str = Field(..., description="encryption, authentication, data-flow, etc.")
    title: str = Field(..., description="Issue title")
    description: str = Field(..., description="Detailed description")
    affected_elements: list[str] = Field(default_factory=list, description="Affected element IDs")
    recommendation: str = Field(..., description="How to fix")
    compliance_impact: list[str] = Field(default_factory=list, description="Affected frameworks")


class SecurityReport(BaseModel):
    """Security analysis report."""

    model_name: str = Field(..., description="Model analyzed")
    total_issues: int = Field(..., description="Total issues found")
    critical: int = Field(default=0)
    high: int = Field(default=0)
    medium: int = Field(default=0)
    low: int = Field(default=0)
    issues: list[SecurityIssue] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    overall_score: float = Field(..., ge=0.0, le=100.0, description="Security score")


class SecurityDependencies:
    """Dependencies for security analysis."""

    def __init__(self, model: C4Model, threat_model: bool = False):
        self.model = model
        self.threat_model = threat_model


def create_security_agent(model_name: str = "anthropic:claude-sonnet-4") -> Agent[
    SecurityDependencies, SecurityReport
]:
    """Create security analysis agent.

    Args:
        model_name: Model identifier

    Returns:
        Configured PydanticAI agent
    """
    agent: Agent[SecurityDependencies, SecurityReport] = Agent(
        model_name,
        deps_type=SecurityDependencies,
        result_type=SecurityReport,
        system_prompt="""You are a cybersecurity expert specializing in application security architecture.

Analyze C4 architecture models for security issues:

1. **Encryption & Data Protection**
   - Unencrypted communications (HTTP vs HTTPS)
   - Unencrypted data at rest
   - Missing encryption for sensitive data
   - Weak encryption algorithms

2. **Authentication & Authorization**
   - Missing authentication
   - Weak authentication (basic auth, no MFA)
   - Missing authorization checks
   - Overly permissive access

3. **Data Flow Security**
   - Sensitive data flowing through insecure channels
   - Logs containing sensitive data
   - Data exfiltration risks
   - Missing data validation

4. **Infrastructure Security**
   - Public access to sensitive systems
   - Missing network segmentation
   - No firewalls or WAF
   - Missing intrusion detection

5. **Compliance**
   - PCI-DSS violations (payment data)
   - HIPAA violations (health data)
   - GDPR violations (personal data)
   - SOC2 requirements

Rate severity:
- **critical**: Immediate security risk, exploitable
- **high**: Significant risk, should fix ASAP
- **medium**: Moderate risk, fix soon
- **low**: Minor risk, consider fixing

Provide specific, actionable recommendations.
Calculate overall security score (0-100) based on issues found.
""",
    )

    @agent.tool
    async def check_encryption(ctx: RunContext[SecurityDependencies]) -> dict[str, Any]:
        """Check encryption configurations.

        Args:
            ctx: Agent context

        Returns:
            Dictionary with encryption issues
        """
        model = ctx.deps.model
        issues = []

        # Check container interfaces
        for container in model.containers:
            for interface in container.interfaces:
                if not interface.encrypted:
                    issues.append({
                        "element": container.name,
                        "issue": f"Interface on port {interface.port} is not encrypted",
                        "severity": "high" if interface.protocol in ["HTTP", "TCP"] else "medium"
                    })

        # Check relationships
        for rel in model.relationships:
            if rel.protocol in ["HTTP", "TCP", "UDP"] and "encrypt" not in rel.description.lower():
                issues.append({
                    "relationship": rel.id,
                    "issue": f"Relationship uses {rel.protocol} without encryption",
                    "severity": "high"
                })

        return {"encryption_issues": issues, "count": len(issues)}

    @agent.tool
    async def check_authentication(ctx: RunContext[SecurityDependencies]) -> dict[str, Any]:
        """Check authentication mechanisms.

        Args:
            ctx: Agent context

        Returns:
            Dictionary with authentication issues
        """
        model = ctx.deps.model
        issues = []

        for container in model.containers:
            for interface in container.interfaces:
                if not interface.authentication or interface.authentication == "none":
                    issues.append({
                        "element": container.name,
                        "issue": "No authentication configured",
                        "severity": "critical"
                    })
                elif "basic" in interface.authentication.lower():
                    issues.append({
                        "element": container.name,
                        "issue": "Using basic authentication (weak)",
                        "severity": "high"
                    })

        return {"authentication_issues": issues, "count": len(issues)}

    @agent.tool
    async def check_sensitive_data(ctx: RunContext[SecurityDependencies]) -> dict[str, Any]:
        """Check handling of sensitive data.

        Args:
            ctx: Agent context

        Returns:
            Dictionary with sensitive data issues
        """
        model = ctx.deps.model
        issues = []

        # Check for sensitive keywords in tags
        sensitive_keywords = ["payment", "credit", "card", "ssn", "health", "phi", "pii", "password"]

        for container in model.containers:
            is_sensitive = any(
                keyword in tag.lower() or keyword in container.name.lower()
                for keyword in sensitive_keywords
                for tag in container.tags
            )

            if is_sensitive and container.criticality not in ["CS1", "CS2"]:
                issues.append({
                    "element": container.name,
                    "issue": "Handles sensitive data but has low criticality",
                    "severity": "high"
                })

        return {"sensitive_data_issues": issues, "count": len(issues)}

    return agent


class SecurityAgent(BaseAgentWithChecklist):
    """Security Agent for analyzing architecture security posture."""

    def __init__(self, model: str = "anthropic:claude-sonnet-4"):
        """Initialize security agent.

        Args:
            model: Model identifier
        """
        super().__init__("SecurityAgent", model)
        self.agent = create_security_agent(model)

    async def create_checklist(
        self,
        task_description: str,
        context: Optional[dict[str, Any]] = None
    ) -> AgentChecklist:
        """Generate security analysis checklist.

        Args:
            task_description: Task description
            context: Should contain 'model' and optional 'threat_model'

        Returns:
            AgentChecklist
        """
        threat_model = context.get("threat_model", False) if context else False

        items = [
            ChecklistItem(
                id="1",
                description="Load and analyze C4 model",
                estimated_duration="5s"
            ),
            ChecklistItem(
                id="2",
                description="Check encryption configurations",
                estimated_duration="10s",
                dependencies=["1"]
            ),
            ChecklistItem(
                id="3",
                description="Verify authentication mechanisms",
                estimated_duration="10s",
                dependencies=["1"]
            ),
            ChecklistItem(
                id="4",
                description="Analyze data flows for sensitive data",
                estimated_duration="15s",
                dependencies=["1"]
            ),
            ChecklistItem(
                id="5",
                description="Check infrastructure security controls",
                estimated_duration="10s",
                dependencies=["1"]
            ),
            ChecklistItem(
                id="6",
                description="Identify compliance violations",
                estimated_duration="10s",
                dependencies=["1"]
            )
        ]

        if threat_model:
            items.append(
                ChecklistItem(
                    id="7",
                    description="Generate threat model",
                    estimated_duration="30s",
                    dependencies=["2", "3", "4", "5", "6"]
                )
            )

        items.append(
            ChecklistItem(
                id="8" if threat_model else "7",
                description="Generate security report with recommendations",
                estimated_duration="10s",
                dependencies=["2", "3", "4", "5", "6"]
            )
        )

        return AgentChecklist(
            agent_name=self.agent_name,
            task_description=task_description,
            items=items,
            estimated_total_duration="1-2 minutes" if not threat_model else "2-3 minutes",
            requires_approval=True
        )

    async def analyze_security(
        self,
        model: C4Model,
        threat_model: bool = False,
        output_file: Optional[str] = None,
        auto_approve: bool = False
    ) -> dict[str, Any]:
        """Analyze security posture of C4 model.

        Args:
            model: C4 model to analyze
            threat_model: Generate threat model
            output_file: Optional output file for report
            auto_approve: Skip approval prompts

        Returns:
            Dictionary with security report and analysis
        """
        context = {
            "model": model,
            "threat_model": threat_model
        }

        # Execute with checklist
        result = await self.execute_with_checklist(
            task_description=f"Security analysis{' with threat modeling' if threat_model else ''}",
            auto_approve=auto_approve,
            context=context
        )

        if result["cancelled"]:
            return result

        # Perform analysis
        deps = SecurityDependencies(model, threat_model)

        prompt = f"""Analyze the security posture of this architecture:

**Model**: {model.metadata.project}
**Systems**: {len(model.systems)}
**Containers**: {len(model.containers)}
**External Systems**: {len(model.externals)}

Use the tools to:
1. Check encryption configurations
2. Verify authentication
3. Analyze sensitive data handling

Identify all security issues with severity ratings and specific recommendations.
Calculate an overall security score (0-100).
"""

        agent_result = await self.agent.run(prompt, deps=deps)
        security_report = agent_result.data

        result["security_report"] = security_report
        result["summary"] = {
            "overall_score": security_report.overall_score,
            "total_issues": security_report.total_issues,
            "critical": security_report.critical,
            "high": security_report.high,
            "medium": security_report.medium,
            "low": security_report.low
        }

        # Save report if requested
        if output_file:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(security_report.model_dump_json(indent=2))
            result["output_file"] = output_file

        return result


async def analyze_security(
    model: C4Model,
    threat_model: bool = False,
    model_name: str = "anthropic:claude-sonnet-4",
    auto_approve: bool = False
) -> SecurityReport:
    """Convenience function to analyze security.

    Args:
        model: C4 model to analyze
        threat_model: Generate threat model
        model_name: Model to use
        auto_approve: Skip approval prompts

    Returns:
        SecurityReport
    """
    agent = SecurityAgent(model_name)
    result = await agent.analyze_security(model, threat_model, None, auto_approve)

    if result.get("cancelled"):
        raise ValueError("Security analysis was cancelled")

    return result["security_report"]
