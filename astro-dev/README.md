# Astro Dev Plugin

Simplified Astro and Starlight development toolkit for Claude Code with intelligent tiered knowledge loading.

## Overview

The astro-dev plugin provides expert assistance for Astro and Starlight development through two primary commands and a smart knowledge system that loads context efficiently based on your task.

**Version**: 0.4.0 (Simplified Architecture)

## Quick Start

```bash
# Main development command - handles everything
/dev Create a blog with categories and pagination

# Quick API reference lookup
/lookup getCollection

# Architecture planning for complex systems
/design Multi-tenant docs system with GitBook integration
```

That's it! The `/dev` command is your primary tool for all Astro/Starlight development.

## Commands

### `/dev [description]`
**Your main command** for all development tasks - from simple components to complex features.

```bash
# Simple component
/dev Add a Footer component with social links

# Feature with collections
/dev Create a blog with categories, tags, and pagination

# Bug fixes
/dev Fix all TypeScript errors in the components folder

# Complex integration
/dev Integrate external API with custom content loader

# With validation control
/dev Add authentication --audit=comprehensive
/dev Create test component --audit=off
```

**Auto-validation**: Automatically validates code based on task size (can override with `--audit` flag).

### `/lookup [query]`
**Quick API reference** for Astro/Starlight APIs and syntax.

```bash
/lookup getCollection
/lookup client directives
/lookup starlight config
/lookup getStaticPaths
```

Returns current syntax, examples, and documentation links.

### `/design [system]`
**Architecture planning** for complex systems (optional, use before complex builds).

```bash
/design Multi-language content system with versioning
/design Integration strategy for Supabase + Astro
/design Refactor 200 pages to content collections
```

Provides design documents, schemas, and implementation roadmaps. Then use `/dev` to implement.

## Skills

The plugin provides two skills with intelligent loading:

### `astro-coding`
**Implementation knowledge** loaded in three tiers:

- **Tier 1** (Always, ~100 tokens): Critical rules that prevent breaking errors
- **Tier 2** (Context-based, ~400 tokens): Relevant patterns for your task
- **Tier 3** (On-demand, ~800 tokens): Deep-dive references for complex work

### `astro-knowledge`
**API reference** for quick documentation lookups via `/lookup` command.

## Critical Rules (Always Applied)

These 10 rules are enforced on every task to prevent build failures:

1. ✅ **File extensions required**: `import Layout from './Layout.astro'` (not `'./Layout'`)
2. ✅ **Correct module prefix**: `'astro:content'` (not `'astro/content'`)
3. ✅ **Use `class` not `className`** in .astro files
4. ✅ **Await in frontmatter only**, never in templates
5. ✅ **Never expose `SECRET_*`** environment variables client-side
6. ✅ **Type all Props interfaces** with TypeScript
7. ✅ **Define `getStaticPaths()`** for dynamic routes
8. ✅ **Don't access `Astro.params`** inside `getStaticPaths()`
9. ✅ **Use `CollectionEntry<'name'>`** types for collections
10. ✅ **Validate XSS risk** with `set:html` (only use with trusted sources)

## Knowledge Base Structure

```
knowledge-base/
├── critical-rules.md          # Tier 1: Always loaded (~100 tokens)
├── astro-patterns.md          # Tier 2: Core patterns (~400 tokens)
├── error-catalog.md           # Tier 2: 100+ errors indexed by symptom
├── starlight-guide.md         # Tier 2: Starlight-specific patterns
└── deep-dive/                 # Tier 3: On-demand (~800 tokens)
    ├── integrations.md        # External data & custom loaders
    ├── content-collections-reference.md
    ├── content-loader-api.md
    ├── external-data-integration.md
    ├── routing-pages-reference.md
    └── starlight-specific.md
```

## Usage Examples

### Simple Component
```bash
/dev Create a Card component with title, description, and image props
```

Result: Component created with proper TypeScript types, accessibility, and validation.

### Feature Implementation
```bash
/dev Add a blog with categories, pagination, and RSS feed
```

Result: Complete blog system with content collections, dynamic routes, and all features.

### Bug Fixing
```bash
/dev Fix the import errors in the components folder
```

Result: All imports fixed with proper extensions and module paths.

### Complex Architecture
```bash
# Step 1: Design the system
/design Multi-tenant docs with role-based access control

# Step 2: Review the architecture document

# Step 3: Implement it
/dev Implement the multi-tenant docs architecture
```

Result: Full implementation following the design plan.

### API Lookup
```bash
/lookup getStaticPaths
```

Result: Current syntax, usage examples, TypeScript types, and documentation links.

## How It Works

### Tiered Knowledge Loading

The plugin loads knowledge intelligently based on your task:

**For simple tasks** (1 file, <20 lines):
- Tier 1: Critical rules only (~100 tokens)
- Fast execution, minimal context

**For standard tasks** (2-5 files, <100 lines):
- Tier 1: Critical rules (~100 tokens)
- Tier 2: Relevant patterns (~400 tokens)
- Balanced approach

**For complex tasks** (>5 files or >100 lines):
- Tier 1: Critical rules (~100 tokens)
- Tier 2: Multiple patterns (~400 tokens)
- Tier 3: Deep-dive references (~800 tokens)
- Comprehensive coverage

### Auto-Validation

Code is automatically validated based on task size:

| Task Size | Validation Level | Checks |
|-----------|------------------|--------|
| Small (1 file, <20 lines) | Light | 5 critical checks |
| Medium (2-5 files, <100 lines) | Medium | 20 checks |
| Large (>5 files or >100 lines) | Comprehensive | 50+ checks |
| Security-sensitive | Always Comprehensive | Full security scan |

Override with `--audit` flag: `--audit=off`, `--audit=light`, `--audit=comprehensive`

## Error Catalog

The plugin includes a comprehensive error catalog with 100+ common Astro errors indexed by symptom:

```
Error: "Cannot find module './Header'"
→ Cause: Missing file extension
→ Fix: Add .astro extension
→ Example: import Header from './Header.astro';
```

**Categories**:
- Import errors
- Component errors
- Routing errors
- Collection errors
- Starlight errors
- Configuration errors
- TypeScript errors
- Runtime errors

## What Changed in v0.4.0

### Simplified Architecture

**Before (v0.3.x)**:
- 5 commands: `/develop`, `/implement`, `/architect`, `/audit`, `/lookup`
- 4 agents: orchestrator, developer, architect, auditor
- Complex orchestration layer
- Decision paralysis ("which command do I use?")

**Now (v0.4.0)**:
- 3 commands: `/dev`, `/design`, `/lookup`
- 0 agents (skills handle everything)
- Direct, simple execution
- Clear purpose for each command

### Benefits

- **60% reduction in complexity**: Fewer commands, no agents, clearer architecture
- **Better UX**: One main command (`/dev`) for all implementation
- **Same expertise**: All domain knowledge preserved in tiered skills
- **Lower token usage**: Intelligent tiered loading reduces overhead by 40-70%
- **Easier maintenance**: Simpler architecture, fewer moving parts

### Migration from v0.3.x

| Old Command | New Command |
|-------------|-------------|
| `/develop [task]` | `/dev [task]` |
| `/implement [task]` | `/dev [task]` |
| `/architect [design]` | `/design [design]` |
| `/audit [level] [path]` | `--audit=level` flag on `/dev` |
| `/lookup [api]` | `/lookup [api]` (unchanged) |

## File Organization

```
astro-dev/
├── .claude-plugin/
│   └── plugin.json              # Plugin manifest
├── skills/
│   ├── astro-coding/
│   │   └── SKILL.md            # Implementation knowledge (tiered)
│   └── astro-knowledge/
│       └── SKILL.md            # API reference
├── commands/
│   ├── dev.md                  # Main development command
│   ├── design.md               # Architecture planning
│   └── lookup.md               # API lookup
├── knowledge-base/
│   ├── critical-rules.md       # Tier 1
│   ├── astro-patterns.md       # Tier 2
│   ├── error-catalog.md        # Tier 2
│   ├── starlight-guide.md      # Tier 2
│   └── deep-dive/              # Tier 3
├── CHANGELOG.md                # Version history
└── README.md                   # This file
```

## Installation

### Via GitHub Marketplace

Add to `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "sb-marketplace": {
      "source": {
        "source": "github",
        "repo": "superbenefit/sb-marketplace"
      }
    }
  },
  "enabledPlugins": {
    "astro-dev@sb-marketplace": true
  }
}
```

Restart Claude Code to load the plugin.

### Verify Installation

Check that commands are available:
```bash
/dev --help
/lookup --help
/design --help
```

## Troubleshooting

### Plugin Not Loading

1. Check `.claude/settings.json` has correct marketplace configuration
2. Verify plugin is enabled: `"astro-dev@sb-marketplace": true`
3. Restart Claude Code
4. Check for errors in Claude Code logs

### Commands Not Working

1. Ensure you're in an Astro/Starlight project directory
2. Try explicit command: `/dev Create a simple component`
3. Check command syntax in `/dev --help`

### Unexpected Results

1. Be more specific in your request
2. Mention constraints: `/dev Add blog (must use existing UI library)`
3. Reference existing patterns: `/dev Create Card (like existing Button component)`

## Best Practices

### Write Clear Requests

```
❌ /dev make a blog
✅ /dev Create a blog collection with title, date, author, tags, and categories

❌ /dev fix it
✅ /dev Fix the TypeScript errors in src/components/Header.astro
```

### Use the Right Command

- **`/dev`** → For all implementation (components, pages, features, fixes)
- **`/design`** → For complex system architecture (multi-collection systems, integrations)
- **`/lookup`** → For quick API reference (syntax, examples)

### Batch Related Work

```bash
# Good - batch related features
/dev Add blog with categories, tags, RSS feed, and pagination

# Less efficient - multiple separate requests
/dev Add blog collection
/dev Add categories to blog
/dev Add tags to blog
/dev Add RSS feed
/dev Add pagination
```

### Specify Constraints

```bash
/dev Add authentication (using Supabase, needs role-based access)
/dev Create dashboard (must match existing design system)
/dev Integrate API (rate limit 100 req/min, needs caching)
```

## Support

- **Issues**: [GitHub Issues](https://github.com/superbenefit/sb-marketplace/issues)
- **Email**: rathermercurial@protonmail.com
- **SuperBenefit**: info@superbenefit.org

## Contributing

Contributions welcome! Areas for improvement:

- Additional error patterns in error catalog
- More patterns in knowledge base
- Deep-dive references for advanced topics
- Documentation improvements
- Bug fixes

## License

CC0 1.0 Universal - Public Domain Dedication

This plugin is dedicated to the public domain. You can copy, modify, distribute and perform the work, even for commercial purposes, all without asking permission.

## Author

Created by rathermercurial.eth for the SuperBenefit community.

---

**Pro tip**: Start with `/dev` for everything. It's smart enough to handle simple to complex tasks automatically. Only use `/design` when you need explicit architecture planning first.
