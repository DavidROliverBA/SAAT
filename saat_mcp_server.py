#!/usr/bin/env python3
"""MCP Server for SAAT - Integrates with Claude Code.

This server exposes SAAT functionality as MCP tools that can be used
by Claude Code for architecture analysis, requirements discovery,
validation, security scanning, documentation, and infrastructure generation.

All tools run with auto_approve=True for seamless integration.
"""

import asyncio
import json
from pathlib import Path
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from saat.agents.discovery import DiscoveryAgent
from saat.agents.documentation import DocumentationAgent
from saat.agents.generator import GeneratorAgent
from saat.agents.requirements import RequirementsAgent
from saat.agents.security import SecurityAgent
from saat.agents.terraform import TerraformAgent
from saat.agents.validation import ValidationAgent
from saat.broker import ContextBroker
from saat.models import C4Model, DiscoveryResult

# Initialize MCP server
server = Server("saat-architecture")

# Model to use (can be overridden via environment)
DEFAULT_MODEL = "anthropic:claude-sonnet-4"


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List all available SAAT tools."""
    return [
        Tool(
            name="discover_architecture",
            description="Analyze repository to discover architecture (brownfield)",
            inputSchema={
                "type": "object",
                "properties": {
                    "repo_path": {
                        "type": "string",
                        "description": "Path to repository to analyze",
                    },
                    "max_depth": {
                        "type": "integer",
                        "default": 3,
                        "description": "Maximum directory depth to explore",
                    },
                },
                "required": ["repo_path"],
            },
        ),
        Tool(
            name="discover_requirements",
            description="Extract requirements from documents for greenfield projects",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_paths": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Paths to requirements documents (markdown, text)",
                    },
                    "project_name": {
                        "type": "string",
                        "description": "Project name for the requirements",
                    },
                },
                "required": ["file_paths"],
            },
        ),
        Tool(
            name="generate_c4_model",
            description="Generate C4 architecture model from discovery or requirements",
            inputSchema={
                "type": "object",
                "properties": {
                    "discovery_file": {
                        "type": "string",
                        "description": "Path to discovery.json file (brownfield)",
                    },
                    "requirements_file": {
                        "type": "string",
                        "description": "Path to requirements.json file (greenfield)",
                    },
                },
            },
        ),
        Tool(
            name="validate_model",
            description="Validate C4 model against standards and compliance frameworks",
            inputSchema={
                "type": "object",
                "properties": {
                    "model_file": {
                        "type": "string",
                        "description": "Path to C4 model JSON file",
                    },
                    "framework": {
                        "type": "string",
                        "enum": ["PCI-DSS", "HIPAA", "GDPR", "SOC2"],
                        "description": "Compliance framework to validate against",
                    },
                },
                "required": ["model_file"],
            },
        ),
        Tool(
            name="analyze_security",
            description="Analyze security posture and identify vulnerabilities",
            inputSchema={
                "type": "object",
                "properties": {
                    "model_file": {
                        "type": "string",
                        "description": "Path to C4 model JSON file",
                    },
                    "threat_model": {
                        "type": "boolean",
                        "default": False,
                        "description": "Generate threat model",
                    },
                },
                "required": ["model_file"],
            },
        ),
        Tool(
            name="generate_documentation",
            description="Generate comprehensive architecture documentation",
            inputSchema={
                "type": "object",
                "properties": {
                    "model_file": {
                        "type": "string",
                        "description": "Path to C4 model JSON file",
                    },
                    "output_dir": {
                        "type": "string",
                        "default": "docs/",
                        "description": "Output directory for documentation",
                    },
                    "formats": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": ["markdown", "plantuml", "mermaid", "adr"],
                        },
                        "default": ["markdown"],
                        "description": "Documentation formats to generate",
                    },
                },
                "required": ["model_file"],
            },
        ),
        Tool(
            name="generate_terraform",
            description="Generate Terraform infrastructure-as-code from C4 model",
            inputSchema={
                "type": "object",
                "properties": {
                    "model_file": {
                        "type": "string",
                        "description": "Path to C4 model JSON file",
                    },
                    "provider": {
                        "type": "string",
                        "enum": ["aws", "azure", "gcp"],
                        "default": "aws",
                        "description": "Cloud provider",
                    },
                    "region": {
                        "type": "string",
                        "default": "us-east-1",
                        "description": "Cloud region",
                    },
                    "output_dir": {
                        "type": "string",
                        "default": "infrastructure/",
                        "description": "Output directory for Terraform files",
                    },
                },
                "required": ["model_file"],
            },
        ),
        Tool(
            name="analyze_architecture_characteristics",
            description="Analyze C4 model against architecture characteristics using Mark Richards' methodology",
            inputSchema={
                "type": "object",
                "properties": {
                    "model_file": {
                        "type": "string",
                        "description": "Path to C4 model JSON file",
                    },
                    "characteristics_file": {
                        "type": "string",
                        "description": "Path to ArchCharCapture JSON file with characteristics",
                    },
                    "output_file": {
                        "type": "string",
                        "default": "archchar-analysis",
                        "description": "Output file path (without extension)",
                    },
                    "format": {
                        "type": "string",
                        "enum": ["markdown", "json", "both"],
                        "default": "both",
                        "description": "Output format",
                    },
                },
                "required": ["model_file", "characteristics_file"],
            },
        ),
        Tool(
            name="full_analysis",
            description="Complete end-to-end analysis: discover, generate, validate, and document",
            inputSchema={
                "type": "object",
                "properties": {
                    "repo_path": {
                        "type": "string",
                        "description": "Path to repository (brownfield)",
                    },
                    "output_dir": {
                        "type": "string",
                        "default": "saat-output/",
                        "description": "Output directory for all generated files",
                    },
                },
                "required": ["repo_path"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Handle tool calls from Claude Code."""
    # All tools use auto_approve=True for seamless MCP integration

    if name == "discover_architecture":
        repo_path = arguments["repo_path"]
        max_depth = arguments.get("max_depth", 3)

        agent = DiscoveryAgent(DEFAULT_MODEL)
        discovery = await agent.analyze_repository(repo_path, max_depth)

        # Save discovery
        output_file = Path(repo_path) / "discovery.json"
        output_file.write_text(discovery.model_dump_json(indent=2))

        return [
            TextContent(
                type="text",
                text=f"""Architecture discovered from {repo_path}:

**Technologies**: {', '.join(discovery.technologies)}
**Patterns**: {', '.join([p.pattern for p in discovery.patterns])}
**Confidence**: {discovery.confidence:.2%}
**Services**: {len(discovery.services)}

Discovery saved to: {output_file}
""",
            )
        ]

    elif name == "discover_requirements":
        file_paths = arguments["file_paths"]
        project_name = arguments.get("project_name")

        agent = RequirementsAgent(DEFAULT_MODEL)
        result = await agent.discover_requirements(
            file_paths=file_paths, project_name=project_name, auto_approve=True
        )

        if result.get("cancelled"):
            return [TextContent(type="text", text="❌ Requirements discovery was cancelled")]

        requirements = result["requirements"]
        summary = result["summary"]

        # Save requirements
        output_file = Path("requirements.json")
        output_file.write_text(requirements.model_dump_json(indent=2))

        return [
            TextContent(
                type="text",
                text=f"""Requirements discovered from {len(file_paths)} document(s):

**Project**: {requirements.project_name}
**Functional Requirements**: {summary['functional_requirements']}
**Non-Functional Requirements**: {summary['non_functional_requirements']}
**User Stories**: {summary['user_stories']}
**Technical Constraints**: {summary['constraints']}
**Stakeholders**: {summary['stakeholders']}

Requirements saved to: {output_file}
""",
            )
        ]

    elif name == "generate_c4_model":
        discovery_file = arguments.get("discovery_file")
        requirements_file = arguments.get("requirements_file")

        if discovery_file:
            # Brownfield: Generate from discovery
            discovery_data = json.loads(Path(discovery_file).read_text())
            discovery = DiscoveryResult(**discovery_data)

            agent = GeneratorAgent(DEFAULT_MODEL)
            model = await agent.generate_model(discovery, None)

            output_file = Path("architecture.json")
            output_file.write_text(model.model_dump_json(indent=2))

            return [
                TextContent(
                    type="text",
                    text=f"""C4 model generated from discovery:

**Systems**: {len(model.systems)}
**Containers**: {len(model.containers)}
**Components**: {len(model.components)}
**Relationships**: {len(model.relationships)}

Model saved to: {output_file}
""",
                )
            ]

        elif requirements_file:
            # Greenfield: Generate from requirements
            # TODO: Implement generation from requirements
            return [
                TextContent(
                    type="text",
                    text="Greenfield model generation from requirements is not yet implemented. Use discovery_file for brownfield projects.",
                )
            ]

        else:
            return [
                TextContent(
                    type="text", text="Either discovery_file or requirements_file must be provided"
                )
            ]

    elif name == "validate_model":
        model_file = arguments["model_file"]
        framework = arguments.get("framework")

        # Load model
        model_data = json.loads(Path(model_file).read_text())
        model = C4Model(**model_data)

        # Validate
        agent = ValidationAgent(DEFAULT_MODEL)
        result = await agent.validate_model(model=model, framework=framework, auto_approve=True)

        if result.get("cancelled"):
            return [TextContent(type="text", text="❌ Validation was cancelled")]

        validation = result["validation"]
        summary = result["summary"]

        # Save report
        output_file = Path("validation-report.json")
        output_file.write_text(validation.model_dump_json(indent=2))

        status = "✅" if summary["valid"] else "❌"
        return [
            TextContent(
                type="text",
                text=f"""{status} Validation complete:

**Score**: {summary['score']}/100
**Total Issues**: {summary['total_issues']}
**Errors**: {summary['errors']}
**Warnings**: {summary['warnings']}
**Info**: {summary['info']}

Report saved to: {output_file}
""",
            )
        ]

    elif name == "analyze_security":
        model_file = arguments["model_file"]
        threat_model = arguments.get("threat_model", False)

        # Load model
        model_data = json.loads(Path(model_file).read_text())
        model = C4Model(**model_data)

        # Analyze security
        agent = SecurityAgent(DEFAULT_MODEL)
        result = await agent.analyze_security(
            model=model, threat_model=threat_model, output_file="security-report.json", auto_approve=True
        )

        if result.get("cancelled"):
            return [TextContent(type="text", text="❌ Security analysis was cancelled")]

        summary = result["summary"]

        return [
            TextContent(
                type="text",
                text=f"""🔒 Security analysis complete:

**Overall Score**: {summary['overall_score']:.1f}/100
**Total Issues**: {summary['total_issues']}
**Critical**: {summary['critical']}
**High**: {summary['high']}
**Medium**: {summary['medium']}
**Low**: {summary['low']}

Report saved to: security-report.json
""",
            )
        ]

    elif name == "generate_documentation":
        model_file = arguments["model_file"]
        output_dir = arguments.get("output_dir", "docs/")
        formats = arguments.get("formats", ["markdown"])

        # Load model
        model_data = json.loads(Path(model_file).read_text())
        model = C4Model(**model_data)

        # Generate documentation
        agent = DocumentationAgent(DEFAULT_MODEL)
        result = await agent.generate_documentation(
            model=model, output_dir=output_dir, formats=formats, auto_approve=True
        )

        if result.get("cancelled"):
            return [TextContent(type="text", text="❌ Documentation generation was cancelled")]

        summary = result["summary"]
        files = "\n".join(f"  - {f}" for f in result["generated_files"])

        return [
            TextContent(
                type="text",
                text=f"""📚 Documentation generated:

**Files**: {summary['total_files']}
**Formats**: {', '.join(summary['formats'])}
**Output Directory**: {output_dir}

Generated files:
{files}
""",
            )
        ]

    elif name == "generate_terraform":
        model_file = arguments["model_file"]
        provider = arguments.get("provider", "aws")
        region = arguments.get("region", "us-east-1")
        output_dir = arguments.get("output_dir", "infrastructure/")

        # Load model
        model_data = json.loads(Path(model_file).read_text())
        model = C4Model(**model_data)

        # Generate Terraform
        agent = TerraformAgent(DEFAULT_MODEL)
        result = await agent.generate_terraform(
            model=model, provider=provider, region=region, output_dir=output_dir, auto_approve=True
        )

        if result.get("cancelled"):
            return [TextContent(type="text", text="❌ Terraform generation was cancelled")]

        summary = result["summary"]
        files = "\n".join(f"  - {f}" for f in result["generated_files"])

        return [
            TextContent(
                type="text",
                text=f"""🏗️  Terraform generated for {provider.upper()}:

**Resources**: {summary['total_resources']}
**Files**: {summary['total_files']}
**Output Directory**: {output_dir}

Generated files:
{files}

Next steps:
  cd {output_dir}
  terraform init
  terraform plan
""",
            )
        ]

    elif name == "full_analysis":
        repo_path = arguments["repo_path"]
        output_dir = arguments.get("output_dir", "saat-output/")

        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Step 1: Discover architecture
        broker = ContextBroker(DEFAULT_MODEL)
        discovery, model = await broker.discover_and_generate(repo_path, None)

        # Save discovery
        discovery_file = output_path / "discovery.json"
        discovery_file.write_text(discovery.model_dump_json(indent=2))

        # Save model
        model_file = output_path / "architecture.json"
        model_file.write_text(model.model_dump_json(indent=2))

        # Step 2: Validate
        val_agent = ValidationAgent(DEFAULT_MODEL)
        val_result = await val_agent.validate_model(model=model, auto_approve=True)

        if not val_result.get("cancelled"):
            val_output = output_path / "validation-report.json"
            val_output.write_text(val_result["validation"].model_dump_json(indent=2))

        # Step 3: Security analysis
        sec_agent = SecurityAgent(DEFAULT_MODEL)
        sec_result = await sec_agent.analyze_security(
            model=model, output_file=str(output_path / "security-report.json"), auto_approve=True
        )

        # Step 4: Generate documentation
        doc_agent = DocumentationAgent(DEFAULT_MODEL)
        doc_result = await doc_agent.generate_documentation(
            model=model, output_dir=str(output_path / "docs"), auto_approve=True
        )

        # Summary
        files_generated = [
            str(discovery_file),
            str(model_file),
            str(output_path / "validation-report.json"),
            str(output_path / "security-report.json"),
        ]

        if not doc_result.get("cancelled"):
            files_generated.extend(doc_result["generated_files"])

        files_list = "\n".join(f"  - {f}" for f in files_generated)

        return [
            TextContent(
                type="text",
                text=f"""✅ Complete analysis finished for {repo_path}:

**Discovery**:
  - Technologies: {', '.join(discovery.technologies)}
  - Confidence: {discovery.confidence:.2%}

**Architecture**:
  - Systems: {len(model.systems)}
  - Containers: {len(model.containers)}
  - Components: {len(model.components)}

**Validation**:
  - Score: {val_result['summary']['score']}/100 (if not cancelled)

**Security**:
  - Score: {sec_result['summary']['overall_score']:.1f}/100 (if not cancelled)

All outputs saved to: {output_dir}

Generated files:
{files_list}
""",
            )
        ]

    elif name == "analyze_architecture_characteristics":
        model_file = arguments["model_file"]
        characteristics_file = arguments["characteristics_file"]
        output_file = arguments.get("output_file", "archchar-analysis")
        format_type = arguments.get("format", "both")

        # Import required modules
        from saat.converters_archchar import import_archchar_json
        from saat.agents.archchar import (
            ArchCharAnalysisAgent,
            save_report,
        )

        # Load C4 model
        model_data = json.loads(Path(model_file).read_text())
        model = C4Model(**model_data)

        # Load architecture characteristics
        archchar_input = import_archchar_json(characteristics_file)

        # Run analysis
        agent = ArchCharAnalysisAgent(DEFAULT_MODEL)
        result = await agent.analyze(model, archchar_input, auto_approve=True)

        # Save reports based on format
        output_path = Path(output_file)
        generated_files = []

        if format_type in ["markdown", "both"]:
            markdown_path = output_path.with_suffix(".md")
            save_report(result, markdown_path, format="markdown")
            generated_files.append(str(markdown_path))

        if format_type in ["json", "both"]:
            json_path = output_path.with_suffix(".json")
            save_report(result, json_path, format="json")
            generated_files.append(str(json_path))

        # Build summary of critical gaps
        critical_summary = ""
        if result.critical_gaps:
            critical_items = []
            for gap in result.critical_gaps[:3]:
                critical_items.append(f"  - {gap.area}: {gap.issue}")
            critical_summary = "\n".join(critical_items)
            if len(result.critical_gaps) > 3:
                critical_summary += f"\n  ... and {len(result.critical_gaps) - 3} more"

        # Build summary of top recommendations
        rec_summary = ""
        if result.top_recommendations:
            rec_items = []
            for rec in result.top_recommendations[:3]:
                rec_items.append(f"  - {rec.title} ({rec.priority} priority)")
            rec_summary = "\n".join(rec_items)
            if len(result.top_recommendations) > 3:
                rec_summary += f"\n  ... and {len(result.top_recommendations) - 3} more"

        files_list = "\n".join(f"  - {f}" for f in generated_files)

        # Build response
        response_text = f"""✅ Architecture characteristics analysis complete:

**Overall Score**: {result.overall_score}/100
**Characteristics Analyzed**: {result.characteristics_analyzed}
**Critical Gaps**: {len(result.critical_gaps)}
**High Priority Gaps**: {len(result.high_priority_gaps)}
**Top Recommendations**: {len(result.top_recommendations)}

**Executive Summary**:
{result.executive_summary}
"""

        if critical_summary:
            response_text += f"\n\n⚠️ **Critical Gaps**:\n{critical_summary}"

        if rec_summary:
            response_text += f"\n\n💡 **Top Recommendations**:\n{rec_summary}"

        response_text += f"\n\n**Generated Reports**:\n{files_list}"
        response_text += "\n\n📖 See full reports for detailed analysis and implementation steps."

        return [TextContent(type="text", text=response_text)]

    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def main() -> None:
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, write_stream, server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
