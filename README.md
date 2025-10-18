# Astro Dev Marketplace

Local Claude Code plugin marketplace for Astro and Starlight development tools.

## Overview

This repository contains a plugin marketplace for Claude Code, featuring the **astro-dev v2.0** plugin - a toolkit for Astro and Starlight development.

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

A toolkit for Astro and Starlight development with orchestrator-based workflows.

#### 🤖 Agents
- **astro-orchestrator**: Coordinates tasks and manages agent workflows
- **astro-developer**: Handles code implementation
- **astro-auditor**: Validates code with configurable rigor levels
- **astro-architect**: Plans content architecture and system design

#### 🎯 Skills
- **astro-coding**: Provides coding patterns and best practices
- **astro-knowledge**: API documentation and reference lookup

#### ⚡ Commands
- `/develop` - Orchestrated workflow
- `/implement` - Direct implementation
- `/architect` - Architecture planning
- `/audit [level]` - Code validation (light/medium/comprehensive/auto)
- `/lookup` - API reference

#### 📚 Knowledge Base
- Error catalog (indexed by symptom)
- Astro patterns (components, routing, collections)
- Starlight guide
- Integrations (loaders, TypeScript, external data)

## Usage

### Primary Workflow

```bash
/develop Add a blog with categories and pagination
```

The orchestrator analyzes your request, determines which agents to use, loads relevant patterns, and coordinates implementation.

### Direct Implementation

```bash
/implement Create a Card component
```

Bypasses orchestration for straightforward tasks.

### Architecture Planning

```bash
/architect Design a multi-language docs system with versioning
```

Get system design and schemas without immediate implementation.

### Code Validation

```bash
/audit auto src/pages/           # Determines appropriate level
/audit light src/components/Button.astro    # Quick check
/audit comprehensive src/lib/auth.ts         # Thorough validation
```

Choose validation rigor based on task complexity.

### API Reference

```bash
/lookup getStaticPaths
/lookup client directives
```

Quick documentation lookup with syntax and examples.

## Features

### v2.0 Architecture

**Orchestration**:
- Task analysis and execution planning
- Agent coordination with parallel execution
- Configurable validation rigor
- Selective context loading

**Organization**:
- Agents handle tasks
- Skills provide context and patterns
- Commands offer direct access

**Efficiency**:
- Reduced token usage for most tasks
- Consolidated knowledge base
- Selective pattern loading

**Validation**:
- Light (5 checks, ~30 seconds) for small changes
- Medium (20 checks, ~2 minutes) for standard work
- Comprehensive (50+ checks, ~5 minutes) for critical areas

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
- Auto-audit hooks removed

### New Features
- `/develop` command for orchestrated workflows
- `/architect` command for planning
- Configurable audit levels
- Consolidated knowledge base

### Backward Compatibility
- `/implement` and `/audit` commands still work
- Knowledge base content preserved
- All patterns and references maintained

## Contributing

This plugin is maintained by the SuperBenefit community. Contributions are welcome!

### Adding Knowledge
- Update consolidated files in `astro-dev/knowledge-base/`
- Add error patterns to error catalog
- Document new Astro features in patterns

### Improving Skills
- Enhance patterns in `skills/astro-coding/`
- Add API references to `astro-knowledge`

### Extending Agents
- Improve agent capabilities in `agents/*.md`
- Refine orchestration logic
- Add specialized agents

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

**Version**: 2.0.0  
**Last Updated**: 2025-10-18
