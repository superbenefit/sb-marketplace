# Astro Dev Marketplace

Local Claude Code plugin marketplace for Astro and Starlight development tools.

## Overview

This repository contains a complete plugin marketplace for Claude Code, featuring the **astro-dev v2.0** plugin - an intelligent, orchestrator-based toolkit for Astro and Starlight development.

## Quick Start

### Installation

1. **Clone this repository** (or add as submodule to your project):
   ```bash
   git clone <repository-url> .claude/sb-marketplace
   ```

2. **Run the setup script**:
   ```bash
   cd .claude/sb-marketplace
   bash setup.sh
   ```

3. **Enable the plugin** in your project's `.claude/settings.json`:
   ```json
   {
     "extraKnownMarketplaces": {
       "sb-marketplace": {
         "source": {
           "source": "local",
           "path": "./.claude/sb-marketplace"
         }
       }
     },
     "enabledPlugins": {
       "astro-dev@sb-marketplace": true
     }
   }
   ```

4. **Start using** the plugin in Claude Code!

## What's Included

### Astro Dev Plugin (v2.0.0)

An intelligent, orchestrator-based toolkit for Astro and Starlight development with adaptive workflows and 50% token reduction.

#### 🤖 Agents
- **astro-orchestrator**: Intelligent task coordinator with adaptive planning
- **astro-developer**: Primary code implementation specialist
- **astro-auditor**: Adaptive validator with 3 rigor levels (light/medium/comprehensive)
- **astro-architect**: Content architecture specialist for complex system design

#### 🎯 Skills
- **astro-coding**: Smart context provider with selective pattern loading
- **astro-knowledge**: On-demand API documentation and reference lookup

#### ⚡ Commands
- `/develop` - Intelligent orchestrated workflow (primary command)
- `/implement` - Direct implementation (bypass orchestration)
- `/architect` - Architecture planning
- `/audit [level]` - Adaptive validation (light/medium/comprehensive/auto)
- `/lookup` - Quick API reference

#### 📚 Knowledge Base (50% optimized)
- Error catalog (indexed by symptom)
- Astro patterns (components, routing, collections)
- Starlight guide (complete documentation)
- Integrations (loaders, TypeScript, external data)
- Quick navigation and cross-references

## Usage

### Primary Workflow (Recommended)

```bash
/develop Add a blog with categories and pagination
```

The orchestrator will:
1. Analyze your request
2. Determine needed agents (architect → developer → auditor)
3. Load only relevant patterns
4. Coordinate implementation
5. Validate with appropriate rigor

**Benefits**: Intelligent automation, optimal token usage, adaptive validation.

### Direct Implementation

```bash
/implement Create a Card component
```

Bypasses orchestration for straightforward coding tasks.

### Architecture Planning

```bash
/architect Design a multi-language docs system with versioning
```

Get system design, schemas, and implementation roadmap without coding.

### Adaptive Validation

```bash
/audit auto src/pages/           # Auto-determines level
/audit light src/components/Button.astro    # Quick check
/audit comprehensive src/lib/auth.ts         # Full validation
```

Choose rigor based on task complexity, or let the auditor decide.

### API Reference

```bash
/lookup getStaticPaths
/lookup client directives
```

Fast documentation lookup with current syntax and examples.

## Features

### v2.0 Architecture

**Intelligent Orchestration**:
- Task analysis and execution planning
- Agent coordination with parallel execution
- Adaptive audit rigor determination
- Token optimization through smart loading

**Clear Separation**:
- Agents perform actions (orchestrate, implement, audit, design)
- Skills provide capabilities (coding patterns, documentation)

**Token Efficiency**:
- 93% reduction for simple tasks (11,500 → 800 tokens)
- 89% reduction for medium tasks (11,500 → 1,200 tokens)
- 80% reduction for complex tasks (11,500 → 2,250 tokens)

**Adaptive Quality**:
- Light audit (5 checks, ~30 seconds) for small changes
- Medium audit (20 checks, ~2 minutes) for standard work
- Comprehensive audit (50+ checks, ~5 minutes) for critical areas

### Developer Experience
- **Single Entry Point**: `/develop` handles everything intelligently
- **Discoverable Features**: All agents accessible via commands
- **Error Prevention**: Catches mistakes before they cause issues
- **Comprehensive Knowledge**: Deep Astro/Starlight expertise

## Requirements

- Claude Code (latest version)
- Git (for installation)
- Bash (for setup script)
- Astro v4.x or later (for target projects)
- Starlight v0.21.x or later (for Starlight projects)

## Migration from v1.0

### Breaking Changes
- `/docs-lookup` renamed to `/lookup`
- `astro-developer` skill renamed to `astro-coding`
- `astro-docs` skill renamed to `astro-knowledge`
- Auto-audit hooks removed (use orchestrator instead)

### New Features
- `/develop` command for orchestrated workflows
- `/architect` command for design planning
- Adaptive audit levels (light/medium/comprehensive/auto)
- 50% token reduction through knowledge base consolidation

### Backward Compatibility
- `/implement` and `/audit` commands still work (updated)
- Knowledge base content preserved (reorganized)
- All patterns and references maintained

## Contributing

This plugin is maintained by the SuperBenefit community. Contributions are welcome!

### Adding Knowledge
- Update consolidated files in `astro-dev/knowledge-base/`
- Error catalog for new common mistakes
- Astro patterns for new features

### Improving Skills
- Enhance `astro-coding` patterns in `skills/astro-coding/`
- Add API references to `astro-knowledge`

### Extending Agents
- Improve agent capabilities in `agents/*.md`
- Enhance orchestration logic
- Add specialized agents for new domains

## Architecture

See [ARCHITECTURE_SPEC.md](ARCHITECTURE_SPEC.md) for complete v2.0 specification.

Key documents:
- `ARCHITECTURE_SPEC.md` - Complete system design
- `IMPLEMENTATION_STATUS.md` - Implementation progress
- `KNOWLEDGE_BASE_CONSOLIDATION.md` - KB optimization details

## License

CC0 1.0 Universal - Public Domain Dedication

See LICENSE file for details.

## Support

For issues, questions, or contributions:
- Create an issue in this repository
- Contact: rathermercurial@protonmail.com
- SuperBenefit Community: info@superbenefit.org

## Credits

Created by rathremercurial.eth for the SuperBenefit community.

Built with Claude Code plugin architecture v2.0 for intelligent orchestration and optimal efficiency.

**Version**: 2.0.0  
**Last Updated**: 2025-10-18
