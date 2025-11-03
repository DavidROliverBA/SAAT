#!/bin/bash
# Install SAAT slash commands for Claude Code
# This makes SAAT agents easily accessible via slash commands

set -e

echo "🚀 Installing SAAT Slash Commands for Claude Code"
echo "=================================================="
echo ""

# Determine installation location
CLAUDE_DIR="$HOME/.claude"
COMMANDS_DIR="$CLAUDE_DIR/commands"

# Create directory if it doesn't exist
if [ ! -d "$COMMANDS_DIR" ]; then
    echo "📁 Creating Claude Code commands directory: $COMMANDS_DIR"
    mkdir -p "$COMMANDS_DIR"
fi

# Copy command files
echo "📋 Copying SAAT command files..."
cp -v .claude/commands/*.md "$COMMANDS_DIR/"

echo ""
echo "✅ Installation complete!"
echo ""
echo "📝 Installed commands:"
echo "  - /saat-discover"
echo "  - /saat-requirements"
echo "  - /saat-generate"
echo "  - /saat-analyze-characteristics ⭐ NEW"
echo "  - /saat-validate"
echo "  - /saat-security"
echo "  - /saat-document"
echo "  - /saat-terraform"
echo "  - /saat-full-pipeline"
echo "  - /saat-help"
echo ""
echo "🎯 Usage:"
echo "  1. Open Claude Code CLI"
echo "  2. Type '/saat' and press Tab to see all commands"
echo "  3. Select a command and follow the prompts"
echo ""
echo "💡 Try it now:"
echo "  /saat-help"
echo ""
echo "📚 Documentation:"
echo "  - .claude/README.md - How to use slash commands"
echo "  - docs/AGENTS_QUICK_REFERENCE.md - All agents overview"
echo "  - docs/ARCHITECTURE_CHARACTERISTICS_USAGE.md - Detailed guide"
echo ""
echo "Happy architecting! 🏗️"
