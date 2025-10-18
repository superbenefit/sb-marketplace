# Astro Content Collections Reference

This document provides comprehensive reference for Astro's Content Collections system, including architecture, configuration, schema definition, and query patterns.

## Architecture Overview

Content Collections provide type-safe, validated access to structured content in Astro projects. They use:
- **Zod schemas** for validation and TypeScript type generation
- **Content Loader API** for flexible data sourcing
- **Type-safe queries** via `getCollection()`, `getEntry()`, and `getEntries()`

## Configuration

### File: `src/content.config.ts`

**Required structure:**
1. Import utilities from `astro:content`
2. Import loaders from `astro/loaders`
3. Define collections using `defineCollection()`
4. Export single `collections` object

**Example:**
```typescript
import { defineCollection, z } from 'astro:content';
import { glob, file } from 'astro/loaders';

const blog = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/data/blog" }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    tags: z.array(z.string()),
  })
});

export const collections = { blog };
```

**Documentation:** https://docs.astro.build/en/guides/content-collections/#defining-collections

## Schema Definition with Zod

### Basic Schema

All frontmatter properties must be defined using Zod data types:

```typescript
schema: z.object({
  // Required fields
  title: z.string(),

  // Optional fields
  description: z.string().optional(),
  draft: z.boolean().default(false),

  // Type coercion
  pubDate: z.coerce.date(),

  // Collections
  tags: z.array(z.string()),

  // Enums
  category: z.enum(['tutorial', 'guide', 'reference']),

  // Validation
  email: z.string().email(),
  url: z.string().url(),
})
```

### Cross-Collection References

Use `reference()` function for relationships between collections:

```typescript
import { defineCollection, z, reference } from 'astro:content';

const blog = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/data/blog" }),
  schema: z.object({
    title: z.string(),
    author: reference('authors'),  // Reference to authors collection
    relatedPosts: z.array(reference('blog')).optional(),  // Self-reference
  })
});

const authors = defineCollection({
  loader: file("src/data/authors.json"),
  schema: z.object({
    name: z.string(),
    bio: z.string(),
  })
});

export const collections = { blog, authors };
```

**Querying references:**
```typescript
import { getEntry, getEntries } from 'astro:content';

const post = await getEntry('blog', 'my-post');
const author = await getEntry(post.data.author);  // Fetch referenced author
const related = await getEntries(post.data.relatedPosts || []);  // Fetch related posts
```

**Documentation:** https://docs.astro.build/en/guides/content-collections/#defining-collection-references

### TypeScript Integration

**Requirements:**
- TypeScript with `strictNullChecks: true` and `allowJs: true`
- Or use `astro/tsconfigs/strict` or `strictest`

**Benefits:**
- Automatic TypeScript type generation from schemas
- Full IntelliSense and autocompletion
- Type-safe collection queries
- Property validation at compile time

**JSON Schemas:**
- Auto-generated in `.astro/collections/` directory
- One schema file per collection
- Usable in VS Code with `$schema` field

**Documentation:** https://docs.astro.build/en/guides/content-collections/#typescript-configuration-for-collections

## Collection Query and Access Patterns

### `getCollection()` - Fetch All Entries

**Basic usage:**
```typescript
import { getCollection } from 'astro:content';

const allBlogPosts = await getCollection('blog');
```

**With filtering:**
```typescript
// Filter by property
const publishedPosts = await getCollection('blog', ({ data }) => {
  return data.draft !== true;
});

// Filter by ID/path
const englishDocs = await getCollection('docs', ({ id }) => {
  return id.startsWith('en/');
});

// Environment-based filtering
const posts = await getCollection('blog', ({ data }) => {
  return import.meta.env.PROD ? data.draft !== true : true;
});
```

**Sorting (required for deterministic order):**
```typescript
const posts = (await getCollection('blog')).sort(
  (a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf()
);
```

**Return type:** `CollectionEntry<'blog'>[]`

**Documentation:** https://docs.astro.build/en/reference/modules/astro-content/#getcollection

### `getEntry()` - Fetch Single Entry

**Usage:**
```typescript
import { getEntry } from 'astro:content';

const post = await getEntry('blog', 'my-post-slug');

if (!post) {
  return Astro.redirect('/404');
}

// Access data
const { title, description } = post.data;
```

**Return type:** `CollectionEntry<'blog'> | undefined`

**Documentation:** https://docs.astro.build/en/reference/modules/astro-content/#getentry

### `getEntries()` - Fetch Multiple Specific Entries

**Usage:**
```typescript
import { getEntries, getEntry } from 'astro:content';

const post = await getEntry('blog', 'my-post');

// Get all related posts
const relatedPosts = await getEntries(post.data.relatedPosts);
```

**Documentation:** https://docs.astro.build/en/reference/modules/astro-content/#getentries

## Rendering Content

### Using `render()` Function

```typescript
import { getEntry, render } from 'astro:content';

const entry = await getEntry('blog', 'post-1');
const { Content, headings } = await render(entry);
```

**Returns:**
- `Content`: Astro component for rendering HTML
- `headings`: Array of rendered headings with `depth`, `slug`, `text`

**In templates:**
```astro
---
import { getEntry, render } from 'astro:content';

const entry = await getEntry('blog', 'post-1');
const { Content, headings } = await render(entry);
---

<article>
  <h1>{entry.data.title}</h1>
  <Content />

  <aside>
    <h2>Table of Contents</h2>
    <ul>
      {headings.map(h => (
        <li>
          <a href={`#${h.slug}`}>{h.text}</a>
        </li>
      ))}
    </ul>
  </aside>
</article>
```

**Documentation:** https://docs.astro.build/en/guides/content-collections/#rendering-body-content

## CollectionEntry Type

```typescript
import type { CollectionEntry } from 'astro:content';

interface Props {
  post: CollectionEntry<'blog'>;
}

const { post } = Astro.props;

// Access properties:
// - post.id: Entry ID
// - post.slug: Optional slug
// - post.data: Validated frontmatter (typed by schema)
// - post.body: Raw markdown content
// - post.collection: Collection name
```

## Key Patterns Summary

1. **Define collections** in `src/content.config.ts` with loaders and schemas
2. **Use Zod** for all schema validation and type safety
3. **Query collections** with `getCollection()`, `getEntry()`, `getEntries()`
4. **Always sort** results if order matters (non-deterministic by default)
5. **Filter at query time** for drafts, locales, categories
6. **Reference other collections** using `reference()` function
7. **Render content** using `render()` for markdown/MDX
8. **Type components** with `CollectionEntry<'collection'>` for props

## Documentation References

- **Content Collections Guide:** https://docs.astro.build/en/guides/content-collections/
- **Content Collection APIs:** https://docs.astro.build/en/reference/content-collection-apis/
- **astro:content Module:** https://docs.astro.build/en/reference/modules/astro-content/
- **Content Layer API:** https://docs.astro.build/en/reference/content-layer-reference/
