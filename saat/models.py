"""Pydantic models for C4 architecture and SAAT data structures."""

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator


class CriticalityLevel(str, Enum):
    """System criticality levels based on availability requirements."""

    CS1 = "CS1"  # Critical - 99.99% uptime
    CS2 = "CS2"  # High - 99.9% uptime
    SL1 = "SL1"  # Standard - 99.5% uptime
    SL2 = "SL2"  # Medium - 99% uptime
    STANDARD = "STANDARD"  # Basic - Best effort


class ElementType(str, Enum):
    """C4 model element types."""

    SYSTEM = "SystemContext"
    CONTAINER = "Container"
    COMPONENT = "Component"
    DATABASE = "Database"
    EXTERNAL = "ExternalSystem"


class RelationshipType(str, Enum):
    """Types of relationships between elements."""

    USES = "uses"
    CALLS = "calls"
    READS = "reads"
    WRITES = "writes"
    DEPENDS_ON = "depends_on"
    CONTAINS = "contains"


# ============================================================================
# C4 Model Components
# ============================================================================


class ModelMetadata(BaseModel):
    """Metadata about the C4 model."""

    project: str = Field(..., description="Project name")
    author: str = Field(..., description="Model author")
    created: datetime = Field(default_factory=datetime.now)
    last_modified: datetime = Field(default_factory=datetime.now)
    description: str = Field(..., description="Model description")
    version: str = Field(default="1.0.0", description="Model version")
    tags: list[str] = Field(default_factory=list)


class Interface(BaseModel):
    """Service interface specification."""

    protocol: str = Field(..., description="Communication protocol (HTTP, gRPC, etc.)")
    port: Optional[int] = Field(None, description="Port number")
    authentication: Optional[str] = Field(None, description="Authentication method")
    rate_limit: Optional[str] = Field(None, description="Rate limit specification")
    encrypted: bool = Field(default=False, description="Whether connection is encrypted")


class SystemContext(BaseModel):
    """C4 Level 1: System Context - High-level system."""

    id: str = Field(..., description="Unique system identifier")
    name: str = Field(..., description="System name")
    description: str = Field(..., description="System description")
    type: ElementType = Field(default=ElementType.SYSTEM)
    technology: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    responsibilities: list[str] = Field(default_factory=list)
    criticality: CriticalityLevel = Field(default=CriticalityLevel.STANDARD)
    owner: Optional[str] = Field(None, description="Team or person responsible")
    repository: Optional[str] = Field(None, description="Source code repository URL")
    documentation: Optional[str] = Field(None, description="Documentation URL")


class Container(BaseModel):
    """C4 Level 2: Container - Application or data store."""

    id: str = Field(..., description="Unique container identifier")
    name: str = Field(..., description="Container name")
    description: str = Field(..., description="Container description")
    type: ElementType = Field(...)
    technology: list[str] = Field(..., description="Technologies used")
    tags: list[str] = Field(default_factory=list)
    system_id: str = Field(..., description="Parent system ID")
    responsibilities: list[str] = Field(default_factory=list)
    criticality: CriticalityLevel = Field(default=CriticalityLevel.STANDARD)
    interfaces: list[Interface] = Field(default_factory=list)
    repository: Optional[str] = None
    documentation: Optional[str] = None


class Component(BaseModel):
    """C4 Level 3: Component - Internal module or class."""

    id: str = Field(..., description="Unique component identifier")
    name: str = Field(..., description="Component name")
    description: str = Field(..., description="Component description")
    type: str = Field(default="Component")
    technology: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    container_id: str = Field(..., description="Parent container ID")
    responsibilities: list[str] = Field(default_factory=list)
    file_path: Optional[str] = Field(None, description="Source code file path")


class ExternalSystem(BaseModel):
    """External system or dependency."""

    id: str = Field(..., description="Unique external system identifier")
    name: str = Field(..., description="External system name")
    description: str = Field(..., description="External system description")
    type: ElementType = Field(default=ElementType.EXTERNAL)
    technology: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    vendor: Optional[str] = Field(None, description="Vendor name")
    sla: Optional[str] = Field(None, description="Service level agreement")
    documentation: Optional[str] = None


class Relationship(BaseModel):
    """Relationship between architectural elements."""

    id: str = Field(..., description="Unique relationship identifier")
    source: str = Field(..., description="Source element ID")
    target: str = Field(..., description="Target element ID")
    description: str = Field(..., description="Relationship description")
    type: RelationshipType = Field(default=RelationshipType.USES)
    protocol: Optional[str] = Field(None, description="Communication protocol")
    synchronous: bool = Field(default=True, description="Synchronous or asynchronous")
    data_flow: list[str] = Field(default_factory=list, description="Data exchanged")


class C4Model(BaseModel):
    """Complete C4 architecture model."""

    version: str = Field(default="1.0.0")
    metadata: ModelMetadata
    systems: list[SystemContext] = Field(default_factory=list)
    containers: list[Container] = Field(default_factory=list)
    components: list[Component] = Field(default_factory=list)
    externals: list[ExternalSystem] = Field(default_factory=list)
    relationships: list[Relationship] = Field(default_factory=list)


# ============================================================================
# Discovery Results
# ============================================================================


class PatternMatch(BaseModel):
    """Detected architectural pattern."""

    pattern: str = Field(..., description="Pattern name")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    evidence: list[str] = Field(..., description="Evidence supporting the pattern")
    location: Optional[str] = Field(None, description="Where pattern was found")


class DiscoveryResult(BaseModel):
    """Results from repository discovery."""

    repository: str = Field(..., description="Repository path or name")
    technologies: list[str] = Field(default_factory=list)
    patterns: list[PatternMatch] = Field(default_factory=list)
    entry_points: list[str] = Field(default_factory=list)
    confidence: float = Field(..., ge=0.0, le=1.0)
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: dict[str, Any] = Field(default_factory=dict)


# ============================================================================
# Business Context
# ============================================================================


class Stakeholder(BaseModel):
    """Business stakeholder."""

    name: str
    role: str
    needs: list[str] = Field(default_factory=list)
    interactions: list[str] = Field(default_factory=list)


class ComplianceRequirement(BaseModel):
    """Compliance or regulatory requirement."""

    framework: str = Field(..., description="Compliance framework name")
    requirements: list[str] = Field(..., description="Specific requirements")
    applicable: bool = Field(default=True)


class BusinessContext(BaseModel):
    """Business context for architecture."""

    purpose: str = Field(..., description="Business purpose of the system")
    stakeholders: list[Stakeholder] = Field(default_factory=list)
    capabilities: list[str] = Field(default_factory=list)
    compliance: list[ComplianceRequirement] = Field(default_factory=list)


# ============================================================================
# Agent Results
# ============================================================================


class AgentError(BaseModel):
    """Error from agent execution."""

    code: str = Field(..., description="Error code")
    message: str = Field(..., description="Error message")
    severity: str = Field(default="error", description="error, warning, info")
    context: dict[str, Any] = Field(default_factory=dict)


class ValidationIssue(BaseModel):
    """Validation issue found in model."""

    severity: str = Field(..., description="error, warning, info")
    message: str = Field(..., description="Issue description")
    element_id: Optional[str] = Field(None, description="Affected element ID")
    suggestion: Optional[str] = Field(None, description="How to fix")


class ValidationResult(BaseModel):
    """Result from model validation."""

    valid: bool = Field(..., description="Whether model is valid")
    score: float = Field(..., ge=0.0, le=100.0, description="Validation score")
    issues: list[ValidationIssue] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.now)


# ============================================================================
# Pipeline Configuration
# ============================================================================


class PipelineStep(BaseModel):
    """Single step in an agent pipeline."""

    name: str = Field(..., description="Step name")
    agent: str = Field(..., description="Agent name to execute")
    task: str = Field(..., description="Task for agent")
    depends_on: list[str] = Field(default_factory=list, description="Prerequisite steps")
    required: bool = Field(default=True, description="Whether step is required")
    timeout: Optional[int] = Field(None, description="Timeout in seconds")


class Pipeline(BaseModel):
    """Agent pipeline configuration."""

    name: str = Field(..., description="Pipeline name")
    description: str = Field(..., description="Pipeline description")
    steps: list[PipelineStep] = Field(..., description="Pipeline steps")
    version: str = Field(default="1.0.0")


# ============================================================================
# Requirements (Greenfield Projects)
# ============================================================================


class Requirement(BaseModel):
    """Single functional or non-functional requirement."""

    id: str = Field(..., description="Requirement ID (e.g., REQ-001)")
    title: str = Field(..., description="Short title")
    description: str = Field(..., description="Detailed description")
    type: str = Field(..., description="functional, non-functional, constraint")
    priority: str = Field(default="medium", description="low, medium, high, critical")
    source: Optional[str] = Field(None, description="Source file or stakeholder")
    acceptance_criteria: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)


class UserStory(BaseModel):
    """User story for agile development."""

    id: str = Field(..., description="Story ID (e.g., US-001)")
    title: str = Field(..., description="Story title")
    as_a: str = Field(..., description="User role")
    i_want: str = Field(..., description="Desired functionality")
    so_that: str = Field(..., description="Business value")
    acceptance_criteria: list[str] = Field(default_factory=list)
    priority: str = Field(default="medium")
    estimated_effort: Optional[str] = Field(None, description="T-shirt size or points")


class TechnicalConstraint(BaseModel):
    """Technical constraint or limitation."""

    id: str = Field(..., description="Constraint ID")
    description: str = Field(..., description="Constraint description")
    type: str = Field(..., description="performance, security, compliance, etc.")
    rationale: Optional[str] = Field(None, description="Why this constraint exists")
    impact: str = Field(default="medium", description="Impact level")


class ProjectRequirements(BaseModel):
    """Complete requirements for a greenfield project."""

    project_name: str = Field(..., description="Project name")
    description: str = Field(..., description="Project description")
    requirements: list[Requirement] = Field(default_factory=list)
    user_stories: list[UserStory] = Field(default_factory=list)
    constraints: list[TechnicalConstraint] = Field(default_factory=list)
    stakeholders: list[Stakeholder] = Field(default_factory=list)
    success_criteria: list[str] = Field(default_factory=list)
    timeline: Optional[str] = Field(None, description="Project timeline")
    budget: Optional[str] = Field(None, description="Budget constraints")
    source_documents: list[str] = Field(default_factory=list, description="Source files")
    created: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)


# ============================================================================
# Agent Checklists & Approval
# ============================================================================


class ChecklistItem(BaseModel):
    """Single item in an agent's task checklist."""

    id: str = Field(..., description="Item ID")
    description: str = Field(..., description="Task description")
    estimated_duration: Optional[str] = Field(None, description="Estimated time")
    dependencies: list[str] = Field(default_factory=list, description="Dependent item IDs")
    completed: bool = Field(default=False)
    result: Optional[str] = Field(None, description="Result or output")


class AgentChecklist(BaseModel):
    """Checklist of tasks an agent will perform."""

    agent_name: str = Field(..., description="Agent performing tasks")
    task_description: str = Field(..., description="Overall task description")
    items: list[ChecklistItem] = Field(..., description="Checklist items")
    estimated_total_duration: Optional[str] = Field(None)
    requires_approval: bool = Field(default=True)
    approved: bool = Field(default=False)
    approved_by: Optional[str] = Field(None)
    approved_at: Optional[datetime] = Field(None)
    created_at: datetime = Field(default_factory=datetime.now)


class ApprovalRequest(BaseModel):
    """Request for human approval before proceeding."""

    checklist: AgentChecklist = Field(..., description="Tasks to approve")
    context: dict[str, Any] = Field(default_factory=dict, description="Additional context")
    timeout_seconds: Optional[int] = Field(None, description="Auto-approve after timeout")
    auto_approve: bool = Field(default=False, description="Skip approval (automation mode)")


class ApprovalResponse(BaseModel):
    """Response to approval request."""

    approved: bool = Field(..., description="Whether approved")
    modified_checklist: Optional[AgentChecklist] = Field(None, description="Modified checklist")
    feedback: Optional[str] = Field(None, description="User feedback")
    timestamp: datetime = Field(default_factory=datetime.now)
