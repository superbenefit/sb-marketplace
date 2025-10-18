#!/bin/bash
# audit-runner.sh - Automatic audit for Astro files
# This script runs quick validation checks on Astro-related files after they are modified

set -euo pipefail

# Only audit relevant files
FILE_PATH="${CLAUDE_HOOK_DATA_TOOL_INPUT_FILE_PATH:-}"
if [[ -z "$FILE_PATH" ]]; then
    exit 0
fi

# Check if it's an Astro-related file
if [[ ! "$FILE_PATH" =~ \.(astro|ts|tsx|mjs|js)$ ]]; then
    exit 0
fi

# Skip if file doesn't exist (might be deleted)
if [[ ! -f "$FILE_PATH" ]]; then
    exit 0
fi

# Create audit request for logging
cat << EOF > /tmp/astro-audit-request.json
{
  "action": "audit",
  "file": "$FILE_PATH",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "checks": [
    "syntax",
    "imports",
    "typescript",
    "security",
    "performance"
  ]
}
EOF

# Run quick validation checks (non-blocking)
{
    sleep 1  # Brief delay to let changes settle

    echo "🔍 Running quick Astro audit on $FILE_PATH..."

    ISSUES_FOUND=0

    # Check for astro/content (should be astro:content)
    if grep -q "astro/content" "$FILE_PATH" 2>/dev/null; then
        echo "⚠️ Warning: Found 'astro/content' - should be 'astro:content'"
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    fi

    # Check for className (should be class in Astro)
    if grep -q "className=" "$FILE_PATH" 2>/dev/null; then
        echo "⚠️ Warning: Found 'className' - should be 'class' in Astro components"
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    fi

    # Check for missing extensions in imports (basic check)
    # This looks for imports without common file extensions
    if grep -E "from ['\"]\.\.?/[^'\"]*[^.astro|.ts|.tsx|.js|.jsx|.json|.css|.scss]['\"]" "$FILE_PATH" 2>/dev/null | grep -v "astro:" | grep -v "node:" | head -1; then
        echo "⚠️ Warning: Possible missing file extension in import (check carefully)"
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    fi

    # Check for Astro.params in getStaticPaths (common mistake)
    if grep -A 20 "getStaticPaths" "$FILE_PATH" 2>/dev/null | grep "Astro\.params" > /dev/null; then
        echo "⚠️ Warning: Accessing Astro.params inside getStaticPaths() is not valid"
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    fi

    # Check for await in template section (basic heuristic)
    # This is a simplified check - may have false positives
    if [[ "$FILE_PATH" == *.astro ]]; then
        # Get content after the frontmatter
        if awk '/^---$/{if(++c==2) flag=1; next} flag' "$FILE_PATH" | grep -q "await " 2>/dev/null; then
            echo "⚠️ Warning: Possible 'await' usage in template section - should be in frontmatter"
            ISSUES_FOUND=$((ISSUES_FOUND + 1))
        fi
    fi

    # Check for exposed environment variables (not PUBLIC_)
    if grep -E "import\.meta\.env\.[A-Z_]+[^P][^U][^B][^L][^I][^C]" "$FILE_PATH" 2>/dev/null; then
        echo "⚠️ Warning: Non-PUBLIC environment variable may be exposed to client"
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    fi

    if [[ $ISSUES_FOUND -eq 0 ]]; then
        echo "✅ Quick audit passed - no obvious issues found"
    else
        echo ""
        echo "Found $ISSUES_FOUND potential issue(s). Run /audit for detailed analysis."
    fi

} &

exit 0
