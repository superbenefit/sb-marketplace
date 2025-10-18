# Astro Content Loader API Reference

This document provides comprehensive reference for Astro's Content Loader API, including loader types, the LoaderContext, DataStore operations, and implementation patterns.

## Loader Types

### Inline Loaders (Simple)

**Purpose:** Quick, simple data fetching defined inline in `src/content.config.ts`

**Pattern:**
```typescript
import { defineCollection } from 'astro:content';

const collection = defineCollection({
  loader: async () => {
    const response = await fetch('https://api.example.com/data');
    const data = await response.json();

    // Must return array with id property OR object with IDs as keys
    return data.map((item) => ({
      id: item.id,
      ...item,
    }));
  },
  schema: z.object({ /* ... */ })
});
```

**Characteristics:**
- Async function returning array or object
- Clears and reloads entire store on each invocation
- Best for simple use cases
- No incremental update support

**Documentation:** https://docs.astro.build/en/reference/content-loader-reference/#inline-loaders

### Object Loaders (Advanced)

**Purpose:** Full control over loading process with incremental updates and state management

**Structure:**
```typescript
import type { Loader } from 'astro/loaders';

export function myLoader(options: LoaderOptions): Loader {
  return {
    name: "my-loader",  // Unique identifier for logging

    load: async (context: LoaderContext): Promise<void> => {
      // Load and update data using context
    },

    schema: async () => z.object({
      // Optional: define entry schema
    })
  };
}
```

**Usage:**
```typescript
import { defineCollection } from 'astro:content';
import { myLoader } from './loaders/myLoader';

const collection = defineCollection({
  loader: myLoader({ url: 'https://api.example.com', apiKey: 'secret' }),
  schema: z.object({ /* ... */ })
});
```

**Documentation:** https://docs.astro.build/en/reference/content-loader-reference/#object-loader-api

## Built-in Loaders

### `glob()` Loader

**Purpose:** Load content from local file directories

**Supported formats:** `.md`, `.mdx`, `.markdoc`, `.json`, `.yaml`, `.yml`, `.toml`

**Configuration:**
```typescript
import { glob } from 'astro/loaders';

const blog = defineCollection({
  loader: glob({
    pattern: "**/*.md",              // String or array of patterns
    base: "./src/data/blog",          // Base directory
    generateId: ({ entry }) => {      // Optional: custom ID generation
      return entry.replace(/\.md$/, '');
    }
  }),
  schema: z.object({ /* ... */ })
});
```

**Pattern syntax:**
- Supports glob wildcards and `**` globstar
- Uses `micromatch` syntax
- Can exclude: `['*.md', '!voyager-*']`
- Generates kebab-cased IDs by default

**Documentation:** https://docs.astro.build/en/reference/content-loader-reference/#glob-loader

### `file()` Loader

**Purpose:** Load multiple entries from a single file

**Supported formats:** JSON, YAML (with optional custom parser)

**Configuration:**
```typescript
import { file } from 'astro/loaders';

const authors = defineCollection({
  loader: file("src/data/authors.json"),
  schema: z.object({ /* ... */ })
});

// With custom parser
const products = defineCollection({
  loader: file("src/data/products.csv", {
    parser: (fileContent) => {
      // Return parsed data
      return parseCSV(fileContent);
    }
  }),
  schema: z.object({ /* ... */ })
});
```

**File format requirements:**
- Array of objects with unique `id` field, OR
- Object with IDs as keys and entries as values

**Documentation:** https://docs.astro.build/en/reference/content-loader-reference/#file-loader

## LoaderContext API

The `LoaderContext` object provides tools for managing collection data:

### Properties

**1. `collection` (string)**
- Unique collection name

**2. `store` (DataStore)**
- Interface for managing collection entries
- Methods: `set()`, `get()`, `entries()`, `keys()`, `values()`, `delete()`, `clear()`, `has()`

**3. `meta` (MetaStore)**
- Persistent key-value store for loader metadata
- Methods: `get(key)`, `set(key, value)`
- Persists between builds

**4. `logger` (AstroIntegrationLogger)**
- Structured logging interface
- Methods: `info()`, `warn()`, `error()`, `debug()`

**5. `config`**
- Full resolved Astro configuration object

**6. `parseData()`**
- Validates data against schema
- Returns validated, typed data

**7. `renderMarkdown()` (Astro 5.9.0+)**
- Converts markdown to HTML
- Returns `RenderedContent` object

**8. `generateDigest()`**
- Creates content hash for change detection
- Used with `store.set()` to prevent unnecessary updates

**Documentation:** https://docs.astro.build/en/reference/content-loader-reference/#loadercontext

## DataStore Methods

### `store.set(entry)`

Adds or updates an entry. Returns `true` if entry was updated (digest changed).

```typescript
const wasUpdated = store.set({
  id: item.id,
  data: parsedData,
  digest: generateDigest(parsedData),
  rendered: await renderMarkdown(item.markdown),
  filePath: item.path,  // Optional: for image resolution
  body: item.markdown   // Optional: raw content
});
```

**Entry properties:**
- `id` (required): Unique identifier
- `data` (required): Validated entry data
- `digest` (optional): Content hash for change detection
- `rendered` (optional): Pre-rendered HTML
- `filePath` (optional): Source file path
- `body` (optional): Raw content

### `store.get(id)`

Retrieves entry by ID. Returns entry object or `undefined`.

```typescript
const entry = store.get('post-1');
```

### `store.delete(id)`

Removes entry from collection.

```typescript
store.delete('old-post');
```

### `store.clear()`

Removes all entries. Use carefully - typically only in inline loaders.

```typescript
store.clear();  // Wipes entire collection
```

### `store.has(id)`

Checks if entry exists.

```typescript
if (store.has('post-1')) {
  // Entry exists
}
```

### `store.entries()`, `store.keys()`, `store.values()`

Iteration methods for accessing store data.

```typescript
for (const [id, entry] of store.entries()) {
  // Process each entry
}

const allIds = Array.from(store.keys());
const allEntries = Array.from(store.values());
```

**Documentation:** https://docs.astro.build/en/reference/content-loader-reference/#datastore

## MetaStore Methods

**Purpose:** Persist loader state between builds

**Methods:**
- `meta.get(key)`: Retrieve metadata
- `meta.set(key, value)`: Store metadata

**Use cases:**
- Track last sync time
- Store pagination cursors
- Save rate limit state
- Track API tokens/versions

**Example:**
```typescript
load: async ({ meta, logger }) => {
  const lastSync = meta.get('lastSync');

  if (lastSync) {
    logger.info(`Last sync: ${lastSync}`);
    // Fetch only updates since last sync
  } else {
    logger.info('First sync - fetching all data');
  }

  // ... fetch data ...

  meta.set('lastSync', new Date().toISOString());
}
```

## parseData() Function

Validates entry data against collection schema.

**Usage:**
```typescript
load: async ({ parseData, store }) => {
  const items = await fetchData();

  for (const item of items) {
    const data = await parseData({
      id: item.id,
      data: {
        title: item.title,
        description: item.description,
        pubDate: new Date(item.publishedAt),
      }
    });

    store.set({ id: item.id, data });
  }
}
```

**Throws error if:**
- Data doesn't match schema
- Required fields missing
- Type validation fails

## renderMarkdown() Function

Renders markdown to HTML (Astro 5.9.0+).

**Usage:**
```typescript
load: async ({ renderMarkdown, store }) => {
  const items = await fetchData();

  for (const item of items) {
    const rendered = await renderMarkdown(item.markdown);

    store.set({
      id: item.id,
      data: item,
      rendered,
      body: item.markdown
    });
  }
}
```

**Returns:** `RenderedContent` object with HTML

## generateDigest() Function

Creates content hash for change detection.

**Usage:**
```typescript
load: async ({ generateDigest, store, parseData }) => {
  const items = await fetchData();

  for (const item of items) {
    const data = await parseData({ id: item.id, data: item });
    const digest = generateDigest(data);

    // Only updates if digest differs from stored version
    store.set({ id: item.id, data, digest });
  }
}
```

**Benefits:**
- Prevents unnecessary rebuilds
- Enables incremental updates
- Optimizes build performance

## Implementation Patterns

### Error Handling

```typescript
export function robustLoader(options): Loader {
  return {
    name: 'robust-loader',

    load: async ({ store, logger, parseData }) => {
      try {
        logger.info('Fetching data');

        const response = await fetch(options.url);

        if (!response.ok) {
          logger.error(`API error: ${response.status}`);
          throw new Error(`Failed to fetch: ${response.status}`);
        }

        const data = await response.json();

        store.clear();
        for (const item of data) {
          const parsed = await parseData({ id: item.id, data: item });
          store.set({ id: item.id, data: parsed });
        }

        logger.info(`Loaded ${data.length} items`);

      } catch (error) {
        logger.error(`Loader failed: ${error.message}`);
        // Data persists from last successful load
      }
    }
  };
}
```

### Incremental Updates

```typescript
export function incrementalLoader(options): Loader {
  return {
    name: 'incremental-loader',

    load: async ({ store, meta, logger, generateDigest, parseData }) => {
      const lastSync = meta.get('lastSync');

      // Fetch only changes since last sync
      const changes = await fetchChanges(options.url, lastSync);

      logger.info(`Processing ${changes.length} changes`);

      for (const change of changes) {
        if (change.deleted) {
          store.delete(change.id);
        } else {
          const data = await parseData({ id: change.id, data: change });
          const digest = generateDigest(data);

          const wasUpdated = store.set({ id: change.id, data, digest });

          if (wasUpdated) {
            logger.info(`Updated: ${change.id}`);
          }
        }
      }

      meta.set('lastSync', new Date().toISOString());
    }
  };
}
```

### With Authentication

```typescript
import { EXTERNAL_API_KEY } from 'astro:env/server';

export function authenticatedLoader(options): Loader {
  return {
    name: 'authenticated-loader',

    load: async ({ store, logger, parseData }) => {
      const response = await fetch(options.url, {
        headers: {
          'Authorization': `Bearer ${EXTERNAL_API_KEY}`,
          'Content-Type': 'application/json'
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

## Key Takeaways

1. **Choose loader type** based on complexity (inline vs object)
2. **Use built-in loaders** (`glob`, `file`) when possible
3. **Leverage LoaderContext** for full control over data management
4. **Implement error handling** to preserve data on failures
5. **Use digest** for change detection and incremental updates
6. **Store metadata** in `meta` for stateful operations
7. **Validate with parseData()** before storing entries
8. **Log with logger** for better debugging

## Documentation References

- **Content Loader Reference:** https://docs.astro.build/en/reference/content-loader-reference/
- **Content Collections Guide:** https://docs.astro.build/en/guides/content-collections/#building-a-custom-loader
- **Data Fetching:** https://docs.astro.build/en/guides/data-fetching/
- **Environment Variables:** https://docs.astro.build/en/guides/environment-variables/
