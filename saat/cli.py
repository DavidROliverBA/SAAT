"""SAAT CLI - Command-line interface for Solution Architecture Agent Toolkit."""

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Optional

import click

from saat import __version__
from saat.agents.discovery import DiscoveryAgent
from saat.agents.generator import GeneratorAgent
from saat.agents.requirements import RequirementsAgent
from saat.agents.validation import ValidationAgent
from saat.agents.documentation import DocumentationAgent
from saat.agents.security import SecurityAgent
from saat.agents.terraform import TerraformAgent
from saat.broker import ContextBroker
from saat.models import BusinessContext, C4Model, DiscoveryResult


@click.group()
@click.version_option(version=__version__, prog_name="saat")
@click.option(
    "--model",
    default="anthropic:claude-sonnet-4",
    envvar="SAAT_MODEL",
    help="Model to use (e.g., anthropic:claude-sonnet-4, openai:gpt-4)",
)
@click.option(
    "--auto-approve",
    "-y",
    is_flag=True,
    help="Skip approval prompts and auto-approve all checklist items",
)
@click.pass_context
def main(ctx: click.Context, model: str, auto_approve: bool) -> None:
    """SAAT - Solution Architecture Agent Toolkit.

    AI-powered C4 architecture discovery and documentation using PydanticAI.

    Supports both brownfield (existing code) and greenfield (from scratch) projects.
    """
    ctx.ensure_object(dict)
    ctx.obj["model"] = model
    ctx.obj["auto_approve"] = auto_approve

    # Check for API key
    if not os.getenv("ANTHROPIC_API_KEY") and "anthropic" in model:
        click.echo(
            "⚠️  Warning: ANTHROPIC_API_KEY not set. Set it with: export ANTHROPIC_API_KEY=your-key",
            err=True,
        )
    if not os.getenv("OPENAI_API_KEY") and "openai" in model:
        click.echo(
            "⚠️  Warning: OPENAI_API_KEY not set. Set it with: export OPENAI_API_KEY=your-key",
            err=True,
        )


@main.command()
@click.option(
    "--path",
    "-p",
    required=True,
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help="Repository path to analyze",
)
@click.option(
    "--output",
    "-o",
    default="discovery.json",
    type=click.Path(),
    help="Output file for discovery results",
)
@click.option(
    "--max-depth",
    default=3,
    type=int,
    help="Maximum directory depth to explore",
)
@click.pass_context
def discover(ctx: click.Context, path: str, output: str, max_depth: int) -> None:
    """Discover architecture from a codebase.

    Analyzes the repository structure, identifies technologies, detects patterns,
    and produces a discovery report.
    """
    click.echo(f"🔍 Discovering architecture in: {path}")

    async def run_discovery() -> None:
        agent = DiscoveryAgent(ctx.obj["model"])
        result = await agent.analyze_repository(path, max_depth)

        # Save results
        output_path = Path(output)
        output_path.write_text(result.model_dump_json(indent=2))

        click.echo(f"\n✅ Discovery complete!")
        click.echo(f"   Technologies: {', '.join(result.technologies)}")
        click.echo(f"   Patterns: {', '.join([p.pattern for p in result.patterns])}")
        click.echo(f"   Confidence: {result.confidence:.2%}")
        click.echo(f"   Output: {output}")

    try:
        asyncio.run(run_discovery())
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option(
    "--discovery",
    "-d",
    required=True,
    type=click.Path(exists=True),
    help="Discovery JSON file",
)
@click.option(
    "--output",
    "-o",
    default="c4-model.json",
    type=click.Path(),
    help="Output file for C4 model",
)
@click.option(
    "--business-context",
    "-b",
    type=click.Path(exists=True),
    help="Business context JSON file",
)
@click.pass_context
def generate(
    ctx: click.Context, discovery: str, output: str, business_context: Optional[str]
) -> None:
    """Generate C4 model from discovery results.

    Converts discovery results into a structured C4 architecture model with
    systems, containers, components, and relationships.
    """
    click.echo("🏗️  Generating C4 model...")

    async def run_generation() -> None:
        # Load discovery
        discovery_data = json.loads(Path(discovery).read_text())
        discovery_result = DiscoveryResult(**discovery_data)

        # Load business context if provided
        business = None
        if business_context:
            business_data = json.loads(Path(business_context).read_text())
            business = BusinessContext(**business_data)
            click.echo(f"   Using business context: {business.purpose}")

        # Generate model
        agent = GeneratorAgent(ctx.obj["model"])
        model = await agent.generate_model(discovery_result, business)

        # Save model
        output_path = Path(output)
        output_path.write_text(model.model_dump_json(indent=2))

        click.echo(f"\n✅ C4 model generated!")
        click.echo(f"   Systems: {len(model.systems)}")
        click.echo(f"   Containers: {len(model.containers)}")
        click.echo(f"   Components: {len(model.components)}")
        click.echo(f"   Relationships: {len(model.relationships)}")
        click.echo(f"   Output: {output}")

    try:
        asyncio.run(run_generation())
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option(
    "--path",
    "-p",
    required=True,
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help="Repository path to analyze",
)
@click.option(
    "--output",
    "-o",
    default="architecture.json",
    type=click.Path(),
    help="Output file for complete architecture",
)
@click.option(
    "--business-context",
    "-b",
    type=click.Path(exists=True),
    help="Business context JSON file",
)
@click.option(
    "--save-discovery",
    is_flag=True,
    help="Also save intermediate discovery results",
)
@click.pass_context
def analyze(
    ctx: click.Context,
    path: str,
    output: str,
    business_context: Optional[str],
    save_discovery: bool,
) -> None:
    """Full analysis: discover and generate in one command.

    Combines discovery and generation into a single workflow. This is the
    recommended command for most use cases.
    """
    click.echo(f"🚀 Analyzing repository: {path}")

    async def run_analysis() -> None:
        # Load business context if provided
        business = None
        if business_context:
            business_data = json.loads(Path(business_context).read_text())
            business = BusinessContext(**business_data)
            click.echo(f"   Business context: {business.purpose}")

        # Create broker and run
        broker = ContextBroker(ctx.obj["model"])
        discovery, model = await broker.discover_and_generate(path, business)

        # Save discovery if requested
        if save_discovery:
            discovery_path = Path(output).with_suffix(".discovery.json")
            discovery_path.write_text(discovery.model_dump_json(indent=2))
            click.echo(f"\n📋 Discovery saved: {discovery_path}")

        # Save model
        output_path = Path(output)
        output_path.write_text(model.model_dump_json(indent=2))

        click.echo(f"\n✅ Analysis complete!")
        click.echo(f"   Technologies: {', '.join(discovery.technologies)}")
        click.echo(f"   Systems: {len(model.systems)}")
        click.echo(f"   Containers: {len(model.containers)}")
        click.echo(f"   Output: {output}")

    try:
        asyncio.run(run_analysis())
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option(
    "--model-file",
    "-m",
    required=True,
    type=click.Path(exists=True),
    help="C4 model JSON file to validate",
)
@click.pass_context
def validate(ctx: click.Context, model_file: str) -> None:
    """Validate a C4 model for correctness and completeness.

    Checks the model for common issues, missing information, and best practice
    violations.
    """
    click.echo(f"🔍 Validating model: {model_file}")

    try:
        # Load and parse model
        model_data = json.loads(Path(model_file).read_text())
        model = C4Model(**model_data)

        click.echo("✅ Model structure is valid")
        click.echo(f"   Systems: {len(model.systems)}")
        click.echo(f"   Containers: {len(model.containers)}")
        click.echo(f"   Components: {len(model.components)}")
        click.echo(f"   Relationships: {len(model.relationships)}")

        # Basic validation checks
        issues = []

        # Check for orphaned containers
        system_ids = {s.id for s in model.systems}
        for container in model.containers:
            if container.system_id not in system_ids:
                issues.append(f"Container '{container.name}' references unknown system")

        # Check for orphaned components
        container_ids = {c.id for c in model.containers}
        for component in model.components:
            if component.container_id not in container_ids:
                issues.append(f"Component '{component.name}' references unknown container")

        # Check relationships
        all_ids = (
            system_ids
            | container_ids
            | {c.id for c in model.components}
            | {e.id for e in model.externals}
        )
        for rel in model.relationships:
            if rel.source not in all_ids:
                issues.append(f"Relationship source '{rel.source}' not found")
            if rel.target not in all_ids:
                issues.append(f"Relationship target '{rel.target}' not found")

        if issues:
            click.echo("\n⚠️  Issues found:")
            for issue in issues:
                click.echo(f"   - {issue}")
        else:
            click.echo("\n✅ No issues found. Model looks good!")

    except Exception as e:
        click.echo(f"❌ Validation failed: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option(
    "--files",
    "-f",
    multiple=True,
    required=True,
    type=click.Path(exists=True),
    help="Requirements document(s) to analyze (markdown, text)",
)
@click.option(
    "--project-name",
    "-n",
    help="Project name for the requirements",
)
@click.option(
    "--output",
    "-o",
    default="requirements.json",
    type=click.Path(),
    help="Output file for structured requirements",
)
@click.pass_context
def discover_requirements(
    ctx: click.Context, files: tuple[str, ...], project_name: Optional[str], output: str
) -> None:
    """Discover requirements from documents (greenfield projects).

    Analyzes markdown or text documents to extract functional requirements,
    non-functional requirements, user stories, technical constraints, and stakeholders.
    """
    click.echo(f"📋 Discovering requirements from {len(files)} file(s)...")

    async def run_discovery() -> None:
        agent = RequirementsAgent(ctx.obj["model"])
        result = await agent.discover_requirements(
            file_paths=list(files),
            project_name=project_name,
            auto_approve=ctx.obj["auto_approve"],
        )

        if result.get("cancelled"):
            click.echo("❌ Requirements discovery was cancelled")
            return

        requirements = result["requirements"]

        # Save requirements
        output_path = Path(output)
        output_path.write_text(requirements.model_dump_json(indent=2))

        summary = result["summary"]
        click.echo(f"\n✅ Requirements discovered!")
        click.echo(f"   Functional: {summary['functional_requirements']}")
        click.echo(f"   Non-Functional: {summary['non_functional_requirements']}")
        click.echo(f"   User Stories: {summary['user_stories']}")
        click.echo(f"   Constraints: {summary['constraints']}")
        click.echo(f"   Stakeholders: {summary['stakeholders']}")
        click.echo(f"   Output: {output}")

    try:
        asyncio.run(run_discovery())
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option(
    "--model-file",
    "-m",
    required=True,
    type=click.Path(exists=True),
    help="C4 model JSON file to validate",
)
@click.option(
    "--framework",
    "-f",
    type=click.Choice(["PCI-DSS", "HIPAA", "GDPR", "SOC2"]),
    help="Compliance framework to validate against",
)
@click.option(
    "--output",
    "-o",
    default="validation-report.json",
    type=click.Path(),
    help="Output file for validation report",
)
@click.pass_context
def validate_model(
    ctx: click.Context, model_file: str, framework: Optional[str], output: str
) -> None:
    """Validate C4 model against standards and compliance.

    Uses ValidationAgent to perform comprehensive validation including structural
    integrity, completeness, best practices, and optional compliance checking.
    """
    click.echo(f"🔍 Validating model: {model_file}")
    if framework:
        click.echo(f"   Framework: {framework}")

    async def run_validation() -> None:
        # Load model
        model_data = json.loads(Path(model_file).read_text())
        model = C4Model(**model_data)

        # Run validation
        agent = ValidationAgent(ctx.obj["model"])
        result = await agent.validate_model(
            model=model, framework=framework, auto_approve=ctx.obj["auto_approve"]
        )

        if result.get("cancelled"):
            click.echo("❌ Validation was cancelled")
            return

        validation = result["validation"]

        # Save report
        output_path = Path(output)
        output_path.write_text(validation.model_dump_json(indent=2))

        summary = result["summary"]
        click.echo(f"\n{'✅' if summary['valid'] else '❌'} Validation complete!")
        click.echo(f"   Score: {summary['score']}/100")
        click.echo(f"   Total Issues: {summary['total_issues']}")
        click.echo(f"   Errors: {summary['errors']}")
        click.echo(f"   Warnings: {summary['warnings']}")
        click.echo(f"   Info: {summary['info']}")
        click.echo(f"   Output: {output}")

        if not summary["valid"]:
            click.echo("\n⚠️  Model has validation errors. See report for details.")

    try:
        asyncio.run(run_validation())
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option(
    "--model-file",
    "-m",
    required=True,
    type=click.Path(exists=True),
    help="C4 model JSON file to document",
)
@click.option(
    "--output-dir",
    "-o",
    default="docs/",
    type=click.Path(),
    help="Output directory for documentation",
)
@click.option(
    "--format",
    "-f",
    "formats",
    multiple=True,
    type=click.Choice(["markdown", "plantuml", "mermaid", "adr"]),
    default=["markdown"],
    help="Documentation format(s) to generate",
)
@click.pass_context
def generate_docs(
    ctx: click.Context, model_file: str, output_dir: str, formats: tuple[str, ...]
) -> None:
    """Generate documentation from C4 model.

    Creates comprehensive documentation including markdown overview, diagrams
    (PlantUML/Mermaid), and Architecture Decision Records (ADRs).
    """
    click.echo(f"📚 Generating documentation from: {model_file}")
    click.echo(f"   Formats: {', '.join(formats)}")

    async def run_generation() -> None:
        # Load model
        model_data = json.loads(Path(model_file).read_text())
        model = C4Model(**model_data)

        # Generate documentation
        agent = DocumentationAgent(ctx.obj["model"])
        result = await agent.generate_documentation(
            model=model,
            output_dir=output_dir,
            formats=list(formats),
            auto_approve=ctx.obj["auto_approve"],
        )

        if result.get("cancelled"):
            click.echo("❌ Documentation generation was cancelled")
            return

        summary = result["summary"]
        click.echo(f"\n✅ Documentation generated!")
        click.echo(f"   Files: {summary['total_files']}")
        click.echo(f"   Output: {output_dir}")
        click.echo("\n   Generated files:")
        for file in result["generated_files"]:
            click.echo(f"   - {file}")

    try:
        asyncio.run(run_generation())
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option(
    "--model-file",
    "-m",
    required=True,
    type=click.Path(exists=True),
    help="C4 model JSON file to analyze",
)
@click.option(
    "--threat-model",
    is_flag=True,
    help="Generate threat model in addition to security analysis",
)
@click.option(
    "--output",
    "-o",
    default="security-report.json",
    type=click.Path(),
    help="Output file for security report",
)
@click.pass_context
def security_scan(
    ctx: click.Context, model_file: str, threat_model: bool, output: str
) -> None:
    """Analyze security posture of architecture.

    Identifies security issues including unencrypted communications, missing
    authentication, sensitive data exposure, and compliance violations.
    """
    click.echo(f"🔒 Analyzing security: {model_file}")
    if threat_model:
        click.echo("   Including threat modeling")

    async def run_security_analysis() -> None:
        # Load model
        model_data = json.loads(Path(model_file).read_text())
        model = C4Model(**model_data)

        # Run security analysis
        agent = SecurityAgent(ctx.obj["model"])
        result = await agent.analyze_security(
            model=model,
            threat_model=threat_model,
            output_file=output,
            auto_approve=ctx.obj["auto_approve"],
        )

        if result.get("cancelled"):
            click.echo("❌ Security analysis was cancelled")
            return

        summary = result["summary"]
        click.echo(f"\n✅ Security analysis complete!")
        click.echo(f"   Overall Score: {summary['overall_score']:.1f}/100")
        click.echo(f"   Total Issues: {summary['total_issues']}")
        click.echo(f"   Critical: {summary['critical']}")
        click.echo(f"   High: {summary['high']}")
        click.echo(f"   Medium: {summary['medium']}")
        click.echo(f"   Low: {summary['low']}")
        click.echo(f"   Output: {output}")

        if summary["critical"] > 0 or summary["high"] > 0:
            click.echo("\n⚠️  Critical or high severity issues found. Review the report!")

    try:
        asyncio.run(run_security_analysis())
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option(
    "--model-file",
    "-m",
    required=True,
    type=click.Path(exists=True),
    help="C4 model JSON file to generate from",
)
@click.option(
    "--provider",
    "-p",
    default="aws",
    type=click.Choice(["aws", "azure", "gcp"]),
    help="Cloud provider for infrastructure",
)
@click.option(
    "--region",
    "-r",
    default="us-east-1",
    help="Cloud region for deployment",
)
@click.option(
    "--output-dir",
    "-o",
    default="infrastructure/",
    type=click.Path(),
    help="Output directory for Terraform files",
)
@click.pass_context
def generate_terraform(
    ctx: click.Context, model_file: str, provider: str, region: str, output_dir: str
) -> None:
    """Generate Terraform infrastructure-as-code.

    Creates production-ready Terraform configurations based on the C4 model,
    with criticality-based resource sizing, networking, monitoring, and backups.
    """
    click.echo(f"🏗️  Generating Terraform for {provider.upper()}...")
    click.echo(f"   Region: {region}")

    async def run_terraform_generation() -> None:
        # Load model
        model_data = json.loads(Path(model_file).read_text())
        model = C4Model(**model_data)

        # Generate Terraform
        agent = TerraformAgent(ctx.obj["model"])
        result = await agent.generate_terraform(
            model=model,
            provider=provider,
            region=region,
            output_dir=output_dir,
            auto_approve=ctx.obj["auto_approve"],
        )

        if result.get("cancelled"):
            click.echo("❌ Terraform generation was cancelled")
            return

        summary = result["summary"]
        click.echo(f"\n✅ Terraform generated!")
        click.echo(f"   Provider: {summary['provider'].upper()}")
        click.echo(f"   Resources: {summary['total_resources']}")
        click.echo(f"   Files: {summary['total_files']}")
        click.echo(f"   Output: {output_dir}")
        click.echo("\n   Generated files:")
        for file in result["generated_files"]:
            click.echo(f"   - {file}")
        click.echo("\n💡 Next steps:")
        click.echo(f"   cd {output_dir}")
        click.echo("   terraform init")
        click.echo("   terraform plan")

    try:
        asyncio.run(run_terraform_generation())
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option(
    "--model-file",
    "-m",
    required=True,
    type=click.Path(exists=True),
    help="SAAT C4 model JSON file to export",
)
@click.option(
    "--output",
    "-o",
    default="structurizr.json",
    type=click.Path(),
    help="Output Structurizr JSON file",
)
@click.pass_context
def export_structurizr(ctx: click.Context, model_file: str, output: str) -> None:
    """Export SAAT model to Structurizr JSON format.

    Converts SAAT's internal C4 model to the industry-standard Structurizr JSON
    format for compatibility with tools like bac4-standalone editor, Structurizr Lite,
    and other C4 visualization tools.
    """
    click.echo(f"📤 Exporting to Structurizr format...")
    click.echo(f"   Input: {model_file}")

    try:
        from saat.converters import export_to_structurizr_file

        # Load SAAT model
        model_data = json.loads(Path(model_file).read_text())
        c4_model = C4Model(**model_data)

        # Export to Structurizr
        export_to_structurizr_file(c4_model, output)

        click.echo(f"\n✅ Export complete!")
        click.echo(f"   Output: {output}")
        click.echo(f"\n💡 You can now:")
        click.echo(f"   - Import into bac4-standalone editor")
        click.echo(f"   - Use with Structurizr Lite")
        click.echo(f"   - View with other C4 tools")

    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option(
    "--structurizr-file",
    "-s",
    required=True,
    type=click.Path(exists=True),
    help="Structurizr JSON file to import",
)
@click.option(
    "--output",
    "-o",
    default="architecture.json",
    type=click.Path(),
    help="Output SAAT model JSON file",
)
@click.pass_context
def import_structurizr(ctx: click.Context, structurizr_file: str, output: str) -> None:
    """Import Structurizr JSON into SAAT model.

    Converts Structurizr JSON (from bac4-standalone or other tools) into SAAT's
    internal C4 model format for validation, documentation, security analysis,
    and infrastructure generation.
    """
    click.echo(f"📥 Importing from Structurizr format...")
    click.echo(f"   Input: {structurizr_file}")

    try:
        from saat.converters import import_from_structurizr_file

        # Import from Structurizr
        c4_model = import_from_structurizr_file(structurizr_file)

        # Save SAAT model
        output_path = Path(output)
        output_path.write_text(c4_model.model_dump_json(indent=2))

        click.echo(f"\n✅ Import complete!")
        click.echo(f"   Systems: {len(c4_model.systems)}")
        click.echo(f"   External Systems: {len(c4_model.externals)}")
        click.echo(f"   Containers: {len(c4_model.containers)}")
        click.echo(f"   Components: {len(c4_model.components)}")
        click.echo(f"   Relationships: {len(c4_model.relationships)}")
        click.echo(f"   Output: {output}")
        click.echo(f"\n💡 You can now:")
        click.echo(f"   saat validate-model -m {output}")
        click.echo(f"   saat security-scan -m {output}")
        click.echo(f"   saat generate-terraform -m {output} -p aws")

    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option(
    "--model-file",
    "-m",
    required=True,
    type=click.Path(exists=True),
    help="C4 model JSON file to analyze",
)
@click.option(
    "--characteristics",
    "-c",
    required=True,
    type=click.Path(exists=True),
    help="ArchCharCapture JSON file with architecture characteristics",
)
@click.option(
    "--output",
    "-o",
    default="archchar-analysis",
    type=click.Path(),
    help="Output file path (without extension)",
)
@click.option(
    "--format",
    "-f",
    type=click.Choice(["markdown", "json", "both"], case_sensitive=False),
    default="both",
    help="Output format",
)
@click.pass_context
def analyze_characteristics(
    ctx: click.Context,
    model_file: str,
    characteristics: str,
    output: str,
    format: str,
) -> None:
    """Analyze C4 model against architecture characteristics.

    Evaluates your C4 architecture model against specified architecture
    characteristics using Mark Richards' methodology. Identifies gaps,
    provides recommendations, and generates compliance scores.

    Requires an ArchCharCapture JSON file (from https://github.com/DavidROliverBA/ArchCharCapture)
    with your selected characteristics and their importance ratings.
    """
    click.echo("🔍 Analyzing architecture characteristics...")
    click.echo(f"   C4 Model: {model_file}")
    click.echo(f"   Characteristics: {characteristics}")

    async def run_analysis() -> None:
        from saat.converters_archchar import import_archchar_json
        from saat.agents.archchar import (
            ArchCharAnalysisAgent,
            generate_markdown_report,
            export_json_report,
            save_report,
        )

        # Load C4 model
        model_data = json.loads(Path(model_file).read_text())
        c4_model = C4Model(**model_data)

        # Load architecture characteristics
        archchar_input = import_archchar_json(characteristics)

        click.echo(f"\n📊 Analyzing {len([c for c in archchar_input.characteristics if c.selected])} selected characteristics...")
        click.echo(f"   Top 7: {', '.join([c.name for c in archchar_input.topCharacteristics])}")

        # Run analysis
        agent = ArchCharAnalysisAgent(ctx.obj["model"])
        result = await agent.analyze(
            c4_model,
            archchar_input,
            auto_approve=ctx.obj["auto_approve"],
        )

        # Save reports based on format
        output_path = Path(output)

        if format in ["markdown", "both"]:
            markdown_path = output_path.with_suffix(".md")
            save_report(result, markdown_path, format="markdown")
            click.echo(f"\n📄 Markdown report: {markdown_path}")

        if format in ["json", "both"]:
            json_path = output_path.with_suffix(".json")
            save_report(result, json_path, format="json")
            click.echo(f"📊 JSON report: {json_path}")

        # Display summary
        click.echo(f"\n✅ Analysis complete!")
        click.echo(f"   Overall Score: {result.overall_score}/100")
        click.echo(f"   Characteristics Analyzed: {result.characteristics_analyzed}")
        click.echo(f"   Critical Gaps: {len(result.critical_gaps)}")
        click.echo(f"   High Priority Gaps: {len(result.high_priority_gaps)}")
        click.echo(f"   Top Recommendations: {len(result.top_recommendations)}")

        if result.critical_gaps:
            click.echo(f"\n⚠️  Critical gaps requiring immediate attention:")
            for gap in result.critical_gaps[:3]:
                click.echo(f"   - {gap.area}: {gap.issue}")
            if len(result.critical_gaps) > 3:
                click.echo(f"   ... and {len(result.critical_gaps) - 3} more")

        if result.top_recommendations:
            click.echo(f"\n💡 Top recommendations:")
            for rec in result.top_recommendations[:3]:
                click.echo(f"   - {rec.title} ({rec.priority} priority)")
            if len(result.top_recommendations) > 3:
                click.echo(f"   ... and {len(result.top_recommendations) - 3} more")

        click.echo(f"\n📖 See full report for detailed analysis and implementation steps.")

    try:
        asyncio.run(run_analysis())
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        import traceback
        if ctx.obj.get("verbose"):
            traceback.print_exc()
        sys.exit(1)


@main.command()
def info() -> None:
    """Display SAAT version and configuration information."""
    click.echo(f"SAAT v{__version__}")
    click.echo(f"Python: {sys.version.split()[0]}")
    click.echo("\nAvailable models:")
    click.echo("  - anthropic:claude-sonnet-4 (default)")
    click.echo("  - anthropic:claude-opus-4")
    click.echo("  - openai:gpt-4")
    click.echo("  - openai:gpt-4-turbo")
    click.echo("\nEnvironment:")
    click.echo(f"  ANTHROPIC_API_KEY: {'✅ set' if os.getenv('ANTHROPIC_API_KEY') else '❌ not set'}")
    click.echo(f"  OPENAI_API_KEY: {'✅ set' if os.getenv('OPENAI_API_KEY') else '❌ not set'}")
    click.echo(f"  SAAT_MODEL: {os.getenv('SAAT_MODEL', 'not set (using default)')}")


if __name__ == "__main__":
    main()
