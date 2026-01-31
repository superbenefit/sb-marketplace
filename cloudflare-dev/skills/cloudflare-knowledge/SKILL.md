---
description: Cloudflare edge platform patterns for Workers, Agents SDK, MCP servers, Vectorize, and Workflows. Use when building on Cloudflare infrastructure.
globs: ["src/**/*.ts", "wrangler.jsonc", "*.ts"]
alwaysApply: false
---

# Cloudflare Knowledge

## Quick Reference

| Task | Read File | Key Constraint |
|------|-----------|----------------|
| Building Agent class | `agents-sdk.md` | `new_sqlite_classes` in migrations |
| Agent design patterns | `agent-patterns.md` | Use AI SDK with Durable Objects |
| MCP server (stateless) | `agents-mcp.md` | Use `createMcpHandler` (recommended) |
| MCP server (stateful) | `agents-mcp.md` | Agent + WorkerTransport + createMcpHandler |
| OAuth / auth patterns | `auth-deployment.md` | `OAUTH_KV` binding required for workers-oauth-provider |
| Vector search | `vectorize.md` | topK ≤20 with metadata, ≤100 without |
| Durable execution | `workflows.md` | Always `await step.do()`, steps must be idempotent |
| R2, KV, D1 bindings | `workers-platform.md` | Use bindings (not REST APIs), D1 prepared statements |
| Logging & tracing | `observability.md` | `observability: { enabled: true }` in wrangler.jsonc |
| CI/CD & deployment | `auth-deployment.md` | Workers Builds, GitHub Actions, secrets management |

## Critical Standards (Always Apply)
```jsonc
// wrangler.jsonc - REQUIRED settings
{
  "compatibility_date": "2025-03-07",  // Minimum for Agents
  "compatibility_flags": ["nodejs_compat"],
  "observability": { "enabled": true }
}
```

### Reranker: MUST Use Batch API
```typescript
// ✅ CORRECT
await env.AI.run("@cf/baai/bge-reranker-base", {
  query: "search query",
  contexts: [{ text: "passage1" }, { text: "passage2" }],
  top_k: 10
});

// ❌ WRONG - deprecated per-document format
await env.AI.run("@cf/baai/bge-reranker-base", {
  text: ["query", "passage"]
});
```

### D1: MUST Use Prepared Statements
```typescript
// ✅ CORRECT
env.DB.prepare("SELECT * FROM users WHERE id = ?").bind(userId)

// ❌ WRONG - SQL injection risk
env.DB.prepare(`SELECT * FROM users WHERE id = '${userId}'`)
```

### KV: Eventually Consistent
```typescript
// ✅ CORRECT - return what you wrote
await env.MY_KV.put("key", newValue);
return Response.json({ value: newValue });

// ❌ WRONG - may return stale data
await env.MY_KV.put("key", newValue);
const readBack = await env.MY_KV.get("key"); // May be stale!
```

## When to Read Detail Files

**Read `agents-sdk.md` when:**
- Creating a new Agent class
- Implementing state management (`this.setState`, `this.sql`)
- Adding scheduling (`this.schedule`)
- Handling WebSocket connections
- Client APIs (AgentClient, useAgent hook)

**Read `agent-patterns.md` when:**
- Designing multi-step AI workflows
- Implementing routing/classification
- Building orchestrator-worker systems
- Need evaluator-optimizer loops

**Read `agents-mcp.md` when:**
- Building an MCP server (use `createMcpHandler`)
- Registering tools with schemas
- Adding OAuth authentication to MCP
- Connecting to external MCP servers as a client

**Read `auth-deployment.md` when:**
- Adding authentication (workers-oauth-provider, OAuth 2.1)
- Setting up CI/CD (Workers Builds, GitHub Actions, GitLab CI)
- Managing secrets (wrangler secret, .dev.vars)
- Creating deploy buttons

**Read `vectorize.md` when:**
- Creating/querying vector indexes
- Implementing semantic search or RAG
- Building two-stage retrieval (vector + rerank)
- Setting up metadata filters

**Read `workflows.md` when:**
- Building durable/long-running tasks
- Need automatic retries with backoff
- Implementing human-in-the-loop (waitForEvent)
- Scheduling delayed execution

**Read `workers-platform.md` when:**
- Using R2 (object storage), KV (key-value), or D1 (SQL)
- Configuring wrangler.jsonc bindings
- Need binding types reference
- Working with multipart uploads, presigned URLs

**Read `observability.md` when:**
- Setting up logging (Workers Logs, wrangler tail)
- Implementing distributed tracing
- Adding custom analytics (Analytics Engine)
- Configuring Logpush or Tail Workers

## File Locations
All detail files are in the `references/` subdirectory of this skill. Read the relevant file before implementing.
