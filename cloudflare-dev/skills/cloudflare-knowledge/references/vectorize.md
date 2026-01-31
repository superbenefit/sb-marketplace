---
description: Vectorize vector database operations for semantic search, embeddings, and RAG workflows
globs: ["src/retrieval/**", "src/consumers/**", "*.ts"]
alwaysApply: false
---

# Cloudflare Vectorize

## Overview

Vectorize is a globally distributed vector database for:
- Semantic search and classification
- Retrieval Augmented Generation (RAG)
- Recommendations and anomaly detection
- Providing context/memory to LLMs

## Creating an Index

```bash
# Create index with dimensions matching your embedding model
npx wrangler vectorize create knowledge-index \
  --dimensions=768 \
  --metric=cosine

# Common dimension sizes:
# - bge-small-en-v1.5: 384
# - bge-base-en-v1.5: 768
# - text-embedding-ada-002 (OpenAI): 1536
```

## Metadata Indexes

**CRITICAL**: Create metadata indexes BEFORE inserting vectors:

```bash
# String property
npx wrangler vectorize create-metadata-index knowledge-index \
  --property-name=contentType \
  --type=string

# Boolean property
npx wrangler vectorize create-metadata-index knowledge-index \
  --property-name=published \
  --type=boolean

# Number property
npx wrangler vectorize create-metadata-index knowledge-index \
  --property-name=relevanceScore \
  --type=number
```

## Configuration (wrangler.jsonc)

```jsonc
{
  "vectorize": [{
    "binding": "VECTORIZE",
    "index_name": "knowledge-index"
  }]
}
```

## Inserting Vectors

```typescript
interface Env {
  VECTORIZE: VectorizeIndex;
  AI: Ai;
}

// Generate embedding with Workers AI
const embedding = await env.AI.run("@cf/baai/bge-base-en-v1.5", {
  text: content
});

// Single vector
const vector: VectorizeVector = {
  id: "doc-123",
  values: embedding.data[0],
  metadata: {
    contentType: "article",
    path: "content/articles/doc.md",
    title: "Document Title",
    status: "published"
  }
};

await env.VECTORIZE.upsert([vector]);

// Batch insert
const vectors: VectorizeVector[] = documents.map((doc, i) => ({
  id: doc.id,
  values: embeddings[i],
  metadata: {
    contentType: doc.type,
    path: doc.path,
    status: doc.status
  }
}));

await env.VECTORIZE.upsert(vectors);
```

## Querying Vectors

### Basic Query

```typescript
const queryEmbedding = await env.AI.run("@cf/baai/bge-base-en-v1.5", {
  text: userQuery
});

const results = await env.VECTORIZE.query(queryEmbedding.data[0], {
  topK: 10,
  returnMetadata: "all"
});

// results.matches: Array<{
//   id: string;
//   score: number;
//   metadata?: Record<string, any>;
// }>
```

### Query with Metadata Filter

```typescript
const results = await env.VECTORIZE.query(queryEmbedding.data[0], {
  topK: 50,
  returnMetadata: "indexed",
  filter: {
    contentType: { $eq: "article" },
    status: { $eq: "published" }
  }
});
```

## Query Constraints (CRITICAL)

| Condition | Max topK | Use Case |
|-----------|----------|----------|
| With values or metadata | **20** | Need vector data or metadata |
| Without values AND metadata | **100** | Just IDs and scores |

`returnMetadata` accepts `"all"`, `"indexed"`, or `"none"`. `returnValues` defaults to `false`.

**Important**: Exceeding topK limits causes errors! If you need more results, set `returnMetadata: "none"` and `returnValues: false`.

## Filter Operators

```typescript
// Equality
{ field: { $eq: "value" } }

// Not equal
{ field: { $ne: "value" } }

// In array
{ field: { $in: ["a", "b", "c"] } }

// Not in array
{ field: { $nin: ["x", "y"] } }

// Numeric comparisons
{ score: { $gt: 0.5 } }
{ score: { $gte: 0.5 } }
{ score: { $lt: 1.0 } }
{ score: { $lte: 1.0 } }

// Combine filters (implicit AND)
{
  contentType: { $eq: "article" },
  status: { $in: ["published", "draft"] }
}
```

## Two-Stage Retrieval Pattern

For high-quality search combining vector search with reranking:

```typescript
interface Env {
  VECTORIZE: VectorizeIndex;
  AI: Ai;
  R2: R2Bucket;
}

async function search(query: string, env: Env) {
  // Stage 1: Generate query embedding
  const queryEmbedding = await env.AI.run("@cf/baai/bge-base-en-v1.5", {
    text: query
  });

  // Stage 2: Vector search with filter (get candidates)
  // topK up to 20 when returning metadata, up to 100 without
  const candidates = await env.VECTORIZE.query(queryEmbedding.data[0], {
    topK: 20,
    returnMetadata: "all",
    filter: { status: { $eq: "published" } }
  });

  // Stage 3: Fetch full content from R2
  const contents = await Promise.all(
    candidates.matches.map(async (match) => {
      const obj = await env.R2.get(match.metadata?.path as string);
      return obj ? await obj.text() : "";
    })
  );

  // Stage 4: Rerank with cross-encoder
  const reranked = await env.AI.run("@cf/baai/bge-reranker-base", {
    query: query,
    contexts: contents
      .filter(c => c.length > 0)
      .map(text => ({ text })),
    top_k: 10
  });

  // Stage 5: Map back to original results
  const finalResults = reranked.response.map((r: any) => ({
    ...candidates.matches[r.id],
    content: contents[r.id],
    rerankerScore: r.score
  }));

  return finalResults;
}
```

## Reranker API (CRITICAL)

**MUST use batch API format:**

```typescript
// ✅ CORRECT: Batch API
const result = await env.AI.run("@cf/baai/bge-reranker-base", {
  query: "search query",
  contexts: [
    { text: "passage 1" },
    { text: "passage 2" },
    { text: "passage 3" }
  ],
  top_k: 10
});

// Returns: { response: [{ id: 0, score: 0.95 }, { id: 2, score: 0.87 }, ...] }

// ❌ WRONG: Per-document format (deprecated)
// const result = await env.AI.run("@cf/baai/bge-reranker-base", {
//   text: ["query", "passage"]  // DON'T USE THIS
// });
```

## Normalize Reranker Scores

Raw reranker scores aren't bounded. Use sigmoid normalization:

```typescript
function sigmoid(x: number): number {
  return 1 / (1 + Math.exp(-x));
}

const normalizedResults = reranked.response
  .map((r: any) => ({
    ...r,
    normalizedScore: sigmoid(r.score)
  }))
  .filter((r: any) => r.normalizedScore >= 0.5);  // Quality threshold
```

## Delete Vectors

```typescript
// Delete by IDs
await env.VECTORIZE.deleteByIds(["doc-123", "doc-456"]);

// Note: No bulk delete by filter - track IDs for deletion
```

## Get Vector by ID

```typescript
const vectors = await env.VECTORIZE.getByIds(["doc-123", "doc-456"]);
// Returns array of VectorizeVector
```

## Best Practices

### Index Design
- One index per use case (search, recommendations, etc.)
- Match dimensions to embedding model exactly
- Create metadata indexes upfront

### Metadata Strategy
- **Indexed metadata**: For filtering (contentType, status, date)
- **Non-indexed metadata**: For display (title, description)
- Keep indexed metadata minimal for performance

### Query Optimization
- Use filters to reduce search space
- Start with `returnMetadata: "indexed"` for larger topK
- Fetch full content from R2 only for top results

### Embedding Consistency
- Use same model for indexing and querying
- Normalize input text consistently
- Consider chunking strategy for long documents

## Error Handling

```typescript
try {
  const results = await env.VECTORIZE.query(embedding, { topK: 10 });
} catch (error) {
  if (error.message.includes("topK")) {
    // Exceeded topK limit for returnMetadata setting
  }
  if (error.message.includes("dimension")) {
    // Vector dimensions don't match index
  }
}
```

## Sources
- https://developers.cloudflare.com/vectorize/
- https://developers.cloudflare.com/vectorize/best-practices/
- https://developers.cloudflare.com/vectorize/reference/client-api/
- https://developers.cloudflare.com/workers-ai/models/bge-base-en-v1.5/
- https://developers.cloudflare.com/workers-ai/models/bge-reranker-base/
