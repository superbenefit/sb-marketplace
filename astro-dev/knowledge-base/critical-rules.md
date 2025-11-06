# Astro/Starlight Critical Rules

**Always load this file** - These are the non-negotiable rules that prevent breaking errors in Astro and Starlight projects.

---

## 1. File Extensions in Imports ✅

**ALWAYS include file extensions** in all imports.

```typescript
// ✅ CORRECT
import Header from './Header.astro';
import { formatDate } from '../utils/dates.ts';
import Button from '../../components/Button.astro';

// ❌ WRONG - Will cause build errors
import Header from './Header';
import { formatDate } from '../utils/dates';
import Button from '../../components/Button';
```

**Why**: Astro requires explicit file extensions for ESM module resolution. Omitting them causes build failures.

**Error if violated**: `Cannot find module './Header'` or `Module not found`

---

## 2. Correct Module Prefixes ✅

Use `astro:content` (with colon), NOT `astro/content` (with slash).

```typescript
// ✅ CORRECT - Use colon
import { defineCollection, z } from 'astro:content';
import { getCollection, getEntry } from 'astro:content';
import type { CollectionEntry } from 'astro:content';

// ❌ WRONG - Will cause errors
import { defineCollection } from 'astro/content';
import { getCollection } from 'astro/content';
```

**Why**: Astro's built-in modules use the `astro:` prefix protocol, not path-style imports.

**Error if violated**: `Cannot resolve 'astro/content'` or module not found

**Other correct module prefixes**:
- `astro:assets` (not `astro/assets`)
- `astro:transitions` (not `astro/transitions`)
- `astro:middleware` (not `astro/middleware`)

---

## 3. Use `class` NOT `className` ✅

In `.astro` files, use the `class` attribute, not `className`.

```astro
<!-- ✅ CORRECT -->
<div class="container">
  <h1 class="title">Hello</h1>
</div>

<!-- ❌ WRONG - This is React/JSX syntax -->
<div className="container">
  <h1 className="title">Hello</h1>
</div>
```

**Why**: Astro uses standard HTML syntax. `className` is JSX/React syntax and won't work in `.astro` files.

**Exception**: Inside React/Preact/Solid components, use `className` as normal.

---

## 4. Async Operations in Frontmatter Only ✅

**ALWAYS `await` async calls in the frontmatter** (the `---` section), NEVER in the template.

```astro
---
// ✅ CORRECT - Await in frontmatter
import { getCollection } from 'astro:content';
const posts = await getCollection('blog');
const published = posts.filter(p => !p.data.draft);
---

<ul>
  {published.map(post => (
    <li>{post.data.title}</li>
  ))}
</ul>
```

```astro
<!-- ❌ WRONG - Async in template -->
<ul>
  {(await getCollection('blog')).map(post => (
    <li>{post.data.title}</li>
  ))}
</ul>
```

**Why**: Astro templates render synchronously. All async operations must complete before template rendering.

**Error if violated**: `await is not allowed in this context` or runtime errors

---

## 5. Never Expose Secrets Client-Side ✅

**NEVER expose environment variables starting with `SECRET_`** to client-side code.

```astro
---
// ✅ CORRECT - Server-side only (frontmatter)
const apiKey = import.meta.env.SECRET_API_KEY;
const response = await fetch('https://api.example.com', {
  headers: { 'Authorization': `Bearer ${apiKey}` }
});
const data = await response.json();
---

<div>{data.title}</div>
```

```astro
---
// ❌ WRONG - Never in script tags
---

<script>
  // This exposes the secret to the browser!
  const apiKey = import.meta.env.SECRET_API_KEY; // ❌ NEVER DO THIS
  fetch('https://api.example.com', {
    headers: { 'Authorization': `Bearer ${apiKey}` }
  });
</script>
```

**Rule**:
- Variables prefixed with `PUBLIC_` → Accessible everywhere (including client)
- Variables prefixed with `SECRET_` or no prefix → Server-side ONLY
- Use API routes (`src/pages/api/`) for client-server communication

**Security risk if violated**: API keys, tokens, and credentials exposed in browser

---

## 6. Type All Component Props ✅

**ALWAYS define a TypeScript `Props` interface** for components with props.

```astro
---
// ✅ CORRECT - Typed Props interface
interface Props {
  title: string;
  items: string[];
  variant?: 'primary' | 'secondary';
  count?: number;
}

const { title, items, variant = 'primary', count } = Astro.props;
---

<div class={`card card--${variant}`}>
  <h2>{title}</h2>
  {count && <span>({count})</span>}
  <ul>
    {items.map(item => <li>{item}</li>)}
  </ul>
</div>
```

```astro
---
// ❌ WRONG - No types (loses type safety)
const { title, items, variant = 'primary' } = Astro.props;
---
```

**Why**: TypeScript provides compile-time safety, catches bugs early, and enables IDE autocomplete.

**Benefits**:
- Compile-time type checking
- IDE autocomplete and IntelliSense
- Catches prop mismatches before runtime
- Self-documenting components

---

## 7. Define `getStaticPaths()` for Dynamic Routes ✅

**ALWAYS export `getStaticPaths()`** in dynamic route files (those with `[param]` in the name).

```astro
---
// File: src/pages/blog/[slug].astro

// ✅ CORRECT - getStaticPaths defined
import { getCollection } from 'astro:content';
import type { CollectionEntry } from 'astro:content';

export async function getStaticPaths() {
  const posts = await getCollection('blog');
  return posts.map(post => ({
    params: { slug: post.slug },
    props: { post },
  }));
}

interface Props {
  post: CollectionEntry<'blog'>;
}

const { post } = Astro.props;
---

<h1>{post.data.title}</h1>
```

**Why**: Astro needs to know what pages to generate at build time for static site generation.

**Error if violated**: `getStaticPaths() is required for dynamic routes` or empty pages

---

## 8. Don't Access `Astro.params` Inside `getStaticPaths()` ✅

`Astro.params` is NOT available inside `getStaticPaths()`.

```typescript
// ❌ WRONG - Astro.params doesn't exist here
export async function getStaticPaths() {
  const slug = Astro.params.slug; // ❌ This will error!
  return [...];
}

// ✅ CORRECT - params is in the generated object
export async function getStaticPaths() {
  const posts = await getCollection('blog');
  return posts.map(post => ({
    params: { slug: post.slug }, // ✅ Define params here
    props: { post },
  }));
}

// Then access later in the component body
const { slug } = Astro.params; // ✅ This works
const { post } = Astro.props;  // ✅ This works
```

**Why**: `getStaticPaths()` runs before any specific page context exists. It's the function that *defines* what params will exist.

---

## 9. Use Proper Collection Types ✅

When working with content collections, use proper TypeScript types.

```typescript
// ✅ CORRECT - Proper types
import type { CollectionEntry } from 'astro:content';

interface Props {
  post: CollectionEntry<'blog'>;
  author: CollectionEntry<'authors'>;
}

const { post, author } = Astro.props;

// Type-safe access
const title: string = post.data.title;
const date: Date = post.data.publishDate;
```

**Available types from `astro:content`**:
- `CollectionEntry<'collectionName'>` - A single collection entry
- `CollectionKey` - Union of all collection names
- `ContentCollectionKey` - Union of content-type collections
- `DataCollectionKey` - Union of data-type collections

---

## 10. Validate XSS Risk with `set:html` ✅

**NEVER use `set:html` with user-generated or unsanitized content**.

```astro
---
const userComment = "<script>alert('XSS')</script>"; // Malicious input
const safeHTML = "<p>This is safe HTML from your CMS</p>"; // Trusted source
---

<!-- ❌ DANGEROUS - XSS vulnerability -->
<div set:html={userComment} />

<!-- ✅ SAFE - Regular interpolation escapes HTML -->
<div>{userComment}</div>
<!-- Output: &lt;script&gt;alert('XSS')&lt;/script&gt; -->

<!-- ✅ ACCEPTABLE - Trusted HTML from your backend/CMS -->
<div set:html={safeHTML} />
```

**Why**: `set:html` bypasses HTML escaping, allowing arbitrary HTML/JavaScript execution.

**Safe uses**:
- Content from your own CMS (trusted source)
- Markdown rendered to HTML by your build process
- Sanitized HTML from libraries like `sanitize-html`

**Never use with**:
- User comments or form inputs
- URL parameters
- Any untrusted external data

---

## Quick Validation Checklist

Before submitting code, verify:

- [ ] All imports have file extensions (`.astro`, `.ts`, `.js`)
- [ ] Using `astro:content` not `astro/content`
- [ ] Using `class` not `className` in .astro files
- [ ] All `await` calls are in frontmatter, not templates
- [ ] No `SECRET_*` variables in `<script>` tags
- [ ] All component Props have TypeScript interfaces
- [ ] Dynamic routes have `getStaticPaths()` defined
- [ ] Not accessing `Astro.params` inside `getStaticPaths()`
- [ ] Collection entries use `CollectionEntry<'name'>` type
- [ ] No `set:html` with user-generated content

---

## Error Messages → Solutions

| Error Message | Likely Cause | Solution |
|--------------|--------------|----------|
| `Cannot find module './Component'` | Missing file extension | Add `.astro` or `.ts` extension |
| `Module 'astro/content' not found` | Wrong module prefix | Change to `astro:content` (colon) |
| `await is not allowed in this context` | Await in template | Move await to frontmatter |
| `getStaticPaths is required` | Missing function in dynamic route | Add `export async function getStaticPaths()` |
| `Astro is not defined` | Wrong context for Astro.params | Check you're not in `getStaticPaths()` |
| `Property 'data' does not exist` | Wrong collection type | Use `CollectionEntry<'name'>` |

---

**Load this file for all Astro/Starlight tasks** - violations of these rules cause build failures or security vulnerabilities.
