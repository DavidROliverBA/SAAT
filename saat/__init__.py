"""SAAT - Solution Architecture Agent Toolkit.

AI-powered C4 architecture discovery and documentation using PydanticAI.
"""

from saat.models import (
    AgentChecklist,
    AgentError,
    ApprovalRequest,
    ApprovalResponse,
    BusinessContext,
    C4Model,
    ChecklistItem,
    Component,
    ComplianceRequirement,
    Container,
    CriticalityLevel,
    DiscoveryResult,
    ElementType,
    ExternalSystem,
    Interface,
    ModelMetadata,
    PatternMatch,
    Pipeline,
    PipelineStep,
    ProjectRequirements,
    Relationship,
    RelationshipType,
    Requirement,
    Stakeholder,
    SystemContext,
    TechnicalConstraint,
    UserStory,
    ValidationIssue,
    ValidationResult,
)

__version__ = "1.0.0"
__all__ = [
    # Models
    "C4Model",
    "SystemContext",
    "Container",
    "Component",
    "ExternalSystem",
    "Relationship",
    "ModelMetadata",
    "Interface",
    # Enums
    "CriticalityLevel",
    "ElementType",
    "RelationshipType",
    # Discovery
    "DiscoveryResult",
    "PatternMatch",
    # Business Context
    "BusinessContext",
    "Stakeholder",
    "ComplianceRequirement",
    # Validation
    "ValidationResult",
    "ValidationIssue",
    "AgentError",
    # Pipeline
    "Pipeline",
    "PipelineStep",
    # Requirements (Greenfield)
    "ProjectRequirements",
    "Requirement",
    "UserStory",
    "TechnicalConstraint",
    # Checklists & Approval
    "AgentChecklist",
    "ChecklistItem",
    "ApprovalRequest",
    "ApprovalResponse",
]
