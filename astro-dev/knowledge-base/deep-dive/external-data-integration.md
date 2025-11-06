# External Data Integration with Astro Reference

This document provides comprehensive patterns for integrating external data sources (APIs, CMSs, GitBook, etc.) into Astro using custom content loaders.

## Custom Loader Patterns for REST APIs

### Basic API Loader

**Inline pattern (simple):**
```typescript
import { defineCollection, z } from 'astro:content';

const externalData = defineCollection({
  loader: async () => {
    const response = await fetch('https://api.example.com/posts');
    const posts = await response.json();

    return posts.map(post => ({
      id: post.id.toString(),
      title: post.title,
      content: post.body,
      publishedAt: new Date(post.created_at),
    }));
  },
  schema: z.object({
    title: z.string(),
    content: z.string(),
    publishedAt: z.date(),
  })
});

export const collections = { externalData };
```

**Object pattern (advanced):**
```typescript
import type { Loader } from 'astro/loaders';

export function apiLoader(options: { url: string }): Loader {
  return {
    name: 'api-loader',

    async load({ store, logger, parseData }) {
      try {
        logger.info('Fetching from API');

        const response = await fetch(options.url);

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();

        store.clear();

        for (const item of data) {
          const parsed = await parseData({
            id: item.id.toString(),
            data: {
              title: item.title,
              content: item.content,
              publishedAt: new Date(item.published_at),
            }
          });

          store.set({ id: item.id.toString(), data: parsed });
        }

        logger.info(`Loaded ${data.length} items`);

      } catch (error) {
        logger.error(`API loader failed: ${error.message}`);
      }
    },

    schema: () => z.object({
      title: z.string(),
      content: z.string(),
      publishedAt: z.date(),
    })
  };
}
```

**Documentation:** https://docs.astro.build/en/reference/content-loader-reference/

## Authentication and API Key Handling

### Type-Safe Environment Variables

**Define in `astro.config.mjs`:**
```typescript
import { defineConfig, envField } from 'astro/config';

export default defineConfig({
  env: {
    schema: {
      GITBOOK_API_TOKEN: envField.string({
        context: 'server',
        access: 'secret',
      }),
      EXTERNAL_API_URL: envField.string({
        context: 'server',
        access: 'public',
      }),
      API_RATE_LIMIT: envField.number({
        context: 'server',
        access: 'public',
        default: 100,
      }),
    }
  }
});
```

**Set in `.env`:**
```
GITBOOK_API_TOKEN=gb_secret_token_here
EXTERNAL_API_URL=https://api.example.com
API_RATE_LIMIT=100
```

**Use in loader:**
```typescript
import { GITBOOK_API_TOKEN, EXTERNAL_API_URL } from 'astro:env/server';
import type { Loader } from 'astro/loaders';

export function authenticatedLoader(): Loader {
  return {
    name: 'authenticated-loader',

    async load({ store, logger, parseData }) {
      const response = await fetch(EXTERNAL_API_URL, {
        headers: {
          'Authorization': `Bearer ${GITBOOK_API_TOKEN}`,
          'Content-Type': 'application/json',
        }
      });

      const data = await response.json();

      store.clear();
      for (const item of data) {
        const parsed = await parseData({ id: item.id, data: item });
        store.set({ id: item.id, data: parsed });
      }
    }
  };
}
```

**Documentation:** https://docs.astro.build/en/guides/environment-variables/

## Rate Limiting and Error Handling

### Rate Limiting Pattern

```typescript
import type { Loader } from 'astro/loaders';

export function rateLimitedLoader(options: { url: string, requestDelay: number }): Loader {
  return {
    name: 'rate-limited-loader',

    async load({ store, meta, logger, parseData }) {
      const lastRequestTime = parseInt(meta.get('lastRequestTime') || '0');
      const now = Date.now();
      const timeSinceLastRequest = now - lastRequestTime;

      // Enforce minimum delay between requests
      if (timeSinceLastRequest < options.requestDelay) {
        const waitTime = options.requestDelay - timeSinceLastRequest;
        logger.info(`Rate limit: waiting ${waitTime}ms`);
        await new Promise(resolve => setTimeout(resolve, waitTime));
      }

      try {
        logger.info('Fetching data');

        const response = await fetch(options.url);

        if (!response.ok) {
          if (response.status === 429) {
            const retryAfter = response.headers.get('Retry-After');
            logger.warn(`Rate limited. Retry after: ${retryAfter}s`);
            return; // Skip this update
          }
          throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();

        store.clear();
        for (const item of data) {
          const parsed = await parseData({ id: item.id, data: item });
          store.set({ id: item.id, data: parsed });
        }

        meta.set('lastRequestTime', Date.now().toString());

      } catch (error) {
        logger.error(`Loader failed: ${error.message}`);
      }
    }
  };
}
```

### Comprehensive Error Handling

```typescript
import type { Loader } from 'astro/loaders';

export function robustLoader(options: { url: string, retries: number }): Loader {
  return {
    name: 'robust-loader',

    async load({ store, logger, parseData }) {
      let lastError: Error | null = null;

      for (let attempt = 1; attempt <= options.retries; attempt++) {
        try {
          logger.info(`Attempt ${attempt} of ${options.retries}`);

          const response = await fetch(options.url, {
            signal: AbortSignal.timeout(10000), // 10s timeout
          });

          if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
          }

          const data = await response.json();

          store.clear();
          for (const item of data) {
            const parsed = await parseData({ id: item.id, data: item });
            store.set({ id: item.id, data: parsed });
          }

          logger.info(`Successfully loaded ${data.length} items`);
          return; // Success!

        } catch (error) {
          lastError = error as Error;
          logger.warn(`Attempt ${attempt} failed: ${error.message}`);

          if (attempt < options.retries) {
            const backoff = Math.min(1000 * Math.pow(2, attempt - 1), 10000);
            logger.info(`Retrying in ${backoff}ms...`);
            await new Promise(resolve => setTimeout(resolve, backoff));
          }
        }
      }

      logger.error(`All ${options.retries} attempts failed: ${lastError?.message}`);
      // Data persists from last successful load
    }
  };
}
```

## GitBook Integration Patterns

### GitBook API Structure

**Typical GitBook API endpoints:**
- Spaces: `/v1/spaces/{spaceId}`
- Pages: `/v1/spaces/{spaceId}/content`
- Collections: `/v1/spaces/{spaceId}/collections`

**Response format (example):**
```json
{
  "pages": [
    {
      "id": "page-id",
      "title": "Page Title",
      "description": "Page description",
      "path": "/docs/getting-started",
      "document": {
        "markdown": "# Content here"
      },
      "updatedAt": "2024-01-15T10:00:00Z"
    }
  ]
}
```

### GitBook Loader Implementation

```typescript
import type { Loader } from 'astro/loaders';
import { z } from 'astro:content';
import { GITBOOK_API_TOKEN, GITBOOK_SPACE_ID } from 'astro:env/server';

export function gitbookLoader(): Loader {
  return {
    name: 'gitbook-loader',

    async load({ store, logger, parseData, generateDigest, renderMarkdown, meta }) {
      try {
        logger.info('Fetching GitBook content');

        // Fetch from GitBook API
        const response = await fetch(
          `https://api.gitbook.com/v1/spaces/${GITBOOK_SPACE_ID}/content`,
          {
            headers: {
              'Authorization': `Bearer ${GITBOOK_API_TOKEN}`,
              'Accept': 'application/json',
            }
          }
        );

        if (!response.ok) {
          throw new Error(`GitBook API error: ${response.status}`);
        }

        const { pages } = await response.json();

        // Track updated count
        let updatedCount = 0;

        for (const page of pages) {
          // Transform GitBook data to Astro format
          const data = await parseData({
            id: page.id,
            data: {
              title: page.title,
              description: page.description || '',
              path: page.path,
              content: page.document?.markdown || '',
              updatedAt: new Date(page.updatedAt),
              gitbookUrl: `https://docs.example.com${page.path}`,
            }
          });

          // Render markdown to HTML
          const rendered = await renderMarkdown(page.document?.markdown || '');

          // Generate digest for change detection
          const digest = generateDigest(data);

          // Only updates if digest changed
          const wasUpdated = store.set({
            id: page.id,
            data,
            rendered,
            digest,
            body: page.document?.markdown,
          });

          if (wasUpdated) {
            updatedCount++;
          }
        }

        logger.info(`Loaded ${pages.length} pages (${updatedCount} updated)`);
        meta.set('lastSync', new Date().toISOString());

      } catch (error) {
        logger.error(`GitBook loader failed: ${error.message}`);
      }
    },

    schema: () => z.object({
      title: z.string(),
      description: z.string(),
      path: z.string(),
      content: z.string(),
      updatedAt: z.date(),
      gitbookUrl: z.string().url(),
    })
  };
}
```

### Using in Collection

```typescript
import { defineCollection } from 'astro:content';
import { gitbookLoader } from './loaders/gitbook';

const docs = defineCollection({
  loader: gitbookLoader(),
});

export const collections = { docs };
```

## Data Transformation

### Converting External Formats

```typescript
function transformGitBookToAstro(gitbookPage: GitBookPage) {
  return {
    id: gitbookPage.id,
    data: {
      // Map fields
      title: gitbookPage.title,
      description: gitbookPage.description || generateDescription(gitbookPage.document.markdown),

      // Transform dates
      publishedAt: new Date(gitbookPage.createdAt),
      updatedAt: new Date(gitbookPage.updatedAt),

      // Extract metadata
      author: gitbookPage.author?.name || 'Unknown',
      tags: extractTags(gitbookPage.document.markdown),

      // Process content
      content: processMarkdown(gitbookPage.document.markdown),
      excerpt: generateExcerpt(gitbookPage.document.markdown, 150),
    }
  };
}

function generateDescription(markdown: string): string {
  // Extract first paragraph
  const firstParagraph = markdown.split('\n\n')[0];
  return firstParagraph.replace(/[#*`]/g, '').substring(0, 160);
}

function extractTags(markdown: string): string[] {
  // Extract from frontmatter or content
  const tagMatch = markdown.match(/tags:\s*\[(.*?)\]/);
  return tagMatch ? tagMatch[1].split(',').map(t => t.trim()) : [];
}

function generateExcerpt(markdown: string, length: number): string {
  const text = markdown.replace(/[#*`\[\]]/g, '').trim();
  return text.length > length ? text.substring(0, length) + '...' : text;
}
```

### Type-Safe Transformation

```typescript
import type { Loader } from 'astro/loaders';
import { z } from 'astro:content';

// External API type
interface ExternalPost {
  id: number;
  title: string;
  body: string;
  created_at: string;
  author: {
    id: number;
    name: string;
  };
  tags: string[];
}

// Astro schema
const postSchema = z.object({
  title: z.string(),
  content: z.string(),
  publishedAt: z.date(),
  author: z.string(),
  tags: z.array(z.string()),
});

export function typedLoader(): Loader {
  return {
    name: 'typed-loader',

    async load({ store, parseData }) {
      const response = await fetch('https://api.example.com/posts');
      const externalPosts: ExternalPost[] = await response.json();

      store.clear();

      for (const post of externalPosts) {
        // Transform to Astro format
        const data = await parseData({
          id: post.id.toString(),
          data: {
            title: post.title,
            content: post.body,
            publishedAt: new Date(post.created_at),
            author: post.author.name,
            tags: post.tags,
          }
        });

        store.set({ id: post.id.toString(), data });
      }
    },

    schema: () => postSchema
  };
}
```

## Handling Images and Assets

### Remote Images

```typescript
import type { Loader } from 'astro/loaders';
import { z } from 'astro:content';

export function imageLoader(): Loader {
  return {
    name: 'image-loader',

    async load({ store, parseData }) {
      const response = await fetch('https://api.example.com/content');
      const items = await response.json();

      store.clear();

      for (const item of items) {
        const data = await parseData({
          id: item.id,
          data: {
            title: item.title,
            // Store remote image URL directly
            imageUrl: item.featured_image.url,
            imageAlt: item.featured_image.alt || item.title,
            // Or multiple images
            gallery: item.images.map(img => ({
              url: img.url,
              alt: img.alt,
              caption: img.caption,
            })),
          }
        });

        store.set({ id: item.id, data });
      }
    },

    schema: () => z.object({
      title: z.string(),
      imageUrl: z.string().url(),
      imageAlt: z.string(),
      gallery: z.array(z.object({
        url: z.string().url(),
        alt: z.string(),
        caption: z.string().optional(),
      })),
    })
  };
}
```

**Using in templates:**
```astro
---
import { Image } from 'astro:assets';
import { getEntry } from 'astro:content';

const entry = await getEntry('content', 'my-post');
---

<!-- Remote image with optimization -->
<Image
  src={entry.data.imageUrl}
  alt={entry.data.imageAlt}
  width={800}
  height={600}
  loading="lazy"
/>

<!-- Gallery -->
{entry.data.gallery.map(img => (
  <figure>
    <Image src={img.url} alt={img.alt} width={400} height={300} />
    {img.caption && <figcaption>{img.caption}</figcaption>}
  </figure>
))}
```

**Documentation:** https://docs.astro.build/en/guides/images/#remote-images

### Downloading Assets

```typescript
import type { Loader } from 'astro/loaders';
import { writeFile, mkdir } from 'node:fs/promises';
import { join } from 'node:path';

export function assetDownloadLoader(): Loader {
  return {
    name: 'asset-download-loader',

    async load({ store, parseData, logger, config }) {
      const response = await fetch('https://api.example.com/content');
      const items = await response.json();

      // Create assets directory
      const assetsDir = join(config.root.pathname, 'public', 'downloaded-assets');
      await mkdir(assetsDir, { recursive: true });

      store.clear();

      for (const item of items) {
        // Download image
        let localImagePath = null;

        if (item.image_url) {
          const imageResponse = await fetch(item.image_url);
          const imageBuffer = Buffer.from(await imageResponse.arrayBuffer());
          const filename = `${item.id}.jpg`;
          const filepath = join(assetsDir, filename);

          await writeFile(filepath, imageBuffer);
          localImagePath = `/downloaded-assets/${filename}`;

          logger.info(`Downloaded image: ${filename}`);
        }

        const data = await parseData({
          id: item.id,
          data: {
            title: item.title,
            image: localImagePath,
            originalImageUrl: item.image_url,
          }
        });

        store.set({ id: item.id, data });
      }
    }
  };
}
```

## Caching Strategies

### Metadata-Based Caching

```typescript
export function cachedLoader(options: { url: string, cacheDuration: number }): Loader {
  return {
    name: 'cached-loader',

    async load({ store, meta, logger }) {
      const lastSync = meta.get('lastSync');
      const now = Date.now();

      if (lastSync) {
        const timeSinceSync = now - parseInt(lastSync);

        if (timeSinceSync < options.cacheDuration) {
          logger.info(`Cache valid for ${(options.cacheDuration - timeSinceSync) / 1000}s more`);
          return; // Skip fetch
        }
      }

      logger.info('Cache expired, fetching fresh data');

      const response = await fetch(options.url);
      const data = await response.json();

      store.clear();
      for (const item of data) {
        store.set({ id: item.id, data: item });
      }

      meta.set('lastSync', now.toString());
    }
  };
}
```

### HTTP Caching Headers

```typescript
export function httpCachedLoader(options: { url: string }): Loader {
  return {
    name: 'http-cached-loader',

    async load({ store, meta, logger }) {
      const lastModified = meta.get('lastModified');
      const etag = meta.get('etag');

      const headers: HeadersInit = {};

      if (lastModified) {
        headers['If-Modified-Since'] = lastModified;
      }

      if (etag) {
        headers['If-None-Match'] = etag;
      }

      const response = await fetch(options.url, { headers });

      if (response.status === 304) {
        logger.info('Content not modified (HTTP 304)');
        return; // Use cached data
      }

      const data = await response.json();

      store.clear();
      for (const item of data) {
        store.set({ id: item.id, data: item });
      }

      // Store cache headers
      const newLastModified = response.headers.get('Last-Modified');
      const newEtag = response.headers.get('ETag');

      if (newLastModified) meta.set('lastModified', newLastModified);
      if (newEtag) meta.set('etag', newEtag);
    }
  };
}
```

## Incremental Updates

### Change Detection with Digest

```typescript
export function incrementalLoader(options: { url: string }): Loader {
  return {
    name: 'incremental-loader',

    async load({ store, meta, logger, generateDigest, parseData }) {
      const lastSync = meta.get('lastSync');

      // Fetch only changes since last sync
      const url = lastSync
        ? `${options.url}?since=${lastSync}`
        : options.url;

      const response = await fetch(url);
      const { items, deleted = [] } = await response.json();

      logger.info(`Processing ${items.length} updates, ${deleted.length} deletions`);

      // Update/add items
      for (const item of items) {
        const data = await parseData({ id: item.id, data: item });
        const digest = generateDigest(data);

        const wasUpdated = store.set({
          id: item.id,
          data,
          digest,
        });

        if (wasUpdated) {
          logger.info(`Updated: ${item.id}`);
        }
      }

      // Remove deleted items
      for (const id of deleted) {
        if (store.has(id)) {
          store.delete(id);
          logger.info(`Deleted: ${id}`);
        }
      }

      meta.set('lastSync', new Date().toISOString());
    }
  };
}
```

## Build-Time vs Runtime Fetching

### Build-Time (Static Generation - Default)

```typescript
// Loader runs during build
export function buildTimeLoader(): Loader {
  return {
    name: 'build-time-loader',

    async load({ store, logger }) {
      logger.info('Fetching at build time');

      const response = await fetch('https://api.example.com/data');
      const data = await response.json();

      // Data baked into static HTML
      store.clear();
      for (const item of data) {
        store.set({ id: item.id, data: item });
      }
    }
  };
}
```

### Runtime (On-Demand Rendering - SSR)

**Enable adapter:**
```javascript
// astro.config.mjs
import { defineConfig } from 'astro/config';
import node from '@astrojs/node';

export default defineConfig({
  output: 'server', // or 'hybrid'
  adapter: node({ mode: 'standalone' }),
});
```

**Runtime fetching in pages:**
```astro
---
export const prerender = false; // Render on demand

// Fetches fresh data on each request
const response = await fetch('https://api.example.com/live-data');
const data = await response.json();
---

<div>Data fetched at: {new Date().toISOString()}</div>
<pre>{JSON.stringify(data, null, 2)}</pre>
```

**Hybrid approach:**
```astro
---
import { getEntry } from 'astro:content';

export const prerender = false;

// Build-time data from loader
const staticEntry = await getEntry('docs', 'static-content');

// Runtime data from API
const liveData = await fetch('https://api.example.com/live').then(r => r.json());
---

<article>
  <h1>{staticEntry.data.title}</h1>
  <div>Live count: {liveData.count}</div>
</article>
```

**Documentation:** https://docs.astro.build/en/guides/on-demand-rendering/

## Key Takeaways

1. **Use object loaders** for production external data integration
2. **Implement auth** with type-safe environment variables
3. **Handle errors** with retries and exponential backoff
4. **Rate limit** requests to respect API limits
5. **Transform data** to match Astro schema requirements
6. **Cache strategically** using metadata and HTTP headers
7. **Use digest** for incremental updates and change detection
8. **Choose fetch timing** based on data freshness needs (build vs runtime)

## Documentation References

- **Content Loader Reference:** https://docs.astro.build/en/reference/content-loader-reference/
- **Environment Variables:** https://docs.astro.build/en/guides/environment-variables/
- **Data Fetching:** https://docs.astro.build/en/guides/data-fetching/
- **Images Guide:** https://docs.astro.build/en/guides/images/
- **On-Demand Rendering:** https://docs.astro.build/en/guides/on-demand-rendering/
