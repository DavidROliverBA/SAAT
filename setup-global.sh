#!/bin/bash
set -e

echo "🚀 Setting up SAAT for use from any directory..."
echo ""

SAAT_DIR="/home/user/SAAT"

# 1. Install SAAT via pip (makes CLI available everywhere)
echo "📦 Installing SAAT globally..."
cd "$SAAT_DIR"
pip install -e . > /dev/null 2>&1

# 2. Install slash commands globally
echo "⚡ Installing slash commands to ~/.claude/commands/..."
bash "$SAAT_DIR/install-claude-commands.sh"

# 3. Verify MCP server configuration
echo "🔌 Checking MCP server configuration..."
CLAUDE_CONFIG="$HOME/.config/claude/config.json"

if [ -f "$CLAUDE_CONFIG" ]; then
    if grep -q "saat" "$CLAUDE_CONFIG"; then
        echo "   ✅ MCP server already configured"
    else
        echo "   ⚠️  MCP server NOT configured"
        echo ""
        echo "Add this to $CLAUDE_CONFIG:"
        echo ""
        cat << 'EOF'
{
  "mcpServers": {
    "saat": {
      "command": "python",
      "args": ["/home/user/SAAT/saat_mcp_server.py"],
      "env": {
        "ANTHROPIC_API_KEY": "${env:ANTHROPIC_API_KEY}"
      }
    }
  }
}
EOF
        echo ""
    fi
else
    echo "   ⚠️  Claude config not found at $CLAUDE_CONFIG"
    echo "   Create it with the MCP server configuration above"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "You can now use SAAT from any directory:"
echo ""
echo "Option 1 (Claude Code slash commands):"
echo "  /saat-orchestrate"
echo "  /saat-discover"
echo "  /saat-analyze-characteristics"
echo ""
echo "Option 2 (CLI):"
echo "  saat discover --path . --output discovery.json"
echo "  saat analyze --path . --output architecture.json"
echo ""
echo "Test it:"
echo "  cd /path/to/any/repo"
echo "  saat --version"
echo "  # Or in Claude Code: /saat-help"
echo ""
