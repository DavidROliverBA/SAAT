#!/usr/bin/env python3
"""Example: Architecture Characteristics Analysis

This example demonstrates how to use the Architecture Characteristics Analysis Agent
to evaluate a C4 model against specified architecture characteristics.

It uses the example e-commerce platform C4 model and characteristics defined in this directory.
"""

import asyncio
import json
from pathlib import Path

from saat.converters_archchar import import_archchar_json
from saat.agents.archchar import (
    analyze_architecture_characteristics,
    generate_markdown_report,
    save_report,
)
from saat.models import C4Model


async def main():
    """Run architecture characteristics analysis example."""

    # File paths
    script_dir = Path(__file__).parent
    c4_model_file = script_dir / "c4-ecommerce.json"
    archchar_file = script_dir / "archchar-ecommerce.json"
    output_file = script_dir / "archchar-analysis-example"

    print("🔍 Architecture Characteristics Analysis Example")
    print("=" * 60)

    # Load C4 model
    print(f"\n📦 Loading C4 model: {c4_model_file}")
    model_data = json.loads(c4_model_file.read_text())
    c4_model = C4Model(**model_data)

    print(f"   Systems: {len(c4_model.systems)}")
    print(f"   Containers: {len(c4_model.containers)}")
    print(f"   Relationships: {len(c4_model.relationships)}")

    # Load architecture characteristics
    print(f"\n📊 Loading architecture characteristics: {archchar_file}")
    archchar_input = import_archchar_json(archchar_file)

    selected = [c for c in archchar_input.characteristics if c.selected]
    top_chars = [c.name for c in archchar_input.topCharacteristics]

    print(f"   Project: {archchar_input.projectName}")
    print(f"   Selected Characteristics: {len(selected)}")
    print(f"   Top 7: {', '.join(top_chars)}")

    # Run analysis
    print("\n🤖 Running architecture characteristics analysis...")
    print("   (This may take a few minutes)")

    result = await analyze_architecture_characteristics(
        c4_model=c4_model,
        archchar_input=archchar_input,
        model_name="anthropic:claude-sonnet-4",
        auto_approve=True,  # Skip approval prompts for this example
    )

    # Display results
    print("\n✅ Analysis Complete!")
    print("=" * 60)
    print(f"\n📈 Overall Score: {result.overall_score}/100")
    print(f"   Characteristics Analyzed: {result.characteristics_analyzed}")
    print(f"   Critical Gaps: {len(result.critical_gaps)}")
    print(f"   High Priority Gaps: {len(result.high_priority_gaps)}")
    print(f"   Top Recommendations: {len(result.top_recommendations)}")

    # Show executive summary
    print(f"\n📋 Executive Summary:")
    print(f"   {result.executive_summary}")

    # Show critical gaps
    if result.critical_gaps:
        print(f"\n⚠️  Critical Gaps:")
        for gap in result.critical_gaps[:3]:
            print(f"   - {gap.area}: {gap.issue}")
        if len(result.critical_gaps) > 3:
            print(f"   ... and {len(result.critical_gaps) - 3} more")

    # Show top recommendations
    if result.top_recommendations:
        print(f"\n💡 Top Recommendations:")
        for i, rec in enumerate(result.top_recommendations[:3], 1):
            print(f"   {i}. {rec.title} ({rec.priority} priority, {rec.implementation_effort} effort)")
        if len(result.top_recommendations) > 3:
            print(f"   ... and {len(result.top_recommendations) - 3} more")

    # Save reports
    print(f"\n💾 Saving Reports...")

    # Save markdown report
    markdown_path = output_file.with_suffix(".md")
    save_report(result, markdown_path, format="markdown")
    print(f"   📄 Markdown: {markdown_path}")

    # Save JSON report
    json_path = output_file.with_suffix(".json")
    save_report(result, json_path, format="json")
    print(f"   📊 JSON: {json_path}")

    # Show sample recommendations in detail
    if result.top_recommendations:
        print(f"\n🔧 Sample Recommendation Details:")
        rec = result.top_recommendations[0]
        print(f"\n   Title: {rec.title}")
        print(f"   Priority: {rec.priority}")
        print(f"   Effort: {rec.implementation_effort}")
        print(f"   Description: {rec.description}")
        if rec.pattern:
            print(f"   Pattern: {rec.pattern}")
        print(f"   Technologies: {', '.join(rec.technologies[:5])}")
        print(f"\n   Implementation Steps:")
        for i, step in enumerate(rec.implementation_steps[:3], 1):
            print(f"     {i}. {step}")
        if len(rec.implementation_steps) > 3:
            print(f"     ... and {len(rec.implementation_steps) - 3} more steps")

    print(f"\n✨ Done! Check the full reports for detailed analysis.")
    print("=" * 60)


if __name__ == "__main__":
    # Ensure you have set ANTHROPIC_API_KEY environment variable
    # export ANTHROPIC_API_KEY=your-api-key

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis cancelled by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
