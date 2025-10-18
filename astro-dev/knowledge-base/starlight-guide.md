# Starlight Documentation Guide

**Complete guide for building documentation sites with Starlight.**

## Project Setup

### Basic Configuration

```typescript
// astro.config.mjs
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  integrations: [
    starlight({
      title: 'My Documentation',
      description: 'Comprehensive docs',

      social: [
        { icon: 'github', label: 'GitHub', href: 'https://github.com/user/repo' },
        { icon: 'discord', label: 'Discord', href: 'https://discord.gg/invite' },
      ],

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

      customCss: ['./src/styles/custom.css'],
      logo: { src: './src/assets/logo.svg' },

      editLink: {
        baseUrl: 'https://github.com/user/repo/edit/main/',
      },
      lastUpdated: true,
    }),
  ],
});
```

---

### Content Configuration

```typescript
// src/content.config.ts
import { defineCollection } from 'astro:content';
import { docsLoader } from '@astrojs/starlight/loaders';
import { docsSchema } from '@astrojs/starlight/schema';

export const collections = {
  // MUST be named 'docs'
  docs: defineCollection({
    loader: docsLoader(),
    schema: docsSchema(),
  }),
};
```

**Critical**: Collection MUST be named `'docs'` for Starlight to work.

---

## Page Types

### Standard Doc Page

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

**Features**:
- Sidebar navigation
- Table of contents (TOC)
- Breadcrumbs
- Edit link
- Pagination (prev/next)

---

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

**Features**:
- Full-width layout
- No sidebar
- No table of contents
- Hero section
- Ideal for landing pages

---

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

**CRITICAL**: Import `StarlightPage` first to establish CSS cascade.

---

## Frontmatter Reference

### Required Fields

**`title`** - Page heading (REQUIRED)

### Common Optional Fields

```markdown
---
title: My Page
description: SEO description
slug: custom-url-path
template: doc  # or 'splash'

# Table of contents
tableOfContents:
  minHeadingLevel: 2
  maxHeadingLevel: 3

# Navigation
prev: false  # Hide prev link
next:
  label: Custom Next
  link: /custom-path

# Sidebar
sidebar:
  label: Custom Label
  order: 1
  badge:
    text: New
    variant: tip
  hidden: false

# Publishing
draft: false
pagefind: true
lastUpdated: 2024-08-13

# Edit link
editUrl: false  # or custom URL

# Banner
banner:
  content: Important announcement here
---
```

---

## Sidebar Configuration

### Auto-Generated

```typescript
// astro.config.mjs
starlight({
  sidebar: [
    {
      label: 'API Reference',
      autogenerate: { directory: 'api' },
    },
  ],
})
```

---

### Manual

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

---

### Mixed (Auto + Manual)

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
      {
        label: 'Discord',
        link: 'https://discord.gg/invite',
        attrs: { target: '_blank' }
      },
    ],
  },
]
```

---

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

---

## Built-in Components

### Tabs

```markdown
import { Tabs, TabItem } from '@astrojs/starlight/components';

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
```

---

### Cards

```markdown
import { Card, CardGrid } from '@astrojs/starlight/components';

<CardGrid>
  <Card title="API Reference" icon="document">
    [View the complete API documentation](/api)
  </Card>

  <Card title="Examples" icon="open-book">
    [Check out example projects](/examples)
  </Card>
</CardGrid>
```

---

### Asides (Callouts)

```markdown
import { Aside } from '@astrojs/starlight/components';

<Aside type="note">
  This is a note callout.
</Aside>

<Aside type="tip" title="Pro Tip">
  This is a custom-titled tip.
</Aside>

<Aside type="caution">
  Be careful with this configuration.
</Aside>

<Aside type="danger">
  This action cannot be undone!
</Aside>
```

**Or use Markdown syntax**:
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

---

### Code Blocks

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

---

## Component Overrides

### Configuration

```typescript
// astro.config.mjs
starlight({
  title: 'My Docs',
  components: {
    Footer: './src/components/Footer.astro',
    SocialIcons: './src/components/SocialIcons.astro',
    PageTitle: './src/components/PageTitle.astro',
  },
})
```

---

### Custom Footer Example

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
    <p>&copy; {new Date().getFullYear()} My Company</p>
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

---

## Route Data Access

### Using starlightRoute

```astro
---
const { id, entry, hasSidebar, pagination } = Astro.locals.starlightRoute;
const { title, description } = entry.data;
---

<!-- Conditional rendering -->
{id.startsWith('api/') && (
  <div class="api-notice">
    This is API documentation
  </div>
)}

<!-- Navigation -->
<nav class="pagination">
  {pagination.prev && (
    <a href={pagination.prev.href}>
      ← {pagination.prev.label}
    </a>
  )}

  {pagination.next && (
    <a href={pagination.next.href}>
      {pagination.next.label} →
    </a>
  )}
</nav>
```

**Available properties**:
- `id` - Page identifier
- `entry` - Content collection entry
- `sidebar` - Navigation sidebar
- `hasSidebar` - Sidebar visibility
- `pagination` - Prev/next links
- `toc` - Table of contents
- `headings` - All markdown headings
- `lastUpdated` - Last update timestamp
- `editUrl` - Edit link URL

---

## Internationalization

### Setup

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
    en: { label: 'English', lang: 'en' },
    es: { label: 'Español', lang: 'es' },
    fr: { label: 'Français', lang: 'fr' },
  },
})
```

---

### Content Structure

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

**Fallback**: Pages without translation automatically use default locale content.

---

## Styling Customization

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

---

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

---

## Search Configuration

### Default (Pagefind)

Starlight includes Pagefind search by default - no configuration needed.

---

### Excluding Pages

```markdown
---
title: Draft Page
pagefind: false
---

This page won't appear in search results.
```

---

### Custom Search

```typescript
// astro.config.mjs
starlight({
  pagefind: false,  // Disable default search
  components: {
    Search: './src/components/CustomSearch.astro',
  },
})
```

---

## Key Patterns Summary

**Setup**:
1. Use `docsLoader()` and `docsSchema()` in content.config.ts
2. Collection MUST be named `'docs'`
3. Configure in astro.config.mjs

**Page Types**:
1. Standard doc page (template: 'doc') - Default with sidebar
2. Splash page (template: 'splash') - Landing page layout
3. Custom pages with StarlightPage component

**Frontmatter**:
- Only `title` is required
- Use `description` for SEO
- `template: splash` for landing pages

**Content**:
- Files in `src/content/docs/`
- Auto-routing from file structure
- Import Starlight components from `@astrojs/starlight/components`

**Customization**:
- Override components in config
- Use Starlight CSS variables
- Access route data via `Astro.locals.starlightRoute`

**i18n**:
- Locale-based directory structure
- Automatic fallback to default locale
- Configure in astro.config.mjs

**Navigation**:
- Auto-generated or manual sidebar
- Per-page sidebar customization
- Built-in pagination support
