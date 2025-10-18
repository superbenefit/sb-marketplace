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
        .extraKnownMarketplaces.\"sb-marketplace\".source.source = "local" |
        .extraKnownMarketplaces.\"sb-marketplace\".source.path = $path |
        .enabledPlugins.\"astro-dev@sb-marketplace\" = true
    ' "$SETTINGS_FILE" > "$SETTINGS_FILE.tmp" && mv "$SETTINGS_FILE.tmp" "$SETTINGS_FILE"

    echo "✅ Settings updated successfully"
else
    echo "ℹ️  jq not found - using manual configuration"
    echo ""
    echo "Please add the following to $SETTINGS_FILE:"
    echo ""
    cat << EOF
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
EOF
    echo ""
fi

# Make audit script executable
chmod +x "$MARKETPLACE_DIR/astro-dev/scripts/audit-runner.sh"
echo "🔧 Made audit-runner.sh executable"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ Setup Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "The Astro Dev plugin is now ready to use!"
echo ""
echo "📦 Plugin: astro-dev@sb-marketplace"
echo "📚 Components:"
echo "   • Skills: astro-developer, astro-docs"
echo "   • Agents: astro-auditor, astro-architect"
echo "   • Commands: /implement, /audit, /docs-lookup"
echo "   • Hooks: Auto-audit on save"
echo ""
echo "🎯 Quick Start:"
echo "   /implement Add a blog listing page"
echo "   /audit src/pages/"
echo "   /docs-lookup getStaticPaths"
echo ""
echo "📖 Documentation:"
echo "   README.md - Marketplace overview"
echo "   astro-dev/README.md - Plugin documentation"
echo "   astro-dev/CHANGELOG.md - Version history"
echo ""
echo "💡 Tips:"
echo "   • Skills load automatically when needed"
echo "   • Use /implement for guided development"
echo "   • Run /audit before committing"
echo "   • Use /docs-lookup for quick API reference"
echo ""

if [ -f "$SETTINGS_FILE.backup."* ]; then
    echo "📋 Settings backup saved:"
    ls -t "$SETTINGS_FILE.backup."* | head -1
    echo ""
fi

echo "Happy coding with Astro! 🚀"
echo ""
