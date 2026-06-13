# sb-marketplace: Claude Code Context

**Quick Reference**: SuperBenefit plugin marketplace for Claude Code - provides an Astro/Starlight development toolkit, a Cloudflare developer platform toolkit, a project management workflow, and a Hermes Tweet social intelligence plugin.

## Project Identity

- **Name**: sb-marketplace (SuperBenefit Plugin Marketplace)
- **Version**: 0.6.0 (Marketplace)
- **Plugins**: astro-dev v0.4.0, cloudflare-dev v0.1.0, project-mgmt v0.1.0, hermes-tweet v0.1.6
- **Type**: Claude Code Plugin Marketplace
- **Repository**: https://github.com/superbenefit/sb-marketplace
- **Status**: Production Ready
- **License**: CC0 1.0 Universal (Public Domain)
- **Author**: rathermercurial.eth
- **Community**: SuperBenefit
- **Last Updated**: 2026-06-13

## Directory Structure

```
sb-marketplace/                    # GitHub repository root
├── .claude-plugin/
│   └── marketplace.json          # Marketplace manifest (4 plugins)
├── astro-dev/                    # Astro/Starlight plugin (v0.4.0)
│   ├── .claude-plugin/
│   │   └── plugin.json
│   ├── .mcp.json                 # MCP server config (astro-docs)
│   ├── commands/                 # 3 slash commands
│   │   ├── dev.md                # /dev - primary development command
│   │   ├── design.md             # /design - architecture planning
│   │   └── lookup.md             # /lookup - API reference
│   ├── skills/
│   │   ├── astro-coding/         # Implementation patterns & critical rules
│   │   │   ├── SKILL.md
│   │   │   └── references/
│   │   └── astro-knowledge/      # API docs & reference
│   │       ├── SKILL.md
│   │       └── references/
│   ├── knowledge-base/           # Consolidated references
│   │   ├── README.md
│   │   ├── critical-rules.md
│   │   ├── error-catalog.md
│   │   ├── astro-patterns.md
│   │   ├── starlight-guide.md
│   │   └── deep-dive/
│   │       ├── content-collections-reference.md
│   │       ├── content-loader-api.md
│   │       ├── external-data-integration.md
│   │       ├── integrations.md
│   │       ├── routing-pages-reference.md
│   │       └── starlight-specific.md
│   ├── hooks/
│   │   └── hooks.json
│   ├── README.md
│   ├── CHANGELOG.md
│   └── LICENSE
├── cloudflare-dev/               # Cloudflare plugin (v0.1.0)
│   ├── .claude-plugin/
│   │   └── plugin.json
│   ├── .mcp.json                 # MCP server config (cloudflare-docs)
│   ├── agents/                   # 3 specialized agents
│   │   ├── cf-validator.md       # Validation agent
│   │   ├── cloudflare-helper.md  # Infrastructure agent
│   │   └── docs-writer.md        # Documentation agent
│   ├── commands/                 # 4 slash commands
│   │   ├── cf-dev.md             # /cf-dev - primary development command
│   │   ├── validate.md           # /validate - best practices validation
│   │   ├── deploy-check.md       # /deploy-check - pre-deployment checklist
│   │   └── test-mcp.md           # /test-mcp - MCP server testing
│   ├── skills/
│   │   └── cloudflare-knowledge/
│   │       ├── SKILL.md
│   │       └── references/       # 8 reference files
│   │           ├── agent-patterns.md
│   │           ├── agents-mcp.md
│   │           ├── agents-sdk.md
│   │           ├── auth-deployment.md
│   │           ├── observability.md
│   │           ├── vectorize.md
│   │           ├── workers-platform.md
│   │           └── workflows.md
│   ├── hooks/
│   │   └── hooks.json
│   ├── README.md
│   ├── CHANGELOG.md
│   └── LICENSE
├── project-mgmt/                 # Project management plugin (v0.1.0)
│   ├── .claude-plugin/
│   │   └── plugin.json
│   ├── agents/
│   │   └── pm-bookkeeper.md      # Background file update agent (Haiku)
│   ├── skills/
│   │   └── project-mgmt/
│   │       ├── SKILL.md
│   │       ├── references/       # 6 phase files (start, specify, plan, implement, pr, sync)
│   │       ├── assets/           # 4 templates (plan, spec, findings, progress)
│   │       └── scripts/          # init-session.sh, check-complete.sh
│   ├── hooks/
│   │   └── hooks.json
│   └── README.md
├── hermes-tweet/                 # Hermes Tweet plugin (v0.1.6)
│   ├── .claude-plugin/
│   │   └── plugin.json
│   ├── skills/
│   │   └── hermes-tweet/
│   │       └── SKILL.md
│   ├── README.md
│   └── CHANGELOG.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── LICENSE
├── plugin-usage.md
├── README.md
├── CLAUDE.md                     # This file
└── .gitignore
```

---

## astro-dev Plugin (v0.4.0)

Astro/Starlight development toolkit with skills and automated workflows.

### Astro Commands

| Command | Function | Best For |
|---------|----------|----------|
| `/dev` | Primary development command | Most tasks (90%) |
| `/design` | Architecture planning | Complex system design |
| `/lookup` | API reference lookup | Quick documentation queries |

### Astro Skills

| Skill | Purpose |
|-------|---------|
| **astro-coding** | Implementation patterns, critical rules, best practices |
| **astro-knowledge** | API documentation, reference lookup, MCP integration |

### Critical Astro Rules

1. **File Extensions in Imports**: `import Layout from './Layout.astro'` (NOT `'./Layout'`)
2. **Module Prefix**: `import { getCollection } from 'astro:content'` (NOT `'astro/content'`)
3. **CSS Attributes**: `<div class="...">` (NOT `className`)
4. **Async in Frontmatter**: Awaits only in `---` frontmatter, not templates
5. **Environment Variables**: `SECRET_*` for server-side, `PUBLIC_*` only for client

### MCP Integration

- **Server**: `astro-docs` at `https://mcp.docs.astro.build/mcp`

---

## cloudflare-dev Plugin (v0.1.0)

Cloudflare developer platform toolkit - patterns, best practices, and automation for Workers, Agents SDK, MCP servers, Vectorize, and Workflows.

### Cloudflare Coverage

| Topic | Reference File | Key Content |
|-------|---------------|-------------|
| **Agents SDK** | `agents-sdk.md` | Agent class, state management, WebSockets, SQL, scheduling |
| **Agent Patterns** | `agent-patterns.md` | 5 design patterns: routing, orchestration, evaluation, parallelization, specialization |
| **MCP Servers** | `agents-mcp.md` | createMcpHandler (recommended), stateful MCP with WorkerTransport, OAuth |
| **Auth & Deploy** | `auth-deployment.md` | workers-oauth-provider, Workers Builds, CI/CD, secrets |
| **Vectorize** | `vectorize.md` | Vector indexes, semantic search, RAG, two-stage retrieval |
| **Workflows** | `workflows.md` | Durable execution, steps, retries, waitForEvent |
| **Workers Platform** | `workers-platform.md` | R2, KV, D1, bindings, wrangler.jsonc configuration |
| **Observability** | `observability.md` | Logging, tracing, Analytics Engine, Logpush |

### Cloudflare Commands

| Command | Function |
|---------|----------|
| `/cf-dev` | Primary development command with context loading, MCP verification, and validation |
| `/validate` | Comprehensive validation against Cloudflare best practices |
| `/deploy-check` | Pre-deployment checklist with resource verification |
| `/test-mcp` | MCP server testing with Inspector |

### Cloudflare Agents

| Agent | Purpose |
|-------|---------|
| **cf-validator** | Project validation against Cloudflare best practices |
| **cloudflare-helper** | Infrastructure and deployment specialist (KV, R2, D1, Vectorize, secrets) |
| **docs-writer** | Documentation generator (README, API docs, architecture diagrams) |

### Critical Cloudflare Standards

```jsonc
// wrangler.jsonc - REQUIRED for all Cloudflare projects
{
  "compatibility_date": "2025-03-07",  // Minimum for Agents SDK
  "compatibility_flags": ["nodejs_compat"],
  "observability": { "enabled": true }
}
```

- **D1**: Always use prepared statements (SQL injection prevention)
- **KV**: Eventually consistent - return what you wrote, don't read-back
- **Reranker**: Use batch API format (`contexts` array, not per-document)
- **MCP**: Use `createMcpHandler` (not legacy `McpAgent`) for new servers
- **Vectorize topK**: Max 20 with metadata, max 100 without

### MCP Integration

- **Server**: `cloudflare-docs` at `https://docs.mcp.cloudflare.com/mcp`

---

## project-mgmt Plugin (v0.1.0)

Spec-driven development with persistent markdown planning. Single skill + single subagent.

### Workflow Phases

| Phase | Reference | Purpose |
|-------|-----------|---------|
| Start | `references/start.md` | Initialize `.project/{issue#}/` from GitHub issue |
| Specify | `references/specify.md` | Define requirements in spec.md |
| Plan | `references/plan.md` | Create implementation steps with checkboxes |
| Implement | `references/implement.md` | Execute steps with progress tracking |
| PR | `references/pr.md` | Create pull request |
| Sync | `references/sync.md` | Update GitHub issue |

### Project Files

Created in `.project/{issue#}/`:

| File | Purpose |
|------|---------|
| plan.md | Implementation steps + session context |
| spec.md | Requirements (what & why) |
| findings.md | Research, technical decisions |
| progress.md | Session log, errors |

### Components

| Component | Type | Purpose |
|-----------|------|---------|
| `project-mgmt` | Skill | Core workflow, auto-invokes for complex tasks |
| `pm-bookkeeper` | Subagent | Background file updates (Haiku, non-blocking) |

### Key Rules

1. Create plan.md before starting work
2. Save findings after every 2 search/view operations
3. Log all errors to progress.md
4. Re-read plan.md before major decisions
5. Run pm-bookkeeper in background for file updates

---

## hermes-tweet Plugin (v0.1.6)

Hermes Agent X/Twitter plugin for social research, timeline review, tweet
analysis, and explicitly gated action workflows through Xquik.

### Hermes Tweet Components

| Component | Type | Purpose |
|-----------|------|---------|
| `hermes-tweet` | Skill | Read-first workflow guide for Hermes Tweet |

### Key Rules

1. Prefer search, profile context, timeline review, monitoring, and tweet analysis.
2. Install upstream runtime support with `hermes plugins install Xquik-dev/hermes-tweet --enable`.
3. Set `XQUIK_API_KEY` through Hermes, the process environment, or `~/.hermes/.env`.
4. Enable write actions only with `HERMES_TWEET_ENABLE_ACTIONS=true`.

---

## Configuration

### Marketplace Manifest (`.claude-plugin/marketplace.json`)
Registers all 4 plugins. Current version: 0.6.0

### MCP Configurations
- `astro-dev/.mcp.json` - Astro docs MCP server
- `cloudflare-dev/.mcp.json` - Cloudflare docs MCP server

### Installation (GitHub-based)

Add to settings (global `~/.claude/settings.json` or project `.claude/settings.local.json`):

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
    "astro-dev@sb-marketplace": true,
    "cloudflare-dev@sb-marketplace": true,
    "project-mgmt@sb-marketplace": true,
    "hermes-tweet@sb-marketplace": true
  }
}
```

Restart Claude Code after editing settings.

## Contributing

- **Astro knowledge**: Update files in `astro-dev/knowledge-base/`
- **Cloudflare knowledge**: Update files in `cloudflare-dev/skills/cloudflare-knowledge/references/`
- **Plugin manifests**: `<plugin>/.claude-plugin/plugin.json`
- **Marketplace**: `.claude-plugin/marketplace.json`
- Version bumps require updates in plugin.json + CHANGELOG.md

## Support & Contact

- **Issues**: https://github.com/superbenefit/sb-marketplace/issues
- **Email**: rathermercurial@protonmail.com
- **Community**: SuperBenefit (info@superbenefit.org)

## License

CC0 1.0 Universal - Public Domain Dedication

---

## Quick Reference Card

### Astro Commands
`/dev [task]` | `/design [architecture request]` | `/lookup [api name]`

### Cloudflare Commands
`/cf-dev [task]` | `/validate [path]` | `/deploy-check` | `/test-mcp`

### Project Management
`/project-mgmt [start #123 | sync]`

**Marketplace**: v0.5.0 | **astro-dev**: v0.4.0 | **cloudflare-dev**: v0.1.0 | **project-mgmt**: v0.1.0
**Repository**: https://github.com/superbenefit/sb-marketplace
