---
name: astro-knowledge
description: API documentation and reference provider for Astro/Starlight. Provides on-demand documentation lookup, API verification, and feature availability checks.
---

# astro-knowledge Skill

Expert documentation and API reference provider for Astro and Starlight development.

## Purpose

The astro-knowledge skill provides **on-demand documentation lookup** and API verification. It helps agents confirm current syntax, check feature availability, and access comprehensive API references.

## Capabilities

- **API Verification**: Confirm current syntax for Astro/Starlight APIs
- **Feature Lookup**: Check availability and usage patterns
- **Documentation Search**: Find relevant docs quickly
- **Best Practices**: Provide current recommendations
- **Version Checking**: Note version-specific features

## Loading Strategy

This skill loads **on-demand** when agents need:
- API syntax confirmation
- Feature availability verification
- Documentation references
- Configuration examples
- Migration guidance

## Usage

This skill is loaded when:
- Using the `/lookup` command for quick API reference
- During implementation via `/dev` for API verification
- When planning with `/design` for feature availability checks
- Whenever current syntax or API documentation is needed

## Documentation Resources

### Cached References
Location: `\${CLAUDE_PLUGIN_ROOT}/skills/astro-knowledge/references/`

- Full Astro API reference
- Starlight configuration guide
- Content Collections API
- Routing patterns

### Knowledge Base
Location: `\${CLAUDE_PLUGIN_ROOT}/knowledge-base/`

- Syntax details
- Common patterns
- Best practices

### MCP Server Integration
If `astro-docs` MCP server is available:
- Real-time documentation lookups
- Latest API information
- Version-specific documentation

## Common Lookups

### Collections API
\`\`\`typescript
// getCollection, getEntry, getEntries
import { getCollection, getEntry } from 'astro:content';

// Get all entries
const posts = await getCollection('blog');

// Get single entry
const post = await getEntry('blog', 'post-slug');

// Filter entries
const published = await getCollection('blog', ({ data }) => 
  data.draft !== true
);
\`\`\`

### Dynamic Routes
\`\`\`typescript
// getStaticPaths return format
export async function getStaticPaths() {
  const entries = await getCollection('docs');
  
  return entries.map(entry => ({
    params: { slug: entry.slug },
    props: { entry }
  }));
}
\`\`\`

### Client Directives
\`\`\`astro
<!-- Load immediately -->
<Component client:load />

<!-- Load when browser idle -->
<Component client:idle />

<!-- Load when visible -->
<Component client:visible />

<!-- Load when media query matches -->
<Component client:media="(max-width: 768px)" />

<!-- Only render on client -->
<Component client:only="react" />
\`\`\`

### Starlight Config
\`\`\`javascript
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  integrations: [
    starlight({
      title: 'My Docs',
      social: {
        github: 'https://github.com/user/repo',
      },
      sidebar: [
        {
          label: 'Guides',
          items: [
            { label: 'Getting Started', link: '/guides/getting-started/' },
          ],
        },
      ],
    })
  ]
});
\`\`\`

## Search Strategy

1. **Identify Section**: Determine relevant docs area
2. **Check Cache**: Look in cached references first
3. **MCP Fallback**: Use MCP server if available
4. **Provide Context**: Include examples and links

## Output Format

When providing documentation:

\`\`\`markdown
# [API Name]

## Current Syntax
[Code example]

## Documentation
Source: https://docs.astro.build/...

## Common Patterns
[Usage patterns]

## Notes
- Available since: vX.X.X
- Deprecations: [if any]
- Related: [Related APIs]
\`\`\`

## Token Optimization

**Quick lookup**: API signature + example (~100 tokens)
**Standard lookup**: Full documentation + patterns (~300 tokens)
**Comprehensive**: Multiple related APIs + guides (~600 tokens)

## Version

**Skill Version**: 2.0 (On-Demand Reference)
**Plugin Version**: v0.4.0+
**Last Updated**: 2025-11-05
