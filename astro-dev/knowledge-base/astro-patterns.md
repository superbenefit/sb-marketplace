# Astro Development Patterns

**Comprehensive patterns for components, routing, collections, configuration, and directives.**

## Component Structure

### File Structure

Every `.astro` file has two required sections:

```astro
---
// SECTION 1: Component frontmatter (server-side JavaScript/TypeScript)
import Layout from '../layouts/Layout.astro';
const title = "Hello";
---

<!-- SECTION 2: Component template (HTML + expressions) -->
<h1>{title}</h1>
```

**Frontmatter capabilities**:
- Import statements
- Variable declarations
- Data fetching with `await`
- Function definitions
- Type definitions

**Template features**:
- Multiple root elements allowed
- JSX-like expressions in `{}`
- HTML attribute names (kebab-case), NOT JSX (camelCase)

---

### Props Pattern

```astro
---
import type { CollectionEntry } from 'astro:content';

interface Props {
  post: CollectionEntry<'blog'>;
  showDate?: boolean;
}

const { post, showDate = true } = Astro.props;
---

<article>
  <h1>{post.data.title}</h1>
  {showDate && <time>{post.data.pubDate.toLocaleDateString()}</time>}
</article>
```

**Best practices**:
- Always define Props interface
- Use TypeScript types for type safety
- Provide defaults for optional props
- Access props via `Astro.props`

---

### Slots Pattern

```astro
<!-- Layout.astro -->
---
const { title } = Astro.props;
const hasHeader = Astro.slots.has('header');
---

<html>
  <head><title>{title}</title></head>
  <body>
    {hasHeader && (
      <header>
        <slot name="header" />
      </header>
    )}

    <main>
      <slot />  <!-- Default slot -->
    </main>

    <footer>
      <slot name="footer">
        <!-- Fallback content if no footer provided -->
        <p>&copy; 2024</p>
      </slot>
    </footer>
  </body>
</html>
```

**Usage**:
```astro
<Layout title="My Page">
  <div slot="header">
    <nav>...</nav>
  </div>

  <!-- Default slot content -->
  <p>Main content here</p>

  <div slot="footer">
    <p>Custom footer</p>
  </div>
</Layout>
```

---

## Import Patterns

### Component Imports

```typescript
// Astro components
import Header from '../components/Header.astro';
import Footer from './Footer.astro';

// Framework components
import ReactCounter from '../components/Counter.jsx';
import VueWidget from '../components/Widget.vue';

// Built-in Astro modules (use astro: prefix)
import { getCollection, getEntry, render } from 'astro:content';
import { Image } from 'astro:assets';
import { SECRET_KEY } from 'astro:env/server';
import { PUBLIC_API_URL } from 'astro:env/client';
```

**Critical rules**:
1. Always include file extensions for relative imports
2. Use `astro:` prefix (not `astro/`) for built-ins
3. Use `import type` for TypeScript types

---

### Glob Imports

```typescript
// All markdown files (pattern must be string literal)
const posts = import.meta.glob('../posts/*.md');

// Eager loading
const posts = import.meta.glob('../posts/*.md', { eager: true });

// Multiple extensions
const content = import.meta.glob('../content/**/*.{md,mdx}');

// ❌ WRONG - variable pattern
const pattern = '../posts/*.md';
const files = import.meta.glob(pattern);  // Error!

// ✅ CORRECT - patterns must start with ./ or ../
const files = import.meta.glob('./posts/*.md');
```

---

## Routing Patterns

### Static Routes

```
src/pages/
├── index.astro                → /
├── about.astro                → /about/
└── blog/
    ├── index.astro           → /blog/
    └── post-1.astro          → /blog/post-1/
```

---

### Dynamic Routes with getStaticPaths()

```astro
---
// src/pages/blog/[slug].astro
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

**Key points**:
- Required for dynamic routes in static mode
- Return array of objects with `params` property
- Pass data via `props`, not `params`
- Can't access `Astro.params` inside getStaticPaths

---

### Rest Parameters (Catch-all)

```astro
---
// src/pages/docs/[...slug].astro
export async function getStaticPaths() {
  const docs = await getCollection('docs');

  return docs.map(doc => ({
    params: { slug: doc.id },
    props: { doc }
  }));
}

const { slug } = Astro.params;  // e.g., "guide/intro/getting-started"
const parts = slug.split('/');   // ["guide", "intro", "getting-started"]
---
```

**Matches**:
- `/docs/guide`
- `/docs/guide/intro`
- `/docs/guide/intro/getting-started`

**Restrictions**: Only ONE rest parameter per route

---

### Pagination

```astro
---
// src/pages/blog/[page].astro
export async function getStaticPaths({ paginate }) {
  const posts = await getCollection('blog');

  const sortedPosts = posts.sort(
    (a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf()
  );

  return paginate(sortedPosts, { pageSize: 10 });
}

const { page } = Astro.props;
---

<h1>Posts (Page {page.currentPage} of {page.lastPage})</h1>

{page.data.map(post => (
  <article>
    <h2>{post.data.title}</h2>
  </article>
))}

<nav>
  {page.url.prev && <a href={page.url.prev}>← Previous</a>}
  {page.url.next && <a href={page.url.next}>Next →</a>}
</nav>
```

**Generates**: `/blog/1/`, `/blog/2/`, `/blog/3/`, etc.

---

## Content Collections

### Collection Definition

```typescript
// src/content.config.ts
import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/data/blog" }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    tags: z.array(z.string()),
    draft: z.boolean().default(false),
  })
});

export const collections = { blog };
```

---

### Query Patterns

```typescript
// Get all entries (with filtering and sorting)
const posts = (await getCollection('blog', ({ data }) => {
  return import.meta.env.PROD ? data.draft !== true : true;
})).sort(
  (a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf()
);

// Get single entry (with null check)
const post = await getEntry('blog', Astro.params.slug);

if (!post) {
  return Astro.redirect('/404');
}

// Render markdown content
const { Content, headings } = await render(post);
```

---

### Cross-Collection References

```typescript
import { defineCollection, z, reference } from 'astro:content';

const blog = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/data/blog" }),
  schema: z.object({
    title: z.string(),
    author: reference('authors'),
    relatedPosts: z.array(reference('blog')).optional(),
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

**Usage**:
```typescript
const post = await getEntry('blog', 'my-post');
const author = await getEntry(post.data.author);
const related = await getEntries(post.data.relatedPosts || []);
```

---

## Hydration Directives

### Client Directive Selection

```astro
<!-- Immediate hydration (critical, above-fold) -->
<InteractiveWidget client:load />

<!-- When browser idle (important but not critical) -->
<ChatWidget client:idle />

<!-- When in viewport (below fold, heavy) -->
<HeavyChart client:visible />

<!-- Based on media query (responsive) -->
<MobileMenu client:media="(max-width: 768px)" />

<!-- Client-only rendering (breaks during SSR) -->
<BrowserOnlyWidget client:only="react" />
```

**Decision tree**:
1. Is it interactive? → If no, don't hydrate
2. Needs immediate interaction? → `client:load`
3. Important but can wait? → `client:idle`
4. Below the fold? → `client:visible`
5. Only for certain screen sizes? → `client:media`
6. Breaks during SSR? → `client:only`

---

### Script Directives

```astro
---
const color = 'red';
const size = 16;
---

<!-- Pass server variables to client script -->
<script define:vars={{ color, size }}>
  console.log(color);  // Accessible in script
</script>

<!-- Pass server variables to CSS -->
<style define:vars={{ color, size }}>
  h1 {
    color: var(--color);
    font-size: calc(var(--size) * 1px);
  }
</style>

<!-- Inline script (not bundled, runs every time) -->
<script is:inline>
  console.log('Inline script');
  // ❌ import statements won't work here
</script>

<!-- Global styles (disable scoping) -->
<style is:global>
  body a { color: red; }
</style>
```

---

## Configuration Patterns

### Basic Config

```typescript
// astro.config.mjs
import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  site: 'https://example.com',
  output: 'static',  // or 'server'

  integrations: [
    react(),
    tailwind(),
  ],

  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'es', 'fr'],
  },
});
```

---

### Environment Variables (Type-Safe)

```typescript
// astro.config.mjs
import { defineConfig, envField } from 'astro/config';

export default defineConfig({
  env: {
    schema: {
      PUBLIC_API_URL: envField.string({
        context: 'client',
        access: 'public'
      }),
      SECRET_API_KEY: envField.string({
        context: 'server',
        access: 'secret'
      }),
    }
  }
});
```

**Usage**:
```typescript
import { PUBLIC_API_URL } from 'astro:env/client';
import { SECRET_API_KEY } from 'astro:env/server';
```

---

### SSR Configuration

```typescript
import { defineConfig } from 'astro/config';
import node from '@astrojs/node';

export default defineConfig({
  output: 'server',  // or 'hybrid'
  adapter: node({ mode: 'standalone' }),
});
```

**Per-page control**:
```astro
---
export const prerender = false;  // Render on demand

const data = await fetch('https://api.example.com/live-data');
---
```

---

## Data Fetching Patterns

### In Frontmatter

```astro
---
import { getCollection } from 'astro:content';

// Runs at build time (or request time in SSR)
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

---

### External API

```astro
---
let data = null;
let error = null;

try {
  const response = await fetch('https://api.example.com/data');
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  data = await response.json();
} catch (e) {
  error = e.message;
}
---

{error && <div class="error">Error: {error}</div>}
{data && <div>{JSON.stringify(data)}</div>}
```

---

## Image Optimization

### Local Images

```astro
---
import { Image } from 'astro:assets';
import myImage from '../assets/photo.jpg';
---

<Image src={myImage} alt="Description" width={800} height={600} />
```

---

### Remote Images

```astro
---
import { Image } from 'astro:assets';
---

<Image
  src="https://example.com/image.jpg"
  alt="Remote image"
  width={800}
  height={600}
  loading="lazy"
/>
```

**Requirements for remote images**:
- Must provide `width` and `height`
- Optional: `loading="lazy"` for below-fold images

---

## Common Utility Patterns

### class:list Directive

```astro
---
const isActive = true;
const type = 'primary';
---

<!-- Array -->
<div class:list={['base', type, { active: isActive }]} />
<!-- Result: class="base primary active" -->

<!-- Object -->
<div class:list={{ active: isActive, hidden: false }} />
<!-- Result: class="active" -->

<!-- Mixed -->
<div class:list={['base', { active: isActive }, ['extra']]} />
```

---

### Dynamic Tags

```astro
---
const Heading = 'h1';  // Must be CAPITALIZED
const Element = 'div';
---

<Element>Content</Element>  <!-- Renders as <div> -->
<Heading>Title</Heading>    <!-- Renders as <h1> -->
```

**Restrictions**:
- ❌ Cannot use `client:*` directives
- ❌ Cannot use `define:vars`
- ✅ Can use regular HTML attributes

---

### Fragments

```astro
<!-- Short syntax -->
<>
  <h1>Title</h1>
  <p>Paragraph</p>
</>

<!-- Named syntax -->
<Fragment>
  <h1>Title</h1>
  <p>Paragraph</p>
</Fragment>

<!-- With directive -->
<Fragment set:html={htmlString} />
```

---

## TypeScript Patterns

### Type Imports

```typescript
import type { CollectionEntry } from 'astro:content';
import type { ImageMetadata } from 'astro';

interface Props {
  post: CollectionEntry<'blog'>;
  image: ImageMetadata;
}
```

**Benefits**:
- Removed at build time
- Better tree-shaking
- Clear intent

---

### Type-Safe Components

```astro
---
import type { CollectionEntry } from 'astro:content';

interface Props {
  post: CollectionEntry<'blog'>;
  showDate?: boolean;
}

const { post, showDate = true } = Astro.props;
---

<article>
  <h1>{post.data.title}</h1>
  {showDate && <time>{post.data.pubDate.toLocaleDateString()}</time>}
</article>
```

---

## Performance Patterns

### Code Splitting

```astro
---
// Dynamic import for heavy components
const HeavyChart = (await import('../components/HeavyChart.jsx')).default;
---

<HeavyChart client:visible />
```

---

### Specific Imports

```typescript
// ❌ Imports entire library
import _ from 'lodash';

// ✅ Only what you need
import debounce from 'lodash/debounce';
```

---

### Scoped CSS

```astro
<div class="container">
  <h1>Title</h1>
</div>

<style>
  /* Automatically scoped to this component */
  .container {
    padding: 1rem;
  }

  h1 {
    color: blue;
  }

  /* Global styles when needed */
  :global(body) {
    font-family: system-ui;
  }
</style>
```

---

## Middleware Pattern

```typescript
// src/middleware.ts
import { defineMiddleware } from 'astro:middleware';

export const onRequest = defineMiddleware(async (context, next) => {
  // Add custom logic before route
  console.log('Request:', context.url.pathname);

  // Continue to route
  const response = await next();

  // Modify response if needed
  return response;
});
```

---

## Key Patterns Summary

**Component Structure**:
- Two sections: frontmatter (---) + template
- Type props with interface
- Use slots for composition

**Imports**:
- File extensions required for relative imports
- `astro:` prefix for built-ins
- `import type` for TypeScript types

**Routing**:
- File-based from `src/pages/`
- `getStaticPaths()` for dynamic routes
- `paginate()` for pagination

**Collections**:
- Define schema for validation
- Always sort if order matters
- Use `render()` for markdown

**Hydration**:
- Only hydrate interactive components
- Choose appropriate `client:*` directive
- Default is server-rendered (fastest)

**Data Fetching**:
- In frontmatter, not templates
- Error handling with try/catch
- Filter and sort at query time

**Performance**:
- Use Image component
- Code split heavy components
- Specific imports over whole libraries
