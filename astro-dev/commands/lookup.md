---
name: lookup
description: Quick API documentation and reference lookup for Astro/Starlight
---

# /lookup Command

Fast API verification and documentation search using the astro-knowledge skill.

## Usage

```bash
/lookup [api-name or topic]
```

## Description

The `/lookup` command provides quick access to Astro and Starlight API documentation, syntax examples, and best practices via the astro-knowledge skill.

## Examples

```bash
/lookup getStaticPaths
/lookup content collections
/lookup starlight config
/lookup client directives
/lookup image optimization
/lookup defineCollection
```

## What You Get

### 1. Current Syntax
```typescript
// Latest API syntax with TypeScript types
import { getCollection } from 'astro:content';

const posts = await getCollection('blog');
```

### 2. Usage Examples
```typescript
// Common patterns
const published = await getCollection('blog', ({ data }) => {
  return data.draft !== true;
});
```

### 3. Documentation Links
- Official Astro docs URL
- Related API references
- Migration guides (if applicable)

### 4. Best Practices
- Performance tips
- Common pitfalls
- Security considerations

## Common Lookups

### Content Collections
```bash
/lookup getCollection
```

**Returns**:
```typescript
import { getCollection, getEntry, getEntries } from 'astro:content';

// Get all entries
const allPosts = await getCollection('blog');

// Filter entries
const publishedPosts = await getCollection('blog', ({ data }) => 
  !data.draft
);

// Get single entry
const post = await getEntry('blog', 'post-slug');
```

### Dynamic Routes
```bash
/lookup getStaticPaths
```

**Returns**:
```typescript
export async function getStaticPaths() {
  const posts = await getCollection('blog');
  
  return posts.map(post => ({
    params: { slug: post.slug },
    props: { post },
  }));
}

const { post } = Astro.props;
```

### Client Directives
```bash
/lookup client directives
```

**Returns**:
```astro
<!-- Load on page load -->
<Component client:load />

<!-- Load when browser idle -->
<Component client:idle />

<!-- Load when visible -->
<Component client:visible />

<!-- Conditional load -->
<Component client:media="(max-width: 768px)" />

<!-- Client-only render -->
<Component client:only="react" />
```

### Starlight Config
```bash
/lookup starlight config
```

**Returns**:
```javascript
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
            { label: 'Getting Started', link: '/guides/start/' },
          ],
        },
      ],
    }),
  ],
});
```

### Image Optimization
```bash
/lookup image
```

**Returns**:
```astro
---
import { Image } from 'astro:assets';
import myImage from '../assets/image.png';
---

<!-- Optimized local image -->
<Image src={myImage} alt="Description" />

<!-- With dimensions -->
<Image src={myImage} alt="Description" width={600} height={400} />

<!-- Remote image -->
<Image 
  src="https://example.com/image.jpg" 
  alt="Description"
  width={600} 
  height={400} 
/>
```

## Lookup Categories

### Core APIs
- Content Collections (`getCollection`, `getEntry`, `getEntries`)
- Dynamic Routes (`getStaticPaths`)
- Astro Global (`Astro.props`, `Astro.params`)
- Configuration (`defineConfig`)

### Integrations
- `@astrojs/starlight`
- `@astrojs/mdx`
- `@astrojs/sitemap`
- `@astrojs/tailwind`

### Features
- Content Collections
- Routing & Pages
- Images & Assets
- Markdown & MDX
- Client Directives
- TypeScript

## Integration

### With astro-knowledge Skill
- Loads cached documentation
- Provides quick reference
- Uses MCP server if available

### With astro-developer Agent
- Verify APIs during implementation
- Check current syntax
- Get code examples

### MCP Server Integration
If `astro-docs` MCP server is available:
- Real-time latest docs
- Version-specific information
- Always up-to-date

## Documentation Sources

**Cached References**:
`${CLAUDE_PLUGIN_ROOT}/skills/astro-knowledge/references/`

**Knowledge Base**:
`${CLAUDE_PLUGIN_ROOT}/knowledge-base/`

**Official Docs**:
- https://docs.astro.build/
- https://starlight.astro.build/

## Response Format

```markdown
# [API/Feature Name]

## Current Syntax
[Code example with types]

## Common Usage
[Practical examples]

## Documentation
Source: https://docs.astro.build/...

## Notes
- Available since: vX.X.X
- Deprecations: [if any]
- Related: [Related APIs]
```

## Tips

**Be Specific**:
```
❌ /lookup routing
✅ /lookup getStaticPaths
```

**Use Keywords**:
```
✅ /lookup content collections
✅ /lookup client hydration
✅ /lookup markdown config
```

**Ask About Versions**:
```
✅ /lookup getCollection (Astro 4.x)
```

## When to Use

Use `/lookup` for:
- ✅ Quick syntax verification
- ✅ API availability checks
- ✅ Import path confirmation
- ✅ Configuration options
- ✅ Fast reference during coding

Use `/architect` for:
- System design decisions
- Architecture planning
- Complex integrations

## Most Common Lookups

1. `getCollection` - Content queries
2. `getStaticPaths` - Dynamic routes  
3. `starlight config` - Starlight setup
4. `client directives` - Hydration
5. `Image` - Image optimization
6. `defineCollection` - Schema definition

## Version

**Command Version**: 2.0
**Compatible with**: astro-dev plugin v2.0+
**Last Updated**: 2025-10-18

Use `/lookup` for fast, accurate API reference.
