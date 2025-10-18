# Claude Code Configuration

This directory contains specialized sub-agents and knowledge bases for developing this Astro/Starlight documentation site.

## Directory Structure

```
.claude/
├── agents/                    # Sub-agent definitions
│   ├── astro-docs-specialist.md
│   ├── astro-content-specialist.md
│   ├── astro-content-specialist-guide.md
│   └── astro-developer.md
├── astro-docs/               # Astro documentation reference
│   ├── astro-sitemap.md
│   ├── llms.txt
│   └── llms-full.md
├── content-knowledge/        # Content architecture reference
│   ├── content-collections-reference.md
│   ├── content-loader-api.md
│   ├── routing-pages-reference.md
│   ├── starlight-specific.md
│   └── external-data-integration.md
├── developer-knowledge/      # Implementation best practices
│   ├── astro-best-practices.md
│   ├── common-mistakes.md
│   └── starlight-patterns.md
└── README.md                 # This file
```

## Sub-Agents

### astro-docs-specialist
**Model**: haiku-4.5
**Purpose**: Documentation research and API verification
**When to use**: Looking up Astro/Starlight APIs, verifying syntax, finding documentation

### astro-content-specialist
**Model**: sonnet
**Purpose**: Content architecture and planning
**When to use**: Designing content collections, planning loaders, architecting routing

### astro-developer
**Model**: sonnet
**Purpose**: Code implementation
**When to use**: Writing code, fixing bugs, making changes

## Usage Protocol

Follow this workflow for best results:

1. **Architecture** → Use `astro-content-specialist` to design the solution
2. **Verify** → Use `astro-docs-specialist` to confirm current APIs
3. **Implement** → Use `astro-developer` to write the code

See `../CLAUDE.md` for detailed usage examples and guidelines.

## Knowledge Bases

### Astro Documentation (`astro-docs/`)
- Complete Astro framework documentation
- 345 documentation sections indexed
- Used by astro-docs-specialist for MCP searches

### Content Knowledge (`content-knowledge/`)
- Content collections architecture
- Content Loader API reference
- Routing and pages patterns
- Starlight-specific features
- External data integration patterns

### Developer Knowledge (`developer-knowledge/`)
- Best practices for Astro development
- Common mistakes and how to avoid them
- Starlight-specific implementation patterns

## For Developers

When working on this project:

1. **Read CLAUDE.md first** - It contains the sub-agent usage protocols
2. **Use the right agent** - Don't skip the workflow steps
3. **Consult knowledge bases** - They prevent common mistakes
4. **Verify APIs** - Use astro-docs-specialist for current syntax

The sub-agent system is designed to produce error-free code by following established patterns and avoiding documented pitfalls.
