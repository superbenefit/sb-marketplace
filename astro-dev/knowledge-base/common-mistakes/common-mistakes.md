# Common Astro & Starlight Mistakes to Avoid

This document catalogs common mistakes when developing with Astro and Starlight, with explanations of why they're wrong and how to fix them.

## Import and Module Errors

### Mistake: Missing File Extensions

**❌ Wrong**:
```astro
import Layout from '../layouts/Layout';
```

**✅ Correct**:
```astro
import Layout from '../layouts/Layout.astro';
```

**Why**: Astro requires explicit file extensions for component imports.

### Mistake: Using require()

**❌ Wrong**:
```javascript
const Layout = require('../layouts/Layout.astro');
```

**✅ Correct**:
```javascript
import Layout from '../layouts/Layout.astro';
```

**Why**: Astro uses ES modules, not CommonJS. Always use `import`.

### Mistake: Incorrect astro: Module Imports

**❌ Wrong**:
```typescript
import { getCollection } from 'astro/content';
```

**✅ Correct**:
```typescript
import { getCollection } from 'astro:content';
```

**Why**: Built-in Astro modules use `astro:` prefix, not `astro/`.

## Component and Hydration Errors

### Mistake: Over-Hydration

**❌ Wrong**:
```astro
<!-- Static content doesn't need hydration -->
<BlogPost client:load />
<StaticHeader client:load />
<Footer client:load />
```

**✅ Correct**:
```astro
<!-- Only hydrate interactive components -->
<BlogPost />
<StaticHeader />
<Footer />
<InteractiveSearch client:load />
```

**Why**: Unnecessary hydration increases bundle size and slows page load.

### Mistake: Wrong Client Directive

**❌ Wrong**:
```astro
<!-- Heavy chart hydrated immediately -->
<ComplexChart client:load />
```

**✅ Correct**:
```astro
<!-- Heavy chart hydrated when visible -->
<ComplexChart client:visible />
```

**Why**: Use appropriate directive for component's priority and position.

### Mistake: Missing Client Directive for Framework Components

**❌ Wrong**:
```astro
<!-- React component without directive won't be interactive -->
<ReactCounter />
```

**✅ Correct**:
```astro
<ReactCounter client:load />
```

**Why**: Framework components need client directive to be interactive.

## getStaticPaths() Errors

### Mistake: Accessing Astro.params Inside getStaticPaths()

**❌ Wrong**:
```typescript
export async function getStaticPaths() {
  const slug = Astro.params.slug;  // Error!
  return [];
}
```

**✅ Correct**:
```typescript
export async function getStaticPaths() {
  const posts = await getCollection('blog');
  return posts.map(post => ({
    params: { slug: post.id }
  }));
}

// Access params OUTSIDE getStaticPaths
const { slug } = Astro.params;
```

**Why**: `Astro.params` is not available inside `getStaticPaths()`.

### Mistake: Missing getStaticPaths() for Dynamic Routes

**❌ Wrong**:
```astro
<!-- src/pages/blog/[slug].astro -->
---
const { slug } = Astro.params;
const post = await getEntry('blog', slug);
---
```

**✅ Correct**:
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

**Why**: Dynamic routes in static mode require `getStaticPaths()`.

### Mistake: Returning Wrong Data Structure

**❌ Wrong**:
```typescript
export async function getStaticPaths() {
  return ['post-1', 'post-2'];  // Wrong format
}
```

**✅ Correct**:
```typescript
export async function getStaticPaths() {
  return [
    { params: { slug: 'post-1' }},
    { params: { slug: 'post-2' }}
  ];
}
```

**Why**: Must return array of objects with `params` property.

## Props Handling Mistakes

### Mistake: Using Spread Props

**❌ Wrong**:
```astro
<BlogPost {...props} />
```

**✅ Correct**:
```astro
<BlogPost title={props.title} date={props.date} author={props.author} />
```

**Why**: Astro requires explicit prop passing (unlike JSX).

### Mistake: Passing Props Incorrectly

**❌ Wrong**:
```astro
<!-- Missing curly braces for expressions -->
<BlogPost title=post.title />
```

**✅ Correct**:
```astro
<BlogPost title={post.title} />
```

**Why**: Dynamic values need curly braces `{}`.

### Mistake: Not Typing Props

**❌ Wrong**:
```astro
---
const { title, date } = Astro.props;
---
```

**✅ Correct**:
```astro
---
interface Props {
  title: string;
  date: Date;
}

const { title, date } = Astro.props;
---
```

**Why**: Type safety prevents runtime errors and improves IDE support.

## Content Collection Mistakes

### Mistake: No Schema Validation

**❌ Wrong**:
```typescript
const blog = defineCollection({
  type: 'content',
  // No schema
});
```

**✅ Correct**:
```typescript
const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    pubDate: z.coerce.date(),
    tags: z.array(z.string()),
  })
});
```

**Why**: Schema validation catches errors early and provides type safety.

### Mistake: Not Sorting Collections

**❌ Wrong**:
```typescript
const posts = await getCollection('blog');
// Order is non-deterministic!
```

**✅ Correct**:
```typescript
const posts = (await getCollection('blog')).sort(
  (a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf()
);
```

**Why**: Collection order is platform-dependent. Always sort if order matters.

### Mistake: Using Wrong Render Pattern

**❌ Wrong**:
```astro
---
const post = await getEntry('blog', 'my-post');
---

<!-- Raw markdown, not rendered -->
<div>{post.body}</div>
```

**✅ Correct**:
```astro
---
import { getEntry, render } from 'astro:content';

const post = await getEntry('blog', 'my-post');
const { Content } = await render(post);
---

<Content />
```

**Why**: Must use `render()` to convert markdown to HTML.

### Mistake: Missing Collection Entry Check

**❌ Wrong**:
```astro
---
const post = await getEntry('blog', Astro.params.slug);
// What if post is undefined?
---

<h1>{post.data.title}</h1>  <!-- Error if post doesn't exist -->
```

**✅ Correct**:
```astro
---
const post = await getEntry('blog', Astro.params.slug);

if (!post) {
  return Astro.redirect('/404');
}
---

<h1>{post.data.title}</h1>
```

**Why**: Entry might not exist - always check before using.

## Data Fetching Errors

### Mistake: Async in Template

**❌ Wrong**:
```astro
<div>
  {await getCollection('blog')}  <!-- Error! -->
</div>
```

**✅ Correct**:
```astro
---
const posts = await getCollection('blog');
---

<div>
  {posts.map(post => <div>{post.data.title}</div>)}
</div>
```

**Why**: Can't use `await` in templates - fetch data in frontmatter.

### Mistake: Fetching in Component Body

**❌ Wrong**:
```astro
<script>
  // This runs in browser, can't access server-side APIs
  const posts = await getCollection('blog');
</script>
```

**✅ Correct**:
```astro
---
// This runs on server at build time
const posts = await getCollection('blog');
---

<script define:vars={{ postsData: posts }}>
  console.log(postsData);
</script>
```

**Why**: Server APIs only work in frontmatter, not client-side scripts.

## Starlight-Specific Mistakes

### Mistake: Wrong Frontmatter Fields

**❌ Wrong**:
```markdown
---
heading: My Page
summary: Page description
---
```

**✅ Correct**:
```markdown
---
title: My Page
description: Page description
---
```

**Why**: Starlight requires specific frontmatter field names.

### Mistake: Incorrect Template Value

**❌ Wrong**:
```markdown
---
title: Landing Page
template: landing  <!-- Wrong value -->
---
```

**✅ Correct**:
```markdown
---
title: Landing Page
template: splash
---
```

**Why**: Only `'doc'` and `'splash'` are valid template values.

### Mistake: Missing docsLoader/docsSchema

**❌ Wrong**:
```typescript
import { defineCollection } from 'astro:content';

export const collections = {
  docs: defineCollection({
    type: 'content'
  })
};
```

**✅ Correct**:
```typescript
import { defineCollection } from 'astro:content';
import { docsLoader } from '@astrojs/starlight/loaders';
import { docsSchema } from '@astrojs/starlight/schema';

export const collections = {
  docs: defineCollection({
    loader: docsLoader(),
    schema: docsSchema()
  })
};
```

**Why**: Starlight requires its specific loader and schema.

### Mistake: Modifying Starlight Collection Name

**❌ Wrong**:
```typescript
export const collections = {
  documentation: defineCollection({  // Wrong name
    loader: docsLoader(),
    schema: docsSchema()
  })
};
```

**✅ Correct**:
```typescript
export const collections = {
  docs: defineCollection({  // Must be 'docs'
    loader: docsLoader(),
    schema: docsSchema()
  })
};
```

**Why**: Starlight expects collection to be named `'docs'`.

## TypeScript Mistakes

### Mistake: Not Using Type Imports

**❌ Wrong**:
```typescript
import { CollectionEntry } from 'astro:content';  // Runtime import
```

**✅ Correct**:
```typescript
import type { CollectionEntry } from 'astro:content';  // Type-only import
```

**Why**: Type-only imports are removed at build time, reducing bundle size.

### Mistake: Missing Type Definitions

**❌ Wrong**:
```astro
---
interface Props {
  post: any;  // Too vague
}
---
```

**✅ Correct**:
```astro
---
import type { CollectionEntry } from 'astro:content';

interface Props {
  post: CollectionEntry<'blog'>;
}
---
```

**Why**: Specific types provide better IDE support and catch errors.

## Image Handling Mistakes

### Mistake: Not Using Image Component

**❌ Wrong**:
```html
<img src="/images/photo.jpg" alt="Photo" />
```

**✅ Correct**:
```astro
---
import { Image } from 'astro:assets';
import photo from '../assets/photo.jpg';
---

<Image src={photo} alt="Photo" />
```

**Why**: Image component provides optimization, responsive sizing, and better performance.

### Mistake: Incorrect Remote Image Syntax

**❌ Wrong**:
```astro
---
import { Image } from 'astro:assets';
---

<!-- Missing width/height for remote images -->
<Image src="https://example.com/image.jpg" alt="Remote" />
```

**✅ Correct**:
```astro
<Image
  src="https://example.com/image.jpg"
  alt="Remote"
  width={800}
  height={600}
/>
```

**Why**: Remote images require explicit dimensions.

## Environment Variable Mistakes

### Mistake: Accessing Secrets on Client

**❌ Wrong**:
```astro
---
import { SECRET_API_KEY } from 'astro:env/server';
---

<script>
  // Exposes secret to client!
  const apiKey = SECRET_API_KEY;
</script>
```

**✅ Correct**:
```astro
---
import { SECRET_API_KEY } from 'astro:env/server';

// Use secret on server only
const data = await fetch('https://api.example.com', {
  headers: { 'Authorization': `Bearer ${SECRET_API_KEY}` }
});
---
```

**Why**: Server-side secrets must never be exposed to client.

### Mistake: Wrong Env Var Context

**❌ Wrong**:
```typescript
// astro.config.mjs
env: {
  schema: {
    PUBLIC_KEY: envField.string({
      context: 'server',  // Wrong context for public var
      access: 'public'
    })
  }
}
```

**✅ Correct**:
```typescript
env: {
  schema: {
    PUBLIC_KEY: envField.string({
      context: 'client',  // Correct for public vars
      access: 'public'
    })
  }
}
```

**Why**: Public vars must use `context: 'client'` to be available on client-side.

## Build and Deployment Errors

### Mistake: Relying on Node-Only APIs in Browser

**❌ Wrong**:
```astro
<script>
  import fs from 'node:fs';  // Error in browser!
  fs.readFileSync('file.txt');
</script>
```

**✅ Correct**:
```astro
---
import fs from 'node:fs';  // OK in frontmatter (server-side)
const content = fs.readFileSync('file.txt', 'utf-8');
---

<script define:vars={{ content }}>
  console.log(content);
</script>
```

**Why**: Node APIs only work server-side, not in browser.

### Mistake: Hard-Coding URLs

**❌ Wrong**:
```astro
<a href="http://localhost:4321/about">About</a>
```

**✅ Correct**:
```astro
<a href="/about">About</a>
```

**Why**: Relative paths work in all environments.

## Performance Mistakes

### Mistake: Importing Entire Libraries

**❌ Wrong**:
```typescript
import _ from 'lodash';  // Imports entire library
```

**✅ Correct**:
```typescript
import debounce from 'lodash/debounce';  // Only what you need
```

**Why**: Tree-shaking works better with specific imports.

### Mistake: Not Lazy Loading Heavy Components

**❌ Wrong**:
```astro
---
import HeavyChart from '../components/HeavyChart';
---

<!-- Chart below fold, but loaded immediately -->
<HeavyChart client:load />
```

**✅ Correct**:
```astro
---
import HeavyChart from '../components/HeavyChart';
---

<HeavyChart client:visible />
```

**Why**: `client:visible` defers load until component is visible.

## Key Takeaways

**Always**:
1. ✅ Include file extensions in imports
2. ✅ Use `astro:` prefix for built-in modules
3. ✅ Define schemas for content collections
4. ✅ Sort collections if order matters
5. ✅ Type component props
6. ✅ Check if collection entries exist
7. ✅ Use `render()` for markdown content
8. ✅ Fetch data in frontmatter, not templates
9. ✅ Use Image component for images
10. ✅ Keep secrets server-side only

**Never**:
1. ❌ Access `Astro.params` in `getStaticPaths()`
2. ❌ Use `await` in templates
3. ❌ Over-hydrate static components
4. ❌ Expose server secrets to client
5. ❌ Use Node APIs in browser scripts
6. ❌ Rely on non-deterministic collection order
7. ❌ Skip type definitions
8. ❌ Use `require()` instead of `import`
9. ❌ Hard-code localhost URLs
10. ❌ Import entire libraries when you need one function
