# knowledge-skill-builder

Transform markdown knowledge repositories into Claude skills with guided analysis, generation, and packaging tools.

Part of the [SuperBenefit Plugin Marketplace](https://github.com/superbenefit/sb-marketplace).

**Version**: 1.0.0

## Overview

The knowledge-skill-builder helps create professional Claude skills from existing markdown content. It provides repository analysis, template-based skill generation, automated validation, and packaging for distribution.

## What You Can Build

- **Knowledge Retrieval Skills**: Search and cite from markdown knowledge bases (docs, wikis, research notes)
- **Framework Guidance Skills**: Interactive help with templates and worksheets (canvases, assessments, planning tools)
- **Translation Skills**: Multilingual content transformation with frontmatter and cross-reference handling

## Quick Start

### 1. Analyze Your Repository

```bash
python skills/knowledge-skill-builder/scripts/analyze_knowledge_repo.py /path/to/knowledge/base
```

Generates a report with content structure, topic clustering, token estimates, and recommended skill configuration.

### 2. Initialize New Skill

```bash
python skills/knowledge-skill-builder/scripts/init_knowledge_skill.py my-skill-name --type knowledge-retrieval
```

Template types: `knowledge-retrieval` (default), `framework-guidance`, `translation`, `generic`

### 3. Customize SKILL.md

Edit the generated `SKILL.md` file - replace `[TODO]` placeholders, add domain-specific capabilities, include usage examples, and configure loading triggers.

### 4. Validate

```bash
python skills/knowledge-skill-builder/scripts/validate_skill.py ./my-skill
```

Checks YAML frontmatter, name/description requirements, directory structure, referenced files, and token budgets.

### 5. Package

```bash
python skills/knowledge-skill-builder/scripts/package_skill.py ./my-skill
```

Creates a distributable ZIP archive ready for installation.

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `analyze_knowledge_repo.py` | Scan markdown repository and generate recommendations |
| `init_knowledge_skill.py` | Create new skill from template |
| `validate_skill.py` | Check skill meets requirements |
| `package_skill.py` | Create distributable ZIP archive |

## Skill References

The plugin includes reference documentation for building skills:

- **skill-structure.md** - Complete guide to skill anatomy
- **loading-strategies.md** - When and how skills are loaded
- **token-optimization.md** - Best practices for efficient skills
- **knowledge-skill-patterns.md** - Common patterns with examples

## Installation

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
    "knowledge-skill-builder@sb-marketplace": true
  }
}
```

Restart Claude Code to load the plugin.

## Requirements

- Python 3.7+
- PyYAML (`pip install pyyaml`)

## File Organization

```
knowledge-skill-builder/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── knowledge-skill-builder/
│       ├── SKILL.md
│       ├── scripts/
│       ├── references/
│       └── assets/templates/
├── CHANGELOG.md
└── LICENSE
```

## Support

- **Issues**: [GitHub Issues](https://github.com/superbenefit/sb-marketplace/issues)
- **Email**: rathermercurial@protonmail.com
- **Community**: [SuperBenefit](https://superbenefit.org)

## License

CC0 1.0 Universal - Public Domain Dedication

Created for the SuperBenefit community.
