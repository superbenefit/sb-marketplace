---
name: deploy-check
description: Pre-deployment checklist for Cloudflare Workers projects
---

# Pre-Deployment Checklist

Run through all deployment prerequisites before pushing to production.

## Checks

### 1. TypeScript Compilation
```bash
npm run typecheck
```
All type errors must be resolved before deploying.

### 2. Configuration Validation
Verify `wrangler.jsonc`:
- [ ] `compatibility_date` is current and intentional
- [ ] `compatibility_flags` includes `"nodejs_compat"`
- [ ] `observability: { "enabled": true }` is set
- [ ] `migrations` block is correct (includes all DO/Agent classes in `new_sqlite_classes`)
- [ ] All bindings reference valid resources

### 3. Secrets Verification
```bash
npx wrangler secret list
```
Verify all required secrets are set. Cross-reference with:
- Environment variables referenced in code (`env.SECRET_NAME`)
- OAuth configuration (client IDs, client secrets)
- API keys for external services

### 4. Resource Verification

**Vectorize indexes** (if used):
```bash
npx wrangler vectorize list
```
- Verify indexes exist with correct dimensions and metrics
- Verify metadata indexes are created

**KV namespaces** (if used):
```bash
npx wrangler kv namespace list
```

**R2 buckets** (if used):
```bash
npx wrangler r2 bucket list
```

**D1 databases** (if used):
```bash
npx wrangler d1 list
```

### 5. Local Testing
- [ ] MCP Inspector test passes (`/test-mcp`)
- [ ] Key functionality verified locally
- [ ] Error handling tested

### 6. Deploy

If all checks pass:
```bash
npm run deploy
```

## Usage

```
/deploy-check $ARGUMENTS
```

`$ARGUMENTS` optionally limits scope. Examples:
- `/deploy-check` - Full checklist
- `/deploy-check secrets` - Only check secrets
- `/deploy-check resources` - Only verify cloud resources
