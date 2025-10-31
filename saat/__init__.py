"""SAAT - Solution Architecture Agent Toolkit.

AI-powered C4 architecture discovery and documentation using PydanticAI.
"""

from saat.models import (
    AgentError,
    BusinessContext,
    C4Model,
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
    Relationship,
    RelationshipType,
    Stakeholder,
    SystemContext,
    ValidationIssue,
    ValidationResult,
)

__version__ = "2.0.0"
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
]
