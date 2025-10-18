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

## Documentation Resources

### Documentation Index
**Location**: `${CLAUDE_PLUGIN_ROOT}/knowledge-base/astro-syntax/`

Comprehensive references for Astro documentation sections for targeted searches.

### Cached Documentation
**Location**: `${CLAUDE_PLUGIN_ROOT}/skills/astro-docs/references/`

- Full Astro API reference
- Starlight configuration guide
- Content Collections API
- Routing patterns

## Search Strategy

1. **Identify Section**: Check knowledge base for relevant section
2. **Target Search**: Use specific terms from section titles
3. **Verify Currency**: Cross-reference with latest docs if needed
4. **Provide Context**: Include URLs and examples

## Common Lookups

### Collections API
```typescript
// Verify with: getCollection, getEntry, getEntries
import { getCollection, getEntry } from 'astro:content';

// Get all entries from a collection
const posts = await getCollection('blog');

// Get a single entry
const post = await getEntry('blog', 'post-slug');

// Filter entries
const published = await getCollection('blog', ({ data }) => {
  return data.draft !== true;
});
```

### Dynamic Routes
```typescript
// Check: getStaticPaths return format
export async function getStaticPaths() {
  const entries = await getCollection('docs');

  return entries.map(entry => ({
    params: {
      slug: entry.slug  // only string|number|undefined
    },
    props: {
      entry  // any data
    }
  }));
}
```

### Starlight Config
```javascript
// Verify: starlight() integration options
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
```

### Client Directives
```astro
<!-- client:load - Load immediately -->
<Component client:load />

<!-- client:idle - Load when browser idle -->
<Component client:idle />

<!-- client:visible - Load when visible in viewport -->
<Component client:visible />

<!-- client:media - Load when media query matches -->
<Component client:media="(max-width: 768px)" />

<!-- client:only - Only render on client -->
<Component client:only="react" />
```

## Integration with Development

When verifying APIs:
1. Check cached references first
2. Note version-specific features
3. Provide migration paths if applicable
4. Include example usage
5. Link to official documentation

## Output Format

When providing documentation:
- Include source URL
- Show current syntax
- Note any deprecations
- Provide working example
- Mention version requirements

## Example Response Format

```markdown
# [API Name]

## Current Syntax
[Code example]

## Documentation
Source: https://docs.astro.build/...

## Common Patterns
[Usage patterns]

## Notes
- Available since: vX.X.X
- Deprecations: None
- Related: [Related APIs]
```

## Working with MCP Server

If the `astro-docs` MCP server is available, use it for:
- Real-time documentation lookups
- Latest API information
- Version-specific documentation

Use this skill for:
- Quick reference from cached docs
- Common patterns and examples
- Integration with development workflow
