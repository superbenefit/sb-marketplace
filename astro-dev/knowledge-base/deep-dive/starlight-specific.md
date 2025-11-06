# Starlight-Specific Content & Pages Reference

This document provides comprehensive reference for Starlight's content structure, page types, routing, frontmatter, and unique features.

## Content Structure

### File Organization

**Primary content location:** `src/content/docs/`

**Supported formats:**
- Markdown (`.md`)
- MDX (`.mdx`)
- Markdoc (`.mdoc`) - with experimental integration

**Routing:**
```
src/content/docs/
├── index.mdx                → /
├── hello-world.md           → /hello-world
└── reference/
    └── faq.md               → /reference/faq
```

**Documentation:** https://starlight.astro.build/guides/pages/

### Content Collections Configuration

**File:** `src/content.config.ts`

**Starlight pattern:**
```typescript
import { defineCollection } from 'astro:content';
import { docsLoader } from '@astrojs/starlight/loaders';
import { docsSchema } from '@astrojs/starlight/schema';

export const collections = {
  docs: defineCollection({
    loader: docsLoader(),
    schema: docsSchema(),
  }),
};
```

**Key components:**
- `docsLoader()`: Loads content from `src/content/docs/`
- `docsSchema()`: Provides Starlight's frontmatter schema with validation

**Documentation:** https://starlight.astro.build/guides/project-structure/

## Page Types

### Standard Doc Pages

**Default template:** `'doc'`

**Features:**
- Sidebar navigation
- Table of contents (TOC)
- Breadcrumbs
- Edit link
- Pagination (prev/next)

**Frontmatter:**
```yaml
---
title: Page Title
description: Page description for SEO
---
```

### Splash Pages

**Template:** `'splash'`

**Features:**
- Full-width layout
- No sidebar
- No table of contents
- Ideal for landing pages

**Frontmatter:**
```yaml
---
title: Welcome
template: splash
hero:
  title: Your App Name
  tagline: Build amazing docs
  image:
    file: ../../assets/logo.png
  actions:
    - text: Get Started
      link: /getting-started
      icon: right-arrow
      variant: primary
---
```

**Documentation:** https://starlight.astro.build/guides/customization/#page-layout

## Custom Pages with StarlightPage

### Creating Custom Routes

**Directory:** `src/pages/`

**Using StarlightPage component:**

```astro
---
import StarlightPage from '@astrojs/starlight/components/StarlightPage.astro';
---

<StarlightPage frontmatter={{ title: 'Custom page' }}>
  <p>This is a custom page with Starlight styling.</p>
</StarlightPage>
```

**CRITICAL:** Import `StarlightPage` first to establish CSS cascade layers.

### StarlightPage Props

| Prop | Type | Required | Notes |
|------|------|----------|-------|
| `frontmatter` | `StarlightPageFrontmatter` | Yes | Must include `title`; `slug` auto-generated |
| `sidebar` | `SidebarEntry[]` | No | Override default sidebar |
| `hasSidebar` | `boolean` | No | Control sidebar visibility |
| `headings` | `{ depth: number; slug: string; text: string; }[]` | No | Custom TOC headings |
| `dir` | `'ltr' \| 'rtl'` | No | Text direction |
| `lang` | `string` | No | Page language |
| `isFallback` | `boolean` | No | Marks translated fallback |

**Documentation:** https://starlight.astro.build/guides/pages/#_top

## Frontmatter Reference

### Required Fields

**`title`** (string)
- Page heading
- Browser tab title
- Used in metadata

### Optional Fields

#### Content & Metadata

**`description`** (string)
- SEO metadata
- Social media previews
- Search engine descriptions

**`slug`** (string)
- Override page URL
- Custom route path

**`editUrl`** (string | boolean)
- Control "Edit page" link
- Set to `false` to disable
- Provide custom URL to override

#### Layout

**`template`** (`'doc'` | `'splash'`)
- `'doc'`: Standard layout (default)
- `'splash'`: Wide landing page layout

**`hero`** (HeroConfig)
- Hero section for page top
- Includes title, tagline, image, actions

**`banner`** ({ content: string })
- Announcement banner
- Supports HTML content

**`tableOfContents`** (false | object)
- Customize TOC heading levels
- Set to `false` to disable
```yaml
tableOfContents:
  minHeadingLevel: 2
  maxHeadingLevel: 3
```

#### Navigation

**`prev`** (boolean | string | object)
- Override previous page link
- Set to `false` to hide

**`next`** (boolean | string | object)
- Override next page link
- Set to `false` to hide

#### Sidebar

**`sidebar`** (SidebarConfig)
- `label`: Override sidebar label
- `order`: Custom sort order
- `hidden`: Hide from sidebar
- `badge`: Display badge
- `attrs`: Custom HTML attributes

#### Publishing

**`draft`** (boolean)
- Mark as draft
- Excluded from production builds

**`pagefind`** (boolean)
- Include in search index (default: `true`)
- Set to `false` to exclude

**`lastUpdated`** (Date | boolean)
- Override Git-based date
- Use YAML date format: `2024-08-13`

#### Advanced

**`head`** (HeadConfig[])
- Add custom `<head>` tags
- Scripts, styles, meta tags

```yaml
head:
  - tag: script
    attrs:
      src: /analytics.js
```

**Documentation:** https://starlight.astro.build/reference/frontmatter/

## Hero Configuration

**Usage with splash template:**

```yaml
---
template: splash
hero:
  title: Welcome to Docs
  tagline: Learn everything you need
  image:
    file: ../../assets/hero.png
    alt: App screenshot
  actions:
    - text: Get Started
      link: /getting-started
      icon: right-arrow
      variant: primary
    - text: View on GitHub
      link: https://github.com/example/repo
      icon: external
      variant: minimal
---
```

**Image variants:**
```yaml
hero:
  image:
    light: ../../assets/hero-light.png
    dark: ../../assets/hero-dark.png
    alt: Product screenshot
```

**Action variants:**
- `primary`: Prominent button
- `secondary`: Standard button
- `minimal`: Text link style

## Route Data

### Accessing starlightRoute

**Location:** `Astro.locals.starlightRoute`

**Usage in components:**
```astro
---
const { hasSidebar, siteTitle } = Astro.locals.starlightRoute;
const { title } = Astro.locals.starlightRoute.entry.data;
---
```

### Route Data Properties

| Property | Type | Description |
|----------|------|-------------|
| `id` | `string` | Page identifier from filename |
| `slug` | `string` | Deprecated - use `id` |
| `lang` | `string` | BCP-47 language tag |
| `dir` | `'ltr' \| 'rtl'` | Text direction |
| `locale` | `string \| undefined` | Locale base path |
| `siteTitle` | `string` | Localized site title |
| `siteTitleHref` | `string` | Homepage link |
| `entry` | `CollectionEntry` | Content collection entry |
| `entryMeta` | `{ dir, lang }` | Entry locale metadata |
| `isFallback` | `boolean \| undefined` | Using fallback translation |
| `sidebar` | `SidebarEntry[]` | Navigation sidebar |
| `hasSidebar` | `boolean` | Sidebar visibility |
| `pagination` | `{ prev?, next? }` | Page navigation |
| `toc` | `object \| undefined` | Table of contents |
| `headings` | `Heading[]` | All markdown headings |
| `lastUpdated` | `Date` | Last update timestamp |
| `editUrl` | `URL` | Edit link URL |

**Documentation:** https://starlight.astro.build/reference/route-data/

### Use Cases

**Conditional rendering:**
```astro
---
const isHomepage = Astro.locals.starlightRoute.id === '';
---

{isHomepage ? (
  <div>Welcome home!</div>
) : (
  <div>Regular page</div>
)}
```

**Custom footer by page:**
```astro
---
const { id } = Astro.locals.starlightRoute;
---

{id.startsWith('api/') ? (
  <footer>API Documentation</footer>
) : (
  <footer>General Documentation</footer>
)}
```

## Component Overrides

Starlight supports overriding built-in components via configuration.

### Override Configuration

**In `astro.config.mjs`:**
```javascript
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  integrations: [
    starlight({
      title: 'My Docs',
      components: {
        SocialIcons: './src/components/CustomSocialIcons.astro',
        PageTitle: './src/components/CustomPageTitle.astro',
        Footer: './src/components/CustomFooter.astro',
      },
    }),
  ],
});
```

### Overridable Components

**Page structure:**
- `PageFrame`: Main page container
- `TwoColumnContent`: Two-column layout
- `PageTitle`: Page heading
- `Footer`: Page footer

**Navigation:**
- `SidebarToggle`: Mobile menu toggle
- `MobileMenuFooter`: Mobile menu footer
- `PageSidebar`: Sidebar wrapper
- `Sidebar`: Sidebar content
- `TableOfContents`: TOC component

**Content:**
- `Hero`: Hero section
- `Head`: Document head
- `ThemeProvider`: Theme management

**Social & Search:**
- `SocialIcons`: Social links
- `Search`: Search component

**Documentation:** https://starlight.astro.build/guides/overriding-components/

### Using Page Data in Overrides

```astro
---
// src/components/CustomFooter.astro
import Default from '@astrojs/starlight/components/Footer.astro';

const { entry } = Astro.locals.starlightRoute;
const showCustomFooter = entry.data.customFooter;
---

{showCustomFooter ? (
  <footer class="custom">Custom footer content</footer>
) : (
  <Default><slot /></Default>
)}
```

## Sidebar Configuration

### Automatic Generation

**By default:** Sidebar auto-generated from `src/content/docs/` structure

### Manual Configuration

**In `astro.config.mjs`:**
```javascript
starlight({
  sidebar: [
    { label: 'Start Here', slug: 'index' },
    {
      label: 'Guides',
      items: [
        { label: 'Getting Started', slug: 'guides/getting-started' },
        { label: 'Advanced', slug: 'guides/advanced' },
      ],
    },
    {
      label: 'Reference',
      autogenerate: { directory: 'reference' },
    },
  ],
})
```

### Sidebar Frontmatter Overrides

```yaml
---
title: My Page
sidebar:
  label: Custom Label
  order: 1
  badge:
    text: New
    variant: tip
  hidden: false
---
```

**Documentation:** https://starlight.astro.build/reference/configuration/#sidebar

## Internationalization

### Setup

**In `astro.config.mjs`:**
```javascript
starlight({
  title: {
    en: 'My Docs',
    es: 'Mis Documentos',
  },
  defaultLocale: 'en',
  locales: {
    en: { label: 'English', lang: 'en' },
    es: { label: 'Español', lang: 'es' },
    'pt-br': { label: 'Português do Brasil', lang: 'pt-BR' },
  },
})
```

### Content Structure

```
src/content/docs/
├── en/
│   └── guide.md          → /en/guide
├── es/
│   └── guide.md          → /es/guide
└── pt-br/
    └── guide.md          → /pt-br/guide
```

### Fallback Content

Pages without translation use default locale content automatically. `starlightRoute.isFallback` indicates fallback usage.

**Documentation:** https://starlight.astro.build/guides/i18n/

## Key Patterns Summary

1. **Content in** `src/content/docs/` for auto-processing
2. **Custom pages in** `src/pages/` with `StarlightPage` component
3. **Two templates:** `'doc'` (default) and `'splash'` (landing)
4. **Frontmatter required:** Only `title` is mandatory
5. **Route data access:** Via `Astro.locals.starlightRoute`
6. **Component overrides:** Configure in `components` option
7. **Sidebar:** Auto-generated or manually configured
8. **i18n:** Locale-based directory structure with fallbacks

## Documentation References

- **Pages Guide:** https://starlight.astro.build/guides/pages/
- **Authoring Content:** https://starlight.astro.build/guides/authoring-content/
- **Project Structure:** https://starlight.astro.build/guides/project-structure/
- **Route Data Guide:** https://starlight.astro.build/guides/route-data/
- **Route Data Reference:** https://starlight.astro.build/reference/route-data/
- **Frontmatter Reference:** https://starlight.astro.build/reference/frontmatter/
- **Configuration Reference:** https://starlight.astro.build/reference/configuration/
- **Overriding Components:** https://starlight.astro.build/guides/overriding-components/
