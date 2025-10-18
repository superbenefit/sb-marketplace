# Astro Routing Reference

**Source**: https://docs.astro.build/en/reference/routing-reference/

This document provides authoritative rules for Astro's file-based routing system.

## File-Based Routing

### Basic Routing

Files in `src/pages/` automatically become routes:

```
src/pages/
├── index.astro                    → /
├── about.astro                    → /about/
├── blog.astro                     → /blog/
└── contact.astro                  → /contact/
```

**Supported file extensions**:
- `.astro`
- `.md`
- `.mdx`
- `.html`

### Nested Routing

Directories create nested routes:

```
src/pages/
├── index.astro                    → /
└── blog/
    ├── index.astro               → /blog/
    ├── post-1.astro              → /blog/post-1/
    └── post-2.astro              → /blog/post-2/
```

## Dynamic Routes

### Single Parameter

Use `[param]` syntax for dynamic segments:

```
src/pages/
└── blog/
    └── [slug].astro              → /blog/anything/
```

**Access parameter**:
```astro
---
const { slug } = Astro.params;
---
```

### Rest Parameters (Catch-all)

Use `[...param]` syntax to match multiple segments:

```
src/pages/
└── blog/
    └── [...path].astro           → /blog/a/b/c/d/
```

**Access parameter**:
```astro
---
const { path } = Astro.params;  // "a/b/c/d"
---
```

### Optional Parameters (v4.4+)

Use `[[param]]` syntax for optional segments:

```
src/pages/
└── shop/
    └── [[category]]/
        └── [id].astro            → /shop/123/ or /shop/electronics/123/
```

### Rest Parameter Restrictions

⚠️ **IMPORTANT**: Only ONE rest parameter per route

✅ **CORRECT**:
```
src/pages/
└── [locale]/
    └── [...slug].astro           → /en/docs/guide/
```

❌ **INCORRECT**: Multiple rest parameters
```
src/pages/
└── [...a]/
    └── [...b].astro              ❌ NOT ALLOWED
```

## getStaticPaths()

### Purpose

In static mode (`output: 'static'`), dynamic routes MUST export `getStaticPaths()` to generate all possible route paths at build time.

### Basic Pattern

```astro
---
export async function getStaticPaths() {
  return [
    { params: { slug: 'post-1' } },
    { params: { slug: 'post-2' } },
    { params: { slug: 'post-3' } },
  ];
}

const { slug } = Astro.params;
---
```

### Required Return Format

Must return **array of objects** with `params` property:

✅ **CORRECT**:
```typescript
export async function getStaticPaths() {
  return [
    { params: { slug: 'post-1' } },
    { params: { slug: 'post-2' } }
  ];
}
```

❌ **INCORRECT**: Wrong format
```typescript
export async function getStaticPaths() {
  return ['post-1', 'post-2'];  // ❌ Wrong: must be objects with params
}
```

❌ **INCORRECT**: params not an object
```typescript
export async function getStaticPaths() {
  return [
    { params: 'post-1' }  // ❌ Wrong: params must be object
  ];
}
```

### With Props

Pass additional data via `props`:

```astro
---
import { getCollection } from 'astro:content';

export async function getStaticPaths() {
  const posts = await getCollection('blog');

  return posts.map(post => ({
    params: { slug: post.id },
    props: { post },  // Pass full post data
  }));
}

// Access via Astro.props, NOT Astro.params
const { post } = Astro.props;
---

<h1>{post.data.title}</h1>
```

### Param Value Types

**Valid param types**:
- `string`
- `number`
- `undefined` (for rest parameters only)

**Invalid param types**:
- ❌ Objects
- ❌ Arrays
- ❌ Booleans
- ❌ Functions

✅ **CORRECT**:
```typescript
return [
  { params: { id: '123' } },      // string ✅
  { params: { page: 1 } },        // number ✅
  { params: { path: undefined } } // undefined for rest ✅
];
```

❌ **INCORRECT**:
```typescript
return [
  { params: { data: { id: 1 } } },     // object ❌
  { params: { tags: ['a', 'b'] } },    // array ❌
  { params: { active: true } },        // boolean ❌
];
```

### Scope Isolation

`getStaticPaths()` must be **isolated** - no access to parent scope variables:

❌ **INCORRECT**: Accessing closure variables
```astro
---
const siteUrl = 'https://example.com';  // Parent scope

export async function getStaticPaths() {
  console.log(siteUrl);  // ❌ ERROR: Not accessible
  return [];
}
---
```

✅ **CORRECT**: Self-contained function
```astro
---
export async function getStaticPaths() {
  const siteUrl = 'https://example.com';  // Defined in function
  console.log(siteUrl);  // ✅ OK
  return [];
}
---
```

### Common Patterns

**From content collection**:
```typescript
export async function getStaticPaths() {
  const posts = await getCollection('blog');
  return posts.map(post => ({
    params: { slug: post.id },
    props: { post }
  }));
}
```

**From API**:
```typescript
export async function getStaticPaths() {
  const response = await fetch('https://api.example.com/posts');
  const posts = await response.json();

  return posts.map(post => ({
    params: { id: post.id.toString() },
    props: { post }
  }));
}
```

**With pagination**:
```typescript
export async function getStaticPaths({ paginate }) {
  const posts = await getCollection('blog');
  return paginate(posts, { pageSize: 10 });
}

const { page } = Astro.props;
```

## SSR Mode (`output: 'server'`)

### Differences from Static

In SSR mode, `getStaticPaths()` is **NOT required**:

```astro
---
// src/pages/blog/[slug].astro

// No getStaticPaths needed in SSR mode!
const { slug } = Astro.params;
const post = await getEntry('blog', slug);
---
```

### Prerendering in SSR

To statically generate specific routes in SSR mode:

```astro
---
export const prerender = true;

export async function getStaticPaths() {
  return [
    { params: { slug: 'about' } },
    { params: { slug: 'contact' } }
  ];
}
---
```

### Rest Parameter Limitation

Same as static mode: only ONE rest parameter allowed:

❌ **INCORRECT**: Multiple rest params (even in SSR)
```
src/pages/
└── [...a]/
    └── [...b].astro              ❌ NOT ALLOWED
```

## Page Exclusion

### Underscore Prefix

Files/directories starting with `_` are **NOT routed**:

```
src/pages/
├── index.astro                    → / (routed)
├── _helper.astro                  → NOT routed
├── _components/
│   └── Header.astro              → NOT routed
└── blog/
    ├── [slug].astro              → /blog/:slug/ (routed)
    └── _draft.astro              → NOT routed
```

**Use cases**:
- Helper components
- Partial templates
- Internal utilities
- Draft content

## Priority Order

When multiple routes could match, Astro uses this priority:

1. **Static routes** (highest priority)
2. **Dynamic routes with single param**
3. **Rest parameters** (catch-all, lowest priority)

**Example**:
```
src/pages/
├── blog/featured.astro           Priority 1 → /blog/featured/
├── blog/[slug].astro             Priority 2 → /blog/anything/
└── blog/[...path].astro          Priority 3 → /blog/a/b/c/
```

Request to `/blog/featured/` → Routes to `featured.astro` (static wins)

## Validation Checklist

### File Structure
- [ ] Files are in `src/pages/` directory
- [ ] File extensions are `.astro`, `.md`, `.mdx`, or `.html`
- [ ] Dynamic segments use `[param]` syntax
- [ ] Rest parameters use `[...param]` syntax
- [ ] Only ONE rest parameter per route

### getStaticPaths() (Static Mode)
- [ ] Exported for all dynamic routes
- [ ] Returns array of objects
- [ ] Each object has `params` property
- [ ] `params` is an object, not primitive
- [ ] Param values are string, number, or undefined only
- [ ] No closure variable access (function is isolated)
- [ ] Props passed via `props` property, not `params`

### getStaticPaths() (SSR Mode)
- [ ] NOT required unless using `prerender = true`
- [ ] If using `prerender`, follows static mode rules

### Parameters
- [ ] Accessed via `Astro.params`
- [ ] NOT accessed inside `getStaticPaths()`
- [ ] Type validated before use

### Page Exclusion
- [ ] Helper/component files prefixed with `_`
- [ ] Internal utilities not accidentally routed

## Common Routing Errors

| Error | Example | Fix |
|-------|---------|-----|
| Missing getStaticPaths | `[slug].astro` without export | Add `export async function getStaticPaths()` |
| Wrong return format | `return ['a', 'b']` | `return [{params: {x: 'a'}}, {params: {x: 'b'}}]` |
| params not object | `{params: 'value'}` | `{params: {key: 'value'}}` |
| Invalid param type | `{params: {x: true}}` | `{params: {x: 'true'}}` (string) |
| Multiple rest params | `[...a]/[...b].astro` | Use only one rest param |
| Accessing Astro.params in getStaticPaths | `Astro.params.slug` | Only access in component frontmatter |
| Closure access | Using parent variables | Define all data inside function |
| Props in params | `{params: {post: obj}}` | `{params: {id}, props: {post: obj}}` |

## Advanced Patterns

### Multiple Dynamic Segments

```
src/pages/
└── [lang]/
    └── [category]/
        └── [product].astro       → /en/electronics/laptop/
```

```typescript
export async function getStaticPaths() {
  return [
    { params: { lang: 'en', category: 'electronics', product: 'laptop' } },
    { params: { lang: 'es', category: 'electronica', product: 'laptop' } }
  ];
}
```

### Optional with Required

```
src/pages/
└── [[lang]]/
    └── [product].astro           → /laptop/ or /en/laptop/
```

### Nested Rest

```
src/pages/
└── docs/
    └── [...slug].astro           → /docs/guide/intro/
```

```astro
---
const { slug } = Astro.params;  // "guide/intro"
const parts = slug.split('/');  // ["guide", "intro"]
---
```

## URL Construction

When building links to dynamic routes:

```astro
---
const posts = await getCollection('blog');
---

{posts.map(post => (
  <a href={`/blog/${post.id}/`}>
    {post.data.title}
  </a>
))}
```

**Remember trailing slash** based on `trailingSlash` config:
- `'always'`: `/blog/post-1/`
- `'never'`: `/blog/post-1`
- `'ignore'`: Either works

## Performance Considerations

### Static Generation

For large datasets, consider filtering in `getStaticPaths()`:

```typescript
export async function getStaticPaths() {
  const allPosts = await getCollection('blog');

  // Only generate published posts
  const publishedPosts = allPosts.filter(post => !post.data.draft);

  return publishedPosts.map(post => ({
    params: { slug: post.id },
    props: { post }
  }));
}
```

### Pagination

Use `paginate()` for large lists:

```typescript
export async function getStaticPaths({ paginate }) {
  const posts = await getCollection('blog');
  return paginate(posts, { pageSize: 10 });
}
```

Creates routes: `/blog/1/`, `/blog/2/`, etc.
