# Astro Imports Reference

**Source**: https://docs.astro.build/en/guides/imports/

This document provides authoritative rules for import statements in Astro.

## Import Fundamentals

### ES Modules Only

Astro uses **ES modules**, NOT CommonJS:

✅ **CORRECT**: ES module imports
```typescript
import Component from './Component.astro';
import { helper } from './utils.ts';
```

❌ **INCORRECT**: CommonJS (not supported)
```javascript
const Component = require('./Component.astro');  // ❌ NOT SUPPORTED
module.exports = { ... };  // ❌ NOT SUPPORTED
```

### File Extensions Required

**CRITICAL RULE**: Always include file extensions for relative imports

✅ **CORRECT**: With file extension
```typescript
import Layout from '../layouts/Layout.astro';
import Button from './Button.jsx';
import data from '../data.json';
import { helper } from './utils.ts';
```

❌ **INCORRECT**: Missing file extension
```typescript
import Layout from '../layouts/Layout';      // ❌ Missing .astro
import Button from './Button';              // ❌ Missing .jsx
import { helper } from './utils';           // ❌ Missing .ts
```

**Exception**: npm packages don't need extensions
```typescript
import React from 'react';              // ✅ OK (npm package)
import { format } from 'date-fns';      // ✅ OK (npm package)
```

## Astro Built-in Modules

### Module Specifier Pattern

Built-in Astro modules use `astro:` prefix (with colon):

✅ **CORRECT**: `astro:` prefix
```typescript
import { getCollection } from 'astro:content';
import { Image } from 'astro:assets';
import { defineAction } from 'astro:actions';
```

❌ **INCORRECT**: Wrong prefix patterns
```typescript
import { getCollection } from 'astro/content';   // ❌ Slash instead of colon
import { getCollection } from '@astro/content';  // ❌ Wrong prefix
import { getCollection } from 'astro-content';   // ❌ Wrong format
```

### Common Built-in Modules

| Module | Import | Purpose |
|--------|--------|---------|
| `astro:content` | `import { getCollection, getEntry, render } from 'astro:content'` | Content collections |
| `astro:assets` | `import { Image, getImage } from 'astro:assets'` | Image optimization |
| `astro:actions` | `import { defineAction } from 'astro:actions'` | Server actions |
| `astro:transitions` | `import { ViewTransitions } from 'astro:transitions'` | View transitions |
| `astro:middleware` | `import { defineMiddleware } from 'astro:middleware'` | Middleware |
| `astro:env/client` | `import { PUBLIC_KEY } from 'astro:env/client'` | Client env vars |
| `astro:env/server` | `import { SECRET_KEY } from 'astro:env/server'` | Server env vars |

**Validation checklist**:
- [ ] Using `astro:` prefix (with colon)
- [ ] Not using `astro/` (with slash)
- [ ] Importing from correct module

## Component Imports

### Astro Components

```typescript
import Header from '../components/Header.astro';
import Footer from './Footer.astro';
import Card from '@/components/Card.astro';  // With path alias
```

**Rules**:
- [ ] `.astro` extension required
- [ ] Relative path or path alias
- [ ] File exists at specified path

### Framework Components

```typescript
import ReactCounter from '../components/Counter.jsx';
import VueWidget from '../components/Widget.vue';
import SvelteCard from '../components/Card.svelte';
import SolidButton from '../components/Button.tsx';
```

**Rules**:
- [ ] Correct framework extension (`.jsx`, `.vue`, `.svelte`, `.tsx`)
- [ ] Framework integration installed
- [ ] Extension matches file type

## Type Imports

### Type-Only Imports

Use `import type` for TypeScript types:

✅ **CORRECT**: Type-only import
```typescript
import type { CollectionEntry } from 'astro:content';
import type { ImageMetadata } from 'astro';
import type { Props } from '../types';
```

**Benefits**:
- Removed at build time (no runtime cost)
- Clear intent (type vs value)
- Better tree-shaking

❌ **LESS OPTIMAL**: Runtime import for types
```typescript
import { CollectionEntry } from 'astro:content';  // Works, but includes in bundle
```

### Combined Imports

```typescript
import { getCollection, type CollectionEntry } from 'astro:content';
```

**Validation**:
- [ ] Types use `import type` or inline `type` keyword
- [ ] Reduces bundle size

## Static Asset Imports

### Images

```typescript
import logo from '../assets/logo.png';
import hero from '../assets/hero.jpg';
import icon from '../assets/icon.svg';
```

**Rules**:
- [ ] File in `src/assets/` or `public/`
- [ ] Supported format (PNG, JPG, SVG, WEBP, AVIF, GIF)
- [ ] Extension included

**Usage**:
```astro
---
import { Image } from 'astro:assets';
import photo from '../assets/photo.jpg';
---

<Image src={photo} alt="Photo" />
```

### JSON

```typescript
import data from '../data/config.json';
import posts from '../data/posts.json';
```

**Rules**:
- [ ] `.json` extension
- [ ] Valid JSON syntax in file

**Usage**:
```astro
---
import config from '../data/config.json';
---

<p>{config.siteName}</p>
```

### Markdown

```typescript
import post from '../posts/article.md';
import readme from '../README.md';
```

**Rules**:
- [ ] `.md` or `.mdx` extension
- [ ] Can access frontmatter and content

## CSS/Style Imports

### Global CSS

```typescript
import '../styles/global.css';
import '@fontsource/inter';
```

**Rules**:
- [ ] File ends in `.css`
- [ ] Import in layouts or pages
- [ ] Styles apply globally

### CSS Modules

```typescript
import styles from '../styles/component.module.css';
```

**Usage**:
```astro
<div class={styles.container}>
  <h1 class={styles.title}>Title</h1>
</div>
```

### Sass/SCSS

```typescript
import '../styles/main.scss';
import '../styles/layout.sass';
```

**Requirements**:
- [ ] Sass integration installed (`npm add sass`)
- [ ] Extension `.scss` or `.sass`

## Dynamic Imports

### Standard Dynamic Import

```typescript
const module = await import('../components/HeavyComponent.astro');
const Component = module.default;
```

**Use cases**:
- Conditional loading
- Code splitting
- Reducing initial bundle

### Glob Imports

**Pattern**: `import.meta.glob(pattern, options)`

```typescript
// All markdown files in posts directory
const posts = import.meta.glob('../posts/*.md');

// Eager loading
const posts = import.meta.glob('../posts/*.md', { eager: true });

// Specific imports
const components = import.meta.glob('../components/*.astro', {
  eager: true,
  import: 'default'
});
```

**CRITICAL RULES**:

1. **Pattern must be string literal** (not variable)

✅ **CORRECT**:
```typescript
const files = import.meta.glob('../posts/*.md');
```

❌ **INCORRECT**: Variable pattern
```typescript
const pattern = '../posts/*.md';
const files = import.meta.glob(pattern);  // ❌ ERROR
```

2. **Pattern must be relative** (`./`, `../`) or absolute (`/`)

✅ **CORRECT**:
```typescript
const files = import.meta.glob('../posts/*.md');     // ✅ Relative
const files = import.meta.glob('./posts/*.md');      // ✅ Relative
const files = import.meta.glob('/src/posts/*.md');   // ✅ Absolute
```

❌ **INCORRECT**: Non-relative pattern
```typescript
const files = import.meta.glob('posts/*.md');  // ❌ Must start with ./ or ../
```

3. **Glob patterns support**:
   - `*` - Matches any characters except `/`
   - `**` - Matches any characters including `/`
   - `{a,b}` - Matches `a` or `b`
   - `[abc]` - Matches `a`, `b`, or `c`

**Examples**:
```typescript
// All .astro files in components
const components = import.meta.glob('../components/*.astro');

// Nested directories
const all = import.meta.glob('../**/*.md');

// Multiple extensions
const content = import.meta.glob('../content/**/*.{md,mdx}');

// Specific files
const configs = import.meta.glob('../config/{dev,prod}.json', { eager: true });
```

## npm Package Imports

### Standard Packages

```typescript
import React from 'react';
import { format } from 'date-fns';
import _ from 'lodash';
```

**Rules**:
- [ ] Package installed in `package.json`
- [ ] No file extension
- [ ] Package name only

### Scoped Packages

```typescript
import { Card } from '@astrojs/starlight/components';
import theme from '@tailwindcss/typography';
```

**Rules**:
- [ ] Starts with `@scope/`
- [ ] Scope and package name

### Subpath Imports

```typescript
import debounce from 'lodash/debounce';
import { Button } from '@mui/material/Button';
```

**Benefits**:
- Better tree-shaking
- Smaller bundles
- Faster builds

## Path Aliases

### Configuration

```json
// tsconfig.json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@components/*": ["src/components/*"],
      "@layouts/*": ["src/layouts/*"]
    }
  }
}
```

### Usage

```typescript
import Layout from '@/layouts/Layout.astro';
import Header from '@components/Header.astro';
import { helper } from '@/utils/helpers.ts';
```

**Rules**:
- [ ] Aliases defined in tsconfig.json
- [ ] Still need file extensions
- [ ] Consistent usage across project

## Import Restrictions

### Node-Only Modules in Browser

❌ **INCORRECT**: Node modules in `<script>` tags
```astro
<script>
  import fs from 'node:fs';  // ❌ ERROR: Node API in browser
  import path from 'node:path';  // ❌ ERROR: Node API in browser
</script>
```

✅ **CORRECT**: Node modules in frontmatter
```astro
---
import fs from 'node:fs';  // ✅ OK: Server-side only
const content = fs.readFileSync('file.txt', 'utf-8');
---
```

### Internal Astro Modules

❌ **AVOID**: Importing from Astro internals
```typescript
import { something } from 'astro/internal/*';  // ❌ Internal API
import { util } from 'astro/runtime/server/*';  // ❌ Internal API
```

These are internal APIs and may change without notice.

## Validation Checklist

### File Extensions
- [ ] All relative imports include extensions
- [ ] Extensions match actual file types
- [ ] npm packages don't have extensions

### Module Specifiers
- [ ] Built-in modules use `astro:` prefix
- [ ] Not using `astro/` (slash) for built-ins
- [ ] Correct module names

### Import Types
- [ ] Type imports use `import type`
- [ ] Value imports are runtime-needed
- [ ] No unnecessary runtime imports

### Glob Patterns
- [ ] Glob patterns are string literals
- [ ] Patterns start with `./`, `../`, or `/`
- [ ] Not using variables for patterns

### Environment
- [ ] Node modules only in frontmatter
- [ ] No Node APIs in browser scripts
- [ ] Client/server separation respected

## Common Import Errors

| Error | Example | Fix |
|-------|---------|-----|
| Missing extension | `import X from './file'` | `import X from './file.astro'` |
| Wrong prefix | `import { X } from 'astro/content'` | `import { X } from 'astro:content'` |
| CommonJS | `require('./file')` | `import X from './file.astro'` |
| Variable glob | `glob(pattern)` | `glob('../*.md')` (literal) |
| Non-relative glob | `glob('posts/*.md')` | `glob('./posts/*.md')` |
| Node in browser | `<script>import fs</script>` | Move to frontmatter |
| No type import | `import { CollectionEntry }` | `import type { CollectionEntry }` |

## Performance Tips

### Prefer Specific Imports

❌ **LESS OPTIMAL**: Importing entire library
```typescript
import _ from 'lodash';
```

✅ **BETTER**: Import specific function
```typescript
import debounce from 'lodash/debounce';
```

### Use Type Imports

❌ **LESS OPTIMAL**: Runtime import for types
```typescript
import { CollectionEntry } from 'astro:content';
```

✅ **BETTER**: Type-only import
```typescript
import type { CollectionEntry } from 'astro:content';
```

### Lazy Load Heavy Components

```typescript
// Conditional dynamic import
if (shouldLoad) {
  const { HeavyChart } = await import('../components/HeavyChart.jsx');
}
```

## Import Order Convention

Recommended import ordering:

```typescript
// 1. Built-in Astro modules
import { getCollection } from 'astro:content';
import { Image } from 'astro:assets';

// 2. Framework components
import React from 'react';

// 3. npm packages
import { format } from 'date-fns';

// 4. Path aliases
import Layout from '@/layouts/Layout.astro';

// 5. Relative imports
import Header from '../components/Header.astro';
import { helper } from './utils.ts';

// 6. Type imports
import type { CollectionEntry } from 'astro:content';

// 7. Styles
import '../styles/global.css';

// 8. Assets
import logo from '../assets/logo.png';
```
