#!/usr/bin/env python3
"""Example: Greenfield project from requirements to infrastructure.

This example demonstrates the complete SAAT workflow for greenfield projects:
1. Discover requirements from documents
2. Generate C4 architecture model from requirements
3. Validate the architecture
4. Generate documentation
5. Analyze security
6. Generate Terraform infrastructure

All steps use auto_approve=True for demonstration purposes.
"""

import asyncio
import sys
from pathlib import Path

from saat.agents.documentation import DocumentationAgent
from saat.agents.generator import GeneratorAgent
from saat.agents.requirements import RequirementsAgent
from saat.agents.security import SecurityAgent
from saat.agents.terraform import TerraformAgent
from saat.agents.validation import ValidationAgent


async def main() -> None:
    """Complete greenfield workflow."""
    print("🏗️  SAAT Greenfield Project Example\n")
    print("=" * 60)

    # Check if requirements file exists
    requirements_doc = Path("examples/requirements.md")
    if not requirements_doc.exists():
        print(f"❌ Requirements document not found: {requirements_doc}")
        print("   Please create examples/requirements.md first.")
        sys.exit(1)

    # Step 1: Discover requirements
    print("\n📋 Step 1: Discovering requirements from PRD...")
    print("-" * 60)

    req_agent = RequirementsAgent()
    req_result = await req_agent.discover_requirements(
        file_paths=[str(requirements_doc)],
        project_name="Payment Processing Platform",
        auto_approve=True,  # Auto-approve for demo
    )

    if req_result.get("cancelled"):
        print("❌ Requirements discovery was cancelled")
        return

    requirements = req_result["requirements"]
    print(f"\n✅ Requirements discovered:")
    print(f"   Functional: {req_result['summary']['functional_requirements']}")
    print(f"   Non-Functional: {req_result['summary']['non_functional_requirements']}")
    print(f"   User Stories: {req_result['summary']['user_stories']}")
    print(f"   Constraints: {req_result['summary']['constraints']}")
    print(f"   Stakeholders: {req_result['summary']['stakeholders']}")

    # Save requirements
    requirements_file = Path("requirements.json")
    requirements_file.write_text(requirements.model_dump_json(indent=2))
    print(f"\n   Saved to: {requirements_file}")

    # Step 2: Generate architecture from requirements
    print("\n\n🏛️  Step 2: Generating C4 architecture model...")
    print("-" * 60)
    print("⚠️  Note: This step requires implementation of requirements-to-architecture generation")
    print("   For now, you would manually create the architecture or use discovery for brownfield.")

    # TODO: Implement GeneratorAgent.generate_from_requirements()
    # For this example, we'll skip to validation assuming a model exists

    # Create a minimal model for demonstration
    # In a real scenario, you would have this generated from requirements
    print("\n   [Skipping model generation for demo - would be implemented]")

    # Step 3: Validate architecture
    print("\n\n✅ Step 3: Validating architecture...")
    print("-" * 60)
    print("   [Skipping - requires generated C4 model]")

    # Step 4: Generate documentation
    print("\n\n📚 Step 4: Generating documentation...")
    print("-" * 60)
    print("   [Skipping - requires generated C4 model]")

    # Step 5: Analyze security
    print("\n\n🔒 Step 5: Analyzing security posture...")
    print("-" * 60)
    print("   [Skipping - requires generated C4 model]")

    # Step 6: Generate infrastructure
    print("\n\n🏗️  Step 6: Generating Terraform infrastructure...")
    print("-" * 60)
    print("   [Skipping - requires generated C4 model]")

    # Summary
    print("\n\n✨ Greenfield Project Workflow Summary")
    print("=" * 60)
    print("\n✅ Completed steps:")
    print("   1. Requirements discovery from markdown")
    print(f"      - Extracted {len(requirements.requirements)} requirements")
    print(f"      - Identified {len(requirements.user_stories)} user stories")
    print(f"      - Found {len(requirements.constraints)} technical constraints")

    print("\n📝 Next steps to complete the workflow:")
    print("   1. Implement GeneratorAgent.generate_from_requirements()")
    print("   2. Validate the generated architecture with ValidationAgent")
    print("   3. Perform security analysis with SecurityAgent")
    print("   4. Generate documentation with DocumentationAgent")
    print("   5. Generate Terraform with TerraformAgent")

    print(f"\n📂 Output files:")
    print(f"   - {requirements_file}")

    print("\n💡 To run the brownfield workflow:")
    print("   python examples/quick_start.py")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Workflow interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
