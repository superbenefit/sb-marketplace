# Astro Development Knowledge Base

**Consolidated reference for Astro and Starlight development patterns, errors, and best practices.**

## Quick Navigation

### [Error Catalog](./error-catalog.md)
**When**: Something's broken and you need a fix NOW.

Common issues indexed by symptom:
- Import errors (missing extensions, wrong prefix)
- Component hydration problems
- getStaticPaths() errors
- Props handling mistakes
- Content collection issues
- Template errors
- Starlight-specific problems
- Environment variable errors
- Image handling
- Build & configuration errors

**Quick lookup**: Search by error message or symptom.

---

### [Astro Patterns](./astro-patterns.md)
**When**: Building features and need implementation patterns.

Comprehensive patterns for:
- **Component Structure** - Props, slots, frontmatter
- **Import Patterns** - Components, modules, glob imports
- **Routing** - Static, dynamic, rest parameters, pagination
- **Content Collections** - Definition, queries, references
- **Hydration Directives** - When to use each client:* directive
- **Configuration** - Basic, env vars, SSR
- **Data Fetching** - Frontmatter, external APIs
- **Image Optimization** - Local and remote images
- **TypeScript** - Type imports, type-safe components

**Best for**: Learning patterns, implementing features, understanding architecture.

---

### [Starlight Guide](./starlight-guide.md)
**When**: Building documentation sites with Starlight.

Complete Starlight reference:
- **Project Setup** - Configuration, content setup
- **Page Types** - Standard docs, splash pages, custom pages
- **Frontmatter** - Required and optional fields
- **Sidebar** - Auto-generated, manual, mixed configurations
- **Built-in Components** - Tabs, Cards, Asides, Code blocks
- **Component Overrides** - Customizing Starlight components
- **Route Data** - Accessing starlightRoute
- **Internationalization** - Multi-language setup
- **Styling** - CSS variables, custom styles
- **Search** - Configuration and customization

**Best for**: Documentation sites, Starlight-specific features.

---

### [Integrations](./integrations.md)
**When**: Integrating external data sources or custom loaders.

External integrations and TypeScript patterns:
- **Content Loaders** - Inline vs object loaders
- **Authentication** - Type-safe environment variables
- **Error Handling** - Retries, rate limiting
- **Incremental Updates** - Change detection with digest
- **Data Transformation** - Type-safe transformations
- **Built-in Loaders** - glob() and file() loaders
- **Image Handling** - Remote images, asset downloads
- **TypeScript Best Practices** - Type safety, utility types
- **Caching** - Metadata and HTTP caching strategies

**Best for**: External APIs, custom data sources, advanced TypeScript.

---

## Common Lookup Paths

### "My build is failing..."
1. Check [Error Catalog](./error-catalog.md) for the specific error
2. Look for import, routing, or collection issues
3. Verify configuration in [Astro Patterns](./astro-patterns.md)

### "How do I..."
- **Create dynamic routes?** → [Astro Patterns - Routing](./astro-patterns.md#routing-patterns)
- **Fetch external data?** → [Integrations - Content Loaders](./integrations.md#content-loader-fundamentals)
- **Build a doc site?** → [Starlight Guide](./starlight-guide.md)
- **Optimize images?** → [Astro Patterns - Image Optimization](./astro-patterns.md#image-optimization)
- **Type components?** → [Astro Patterns - TypeScript](./astro-patterns.md#typescript-patterns)

### "Something isn't working..."
- **Component not interactive?** → [Error Catalog - Hydration](./error-catalog.md#component--hydration-errors)
- **Collection not found?** → [Error Catalog - Collections](./error-catalog.md#content-collection-errors)
- **Import failing?** → [Error Catalog - Imports](./error-catalog.md#import-errors)
- **Starlight issue?** → [Error Catalog - Starlight](./error-catalog.md#starlight-specific-errors)

### "I want to learn..."
- **Astro fundamentals?** → [Astro Patterns](./astro-patterns.md)
- **Starlight features?** → [Starlight Guide](./starlight-guide.md)
- **Advanced integrations?** → [Integrations](./integrations.md)
- **TypeScript patterns?** → [Integrations - TypeScript](./integrations.md#typescript-best-practices)

---

## File Organization

**Before consolidation**: 17 files, ~2500 lines, ~8000 tokens
**After consolidation**: 5 files, ~1500 lines, ~4000 tokens

**Eliminated**:
- 30-40% redundant content across files
- Duplicate error patterns
- Repeated syntax references
- Overlapping best practices

**Preserved**:
- All unique error patterns
- All implementation patterns
- All configuration examples
- All critical references

---

## Usage Tips

**For quick fixes**: Start with [Error Catalog](./error-catalog.md) and search by symptom.

**For learning**: Read [Astro Patterns](./astro-patterns.md) section by section.

**For Starlight projects**: Keep [Starlight Guide](./starlight-guide.md) open as reference.

**For integrations**: Check [Integrations](./integrations.md) for external data patterns.

**Cross-referencing**: Each file references related content in other files.

---

## What's New in Consolidated Version

**Improvements**:
- Single source of truth for each pattern
- Error catalog indexed by symptom for faster lookup
- Cross-referenced content instead of duplication
- Clearer organization by use case
- 50% token reduction when loaded

**Coverage**:
- Complete error catalog with quick fixes
- All Astro patterns (components, routing, collections, config)
- Full Starlight guide (setup, pages, components, customization)
- External integrations (loaders, auth, TypeScript)
- TypeScript best practices integrated where relevant

---

## Quick Reference Cards

### Critical Import Rules
```typescript
// ✅ File extensions required
import Layout from '../layouts/Layout.astro';

// ✅ Use astro: prefix for built-ins
import { getCollection } from 'astro:content';

// ✅ Type-only imports
import type { CollectionEntry } from 'astro:content';
```

### Dynamic Route Pattern
```astro
---
export async function getStaticPaths() {
  const posts = await getCollection('blog');
  return posts.map(post => ({
    params: { slug: post.id },
    props: { post }
  }));
}
const { post } = Astro.props;
---
```

### Collection Query Pattern
```typescript
const posts = (await getCollection('blog', ({ data }) => {
  return data.draft !== true;
})).sort(
  (a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf()
);
```

### Starlight Setup
```typescript
// src/content.config.ts
import { docsLoader } from '@astrojs/starlight/loaders';
import { docsSchema } from '@astrojs/starlight/schema';

export const collections = {
  docs: defineCollection({
    loader: docsLoader(),
    schema: docsSchema(),
  }),
};
```

---

## Contributing

When adding new content:
1. Check if pattern already exists (avoid duplication)
2. Add to appropriate file based on topic
3. Cross-reference related content
4. Keep examples concise and practical
5. Index errors by symptom in error-catalog.md
