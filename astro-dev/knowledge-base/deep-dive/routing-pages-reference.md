# Astro Routing & Pages Reference

This document provides comprehensive reference for Astro's routing system, page generation, dynamic routes, and data passing patterns.

## File-Based Routing

Astro uses automatic file-based routing from `src/pages/` directory.

### Routing Basics

- Files in `src/pages/` automatically become routes
- No separate routing configuration needed
- Route URL corresponds to file path
- Supported formats: `.astro`, `.md`, `.mdx`

**Examples:**
```
src/pages/index.astro        → /
src/pages/about.astro        → /about
src/pages/about/index.astro  → /about
src/pages/about/me.astro     → /about/me
src/pages/posts/1.md         → /posts/1
```

**Documentation:** https://docs.astro.build/en/guides/routing/#static-routes

## Dynamic Routes

### Named Parameters

Use `[param]` syntax in filename to create dynamic routes.

**Structure:**
```
src/pages/
├── dogs/
│   └── [dog].astro          → /dogs/clifford, /dogs/rover, etc.
├── [lang]-[version]/
│   └── info.astro           → /en-v1/info, /es-v2/info, etc.
```

**Access parameters:**
```astro
---
const { dog } = Astro.params;  // From /dogs/[dog].astro
const { lang, version } = Astro.params;  // From /[lang]-[version]/info.astro
---
<h1>Dog: {dog}</h1>
```

### Rest Parameters (Catch-All)

Use `[...path]` for routes that match any depth.

**Structure:**
```
src/pages/sequences/[...path].astro

Matches:
/sequences/one
/sequences/one/two
/sequences/one/two/three
```

**Access:**
```astro
---
const { path } = Astro.params;  // 'one/two/three'
---
```

**Top-level match:**
```astro
---
export function getStaticPaths() {
  return [
    { params: { path: undefined } },  // Matches /sequences
    // Other paths...
  ];
}
---
```

**Documentation:** https://docs.astro.build/en/guides/routing/#dynamic-routes

## Route Priority Order

When multiple routes match, Astro uses this priority (highest to lowest):

1. **Reserved routes:** `_astro/`, `_server_islands/`, `_actions/`
2. **More path segments:** `/posts/create` > `/posts/[id]`
3. **Static routes:** `/posts/create` > `/posts/[id]`
4. **Named parameters:** `/posts/[id]` > `/posts/[...slug]`
5. **Pre-rendered dynamic:** Pre-rendered > server-rendered
6. **Endpoints:** Endpoints > pages
7. **File-based:** File routes > redirects
8. **Alphabetical:** As last resort

**Example:**
```
/posts/create.astro        # Priority 1: Most specific
/posts/[page].astro        # Priority 2: Named param
/posts/[...slug].astro     # Priority 3: Rest param
/[...slug].astro           # Priority 4: Catch-all
```

**Documentation:** https://docs.astro.build/en/guides/routing/#route-priority-order

## getStaticPaths() Function

Required for dynamic routes in static (SSG) mode.

### Basic Structure

```astro
---
export async function getStaticPaths() {
  return [
    { params: { dog: 'clifford' }},
    { params: { dog: 'rover' }},
    { params: { dog: 'spot' }},
  ];
}

const { dog } = Astro.params;
---
<h1>{dog}</h1>
```

**Requirements:**
- Must return array of objects
- Each object must have `params` property
- `params` values must be strings or numbers
- Can optionally include `props` property

**Documentation:** https://docs.astro.build/en/reference/routing-reference/#getstaticpaths

### Generating from Collections

```astro
---
import { getCollection, render } from 'astro:content';

export async function getStaticPaths() {
  const posts = await getCollection('blog');

  return posts.map(post => ({
    params: { slug: post.id },
    props: { post },
  }));
}

const { post } = Astro.props;
const { Content } = await render(post);
---

<article>
  <h1>{post.data.title}</h1>
  <Content />
</article>
```

**Key points:**
- Use `post.id` for URL parameter
- Pass entire entry as prop
- Use `render()` to get Content component

**Documentation:** https://docs.astro.build/en/guides/content-collections/#generating-routes-from-content

### With External Data

```astro
---
export async function getStaticPaths() {
  const response = await fetch('https://api.example.com/posts');
  const posts = await response.json();

  return posts.map((post) => ({
    params: { id: post.id.toString() },
    props: { post },
  }));
}

const { post } = Astro.props;
---

<h1>{post.title}</h1>
<p>{post.body}</p>
```

## Params vs Props Pattern

**Critical distinction:**

**Inside `getStaticPaths()`:**
- Fetch and process data
- Define route generation logic

**Outside `getStaticPaths()`:**
- Receive and use `params` and `props`
- Build page template

**Example:**
```astro
---
// INSIDE getStaticPaths() - fetch and return data
export async function getStaticPaths() {
  const posts = await getCollection('blog');

  return posts.map(post => ({
    params: { slug: post.slug },    // Used for URL
    props: { post }                  // Passed to template
  }));
}

// OUTSIDE getStaticPaths() - use data
const { slug } = Astro.params;      // From params
const { post } = Astro.props;       // From props
---
```

**Params:**
- Encoded in URL
- Must be strings/numbers
- Used for route generation

**Props:**
- Not in URL
- Any data type allowed
- Passed to template

**Documentation:** https://docs.astro.build/en/reference/routing-reference/#data-passing-with-props

## Pagination

### Built-in paginate() Function

Astro provides `paginate()` for easy pagination.

**Basic usage:**
```astro
---
export async function getStaticPaths({ paginate }) {
  const posts = await getCollection('blog');

  // Sort by date
  const sortedPosts = posts.sort(
    (a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf()
  );

  return paginate(sortedPosts, { pageSize: 10 });
}

const { page } = Astro.props;
---

<h1>Posts (Page {page.currentPage})</h1>

{page.data.map(post => (
  <article>
    <h2>{post.data.title}</h2>
  </article>
))}

<!-- Pagination controls -->
{page.url.prev && <a href={page.url.prev}>Previous</a>}
{page.url.next && <a href={page.url.next}>Next</a>}
```

**Generates:**
- `/posts/1`, `/posts/2`, `/posts/3`, etc.
- First page is always `/posts/1` (not `/posts`)

### Page Object Properties

```typescript
{
  data: T[];              // Current page's data slice
  start: number;          // First item index (0-based)
  end: number;            // Last item index (0-based)
  total: number;          // Total items across all pages
  currentPage: number;    // Current page number (1-based)
  size: number;           // Items per page
  lastPage: number;       // Total number of pages
  url: {
    current: string;      // Current page URL
    prev?: string;        // Previous page URL
    next?: string;        // Next page URL
    first?: string;       // First page URL
    last?: string;        // Last page URL
  };
}
```

### Nested Pagination

Combine pagination with other parameters.

**Example - Paginate by tag:**
```astro
---
export async function getStaticPaths({ paginate }) {
  const allPosts = await getCollection('blog');
  const uniqueTags = [...new Set(allPosts.flatMap(p => p.data.tags))];

  return uniqueTags.flatMap((tag) => {
    const filteredPosts = allPosts.filter(p => p.data.tags.includes(tag));

    return paginate(filteredPosts, {
      params: { tag },
      pageSize: 10
    });
  });
}

const { tag } = Astro.params;
const { page } = Astro.props;
---

<h1>Posts tagged "{tag}" (Page {page.currentPage})</h1>

{page.data.map(post => (
  <article>
    <h2>{post.data.title}</h2>
  </article>
))}
```

**Generates:**
- `/tags/astro/1`, `/tags/astro/2`
- `/tags/react/1`, `/tags/react/2`
- etc.

**Documentation:** https://docs.astro.build/en/guides/routing/#nested-pagination

## Data Fetching in Pages

### In getStaticPaths()

Fetch data for route generation:

```astro
---
export async function getStaticPaths() {
  // Runs at build time
  const response = await fetch('https://api.example.com/data');
  const items = await response.json();

  return items.map(item => ({
    params: { id: item.id },
    props: { item }
  }));
}

const { item } = Astro.props;
---
```

### Direct in Component

Fetch data outside getStaticPaths:

```astro
---
// Runs at build time (static) or request time (SSR)
const response = await fetch('https://api.example.com/settings');
const settings = await response.json();
---

<div>Settings: {JSON.stringify(settings)}</div>
```

### With Collections

```astro
---
import { getCollection } from 'astro:content';

const posts = await getCollection('blog', ({ data }) => {
  return data.draft !== true;
});

const sortedPosts = posts.sort(
  (a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf()
);
---

{sortedPosts.map(post => (
  <article>
    <h2>{post.data.title}</h2>
  </article>
))}
```

**Documentation:** https://docs.astro.build/en/guides/data-fetching/

## Frontmatter Access

### In Markdown/MDX Files

Frontmatter automatically parsed:

```markdown
---
title: "My Post"
date: 2024-01-15
tags: ["astro", "web"]
---

# Content
```

### In Collection Entries

```astro
---
import { getEntry } from 'astro:content';

const entry = await getEntry('blog', 'my-post');

// Access frontmatter via entry.data
const { title, date, tags } = entry.data;
---

<h1>{title}</h1>
<time>{date.toLocaleDateString()}</time>
```

### Modifying Programmatically

Via remark/rehype plugins:

```javascript
// remark plugin
export function customPlugin() {
  return function (tree, file) {
    file.data.astro.frontmatter.customField = 'Generated';
  }
}

// In astro.config.mjs
export default defineConfig({
  markdown: {
    remarkPlugins: [customPlugin]
  }
});
```

**Documentation:** https://docs.astro.build/en/guides/markdown-content/#modifying-frontmatter-programmatically

## Server-Side Rendering (SSR)

### Enable On-Demand Rendering

```javascript
// astro.config.mjs
import { defineConfig } from 'astro/config';
import node from '@astrojs/node';

export default defineConfig({
  output: 'server',  // or 'hybrid'
  adapter: node({ mode: 'standalone' })
});
```

### Per-Page Control

```astro
---
export const prerender = false;  // Render on demand

// Fetch fresh data on each request
const data = await fetch('https://api.example.com/live-data');
---
```

**Output modes:**
- `static` (default): All pages pre-rendered
- `server`: All pages on-demand (unless `prerender: true`)
- `hybrid`: Static by default (opt-in with `prerender: false`)

**Documentation:** https://docs.astro.build/en/guides/on-demand-rendering/

## Key Patterns Summary

1. **File-based routing:** Files in `src/pages/` = routes
2. **Dynamic routes:** Use `[param]` for variables, `[...path]` for catch-all
3. **Route priority:** Specific > static > named params > rest params
4. **getStaticPaths():** Required for dynamic routes in static mode
5. **Params vs Props:** Params in URL, props for additional data
6. **Pagination:** Use `paginate()` for built-in pagination
7. **Collections:** Use `getCollection()` in getStaticPaths()
8. **Data fetching:** In getStaticPaths or directly in component
9. **SSR:** Use adapters and `prerender` for on-demand rendering

## Documentation References

- **Routing Guide:** https://docs.astro.build/en/guides/routing/
- **Routing Reference:** https://docs.astro.build/en/reference/routing-reference/
- **Astro Pages:** https://docs.astro.build/en/basics/astro-pages/
- **Data Fetching:** https://docs.astro.build/en/guides/data-fetching/
- **On-Demand Rendering:** https://docs.astro.build/en/guides/on-demand-rendering/
- **Content Collections:** https://docs.astro.build/en/guides/content-collections/
