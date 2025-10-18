# Astro Dev Marketplace

Local Claude Code plugin marketplace for Astro and Starlight development tools.

## Overview

This repository contains a complete plugin marketplace for Claude Code, featuring the **astro-dev** plugin - a comprehensive toolkit for Astro and Starlight development.

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

### Astro Dev Plugin (v1.0.0)

A complete toolkit for Astro and Starlight development featuring:

#### 🎯 Skills
- **astro-developer**: Expert implementation skill for components, routes, and configs
- **astro-docs**: Documentation specialist for API verification

#### 🤖 Agents
- **astro-auditor**: Comprehensive code auditor with 3-priority system
- **astro-architect**: Content architecture specialist for complex planning

#### ⚡ Commands
- `/implement` - Start implementation with best practices loaded
- `/audit` - Trigger comprehensive code audit
- `/docs-lookup` - Quick API documentation lookup

#### 🔗 Hooks
- Auto-audit after file edits
- Pre-implementation notifications

> **⚠️ Security Notice**: Hooks execute automatically when you edit Astro/TypeScript files. The audit-runner.sh script will run in the background after Write/Edit operations to check for common mistakes and provide immediate feedback. All hooks are non-blocking with a 30-second timeout.

#### 📚 Knowledge Base
- Astro syntax references
- Common mistakes catalog
- Best practices
- Architecture patterns
- Loader examples
- Integration guides

## Usage

### Implementing a Feature

```bash
/implement Add a blog post listing page with pagination
```

This will:
1. Load the astro-developer skill
2. Review project structure
3. Check best practices
4. Implement the feature
5. Auto-audit the code

### Running an Audit

```bash
/audit src/pages/blog/[slug].astro
```

Get a prioritized report with:
- ❌ Build-breaking issues
- ⚠️ Security and performance concerns
- 💡 Best practice suggestions

### Looking Up Documentation

```bash
/docs-lookup getStaticPaths
```

Returns current syntax, examples, and documentation links.

### Complex Architecture

For complex content architecture planning:
```
Can you help design a multi-source content system with GitBook integration?
```

The astro-architect agent will provide:
- System design
- Schema definitions
- Loader architecture
- Implementation roadmap

## Plugin Structure

```
.claude/sb-marketplace/
├── .claude-plugin/
│   └── marketplace.json          # Marketplace manifest
├── astro-dev/                     # Astro Dev Plugin
│   ├── .claude-plugin/
│   │   └── plugin.json            # Plugin manifest
│   ├── skills/                    # Skills
│   │   ├── astro-developer/
│   │   └── astro-docs/
│   ├── agents/                    # Sub-agents
│   │   ├── astro-auditor.md
│   │   └── astro-architect.md
│   ├── commands/                  # Slash commands
│   │   ├── implement.md
│   │   ├── audit.md
│   │   └── docs-lookup.md
│   ├── hooks/                     # Automation hooks
│   │   └── hooks.json
│   ├── scripts/                   # Utility scripts
│   │   └── audit-runner.sh
│   ├── knowledge-base/            # Reference material
│   │   ├── astro-syntax/
│   │   ├── common-mistakes/
│   │   ├── best-practices/
│   │   └── ...
│   ├── LICENSE                    # CC0 License
│   ├── CHANGELOG.md              # Version history
│   └── README.md                 # Plugin docs
├── references/                    # Source reference files
└── setup.sh                       # Installation script
```

## Features

### Context Efficiency
- **Progressive Loading**: Only loads what's needed
- **Skill Metadata**: ~100 tokens for discovery
- **On-Demand Resources**: No context penalty for unused files

### Workflow Automation
- **Auto-Audit**: Quality checks after file edits
- **Smart Skills**: Auto-triggered based on context
- **Parallel Processing**: Agents work independently

### Developer Experience
- **Quick Commands**: Fast access to common operations
- **Comprehensive Knowledge**: Deep Astro/Starlight expertise
- **Error Prevention**: Catches mistakes before they cause issues

## Requirements

- Claude Code (latest version)
- Git (for installation)
- Bash (for setup script)
- Astro v4.x or later (for target projects)
- Starlight v0.21.x or later (for Starlight projects)

## Contributing

This plugin is maintained by the SuperBenefit community. Contributions are welcome!

### Adding Knowledge
- Update files in `astro-dev/knowledge-base/`
- Document common mistakes as discovered
- Add new patterns and examples

### Improving Skills
- Enhance skill prompts in `skills/*/SKILL.md`
- Add reference materials
- Update quick reference guides

### Extending Agents
- Improve agent capabilities in `agents/*.md`
- Add new specialized agents
- Enhance audit checklists

## Future Enhancements

### Planned Features
- Additional skills for testing and performance
- ✅ MCP server for real-time documentation (implemented in `.mcp.json`)
- Advanced hooks for pre-commit validation
- Team collaboration features

See [astro-dev/CHANGELOG.md](astro-dev/CHANGELOG.md) for version history and roadmap.

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

Built with the Claude Code plugin architecture for optimal context efficiency and developer experience.
