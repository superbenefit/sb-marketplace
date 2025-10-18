---
name: docs-lookup
description: Quick Astro API documentation lookup
---

# Documentation Lookup

Fast API verification and documentation search for Astro/Starlight features.

## Usage

```bash
/docs-lookup [api-name or topic]
```

## Examples

```bash
/docs-lookup getStaticPaths
/docs-lookup content collections
/docs-lookup starlight config
/docs-lookup client directives
/docs-lookup image optimization
/docs-lookup markdown config
```

## What This Returns

For each lookup, you'll get:

### 1. Current Syntax
```typescript
// Latest API syntax with types
import { getCollection } from 'astro:content';

const posts = await getCollection('blog');
```

### 2. Usage Examples
```typescript
// Common usage patterns
const published = await getCollection('blog', ({ data }) => {
  return data.draft !== true;
});
```

### 3. Documentation Links
- Official Astro docs URL
- Related API references
- Migration guides (if applicable)

### 4. Common Patterns
- Best practices
- Performance tips
- Gotchas and pitfalls

## Common Lookups

### Content Collections API

```bash
/docs-lookup getCollection
```

Returns:
```typescript
import { getCollection, getEntry, getEntries } from 'astro:content';

// Get all entries
const allPosts = await getCollection('blog');

// Filter entries
const publishedPosts = await getCollection('blog', ({ data }) => {
  return !data.draft;
});

// Get single entry
const post = await getEntry('blog', 'post-slug');

// Get multiple entries
const posts = await getEntries([
  { collection: 'blog', id: 'post-1' },
  { collection: 'blog', id: 'post-2' },
]);
```

### Dynamic Routes

```bash
/docs-lookup getStaticPaths
```

Returns:
```typescript
export async function getStaticPaths() {
  const posts = await getCollection('blog');

  return posts.map(post => ({
    params: { slug: post.slug },
    props: { post },
  }));
}

// Access in component
const { post } = Astro.props;
```

### Starlight Configuration

```bash
/docs-lookup starlight config
```

Returns:
```javascript
import starlight from '@astrojs/starlight';

export default defineConfig({
  integrations: [
    starlight({
      title: 'My Docs',
      description: 'My awesome docs site',
      social: {
        github: 'https://github.com/user/repo',
      },
      sidebar: [
        {
          label: 'Start Here',
          items: [
            { label: 'Getting Started', link: '/getting-started/' },
          ],
        },
      ],
      customCss: ['./src/styles/custom.css'],
      locales: {
        root: { label: 'English', lang: 'en' },
        es: { label: 'Español', lang: 'es' },
      },
    }),
  ],
});
```

### Client Directives

```bash
/docs-lookup client directives
```

Returns:
```astro
<!-- Load on page load -->
<Component client:load />

<!-- Load when browser idle -->
<Component client:idle />

<!-- Load when visible -->
<Component client:visible />

<!-- Load when media query matches -->
<Component client:media="(max-width: 768px)" />

<!-- Only render on client -->
<Component client:only="react" />
```

### Image Optimization

```bash
/docs-lookup image
```

Returns:
```astro
---
import { Image } from 'astro:assets';
import myImage from '../assets/image.png';
---

<!-- Optimized image -->
<Image src={myImage} alt="Description" />

<!-- With specific dimensions -->
<Image src={myImage} alt="Description" width={600} height={400} />

<!-- Remote image -->
<Image
  src="https://example.com/image.jpg"
  alt="Description"
  width={600}
  height={400}
/>
```

## Integration

### With astro-developer Skill
- Verify APIs during implementation
- Check current syntax
- Get migration paths

### With astro-docs Skill
- Loads full documentation context
- Provides detailed explanations
- Searches comprehensive docs

### With MCP Server
If `astro-docs` MCP server is available:
- Real-time documentation
- Latest API updates
- Version-specific info

## Documentation Sources

### Cached References
Located at: `${CLAUDE_PLUGIN_ROOT}/skills/astro-docs/references/`
- Astro core API
- Starlight configuration
- Content Collections API
- Common patterns

### Knowledge Base
Located at: `${CLAUDE_PLUGIN_ROOT}/knowledge-base/`
- Syntax references
- Best practices
- Common mistakes
- Integration guides

### Official Docs
- https://docs.astro.build/
- https://starlight.astro.build/

## Lookup Categories

### Core APIs
- `getCollection`, `getEntry`, `getEntries`
- `getStaticPaths`
- `Astro` global
- `defineConfig`

### Integrations
- `@astrojs/starlight`
- `@astrojs/mdx`
- `@astrojs/sitemap`
- `@astrojs/tailwind`

### Features
- Content Collections
- Routing & Navigation
- Images & Assets
- Markdown & MDX
- TypeScript
- Styling

### Configuration
- `astro.config.mjs`
- TypeScript config
- Starlight options
- Build options

## Tips for Effective Lookups

1. **Be Specific**: Use exact API names when possible
2. **Use Keywords**: "content collections", "dynamic routes"
3. **Ask About**: Syntax, configuration, best practices
4. **Version Info**: Mention if you need version-specific docs

## Response Format

```markdown
# [API/Feature Name]

## Current Syntax
[Code example with TypeScript types]

## Common Usage
[Practical examples]

## Documentation
**Source**: https://docs.astro.build/...

## Related
- [Related API 1]
- [Related API 2]

## Notes
- Available since: vX.X.X
- Breaking changes: None
- Deprecations: None
```

## Quick Reference

### Most Common Lookups
1. `getCollection` - Content queries
2. `getStaticPaths` - Dynamic routes
3. `starlight config` - Starlight setup
4. `client directives` - Hydration
5. `Image` - Image optimization
6. `defineCollection` - Schema definition
7. `frontmatter` - Page/component data
8. `layouts` - Layout patterns

## When to Use

- ✅ Verifying API syntax before implementation
- ✅ Checking feature availability
- ✅ Finding correct import paths
- ✅ Understanding configuration options
- ✅ Getting migration information

## When to Use Full Docs Skill

For more complex needs:
- Deep dives into features
- Architecture decisions
- Multiple related APIs
- Comprehensive guides

Use `/docs-lookup` for quick checks, use the `astro-docs` skill for detailed research.
