#!/bin/bash

echo "🚀 Setting up Astro Dev Plugin Marketplace..."
echo ""

# Get the absolute path to the marketplace
MARKETPLACE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "📍 Marketplace location: $MARKETPLACE_DIR"
echo ""

# Check if we're in a .claude directory
if [[ "$MARKETPLACE_DIR" == *"/.claude/"* ]]; then
    echo "✅ Marketplace is in .claude directory"
    PROJECT_ROOT="$(echo "$MARKETPLACE_DIR" | sed 's|\(.*\)/.claude/.*|\1|')"
    echo "📂 Project root: $PROJECT_ROOT"
    SETTINGS_FILE="$PROJECT_ROOT/.claude/settings.json"
else
    echo "ℹ️  Marketplace is not in project .claude directory"
    echo "   Using global Claude Code settings"
    SETTINGS_FILE="$HOME/.claude/settings.json"
fi

echo ""
echo "⚙️  Configuration file: $SETTINGS_FILE"
echo ""

# Create settings directory if it doesn't exist
SETTINGS_DIR="$(dirname "$SETTINGS_FILE")"
mkdir -p "$SETTINGS_DIR"

# Create settings file if it doesn't exist
if [ ! -f "$SETTINGS_FILE" ]; then
    echo '{}' > "$SETTINGS_FILE"
    echo "📝 Created new settings file"
fi

# Backup settings
cp "$SETTINGS_FILE" "$SETTINGS_FILE.backup.$(date +%Y%m%d_%H%M%S)"
echo "💾 Backed up existing settings"

# Determine relative or absolute path
if [[ "$MARKETPLACE_DIR" == *"/.claude/"* ]]; then
    # Use relative path for project-local marketplace
    REL_PATH="./.claude/sb-marketplace"
    echo "📌 Using relative path: $REL_PATH"
else
    # Use absolute path for global marketplace
    REL_PATH="$MARKETPLACE_DIR"
    echo "📌 Using absolute path: $REL_PATH"
fi

# Create settings update using jq if available, otherwise manual
if command -v jq &> /dev/null; then
    echo "✨ Using jq for settings update"

    jq --arg path "$REL_PATH" '
        .extraKnownMarketplaces."sb-marketplace".source.source = "local" |
        .extraKnownMarketplaces."sb-marketplace".source.path = $path |
        .enabledPlugins."astro-dev@sb-marketplace" = true
    ' "$SETTINGS_FILE" > "$SETTINGS_FILE.tmp" && mv "$SETTINGS_FILE.tmp" "$SETTINGS_FILE"

    echo "✅ Settings updated successfully"
else
    echo "ℹ️  jq not found - using manual configuration"
    echo ""
    echo "Please add the following to $SETTINGS_FILE:"
    echo ""
    cat << INNER_EOF
{
  "extraKnownMarketplaces": {
    "sb-marketplace": {
      "source": {
        "source": "local",
        "path": "$REL_PATH"
      }
    }
  },
  "enabledPlugins": {
    "astro-dev@sb-marketplace": true
  }
}
INNER_EOF
    echo ""
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ Setup Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "The Astro Dev plugin (v2.0) is now ready to use!"
echo ""
echo "📦 Plugin: astro-dev@sb-marketplace v2.0.0"
echo "📚 Components:"
echo "   • Agents: astro-orchestrator, astro-developer, astro-auditor, astro-architect"
echo "   • Skills: astro-coding, astro-knowledge"
echo "   • Commands: /develop, /implement, /architect, /audit, /lookup"
echo ""
echo "🎯 Quick Start:"
echo "   /develop Add a blog with categories and pagination"
echo "   /implement Create a Card component"
echo "   /architect Design a multi-language docs system"
echo "   /audit auto src/pages/"
echo "   /lookup getStaticPaths"
echo ""
echo "📖 Documentation:"
echo "   README.md - Marketplace overview"
echo "   astro-dev/README.md - Plugin documentation"
echo "   ARCHITECTURE_SPEC.md - v2.0 system design"
echo ""
echo "💡 Tips:"
echo "   • Use /develop for most tasks (orchestrated workflow)"
echo "   • Use /implement for simple, direct changes"
echo "   • Audit levels adapt automatically (light/medium/comprehensive)"
echo "   • Skills load selectively to optimize token usage"
echo ""

if [ -f "$SETTINGS_FILE.backup."* ]; then
    echo "📋 Settings backup saved:"
    ls -t "$SETTINGS_FILE.backup."* | head -1
    echo ""
fi

echo "Happy coding with Astro! 🚀"
echo ""
