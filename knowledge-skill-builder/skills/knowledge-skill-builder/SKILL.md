---
name: knowledge-skill-builder
description: Transform markdown knowledge repositories into Claude skills. Analyzes knowledge bases, generates SKILL.md files with appropriate loading strategies, and packages distributable skills. Use when creating skills from documentation, frameworks, or knowledge gardens.
---

# Knowledge Skill Builder

Build Claude skills from markdown knowledge repositories with guided analysis, generation, and packaging.

## Purpose

Transform existing markdown documentation, knowledge gardens, and framework repositories into well-structured Claude skills. Help users create knowledge-retrieval skills, framework-guidance skills, and translation skills without needing deep understanding of skill architecture.

## When to Use This Skill

- Creating skills from markdown documentation or knowledge bases
- Converting framework documentation into interactive guidance skills
- Building knowledge retrieval skills from existing content repositories
- Optimizing or refactoring existing knowledge-based skills
- Packaging skills for distribution in plugin marketplaces

## Resource Organization

**Scripts**: Python automation tools for analyzing repos, initializing skills, validating structure, and packaging for distribution

**References**: Documentation on skill structure, loading strategies, token optimization, and knowledge-skill patterns

**Assets**: Skill templates (SKILL.md templates for different skill types) that users can customize

## Progressive Disclosure

- **Metadata**: Name and description always available (~100 tokens)
- **This file**: Loaded when skill creation is requested (<5K words)
- **References**: Loaded as needed for specific guidance topics
- **Scripts**: Executed when automation is needed
- **Assets**: Templates provided to users without loading to context

## Core Capabilities

### 1. Analyze Knowledge Repository

Scan and understand markdown repository structure to inform skill design decisions.

**Process:**
1. Scan directory structure and identify file organization patterns
2. Parse YAML frontmatter schemas to understand metadata conventions
3. Identify linking patterns: wikilinks `[[page]]`, backlinks, hashtags `#tag`
4. Map content clusters and topic areas
5. Calculate token estimates for different loading strategies
6. Generate recommendations for skill structure

**Script:** Execute `scripts/analyze_knowledge_repo.py <repo-path>`

**Output:** Analysis report including:
- Content structure overview
- Topic clustering suggestions
- Linking pattern analysis
- Recommended loading strategy
- Token budget estimates
- Example trigger keywords

### 2. Initialize Knowledge Skill

Create new skill directory with structure optimized for knowledge-based skills following official Anthropic patterns.

**Process:**
1. Create skill directory with official structure: scripts/, references/, assets/
2. Generate SKILL.md from selected template type
3. Set up directories with example files appropriate to skill type
4. Include validation placeholders
5. Provide next-step guidance

**Script:** Execute `scripts/init_knowledge_skill.py <skill-name> --type <template-type>`

**Template Types Available:**
- `knowledge-retrieval`: Search, lookup, and citation skills
- `framework-guidance`: Interactive worksheet and template completion skills
- `knowledge-translation`: Multilingual content transformation skills
- `generic`: Blank template for custom use cases

**Directory Structure Created:**
```
skill-name/
├── SKILL.md                    # Generated from template
├── scripts/                    # Optional automation scripts
├── references/                 # Documentation loaded as needed
│   ├── quick-reference.md
│   └── examples.md
└── assets/                     # Templates and output files
    └── templates/
```

### 3. Generate SKILL.md Content

Create comprehensive SKILL.md content based on knowledge repository analysis.

**Process:**
1. Extract key concepts and patterns from analyzed knowledge base
2. Define capabilities based on content type and user requirements
3. Generate usage patterns with concrete examples
4. Configure loading triggers (keywords, file patterns, task context)
5. Create token optimization strategy
6. Write all content in imperative form (official Anthropic standard)

**Key Sections Generated:**
- YAML frontmatter (name, description, optional allowed-tools)
- Purpose statement explaining what the skill accomplishes
- When to Use section with clear trigger conditions
- Resource organization description
- Progressive disclosure strategy
- Core capabilities with detailed processes
- Usage patterns demonstrating common scenarios
- Token budget table
- References to bundled resources

### 4. Organize References

Structure the references/ directory for efficient progressive loading and token optimization.

**Process:**
1. Identify essential quick-reference content (API signatures, common patterns)
2. Extract reusable patterns and templates from knowledge base
3. Consolidate redundant information across documents
4. Create topic-specific reference files
5. Link references appropriately from SKILL.md

**Reference Categories:**
- **Quick references**: API signatures, syntax patterns (~200-500 tokens)
- **Detailed guides**: Comprehensive documentation (~1K-3K tokens)
- **Examples**: Real-world usage patterns with context (~500-1K tokens)

**Best Practices:**
- Keep frequently-used content in quick references
- Move detailed explanations to separate reference files
- Cross-reference related content instead of duplicating
- Estimate token usage for each reference file

### 5. Create Assets

Package output-ready files in assets/ directory that Claude can use or provide to users without loading into context.

**Asset Types:**
- **Templates**: Blank worksheets, canvas templates, forms
- **Schemas**: JSON/YAML schema definition files
- **Configuration examples**: Sample config files
- **Media**: Images, diagrams (if applicable)

**Process:**
1. Identify files users need as direct output (not for context)
2. Extract template structures from knowledge base
3. Format templates for immediate use
4. Organize by category in assets/ subdirectories

**Key Distinction:** Assets are used/provided to users WITHOUT loading into Claude's context, unlike references which ARE loaded when needed.

### 6. Validate Skill

Ensure skill meets official requirements before packaging and distribution.

**Script:** Execute `scripts/validate_skill.py <skill-path>`

**Validations Performed:**
- SKILL.md file exists and is readable
- YAML frontmatter is valid and properly formatted
- `name` field: lowercase letters, numbers, hyphens only, max 64 characters
- `description` field: present and within 1024 character limit
- Directory structure follows official conventions (scripts/, references/, assets/)
- Referenced files exist and are accessible
- No circular reference dependencies
- Token estimates are documented and reasonable
- Imperative form is used (not second-person language)

**Output:** Validation report with pass/fail status and specific issues if any

### 7. Package Skill

Create distributable .zip archive of completed skill ready for marketplace publication.

**Script:** Execute `scripts/package_skill.py <skill-path> --output <output-dir>`

**Process:**
1. Run complete validation checks
2. Create ZIP archive with proper compression
3. Preserve directory structure in archive
4. Include all scripts, references, and assets
5. Generate package metadata
6. Output to specified location or current directory

**Output:** `skill-name.zip` ready for installation via Claude Code

## Usage Patterns

### Pattern 1: Create Knowledge Retrieval Skill

**Scenario:** User has a markdown knowledge garden about decentralized organizing and wants to create a searchable skill.

**Workflow:**
1. Run repository analysis: `analyze_knowledge_repo.py ~/docs/dao-knowledge`
2. Review analysis report showing 47 files, wikilink patterns, tag taxonomy
3. Recommend knowledge-retrieval template with on-demand loading
4. Initialize skill: `init_knowledge_skill.py dao-knowledge --type knowledge-retrieval`
5. Generate SKILL.md with capabilities:
   - Full-text search across markdown files
   - Wikilink resolution and backlink navigation
   - Tag-based content filtering
   - Citation formatting with source attribution
6. Organize references:
   - `references/quick-reference.md`: Common DAO patterns
   - `references/governance-examples.md`: Real-world examples
7. Validate: `validate_skill.py dao-knowledge`
8. Package: `package_skill.py dao-knowledge`

### Pattern 2: Create Framework Guidance Skill

**Scenario:** User wants to help team members complete Social Lean Canvas worksheets interactively.

**Workflow:**
1. Analyze framework documentation repository
2. Recommend framework-guidance template with selective loading (keyword triggers)
3. Initialize: `init_knowledge_skill.py social-lean-canvas --type framework-guidance`
4. Generate SKILL.md with capabilities:
   - Deliver blank and annotated templates
   - Provide section-by-section completion guidance
   - Ask contextual questions to help users think through each section
   - Review completed canvases and suggest improvements
5. Create assets:
   - `assets/templates/blank-canvas.md`: Empty template for completion
   - `assets/templates/annotated-canvas.md`: Template with guidance notes
6. Organize references:
   - `references/canvas-guide.md`: How to complete each section
   - `references/examples.md`: Real completed canvases from community
7. Set up selective loading triggers: "social lean canvas", "business model", "lean canvas"
8. Validate and package

### Pattern 3: Optimize Existing Skill

**Scenario:** User's DAO knowledge skill is consuming 4000 tokens and needs optimization.

**Workflow:**
1. Read current SKILL.md and analyze structure
2. Run validation to identify issues:
   - Too many detailed examples embedded in SKILL.md body
   - Redundant pattern descriptions repeated across sections
   - Missing references/ directory structure
   - All content loaded at once instead of progressive disclosure
3. Recommend optimization changes:
   - Move detailed examples to `references/examples.md` (load as needed)
   - Consolidate redundant pattern descriptions
   - Create `references/quick-reference.md` for common queries
   - Restructure for progressive disclosure
4. Regenerate optimized SKILL.md with:
   - Leaner body focused on capabilities and workflows
   - References to detailed content instead of embedding
   - Proper progressive loading structure
5. Estimate new token usage: ~1200 tokens (70% reduction)
6. Validate optimized structure
7. Package updated version

### Pattern 4: Create Translation Skill

**Scenario:** User maintains multilingual knowledge base and wants skill to help translate while preserving markdown structure.

**Workflow:**
1. Analyze knowledge base for multilingual patterns
2. Initialize: `init_knowledge_skill.py knowledge-translator --type knowledge-translation`
3. Generate SKILL.md with capabilities:
   - Translate content while preserving markdown syntax
   - Maintain YAML frontmatter structure and metadata
   - Update cross-language reference links
   - Handle locale-specific formatting
4. Create references:
   - `references/translation-patterns.md`: Common translation scenarios
   - `references/frontmatter-handling.md`: Metadata translation rules
5. Set up on-demand loading (triggered by translation requests)
6. Validate and package

## Token Budget

| Operation | Estimated Tokens | Loading Strategy |
|-----------|------------------|------------------|
| Metadata scan | ~100 | Always loaded at startup |
| SKILL.md body | ~2500-3000 | Loaded when skill creation requested |
| Repository analysis | ~1000-1500 | Loaded when analyzing repos |
| Template generation | ~800-1200 | Loaded during skill initialization |
| Optimization guidance | ~600-1000 | Loaded when optimizing existing skills |
| Reference docs (each) | ~500-2000 | Loaded as specific topics needed |
| Complete session | ~5000-8000 | Full skill creation workflow |

## Workflow Overview

### Standard Skill Creation Process

1. **Analyze**: Run repository analysis to understand content structure
2. **Design**: Review analysis and decide on skill type and loading strategy
3. **Initialize**: Create skill directory from appropriate template
4. **Generate**: Create SKILL.md content based on knowledge base
5. **Organize**: Structure references/ and assets/ directories
6. **Validate**: Check all requirements are met
7. **Package**: Create distributable ZIP archive
8. **Iterate**: Test skill and refine based on real usage

### Quick Start for Common Cases

**Simple documentation skill:**
- Run init with knowledge-retrieval template
- Copy key docs to references/
- Validate and package

**Framework/worksheet skill:**
- Run init with framework-guidance template
- Add templates to assets/
- Add guidance to references/
- Configure selective loading triggers
- Validate and package

**Optimization of existing skill:**
- Run validate to identify issues
- Restructure content for progressive disclosure
- Move heavy content to references
- Re-validate to confirm improvements

## Best Practices

### Writing SKILL.md Content

- Use imperative/infinitive form: "To accomplish X, do Y" (not "You should...")
- Keep metadata (name + description) under 150 tokens
- Keep SKILL.md body under 5K words
- Reference detailed content instead of embedding
- Include concrete usage examples
- Document token budgets for transparency

### Organizing Resources

- **scripts/**: Only include automation that will be repeatedly useful
- **references/**: Content meant to be loaded into Claude's context
- **assets/**: Content meant to be used/delivered WITHOUT loading to context
- Consolidate redundant information
- Create topic-specific files rather than monolithic docs

### Loading Strategy Selection

- **Model-invoked (automatic)**: Claude decides based on description - most common
- **Progressive disclosure**: Always use this within skill structure
- **Trigger keywords**: Include in description for selective loading
- **File patterns**: Mention in description if skill applies to specific file types

### Token Optimization

- Start with lean SKILL.md focused on capabilities and workflows
- Move examples and detailed content to references
- Create quick-reference files for common queries (~200-500 tokens)
- Keep detailed guides separate (~1K-3K tokens each)
- Document token estimates for transparency
- Test actual usage to validate estimates

## Available Scripts

All scripts located in `${CLAUDE_PLUGIN_ROOT}/skills/knowledge-skill-builder/scripts/`

### init_knowledge_skill.py
Initialize new skill from template with proper structure

### analyze_knowledge_repo.py
Analyze markdown repository and generate recommendations

### validate_skill.py
Check skill meets all requirements before packaging

### package_skill.py
Create distributable ZIP archive with validation

## Available References

All references located in `${CLAUDE_PLUGIN_ROOT}/skills/knowledge-skill-builder/references/`

### skill-structure.md
Complete guide to skill anatomy following Anthropic patterns

### loading-strategies.md
When and how to use different loading approaches

### token-optimization.md
Best practices for creating token-efficient skills

### knowledge-skill-patterns.md
Common patterns for knowledge-based skills with examples

## Available Templates

All templates located in `${CLAUDE_PLUGIN_ROOT}/skills/knowledge-skill-builder/assets/templates/`

### SKILL-template.md
Generic template following official format

### knowledge-retrieval-template.md
Pre-configured for search and lookup skills

### framework-guidance-template.md
Pre-configured for interactive worksheet and template skills

### translation-template.md
Pre-configured for multilingual content skills

## Version

**Skill Version**: 1.0.0
**Last Updated**: 2025-11-07
**Compatible With**: Claude Code plugin system, Anthropic skill standards
