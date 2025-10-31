"""Discovery Agent - Analyzes codebases to discover architecture using PydanticAI."""

import asyncio
import json
from pathlib import Path
from typing import Any, Optional

from pydantic import Field
from pydantic_ai import Agent, RunContext

from saat.models import DiscoveryResult, PatternMatch


# ============================================================================
# Dependencies (Context) for the Discovery Agent
# ============================================================================


class DiscoveryDependencies:
    """Dependencies injected into discovery agent tools."""

    def __init__(self, repo_path: str, max_depth: int = 3):
        self.repo_path = Path(repo_path)
        self.max_depth = max_depth
        self.file_cache: dict[str, str] = {}

    async def read_file(self, file_path: str) -> str:
        """Read and cache file contents."""
        if file_path in self.file_cache:
            return self.file_cache[file_path]

        full_path = self.repo_path / file_path
        if full_path.exists() and full_path.is_file():
            try:
                content = full_path.read_text(encoding="utf-8", errors="ignore")
                self.file_cache[file_path] = content
                return content
            except Exception as e:
                return f"Error reading file: {e}"
        return "File not found"

    async def list_files(self, pattern: str = "*") -> list[str]:
        """List files matching pattern."""
        try:
            files = []
            for p in self.repo_path.rglob(pattern):
                if p.is_file():
                    relative = p.relative_to(self.repo_path)
                    # Skip common ignore patterns
                    if not any(
                        part.startswith(".")
                        or part in {"node_modules", "__pycache__", "venv", "dist", "build"}
                        for part in relative.parts
                    ):
                        files.append(str(relative))
            return files[:100]  # Limit to first 100 files
        except Exception:
            return []


# ============================================================================
# Create Discovery Agent with PydanticAI
# ============================================================================


def create_discovery_agent(model: str = "anthropic:claude-sonnet-4") -> Agent[
    DiscoveryDependencies, DiscoveryResult
]:
    """Create a Discovery Agent using PydanticAI.

    Args:
        model: Model identifier (e.g., "anthropic:claude-sonnet-4", "openai:gpt-4")

    Returns:
        Configured PydanticAI Agent
    """
    agent: Agent[DiscoveryDependencies, DiscoveryResult] = Agent(
        model,
        deps_type=DiscoveryDependencies,
        result_type=DiscoveryResult,
        system_prompt="""You are an expert software architecture analyst specializing in discovering
architectural patterns and technologies from source code repositories.

Your role is to:
1. Analyze repository structure and files
2. Identify technologies, frameworks, and languages used
3. Detect architectural patterns (microservices, monolith, event-driven, etc.)
4. Find entry points (main files, APIs, CLI interfaces)
5. Assess confidence based on evidence found

Provide detailed, accurate analysis with confidence scores and supporting evidence.""",
    )

    @agent.tool
    async def discover_technologies(
        ctx: RunContext[DiscoveryDependencies], file_patterns: list[str]
    ) -> dict[str, Any]:
        """Discover technologies by checking for specific configuration files.

        Args:
            ctx: Agent context with repository access
            file_patterns: List of file patterns to check (e.g., ['package.json', '*.py'])

        Returns:
            Dictionary with found files and their contents
        """
        found_files: dict[str, str] = {}

        for pattern in file_patterns:
            files = await ctx.deps.list_files(pattern)
            for file_path in files[:10]:  # Limit to 10 files per pattern
                content = await ctx.deps.read_file(file_path)
                if content and "Error" not in content and "not found" not in content.lower():
                    # Truncate large files
                    if len(content) > 2000:
                        content = content[:2000] + "..."
                    found_files[file_path] = content

        return {"found_files": found_files, "total_matches": len(found_files)}

    @agent.tool
    async def analyze_file_structure(
        ctx: RunContext[DiscoveryDependencies],
    ) -> dict[str, Any]:
        """Analyze the overall repository file structure.

        Args:
            ctx: Agent context with repository access

        Returns:
            Repository structure information
        """
        # Get all files
        all_files = await ctx.deps.list_files("*")

        # Categorize by extension
        extensions: dict[str, int] = {}
        directories: set[str] = set()

        for file_path in all_files:
            path = Path(file_path)
            ext = path.suffix.lower()
            if ext:
                extensions[ext] = extensions.get(ext, 0) + 1

            # Track top-level directories
            if len(path.parts) > 0:
                directories.add(path.parts[0])

        return {
            "total_files": len(all_files),
            "extensions": extensions,
            "top_directories": sorted(directories),
            "sample_files": all_files[:20],
        }

    @agent.tool
    async def read_specific_files(
        ctx: RunContext[DiscoveryDependencies], file_paths: list[str]
    ) -> dict[str, str]:
        """Read specific files from the repository.

        Args:
            ctx: Agent context with repository access
            file_paths: List of file paths to read

        Returns:
            Dictionary mapping file paths to their contents
        """
        contents: dict[str, str] = {}

        for file_path in file_paths[:10]:  # Limit to 10 files
            content = await ctx.deps.read_file(file_path)
            if len(content) > 3000:
                content = content[:3000] + "..."
            contents[file_path] = content

        return contents

    return agent


# ============================================================================
# High-level Discovery Agent wrapper
# ============================================================================


class DiscoveryAgent:
    """High-level wrapper for the discovery agent."""

    def __init__(self, model: str = "anthropic:claude-sonnet-4"):
        """Initialize Discovery Agent.

        Args:
            model: Model identifier
        """
        self.agent = create_discovery_agent(model)
        self.model = model

    async def analyze_repository(
        self, repo_path: str, max_depth: int = 3
    ) -> DiscoveryResult:
        """Analyze a repository and discover its architecture.

        Args:
            repo_path: Path to repository to analyze
            max_depth: Maximum directory depth to explore

        Returns:
            Discovery results with technologies, patterns, and confidence
        """
        deps = DiscoveryDependencies(repo_path, max_depth)

        result = await self.agent.run(
            f"""Analyze the repository at '{repo_path}' and discover:

1. All technologies used (languages, frameworks, databases, tools)
2. Architectural patterns (microservices, monolith, event-driven, layered, etc.)
3. Entry points (main application files, API endpoints, CLI commands)
4. Overall confidence in your analysis (0.0 to 1.0)

Use the available tools to explore the repository structure and read key files.
Provide comprehensive analysis with evidence for each finding.""",
            deps=deps,
        )

        return result.data

    async def analyze_repository_with_context(
        self, repo_path: str, context: str, max_depth: int = 3
    ) -> DiscoveryResult:
        """Analyze repository with additional context.

        Args:
            repo_path: Path to repository
            context: Additional context or focus areas
            max_depth: Maximum directory depth

        Returns:
            Discovery results
        """
        deps = DiscoveryDependencies(repo_path, max_depth)

        result = await self.agent.run(
            f"""Analyze the repository at '{repo_path}' with this context: {context}

Discover:
1. Technologies used
2. Architectural patterns
3. Entry points
4. Confidence score

Use tools to explore the repository.""",
            deps=deps,
        )

        return result.data


# ============================================================================
# Convenience functions
# ============================================================================


async def discover_repository(
    repo_path: str, model: str = "anthropic:claude-sonnet-4", max_depth: int = 3
) -> DiscoveryResult:
    """Convenience function to discover a repository's architecture.

    Args:
        repo_path: Path to repository
        model: Model to use
        max_depth: Maximum directory depth

    Returns:
        Discovery results
    """
    agent = DiscoveryAgent(model)
    return await agent.analyze_repository(repo_path, max_depth)
