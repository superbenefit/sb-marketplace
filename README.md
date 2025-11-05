# Astro Dev Marketplace

Claude Code plugin marketplace for Astro and Starlight development - hosted on GitHub for easy installation.

> **For Claude Code**: See [`claude.md`](./claude.md) for comprehensive repository context, architecture details, and quick reference. This file provides complete codebase understanding to reduce startup time and token usage.

## Overview

This repository is a plugin marketplace for Claude Code, featuring the **astro-dev v0.3** plugin - a comprehensive toolkit for Astro and Starlight development with intelligent orchestration, specialized agents, and extensive knowledge base.

## Quick Start

### Installation

**For global installation** (all projects), edit `~/.claude/settings.json`:

**For single project**, edit `<project>/.claude/settings.local.json`:

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
    "astro-dev@sb-marketplace": true
  }
}
```

Then restart Claude Code. The plugin will be automatically downloaded and enabled.

## What's Included

### Astro Dev Plugin (v0.3.1)

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
- Astro v4.x or later (for target projects)
- Starlight v0.21.x or later (for Starlight projects)

## Migration from v0.2.0

### Breaking Changes in v0.3.0
- **Installation method changed**: Now uses GitHub source instead of directory
- `setup.sh` removed - no longer needed with GitHub loading
- Must update settings.json to use GitHub source

### Migration Steps
If you're upgrading from v0.2.0, update your `.claude/settings.json`:

**Old (v0.2.0)**:
```json
{
  "extraKnownMarketplaces": {
    "sb-marketplace": {
      "source": {
        "source": "directory",
        "path": "./.claude/sb-marketplace"
      }
    }
  }
}
```

**New (v0.3.0)**:
```json
{
  "extraKnownMarketplaces": {
    "sb-marketplace": {
      "source": {
        "source": "github",
        "repo": "superbenefit/sb-marketplace"
      }
    }
  }
}
```

Then restart Claude Code. The plugin functionality remains unchanged.

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

## Documentation

### For Users
- **[README.md](./README.md)** (this file) - Quick start and usage guide
- **[astro-dev/README.md](./astro-dev/README.md)** - Detailed plugin documentation

### For Claude Code
- **[claude.md](./claude.md)** - Comprehensive repository context (recommended for AI assistants)

### For Developers
- **[ARCHITECTURE_SPEC.md](./ARCHITECTURE_SPEC.md)** - Complete v2.0 system design
- **[IMPLEMENTATION_STATUS.md](./IMPLEMENTATION_STATUS.md)** - Implementation progress
- **[KNOWLEDGE_BASE_CONSOLIDATION.md](./KNOWLEDGE_BASE_CONSOLIDATION.md)** - KB optimization details

## License

CC0 1.0 Universal - Public Domain Dedication

See LICENSE file for details.

## Support

For issues, questions, or contributions:
- Create an issue in this repository
- Contact: rathermercurial@protonmail.com
- SuperBenefit Community: info@superbenefit.org

## Credits

Created by rathermercurial.eth for the SuperBenefit community.

**Version**: 0.3.1
**Last Updated**: 2025-10-20
**Repository**: https://github.com/superbenefit/sb-marketplace
