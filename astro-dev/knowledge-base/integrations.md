# External Integrations & Custom Loaders

**Patterns for integrating external data sources, custom loaders, and TypeScript configuration.**

## Content Loader Fundamentals

### Inline Loader (Simple)

```typescript
// src/content.config.ts
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

**Use for**: Quick, simple data fetching without state management.

---

### Object Loader (Advanced)

```typescript
import type { Loader } from 'astro/loaders';

export function apiLoader(options: { url: string }): Loader {
  return {
    name: 'api-loader',

    async load({ store, logger, parseData, generateDigest }) {
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

          const digest = generateDigest(parsed);

          store.set({
            id: item.id.toString(),
            data: parsed,
            digest,
          });
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

**Use for**: Production integrations with error handling, incremental updates, and state management.

---

## Authentication & Environment Variables

### Type-Safe Environment Variables

```typescript
// astro.config.mjs
import { defineConfig, envField } from 'astro/config';

export default defineConfig({
  env: {
    schema: {
      EXTERNAL_API_KEY: envField.string({
        context: 'server',
        access: 'secret',
      }),
      EXTERNAL_API_URL: envField.string({
        context: 'server',
        access: 'public',
      }),
      PUBLIC_FEATURE_FLAG: envField.string({
        context: 'client',
        access: 'public',
      }),
    }
  }
});
```

**Set in `.env`**:
```
EXTERNAL_API_KEY=secret_token_here
EXTERNAL_API_URL=https://api.example.com
PUBLIC_FEATURE_FLAG=enabled
```

---

### Using in Loader

```typescript
import { EXTERNAL_API_KEY, EXTERNAL_API_URL } from 'astro:env/server';
import type { Loader } from 'astro/loaders';

export function authenticatedLoader(): Loader {
  return {
    name: 'authenticated-loader',

    async load({ store, logger, parseData }) {
      const response = await fetch(EXTERNAL_API_URL, {
        headers: {
          'Authorization': `Bearer ${EXTERNAL_API_KEY}`,
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

---

## Error Handling & Resilience

### Retry with Exponential Backoff

```typescript
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
    }
  };
}
```

---

### Rate Limiting

```typescript
export function rateLimitedLoader(options: { url: string, requestDelay: number }): Loader {
  return {
    name: 'rate-limited-loader',

    async load({ store, meta, logger, parseData }) {
      const lastRequestTime = parseInt(meta.get('lastRequestTime') || '0');
      const now = Date.now();
      const timeSinceLastRequest = now - lastRequestTime;

      // Enforce minimum delay
      if (timeSinceLastRequest < options.requestDelay) {
        const waitTime = options.requestDelay - timeSinceLastRequest;
        logger.info(`Rate limit: waiting ${waitTime}ms`);
        await new Promise(resolve => setTimeout(resolve, waitTime));
      }

      try {
        const response = await fetch(options.url);

        if (response.status === 429) {
          const retryAfter = response.headers.get('Retry-After');
          logger.warn(`Rate limited. Retry after: ${retryAfter}s`);
          return; // Skip this update
        }

        if (!response.ok) {
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

---

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

---

## Data Transformation

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

---

## Built-in Loaders

### glob() Loader

```typescript
import { glob } from 'astro/loaders';

const blog = defineCollection({
  loader: glob({
    pattern: "**/*.md",
    base: "./src/data/blog",
    generateId: ({ entry }) => {
      return entry.replace(/\.md$/, '');
    }
  }),
  schema: z.object({
    title: z.string(),
    pubDate: z.coerce.date(),
  })
});
```

**Pattern syntax**:
- `*` - Matches any characters except `/`
- `**` - Matches any characters including `/`
- `{a,b}` - Matches `a` or `b`
- Exclude: `['*.md', '!draft-*']`

---

### file() Loader

```typescript
import { file } from 'astro/loaders';

const authors = defineCollection({
  loader: file("src/data/authors.json"),
  schema: z.object({
    name: z.string(),
    bio: z.string(),
  })
});

// With custom parser
const products = defineCollection({
  loader: file("src/data/products.csv", {
    parser: (fileContent) => {
      return parseCSV(fileContent);
    }
  }),
  schema: z.object({ /* ... */ })
});
```

**File requirements**:
- Array of objects with `id` field, OR
- Object with IDs as keys

---

## Image Handling

### Remote Images

```typescript
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
            imageUrl: item.featured_image.url,
            imageAlt: item.featured_image.alt || item.title,
          }
        });

        store.set({ id: item.id, data });
      }
    },

    schema: () => z.object({
      title: z.string(),
      imageUrl: z.string().url(),
      imageAlt: z.string(),
    })
  };
}
```

**Using in templates**:
```astro
---
import { Image } from 'astro:assets';
import { getEntry } from 'astro:content';

const entry = await getEntry('content', 'my-post');
---

<Image
  src={entry.data.imageUrl}
  alt={entry.data.imageAlt}
  width={800}
  height={600}
  loading="lazy"
/>
```

---

## TypeScript Best Practices

### Avoid `any`

```typescript
// ❌ Wrong
function processData(data: any) {
  return data.value;
}

// ✅ Correct
interface Data {
  value: string;
}

function processData(data: Data): string {
  return data.value;
}
```

---

### Use `unknown` for Uncertain Types

```typescript
// ✅ Correct
function processUserInput(input: unknown) {
  if (typeof input === 'string') {
    return input.toUpperCase();
  }
  throw new Error('Expected string input');
}
```

---

### Type-Only Imports

```typescript
// ✅ Correct
import type { CollectionEntry } from 'astro:content';
import type { Loader } from 'astro/loaders';

interface Props {
  post: CollectionEntry<'blog'>;
}
```

**Benefits**:
- Removed at build time
- Better tree-shaking
- Clear intent

---

### Generic Type Constraints

```typescript
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

interface User {
  id: string;
  name: string;
}

const user: User = { id: '1', name: 'Alice' };
const name = getProperty(user, 'name');  // ✅ OK
const invalid = getProperty(user, 'age');  // ❌ Error
```

---

### Utility Types

```typescript
interface User {
  id: string;
  name: string;
  email: string;
  age: number;
}

// Partial - all properties optional
type UserUpdate = Partial<User>;

// Pick - select specific properties
type UserPreview = Pick<User, 'id' | 'name'>;

// Omit - exclude specific properties
type UserWithoutAge = Omit<User, 'age'>;

// Required - all properties required
type RequiredUser = Required<Partial<User>>;

// Readonly - all properties readonly
type ImmutableUser = Readonly<User>;

// Record - object with specific key/value types
type UserMap = Record<string, User>;
```

---

### Type Guards

```typescript
// Custom type guard
function isUser(obj: unknown): obj is User {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    'id' in obj &&
    'name' in obj
  );
}

function greetUser(data: unknown) {
  if (isUser(data)) {
    console.log(`Hello, ${data.name}`);
  }
}
```

---

### Discriminated Unions

```typescript
interface SuccessResult {
  success: true;
  data: User;
}

interface ErrorResult {
  success: false;
  error: string;
}

type Result = SuccessResult | ErrorResult;

function handleResult(result: Result) {
  if (result.success) {
    console.log(result.data.name);
  } else {
    console.log(result.error);
  }
}
```

---

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
          logger.info(`Cache valid for ${(options.cacheDuration - timeSinceSync) / 1000}s`);
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

---

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
        return;
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

---

## Key Patterns Summary

**Loader Types**:
- Inline loaders for simple use cases
- Object loaders for production integrations
- Built-in `glob()` and `file()` loaders

**Best Practices**:
1. Use type-safe environment variables
2. Implement error handling with retries
3. Rate limit API requests
4. Use digest for change detection
5. Cache strategically with metadata
6. Transform data to match schema

**TypeScript**:
- Avoid `any`, use `unknown` instead
- Use `import type` for types
- Type guards for narrowing
- Utility types for transformations
- Generic constraints where needed

**Error Handling**:
- Retry with exponential backoff
- Handle rate limits gracefully
- Log errors for debugging
- Preserve data on failures

**Performance**:
- Incremental updates when possible
- HTTP caching headers
- Digest-based change detection
- Metadata for state persistence
