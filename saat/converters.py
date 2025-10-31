"""Converters between SAAT's internal C4 model and Structurizr JSON format.

This module enables round-trip conversion between SAAT's rich internal model
(with criticality levels, interfaces, etc.) and the industry-standard Structurizr
format for compatibility with tools like bac4-standalone editor.

SAAT Model → Structurizr: For exporting to visual editors
Structurizr → SAAT Model: For importing from visual editors
"""

from datetime import datetime
from typing import Optional

from saat import structurizr as sz
from saat.models import (
    C4Model,
    Component,
    Container,
    CriticalityLevel,
    ExternalSystem,
    Interface,
    ModelMetadata,
    Relationship,
    SystemContext,
)


# ============================================================================
# SAAT → Structurizr Conversion
# ============================================================================


def saat_to_structurizr(c4_model: C4Model) -> sz.Workspace:
    """Convert SAAT C4 model to Structurizr workspace.

    Args:
        c4_model: SAAT C4 model

    Returns:
        Structurizr workspace ready for export
    """
    # Create workspace
    workspace = sz.Workspace(
        name=c4_model.metadata.project,
        description=c4_model.metadata.description,
        version=c4_model.metadata.version,
        lastModifiedDate=c4_model.metadata.last_modified.isoformat(),
        lastModifiedAgent="SAAT",
        model=sz.Model(
            people=[],
            softwareSystems=[],
            deploymentNodes=[],
        ),
        views=sz.Views(
            systemLandscapeViews=[],
            systemContextViews=[],
            containerViews=[],
            componentViews=[],
        ),
    )

    # Track ID mappings
    system_map: dict[str, sz.SoftwareSystem] = {}

    # Convert systems
    for system in c4_model.systems:
        sz_system = _convert_system_to_structurizr(system)
        system_map[system.id] = sz_system
        workspace.model.softwareSystems.append(sz_system)

    # Convert external systems
    for external in c4_model.externals:
        sz_external = _convert_external_to_structurizr(external)
        workspace.model.softwareSystems.append(sz_external)

    # Convert containers (add to their parent systems)
    for container in c4_model.containers:
        if container.system_id in system_map:
            sz_container = _convert_container_to_structurizr(container)
            system_map[container.system_id].containers.append(sz_container)

    # Convert components (add to their parent containers)
    for component in c4_model.components:
        # Find parent container
        for system in workspace.model.softwareSystems:
            for sz_container in system.containers or []:
                if sz_container.id == component.container_id:
                    sz_component = _convert_component_to_structurizr(component)
                    sz_container.components.append(sz_component)
                    break

    # Convert relationships
    _add_relationships_to_structurizr(c4_model, workspace)

    # Create default views
    _create_default_views(c4_model, workspace)

    return workspace


def _convert_system_to_structurizr(system: SystemContext) -> sz.SoftwareSystem:
    """Convert SAAT system to Structurizr software system."""
    # Build tags
    tags = ",".join(system.tags) if system.tags else None

    # Build properties for SAAT-specific fields
    properties = {
        "criticality": system.criticality.value,
        "saat_type": system.type.value,
    }
    if system.owner:
        properties["owner"] = system.owner
    if system.repository:
        properties["repository"] = system.repository
    if system.responsibilities:
        properties["responsibilities"] = "; ".join(system.responsibilities)

    return sz.SoftwareSystem(
        id=system.id,
        name=system.name,
        description=system.description,
        location=sz.Location.INTERNAL,
        tags=tags,
        url=system.documentation,
        containers=[],
        properties=properties,
        relationships=[],
    )


def _convert_external_to_structurizr(external: ExternalSystem) -> sz.SoftwareSystem:
    """Convert SAAT external system to Structurizr external software system."""
    tags = ",".join(external.tags) if external.tags else "External"

    properties = {
        "saat_type": "ExternalSystem",
    }
    if external.vendor:
        properties["vendor"] = external.vendor

    return sz.SoftwareSystem(
        id=external.id,
        name=external.name,
        description=external.description,
        location=sz.Location.EXTERNAL,
        tags=tags,
        url=external.documentation,
        containers=[],
        properties=properties,
        relationships=[],
    )


def _convert_container_to_structurizr(container: Container) -> sz.Container:
    """Convert SAAT container to Structurizr container."""
    # Technology: use first tech or all joined
    technology = ", ".join(container.technology) if container.technology else None

    tags = ",".join(container.tags) if container.tags else None

    # Store SAAT-specific data in properties
    properties = {
        "criticality": container.criticality.value,
        "saat_type": container.type.value,
    }
    if container.responsibilities:
        properties["responsibilities"] = "; ".join(container.responsibilities)
    if container.repository:
        properties["repository"] = container.repository

    # Store interfaces as properties (JSON-serializable)
    if container.interfaces:
        for i, interface in enumerate(container.interfaces):
            properties[f"interface_{i}_protocol"] = interface.protocol
            if interface.port:
                properties[f"interface_{i}_port"] = str(interface.port)
            if interface.authentication:
                properties[f"interface_{i}_auth"] = interface.authentication
            properties[f"interface_{i}_encrypted"] = str(interface.encrypted)

    return sz.Container(
        id=container.id,
        name=container.name,
        description=container.description,
        technology=technology,
        tags=tags,
        url=container.documentation,
        components=[],
        properties=properties,
        relationships=[],
    )


def _convert_component_to_structurizr(component: Component) -> sz.Component:
    """Convert SAAT component to Structurizr component."""
    technology = ", ".join(component.technology) if component.technology else None
    tags = ",".join(component.tags) if component.tags else None

    properties = {
        "saat_type": "Component",
    }
    if component.responsibilities:
        properties["responsibilities"] = "; ".join(component.responsibilities)

    return sz.Component(
        id=component.id,
        name=component.name,
        description=component.description,
        technology=technology,
        tags=tags,
        url=component.documentation,
        properties=properties,
        relationships=[],
    )


def _add_relationships_to_structurizr(c4_model: C4Model, workspace: sz.Workspace) -> None:
    """Add all relationships to Structurizr model."""
    # Build element lookup
    elements: dict[str, any] = {}

    for system in workspace.model.softwareSystems:
        elements[system.id] = system
        for container in system.containers or []:
            elements[container.id] = container
            for component in container.components or []:
                elements[component.id] = component

    for person in workspace.model.people or []:
        elements[person.id] = person

    # Convert relationships
    for rel in c4_model.relationships:
        sz_rel = sz.Relationship(
            id=rel.id,
            sourceId=rel.source,
            destinationId=rel.target,
            description=rel.description,
            technology=rel.technology,
            tags=",".join(rel.tags) if rel.tags else None,
            properties={"saat_type": rel.type.value},
        )

        # Add relationship to source element
        if rel.source in elements:
            source = elements[rel.source]
            if not source.relationships:
                source.relationships = []
            source.relationships.append(sz_rel)


def _create_default_views(c4_model: C4Model, workspace: sz.Workspace) -> None:
    """Create default views for the workspace."""
    # System landscape view
    if workspace.model.softwareSystems:
        landscape = sz.SystemLandscapeView(
            key="SystemLandscape",
            title=f"{workspace.name} - System Landscape",
            description="Overview of all systems",
            enterpriseBoundaryVisible=True,
            elements=[],
            relationships=[],
            automaticLayout=sz.AutomaticLayout(rankDirection="TopBottom", rankSeparation=150, nodeSeparation=150),
        )
        workspace.views.systemLandscapeViews.append(landscape)

    # System context views (one per internal system)
    for system in workspace.model.softwareSystems:
        if system.location == sz.Location.INTERNAL:
            context_view = sz.SystemContextView(
                key=f"SystemContext-{system.id}",
                softwareSystemId=system.id,
                title=f"{system.name} - System Context",
                description=f"System context diagram for {system.name}",
                enterpriseBoundaryVisible=True,
                elements=[],
                relationships=[],
                automaticLayout=sz.AutomaticLayout(rankDirection="TopBottom", rankSeparation=150, nodeSeparation=150),
            )
            workspace.views.systemContextViews.append(context_view)

            # Container view for this system
            if system.containers:
                container_view = sz.ContainerView(
                    key=f"Container-{system.id}",
                    softwareSystemId=system.id,
                    title=f"{system.name} - Containers",
                    description=f"Container diagram for {system.name}",
                    externalSoftwareSystemBoundariesVisible=True,
                    elements=[],
                    relationships=[],
                    automaticLayout=sz.AutomaticLayout(rankDirection="TopBottom", rankSeparation=150, nodeSeparation=150),
                )
                workspace.views.containerViews.append(container_view)

                # Component views (one per container with components)
                for container in system.containers:
                    if container.components:
                        component_view = sz.ComponentView(
                            key=f"Component-{container.id}",
                            containerId=container.id,
                            title=f"{container.name} - Components",
                            description=f"Component diagram for {container.name}",
                            externalContainerBoundariesVisible=True,
                            elements=[],
                            relationships=[],
                            automaticLayout=sz.AutomaticLayout(rankDirection="TopBottom", rankSeparation=150, nodeSeparation=150),
                        )
                        workspace.views.componentViews.append(component_view)


# ============================================================================
# Structurizr → SAAT Conversion
# ============================================================================


def structurizr_to_saat(workspace: sz.Workspace) -> C4Model:
    """Convert Structurizr workspace to SAAT C4 model.

    Args:
        workspace: Structurizr workspace

    Returns:
        SAAT C4 model
    """
    # Create metadata
    metadata = ModelMetadata(
        project=workspace.name,
        author=workspace.lastModifiedUser or "Unknown",
        created=datetime.now(),
        last_modified=datetime.fromisoformat(workspace.lastModifiedDate) if workspace.lastModifiedDate else datetime.now(),
        description=workspace.description or "",
        version=workspace.version or "1.0.0",
        tags=[],
    )

    # Initialize collections
    systems: list[SystemContext] = []
    externals: list[ExternalSystem] = []
    containers: list[Container] = []
    components: list[Component] = []
    relationships: list[Relationship] = []

    # Convert software systems
    for sz_system in workspace.model.softwareSystems or []:
        if sz_system.location == sz.Location.EXTERNAL:
            externals.append(_convert_structurizr_to_external(sz_system))
        else:
            systems.append(_convert_structurizr_to_system(sz_system))

        # Convert containers
        for sz_container in sz_system.containers or []:
            containers.append(_convert_structurizr_to_container(sz_container, sz_system.id))

            # Convert components
            for sz_component in sz_container.components or []:
                components.append(_convert_structurizr_to_component(sz_component, sz_container.id))

    # Convert all relationships
    relationships = _extract_all_relationships(workspace)

    return C4Model(
        metadata=metadata,
        systems=systems,
        externals=externals,
        containers=containers,
        components=components,
        relationships=relationships,
    )


def _convert_structurizr_to_system(sz_system: sz.SoftwareSystem) -> SystemContext:
    """Convert Structurizr software system to SAAT system."""
    props = sz_system.properties or {}

    criticality = CriticalityLevel(props.get("criticality", "STANDARD"))
    tags = sz_system.tags.split(",") if sz_system.tags else []

    responsibilities = []
    if "responsibilities" in props:
        responsibilities = props["responsibilities"].split("; ")

    return SystemContext(
        id=sz_system.id,
        name=sz_system.name,
        description=sz_system.description or "",
        technology=[],  # Not stored at system level in Structurizr
        tags=tags,
        responsibilities=responsibilities,
        criticality=criticality,
        owner=props.get("owner"),
        repository=props.get("repository"),
        documentation=sz_system.url,
    )


def _convert_structurizr_to_external(sz_system: sz.SoftwareSystem) -> ExternalSystem:
    """Convert Structurizr external system to SAAT external system."""
    props = sz_system.properties or {}
    tags = sz_system.tags.split(",") if sz_system.tags else []

    return ExternalSystem(
        id=sz_system.id,
        name=sz_system.name,
        description=sz_system.description or "",
        vendor=props.get("vendor"),
        tags=tags,
        documentation=sz_system.url,
    )


def _convert_structurizr_to_container(sz_container: sz.Container, system_id: str) -> Container:
    """Convert Structurizr container to SAAT container."""
    props = sz_container.properties or {}

    criticality = CriticalityLevel(props.get("criticality", "STANDARD"))
    tags = sz_container.tags.split(",") if sz_container.tags else []
    technology = sz_container.technology.split(", ") if sz_container.technology else []

    responsibilities = []
    if "responsibilities" in props:
        responsibilities = props["responsibilities"].split("; ")

    # Reconstruct interfaces from properties
    interfaces: list[Interface] = []
    i = 0
    while f"interface_{i}_protocol" in props:
        interface = Interface(
            protocol=props[f"interface_{i}_protocol"],
            port=int(props[f"interface_{i}_port"]) if f"interface_{i}_port" in props else None,
            authentication=props.get(f"interface_{i}_auth"),
            encrypted=props.get(f"interface_{i}_encrypted", "False") == "True",
        )
        interfaces.append(interface)
        i += 1

    from saat.models import ElementType

    element_type = ElementType.CONTAINER
    if "saat_type" in props:
        element_type = ElementType(props["saat_type"])

    return Container(
        id=sz_container.id,
        name=sz_container.name,
        description=sz_container.description or "",
        type=element_type,
        technology=technology,
        tags=tags,
        system_id=system_id,
        responsibilities=responsibilities,
        criticality=criticality,
        interfaces=interfaces,
        repository=props.get("repository"),
        documentation=sz_container.url,
    )


def _convert_structurizr_to_component(sz_component: sz.Component, container_id: str) -> Component:
    """Convert Structurizr component to SAAT component."""
    props = sz_component.properties or {}
    tags = sz_component.tags.split(",") if sz_component.tags else []
    technology = sz_component.technology.split(", ") if sz_component.technology else []

    responsibilities = []
    if "responsibilities" in props:
        responsibilities = props["responsibilities"].split("; ")

    return Component(
        id=sz_component.id,
        name=sz_component.name,
        description=sz_component.description or "",
        technology=technology,
        tags=tags,
        container_id=container_id,
        responsibilities=responsibilities,
        documentation=sz_component.url,
    )


def _extract_all_relationships(workspace: sz.Workspace) -> list[Relationship]:
    """Extract all relationships from Structurizr workspace."""
    from saat.models import RelationshipType

    relationships: list[Relationship] = []

    # Helper to add relationships from any element
    def add_from_element(element: any) -> None:
        if not element.relationships:
            return

        for sz_rel in element.relationships:
            props = sz_rel.properties or {}

            # Determine relationship type
            rel_type = RelationshipType.USES
            if "saat_type" in props:
                rel_type = RelationshipType(props["saat_type"])

            tags = sz_rel.tags.split(",") if sz_rel.tags else []

            relationship = Relationship(
                id=sz_rel.id or f"{sz_rel.sourceId}-{sz_rel.destinationId}",
                source=sz_rel.sourceId,
                target=sz_rel.destinationId,
                description=sz_rel.description,
                technology=sz_rel.technology,
                type=rel_type,
                tags=tags,
                documentation=sz_rel.url,
            )
            relationships.append(relationship)

    # Extract from all element types
    for system in workspace.model.softwareSystems or []:
        add_from_element(system)
        for container in system.containers or []:
            add_from_element(container)
            for component in container.components or []:
                add_from_element(component)

    for person in workspace.model.people or []:
        add_from_element(person)

    for node in workspace.model.deploymentNodes or []:
        add_from_element(node)

    return relationships


# ============================================================================
# Convenience Functions
# ============================================================================


def export_to_structurizr_file(c4_model: C4Model, output_path: str) -> None:
    """Export SAAT model to Structurizr JSON file.

    Args:
        c4_model: SAAT C4 model
        output_path: Path to output JSON file
    """
    from pathlib import Path

    workspace = saat_to_structurizr(c4_model)
    Path(output_path).write_text(workspace.model_dump_json(indent=2, exclude_none=True))


def import_from_structurizr_file(input_path: str) -> C4Model:
    """Import SAAT model from Structurizr JSON file.

    Args:
        input_path: Path to Structurizr JSON file

    Returns:
        SAAT C4 model
    """
    import json
    from pathlib import Path

    data = json.loads(Path(input_path).read_text())
    workspace = sz.Workspace(**data)
    return structurizr_to_saat(workspace)
