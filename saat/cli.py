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
@click.pass_context
def main(ctx: click.Context, model: str) -> None:
    """SAAT - Solution Architecture Agent Toolkit.

    AI-powered C4 architecture discovery and documentation using PydanticAI.
    """
    ctx.ensure_object(dict)
    ctx.obj["model"] = model

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
