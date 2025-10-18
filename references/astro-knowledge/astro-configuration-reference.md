# Astro Configuration Reference

**Source**: https://docs.astro.build/en/reference/configuration-reference/

This document provides validation rules for `astro.config.mjs`.

## Configuration File Basics

### File Location

```
project-root/
└── astro.config.mjs  (or .ts, .cjs, .mjs)
```

### Basic Structure

```javascript
// astro.config.mjs
import { defineConfig } from 'astro/config';

export default defineConfig({
  // Configuration options
});
```

**Validation**:
- [ ] File exports `defineConfig()` result
- [ ] Import from `'astro/config'`
- [ ] Single default export

## Top-Level Options

### Project Directories

#### `root`
**Type**: `string`
**Default**: `'.'` (current directory)
**Description**: Project root directory

```javascript
export default defineConfig({
  root: './my-project',
});
```

**Validation**:
- [ ] Must be valid directory path
- [ ] Directory must exist
- [ ] Usually not needed (defaults to current directory)

#### `srcDir`
**Type**: `string`
**Default**: `'./src'`
**Description**: Source files directory

```javascript
export default defineConfig({
  srcDir: './source',
});
```

**Validation**:
- [ ] Must be valid directory path
- [ ] Relative to `root`

#### `publicDir`
**Type**: `string`
**Default**: `'./public'`
**Description**: Static assets directory

```javascript
export default defineConfig({
  publicDir: './static',
});
```

**Validation**:
- [ ] Must be valid directory path
- [ ] Files copied to build output as-is

#### `outDir`
**Type**: `string`
**Default**: `'./dist'`
**Description**: Build output directory

```javascript
export default defineConfig({
  outDir: './build',
});
```

**Validation**:
- [ ] Must be valid directory path
- [ ] Will be created if doesn't exist

### Site Metadata

#### `site`
**Type**: `string` (URL)
**Default**: `undefined`
**Description**: Deployed site URL

```javascript
export default defineConfig({
  site: 'https://example.com',
});
```

**Validation**:
- [ ] Must be valid URL
- [ ] Must start with `http://` or `https://`
- [ ] Required for:
  - Sitemaps
  - RSS feeds
  - Canonical URLs
  - Open Graph tags

❌ **INCORRECT**:
```javascript
site: 'example.com',           // ❌ Missing protocol
site: 'http://localhost:3000',  // ⚠️ Don't use localhost for production
```

✅ **CORRECT**:
```javascript
site: 'https://example.com',
site: 'https://www.example.com',
site: 'https://subdomain.example.com',
```

#### `base`
**Type**: `string`
**Default**: `'/'`
**Description**: Base path for deployment

```javascript
export default defineConfig({
  base: '/my-site',
});
```

**Validation**:
- [ ] Must start with `/`
- [ ] Must end with `/` (or be `/`)
- [ ] Used when deploying to subdirectory

❌ **INCORRECT**:
```javascript
base: 'my-site',      // ❌ Must start with /
base: '/my-site',     // ⚠️ Should end with / for consistency
```

✅ **CORRECT**:
```javascript
base: '/',
base: '/docs/',
base: '/v2/docs/',
```

#### `trailingSlash`
**Type**: `'always' | 'never' | 'ignore'`
**Default**: `'ignore'`
**Description**: URL trailing slash behavior

```javascript
export default defineConfig({
  trailingSlash: 'always',  // /about/ (with slash)
  trailingSlash: 'never',   // /about (without slash)
  trailingSlash: 'ignore',  // Both work
});
```

**Validation**:
- [ ] Must be one of: `'always'`, `'never'`, `'ignore'`
- [ ] Affects URL routing and redirects

### Build Configuration

#### `output`
**Type**: `'static' | 'server'`
**Default**: `'static'`
**Description**: Build output type

```javascript
export default defineConfig({
  output: 'static',  // Static site generation (SSG)
  output: 'server',  // Server-side rendering (SSR)
});
```

**Validation**:
- [ ] Must be `'static'` or `'server'`
- [ ] `'static'`: Pre-renders all pages
- [ ] `'server'`: On-demand rendering

❌ **INCORRECT**:
```javascript
output: 'ssr',       // ❌ Use 'server'
output: 'hybrid',    // ❌ Not valid, use 'server' with prerender
```

#### `adapter`
**Type**: Adapter object
**Default**: `undefined`
**Required**: When `output: 'server'`

```javascript
import netlify from '@astrojs/netlify';

export default defineConfig({
  output: 'server',
  adapter: netlify(),
});
```

**Validation**:
- [ ] Required when `output: 'server'`
- [ ] Adapter package must be installed
- [ ] Adapter must be called as function

### Integrations

#### `integrations`
**Type**: `Array<Integration>`
**Default**: `[]`

```javascript
import react from '@astrojs/react';
import tailwind from '@astrojs/tailwind';
import starlight from '@astrojs/starlight';

export default defineConfig({
  integrations: [
    react(),
    tailwind(),
    starlight({
      title: 'My Docs',
    }),
  ],
});
```

**Validation**:
- [ ] Must be array
- [ ] Each integration must be called as function
- [ ] Integration packages must be installed
- [ ] Order may matter for some integrations

❌ **INCORRECT**:
```javascript
integrations: [react],  // ❌ Missing () - must call function
integrations: react(),  // ❌ Must be array
```

### Environment Variables (v5.0+)

#### `env`
**Type**: Environment configuration object
**Default**: `undefined`

```javascript
import { defineConfig, envField } from 'astro/config';

export default defineConfig({
  env: {
    schema: {
      PUBLIC_API_URL: envField.string({
        context: 'client',
        access: 'public',
      }),
      SECRET_API_KEY: envField.string({
        context: 'server',
        access: 'secret',
      }),
    },
    validateSecrets: true,
  },
});
```

**Field Types**:
- `envField.string(options)`
- `envField.number(options)`
- `envField.boolean(options)`
- `envField.enum(options)`

**Required Options**:
- `context`: `'client'` | `'server'`
- `access`: `'public'` | `'secret'`

**Validation**:
- [ ] Each field has `context` property
- [ ] Each field has `access` property
- [ ] `context: 'client'` only with `access: 'public'`
- [ ] `context: 'server'` can be `'public'` or `'secret'`

❌ **INCORRECT**:
```javascript
env: {
  schema: {
    API_KEY: envField.string(),  // ❌ Missing context and access
    SECRET: envField.string({
      context: 'client',  // ❌ Client can't access secrets
      access: 'secret',
    }),
  },
}
```

✅ **CORRECT**:
```javascript
env: {
  schema: {
    PUBLIC_KEY: envField.string({
      context: 'client',
      access: 'public',
    }),
    SECRET_KEY: envField.string({
      context: 'server',
      access: 'secret',
    }),
  },
}
```

### Internationalization (i18n)

#### `i18n` (v3.5+)
**Type**: i18n configuration object
**Default**: `undefined`

```javascript
export default defineConfig({
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'es', 'fr'],
    fallback: {
      es: 'en',
      fr: 'en',
    },
    routing: {
      prefixDefaultLocale: false,
    },
  },
});
```

**Required Fields**:
- `defaultLocale`: REQUIRED if using i18n
- `locales`: REQUIRED if using i18n

**Validation**:
- [ ] `defaultLocale` is in `locales` array
- [ ] `locales` matches folder structure in `src/pages/`
- [ ] `fallback` keys are in `locales` array
- [ ] `fallback` values are in `locales` array

❌ **INCORRECT**:
```javascript
i18n: {
  defaultLocale: 'en',
  locales: ['es', 'fr'],  // ❌ Missing 'en' (default locale)
}
```

❌ **INCORRECT**:
```javascript
i18n: {
  defaultLocale: 'en',
  locales: ['en', 'es'],
  fallback: {
    es: 'fr',  // ❌ 'fr' not in locales
  },
}
```

### Build Options

#### `build.format`
**Type**: `'file' | 'directory'`
**Default**: `'directory'`

```javascript
export default defineConfig({
  build: {
    format: 'file',       // /about.html
    format: 'directory',  // /about/index.html
  },
});
```

#### `build.assets`
**Type**: `string`
**Default**: `'_astro'`
**Description**: Asset directory name in build output

```javascript
export default defineConfig({
  build: {
    assets: 'assets',
  },
});
```

#### `build.inlineStylesheets`
**Type**: `'always' | 'auto' | 'never'`
**Default**: `'auto'`

```javascript
export default defineConfig({
  build: {
    inlineStylesheets: 'never',
  },
});
```

### Server Options

#### `server.port`
**Type**: `number`
**Default**: `4321`

```javascript
export default defineConfig({
  server: {
    port: 3000,
  },
});
```

#### `server.host`
**Type**: `string | boolean`
**Default**: `false`

```javascript
export default defineConfig({
  server: {
    host: true,         // Listen on all addresses
    host: '0.0.0.0',    // Listen on specific address
  },
});
```

### Image Options

#### `image.service`
**Type**: Image service configuration
**Default**: Built-in service

```javascript
export default defineConfig({
  image: {
    service: {
      entrypoint: 'astro/assets/services/sharp',
    },
  },
});
```

## Validation Checklist

### Required Fields
- [ ] When `output: 'server'`, `adapter` is provided
- [ ] When using `i18n`, both `defaultLocale` and `locales` are set
- [ ] When using env vars, each field has `context` and `access`

### URL Validation
- [ ] `site` starts with `http://` or `https://`
- [ ] `base` starts with `/`
- [ ] `site` is provided if using sitemaps/RSS

### Type Validation
- [ ] `output` is `'static'` or `'server'`
- [ ] `trailingSlash` is `'always'`, `'never'`, or `'ignore'`
- [ ] `integrations` is an array of called functions

### i18n Validation
- [ ] `defaultLocale` is in `locales` array
- [ ] Folder structure matches locale configuration
- [ ] `fallback` locales exist in `locales`

### Environment Variables
- [ ] Client variables use `context: 'client'`, `access: 'public'`
- [ ] Secret variables use `context: 'server'`, `access: 'secret'`
- [ ] No missing required options

## Common Configuration Errors

| Error | Example | Fix |
|-------|---------|-----|
| Missing site protocol | `site: 'example.com'` | `site: 'https://example.com'` |
| base without slash | `base: 'docs'` | `base: '/docs/'` |
| Invalid output | `output: 'ssr'` | `output: 'server'` |
| Missing adapter | `output: 'server'` without adapter | Add `adapter: netlify()` |
| Uncalled integration | `integrations: [react]` | `integrations: [react()]` |
| Missing env options | `envField.string()` | `envField.string({context, access})` |
| Default locale missing | `locales: ['es']`, `defaultLocale: 'en'` | Add 'en' to locales |

## Example: Complete Configuration

```javascript
import { defineConfig, envField } from 'astro/config';
import react from '@astrojs/react';
import tailwind from '@astrojs/tailwind';
import starlight from '@astrojs/starlight';

export default defineConfig({
  // Site metadata
  site: 'https://example.com',
  base: '/',
  trailingSlash: 'always',

  // Build configuration
  output: 'static',

  // Integrations
  integrations: [
    react(),
    tailwind(),
    starlight({
      title: 'My Documentation',
      social: [
        { icon: 'github', href: 'https://github.com/user/repo' },
      ],
    }),
  ],

  // Environment variables
  env: {
    schema: {
      PUBLIC_API_URL: envField.string({
        context: 'client',
        access: 'public',
      }),
      SECRET_API_KEY: envField.string({
        context: 'server',
        access: 'secret',
      }),
    },
  },

  // i18n
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'es', 'fr'],
    fallback: {
      es: 'en',
      fr: 'en',
    },
  },

  // Server options
  server: {
    port: 4321,
    host: true,
  },

  // Build options
  build: {
    format: 'directory',
    inlineStylesheets: 'auto',
  },
});
```

## Audit Priority

### Critical (Will Break Builds)
- [ ] `output: 'server'` without `adapter`
- [ ] Invalid enum values (`output`, `trailingSlash`, etc.)
- [ ] Missing required i18n fields

### Important (Common Issues)
- [ ] `site` without protocol
- [ ] `base` without slashes
- [ ] Uncalled integration functions
- [ ] Missing env var options

### Best Practices
- [ ] Provide `site` for production
- [ ] Use TypeScript for config (.ts)
- [ ] Document non-standard options
