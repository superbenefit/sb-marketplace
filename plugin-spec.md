# Astro Development Plugin Architecture Specification

## Overview

This specification outlines the architecture for transforming the current sub-agent configuration into an optimized Claude Code plugin that combines Skills, Sub-agents, Hooks, and Commands for comprehensive Astro/Starlight development support.

## Architecture Design Principles

### Component Selection Strategy

- **Skills**: For frequently-used capabilities that don't require parallel processing
- **Sub-agents**: For complex, parallelizable tasks requiring separate context
- **Hooks**: For automatic workflows (like post-implementation auditing)
- **Slash commands**: For quick access to common operations
- **MCP servers**: For tool integration (future expansion)

### Progressive Disclosure

Skills and resources load only when needed, optimizing context window usage:
1. **Metadata** (~100 tokens): Always loaded for discovery
2. **Skill body** (<5k tokens): Loaded when triggered
3. **Resources** (unlimited): Loaded on-demand via filesystem

## File Structure

```
F:\projects\sb-governance-starlight\
└── .claude/
    └── dev-marketplace/                   # Marketplace repository
        ├── .claude-plugin/                # Marketplace metadata
        │   └── marketplace.json           # Marketplace manifest
        ├── astro-dev/                     # Plugin directory
        │   ├── .claude-plugin/
        │   │   └── plugin.json            # Plugin manifest
        │   ├── skills/                    # Agent Skills
        │   │   ├── astro-developer/
        │   │   │   ├── SKILL.md
        │   │   │   └── references/
        │   │   └── astro-docs/
        │   │       ├── SKILL.md
        │   │       └── references/
        │   ├── agents/                    # Specialized sub-agents
        │   │   ├── astro-auditor.md
        │   │   └── astro-architect.md
        │   ├── commands/                  # Slash commands
        │   │   ├── audit.md
        │   │   ├── implement.md
        │   │   └── docs-lookup.md
        │   ├── hooks/                     # Automation hooks
        │   │   └── hooks.json
        │   ├── scripts/                   # Utility scripts
        │   │   └── audit-runner.sh
        │   └── knowledge-base/            # Shared references
        │       ├── astro-syntax/
        │       ├── common-mistakes/
        │       └── best-practices/
        └── setup.sh                       # Installation script
```

## Component Specifications

### 1. Marketplace Manifest

**Location**: `.claude/dev-marketplace/.claude-plugin/marketplace.json`

```json
{
  "name": "astro-dev-marketplace",
  "description": "Local development marketplace for Astro/Starlight development tools",
  "owner": {
    "name": "Your Team",
    "email": "team@example.com"
  },
  "plugins": [
    {
      "name": "astro-dev",
      "source": "./astro-dev",
      "description": "Complete Astro/Starlight development toolkit with skills, agents, and automated workflows",
      "version": "1.0.0",
      "author": {
        "name": "Your Team"
      },
      "tags": ["development", "astro", "starlight", "documentation"],
      "category": "development"
    }
  ]
}
```

### 2. Plugin Manifest

**Location**: `.claude/dev-marketplace/astro-dev/.claude-plugin/plugin.json`

```json
{
  "name": "astro-dev",
  "description": "Comprehensive Astro/Starlight development toolkit with skills, agents, and automated workflows",
  "version": "1.0.0",
  "author": {
    "name": "Your Team",
    "email": "team@example.com"
  },
  "license": "MIT",
  "tags": ["astro", "starlight", "development", "documentation"],
  "agents": {
    "astro-auditor": {
      "path": "agents/astro-auditor.md",
      "description": "Code auditor for Astro/Starlight projects"
    },
    "astro-architect": {
      "path": "agents/astro-architect.md", 
      "description": "Content architecture specialist for complex planning"
    }
  },
  "commands": {
    "audit": "commands/audit.md",
    "implement": "commands/implement.md",
    "docs-lookup": "commands/docs-lookup.md"
  },
  "hooks": "hooks/hooks.json",
  "skills": [
    {
      "name": "astro-developer",
      "path": "skills/astro-developer"
    },
    {
      "name": "astro-docs",
      "path": "skills/astro-docs"
    }
  ]
}
```

### 3. Developer Skill

**Location**: `.claude/dev-marketplace/astro-dev/skills/astro-developer/SKILL.md`

```markdown
---
name: astro-developer
description: Expert Astro/Starlight developer for implementing features, writing components, fixing bugs, and configuring projects. Use for all code implementation tasks in Astro projects, including components, pages, layouts, content collections, and configuration.
---

# Astro Developer Skill

This skill provides expert Astro/Starlight development capabilities with deep knowledge of best practices and common pitfalls.

## Core Capabilities

- **Component Development**: Write .astro components with proper syntax and directives
- **Page & Routing**: Implement dynamic routes with getStaticPaths
- **Content Collections**: Create and query collections with proper schemas
- **Configuration**: Modify astro.config.mjs and TypeScript configs
- **Bug Fixes**: Diagnose and fix common Astro errors

## Knowledge Base Access

When implementing, reference these knowledge files as needed:

### Syntax References (references/astro-syntax/)
- `component-structure.md`: Component anatomy, frontmatter, templates
- `directives.md`: All client:*, is:*, set:* directives
- `imports.md`: Import patterns with required file extensions
- `routing.md`: Dynamic routes, getStaticPaths patterns

### Best Practices (references/best-practices/)
- `common-mistakes.md`: Cataloged errors and fixes
- `typescript-patterns.md`: Type safety requirements
- `performance.md`: Hydration and optimization patterns

## Implementation Protocol

### Before Writing Code
1. Check `references/common-mistakes.md` for known pitfalls
2. Review similar patterns in the project
3. Verify TypeScript strict mode requirements

### Critical Rules

**ALWAYS**:
- Include file extensions in imports (.astro, .ts, .tsx)
- Use `astro:content` not `astro/content`
- Type all Props interfaces
- Fetch data in frontmatter, not templates
- Sort collections when order matters
- Check entry existence before use

**NEVER**:
- Access Astro.params inside getStaticPaths()
- Use await in templates
- Expose server secrets to client
- Over-hydrate static content

### Quick Reference

#### Component Template
```typescript
---
import type { Props } from './types';
import Layout from '../layouts/Layout.astro'; // ✅ Extension

export interface Props {
  title: string;
  showDate?: boolean;
}

const { title, showDate = true } = Astro.props;
// Fetch data here, not in template
---

<Layout title={title}>
  <!-- Template here, no await -->
</Layout>
```

#### Dynamic Route Template
```typescript
---
import { getCollection } from 'astro:content'; // ✅ astro: prefix

export async function getStaticPaths() {
  const posts = await getCollection('blog');
  
  // ✅ Sort collections
  const sorted = posts.sort((a, b) => 
    b.data.date.valueOf() - a.data.date.valueOf()
  );
  
  return sorted.map(post => ({
    params: { slug: post.id },
    props: { post }
  }));
}

const { post } = Astro.props; // ✅ From props, not params

if (!post) {
  return Astro.redirect('/404'); // ✅ Handle missing
}
---
```

## Working with Other Components

- **For API verification**: Request docs lookup with `/docs-lookup` command
- **For architecture planning**: Invoke @astro-architect agent
- **After implementation**: Auto-audit hook will check your code

## Error Handling Patterns

Always implement proper error boundaries:

```typescript
try {
  const data = await fetchAPI();
  // process data
} catch (error) {
  console.error('API fetch failed:', error);
  // graceful fallback
}
```

## Testing Checklist

Before considering implementation complete:
- [ ] All imports have extensions
- [ ] TypeScript types defined
- [ ] Collections sorted if needed
- [ ] Error handling in place
- [ ] No server secrets exposed
- [ ] Accessibility considered
```

### 4. Docs Lookup Skill

**Location**: `.claude/dev-marketplace/astro-dev/skills/astro-docs/SKILL.md`

```markdown
---
name: astro-docs
description: Astro/Starlight documentation specialist for API verification, syntax lookup, and feature availability checks. Use when needing to verify current Astro APIs, check feature support, or find documentation for unfamiliar Astro/Starlight features.
---

# Astro Documentation Skill

Expert at finding and verifying Astro/Starlight API documentation and best practices.

## Capabilities

- **API Verification**: Confirm current syntax for Astro APIs
- **Feature Lookup**: Check availability and usage of features
- **Documentation Search**: Find relevant docs quickly
- **Best Practices**: Provide current recommendations

## Documentation Index

### Quick Reference (references/docs-index.md)
Comprehensive sitemap of Astro documentation sections for targeted searches.

### Cached Documentation (references/llms-cache/)
- Full Astro API reference
- Starlight configuration guide
- Content Collections API
- Routing patterns

## Search Strategy

1. **Identify Section**: Check docs-index.md for relevant section
2. **Target Search**: Use specific terms from section titles
3. **Verify Currency**: Cross-reference with latest docs if needed
4. **Provide Context**: Include URLs and examples

## Common Lookups

### Collections API
```typescript
// Verify with: getCollection, getEntry, getEntries
import { getCollection, getEntry } from 'astro:content';
```

### Dynamic Routes
```typescript
// Check: getStaticPaths return format
export async function getStaticPaths() {
  return [{
    params: { /* only string|number|undefined */ },
    props: { /* any data */ }
  }];
}
```

### Starlight Config
```javascript
// Verify: starlight() integration options
export default defineConfig({
  integrations: [
    starlight({
      title: 'Docs',
      // verify available options
    })
  ]
});
```

## Integration with Development

When verifying APIs:
1. Check cached references first
2. Note version-specific features
3. Provide migration paths if applicable
4. Include example usage

## Output Format

When providing documentation:
- Include source URL
- Show current syntax
- Note any deprecations
- Provide working example
```

### 5. Auditor Sub-Agent

**Location**: `.claude/dev-marketplace/astro-dev/agents/astro-auditor.md`

```markdown
---
name: astro-auditor
description: Comprehensive code auditor for Astro/Starlight implementations. Use AFTER code changes to verify correctness, security, and best practices.
model: sonnet
---

# Astro Code Auditor

Expert auditor for reviewing Astro/Starlight code changes with deep knowledge of syntax rules and common pitfalls.

## Audit Protocol

### Priority 1: Build-Breaking Issues ❌
**Check immediately - these will cause failures**

- [ ] Component structure (---/--- fence matching)
- [ ] Missing file extensions in imports
- [ ] Wrong module prefixes (astro:content not astro/content)
- [ ] Dynamic routes missing getStaticPaths()
- [ ] Invalid directive syntax

### Priority 2: Critical Issues ⚠️
**Security, performance, and common bugs**

#### Security
- [ ] set:html with user input (XSS risk)
- [ ] Exposed secrets in client code
- [ ] Missing input validation

#### Performance
- [ ] Over-hydration (client:load on static content)
- [ ] Missing image dimensions
- [ ] Unnecessary client bundles

#### Common Mistakes
- [ ] className instead of class
- [ ] Accessing params in getStaticPaths
- [ ] Unsorted collections
- [ ] Missing null checks

### Priority 3: Best Practices 💡
**Code quality improvements**

- [ ] TypeScript usage
- [ ] Error handling
- [ ] Accessibility
- [ ] Code organization

## Knowledge Base References

Consult during audit:
- `${CLAUDE_PLUGIN_ROOT}/knowledge-base/astro-syntax/*`
- `${CLAUDE_PLUGIN_ROOT}/knowledge-base/common-mistakes/*`
- `${CLAUDE_PLUGIN_ROOT}/knowledge-base/best-practices/*`

## Report Format

```markdown
# Audit Report

## Summary
- Files reviewed: X
- Critical issues: X
- Warnings: X
- Suggestions: X

## Priority 1: Critical ❌
[Detailed issues with fixes]

## Priority 2: Important ⚠️
[Issues with explanations]

## Priority 3: Suggestions 💡
[Improvements]

## ✅ Good Patterns Observed
[Positive feedback]
```

## Integration

- Triggered automatically via hooks after file changes
- Can be manually invoked with `/audit` command
- Works in parallel without affecting main context
```

### 6. Architect Sub-Agent

**Location**: `.claude/dev-marketplace/astro-dev/agents/astro-architect.md`

```markdown
---
name: astro-architect
description: Content architecture specialist for complex Astro/Starlight planning. Use for designing collection structures, loader architectures, and multi-source content systems.
model: sonnet
---

# Astro Content Architect

Expert at designing robust content architectures for Astro/Starlight projects.

## Specializations

### Content Collections
- Schema design with Zod
- Cross-collection references
- Query optimization patterns
- TypeScript integration

### Custom Loaders
- External API integration
- Authentication strategies
- Caching mechanisms
- Error handling patterns

### Routing Strategy
- Dynamic route design
- Pagination architecture
- Nested routing patterns
- Performance optimization

### Multi-Source Systems
- GitBook integration
- CMS connections
- API data pipelines
- Build vs runtime strategies

## Architecture Process

1. **Requirements Analysis**
   - Data sources identification
   - Performance requirements
   - Scalability needs
   - Team constraints

2. **Design Phase**
   - Collection structure
   - Schema definitions
   - Loader architecture
   - Caching strategy

3. **Implementation Planning**
   - Step-by-step roadmap
   - API verification needs
   - Risk mitigation
   - Testing approach

## Knowledge Base

Access architectural patterns:
- `${CLAUDE_PLUGIN_ROOT}/knowledge-base/architecture-patterns/*`
- `${CLAUDE_PLUGIN_ROOT}/knowledge-base/loader-examples/*`
- `${CLAUDE_PLUGIN_ROOT}/knowledge-base/integration-guides/*`

## Output Deliverables

### Architecture Document
- System overview
- Component design
- Data flow diagrams
- Implementation steps

### Code Templates
- Collection schemas
- Loader boilerplate
- Route structures
- Type definitions

## Collaboration

- Works with astro-developer skill for implementation
- Coordinates with astro-docs for API verification
- Provides specs for astro-auditor validation
```

### 7. Hooks Configuration

**Location**: `.claude/dev-marketplace/astro-dev/hooks/hooks.json`

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/audit-runner.sh",
            "timeout": 30,
            "description": "Auto-audit Astro files after changes"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command", 
            "command": "bash -c 'file=\"$1\"; [[ $file == *.astro || $file == *.ts || $file == *.tsx ]] && echo \"🔍 Will audit after implementation\" || true' -- \"${CLAUDE_HOOK_DATA_TOOL_INPUT_FILE_PATH}\"",
            "description": "Notify about upcoming audit"
          }
        ]
      }
    ]
  }
}
```

### 8. Slash Commands

#### `/implement` Command
**Location**: `.claude/dev-marketplace/astro-dev/commands/implement.md`

```markdown
---
name: implement
description: Start Astro implementation with best practices loaded
---

# Implement Astro Feature

Initializes an implementation session with:
- Best practices loaded
- Common mistakes reference ready
- TypeScript patterns available
- Auto-audit enabled

## Usage

```
/implement [feature-description]
```

## What This Does

1. Loads astro-developer skill
2. Reviews project structure
3. Checks for similar patterns
4. Enables audit hooks
5. Starts implementation

## Options

- `--no-audit`: Skip automatic auditing
- `--with-tests`: Generate test files
- `--typescript`: Enforce strict TypeScript
```

#### `/audit` Command
**Location**: `.claude/dev-marketplace/astro-dev/commands/audit.md`

```markdown
---
name: audit
description: Manually trigger comprehensive code audit
---

# Audit Astro Code

Performs comprehensive audit of recent changes.

## Usage

```
/audit [file-pattern]
```

## Audit Scope

- Syntax validation
- Security review
- Performance check
- Best practices
- Accessibility

## Output

Provides prioritized report:
- Critical issues (must fix)
- Important issues (should fix)
- Suggestions (consider)
```

#### `/docs-lookup` Command
**Location**: `.claude/dev-marketplace/astro-dev/commands/docs-lookup.md`

```markdown
---
name: docs-lookup
description: Quick Astro API documentation lookup
---

# Documentation Lookup

Fast API verification and documentation search.

## Usage

```
/docs-lookup [api-name]
```

## Examples

```
/docs-lookup getStaticPaths
/docs-lookup content collections
/docs-lookup starlight config
```

## Returns

- Current syntax
- Usage examples
- Common patterns
- Migration notes
```

### 9. Audit Runner Script

**Location**: `.claude/dev-marketplace/astro-dev/scripts/audit-runner.sh`

```bash
#!/bin/bash
# audit-runner.sh - Automatic audit for Astro files

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

# Create audit request
cat << EOF | tee /tmp/astro-audit-request.json
{
  "action": "audit",
  "file": "$FILE_PATH",
  "checks": [
    "syntax",
    "imports", 
    "typescript",
    "security",
    "performance"
  ]
}
EOF

# Trigger audit (non-blocking to avoid interrupting flow)
{
    sleep 2  # Brief delay to let changes settle
    echo "🔍 Running Astro audit on $FILE_PATH..."
    
    # Check critical issues only
    if grep -q "astro/content" "$FILE_PATH" 2>/dev/null; then
        echo "⚠️ Warning: Found 'astro/content' - should be 'astro:content'"
    fi
    
    if grep -q "className=" "$FILE_PATH" 2>/dev/null; then
        echo "⚠️ Warning: Found 'className' - should be 'class' in Astro"
    fi
    
    # Check for missing extensions in imports
    if grep -E "from ['\"][^'\"]*(?<!\.astro|\.ts|\.tsx|\.js|\.jsx|\.json|\.css|\.scss)['\"]" "$FILE_PATH" 2>/dev/null; then
        echo "⚠️ Warning: Possible missing file extension in import"
    fi
} &

exit 0
```

## Installation Instructions

### Setup Script

**Location**: `.claude/setup.sh`

```bash
#!/bin/bash

echo "🚀 Setting up Astro Dev Plugin Marketplace..."

# Ensure marketplace structure exists
mkdir -p .claude/dev-marketplace/.claude-plugin
mkdir -p .claude/dev-marketplace/astro-dev/.claude-plugin

# Create marketplace manifest
cat > .claude/dev-marketplace/.claude-plugin/marketplace.json << 'EOF'
{
  "name": "astro-dev-marketplace",
  "description": "Local development marketplace for Astro/Starlight development tools",
  "owner": {
    "name": "Your Team"
  },
  "plugins": [
    {
      "name": "astro-dev",
      "source": "./astro-dev",
      "description": "Complete Astro/Starlight development toolkit",
      "version": "1.0.0",
      "tags": ["development", "astro", "starlight"],
      "category": "development"
    }
  ]
}
EOF

# Copy existing knowledge base
echo "📚 Migrating knowledge base..."
mkdir -p .claude/dev-marketplace/astro-dev/knowledge-base
cp -r .claude/*-knowledge/* .claude/dev-marketplace/astro-dev/knowledge-base/ 2>/dev/null || true

# Create plugin manifest
cat > .claude/dev-marketplace/astro-dev/.claude-plugin/plugin.json << 'EOF'
{
  "name": "astro-dev",
  "description": "Comprehensive Astro/Starlight development toolkit",
  "version": "1.0.0",
  "author": {
    "name": "Your Team"
  }
}
EOF

# Update user settings to include the marketplace
echo "📦 Adding local marketplace to settings..."
SETTINGS_FILE="$HOME/.claude/settings.json"

# Create settings file if it doesn't exist
if [ ! -f "$SETTINGS_FILE" ]; then
    echo '{}' > "$SETTINGS_FILE"
fi

# Add marketplace using absolute path
MARKETPLACE_PATH="$(pwd)/.claude/dev-marketplace"
cat << EOF > /tmp/claude-settings-update.json
{
  "extraKnownMarketplaces": {
    "astro-dev-local": {
      "source": {
        "source": "local",
        "path": "$MARKETPLACE_PATH"
      }
    }
  }
}
EOF

echo "✅ Setup complete!"
echo ""
echo "To use the plugin in Claude Code:"
echo "1. Run: /plugin marketplace add astro-dev-local"
echo "2. Run: /plugin install astro-dev@astro-dev-local"
echo ""
echo "Or add to your project's .claude/settings.json:"
echo '  "enabledPlugins": {'
echo '    "astro-dev@astro-dev-local": true'
echo '  }'
```

### Repository-Level Configuration

**Location**: `.claude/settings.json`

```json
{
  "extraKnownMarketplaces": {
    "astro-dev-local": {
      "source": {
        "source": "local",
        "path": "./.claude/dev-marketplace"
      }
    }
  },
  "enabledPlugins": {
    "astro-dev@astro-dev-local": true
  }
}
```

## Migration Strategy

### Phase 1: Local Development Testing
1. Create plugin structure in `.claude/dev-marketplace/`
2. Copy knowledge base files to plugin
3. Test each component individually
4. Validate hooks and automation

### Phase 2: Team Testing
1. Share via local marketplace
2. Gather feedback on workflows
3. Iterate on skills and agents
4. Optimize knowledge base

### Phase 3: Production Distribution
1. Move to GitHub repository (`your-org/sb-marketplace`)
2. Add versioning and changelog
3. Implement CI/CD for updates
4. Document for team adoption

## Benefits of This Architecture

### Context Efficiency
- **Progressive Loading**: Only loads what's needed
- **Skill Metadata**: ~100 tokens for discovery
- **On-Demand Resources**: No context penalty for unused files

### Workflow Automation
- **Auto-Audit**: Hooks ensure quality checks
- **Format on Save**: Automatic code formatting
- **Error Prevention**: Pre-commit validation

### Team Collaboration
- **Shared Standards**: Consistent tooling across team
- **Easy Distribution**: Single command installation
- **Version Control**: Track and update centrally

### Developer Experience
- **Quick Commands**: `/implement`, `/audit`, `/docs-lookup`
- **Smart Skills**: Auto-triggered based on context
- **Parallel Processing**: Sub-agents work independently

## Future Enhancements

### Additional Skills
- `astro-testing`: Test generation and runner
- `astro-performance`: Performance optimization
- `astro-migration`: Version migration helper

### MCP Servers
- Documentation server for real-time API lookup
- Build status monitoring
- Deployment automation

### Advanced Hooks
- Pre-commit validation
- Post-deployment checks
- Team notification system

## Appendix: Knowledge Base Migration

### Current Knowledge Files to Migrate

From `.claude/astro-knowledge/`:
- `astro-syntax-reference.md` → `knowledge-base/astro-syntax/`
- `astro-directives-reference.md` → `knowledge-base/astro-syntax/`
- `astro-routing-reference.md` → `knowledge-base/astro-syntax/`
- `astro-imports-reference.md` → `knowledge-base/astro-syntax/`
- `astro-configuration-reference.md` → `knowledge-base/astro-syntax/`

From `.claude/developer-knowledge/`:
- `astro-best-practices.md` → `knowledge-base/best-practices/`
- `common-mistakes.md` → `knowledge-base/common-mistakes/`
- `starlight-patterns.md` → `knowledge-base/best-practices/`

From `.claude/content-knowledge/`:
- `content-collections-reference.md` → `knowledge-base/architecture-patterns/`
- `content-loader-api.md` → `knowledge-base/loader-examples/`
- `routing-pages-reference.md` → `knowledge-base/architecture-patterns/`
- `starlight-specific.md` → `knowledge-base/starlight/`
- `external-data-integration.md` → `knowledge-base/integration-guides/`

From `.claude/auditor-knowledge/`:
- `audit-checklist.md` → `knowledge-base/audit/`
- `code-quality-standards.md` → `knowledge-base/audit/`
- `typescript-standards.md` → `knowledge-base/best-practices/`

## Conclusion

This plugin architecture optimally combines Skills for capabilities, Sub-agents for complex work, Hooks for automation, and Commands for quick access. It maintains the strengths of the current system while adding the benefits of the Claude Code plugin ecosystem.

The progressive disclosure model ensures efficient context usage, while the marketplace structure enables easy team distribution and future expansion to other repositories.
