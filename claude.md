# sb-marketplace: Claude Code Context

**Quick Reference**: This is the Astro Dev Marketplace - a local plugin marketplace for Claude Code providing a comprehensive Astro/Starlight development toolkit (v2.0.0).

## Project Identity

- **Name**: sb-marketplace (Astro Dev Marketplace)
- **Version**: 2.0.0 (Marketplace: 1.0.0)
- **Type**: Claude Code Plugin Marketplace
- **Status**: Production-ready (stable)
- **License**: CC0 1.0 Universal (Public Domain)
- **Author**: rathremercurial.eth
- **Community**: SuperBenefit
- **Last Updated**: 2025-10-18

## Architecture at a Glance

### V2.0 Orchestration Model

The plugin uses a **multi-layer orchestration architecture** with intelligent task coordination:

```
User Commands (/develop, /implement, /architect, /audit, /lookup)
        ↓
Orchestration Layer (astro-orchestrator)
  • Task analysis & complexity estimation
  • Agent coordination (parallel when beneficial)
  • Audit rigor calibration (light/medium/comprehensive)
  • Token optimization via selective loading
        ↓
Specialized Agents (astro-developer, astro-architect, astro-auditor)
  • Code implementation with best practices
  • System design & architecture planning
  • 3-priority validation (P1: Breaking, P2: Security, P3: Best practices)
        ↓
Capability Providers (astro-coding skill, astro-knowledge skill)
  • Implementation patterns & critical rules
  • API documentation & reference lookup
  • Progressive disclosure (metadata → body → resources)
        ↓
Knowledge Base (5 consolidated files, ~1500 lines)
  • error-catalog.md (indexed by symptom)
  • astro-patterns.md (components, routing, collections)
  • starlight-guide.md (Starlight-specific features)
  • integrations.md (loaders, external data, TypeScript)
  • content-knowledge/ (detailed references)
```

### Key Design Principles

1. **Token Optimization**: 50% reduction through consolidation + selective loading
2. **Progressive Disclosure**: Load metadata first, resources on-demand
3. **Adaptive Validation**: Audit rigor scales with task complexity
4. **Parallel Execution**: Multiple agents work simultaneously when beneficial
5. **Rule Enforcement**: 5 critical rules enforced in ALL code

## Directory Structure

```
F:/projects/sb-marketplace/
├── .claude-plugin/
│   └── marketplace.json          # Marketplace manifest (plugin registry)
├── .claude/                      # Claude Code local settings (gitignored)
├── astro-dev/                    # Main plugin directory (v2.0.0)
│   ├── .claude-plugin/
│   │   └── plugin.json           # Plugin manifest
│   ├── .mcp.json                 # MCP server config (astro-docs)
│   ├── agents/                   # 4 specialized agents
│   │   ├── astro-orchestrator.md # Task coordinator
│   │   ├── astro-developer.md    # Code implementation
│   │   ├── astro-auditor.md      # Code validation
│   │   └── astro-architect.md    # System design planning
│   ├── commands/                 # 5 slash commands
│   │   ├── develop.md            # /develop - orchestrated workflow
│   │   ├── implement.md          # /implement - direct implementation
│   │   ├── architect.md          # /architect - architecture planning
│   │   ├── audit.md              # /audit - code validation
│   │   └── lookup.md             # /lookup - API reference
│   ├── skills/                   # 2 capability providers
│   │   ├── astro-coding/         # Implementation patterns
│   │   │   ├── SKILL.md
│   │   │   └── references/
│   │   └── astro-knowledge/      # API docs & reference
│   │       ├── SKILL.md
│   │       └── references/       # (docs-index.md, llms.txt, llms-full.md)
│   ├── knowledge-base/           # Consolidated references (~1500 lines)
│   │   ├── README.md             # Navigation guide
│   │   ├── error-catalog.md      # 10+ error categories
│   │   ├── astro-patterns.md     # Components, routing, collections, etc.
│   │   ├── starlight-guide.md    # Starlight-specific docs
│   │   ├── integrations.md       # External data, loaders, TypeScript
│   │   └── content-knowledge/    # Detailed reference materials
│   │       ├── content-collections-reference.md
│   │       ├── content-loader-api.md
│   │       ├── external-data-integration.md
│   │       ├── routing-pages-reference.md
│   │       └── starlight-specific.md
│   ├── hooks/
│   │   └── hooks.json            # Currently empty; reserved for future
│   ├── README.md                 # Detailed plugin documentation
│   ├── CHANGELOG.md              # Version history
│   └── LICENSE                   # CC0 dedication
├── setup.sh                      # Installation & configuration script
├── plugin-usage.md               # Troubleshooting & known issues
├── README.md                     # Marketplace overview & quick start
├── claude.md                     # This file - primary context document
└── .gitignore
```

## Components Overview

### Agents (4 Specialized Coordinators)

| Agent | File | Purpose | Invoked By |
|-------|------|---------|------------|
| **astro-orchestrator** | `agents/astro-orchestrator.md` | Task analysis, agent coordination, rigor calibration | `/develop` command |
| **astro-developer** | `agents/astro-developer.md` | Code implementation with pattern enforcement | Most tasks; primary executor |
| **astro-auditor** | `agents/astro-auditor.md` | 3-priority validation (P1/P2/P3) | All implementations; `/audit` |
| **astro-architect** | `agents/astro-architect.md` | System design, collection architecture | `/architect`, complex tasks |

### Skills (2 Capability Providers)

| Skill | Directory | Purpose | Loading Strategy |
|-------|-----------|---------|------------------|
| **astro-coding** | `skills/astro-coding/` | Patterns, best practices, critical rules | Selective (keyword-based) |
| **astro-knowledge** | `skills/astro-knowledge/` | API docs, references, feature lookup | On-demand + MCP integration |

### Commands (5 User Entry Points)

| Command | File | Function | Best For |
|---------|------|----------|----------|
| `/develop` | `commands/develop.md` | Orchestrated workflow | Most tasks; primary command |
| `/implement` | `commands/implement.md` | Direct implementation | Simple, straightforward changes |
| `/architect` | `commands/architect.md` | Architecture planning only | Complex system design |
| `/audit [level]` | `commands/audit.md` | Code validation | Quality checks (auto/light/medium/comprehensive) |
| `/lookup` | `commands/lookup.md` | API reference | Quick documentation lookup |

### Knowledge Base (5 Consolidated Files)

| File | Lines | Purpose | Key Content |
|------|-------|---------|-------------|
| **error-catalog.md** | ~300 | Error index by symptom | Import errors, hydration, routing, collections, build, TypeScript, config, CSS, MDX, runtime |
| **astro-patterns.md** | ~400 | Implementation patterns | Components, routing (static/dynamic), collections, hydration, config, data fetching, images, TypeScript |
| **starlight-guide.md** | ~300 | Starlight-specific | Setup, page types, frontmatter, sidebars, components, overrides, i18n, styling, search |
| **integrations.md** | ~300 | Advanced patterns | Content loaders, auth, error handling, incremental updates, data transformation, caching, TypeScript |
| **content-knowledge/** | ~200 | Detailed references | In-depth guides for collections, loaders, external data, routing, Starlight |

## Critical Rules (Mandatory for ALL Code)

These 5 rules are enforced by all agents and must NEVER be violated:

1. **File Extensions in Imports**: `import Layout from './Layout.astro'` ✅ (NOT `'./Layout'` ❌)
2. **Module Prefix**: `import { getCollection } from 'astro:content'` ✅ (NOT `'astro/content'` ❌)
3. **CSS Attributes**: `<div class="...">` ✅ (NOT `className` ❌)
4. **Async in Frontmatter**: Awaits only in `---` frontmatter, not templates ✅
5. **Environment Variables**: `SECRET_*` for server-side, `PUBLIC_*` only for client ✅

## Workflow Examples

### Example 1: Simple Task
```bash
/develop Add a Footer component
```

**Flow**:
1. `astro-orchestrator` analyzes: scope = 1 component (~20 lines)
2. Determines: `astro-developer` + light audit
3. `astro-developer` loads component patterns only
4. Implements footer, applies critical rules
5. `astro-auditor` runs 5 quick checks
6. Complete in ~1 minute

### Example 2: Complex Task
```bash
/develop Build multi-language system with GitBook integration
```

**Flow**:
1. `astro-orchestrator` analyzes: multi-source, complex architecture
2. Determines: `astro-architect` → `astro-developer` → comprehensive audit
3. `astro-architect` loads collection + integration patterns
4. Designs system architecture, defines schemas
5. `astro-developer` implements (parallel if beneficial)
6. `astro-auditor` runs 50+ comprehensive checks
7. Complete in ~15 minutes

### Example 3: Direct Implementation
```bash
/implement Create a Card component with image and description
```

**Flow**:
1. Bypasses orchestration
2. `astro-developer` invoked directly
3. Loads component patterns
4. Implements Card.astro
5. Applies critical rules
6. Complete in ~30 seconds

## Adaptive Audit Rigor

| Level | Checks | Duration | Use Case |
|-------|--------|----------|----------|
| **Light** | 5 | ~30 sec | <20 lines, 1 file, low-risk changes |
| **Medium** | 20 | ~2 min | Standard features, typical development |
| **Comprehensive** | 50+ | ~5 min | Critical areas, large scope, security-sensitive |
| **Auto** | Variable | Variable | Orchestrator determines appropriate level |

**Validation Priorities**:
- **P1 (Breaking)**: Build failures, syntax errors, import issues - MUST fix
- **P2 (Security/Performance)**: Security holes, performance problems, bugs - SHOULD fix
- **P3 (Best Practices)**: Style issues, minor optimizations - NICE to fix

## Technology Stack

### Core Technologies
- **Claude Code** (latest) - AI-powered code editor/assistant
- **Astro v4.x+** - Static site builder and modern web framework
- **Starlight v0.21.x+** - Astro-based documentation framework
- **TypeScript** - Type-safe development
- **Markdown** - All documentation and skill definitions
- **Bash/Shell** - Setup and automation

### Plugin Infrastructure
- **Claude Code Plugin System** - Extensible architecture
- **Skill-based Design** - Modular capability providers
- **Agent-based Workflows** - Specialized task coordinators
- **Hook System** - PreToolUse/PostToolUse for automation (reserved)
- **MCP Integration** - Model Context Protocol for real-time docs

### External Integrations
- **MCP Server**: `astro-docs` (HTTPS at mcp.docs.astro.build/mcp)
- Optional: GitBook, PostgreSQL, other CMSs (documented in integrations.md)

## Configuration Files

### 1. Plugin Manifest (`astro-dev/.claude-plugin/plugin.json`)
Defines plugin metadata, agents, commands, skills, and hooks. Current version: 2.0.0

### 2. Marketplace Manifest (`.claude-plugin/marketplace.json`)
Registers plugins in the marketplace. Source type: `directory`, points to `./astro-dev`

### 3. MCP Configuration (`astro-dev/.mcp.json`)
Connects to astro-docs MCP server for real-time API documentation

### 4. Hooks Configuration (`astro-dev/hooks/hooks.json`)
Currently empty; reserved for automated workflows (PostToolUse, PreToolUse)

### 5. Setup Script (`setup.sh`)
- Auto-detects marketplace location (project-local vs global)
- Configures Claude Code settings with backups
- Uses `jq` for JSON updates (manual fallback available)
- Displays v2.0 quick start guide

## Installation & Setup

### Quick Installation
```bash
# 1. Clone to .claude directory
git clone <repository-url> .claude/sb-marketplace

# 2. Run setup script
cd .claude/sb-marketplace
bash setup.sh

# 3. Restart Claude Code

# 4. Commands are now available!
/develop Your task here
```

### Manual Configuration (if setup.sh fails)

Add to `.claude/settings.json`:
```json
{
  "extraKnownMarketplaces": {
    "sb-marketplace": {
      "source": {
        "source": "directory",
        "path": "./.claude/sb-marketplace"
      }
    }
  },
  "enabledPlugins": {
    "astro-dev@sb-marketplace": true
  }
}
```

## Git Status

**Current Branch**: `main`
**Status**: Clean (no uncommitted changes)
**Recent Commits**:
- `599851a`: Fix marketplace source type from 'local' to 'directory'
- `0955540`: Fix plugin version inconsistencies and document usage issues
- `553af3a`: Update setup.sh to reflect v2.0 architecture
- `02c6b7e`: Add claude.md snippet to READMEs
- `0f65f4b`: Add .claude/ to .gitignore

## Version History

### v2.0.0 (Current - 2025-10-18)
**Major Release**: Orchestration architecture

**New Features**:
- Orchestration-based workflows (`astro-orchestrator` agent)
- `/develop` command for intelligent task planning
- `/architect` command for system design
- Adaptive audit levels (light/medium/comprehensive)
- Knowledge base consolidation (17 files → 5 files)
- 50% token reduction through selective loading
- Parallel agent execution when beneficial

**Breaking Changes**:
- `/docs-lookup` renamed to `/lookup`
- `astro-developer` skill → `astro-coding`
- `astro-docs` skill → `astro-knowledge`
- Auto-audit hooks removed

**Improvements**:
- Token usage optimized by ~50%
- Progressive disclosure pattern implemented
- Task complexity analysis algorithm
- Rigor calibration system
- 4 agents (was 2 in v1.0)

### v1.0.0 (Previous)
- Initial release
- Basic agent system
- Direct command invocation
- 17 knowledge base files
- Fixed audit levels

## Known Issues & Troubleshooting

See `plugin-usage.md` for documented issues:
- Marketplace plugin command loading edge cases
- Version inconsistencies (resolved in recent commits)
- Setup script compatibility notes

## File Statistics

- **Total Documentation Lines**: ~6,138 across all .md files
- **Knowledge Base**: ~1,500 lines (consolidated from ~3,000)
- **Token Reduction**: ~50% through consolidation + selective loading
- **Agent Count**: 4 (orchestrator, developer, auditor, architect)
- **Command Count**: 5 (develop, implement, architect, audit, lookup)
- **Skill Count**: 2 (astro-coding, astro-knowledge)
- **Critical Rules**: 5 (enforced in all code)

## Best Practices for Using This Marketplace

### When to Use Each Command

1. **Use `/develop`** (90% of tasks):
   - Any task requiring analysis or planning
   - Multi-step implementations
   - When unsure of complexity
   - Default choice for most work

2. **Use `/implement`** (for simple tasks):
   - Single component creation
   - Straightforward changes
   - <20 lines of code
   - No architecture needed

3. **Use `/architect`** (planning phase):
   - Before starting complex features
   - Multi-source content systems
   - Collection architecture design
   - Integration planning

4. **Use `/audit`** (quality checks):
   - After manual code changes
   - Before committing critical code
   - When debugging issues
   - Periodic codebase reviews

5. **Use `/lookup`** (quick reference):
   - Syntax verification
   - API parameter lookup
   - Quick examples
   - Feature availability check

### Token Optimization Tips

1. **Trust the orchestrator**: `/develop` automatically optimizes loading
2. **Use specific keywords**: Helps selective pattern loading
3. **Start with `/architect`** for complex tasks: Prevents re-planning
4. **Choose appropriate audit level**: Don't over-validate simple changes
5. **Use `/lookup`** for docs**: Lighter than loading full knowledge base

## Contributing

### Adding Knowledge
- Update consolidated files in `astro-dev/knowledge-base/`
- Add error patterns to `error-catalog.md` (indexed by symptom)
- Document new Astro features in `astro-patterns.md`
- Update version info in this claude.md file

### Improving Skills
- Enhance patterns in `skills/astro-coding/references/`
- Add API references to `astro-knowledge/references/`
- Update critical rules if needed (coordinate with agents)

### Extending Agents
- Improve agent capabilities in `agents/*.md`
- Refine orchestration logic in `astro-orchestrator.md`
- Add specialized agents (update plugin.json)

### Updating Configuration
- Plugin manifest: `astro-dev/.claude-plugin/plugin.json`
- Marketplace manifest: `.claude-plugin/marketplace.json`
- Version bumps require updates in both + CHANGELOG.md

## Support & Contact

- **Issues**: Create an issue in this repository
- **Email**: rathermercurial@protonmail.com
- **Community**: SuperBenefit (info@superbenefit.org)

## License

CC0 1.0 Universal - Public Domain Dedication

This work is dedicated to the public domain. You can copy, modify, distribute and perform the work, even for commercial purposes, all without asking permission.

---

## Quick Reference Card

**Primary Command**: `/develop [task description]`
**Direct Implementation**: `/implement [simple task]`
**Planning Only**: `/architect [design request]`
**Validation**: `/audit [auto|light|medium|comprehensive] [path]`
**Quick Docs**: `/lookup [api name]`

**Critical Rules**: Extensions in imports, `astro:` prefix, `class` not `className`, async in frontmatter, `SECRET_*` vs `PUBLIC_*`

**File Paths**:
- Plugin: `F:/projects/sb-marketplace/astro-dev/`
- Knowledge Base: `F:/projects/sb-marketplace/astro-dev/knowledge-base/`
- Agents: `F:/projects/sb-marketplace/astro-dev/agents/`
- Commands: `F:/projects/sb-marketplace/astro-dev/commands/`

**Version**: 2.0.0 | **Status**: Stable | **Updated**: 2025-10-18
