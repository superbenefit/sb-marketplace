# Starlight Development Patterns

This document provides implementation patterns specific to Starlight documentation sites.

## Project Configuration

### Basic Starlight Setup

```typescript
// astro.config.mjs
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  integrations: [
    starlight({
      title: 'My Documentation',
      description: 'Comprehensive docs for my project',

      // Social links
      social: [
        { icon: 'github', label: 'GitHub', href: 'https://github.com/user/repo' },
        { icon: 'discord', label: 'Discord', href: 'https://discord.gg/invite' },
      ],

      // Sidebar configuration
      sidebar: [
        {
          label: 'Getting Started',
          items: [
            { label: 'Introduction', slug: 'index' },
            { label: 'Installation', slug: 'getting-started/installation' },
          ],
        },
        {
          label: 'Guides',
          autogenerate: { directory: 'guides' },
        },
      ],

      // Customization
      customCss: ['./src/styles/custom.css'],
      logo: {
        src: './src/assets/logo.svg',
      },

      // Features
      editLink: {
        baseUrl: 'https://github.com/user/repo/edit/main/',
      },
      lastUpdated: true,
    }),
  ],
});
```

### Content Configuration

```typescript
// src/content.config.ts
import { defineCollection } from 'astro:content';
import { docsLoader } from '@astrojs/starlight/loaders';
import { docsSchema } from '@astrojs/starlight/schema';

export const collections = {
  // Starlight docs collection (required name: 'docs')
  docs: defineCollection({
    loader: docsLoader(),
    schema: docsSchema(),
  }),
};
```

## Page Patterns

### Standard Documentation Page

```markdown
---
title: Getting Started
description: Learn how to get started with our project
---

# Getting Started

This guide will help you get up and running quickly.

## Installation

Install the package using npm:

\`\`\`bash
npm install my-package
\`\`\`

## Basic Usage

Here's a simple example:

\`\`\`typescript
import { myFunction } from 'my-package';

myFunction();
\`\`\`
```

### Splash Page (Landing)

```markdown
---
title: Welcome
template: splash
hero:
  title: 'My Awesome Project'
  tagline: Build amazing things faster
  image:
    file: ../../assets/hero.webp
    alt: Project screenshot
  actions:
    - text: Get Started
      link: /getting-started/installation
      icon: right-arrow
      variant: primary
    - text: View on GitHub
      link: https://github.com/user/repo
      icon: external
      variant: minimal
---

import { Card, CardGrid } from '@astrojs/starlight/components';

## Why Choose Us?

<CardGrid>
  <Card title="Fast" icon="rocket">
    Lightning-fast performance out of the box.
  </Card>

  <Card title="Flexible" icon="puzzle">
    Customize everything to match your needs.
  </Card>

  <Card title="Developer Friendly" icon="seti:typescript">
    Full TypeScript support and great DX.
  </Card>
</CardGrid>
```

### Custom Page with StarlightPage

```astro
---
// src/pages/custom.astro
import StarlightPage from '@astrojs/starlight/components/StarlightPage.astro';

const data = await fetch('https://api.example.com/stats').then(r => r.json());
---

<StarlightPage frontmatter={{ title: 'Live Stats' }}>
  <h2>Current Statistics</h2>

  <div class="stats-grid">
    <div class="stat">
      <span class="label">Users</span>
      <span class="value">{data.users}</span>
    </div>

    <div class="stat">
      <span class="label">Downloads</span>
      <span class="value">{data.downloads}</span>
    </div>
  </div>
</StarlightPage>

<style>
  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin-top: 2rem;
  }

  .stat {
    padding: 1.5rem;
    border: 1px solid var(--sl-color-gray-5);
    border-radius: 0.5rem;
  }

  .label {
    display: block;
    font-size: 0.875rem;
    color: var(--sl-color-gray-3);
  }

  .value {
    display: block;
    font-size: 2rem;
    font-weight: bold;
    margin-top: 0.5rem;
  }
</style>
```

## Component Override Patterns

### Custom Footer

```astro
---
// src/components/Footer.astro
import type { Props } from '@astrojs/starlight/props';
import Default from '@astrojs/starlight/components/Footer.astro';

const { entry } = Astro.locals.starlightRoute;
const showCustomFooter = entry.data.customFooter ?? false;
---

{showCustomFooter ? (
  <footer class="custom-footer">
    <p>Custom footer content for this page</p>
    <p>© {new Date().getFullYear()} My Company</p>
  </footer>
) : (
  <Default {...Astro.props}><slot /></Default>
)}

<style>
  .custom-footer {
    padding: 2rem;
    text-align: center;
    border-top: 1px solid var(--sl-color-gray-5);
  }
</style>
```

```typescript
// astro.config.mjs - Register override
starlight({
  components: {
    Footer: './src/components/Footer.astro',
  },
})
```

### Custom Social Icons

```astro
---
// src/components/SocialIcons.astro
import type { Props } from '@astrojs/starlight/props';
import Default from '@astrojs/starlight/components/SocialIcons.astro';
---

<Default {...Astro.props} />

<!-- Add custom social link -->
<a href="https://youtube.com/@myhandle" rel="me" class="sl-flex">
  <span class="sr-only">YouTube</span>
  <svg aria-hidden="true" width="16" height="16" viewBox="0 0 24 24">
    <path fill="currentColor" d="M23.498 6.186..."/>
  </svg>
</a>
```

## Sidebar Patterns

### Manual Sidebar

```typescript
sidebar: [
  {
    label: 'Start Here',
    items: [
      { label: 'Introduction', slug: 'index' },
      { label: 'Quick Start', slug: 'quick-start' },
    ],
  },
  {
    label: 'Core Concepts',
    badge: { text: 'New', variant: 'tip' },
    items: [
      { label: 'Architecture', slug: 'concepts/architecture' },
      { label: 'Data Flow', slug: 'concepts/data-flow' },
    ],
  },
]
```

### Auto-Generated Sidebar

```typescript
sidebar: [
  {
    label: 'API Reference',
    autogenerate: { directory: 'api' },
  },
]
```

### Mixed Sidebar

```typescript
sidebar: [
  // Manual entries
  {
    label: 'Getting Started',
    items: [
      { label: 'Introduction', slug: 'index' },
    ],
  },

  // Auto-generated section
  {
    label: 'Guides',
    autogenerate: { directory: 'guides' },
  },

  // External link
  {
    label: 'Community',
    items: [
      { label: 'Discord', link: 'https://discord.gg/invite', attrs: { target: '_blank' } },
    ],
  },
]
```

### Per-Page Sidebar Customization

```markdown
---
title: Special Page
sidebar:
  label: Custom Label
  order: 1
  badge:
    text: Beta
    variant: caution
  hidden: false
---
```

## Internationalization Patterns

### i18n Configuration

```typescript
// astro.config.mjs
starlight({
  title: {
    en: 'My Docs',
    es: 'Mis Documentos',
    fr: 'Ma Documentation',
  },
  defaultLocale: 'en',
  locales: {
    en: {
      label: 'English',
      lang: 'en',
    },
    es: {
      label: 'Español',
      lang: 'es',
    },
    fr: {
      label: 'Français',
      lang: 'fr',
    },
  },
})
```

### Localized Content Structure

```
src/content/docs/
├── en/
│   ├── index.md           → /en/
│   └── guide.md           → /en/guide
├── es/
│   ├── index.md           → /es/
│   └── guide.md           → /es/guide
└── fr/
    ├── index.md           → /fr/
    └── guide.md           → /fr/guide
```

### Fallback Content

```markdown
<!-- en/advanced.md exists, es/advanced.md doesn't -->
<!-- Visitors to /es/advanced see English content with fallback indicator -->
```

## Route Data Usage Patterns

### Conditional Rendering Based on Route

```astro
---
const { id, entry } = Astro.locals.starlightRoute;
const isApiDoc = id.startsWith('api/');
const showTOC = entry.data.tableOfContents !== false;
---

{isApiDoc && (
  <div class="api-notice">
    This is API documentation
  </div>
)}

{showTOC && (
  <nav class="toc">
    <!-- Table of contents -->
  </nav>
)}
```

### Accessing Entry Data

```astro
---
const { entry } = Astro.locals.starlightRoute;
const { title, description, lastUpdated } = entry.data;
---

<article>
  <h1>{title}</h1>
  <p class="description">{description}</p>
  {lastUpdated && (
    <time datetime={lastUpdated.toISOString()}>
      Last updated: {lastUpdated.toLocaleDateString()}
    </time>
  )}
</article>
```

### Navigation with Pagination

```astro
---
const { pagination } = Astro.locals.starlightRoute;
---

<nav class="pagination">
  {pagination.prev && (
    <a href={pagination.prev.href} rel="prev">
      ← {pagination.prev.label}
    </a>
  )}

  {pagination.next && (
    <a href={pagination.next.href} rel="next">
      {pagination.next.label} →
    </a>
  )}
</nav>
```

## Styling Patterns

### Custom CSS Variables

```css
/* src/styles/custom.css */
:root {
  --sl-color-accent: hsl(250, 90%, 60%);
  --sl-color-accent-high: hsl(250, 90%, 70%);

  --sl-font-system: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;

  --sl-sidebar-width: 20rem;
}

/* Dark mode overrides */
:root[data-theme='dark'] {
  --sl-color-accent: hsl(250, 90%, 70%);
}
```

### Scoped Component Styles

```astro
<div class="feature-box">
  <h3>Feature Title</h3>
  <p>Feature description</p>
</div>

<style>
  .feature-box {
    padding: var(--sl-spacing-large);
    background: var(--sl-color-bg-accent);
    border-radius: var(--sl-radius-medium);
  }

  .feature-box h3 {
    color: var(--sl-color-white);
    margin-bottom: var(--sl-spacing-small);
  }
</style>
```

## Content Authoring Patterns

### Using Starlight Components

```markdown
---
title: Example Page
---

import { Tabs, TabItem } from '@astrojs/starlight/components';
import { Code } from '@astrojs/starlight/components';
import { Card, CardGrid } from '@astrojs/starlight/components';
import { Aside } from '@astrojs/starlight/components';

## Installation

<Tabs>
  <TabItem label="npm">
    \`\`\`bash
    npm install my-package
    \`\`\`
  </TabItem>

  <TabItem label="pnpm">
    \`\`\`bash
    pnpm add my-package
    \`\`\`
  </TabItem>

  <TabItem label="yarn">
    \`\`\`bash
    yarn add my-package
    \`\`\`
  </TabItem>
</Tabs>

## Important Note

<Aside type="caution">
  Make sure to configure your environment variables before running.
</Aside>

## Related Resources

<CardGrid>
  <Card title="API Reference" icon="document">
    [View the complete API documentation](/api)
  </Card>

  <Card title="Examples" icon="open-book">
    [Check out example projects](/examples)
  </Card>
</CardGrid>
```

### Code Blocks with Highlights

````markdown
```typescript {2-4} title="config.ts"
export const config = {
  // These lines are highlighted
  apiKey: process.env.API_KEY,
  endpoint: 'https://api.example.com',
  timeout: 5000,
};
```
````

### Asides/Callouts

```markdown
:::note
This is a note callout.
:::

:::tip[Pro Tip]
This is a custom-titled tip.
:::

:::caution
Be careful with this configuration.
:::

:::danger
This action cannot be undone!
:::
```

## Dynamic Content Patterns

### Generating Pages from API Data

```typescript
// src/pages/changelog/[version].astro
---
export async function getStaticPaths() {
  const releases = await fetch('https://api.github.com/repos/user/repo/releases')
    .then(r => r.json());

  return releases.map((release) => ({
    params: { version: release.tag_name },
    props: { release },
  }));
}

import StarlightPage from '@astrojs/starlight/components/StarlightPage.astro';

const { release } = Astro.props;
---

<StarlightPage
  frontmatter={{
    title: `Release ${release.tag_name}`,
    description: `Changelog for version ${release.tag_name}`,
  }}
>
  <article set:html={release.body_html} />
</StarlightPage>
```

## Search Configuration

### Default Pagefind Search

Starlight includes Pagefind search by default - no configuration needed.

### Excluding Pages from Search

```markdown
---
title: Draft Page
pagefind: false
---

This page won't appear in search results.
```

### Custom Search Implementation

```typescript
// astro.config.mjs
starlight({
  pagefind: false,  // Disable default search
  components: {
    Search: './src/components/CustomSearch.astro',
  },
})
```

## Key Patterns Summary

1. ✅ Use `docsLoader()` and `docsSchema()` for Starlight collections
2. ✅ Name collection `'docs'` (required by Starlight)
3. ✅ Use `template: splash` for landing pages
4. ✅ Import Starlight components from `@astrojs/starlight/components`
5. ✅ Access route data via `Astro.locals.starlightRoute`
6. ✅ Override components by registering in `components` config
7. ✅ Use Starlight CSS variables for consistent theming
8. ✅ Organize i18n content by locale subdirectories
9. ✅ Use `StarlightPage` component for custom pages
10. ✅ Leverage auto-generated sidebar for large doc sets
