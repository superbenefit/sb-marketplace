# Astro Development Best Practices

This document provides best practices for developing with Astro and Starlight, based on official documentation and common patterns.

## Import Patterns

### Correct Import Syntax

**DO**: Use proper import statements for Astro components
```astro
---
import Layout from '../layouts/Layout.astro';
import { getCollection } from 'astro:content';
import { Image } from 'astro:assets';
---
```

**DON'T**: Use require() or incorrect paths
```javascript
// ❌ Wrong - require not supported
const Layout = require('../layouts/Layout.astro');

// ❌ Wrong - missing file extension
import Layout from '../layouts/Layout';
```

### Astro Built-in Modules

Always use the `astro:` prefix for built-in modules:

```typescript
import { getCollection, getEntry, render } from 'astro:content';
import { Image } from 'astro:assets';
import type { APIRoute } from 'astro';
```

### Component Imports

**Astro components** (`.astro` files):
```astro
import Header from '../components/Header.astro';
import Footer from './Footer.astro';
```

**Framework components** (React, Vue, etc.):
```astro
import ReactComponent from '../components/ReactComponent.jsx';
import VueComponent from '../components/VueComponent.vue';
```

## Component Hydration

### Client Directives

Use client directives sparingly and appropriately:

**`client:load`** - Hydrate immediately on page load
```astro
<InteractiveWidget client:load />
```
**Use when**: Component needs to be interactive immediately

**`client:idle`** - Hydrate when browser is idle
```astro
<ChatWidget client:idle />
```
**Use when**: Component is important but not immediately needed

**`client:visible`** - Hydrate when component enters viewport
```astro
<HeavyChart client:visible />
```
**Use when**: Component is below the fold or in a tab

**`client:media`** - Hydrate based on media query
```astro
<MobileMenu client:media="(max-width: 768px)" />
```
**Use when**: Component only needed on certain screen sizes

**`client:only`** - Skip server rendering, only render on client
```astro
<BrowserOnlyWidget client:only="react" />
```
**Use when**: Component breaks during SSR (uses window, document, etc.)

### Server-First Approach

**DO**: Render on server by default
```astro
---
// This runs on the server at build time
const posts = await getCollection('blog');
---

<ul>
  {posts.map(post => (
    <li>{post.data.title}</li>
  ))}
</ul>
```

**DON'T**: Add client directives unnecessarily
```astro
<!-- ❌ Wrong - static content doesn't need hydration -->
<StaticBlogPost client:load />

<!-- ✅ Correct - server-rendered by default -->
<StaticBlogPost />
```

## Data Fetching Patterns

### In Component Frontmatter

**DO**: Fetch data in frontmatter (runs at build time)
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
```

**DON'T**: Fetch data in template (will cause errors)
```astro
<!-- ❌ Wrong - can't use await in template -->
<div>
  {await getCollection('blog')}
</div>
```

### In getStaticPaths()

**DO**: Return both params and props
```typescript
export async function getStaticPaths() {
  const posts = await getCollection('blog');

  return posts.map(post => ({
    params: { slug: post.id },
    props: { post },
  }));
}

const { post } = Astro.props;
```

**DON'T**: Access Astro.params inside getStaticPaths()
```typescript
// ❌ Wrong - Astro.params not available here
export async function getStaticPaths() {
  const slug = Astro.params.slug; // Error!
  return [];
}
```

### External API Calls

**DO**: Use fetch in frontmatter or getStaticPaths
```astro
---
const response = await fetch('https://api.example.com/data');
const data = await response.json();
---
```

**DO**: Add error handling
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

{error && <div>Error: {error}</div>}
{data && <div>{JSON.stringify(data)}</div>}
```

## Content Collections

### Schema Definition

**DO**: Define all frontmatter fields explicitly
```typescript
import { z, defineCollection } from 'astro:content';

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    tags: z.array(z.string()),
    draft: z.boolean().default(false),
  })
});
```

**DON'T**: Leave frontmatter fields untyped
```typescript
// ❌ Wrong - no schema validation
const blog = defineCollection({
  type: 'content',
});
```

### Query Patterns

**DO**: Always sort if order matters
```typescript
const posts = (await getCollection('blog')).sort(
  (a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf()
);
```

**DON'T**: Rely on default order
```typescript
// ❌ Wrong - order is non-deterministic
const posts = await getCollection('blog');
// Posts may be in any order!
```

**DO**: Filter at query time
```typescript
const publishedPosts = await getCollection('blog', ({ data }) => {
  return import.meta.env.PROD ? data.draft !== true : true;
});
```

### Rendering Content

**DO**: Use render() function
```astro
---
import { getEntry, render } from 'astro:content';

const post = await getEntry('blog', 'my-post');
const { Content, headings } = await render(post);
---

<article>
  <h1>{post.data.title}</h1>
  <Content />
</article>
```

**DON'T**: Try to access raw content directly
```astro
<!-- ❌ Wrong - post.body is raw markdown -->
<div>{post.body}</div>

<!-- ✅ Correct - use Content component -->
<Content />
```

## TypeScript Usage

### Type Imports

**DO**: Use type imports for types
```typescript
import type { CollectionEntry } from 'astro:content';
import type { ImageMetadata } from 'astro';

interface Props {
  post: CollectionEntry<'blog'>;
  image: ImageMetadata;
}
```

**DO**: Type component props
```astro
---
import type { CollectionEntry } from 'astro:content';

interface Props {
  post: CollectionEntry<'blog'>;
  showDate?: boolean;
}

const { post, showDate = true } = Astro.props;
---
```

### Configuration

**DO**: Use strict TypeScript config
```json
{
  "extends": "astro/tsconfigs/strict"
}
```

**DO**: Enable type checking
```bash
npm run astro check
```

## Props and Astro.props

### Passing Props

**DO**: Pass props with proper syntax
```astro
<BlogPost post={post} showDate={true} />
```

**DON'T**: Use JSX spread incorrectly
```astro
<!-- ❌ Wrong - props must be explicit in Astro -->
<BlogPost {...props} />

<!-- ✅ Correct - destructure and pass explicitly -->
<BlogPost title={props.title} date={props.date} />
```

### Accessing Props

**DO**: Destructure Astro.props
```astro
---
const { title, description } = Astro.props;
---
```

**DO**: Provide defaults
```astro
---
const { showSidebar = true, theme = 'light' } = Astro.props;
---
```

## File Organization

### Project Structure

**DO**: Follow Astro conventions
```
src/
├── components/        # Reusable components
├── layouts/           # Page layouts
├── pages/             # Routes (file-based routing)
├── content/           # Content collections
│   ├── docs/
│   └── blog/
├── assets/            # Images, fonts (processed by Astro)
├── styles/            # Global styles
└── utils/             # Utility functions

public/                # Static assets (copied as-is)
```

### Component Files

**DO**: Use descriptive names
```
components/
├── Header.astro
├── Footer.astro
├── blog/
│   ├── BlogPost.astro
│   ├── BlogList.astro
│   └── BlogCard.astro
```

**DON'T**: Mix concerns
```
// ❌ Don't put layout logic in components
// ❌ Don't put business logic in layouts
```

## Performance Optimization

### Image Optimization

**DO**: Use Astro's Image component
```astro
---
import { Image } from 'astro:assets';
import myImage from '../assets/photo.jpg';
---

<Image src={myImage} alt="Description" width={800} height={600} />
```

**DO**: Optimize remote images
```astro
<Image
  src="https://example.com/image.jpg"
  alt="Remote image"
  width={800}
  height={600}
  loading="lazy"
/>
```

### Code Splitting

**DO**: Use dynamic imports for heavy components
```astro
---
const HeavyChart = (await import('../components/HeavyChart.jsx')).default;
---

<HeavyChart client:visible />
```

### CSS Optimization

**DO**: Scope styles to components
```astro
<style>
  /* Automatically scoped to this component */
  .title {
    color: blue;
  }
</style>
```

**DO**: Use :global() for global styles
```astro
<style>
  :global(body) {
    font-family: system-ui;
  }
</style>
```

## Environment Variables

### Type-Safe Env Vars

**DO**: Define in astro.config.mjs
```typescript
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

**DO**: Import from astro:env
```typescript
import { PUBLIC_API_URL } from 'astro:env/client';
import { SECRET_API_KEY } from 'astro:env/server';
```

**DON'T**: Use import.meta.env for new projects
```typescript
// ❌ Legacy pattern - use astro:env instead
const apiKey = import.meta.env.SECRET_API_KEY;
```

## Error Handling

### Graceful Degradation

**DO**: Handle missing data
```astro
---
const post = await getEntry('blog', Astro.params.slug);

if (!post) {
  return Astro.redirect('/404');
}
---
```

**DO**: Validate user input
```astro
---
const { page = '1' } = Astro.params;
const pageNum = parseInt(page);

if (isNaN(pageNum) || pageNum < 1) {
  return Astro.redirect('/blog');
}
---
```

### Error Boundaries

**DO**: Wrap potentially failing code
```astro
---
let externalData = null;

try {
  const response = await fetch('https://api.example.com/data');
  externalData = await response.json();
} catch (error) {
  console.error('Failed to fetch external data:', error);
}
---

{externalData ? (
  <ExternalWidget data={externalData} />
) : (
  <div>Content temporarily unavailable</div>
)}
```

## Testing

### Type Checking

**DO**: Run type checking regularly
```bash
npm run astro check
```

### Build Testing

**DO**: Test production builds
```bash
npm run build
npm run preview
```

### Link Checking

**DO**: Verify internal links work
```bash
npm run build
# Check for broken links in dist/
```

## Common Patterns

### Pagination

**DO**: Use paginate() helper
```typescript
export async function getStaticPaths({ paginate }) {
  const posts = await getCollection('blog');
  return paginate(posts, { pageSize: 10 });
}

const { page } = Astro.props;
```

### i18n

**DO**: Use Astro's i18n routing
```typescript
export default defineConfig({
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'es', 'fr'],
  }
});
```

### Middleware

**DO**: Use middleware for cross-cutting concerns
```typescript
// src/middleware.ts
import { defineMiddleware } from 'astro:middleware';

export const onRequest = defineMiddleware(async (context, next) => {
  // Add custom logic
  return await next();
});
```

## Key Takeaways

1. ✅ **Server-first**: Render on server by default, add client directives only when needed
2. ✅ **Type safety**: Use TypeScript and schema validation
3. ✅ **Data fetching**: In frontmatter or getStaticPaths(), not in templates
4. ✅ **Content collections**: Define schemas, always sort, use render()
5. ✅ **Images**: Use Image component for optimization
6. ✅ **Error handling**: Graceful degradation and validation
7. ✅ **Performance**: Code splitting, lazy loading, scoped CSS
8. ✅ **File organization**: Follow Astro conventions
9. ✅ **Testing**: Type check and build regularly
10. ✅ **Environment**: Use type-safe env vars via astro:env
