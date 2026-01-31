# Changelog

All notable changes to the Cloudflare Dev plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-30

### Initial Release

First release of the Cloudflare developer platform toolkit.

### Added

#### Commands
- **/cf-dev**: Primary development command with context loading, MCP verification, and validation
- **/validate**: Comprehensive validation against Cloudflare best practices
- **/deploy-check**: Pre-deployment checklist with resource verification
- **/test-mcp**: MCP server testing with Inspector

#### Agents
- **cf-validator**: Project validation against Cloudflare best practices
- **cloudflare-helper**: Infrastructure and deployment specialist
- **docs-writer**: Documentation generator

#### Skills
- **cloudflare-knowledge**: Comprehensive reference documentation with selective loading

#### Knowledge Base (8 reference files)
- **agents-sdk.md**: Agent class API, state management, scheduling, WebSockets, SQL
- **agent-patterns.md**: 5 AI agent design patterns (prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer)
- **agents-mcp.md**: MCP server patterns (createMcpHandler, stateful, OAuth, client)
- **auth-deployment.md**: Authentication (workers-oauth-provider), CI/CD, secrets, deploy buttons
- **vectorize.md**: Vector database operations, metadata, reranker, two-stage retrieval
- **workflows.md**: Durable execution, steps, waitForEvent, error handling
- **workers-platform.md**: R2, KV, D1 APIs, all binding types, wrangler.jsonc configuration
- **observability.md**: Logging, traces, Analytics Engine, Tail Workers

#### Infrastructure
- MCP server integration (docs.mcp.cloudflare.com)
- Plugin manifest with auto-discovery
- Hooks configuration (reserved for future)

### Compatibility

- **Claude Code**: Latest version
- **Cloudflare Workers**: Current platform
- **Agents SDK**: Current version
- **Wrangler**: v3+

---

**License**: CC0 1.0 Universal - Public Domain Dedication
**Author**: rathermercurial.eth
**Community**: SuperBenefit
