# Cloudflare Dev Plugin

Cloudflare developer platform toolkit for Claude Code - patterns, best practices, and automation for building on the Cloudflare edge.

## Overview

The cloudflare-dev plugin provides expert assistance for Cloudflare Workers, Agents SDK, MCP servers, Vectorize, and Workflows through specialized commands, agents, and a comprehensive knowledge base.

**Version**: 0.1.0

## Quick Start

```bash
# Primary development command
/cf-dev Build an MCP server with OAuth authentication

# Validate a project against best practices
/validate

# Pre-deployment checklist
/deploy-check

# Test MCP server with Inspector
/test-mcp
```

## Commands

### `/cf-dev [description]`
**Primary command** for Cloudflare development. Loads relevant context, verifies against MCP docs, implements, and validates.

```bash
/cf-dev Create a Vectorize-backed RAG agent with semantic search
/cf-dev Add OAuth authentication to my MCP server
/cf-dev Build a Workflow for content sync with retry logic
```

### `/validate`
**Comprehensive validation** against Cloudflare best practices.

```bash
/validate              # Full project validation
/validate src/         # Validate specific directory
```

Checks: configuration, dependencies, MCP patterns, API patterns, workflow patterns.

### `/deploy-check`
**Pre-deployment checklist** with resource verification.

```bash
/deploy-check          # Run full deployment readiness check
```

### `/test-mcp`
**MCP server testing** with the MCP Inspector tool.

```bash
/test-mcp              # Start interactive MCP testing
```

## Agents

### `cf-validator`
Validates projects against Cloudflare best practices. Checks configuration, dependencies, MCP server patterns, API usage, and workflow patterns.

### `cloudflare-helper`
Infrastructure and deployment specialist. Handles KV, R2, D1, Vectorize, Queues, secrets management, and debugging.

### `docs-writer`
Documentation generator. Produces README files, API docs, architecture diagrams, and troubleshooting guides.

## Knowledge Base

The plugin includes comprehensive reference documentation:

| File | Coverage |
|------|----------|
| `agents-sdk.md` | Agent class, state, scheduling, WebSockets, SQL |
| `agent-patterns.md` | 5 design patterns (chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer) |
| `agents-mcp.md` | MCP servers (createMcpHandler, stateful, OAuth, client) |
| `auth-deployment.md` | OAuth (workers-oauth-provider), CI/CD, secrets, deploy buttons |
| `vectorize.md` | Vector search, metadata, reranker, two-stage retrieval |
| `workflows.md` | Durable execution, steps, waitForEvent, error handling |
| `workers-platform.md` | R2, KV, D1 APIs, all binding types, wrangler.jsonc |
| `observability.md` | Logging, traces, Analytics Engine, Tail Workers |

## Critical Standards

These are enforced in all generated code:

```jsonc
// wrangler.jsonc - REQUIRED settings
{
  "compatibility_date": "2025-03-07",        // Minimum for Agents
  "compatibility_flags": ["nodejs_compat"],
  "observability": { "enabled": true }
}
```

- **Agents**: `new_sqlite_classes` MUST be in migrations
- **MCP**: Use `createMcpHandler` (not legacy McpAgent) for new servers
- **D1**: Always use prepared statements (no string interpolation)
- **KV**: Eventually consistent - return written value, don't re-read
- **R2**: Use conditional headers for cache-aware reads
- **Vectorize**: topK max 20 with metadata, max 100 without
- **Reranker**: Must use batch API format
- **Workflows**: Always await steps, steps must be idempotent

## MCP Integration

Connects to the Cloudflare docs MCP server for real-time API verification:
- Server: `https://docs.mcp.cloudflare.com/mcp`
- Used by `/cf-dev` command to verify implementations

## Installation

### Via GitHub Marketplace

Add to your Claude Code settings (global `~/.claude/settings.json` or project `.claude/settings.local.json`):

```json
{
  "extraKnownMarketplaces": {
    "sb-marketplace": {
      "source": {
        "source": "github",
        "repo": "superbenefit/sb-marketplace"
      }
    }
  },
  "enabledPlugins": {
    "cloudflare-dev@sb-marketplace": true
  }
}
```

Restart Claude Code to load the plugin.

## File Organization

```
cloudflare-dev/
├── .claude-plugin/
│   └── plugin.json                    # Plugin manifest
├── .mcp.json                          # MCP server config
├── agents/
│   ├── cf-validator.md                # Validation agent
│   ├── cloudflare-helper.md           # Infrastructure agent
│   └── docs-writer.md                 # Documentation agent
├── commands/
│   ├── cf-dev.md                      # Primary dev command
│   ├── validate.md                    # Validation command
│   ├── deploy-check.md                # Deployment checklist
│   └── test-mcp.md                    # MCP testing
├── hooks/
│   └── hooks.json                     # Reserved for future
├── skills/
│   └── cloudflare-knowledge/
│       ├── SKILL.md                   # Skill manifest
│       └── references/                # 8 reference files
├── CHANGELOG.md
├── LICENSE
└── README.md
```

## Support

- **Issues**: [GitHub Issues](https://github.com/superbenefit/sb-marketplace/issues)
- **Email**: rathermercurial@protonmail.com
- **Community**: SuperBenefit (info@superbenefit.org)

## License

CC0 1.0 Universal - Public Domain Dedication

## Author

Created by rathermercurial.eth for the SuperBenefit community.
