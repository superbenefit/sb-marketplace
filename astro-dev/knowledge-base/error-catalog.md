# Astro Error Catalog & Quick Fixes

**Quick Reference**: Error patterns indexed by symptom with immediate fixes.

## Import Errors

### Missing File Extensions

**Symptom**: Module not found error for local imports

**Error**: `Cannot find module '../layouts/Layout'`

**Fix**: Always include file extensions for relative imports
```typescript
// ❌ Wrong
import Layout from '../layouts/Layout';

// ✅ Correct
import Layout from '../layouts/Layout.astro';
import Button from './Button.jsx';
import { helper } from './utils.ts';
```

**Why**: Astro requires explicit file extensions for ES module imports

---

### Wrong Astro Module Prefix

**Symptom**: Module not found for Astro built-ins

**Error**: `Cannot find module 'astro/content'`

**Fix**: Use `astro:` prefix (with colon), not `astro/`
```typescript
// ❌ Wrong
import { getCollection } from 'astro/content';

// ✅ Correct
import { getCollection } from 'astro:content';
import { Image } from 'astro:assets';
import { SECRET_KEY } from 'astro:env/server';
```

**Why**: Built-in Astro modules use `astro:` prefix, npm packages use `astro/`

---

### CommonJS Require

**Symptom**: require() not working in Astro files

**Error**: `require is not defined`

**Fix**: Use ES module imports instead
```typescript
// ❌ Wrong
const Layout = require('../layouts/Layout.astro');

// ✅ Correct
import Layout from '../layouts/Layout.astro';
```

**Why**: Astro uses ES modules, not CommonJS

---

## Component & Hydration Errors

### Over-Hydration

**Symptom**: Large bundle sizes, slow page load

**Fix**: Only hydrate interactive components
```astro
<!-- ❌ Wrong - static content doesn't need hydration -->
<BlogPost client:load />
<Header client:load />

<!-- ✅ Correct - only hydrate interactive parts -->
<BlogPost />
<Header />
<InteractiveSearch client:load />
```

**Why**: Unnecessary hydration adds JavaScript bundle weight

---

### Wrong Client Directive

**Symptom**: Heavy components hydrate immediately, slowing page

**Fix**: Use appropriate directive for component priority
```astro
<!-- ❌ Wrong - heavy chart loaded immediately -->
<ComplexChart client:load />

<!-- ✅ Correct - lazy load when visible -->
<ComplexChart client:visible />
```

**Directive Guide**:
- `client:load` - Immediate (above-fold critical interactions)
- `client:idle` - When browser idle (important but not critical)
- `client:visible` - When in viewport (below-fold, heavy components)
- `client:media="(max-width: 768px)"` - Based on media query
- `client:only="react"` - Client-only (no SSR)

---

### Missing Client Directive

**Symptom**: Framework component not interactive

**Fix**: Add client directive to framework components
```astro
<!-- ❌ Wrong - React component won't be interactive -->
<ReactCounter />

<!-- ✅ Correct -->
<ReactCounter client:load />
```

**Why**: Framework components need client directive for interactivity

---

### Missing Framework Hint for client:only

**Symptom**: Build error with client:only directive

**Error**: `client:only directive requires a framework hint`

**Fix**: Specify the framework
```astro
<!-- ❌ Wrong -->
<BrowserWidget client:only />

<!-- ✅ Correct -->
<BrowserWidget client:only="react" />
```

**Valid frameworks**: `"react"`, `"preact"`, `"vue"`, `"svelte"`, `"solid-js"`

---

### Missing Media Query for client:media

**Symptom**: Build error with client:media directive

**Error**: `client:media directive requires a media query value`

**Fix**: Provide media query
```astro
<!-- ❌ Wrong -->
<MobileMenu client:media />

<!-- ✅ Correct -->
<MobileMenu client:media="(max-width: 768px)" />
```

---

## getStaticPaths() Errors

### Missing getStaticPaths()

**Symptom**: Build fails for dynamic route

**Error**: `getStaticPaths() function is required for dynamic routes`

**Fix**: Export getStaticPaths for dynamic routes in static mode
```astro
<!-- src/pages/blog/[slug].astro -->
---
// ❌ Wrong - missing getStaticPaths
const { slug } = Astro.params;
---

<!-- ✅ Correct -->
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

**Why**: Static mode requires all paths generated at build time

---

### Accessing Astro.params in getStaticPaths()

**Symptom**: Astro.params is undefined

**Error**: `Cannot read property 'slug' of undefined`

**Fix**: Don't access Astro.params inside getStaticPaths()
```typescript
// ❌ Wrong
export async function getStaticPaths() {
  const slug = Astro.params.slug;  // Not available here!
  return [];
}

// ✅ Correct
export async function getStaticPaths() {
  const posts = await getCollection('blog');
  return posts.map(post => ({
    params: { slug: post.id }
  }));
}

// Access params OUTSIDE getStaticPaths
const { slug } = Astro.params;
```

---

### Wrong Return Format

**Symptom**: getStaticPaths return format error

**Error**: `Expected array of objects with params property`

**Fix**: Return array of objects with params
```typescript
// ❌ Wrong
export async function getStaticPaths() {
  return ['post-1', 'post-2'];
}

// ❌ Wrong
export async function getStaticPaths() {
  return [{ params: 'post-1' }];
}

// ✅ Correct
export async function getStaticPaths() {
  return [
    { params: { slug: 'post-1' } },
    { params: { slug: 'post-2' } }
  ];
}
```

---

## Props Handling Errors

### Using JSX Spread Props

**Symptom**: Props not passing through

**Fix**: Pass props explicitly in Astro (not like JSX)
```astro
<!-- ❌ Wrong - Astro doesn't support spread props like JSX -->
<BlogPost {...props} />

<!-- ✅ Correct - be explicit -->
<BlogPost title={props.title} date={props.date} author={props.author} />
```

---

### Missing Curly Braces

**Symptom**: Props showing literal text instead of values

**Fix**: Use curly braces for dynamic values
```astro
<!-- ❌ Wrong -->
<BlogPost title=post.title />

<!-- ✅ Correct -->
<BlogPost title={post.title} />
```

---

### Missing Props Interface

**Symptom**: No TypeScript IntelliSense, runtime errors

**Fix**: Always type your props
```astro
---
// ❌ Wrong
const { title, date } = Astro.props;
---

<!-- ✅ Correct -->
---
interface Props {
  title: string;
  date: Date;
  draft?: boolean;
}

const { title, date, draft = false } = Astro.props;
---
```

---

## Content Collection Errors

### Missing Schema Validation

**Symptom**: No type safety, runtime errors from bad data

**Fix**: Always define collection schemas
```typescript
// ❌ Wrong
const blog = defineCollection({
  type: 'content'
});

// ✅ Correct
const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    pubDate: z.coerce.date(),
    tags: z.array(z.string()),
  })
});
```

---

### Non-Deterministic Collection Order

**Symptom**: Collections in random order, different on each build

**Fix**: Always sort collections if order matters
```typescript
// ❌ Wrong - order is platform-dependent
const posts = await getCollection('blog');

// ✅ Correct - explicit sorting
const posts = (await getCollection('blog')).sort(
  (a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf()
);
```

---

### Wrong Render Pattern

**Symptom**: Raw markdown showing instead of HTML

**Fix**: Use render() function for markdown content
```astro
---
// ❌ Wrong - raw markdown
const post = await getEntry('blog', 'my-post');
---
<div>{post.body}</div>

<!-- ✅ Correct -->
---
import { getEntry, render } from 'astro:content';

const post = await getEntry('blog', 'my-post');
const { Content } = await render(post);
---
<Content />
```

---

### Missing Null Check

**Symptom**: Runtime error when entry doesn't exist

**Error**: `Cannot read property 'data' of undefined`

**Fix**: Always check if entry exists
```astro
---
// ❌ Wrong
const post = await getEntry('blog', Astro.params.slug);
---
<h1>{post.data.title}</h1>

<!-- ✅ Correct -->
---
const post = await getEntry('blog', Astro.params.slug);

if (!post) {
  return Astro.redirect('/404');
}
---
<h1>{post.data.title}</h1>
```

---

## Template Errors

### Async in Template

**Symptom**: Syntax error in template

**Error**: `Unexpected reserved word 'await'`

**Fix**: Fetch data in frontmatter, not templates
```astro
<!-- ❌ Wrong -->
<div>
  {await getCollection('blog')}
</div>

<!-- ✅ Correct -->
---
const posts = await getCollection('blog');
---
<div>
  {posts.map(post => <div>{post.data.title}</div>)}
</div>
```

---

### Event Handlers on HTML Elements

**Symptom**: onClick handler not working

**Fix**: Use framework component or vanilla JS
```astro
<!-- ❌ Wrong - event handlers don't work on static HTML -->
<button onClick={handleClick}>Click</button>

<!-- ✅ Correct - Option 1: Framework component -->
---
import Button from '../components/Button.jsx';
---
<Button onClick={handleClick} client:load />

<!-- ✅ Correct - Option 2: Vanilla JS -->
<button id="myButton">Click</button>
<script>
  document.getElementById('myButton').addEventListener('click', () => {
    console.log('Clicked!');
  });
</script>
```

---

## Starlight-Specific Errors

### Wrong Frontmatter Fields

**Symptom**: Starlight features not working

**Fix**: Use correct Starlight field names
```markdown
<!-- ❌ Wrong -->
---
heading: My Page
summary: Description
---

<!-- ✅ Correct -->
---
title: My Page
description: Description
---
```

---

### Wrong Template Value

**Symptom**: Template not recognized

**Error**: `Invalid template value 'landing'`

**Fix**: Use valid template values
```markdown
<!-- ❌ Wrong -->
---
template: landing
---

<!-- ✅ Correct -->
---
template: splash
---
```

**Valid values**: `'doc'` (default) or `'splash'`

---

### Missing docsLoader/docsSchema

**Symptom**: Starlight features don't work

**Fix**: Use Starlight's loader and schema
```typescript
// ❌ Wrong
export const collections = {
  docs: defineCollection({
    type: 'content'
  })
};

// ✅ Correct
import { docsLoader } from '@astrojs/starlight/loaders';
import { docsSchema } from '@astrojs/starlight/schema';

export const collections = {
  docs: defineCollection({
    loader: docsLoader(),
    schema: docsSchema()
  })
};
```

---

### Wrong Collection Name

**Symptom**: Starlight routes don't generate

**Fix**: Collection must be named 'docs'
```typescript
// ❌ Wrong
export const collections = {
  documentation: defineCollection({
    loader: docsLoader(),
    schema: docsSchema()
  })
};

// ✅ Correct
export const collections = {
  docs: defineCollection({
    loader: docsLoader(),
    schema: docsSchema()
  })
};
```

---

## Environment Variable Errors

### Exposing Secrets to Client

**Symptom**: Security vulnerability

**Fix**: Never pass server secrets to client code
```astro
---
import { SECRET_API_KEY } from 'astro:env/server';
---

<!-- ❌ DANGER - exposes secret! -->
<script>
  const apiKey = SECRET_API_KEY;
</script>

<!-- ✅ Correct - use secret on server only -->
---
import { SECRET_API_KEY } from 'astro:env/server';

const data = await fetch('https://api.example.com', {
  headers: { 'Authorization': `Bearer ${SECRET_API_KEY}` }
});
---
```

---

### Wrong Env Var Context

**Symptom**: Environment variable not available on client

**Fix**: Public vars must use context: 'client'
```typescript
// ❌ Wrong
env: {
  schema: {
    PUBLIC_KEY: envField.string({
      context: 'server',  // Wrong for public var
      access: 'public'
    })
  }
}

// ✅ Correct
env: {
  schema: {
    PUBLIC_KEY: envField.string({
      context: 'client',
      access: 'public'
    })
  }
}
```

---

## Image Handling Errors

### Not Using Image Component

**Symptom**: No image optimization, large page sizes

**Fix**: Use Astro's Image component
```astro
<!-- ❌ Wrong - no optimization -->
<img src="/images/photo.jpg" alt="Photo" />

<!-- ✅ Correct - optimized -->
---
import { Image } from 'astro:assets';
import photo from '../assets/photo.jpg';
---
<Image src={photo} alt="Photo" />
```

---

### Missing Dimensions for Remote Images

**Symptom**: Build error with remote images

**Error**: `Remote images require width and height`

**Fix**: Provide dimensions for remote images
```astro
<!-- ❌ Wrong -->
<Image src="https://example.com/image.jpg" alt="Remote" />

<!-- ✅ Correct -->
<Image
  src="https://example.com/image.jpg"
  alt="Remote"
  width={800}
  height={600}
/>
```

---

## Build & Configuration Errors

### Node APIs in Browser

**Symptom**: Build error or runtime error

**Error**: `fs is not defined`

**Fix**: Use Node APIs only in frontmatter
```astro
<!-- ❌ Wrong -->
<script>
  import fs from 'node:fs';
  fs.readFileSync('file.txt');
</script>

<!-- ✅ Correct -->
---
import fs from 'node:fs';
const content = fs.readFileSync('file.txt', 'utf-8');
---
<script define:vars={{ content }}>
  console.log(content);
</script>
```

---

### Missing Adapter for SSR

**Symptom**: Build fails with output: 'server'

**Error**: `output: 'server' requires an adapter`

**Fix**: Add adapter for server output
```typescript
// ❌ Wrong
export default defineConfig({
  output: 'server'
});

// ✅ Correct
import node from '@astrojs/node';

export default defineConfig({
  output: 'server',
  adapter: node()
});
```

---

### Missing Protocol in Site URL

**Symptom**: Sitemap/RSS generation fails

**Error**: `site URL must include protocol`

**Fix**: Include http:// or https://
```typescript
// ❌ Wrong
site: 'example.com'

// ✅ Correct
site: 'https://example.com'
```

---

## Quick Reference: Common Fixes

**Imports**:
1. Add file extensions to relative imports
2. Use `astro:` prefix for built-ins
3. Use `import`, not `require()`

**Components**:
1. Only hydrate interactive components
2. Framework components need `client:*` directives
3. No event handlers on static HTML

**Dynamic Routes**:
1. Export `getStaticPaths()` in static mode
2. Return array with `{ params: {...} }` format
3. Don't access `Astro.params` inside `getStaticPaths()`

**Collections**:
1. Define schemas for all collections
2. Always sort if order matters
3. Use `render()` for markdown content
4. Check if entry exists before using

**Data**:
1. Fetch in frontmatter, not templates
2. No `await` in template section
3. Type all props with interface

**Starlight**:
1. Use `docsLoader()` and `docsSchema()`
2. Collection must be named `'docs'`
3. Only `title` is required in frontmatter
