"""Converters for Architecture Characteristics formats.

Import and export ArchCharCapture JSON format.
"""

import json
from pathlib import Path
from typing import Any

from saat.models_archchar import ArchCharacteristic, ArchCharInput


def import_archchar_json(file_path: str | Path) -> ArchCharInput:
    """Import ArchCharCapture JSON file.

    Args:
        file_path: Path to ArchCharCapture JSON file

    Returns:
        ArchCharInput model

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If JSON is invalid or doesn't match schema
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"ArchCharCapture file not found: {path}")

    try:
        data = json.loads(path.read_text())
        return ArchCharInput(**data)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {path}: {e}")
    except Exception as e:
        raise ValueError(f"Failed to parse ArchCharCapture JSON: {e}")


def export_archchar_json(archchar_input: ArchCharInput, file_path: str | Path) -> None:
    """Export ArchCharInput to JSON file.

    Args:
        archchar_input: ArchCharInput model to export
        file_path: Destination file path
    """
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    json_data = archchar_input.model_dump_json(indent=2)
    path.write_text(json_data)


def create_example_archchar() -> ArchCharInput:
    """Create an example ArchCharInput for testing/demonstration.

    Returns:
        Sample ArchCharInput with typical e-commerce characteristics
    """
    characteristics = [
        ArchCharacteristic(
            id="char_avail_001",
            name="Availability",
            description="The ability of a system to be accessible and operational when required.",
            selected=True,
            isTop=True,
            rating="critical",
            notes="99.99% uptime required per SLA. Must handle planned maintenance without downtime.",
            isCustom=False,
        ),
        ArchCharacteristic(
            id="char_scale_001",
            name="Scalability",
            description="The ability to handle increased workload by adding resources.",
            selected=True,
            isTop=True,
            rating="critical",
            notes="Must handle 10x traffic during Black Friday. Auto-scaling required.",
            isCustom=False,
        ),
        ArchCharacteristic(
            id="char_perf_001",
            name="Performance",
            description="The speed and efficiency of the system in executing tasks.",
            selected=True,
            isTop=True,
            rating="high",
            notes="Page load under 2s, checkout under 3s. P95 response time < 500ms.",
            isCustom=False,
        ),
        ArchCharacteristic(
            id="char_sec_001",
            name="Security",
            description="The ability to protect data and functionality from unauthorized access.",
            selected=True,
            isTop=True,
            rating="critical",
            notes="PCI-DSS compliance required for payment processing. GDPR for EU customers.",
            isCustom=False,
        ),
        ArchCharacteristic(
            id="char_rel_001",
            name="Reliability",
            description="The ability to function correctly and consistently over time.",
            selected=True,
            isTop=False,
            rating="high",
            notes="Order processing must be reliable. No lost transactions.",
            isCustom=False,
        ),
        ArchCharacteristic(
            id="char_maint_001",
            name="Maintainability",
            description="The ease with which a system can be modified, updated, or repaired.",
            selected=True,
            isTop=False,
            rating="high",
            notes="Need to support rapid feature development. Code quality is priority.",
            isCustom=False,
        ),
        ArchCharacteristic(
            id="char_test_001",
            name="Testability",
            description="The ease with which the system can be tested for defects.",
            selected=True,
            isTop=True,
            rating="high",
            notes="Automated testing required. 80% code coverage target.",
            isCustom=False,
        ),
        ArchCharacteristic(
            id="char_deploy_001",
            name="Deployability",
            description="The ease and frequency with which the system can be deployed.",
            selected=True,
            isTop=True,
            rating="high",
            notes="Multiple deployments per day. CI/CD pipeline essential.",
            isCustom=False,
        ),
        ArchCharacteristic(
            id="char_fault_001",
            name="Fault Tolerance",
            description="The ability to continue operating despite failures in components.",
            selected=True,
            isTop=True,
            rating="critical",
            notes="Single component failure should not bring down system. Circuit breakers needed.",
            isCustom=False,
        ),
        ArchCharacteristic(
            id="char_recov_001",
            name="Recoverability",
            description="The ability to restore functionality after a failure.",
            selected=True,
            isTop=False,
            rating="high",
            notes="RTO: 4 hours, RPO: 1 hour for critical data.",
            isCustom=False,
        ),
        ArchCharacteristic(
            id="char_interop_001",
            name="Interoperability",
            description="The ability to exchange data and interact with other systems.",
            selected=True,
            isTop=False,
            rating="medium",
            notes="Must integrate with payment gateway, shipping providers, and inventory systems.",
            isCustom=False,
        ),
        ArchCharacteristic(
            id="char_config_001",
            name="Configurability",
            description="The ease with which system behavior can be changed through configuration.",
            selected=True,
            isTop=False,
            rating="medium",
            notes="Feature flags for A/B testing. Environment-specific configurations.",
            isCustom=False,
        ),
        ArchCharacteristic(
            id="char_extend_001",
            name="Extensibility",
            description="The ease with which new functionality can be added.",
            selected=True,
            isTop=False,
            rating="medium",
            notes="Need to add new payment methods and shipping options regularly.",
            isCustom=False,
        ),
        ArchCharacteristic(
            id="char_usab_001",
            name="Usability",
            description="The ease of use and user experience of the system.",
            selected=True,
            isTop=False,
            rating="high",
            notes="Mobile-first design. Accessibility standards (WCAG 2.1 AA).",
            isCustom=False,
        ),
    ]

    # Top 7 are the ones with isTop=True
    top_characteristics = [c for c in characteristics if c.isTop]

    return ArchCharInput(
        projectName="E-Commerce Platform",
        architect="Architecture Team",
        date="2025-10-31",
        notes="High-scale e-commerce platform with international reach. Expecting significant growth in next 12 months.",
        characteristics=characteristics,
        topCharacteristics=top_characteristics,
    )


def validate_archchar_input(archchar_input: ArchCharInput) -> dict[str, Any]:
    """Validate ArchCharInput for common issues.

    Args:
        archchar_input: Input to validate

    Returns:
        Dictionary with validation results:
        - valid: bool
        - warnings: list[str]
        - errors: list[str]
    """
    errors = []
    warnings = []

    # Check top characteristics count
    if len(archchar_input.topCharacteristics) > 7:
        errors.append(
            f"Too many top characteristics: {len(archchar_input.topCharacteristics)}. "
            "Maximum is 7 according to Mark Richards' methodology."
        )

    if len(archchar_input.topCharacteristics) == 0:
        warnings.append("No top characteristics selected. Analysis may lack prioritization.")

    # Check that top characteristics are also selected
    selected_ids = {c.id for c in archchar_input.characteristics if c.selected}
    for top_char in archchar_input.topCharacteristics:
        if top_char.id not in selected_ids:
            errors.append(
                f"Top characteristic '{top_char.name}' is not marked as selected in characteristics list."
            )

    # Check for duplicate IDs
    all_ids = [c.id for c in archchar_input.characteristics]
    if len(all_ids) != len(set(all_ids)):
        errors.append("Duplicate characteristic IDs found.")

    # Check for duplicate names (warning only)
    all_names = [c.name for c in archchar_input.characteristics]
    if len(all_names) != len(set(all_names)):
        warnings.append("Duplicate characteristic names found.")

    # Check that isTop matches topCharacteristics
    is_top_from_list = {c.id for c in archchar_input.topCharacteristics}
    is_top_from_field = {c.id for c in archchar_input.characteristics if c.isTop}
    if is_top_from_list != is_top_from_field:
        warnings.append(
            "Mismatch between topCharacteristics list and isTop fields. "
            "This may indicate data inconsistency."
        )

    # Check for missing notes on critical characteristics
    critical_without_notes = [
        c.name
        for c in archchar_input.characteristics
        if c.selected and c.rating == "critical" and not c.notes.strip()
    ]
    if critical_without_notes:
        warnings.append(
            f"Critical characteristics without notes: {', '.join(critical_without_notes)}. "
            "Consider adding specific requirements."
        )

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
    }
