# Skill Structure Guide

Complete guide to skill anatomy following official Anthropic patterns.

## Overview

A well-structured skill consists of:

1. **SKILL.md** (required) - Main skill definition with YAML frontmatter
2. **scripts/** (optional) - Executable automation scripts
3. **references/** (optional) - Documentation loaded into context as needed
4. **assets/** (optional) - Output-ready files used without loading to context

## SKILL.md File Structure

### YAML Frontmatter (Required)

Every SKILL.md must begin with YAML frontmatter enclosed in `---`:

```yaml
---
name: skill-name
description: Brief description of what this skill does and when to use it
---
```

#### Required Fields

**name** (string)
- Format: lowercase letters, numbers, hyphens only
- Length: maximum 64 characters
- Examples: `dao-knowledge`, `social-lean-canvas`, `knowledge-translator`
- Invalid: `DAO_Knowledge`, `Social Lean Canvas`, `my skill`

**description** (string)
- Length: maximum 1024 characters
- Should include:
  - What the skill does
  - When to use it (triggers for automatic loading)
  - Key capabilities or domains
- Example: "Search and retrieve knowledge from DAO governance documentation. Use when users ask about decentralized governance, DAO primitives, or organizational frameworks."

#### Optional Fields

**allowed-tools** (list)
- Restricts which tools Claude can use when skill is active
- Example: `['Read', 'Grep', 'Glob']` for read-only file access
- Use sparingly - most skills don't need this restriction

### Markdown Content (Required)

Following the frontmatter, write comprehensive skill documentation in markdown.

#### Recommended Sections

**Purpose**
- Clear statement of what the skill accomplishes
- Target audience or use cases
- How it differs from similar skills

**When to Use This Skill**
- Specific scenarios that trigger skill activation
- Keywords or phrases that should load this skill
- File patterns or task types

**Resource Organization**
- Brief description of scripts/, references/, assets/ contents
- How resources are used

**Progressive Disclosure**
- How context is managed (metadata → SKILL.md → references → assets)
- Token budgets for different loading levels

**Core Capabilities**
- List of main capabilities (numbered or bulleted)
- Each capability with clear description and process
- Use imperative form: "To accomplish X, do Y"

**Usage Patterns**
- Common scenarios with step-by-step workflows
- Concrete examples showing skill in action
- Different use cases demonstrating versatility

**Token Budget** (optional but recommended)
- Table showing estimated token usage for operations
- Helps users understand performance characteristics
- Demonstrates thought given to efficiency

**Workflow Overview**
- High-level process flow
- How different capabilities work together
- Integration points with other tools

**Available Resources**
- List of scripts with brief descriptions
- List of references with brief descriptions
- List of assets with brief descriptions

**Version**
- Skill version number
- Last updated date
- Compatibility notes if relevant

## Directory Structure

### scripts/

Executable code that performs deterministic tasks.

**When to Use:**
- Tasks that need to be run repeatedly
- Operations that shouldn't be rewritten each time
- Complex automation (analysis, packaging, validation)

**Best Practices:**
- Use Python for cross-platform compatibility
- Make scripts executable (`chmod +x`)
- Include clear docstrings with usage examples
- Provide helpful error messages
- Return proper exit codes (0 for success, 1 for error)

**Example Scripts:**
- `init_skill.py` - Initialize new skill from template
- `analyze_repo.py` - Analyze knowledge repository
- `validate.py` - Check skill meets requirements
- `package.py` - Create distributable archive

### references/

Documentation files loaded into Claude's context when needed.

**When to Use:**
- API documentation and schemas
- Detailed guides and tutorials
- Pattern libraries and examples
- Reference materials too large for SKILL.md

**Best Practices:**
- Keep frequently-used content in quick reference files
- Organize by topic (one topic per file typically better than one large file)
- Cross-reference related content
- Estimate and document token usage
- Use clear, descriptive filenames

**Token Optimization:**
- Quick references: ~200-500 tokens (frequently accessed)
- Standard guides: ~1000-2000 tokens (moderate detail)
- Comprehensive docs: ~2000-5000 tokens (rarely need full load)

**Example References:**
- `quick-reference.md` - Common patterns, frequently used
- `api-documentation.md` - Complete API reference
- `examples.md` - Real-world usage examples
- `troubleshooting.md` - Common issues and solutions

### assets/

Files meant to be used or delivered to users WITHOUT loading into context.

**When to Use:**
- Templates users will fill out
- Configuration file examples
- Images, diagrams, charts
- Schemas for validation
- Any output-ready files

**Best Practices:**
- Organize in subdirectories by type (templates/, schemas/, images/)
- Use descriptive filenames
- Include both blank and annotated versions of templates
- Keep files in ready-to-use formats

**Key Difference from References:**
- References: Loaded into Claude's context for understanding
- Assets: Provided to users without context loading

**Example Assets:**
- `templates/blank-canvas.md` - Empty template for users
- `templates/annotated-canvas.md` - Template with guidance notes
- `schemas/config-schema.json` - JSON schema for validation
- `images/workflow-diagram.png` - Visual workflow guide

## Progressive Disclosure Strategy

Skills manage context efficiently through layered loading:

### Level 1: Metadata (~100 tokens)
**Always loaded at startup**
- name field
- description field
- Allows Claude to know when to use skill without loading full content

### Level 2: SKILL.md Body (<5K words)
**Loaded when skill is triggered**
- Core capabilities
- Usage patterns
- Workflow overview
- References to deeper content

### Level 3: References (varies)
**Loaded as Claude determines necessity**
- Quick references loaded frequently
- Detailed guides loaded when specific topics needed
- Comprehensive docs loaded rarely

### Level 4: Assets (not loaded)
**Used without loading to context**
- Templates provided to users
- Files referenced but not analyzed
- Output-ready content

## Writing Style Guidelines

### Use Imperative Form

**Good:**
- "To create a skill, run init_skill.py"
- "Validate the skill before packaging"
- "Extract key concepts from the knowledge base"

**Avoid:**
- "You should run init_skill.py"
- "You must validate the skill"
- "You can extract key concepts"

### Be Specific and Actionable

**Good:**
- "Search markdown files using full-text search, tags, or wikilinks"
- "Parse YAML frontmatter to extract metadata and relationships"

**Avoid:**
- "Search the files"
- "Look at the metadata"

### Include Concrete Examples

**Good:**
```markdown
### Example: Direct Question

User: "What are the key principles of decentralized governance?"
→ Skill searches knowledge base for governance topics
→ Extracts principles from multiple documents
→ Synthesizes answer with citations
```

**Avoid:**
```markdown
The skill can answer questions about governance.
```

## Token Budget Documentation

Include a token budget table to help users understand performance:

```markdown
| Operation | Estimated Tokens | Loading Strategy |
|-----------|------------------|------------------|
| Metadata scan | ~100 | Always loaded |
| SKILL.md body | ~2500 | Loaded when triggered |
| Quick reference | ~500 | Loaded frequently |
| Deep dive | ~3000 | Loaded rarely |
```

## Validation Checklist

Before finalizing a skill, verify:

- ✅ SKILL.md exists and begins with valid YAML frontmatter
- ✅ name field: lowercase, hyphens, max 64 chars
- ✅ description field: clear, max 1024 chars, includes trigger keywords
- ✅ Markdown content is comprehensive and well-organized
- ✅ Imperative form used throughout (not second-person)
- ✅ Concrete examples included
- ✅ Resources organized appropriately (scripts/, references/, assets/)
- ✅ Token budgets documented
- ✅ Referenced files exist
- ✅ Scripts are executable
- ✅ No TODO placeholders remain

## Common Mistakes

### 1. Too Much in SKILL.md
**Problem:** Embedding all content directly in SKILL.md
**Solution:** Move detailed examples and references to references/ directory

### 2. Wrong Resource Location
**Problem:** Templates in references/ instead of assets/
**Solution:** Remember: references = load to context, assets = use without loading

### 3. Vague Description
**Problem:** "Helps with documentation"
**Solution:** "Searches Python API documentation and provides code examples. Use when working with Python standard library or third-party packages."

### 4. Second-Person Language
**Problem:** "You should validate your input"
**Solution:** "Validate input before processing"

### 5. Missing Trigger Keywords
**Problem:** Description doesn't mention when to use skill
**Solution:** Include keywords and scenarios in description

## Examples from Official Skills

### skill-creator (Anthropic)

```yaml
---
name: skill-creator
description: Build Claude skills using markdown, scripts, and references following official patterns
---
```

**Structure:**
- SKILL.md (~3000 words)
- scripts/
  - init_skill.py
  - package_skill.py
- references/ (none - all content in SKILL.md)
- assets/ (none)

**Note:** Minimal structure, most content in SKILL.md because skill is about skill creation itself.

### Example Knowledge Skill Structure

```yaml
---
name: dao-governance
description: Search and retrieve knowledge about DAO governance frameworks, voting mechanisms, and treasury management. Use when users ask about DAOs, decentralized governance, or organizational primitives.
---
```

**Structure:**
- SKILL.md (~2500 words - core capabilities)
- scripts/
  - update_index.py (optional - refresh knowledge index)
- references/
  - quick-reference.md (~500 tokens - common patterns)
  - voting-mechanisms.md (~1500 tokens - detailed guide)
  - treasury-management.md (~1500 tokens - detailed guide)
  - examples.md (~1000 tokens - real DAO examples)
- assets/
  - templates/
    - governance-proposal-template.md
    - voting-template.md

## Version History

**1.0.0** (2025-11-07)
- Initial guide based on official Anthropic patterns
- Comprehensive coverage of skill structure
- Examples and validation checklist
