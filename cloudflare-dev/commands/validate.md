---
name: validate
description: Validate a Cloudflare project against platform best practices and SDK patterns
---

# Validate Cloudflare Implementation

Run a comprehensive validation of the current project against Cloudflare best practices.

## Validation Steps

### 1. Configuration Check (wrangler.jsonc)

Verify:
- `compatibility_date` is set and appropriate (>= `"2025-03-07"` for Agents SDK)
- `compatibility_flags` includes `"nodejs_compat"`
- `observability: { "enabled": true }` is present
- `migrations` block has `new_sqlite_classes` for every Agent/DO class
- All required bindings are declared (KV, R2, D1, Vectorize, DO, AI, Queues)
- No stale or orphaned bindings

### 2. Dependencies Check (package.json)

Verify:
- `agents` package installed (for Agents SDK projects)
- `@modelcontextprotocol/sdk` installed (for MCP servers)
- `workers-oauth-provider` installed (if using OAuth)
- No known deprecated packages
- TypeScript and wrangler are dev dependencies

### 3. MCP Server Pattern Check

If the project has MCP servers, verify:
- Uses `createMcpHandler` for stateless servers (recommended pattern)
- If using `McpAgent`: server is a class property, tools registered in `init()`
- Tool parameters use Zod schemas with `.describe()` annotations
- Error responses include `isError: true`
- OAuth uses `workers-oauth-provider` with proper KV binding

### 4. API Pattern Check

Verify:
- Reranker uses batch API: `{ query, contexts: [{text}], top_k }`
- Vectorize queries respect topK limits per `returnMetadata` setting
- WebSocket uses hibernation API (not legacy `addEventListener`)
- SQL uses tagged template literals (`this.sql\`...\``)
- D1 uses prepared statements
- R2 accessed via bindings (not REST API)

### 5. Workflow Pattern Check (if applicable)

Verify:
- All `step.do()` calls are awaited
- Steps are idempotent (safe to retry)
- No side effects outside steps
- Bindings accessed via `this.env` (not closures)
- Return values are JSON-serializable

## Output

Report findings as:
- ✅ **Compliant**: Follows best practices
- ❌ **Non-compliant**: Must fix (with file:line reference and suggested fix)
- ⚠️ **Warning**: Should consider (with recommendation)

## Usage

```
/validate $ARGUMENTS
```

`$ARGUMENTS` optionally specifies a path or focus area. Examples:
- `/validate` - Full project validation
- `/validate src/server/` - Validate specific directory
- `/validate mcp` - Focus on MCP patterns only
- `/validate config` - Focus on wrangler.jsonc and package.json only
