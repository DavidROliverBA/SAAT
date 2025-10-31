"""Structurizr JSON format models for C4 architecture interchange.

This module provides Pydantic models matching the Structurizr JSON schema,
enabling SAAT to export/import C4 models in the industry-standard format
for compatibility with tools like bac4-standalone editor and other Structurizr tools.

Reference: https://github.com/structurizr/json
"""

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class Location(str, Enum):
    """Element location - internal or external to enterprise."""

    INTERNAL = "Internal"
    EXTERNAL = "External"
    UNSPECIFIED = "Unspecified"


class InteractionStyle(str, Enum):
    """Communication pattern between elements."""

    SYNCHRONOUS = "Synchronous"
    ASYNCHRONOUS = "Asynchronous"


# ============================================================================
# Core Elements
# ============================================================================


class Perspective(BaseModel):
    """Additional perspective on an element (e.g., security, performance)."""

    name: str = Field(..., description="Perspective name")
    description: str = Field(..., description="Perspective description")
    value: Optional[str] = Field(None, description="Perspective value")


class Relationship(BaseModel):
    """Relationship between two elements."""

    id: Optional[str] = Field(None, description="Unique relationship identifier")
    sourceId: str = Field(..., description="Source element ID")
    destinationId: str = Field(..., description="Destination element ID")
    description: str = Field(..., description="Relationship description (e.g., 'uses', 'calls')")
    technology: Optional[str] = Field(None, description="Technology used (e.g., 'HTTPS', 'gRPC')")
    interactionStyle: Optional[InteractionStyle] = Field(None, description="Sync or async")
    tags: Optional[str] = Field(None, description="Comma-separated tags")
    url: Optional[str] = Field(None, description="Reference URL")
    properties: Optional[dict[str, str]] = Field(None, description="Custom properties")
    perspectives: Optional[list[Perspective]] = Field(None, description="Additional perspectives")
    linkedRelationshipId: Optional[str] = Field(None, description="Parent relationship reference")


class Person(BaseModel):
    """Person who interacts with the system."""

    id: str = Field(..., description="Unique person identifier")
    name: str = Field(..., description="Person name or role")
    description: Optional[str] = Field(None, description="Person description")
    location: Optional[Location] = Field(Location.UNSPECIFIED, description="Internal or external")
    tags: Optional[str] = Field(None, description="Comma-separated tags")
    url: Optional[str] = Field(None, description="Reference URL")
    group: Optional[str] = Field(None, description="Group name")
    properties: Optional[dict[str, str]] = Field(None, description="Custom properties")
    perspectives: Optional[list[Perspective]] = Field(None, description="Additional perspectives")
    relationships: Optional[list[Relationship]] = Field(default_factory=list, description="Outgoing relationships")


class Component(BaseModel):
    """C4 Component - code-level module or service."""

    id: str = Field(..., description="Unique component identifier")
    name: str = Field(..., description="Component name")
    description: Optional[str] = Field(None, description="Component description")
    technology: Optional[str] = Field(None, description="Technology (e.g., 'Spring Bean', 'React Component')")
    tags: Optional[str] = Field(None, description="Comma-separated tags")
    url: Optional[str] = Field(None, description="Reference URL")
    group: Optional[str] = Field(None, description="Group name")
    properties: Optional[dict[str, str]] = Field(None, description="Custom properties")
    perspectives: Optional[list[Perspective]] = Field(None, description="Additional perspectives")
    relationships: Optional[list[Relationship]] = Field(default_factory=list, description="Outgoing relationships")


class Container(BaseModel):
    """C4 Container - application or data store."""

    id: str = Field(..., description="Unique container identifier")
    name: str = Field(..., description="Container name")
    description: Optional[str] = Field(None, description="Container description")
    technology: Optional[str] = Field(None, description="Technology (e.g., 'Spring Boot', 'PostgreSQL')")
    tags: Optional[str] = Field(None, description="Comma-separated tags")
    url: Optional[str] = Field(None, description="Reference URL")
    components: Optional[list[Component]] = Field(default_factory=list, description="Nested components")
    group: Optional[str] = Field(None, description="Group name")
    properties: Optional[dict[str, str]] = Field(None, description="Custom properties")
    perspectives: Optional[list[Perspective]] = Field(None, description="Additional perspectives")
    relationships: Optional[list[Relationship]] = Field(default_factory=list, description="Outgoing relationships")


class SoftwareSystem(BaseModel):
    """C4 Software System - high-level system."""

    id: str = Field(..., description="Unique system identifier")
    name: str = Field(..., description="System name")
    description: Optional[str] = Field(None, description="System description")
    location: Optional[Location] = Field(Location.UNSPECIFIED, description="Internal or external")
    tags: Optional[str] = Field(None, description="Comma-separated tags")
    url: Optional[str] = Field(None, description="Reference URL")
    containers: Optional[list[Container]] = Field(default_factory=list, description="Nested containers")
    group: Optional[str] = Field(None, description="Group name")
    properties: Optional[dict[str, str]] = Field(None, description="Custom properties")
    perspectives: Optional[list[Perspective]] = Field(None, description="Additional perspectives")
    relationships: Optional[list[Relationship]] = Field(default_factory=list, description="Outgoing relationships")


class DeploymentNode(BaseModel):
    """Infrastructure node (server, container, etc.)."""

    id: str = Field(..., description="Unique node identifier")
    name: str = Field(..., description="Node name")
    description: Optional[str] = Field(None, description="Node description")
    technology: Optional[str] = Field(None, description="Technology (e.g., 'AWS EC2', 'Docker')")
    environment: Optional[str] = Field(None, description="Environment (e.g., 'Production', 'Development')")
    instances: Optional[int] = Field(1, description="Number of instances")
    tags: Optional[str] = Field(None, description="Comma-separated tags")
    url: Optional[str] = Field(None, description="Reference URL")
    children: Optional[list["DeploymentNode"]] = Field(default_factory=list, description="Nested nodes")
    containerInstances: Optional[list[dict]] = Field(default_factory=list, description="Container instances")
    infrastructureNodes: Optional[list[dict]] = Field(default_factory=list, description="Infrastructure nodes")
    properties: Optional[dict[str, str]] = Field(None, description="Custom properties")
    perspectives: Optional[list[Perspective]] = Field(None, description="Additional perspectives")
    relationships: Optional[list[Relationship]] = Field(default_factory=list, description="Outgoing relationships")


class Enterprise(BaseModel):
    """Enterprise information."""

    name: str = Field(..., description="Enterprise name")


class Model(BaseModel):
    """C4 Model containing all elements and relationships."""

    enterprise: Optional[Enterprise] = Field(None, description="Enterprise information")
    people: Optional[list[Person]] = Field(default_factory=list, description="People/actors")
    softwareSystems: Optional[list[SoftwareSystem]] = Field(default_factory=list, description="Software systems")
    deploymentNodes: Optional[list[DeploymentNode]] = Field(default_factory=list, description="Deployment nodes")
    properties: Optional[dict[str, str]] = Field(None, description="Custom properties")


# ============================================================================
# Views
# ============================================================================


class AutomaticLayout(BaseModel):
    """Automatic layout configuration."""

    rankDirection: str = Field(..., description="Layout direction: TopBottom, BottomTop, LeftRight, RightLeft")
    rankSeparation: Optional[int] = Field(None, description="Separation between ranks")
    nodeSeparation: Optional[int] = Field(None, description="Separation between nodes")
    edgeSeparation: Optional[int] = Field(None, description="Separation between edges")
    vertices: Optional[bool] = Field(None, description="Create vertices for edges")


class ElementView(BaseModel):
    """Element view in a diagram."""

    id: str = Field(..., description="Element ID")
    x: Optional[int] = Field(None, description="X coordinate")
    y: Optional[int] = Field(None, description="Y coordinate")


class RelationshipView(BaseModel):
    """Relationship view in a diagram."""

    id: str = Field(..., description="Relationship ID")
    description: Optional[str] = Field(None, description="Override description")
    order: Optional[str] = Field(None, description="Display order")
    vertices: Optional[list[dict]] = Field(None, description="Routing vertices")
    routing: Optional[str] = Field(None, description="Routing algorithm")
    position: Optional[int] = Field(None, description="Label position")


class SystemLandscapeView(BaseModel):
    """System landscape view showing all systems."""

    key: str = Field(..., description="Unique view key")
    title: Optional[str] = Field(None, description="View title")
    description: Optional[str] = Field(None, description="View description")
    order: Optional[int] = Field(None, description="Display order")
    enterpriseBoundaryVisible: Optional[bool] = Field(True, description="Show enterprise boundary")
    elements: Optional[list[ElementView]] = Field(default_factory=list, description="Elements in view")
    relationships: Optional[list[RelationshipView]] = Field(default_factory=list, description="Relationships in view")
    automaticLayout: Optional[AutomaticLayout] = Field(None, description="Auto layout config")
    properties: Optional[dict[str, str]] = Field(None, description="Custom properties")


class SystemContextView(BaseModel):
    """System context view for a specific system."""

    key: str = Field(..., description="Unique view key")
    softwareSystemId: str = Field(..., description="System to show context for")
    title: Optional[str] = Field(None, description="View title")
    description: Optional[str] = Field(None, description="View description")
    order: Optional[int] = Field(None, description="Display order")
    enterpriseBoundaryVisible: Optional[bool] = Field(True, description="Show enterprise boundary")
    elements: Optional[list[ElementView]] = Field(default_factory=list, description="Elements in view")
    relationships: Optional[list[RelationshipView]] = Field(default_factory=list, description="Relationships in view")
    automaticLayout: Optional[AutomaticLayout] = Field(None, description="Auto layout config")
    properties: Optional[dict[str, str]] = Field(None, description="Custom properties")


class ContainerView(BaseModel):
    """Container view for a system."""

    key: str = Field(..., description="Unique view key")
    softwareSystemId: str = Field(..., description="System to show containers for")
    title: Optional[str] = Field(None, description="View title")
    description: Optional[str] = Field(None, description="View description")
    order: Optional[int] = Field(None, description="Display order")
    externalSoftwareSystemBoundariesVisible: Optional[bool] = Field(True, description="Show external boundaries")
    elements: Optional[list[ElementView]] = Field(default_factory=list, description="Elements in view")
    relationships: Optional[list[RelationshipView]] = Field(default_factory=list, description="Relationships in view")
    automaticLayout: Optional[AutomaticLayout] = Field(None, description="Auto layout config")
    properties: Optional[dict[str, str]] = Field(None, description="Custom properties")


class ComponentView(BaseModel):
    """Component view for a container."""

    key: str = Field(..., description="Unique view key")
    containerId: str = Field(..., description="Container to show components for")
    title: Optional[str] = Field(None, description="View title")
    description: Optional[str] = Field(None, description="View description")
    order: Optional[int] = Field(None, description="Display order")
    externalContainerBoundariesVisible: Optional[bool] = Field(True, description="Show external boundaries")
    elements: Optional[list[ElementView]] = Field(default_factory=list, description="Elements in view")
    relationships: Optional[list[RelationshipView]] = Field(default_factory=list, description="Relationships in view")
    automaticLayout: Optional[AutomaticLayout] = Field(None, description="Auto layout config")
    properties: Optional[dict[str, str]] = Field(None, description="Custom properties")


class ViewConfiguration(BaseModel):
    """Configuration for all views."""

    styles: Optional[dict] = Field(None, description="Styling configuration")
    themes: Optional[list[str]] = Field(None, description="Theme URLs")
    branding: Optional[dict] = Field(None, description="Branding configuration")
    terminology: Optional[dict] = Field(None, description="Custom terminology")
    properties: Optional[dict[str, str]] = Field(None, description="Custom properties")


class Views(BaseModel):
    """Collection of all views."""

    systemLandscapeViews: Optional[list[SystemLandscapeView]] = Field(default_factory=list)
    systemContextViews: Optional[list[SystemContextView]] = Field(default_factory=list)
    containerViews: Optional[list[ContainerView]] = Field(default_factory=list)
    componentViews: Optional[list[ComponentView]] = Field(default_factory=list)
    configuration: Optional[ViewConfiguration] = Field(None, description="View configuration")
    properties: Optional[dict[str, str]] = Field(None, description="Custom properties")


# ============================================================================
# Workspace (Top Level)
# ============================================================================


class WorkspaceConfiguration(BaseModel):
    """Workspace configuration."""

    users: Optional[list[dict]] = Field(None, description="User configurations")
    properties: Optional[dict[str, str]] = Field(None, description="Custom properties")


class Workspace(BaseModel):
    """Structurizr workspace - top-level container."""

    id: Optional[int] = Field(None, description="Workspace ID")
    name: str = Field(..., description="Workspace name")
    description: Optional[str] = Field(None, description="Workspace description")
    version: Optional[str] = Field(None, description="Version number")
    revision: Optional[int] = Field(None, description="Revision number")
    lastModifiedDate: Optional[str] = Field(None, description="ISO 8601 timestamp")
    lastModifiedUser: Optional[str] = Field(None, description="User identifier")
    lastModifiedAgent: Optional[str] = Field(None, description="Agent identifier (e.g., 'SAAT')")
    model: Model = Field(..., description="C4 model")
    views: Optional[Views] = Field(None, description="Diagram views")
    configuration: Optional[WorkspaceConfiguration] = Field(None, description="Workspace configuration")
    properties: Optional[dict[str, str]] = Field(None, description="Custom properties")

    @classmethod
    def create_empty(cls, name: str, description: str) -> "Workspace":
        """Create an empty workspace with default structure.

        Args:
            name: Workspace name
            description: Workspace description

        Returns:
            Empty workspace
        """
        return cls(
            name=name,
            description=description,
            version="1.0.0",
            lastModifiedDate=datetime.now().isoformat(),
            lastModifiedAgent="SAAT",
            model=Model(
                people=[],
                softwareSystems=[],
                deploymentNodes=[],
            ),
            views=Views(
                systemLandscapeViews=[],
                systemContextViews=[],
                containerViews=[],
                componentViews=[],
            ),
        )


# Enable forward references for DeploymentNode
DeploymentNode.model_rebuild()
