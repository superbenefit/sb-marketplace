# Skill Templates

This directory contains templates used by `init_knowledge_skill.py` to create new skills.

## Available Templates

### SKILL-template.md
Generic template suitable for any skill type. Use when creating custom skills that don't fit other categories.

### knowledge-retrieval-template.md
Pre-configured template for skills that search and retrieve knowledge from repositories. Use for documentation skills, knowledge gardens, or research note collections.

### framework-guidance-template.md
Pre-configured template for skills that help users complete structured frameworks or worksheets. Use for business canvases, assessment tools, or planning frameworks.

### translation-template.md
Pre-configured template for skills that translate markdown content across languages. Use for multilingual documentation or knowledge bases.

## Usage

Templates are embedded in `scripts/init_knowledge_skill.py` and automatically used when creating new skills:

```bash
# Use default (knowledge-retrieval) template
python scripts/init_knowledge_skill.py my-skill

# Specify template type
python scripts/init_knowledge_skill.py my-skill --type framework-guidance

# Template types:
#   - generic
#   - knowledge-retrieval (default)
#   - framework-guidance
#   - translation
```

## Template Structure

All templates follow official Anthropic skill structure:

```markdown
---
name: skill-name
description: [Description with trigger keywords]
---

# Skill Title

## Purpose
[What the skill accomplishes]

## When to Use This Skill
[Specific scenarios and keywords]

## Resource Organization
[How scripts/, references/, assets/ are used]

## Progressive Disclosure
[Token loading strategy]

## Core Capabilities
[Numbered list of capabilities with processes]

## Usage Patterns
[Common scenarios with workflows]

## Token Budget
[Estimated token usage table]

## Available Resources
[Lists of scripts, references, assets]

## Version
[Version info]
```

## Customization

After running `init_knowledge_skill.py`:

1. Replace `[TODO]` placeholders with actual content
2. Add specific capabilities relevant to your knowledge base
3. Include concrete usage examples from your domain
4. Organize references and assets appropriately
5. Document token budgets based on your content size

## Template Selection Guide

| If your skill... | Use template |
|------------------|--------------|
| Searches documentation or knowledge bases | `knowledge-retrieval` |
| Helps users complete frameworks/worksheets | `framework-guidance` |
| Translates content between languages | `translation` |
| Doesn't fit above categories | `generic` |

## Examples

### Knowledge Retrieval
```bash
python scripts/init_knowledge_skill.py dao-knowledge --type knowledge-retrieval
```
Creates skill for searching DAO documentation with search, parsing, citation capabilities.

### Framework Guidance
```bash
python scripts/init_knowledge_skill.py social-lean-canvas --type framework-guidance
```
Creates skill for guiding users through Social Lean Canvas with templates and interactive support.

### Translation
```bash
python scripts/init_knowledge_skill.py knowledge-translator --type translation
```
Creates skill for translating markdown while preserving structure and links.

## Next Steps After Init

1. **Analyze your knowledge base:**
   ```bash
   python scripts/analyze_knowledge_repo.py /path/to/knowledge/base
   ```

2. **Edit SKILL.md:**
   - Replace TODO placeholders
   - Add domain-specific capabilities
   - Include real usage examples

3. **Organize references:**
   - Create quick-reference.md for common patterns
   - Add topic-specific guides
   - Include real examples

4. **Add assets:**
   - Templates for users to fill out
   - Configuration examples
   - Schemas or images

5. **Validate:**
   ```bash
   python scripts/validate_skill.py ./your-skill
   ```

6. **Package:**
   ```bash
   python scripts/package_skill.py ./your-skill
   ```

## Version

**Version:** 1.0.0
**Last Updated:** 2025-11-07
