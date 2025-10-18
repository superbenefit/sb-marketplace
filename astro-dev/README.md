# Astro Dev Plugin

Comprehensive Astro and Starlight development toolkit for Claude Code.

## Overview

This plugin provides expert assistance for Astro and Starlight development through skills, agents, commands, and automated workflows.

## Components

### Skills

#### `astro-developer`
Expert implementation skill for all Astro/Starlight code:
- Component development
- Dynamic routing with getStaticPaths
- Content collections
- Configuration management
- Bug fixes and debugging

**When it loads**: When implementing features, writing components, or fixing code.

#### `astro-docs`
Documentation specialist for quick API verification:
- API syntax lookup
- Feature availability checks
- Current best practices
- Documentation search

**When it loads**: When using `/docs-lookup` or needing API verification.

### Agents

#### `astro-auditor`
Comprehensive code auditor running in parallel:
- **Priority 1**: Build-breaking issues (missing extensions, wrong imports)
- **Priority 2**: Security, performance, common bugs
- **Priority 3**: Best practices and code quality

**When to use**: After implementations or via `/audit` command.

#### `astro-architect`
Content architecture specialist for complex planning:
- Collection structure design
- Custom loader architecture
- Multi-source content systems
- Routing strategy

**When to use**: When planning complex content architectures or integrations.

### Commands

#### `/implement [feature]`
Starts implementation with full context:
```bash
/implement Add blog pagination with TypeScript types
```

Loads best practices, syntax references, and enables auto-audit.

#### `/audit [path]`
Runs comprehensive code audit:
```bash
/audit src/pages/blog/
```

Returns prioritized report with fixes.

#### `/docs-lookup [api]`
Quick documentation lookup:
```bash
/docs-lookup getCollection
```

Returns syntax, examples, and documentation links.

### Hooks

#### PostToolUse: Auto-Audit
Automatically runs quick validation after editing Astro files:
- Checks common mistakes
- Validates imports
- Detects security issues
- Non-blocking execution

#### PreToolUse: Audit Notification
Notifies before implementing in Astro files.

### Scripts

#### `audit-runner.sh`
Automated validation script that checks:
- `astro:content` vs `astro/content`
- `class` vs `className`
- Missing file extensions
- `Astro.params` in getStaticPaths
- Template `await` usage
- Exposed environment variables

## Knowledge Base

Comprehensive reference materials organized by category:

### `astro-syntax/`
- Component structure
- Directives reference
- Import patterns
- Routing patterns
- Configuration options

### `common-mistakes/`
- Cataloged errors and fixes
- Why they happen
- How to prevent them

### `best-practices/`
- Astro development patterns
- Starlight-specific guidance
- TypeScript patterns
- Performance optimization

### `architecture-patterns/`
- Content collections design
- Routing architecture
- System organization

### `loader-examples/`
- Custom loader implementations
- API integration patterns

### `integration-guides/`
- External data sources
- CMS integration
- Multi-source systems

### `starlight/`
- Starlight configuration
- Theme customization
- Plugin integration

### `audit/`
- Audit checklists
- Quality standards
- Code review guidelines

## Usage Patterns

### Basic Implementation

```bash
/implement Create a dynamic route for documentation pages
```

Claude will:
1. Load astro-developer skill
2. Check project structure
3. Review best practices
4. Implement the feature
5. Auto-audit the code
6. Report any issues

### Complex Architecture

```
I need to integrate content from GitBook and local MDX files into a unified documentation site with versioning
```

Claude will:
1. Invoke astro-architect agent
2. Design collection structure
3. Plan loader architecture
4. Create implementation roadmap
5. Provide code templates

### API Verification

```bash
/docs-lookup getStaticPaths
```

Returns:
- Current syntax with types
- Common usage patterns
- Documentation link
- Related APIs

### Code Audit

```bash
/audit
```

Get comprehensive report:
- Critical issues requiring fixes
- Performance improvements
- Best practice suggestions
- Positive patterns observed

## Critical Rules

The plugin enforces these critical Astro rules:

### ✅ DO
- Include file extensions in imports: `import Layout from './Layout.astro'`
- Use `astro:content` for content collections
- Use `class` not `className` in Astro components
- Fetch data in frontmatter, not templates
- Sort collections when order matters
- Type all component Props

### ❌ DON'T
- Access `Astro.params` inside `getStaticPaths()`
- Use `await` in template sections
- Expose server secrets to client
- Over-hydrate static content
- Use `className` in Astro components

## Progressive Context Loading

The plugin uses progressive disclosure to optimize context:

1. **Metadata** (~100 tokens): Skill descriptions always loaded
2. **Skill Body** (<5k tokens): Loaded when skill is triggered
3. **Resources** (unlimited): Loaded on-demand from knowledge base

This ensures efficient context usage while maintaining comprehensive capabilities.

## Integration with MCP

If you have the `astro-docs` MCP server installed, the plugin integrates for:
- Real-time documentation lookups
- Latest API information
- Version-specific docs

The skill provides cached fallback when MCP is unavailable.

## File Organization

```
astro-dev/
├── .claude-plugin/
│   └── plugin.json              # Manifest
├── skills/
│   ├── astro-developer/
│   │   ├── SKILL.md            # Skill definition
│   │   └── references/         # Quick references
│   └── astro-docs/
│       ├── SKILL.md            # Skill definition
│       └── references/         # Cached docs
├── agents/
│   ├── astro-auditor.md        # Auditor agent
│   └── astro-architect.md      # Architect agent
├── commands/
│   ├── implement.md            # /implement command
│   ├── audit.md                # /audit command
│   └── docs-lookup.md          # /docs-lookup command
├── hooks/
│   └── hooks.json              # Hook configuration
├── scripts/
│   └── audit-runner.sh         # Audit automation
└── knowledge-base/
    ├── astro-syntax/           # Syntax refs
    ├── common-mistakes/        # Error catalog
    ├── best-practices/         # Patterns
    ├── architecture-patterns/  # Design refs
    ├── loader-examples/        # Loader code
    ├── integration-guides/     # Integration docs
    ├── starlight/              # Starlight refs
    └── audit/                  # Audit guides
```

## Troubleshooting

### Plugin Not Loading

1. Check `.claude/settings.json` has correct marketplace path
2. Verify plugin is enabled in settings
3. Restart Claude Code

### Hooks Not Working

1. Ensure `audit-runner.sh` is executable: `chmod +x scripts/audit-runner.sh`
2. Check hook configuration in `hooks/hooks.json`
3. Verify bash is available in PATH

### Skills Not Triggering

1. Skills load on-demand when relevant
2. Use commands to explicitly trigger: `/implement`, `/docs-lookup`
3. Check skill names match plugin manifest

## Version

Current version: 1.0.0

See CHANGELOG.md for version history and updates.

## License

CC0 1.0 Universal - Public Domain Dedication

This plugin is dedicated to the public domain. You can copy, modify, distribute and perform the work, even for commercial purposes, all without asking permission.

## Author

Created by rathremercurial.eth for the SuperBenefit community.

## Contributing

Contributions welcome! Areas for improvement:
- Additional knowledge base content
- New skills and agents
- Enhanced audit checks
- Better documentation
- Bug fixes and optimizations

## Support

- Email: rathermercurial@protonmail.com
- SuperBenefit: info@superbenefit.org
