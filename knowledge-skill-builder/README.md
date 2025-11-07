# Knowledge Skill Builder

**Transform markdown knowledge repositories into Claude skills**

Build Claude skills from your markdown documentation, knowledge gardens, and framework repositories with guided analysis, generation, and packaging tools.

## Overview

The Knowledge Skill Builder helps you create professional Claude skills from existing markdown content without needing deep understanding of skill architecture. It provides:

- **Repository Analysis**: Understand your knowledge base structure and get recommendations
- **Skill Generation**: Create properly-structured skills from templates
- **Automated Validation**: Ensure skills meet official Anthropic requirements
- **Professional Packaging**: Create distributable ZIP archives for marketplace publication

## What You Can Build

### Knowledge Retrieval Skills
Search and cite from markdown knowledge bases
- Documentation sites
- Research note collections
- Knowledge gardens
- Technical wikis

### Framework Guidance Skills
Interactive help with templates and worksheets
- Business model canvases
- Strategic planning frameworks
- Assessment tools
- Organizational worksheets

### Translation Skills
Multilingual content transformation
- Preserve markdown structure
- Handle YAML frontmatter
- Maintain cross-references
- Support multilingual knowledge bases

## Quick Start

### 1. Analyze Your Knowledge Repository

```bash
python skills/knowledge-skill-builder/scripts/analyze_knowledge_repo.py /path/to/knowledge/base
```

This generates a report with:
- Content structure overview
- Topic clustering
- Linking patterns
- Token estimates
- Recommended skill type and configuration

### 2. Initialize New Skill

```bash
python skills/knowledge-skill-builder/scripts/init_knowledge_skill.py my-skill-name --type knowledge-retrieval
```

Template types:
- `knowledge-retrieval` - Search and lookup skills (default)
- `framework-guidance` - Interactive worksheet/template skills
- `translation` - Multilingual content skills
- `generic` - Blank template for custom needs

### 3. Customize SKILL.md

Edit the generated `SKILL.md` file:
- Replace `[TODO]` placeholders
- Add domain-specific capabilities
- Include real usage examples
- Configure loading triggers

### 4. Organize Resources

```
my-skill/
├── SKILL.md                 # Main skill definition
├── scripts/                 # Optional automation
├── references/              # Docs loaded as needed
│   ├── quick-reference.md
│   └── detailed-guide.md
└── assets/                  # Templates, not loaded
    └── templates/
```

### 5. Validate

```bash
python skills/knowledge-skill-builder/scripts/validate_skill.py ./my-skill
```

Checks:
- YAML frontmatter validity
- Name/description requirements
- Directory structure
- Referenced files exist
- Token budgets documented

### 6. Package for Distribution

```bash
python skills/knowledge-skill-builder/scripts/package_skill.py ./my-skill
```

Creates `my-skill.zip` ready for installation via Claude Code.

## Features

### Repository Analysis

Understand your knowledge base before building:
- File structure and organization
- Frontmatter schema detection
- Linking patterns (wikilinks, tags, backlinks)
- Topic clustering
- Token usage estimates
- Skill configuration recommendations

### Multiple Templates

Choose the right template for your use case:
- **Knowledge Retrieval**: Pre-configured for search/lookup with citation
- **Framework Guidance**: Interactive completion with templates and examples
- **Translation**: Markdown-aware multilingual transformation
- **Generic**: Blank slate for custom skills

### Automated Validation

Ensure quality before packaging:
- YAML frontmatter structure
- Field requirements (name, description)
- Character limits (name ≤64, description ≤1024)
- Directory structure conventions
- Reference integrity
- Writing style (imperative form check)

### Professional Packaging

Create distributable archives:
- ZIP with proper structure
- Validation before packaging
- Size reporting
- Installation instructions

## Scripts Reference

### analyze_knowledge_repo.py

Scan markdown repository and generate recommendations.

**Usage:**
```bash
python analyze_knowledge_repo.py <repo-path> [--output <report.md>]
```

**Output:**
- Content structure analysis
- Topic identification
- Linking patterns
- Token estimates
- Recommended skill type
- Suggested configuration

### init_knowledge_skill.py

Create new skill from template.

**Usage:**
```bash
python init_knowledge_skill.py <skill-name> [--type <template>] [--path <output-dir>]
```

**Templates:**
- `knowledge-retrieval` (default)
- `framework-guidance`
- `translation`
- `generic`

**Output:**
- Complete skill directory structure
- SKILL.md from template
- Example reference files
- scripts/, references/, assets/ directories

### validate_skill.py

Check skill meets official requirements.

**Usage:**
```bash
python validate_skill.py <skill-path>
```

**Checks:**
- SKILL.md exists with valid YAML
- name: lowercase-hyphen, max 64 chars
- description: max 1024 chars
- Directory structure
- Referenced files exist
- Token budgets documented

**Exit codes:**
- 0: Valid (no errors)
- 1: Invalid (has errors)

### package_skill.py

Create distributable ZIP archive.

**Usage:**
```bash
python package_skill.py <skill-path> [--output <output-dir>]
```

**Process:**
1. Runs validation checks
2. Creates ZIP archive
3. Preserves directory structure
4. Reports size
5. Provides installation instructions

## Examples

### Example 1: DAO Knowledge Skill

```bash
# Analyze DAO documentation
python scripts/analyze_knowledge_repo.py ~/docs/dao-knowledge

# Create skill
python scripts/init_knowledge_skill.py dao-knowledge --type knowledge-retrieval

# Edit SKILL.md, add references

# Validate
python scripts/validate_skill.py dao-knowledge

# Package
python scripts/package_skill.py dao-knowledge
```

Result: Skill that searches DAO governance documentation with wikilink navigation and source citations.

### Example 2: Social Lean Canvas Skill

```bash
# Create framework guidance skill
python scripts/init_knowledge_skill.py social-lean-canvas --type framework-guidance

# Add to assets/templates/:
# - blank-canvas.md
# - annotated-canvas.md

# Add to references/:
# - canvas-guide.md
# - examples.md

# Validate and package
python scripts/validate_skill.py social-lean-canvas
python scripts/package_skill.py social-lean-canvas
```

Result: Skill that guides users through completing Social Lean Canvas interactively.

## Documentation

### References

The skill includes comprehensive reference documentation:

- **skill-structure.md** - Complete guide to skill anatomy following Anthropic patterns
- **loading-strategies.md** - When and how skills are loaded
- **token-optimization.md** - Best practices for efficient skills
- **knowledge-skill-patterns.md** - Common patterns with real examples

### Learning Path

1. Read `references/skill-structure.md` to understand skill anatomy
2. Run `analyze_knowledge_repo.py` on your knowledge base
3. Review analysis report recommendations
4. Initialize skill with appropriate template
5. Read `references/loading-strategies.md` for trigger configuration
6. Consult `references/knowledge-skill-patterns.md` for your skill type
7. Apply `references/token-optimization.md` for efficiency
8. Validate and iterate
9. Package when ready

## Installation

### As Plugin

Add to your Claude Code marketplace:

```bash
# Add sb-marketplace
claude plugin marketplace add superbenefit/sb-marketplace

# Install plugin
claude plugin install knowledge-skill-builder@sb-marketplace
```

### Direct Use

Clone and use scripts directly:

```bash
git clone https://github.com/superbenefit/sb-marketplace.git
cd sb-marketplace/knowledge-skill-builder
python skills/knowledge-skill-builder/scripts/init_knowledge_skill.py my-skill
```

## Requirements

- Python 3.7+
- PyYAML (for frontmatter parsing)

Install dependencies:
```bash
pip install pyyaml
```

## Token Optimization

The knowledge-skill-builder follows its own best practices:

**Skill Metadata**: ~100 tokens (name + description)
**SKILL.md Body**: ~2500-3000 tokens (core capabilities and patterns)
**References**: ~500-3000 tokens each (loaded as needed)
**Assets**: 0 tokens (templates not loaded to context)

Typical usage: ~3000-5000 tokens for complete skill creation workflow

## Best Practices

1. ✅ Start with repository analysis to understand your content
2. ✅ Choose the most appropriate template for your use case
3. ✅ Keep SKILL.md under 3500 words
4. ✅ Move detailed content to references/
5. ✅ Put templates and outputs in assets/
6. ✅ Validate before packaging
7. ✅ Document token budgets
8. ✅ Include concrete usage examples
9. ✅ Use imperative form (not second-person)
10. ✅ Test with real scenarios before publishing

## Contributing

Contributions welcome! Please:

1. Follow official Anthropic skill patterns
2. Validate all changes
3. Update documentation
4. Include examples
5. Test with real knowledge repositories

## License

CC0 - Public Domain

## Support

- Issues: https://github.com/superbenefit/sb-marketplace/issues
- Community: https://superbenefit.org

## Version

**Version**: 1.0.0
**Last Updated**: 2025-11-07
**Compatible With**: Claude Code plugin system, Anthropic skill standards

## Acknowledgments

Built following official Anthropic skill-creator patterns and validated against Claude Code plugin documentation.
