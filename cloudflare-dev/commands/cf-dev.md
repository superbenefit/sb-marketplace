---
name: cf-dev
description: Primary development command for building on the Cloudflare developer platform. Loads platform knowledge and validates against current best practices.
---

# Cloudflare Development Workflow

You are working on a Cloudflare project. Follow this workflow for all implementation tasks.

## Step 1: Load Context

Read the relevant reference file(s) from the `cloudflare-knowledge` skill based on the task:

| Task Type | Reference File | Key Focus |
|-----------|---------------|-----------|
| Agent class, state, WebSocket | `agents-sdk.md` | `new_sqlite_classes` in migrations |
| AI agent design patterns | `agent-patterns.md` | Pattern selection guide |
| MCP server or client | `agents-mcp.md` | `createMcpHandler` (recommended) |
| Vector search, RAG, embeddings | `vectorize.md` | topK limits per returnMetadata |
| Durable execution, retries | `workflows.md` | Always `await step.do()` |
| Workers, R2, KV, D1, bindings | `workers-platform.md` | Use bindings, not REST API |
| OAuth, CI/CD, secrets, deploys | `auth-deployment.md` | `workers-oauth-provider` patterns |
| Logs, traces, analytics | `observability.md` | `observability: { enabled: true }` |

Reference files are located at: `${CLAUDE_PLUGIN_ROOT}/skills/cloudflare-knowledge/references/`

## Step 2: Verify with Cloudflare Docs MCP

Before implementing any pattern, verify the current API against the `cloudflare-docs` MCP server:

**Recommended MCP queries by task:**
- Agents: `"Agents SDK Agent class API"`, `"Agents SDK state management"`
- MCP servers: `"createMcpHandler MCP server"`, `"workers-oauth-provider"`
- Storage: `"R2 Workers API put get"`, `"KV Workers API"`, `"D1 prepared statements"`
- Vectorize: `"Vectorize query API topK"`, `"Workers AI reranker"`
- Workflows: `"Workflows step.do"`, `"Workflows waitForEvent"`
- Observability: `"Workers observability traces"`, `"Analytics Engine writeDataPoint"`
- Deployment: `"Workers Builds"`, `"wrangler secret"`

## Step 3: Implement

Follow the validated patterns from Steps 1-2. Apply these critical standards to ALL code:

### Mandatory Configuration (wrangler.jsonc)
```jsonc
{
  "compatibility_date": "2025-03-07",  // Minimum for Agents
  "compatibility_flags": ["nodejs_compat"],
  "observability": { "enabled": true }
}
```

### Critical Rules
1. **WebSocket Hibernation API**: Use `this.ctx.acceptWebSocket(server)` + `webSocketMessage()` handlers. Never use legacy `server.accept()` + `addEventListener`.
2. **Reranker Batch API**: Use `{ query, contexts: [{text}], top_k }`. Never use deprecated `{ text: [query, passage] }`.
3. **MCP pattern**: Use `createMcpHandler` for new stateless servers. Use `McpAgent` only for SSE backward compatibility.
4. **Vectorize topK limits**: `"all"` → max 20, `"indexed"` → max 100, `"none"` → max 1000.
5. **Workflow steps**: Always `await step.do()`. Steps must be idempotent. No side effects outside steps.
6. **Agent migrations**: Always include `new_sqlite_classes: ["ClassName"]` in migrations block.
7. **Bindings**: Always use env bindings from Workers (not REST API). Use prepared statements for D1.

## Step 4: Validate

Before completing, verify:
- [ ] wrangler.jsonc has correct compatibility_date, flags, observability, migrations
- [ ] All Agent/DO classes listed in `new_sqlite_classes`
- [ ] MCP servers use `createMcpHandler` (or justified McpAgent usage)
- [ ] Reranker uses batch API format
- [ ] Vectorize queries respect topK limits
- [ ] Workflow steps are awaited and idempotent
- [ ] TypeScript compiles without errors

## Usage

```
/cf-dev $ARGUMENTS
```

`$ARGUMENTS` describes the development task. Examples:
- `/cf-dev Build an MCP server with vector search`
- `/cf-dev Add a Workflow for content syncing`
- `/cf-dev Configure R2 bucket with event notifications`
- `/cf-dev Set up OAuth for the MCP server`
