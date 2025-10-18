# Astro Development Knowledge Base

This knowledge base provides comprehensive reference material for Astro and Starlight development.

## Directory Structure

### `astro-syntax/`
Core Astro syntax references:
- `component-structure.md` - Astro component anatomy, frontmatter, templates
- `directives.md` - All client:*, is:*, set:* directives
- `imports.md` - Import patterns and file extension requirements
- `routing.md` - Dynamic routes, getStaticPaths patterns
- `configuration.md` - Astro and Starlight configuration options

### `common-mistakes/`
Cataloged errors and their fixes:
- `common-mistakes.md` - Frequently encountered errors and solutions

### `best-practices/`
Recommended patterns and approaches:
- `astro-best-practices.md` - General Astro development best practices
- `starlight-patterns.md` - Starlight-specific patterns
- `typescript-patterns.md` - TypeScript usage in Astro projects

### `architecture-patterns/`
System design and content organization:
- `content-collections-reference.md` - Content collections design patterns
- `routing-pages-reference.md` - Routing architecture

### `loader-examples/`
Custom loader implementations:
- `content-loader-api.md` - Loader API reference and examples

### `integration-guides/`
External system integration:
- `external-data-integration.md` - Integrating external data sources

### `starlight/`
Starlight-specific documentation:
- `starlight-specific.md` - Starlight features and configuration

### `audit/`
Code quality and audit checklists:
- `audit-checklist.md` - Comprehensive audit checklist
- `code-quality-standards.md` - Code quality standards

## Usage

These files are referenced by:
- **astro-developer** skill - For implementation guidance
- **astro-docs** skill - For documentation lookup
- **astro-auditor** agent - For code review
- **astro-architect** agent - For architecture planning

## Accessing Files

In skills and agents, use the `${CLAUDE_PLUGIN_ROOT}` variable:

```markdown
Access via `${CLAUDE_PLUGIN_ROOT}/knowledge-base/astro-syntax/directives.md`
```

## Maintenance

- Keep files updated with latest Astro versions
- Add new common mistakes as they're discovered
- Document team-specific patterns
- Cross-reference related topics
