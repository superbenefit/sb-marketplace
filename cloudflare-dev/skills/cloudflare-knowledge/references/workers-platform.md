---
description: Workers platform fundamentals including fetch handler, R2 object storage, KV key-value, D1 SQL database, bindings, and wrangler.jsonc configuration
globs: ["src/**/*.ts", "*.ts", "wrangler.jsonc"]
alwaysApply: false
---

# Workers Platform Reference

## Workers Fundamentals

### Module Worker Format

All Workers use the ES module format with a default export containing handler functions:

```typescript
interface Env {
  MY_KV: KVNamespace;
  MY_R2: R2Bucket;
  MY_DB: D1Database;
}

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);

    if (url.pathname === "/api/data") {
      const value = await env.MY_KV.get("key");
      return Response.json({ value });
    }

    return new Response("Not Found", { status: 404 });
  },

  async scheduled(event: ScheduledEvent, env: Env, ctx: ExecutionContext) {
    ctx.waitUntil(doBackgroundWork(env));
  },

  async queue(batch: MessageBatch, env: Env, ctx: ExecutionContext) {
    for (const message of batch.messages) {
      // Process queue messages
      message.ack();
    }
  }
} satisfies ExportedHandler<Env>;
```

### ExecutionContext

| Method | Purpose |
|--------|---------|
| `ctx.waitUntil(promise)` | Extend Worker lifetime for background work after response |
| `ctx.passThroughOnException()` | Fall through to origin on uncaught exception |

### Request Routing Pattern

```typescript
export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);
    const { pathname } = url;

    if (request.method === "GET" && pathname === "/health") {
      return new Response("OK");
    }

    if (request.method === "POST" && pathname === "/api/upload") {
      return handleUpload(request, env);
    }

    if (request.method === "GET" && pathname.startsWith("/api/items")) {
      return handleList(request, env);
    }

    return new Response("Not Found", { status: 404 });
  }
} satisfies ExportedHandler<Env>;
```

---

## R2 (Object Storage)

### Binding

```typescript
interface Env {
  MY_BUCKET: R2Bucket;
}
```

### Put (Write Objects)

```typescript
// Simple put
await env.MY_BUCKET.put("images/photo.png", imageData);

// Put with metadata and headers
await env.MY_BUCKET.put("docs/report.pdf", pdfData, {
  httpMetadata: {
    contentType: "application/pdf",
    cacheControl: "public, max-age=86400",
    contentDisposition: 'attachment; filename="report.pdf"',
  },
  customMetadata: {
    uploadedBy: "user-123",
    version: "2",
  },
  sha256: expectedHash,          // Optional integrity check
  storageClass: "Standard",      // "Standard" | "InfrequentAccess"
});
```

### Get (Read Objects)

```typescript
const object = await env.MY_BUCKET.get("images/photo.png");

if (object === null) {
  return new Response("Not Found", { status: 404 });
}

// Stream the body as response
const headers = new Headers();
object.writeHttpMetadata(headers);
headers.set("etag", object.httpEtag);

return new Response(object.body, { headers });
```

### Get with Conditional Headers (CRITICAL)

Always use conditional headers for cache-aware reads:

```typescript
const object = await env.MY_BUCKET.get("file.txt", {
  onlyIf: {
    etagMatches: request.headers.get("if-none-match"),
    uploadedAfter: request.headers.get("if-modified-since")
      ? new Date(request.headers.get("if-modified-since")!)
      : undefined,
  },
});

if (object === null) {
  return new Response("Not Found", { status: 404 });
}

// R2ObjectBody if condition met, R2Object (no body) if not
if (!("body" in object)) {
  return new Response(null, { status: 304 });
}
```

### Head (Object Metadata Only)

```typescript
const head = await env.MY_BUCKET.head("images/photo.png");
// Returns R2Object (no body) with size, etag, httpMetadata, customMetadata
if (head) {
  console.log(head.size, head.etag, head.uploaded);
}
```

### List Objects

```typescript
// Basic list
const listed = await env.MY_BUCKET.list();

// With prefix and pagination
const listed = await env.MY_BUCKET.list({
  prefix: "images/",
  limit: 100,
  cursor: previousCursor,         // For pagination
  delimiter: "/",                  // For directory-like listing
  include: ["httpMetadata", "customMetadata"],
});

// Iterate results
for (const object of listed.objects) {
  console.log(object.key, object.size, object.uploaded);
}

// Check for more pages
if (listed.truncated) {
  const nextPage = await env.MY_BUCKET.list({ cursor: listed.cursor });
}
```

### Delete

```typescript
// Single delete
await env.MY_BUCKET.delete("old-file.txt");

// Bulk delete (up to 1000 keys)
await env.MY_BUCKET.delete(["file1.txt", "file2.txt", "file3.txt"]);
```

### Multipart Uploads

```typescript
// Create multipart upload
const multipart = await env.MY_BUCKET.createMultipartUpload("large-file.zip", {
  httpMetadata: { contentType: "application/zip" },
});

// Upload parts (minimum 5MB per part except last)
const part1 = await multipart.uploadPart(1, chunk1);
const part2 = await multipart.uploadPart(2, chunk2);
const part3 = await multipart.uploadPart(3, chunk3);

// Complete upload
const object = await multipart.complete([part1, part2, part3]);

// Or abort if needed
// await multipart.abort();
```

### Presigned URLs

Presigned URLs are generated via the S3-compatible API, not the Workers binding directly. Use the `aws4fetch` library:

```typescript
import { AwsClient } from "aws4fetch";

const r2 = new AwsClient({
  accessKeyId: env.R2_ACCESS_KEY_ID,
  secretAccessKey: env.R2_SECRET_ACCESS_KEY,
});

const url = new URL(`https://${env.ACCOUNT_ID}.r2.cloudflarestorage.com/${bucket}/${key}`);
url.searchParams.set("X-Amz-Expires", "3600");

const signed = await r2.sign(new Request(url, { method: "GET" }), {
  aws: { signQuery: true },
});

return new Response(signed.url);
```

### R2 wrangler.jsonc Config

```jsonc
{
  "r2_buckets": [
    {
      "binding": "MY_BUCKET",
      "bucket_name": "my-production-bucket",
      "preview_bucket_name": "my-dev-bucket"   // Optional: for local dev
    }
  ]
}
```

---

## KV (Key-Value Store)

### Binding

```typescript
interface Env {
  MY_KV: KVNamespace;
}
```

### Get

```typescript
// Get as string (default)
const value = await env.MY_KV.get("user:123");

// Get as JSON
const data = await env.MY_KV.get<UserProfile>("user:123", "json");

// Get as ArrayBuffer
const binary = await env.MY_KV.get("file:data", "arrayBuffer");

// Get as ReadableStream
const stream = await env.MY_KV.get("file:large", "stream");

// Get with metadata
const { value, metadata } = await env.MY_KV.getWithMetadata<string, { role: string }>(
  "user:123",
  "text"
);
```

### Put

```typescript
// Simple put
await env.MY_KV.put("user:123", JSON.stringify(userData));

// Put with TTL (seconds from now)
await env.MY_KV.put("session:abc", token, {
  expirationTtl: 3600,         // Expires in 1 hour
});

// Put with absolute expiration (Unix timestamp in seconds)
await env.MY_KV.put("cache:page", html, {
  expiration: Math.floor(Date.now() / 1000) + 86400,
});

// Put with metadata
await env.MY_KV.put("user:123", JSON.stringify(userData), {
  metadata: { role: "admin", updatedAt: Date.now() },
  expirationTtl: 86400,
});
```

### Delete

```typescript
await env.MY_KV.delete("user:123");
```

### List

```typescript
// Basic list
const result = await env.MY_KV.list();

// With prefix and pagination
const result = await env.MY_KV.list({
  prefix: "user:",
  limit: 50,
  cursor: previousCursor,
});

// Iterate keys
for (const key of result.keys) {
  console.log(key.name, key.expiration, key.metadata);
}

// Paginate
if (!result.list_complete) {
  const nextPage = await env.MY_KV.list({ cursor: result.cursor });
}
```

### KV Consistency Model (CRITICAL)

KV is **eventually consistent**. After a write, reads may return stale data for up to 60 seconds. Design accordingly:

```typescript
// ✅ CORRECT: Return written value directly, don't re-read
await env.MY_KV.put("key", newValue);
return Response.json({ value: newValue }); // Return what you wrote

// ❌ WRONG: Reading immediately after write may return old value
await env.MY_KV.put("key", newValue);
const readBack = await env.MY_KV.get("key"); // May be stale!
```

### KV wrangler.jsonc Config

```jsonc
{
  "kv_namespaces": [
    {
      "binding": "MY_KV",
      "id": "abc123def456",
      "preview_id": "789ghi012jkl"    // Optional: for local dev
    }
  ]
}
```

---

## D1 (SQL Database)

### Binding

```typescript
interface Env {
  DB: D1Database;
}
```

### Prepared Statements (CRITICAL - Always Use These)

```typescript
// ✅ CORRECT: Parameterized queries prevent SQL injection
const user = await env.DB
  .prepare("SELECT * FROM users WHERE id = ?")
  .bind(userId)
  .first<User>();

// ❌ WRONG: String interpolation is vulnerable to SQL injection
const user = await env.DB
  .prepare(`SELECT * FROM users WHERE id = '${userId}'`)
  .first<User>();
```

### Query Methods

```typescript
// .first<T>() - Returns first row or null
const user = await env.DB
  .prepare("SELECT * FROM users WHERE email = ?")
  .bind(email)
  .first<User>();

// .all<T>() - Returns all matching rows
const { results, meta } = await env.DB
  .prepare("SELECT * FROM users WHERE role = ? LIMIT ? OFFSET ?")
  .bind("admin", 10, 0)
  .all<User>();
// meta.changes, meta.duration, meta.last_row_id, meta.rows_read, meta.rows_written

// .run() - Execute without returning rows (INSERT, UPDATE, DELETE)
const { meta } = await env.DB
  .prepare("INSERT INTO users (name, email) VALUES (?, ?)")
  .bind("Alice", "alice@example.com")
  .run();
// meta.last_row_id for auto-increment ID

// .raw<T>() - Returns array of arrays (no column names)
const rows = await env.DB
  .prepare("SELECT id, name FROM users")
  .raw<[number, string]>();
// [[1, "Alice"], [2, "Bob"]]

// .raw with column names
const rowsWithCols = await env.DB
  .prepare("SELECT id, name FROM users")
  .raw<[number, string]>({ columnNames: true });
// First row is column names: [["id", "name"], [1, "Alice"], [2, "Bob"]]
```

### Batch Queries (CRITICAL for Performance)

Batch queries run inside an implicit transaction. All succeed or all fail:

```typescript
const results = await env.DB.batch([
  env.DB.prepare("INSERT INTO users (name, email) VALUES (?, ?)").bind("Alice", "a@b.com"),
  env.DB.prepare("INSERT INTO users (name, email) VALUES (?, ?)").bind("Bob", "b@b.com"),
  env.DB.prepare("SELECT * FROM users"),
]);

// results[0] = first INSERT result
// results[1] = second INSERT result
// results[2] = SELECT result with .results array
```

### exec (Raw SQL - Use Sparingly)

```typescript
// For migrations or multi-statement SQL
const result = await env.DB.exec(`
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at TEXT DEFAULT (datetime('now'))
  );
  CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
`);
```

### D1 Time Travel

D1 automatically retains a history of changes (30 days on paid plans). Restore to any point:

```bash
# List available bookmarks
npx wrangler d1 time-travel info my-db

# Restore to a specific timestamp
npx wrangler d1 time-travel restore my-db --timestamp="2025-01-15T10:00:00Z"

# Restore to a specific bookmark
npx wrangler d1 time-travel restore my-db --bookmark=<bookmark_id>
```

### D1 Read Replication

D1 automatically creates read replicas close to users. Read replicas are used for queries by default. Force reading from primary for strong consistency:

```typescript
// Default: may read from replica (eventually consistent)
const user = await env.DB
  .prepare("SELECT * FROM users WHERE id = ?")
  .bind(userId)
  .first();

// Force read from primary (strongly consistent)
// Use a batch with a leading write to force primary
const [_, result] = await env.DB.batch([
  env.DB.prepare("SELECT 1"),  // Forces primary routing when in batch with writes
  env.DB.prepare("SELECT * FROM users WHERE id = ?").bind(userId),
]);
```

### D1 wrangler.jsonc Config

```jsonc
{
  "d1_databases": [
    {
      "binding": "DB",
      "database_name": "my-database",
      "database_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "migrations_dir": "migrations"     // Optional: for wrangler d1 migrations
    }
  ]
}
```

---

## All Binding Types

| Binding | Type in Env | Purpose | wrangler.jsonc Key |
|---------|-------------|---------|-------------------|
| **AI** | `Ai` | Run ML models (LLMs, embeddings, image gen) | `ai = { binding = "AI" }` |
| **Analytics Engine** | `AnalyticsEngineDataset` | Write analytics events | `analytics_engine_datasets` |
| **Assets** | `Fetcher` | Serve static assets | `assets = { binding = "ASSETS" }` |
| **Browser Rendering** | `BrowserWorker` | Headless Chromium | `browser = { binding = "BROWSER" }` |
| **D1** | `D1Database` | SQL database | `d1_databases` |
| **Durable Objects** | `DurableObjectNamespace` | Stateful coordination | `durable_objects.bindings` |
| **Hyperdrive** | `Hyperdrive` | Accelerated Postgres connections | `hyperdrive` |
| **KV** | `KVNamespace` | Key-value storage | `kv_namespaces` |
| **mTLS** | `Fetcher` | Mutual TLS client certificates | `mtls_certificates` |
| **Queues** (Producer) | `Queue` | Send messages to queue | `queues.producers` |
| **Queues** (Consumer) | handler | Receive messages from queue | `queues.consumers` |
| **R2** | `R2Bucket` | Object storage | `r2_buckets` |
| **Rate Limiting** | `RateLimit` | Request rate limiting | `unsafe.bindings` (type: ratelimit) |
| **Secrets** | `string` | Environment secrets | `wrangler secret put` |
| **Service Bindings** | `Fetcher` | Worker-to-Worker RPC | `services` |
| **Vectorize** | `VectorizeIndex` | Vector database | `vectorize` |
| **Workflows** | `Workflow` | Durable execution | `workflows` |

---

## Wrangler Configuration (wrangler.jsonc)

### Complete Configuration Example

```jsonc
{
  "$schema": "node_modules/wrangler/config-schema.json",
  "name": "my-worker",
  "main": "src/index.ts",
  "compatibility_date": "2025-01-01",
  "compatibility_flags": ["nodejs_compat"],

  // Observability
  "observability": {
    "enabled": true
  },

  // KV Namespaces
  "kv_namespaces": [
    {
      "binding": "MY_KV",
      "id": "abc123"
    }
  ],

  // R2 Buckets
  "r2_buckets": [
    {
      "binding": "MY_BUCKET",
      "bucket_name": "production-bucket"
    }
  ],

  // D1 Databases
  "d1_databases": [
    {
      "binding": "DB",
      "database_name": "my-db",
      "database_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    }
  ],

  // Service Bindings (Worker-to-Worker)
  "services": [
    {
      "binding": "AUTH_SERVICE",
      "service": "auth-worker"
    }
  ],

  // Durable Objects
  "durable_objects": {
    "bindings": [
      {
        "name": "MY_DO",
        "class_name": "MyDurableObject"
      }
    ]
  },
  "migrations": [
    {
      "tag": "v1",
      "new_classes": ["MyDurableObject"]
    }
  ],

  // Queues
  "queues": {
    "producers": [
      {
        "binding": "MY_QUEUE",
        "queue": "my-queue-name"
      }
    ],
    "consumers": [
      {
        "queue": "my-queue-name",
        "max_batch_size": 10,
        "max_batch_timeout": 5
      }
    ]
  },

  // AI
  "ai": {
    "binding": "AI"
  },

  // Vectorize
  "vectorize": [
    {
      "binding": "VECTORIZE",
      "index_name": "my-index"
    }
  ],

  // Workflows
  "workflows": [
    {
      "name": "my-workflow",
      "binding": "MY_WORKFLOW",
      "class_name": "MyWorkflow"
    }
  ],

  // Browser Rendering
  "browser": {
    "binding": "BROWSER"
  },

  // Hyperdrive
  "hyperdrive": [
    {
      "binding": "HYPERDRIVE",
      "id": "xxxxxxxx"
    }
  ],

  // Analytics Engine
  "analytics_engine_datasets": [
    {
      "binding": "ANALYTICS",
      "dataset": "my-dataset"
    }
  ],

  // Triggers
  "triggers": {
    "crons": ["0 */6 * * *"]
  },

  // Environment variables
  "vars": {
    "ENVIRONMENT": "production",
    "API_URL": "https://api.example.com"
  }
}
```

---

## Critical Rules

### 1. Always Use Bindings from Workers (NOT REST APIs)

```typescript
// ✅ CORRECT: Use binding
const value = await env.MY_KV.get("key");
const object = await env.MY_BUCKET.get("file.txt");
const user = await env.DB.prepare("SELECT * FROM users WHERE id = ?").bind(1).first();

// ❌ WRONG: Don't use REST API from within a Worker
const resp = await fetch("https://api.cloudflare.com/client/v4/accounts/.../storage/kv/...");
```

### 2. Always Use Prepared Statements for D1

```typescript
// ✅ CORRECT: Parameterized
env.DB.prepare("SELECT * FROM users WHERE id = ?").bind(userId)

// ❌ WRONG: String interpolation (SQL injection risk)
env.DB.prepare(`SELECT * FROM users WHERE id = '${userId}'`)
```

### 3. Handle R2 Conditional Headers

```typescript
// ✅ CORRECT: Check for conditional response
const obj = await env.MY_BUCKET.get(key, {
  onlyIf: { etagMatches: request.headers.get("if-none-match") }
});
if (obj && !("body" in obj)) {
  return new Response(null, { status: 304 });
}
```

### 4. Type Your Env Interface

```typescript
// ✅ CORRECT: Fully typed Env
interface Env {
  MY_KV: KVNamespace;
  MY_BUCKET: R2Bucket;
  DB: D1Database;
  AI: Ai;
  MY_SECRET: string;
  ENVIRONMENT: string;
}

// ❌ WRONG: Untyped or using 'any'
export default { async fetch(req: Request, env: any) { } }
```

### 5. Use ctx.waitUntil for Background Work

```typescript
// ✅ CORRECT: Response returns immediately, logging continues
export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext) {
    ctx.waitUntil(env.MY_KV.put("last-request", new Date().toISOString()));
    return new Response("OK");
  }
};

// ❌ WRONG: Awaiting non-critical work delays response
export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext) {
    await env.MY_KV.put("last-request", new Date().toISOString());
    return new Response("OK");
  }
};
```

### 6. KV is Eventually Consistent

Do not read-after-write and expect the new value. Return the value you wrote directly instead of re-reading from KV.

### 7. D1 Batch for Transactions

Use `env.DB.batch([...])` when you need multiple queries to succeed or fail atomically. Individual queries outside a batch are NOT transactional with each other.

## Sources

- https://developers.cloudflare.com/workers/runtime-apis/handlers/fetch/
- https://developers.cloudflare.com/workers/runtime-apis/bindings/
- https://developers.cloudflare.com/workers/wrangler/configuration/
- https://developers.cloudflare.com/r2/api/workers/workers-api-reference/
- https://developers.cloudflare.com/r2/api/workers/workers-multipart-usage/
- https://developers.cloudflare.com/r2/api/s3/presigned-urls/
- https://developers.cloudflare.com/kv/api/
- https://developers.cloudflare.com/d1/worker-api/d1-client-api/
- https://developers.cloudflare.com/d1/platform/time-travel/
- https://developers.cloudflare.com/d1/platform/read-replication/
