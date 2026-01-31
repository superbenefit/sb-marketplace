# astro-dev

Astro and Starlight development toolkit for Claude Code with intelligent tiered knowledge loading.

Part of the [SuperBenefit Plugin Marketplace](https://github.com/superbenefit/sb-marketplace).

**Version**: 0.4.0

## Quick Start

```bash
# Main development command - handles everything
/dev Create a blog with categories and pagination

# Quick API reference lookup
/lookup getCollection

# Architecture planning for complex systems
/design Multi-tenant docs system with versioning
```

## Commands

### `/dev [description]`
Primary command for all development tasks - components, features, bug fixes, integrations. Automatically validates code based on task size.

```bash
/dev Add a Footer component with social links
/dev Create a blog with categories, tags, and pagination
/dev Fix all TypeScript errors in the components folder
/dev Add authentication --audit=comprehensive
```

### `/lookup [query]`
Quick API reference for Astro/Starlight APIs and syntax.

```bash
/lookup getCollection
/lookup client directives
/lookup starlight config
```

### `/design [system]`
Architecture planning for complex systems. Use before implementing large features.

```bash
/design Multi-language content system with versioning
/design Refactor 200 pages to content collections
```

## Skills

### astro-coding
Implementation knowledge loaded in three tiers:
- **Tier 1** (always): Critical rules that prevent build failures
- **Tier 2** (context-based): Relevant patterns for the current task
- **Tier 3** (on-demand): Deep-dive references for complex work

### astro-knowledge
API reference for documentation lookups via the `/lookup` command.

## Critical Rules

These rules are enforced on every task to prevent build failures:

1. **File extensions required**: `import Layout from './Layout.astro'` (not `'./Layout'`)
2. **Correct module prefix**: `'astro:content'` (not `'astro/content'`)
3. **Use `class` not `className`** in .astro files
4. **Await in frontmatter only**, never in templates
5. **Never expose `SECRET_*`** environment variables client-side
6. **Type all Props interfaces** with TypeScript
7. **Define `getStaticPaths()`** for dynamic routes
8. **Don't access `Astro.params`** inside `getStaticPaths()`
9. **Use `CollectionEntry<'name'>`** types for collections
10. **Validate XSS risk** with `set:html` (only use with trusted sources)

## Knowledge Base

```
knowledge-base/
├── critical-rules.md          # Tier 1: Always loaded
├── astro-patterns.md          # Tier 2: Core patterns
├── error-catalog.md           # Tier 2: 100+ errors indexed by symptom
├── starlight-guide.md         # Tier 2: Starlight-specific patterns
└── deep-dive/                 # Tier 3: On-demand
    ├── integrations.md
    ├── content-collections-reference.md
    ├── content-loader-api.md
    ├── external-data-integration.md
    ├── routing-pages-reference.md
    └── starlight-specific.md
```

## Installation

Add to your Claude Code settings (global `~/.claude/settings.json` or project `.claude/settings.local.json`):

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

## File Organization

```
astro-dev/
├── .claude-plugin/
│   └── plugin.json              # Plugin manifest
├── .mcp.json                    # Astro docs MCP server
├── commands/
│   ├── dev.md                   # Main development command
│   ├── design.md                # Architecture planning
│   └── lookup.md                # API lookup
├── skills/
│   ├── astro-coding/
│   │   ├── SKILL.md
│   │   └── references/
│   └── astro-knowledge/
│       ├── SKILL.md
│       └── references/
├── knowledge-base/              # Tiered reference content
├── hooks/
│   └── hooks.json
├── CHANGELOG.md
└── LICENSE
```

## Support

- **Issues**: [GitHub Issues](https://github.com/superbenefit/sb-marketplace/issues)
- **Email**: rathermercurial@protonmail.com
- **Community**: [SuperBenefit](https://superbenefit.org)

## License

CC0 1.0 Universal - Public Domain Dedication

Created by rathermercurial.eth for the SuperBenefit community.
