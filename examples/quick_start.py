#!/usr/bin/env python3
"""Quick start example for SAAT using PydanticAI.

This script demonstrates how to use SAAT programmatically to:
1. Discover architecture from a repository
2. Generate a C4 model
3. Save the results
"""

import asyncio
import json
import sys
from pathlib import Path

from saat import SAATClient
from saat.models import BusinessContext, Stakeholder, ComplianceRequirement


async def main() -> None:
    """Main example function."""
    # Initialize SAAT client
    print("🚀 SAAT Quick Start Example\n")
    client = SAATClient(model="anthropic:claude-sonnet-4")

    # Analyze the SAAT repository itself as an example
    repo_path = Path(__file__).parent.parent
    print(f"📁 Analyzing repository: {repo_path}\n")

    # Option 1: Simple analysis (discover + generate in one call)
    print("Running full analysis...")
    discovery, model = await client.analyze(str(repo_path))

    print(f"\n✅ Analysis complete!")
    print(f"\n📋 Discovery Results:")
    print(f"   Technologies: {', '.join(discovery.technologies)}")
    print(f"   Patterns: {', '.join([p.pattern for p in discovery.patterns])}")
    print(f"   Confidence: {discovery.confidence:.2%}")

    print(f"\n🏗️  C4 Model:")
    print(f"   Systems: {len(model.systems)}")
    print(f"   Containers: {len(model.containers)}")
    print(f"   Components: {len(model.components)}")
    print(f"   Relationships: {len(model.relationships)}")

    # Save results
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    model_file = output_dir / "saat-architecture.json"
    model_file.write_text(model.model_dump_json(indent=2))
    print(f"\n💾 Model saved to: {model_file}")

    # Option 2: Step-by-step with business context
    print("\n" + "=" * 60)
    print("Example 2: Analysis with Business Context")
    print("=" * 60 + "\n")

    business = BusinessContext(
        purpose="AI-powered architecture discovery and documentation toolkit",
        stakeholders=[
            Stakeholder(
                name="Solution Architects",
                role="Primary Users",
                needs=["Automated architecture discovery", "C4 model generation"],
                interactions=["CLI", "Python API"],
            ),
            Stakeholder(
                name="Development Teams",
                role="End Users",
                needs=["Architecture documentation", "System understanding"],
                interactions=["Generated documentation"],
            ),
        ],
        capabilities=[
            "Repository analysis",
            "Technology detection",
            "Pattern recognition",
            "C4 model generation",
            "Multi-model support",
        ],
        compliance=[
            ComplianceRequirement(
                framework="MIT License",
                requirements=["Open source", "Attribution required"],
                applicable=True,
            )
        ],
    )

    # Generate model with business context
    model_with_context = await client.generate_model(discovery, business)

    print(f"✅ Enhanced model generated with business context")
    print(f"   Purpose: {model_with_context.metadata.project}")
    print(f"   Description: {model_with_context.metadata.description}")

    # Save enhanced model
    enhanced_file = output_dir / "saat-architecture-enhanced.json"
    enhanced_file.write_text(model_with_context.model_dump_json(indent=2))
    print(f"💾 Enhanced model saved to: {enhanced_file}")

    print("\n✨ Done! Check the output/ directory for results.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
