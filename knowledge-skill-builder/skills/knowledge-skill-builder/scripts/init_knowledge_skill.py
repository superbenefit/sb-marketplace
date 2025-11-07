#!/usr/bin/env python3
"""
Initialize a new knowledge-based skill from template.

Usage:
  python init_knowledge_skill.py <skill-name> [--type <template-type>] [--path <output-path>]

Template Types:
  - knowledge-retrieval: Search, lookup, and citation skills (default)
  - framework-guidance: Interactive worksheet and template completion skills
  - knowledge-translation: Multilingual content transformation skills
  - generic: Blank template for custom use cases

Examples:
  python init_knowledge_skill.py dao-knowledge
  python init_knowledge_skill.py dao-knowledge --type knowledge-retrieval
  python init_knowledge_skill.py social-lean-canvas --type framework-guidance --path ./skills
"""

import argparse
import os
import sys
from pathlib import Path

# Template content for different skill types
GENERIC_TEMPLATE = """---
name: {skill_name}
description: [TODO: Brief description of what this skill does and when to use it (max 1024 chars)]
---

# {skill_title}

## Purpose

[TODO: State clearly what this skill helps accomplish]

## When to Use This Skill

[TODO: List specific scenarios when this skill should be activated]

## Resource Organization

**Scripts**: [TODO: Describe any executable automation scripts]

**References**: [TODO: List documentation files loaded as needed]

**Assets**: [TODO: List output-ready files like templates]

## Progressive Disclosure

- **Metadata**: Name and description always available (~100 tokens)
- **This file**: Loaded when skill is triggered (<5K words)
- **References**: Loaded as Claude determines necessity
- **Assets**: Used without loading to context

## Core Capabilities

### 1. [Capability Name]

[TODO: Describe what this capability does in imperative form]

**Process:**
1. [First step]
2. [Second step]
3. [Continue...]

### 2. [Another Capability]

[TODO: Describe what this capability does in imperative form]

## Usage Patterns

### Pattern 1: [Common Use Case]

**Scenario:** [Describe the scenario]

**Workflow:**
1. [Step by step process]
2. [Continue...]

### Pattern 2: [Another Use Case]

**Scenario:** [Describe the scenario]

**Workflow:**
1. [Step by step process]
2. [Continue...]

## Token Budget

| Operation | Estimated Tokens | Loading Strategy |
|-----------|------------------|------------------|
| Metadata scan | ~100 | Always loaded |
| SKILL.md body | ~[estimate] | Loaded when triggered |
| [Operation 1] | ~[estimate] | [Strategy] |
| [Operation 2] | ~[estimate] | [Strategy] |

## Workflow Overview

1. [Step 1 in imperative form]
2. [Step 2 in imperative form]
3. [Continue...]

## Available Scripts

[TODO: List scripts in scripts/ directory with brief descriptions]

## Available References

[TODO: List reference files in references/ directory with brief descriptions]

## Available Assets

[TODO: List asset files in assets/ directory with brief descriptions]

## Version

**Skill Version**: 1.0.0
**Last Updated**: [Date]
"""

KNOWLEDGE_RETRIEVAL_TEMPLATE = """---
name: {skill_name}
description: [TODO: Search, retrieve, and cite knowledge from [your domain]. Use when users ask questions about [topics] or need information from [knowledge base name].]
---

# {skill_title}

## Purpose

Retrieve and interpret knowledge from markdown-based knowledge repository about [TODO: your domain]. Provide accurate answers with source citations and suggest related content.

## When to Use This Skill

- Users ask questions about [TODO: your domain topics]
- Users request information from [TODO: knowledge base name]
- Users need to explore related concepts or documents
- Users mention keywords: [TODO: list relevant keywords]

## Resource Organization

**Scripts**: Optional automation for knowledge base updates or indexing

**References**: Quick reference guides and common patterns from knowledge base

**Assets**: Templates for citations or output formats

## Progressive Disclosure

- **Metadata**: Name and description always available (~100 tokens)
- **This file**: Loaded when knowledge questions detected (<5K words)
- **References**: Loaded as specific topics are queried
- **Assets**: Citation templates provided without context loading

## Core Capabilities

### 1. Search Knowledge Base

Search across markdown files using full-text search, tags, and wikilinks.

**Process:**
1. Parse user query to extract key concepts and search terms
2. Search markdown files using appropriate strategy (full-text, tags, links)
3. Identify relevant documents and sections
4. Rank results by relevance to query
5. Extract pertinent information from top results

### 2. Parse and Interpret Content

Extract and synthesize information from multiple markdown documents.

**Process:**
1. Read relevant markdown files identified by search
2. Parse YAML frontmatter for metadata and relationships
3. Extract key sections using markdown structure (headings, lists)
4. Synthesize information across multiple sources
5. Maintain context from document relationships

### 3. Navigate Knowledge Graph

Follow backlinks, wikilinks, and tags to find related content.

**Process:**
1. Identify links in current document (wikilinks [[page]], tags #tag)
2. Resolve links to actual files in knowledge base
3. Follow relationships to related content
4. Build context by traversing knowledge graph
5. Suggest related topics based on graph structure

### 4. Cite Sources

Provide proper attribution for all knowledge retrieved.

**Process:**
1. Track source file and location for all information used
2. Format citations with file path and section
3. Include relevant metadata from frontmatter
4. Link to original documents when possible
5. Maintain provenance chain for synthesized information

## Usage Patterns

### Pattern 1: Direct Question

**Scenario:** User asks "What are [TODO: key concepts in your domain]?"

**Workflow:**
1. Identify key search terms from question
2. Search knowledge base for relevant documents
3. Parse top results for concept definitions and explanations
4. Synthesize comprehensive answer from multiple sources
5. Provide answer with citations to source documents
6. Suggest related concepts user might explore

### Pattern 2: Topic Exploration

**Scenario:** User requests "Show me everything about [TODO: a topic]"

**Workflow:**
1. Find main document(s) about the topic
2. Navigate knowledge graph to find related documents
3. Identify subtopics and related concepts via links and tags
4. Present topic overview with structure
5. Offer deep-dive paths into specific aspects
6. Cite all sources

### Pattern 3: Find Related Content

**Scenario:** User asks "What's related to [TODO: concept]?"

**Workflow:**
1. Locate document(s) about the concept
2. Extract backlinks (pages linking to this concept)
3. Extract forward links (pages this concept links to)
4. Identify shared tags and similar metadata
5. Present map of related concepts with descriptions
6. Provide citations for each relationship

## Token Budget

| Operation | Estimated Tokens | Loading Strategy |
|-----------|------------------|------------------|
| Metadata scan | ~100 | Always loaded |
| SKILL.md body | ~2000-2500 | Loaded when knowledge queries detected |
| Quick lookup | ~500-1000 | Single doc, specific section |
| Standard query | ~1000-1500 | 2-3 docs, synthesized answer |
| Deep research | ~2000-3000 | Multiple docs, full context |
| Reference files | ~500-1500 each | Loaded per topic as needed |

## Workflow Overview

1. Detect knowledge query from user request
2. Identify search strategy (keywords, tags, links)
3. Search knowledge base for relevant content
4. Parse and extract information from markdown files
5. Navigate relationships for additional context
6. Synthesize answer from multiple sources
7. Format response with proper citations
8. Suggest related content for exploration

## Available Scripts

[TODO: Add scripts if needed for knowledge base indexing or maintenance]

## Available References

`references/quick-reference.md` - [TODO: Common patterns and frequently accessed content]

`references/search-patterns.md` - [TODO: Effective search strategies for this knowledge base]

## Available Assets

`assets/citation-template.md` - [TODO: Standard citation format]

## Notes

[TODO: Add specific notes about your knowledge base structure, linking conventions, tagging system, etc.]

## Version

**Skill Version**: 1.0.0
**Last Updated**: [Date]
"""

FRAMEWORK_GUIDANCE_TEMPLATE = """---
name: {skill_name}
description: [TODO: Guide users through [framework name] completion with templates, examples, and interactive support. Use when users mention "[framework name]", need templates, or request help with [framework purpose].]
---

# {skill_title}

## Purpose

Help users apply [TODO: framework name] to their specific organizational context. Provide templates, guide completion, ask clarifying questions, and review completed work.

## When to Use This Skill

- Users mention "[TODO: framework name]" or related keywords
- Users request templates or worksheets
- Users need help with [TODO: framework purpose like "business model design", "governance planning"]
- Users ask for examples or guidance on [TODO: framework application]

## Resource Organization

**Scripts**: Optional automation for template generation or validation

**References**: Complete framework guides, examples, and best practices

**Assets**: Templates (blank and annotated) for direct use

## Progressive Disclosure

- **Metadata**: Name and description always available (~100 tokens)
- **This file**: Loaded when framework keywords detected (<5K words)
- **References**: Framework guides loaded as needed for specific sections
- **Assets**: Templates provided to users without loading to context

## Core Capabilities

### 1. Deliver Templates

Provide blank and annotated templates in markdown format.

**Process:**
1. Determine which template user needs (blank or annotated)
2. Retrieve template from assets/ directory
3. Provide template with brief explanation of purpose
4. Offer to guide completion or answer questions
5. Suggest examples if user wants to see completed versions

### 2. Guide Interactive Completion

Walk users through framework section by section with contextual questions.

**Process:**
1. Present first section of framework with explanation
2. Ask clarifying questions about user's specific context
3. Provide prompts to help user think through each element
4. Offer examples relevant to user's situation
5. Move to next section when current is clear
6. Summarize completed sections periodically

### 3. Adapt to User Context

Translate generic framework to user's specific organizational situation.

**Process:**
1. Ask about user's organization type, size, and goals
2. Identify which framework elements are most relevant
3. Provide industry or domain-specific examples
4. Suggest adaptations for user's context
5. Bridge framework theory to user's practical reality
6. Reference similar examples from knowledge base

### 4. Review Completed Work

Examine user's completed framework and suggest improvements.

**Process:**
1. Read user's completed framework or section
2. Check for completeness of all required elements
3. Assess clarity and specificity of responses
4. Identify gaps or areas needing more detail
5. Suggest refinements and improvements
6. Connect to related concepts in knowledge base
7. Validate alignment with framework best practices

## Usage Patterns

### Pattern 1: Template Request

**Scenario:** User says "I need a [TODO: framework name] template"

**Workflow:**
1. Ask if user wants blank template or annotated version with guidance
2. Provide requested template from assets/
3. Briefly explain framework purpose and structure
4. Offer to guide completion interactively
5. Point to examples in references/ if user wants to see completed versions

### Pattern 2: Guided Completion

**Scenario:** User requests "Help me complete a [TODO: framework name]"

**Workflow:**
1. Provide overview of framework structure
2. Ask about user's organizational context
3. Start with first section:
   - Explain section purpose
   - Ask contextual questions
   - Provide relevant examples
   - Help user articulate their response
4. Move through each section systematically
5. Summarize and review completed framework
6. Suggest refinements

### Pattern 3: Framework Review

**Scenario:** User shares completed framework and asks "Can you review this?"

**Workflow:**
1. Read completed framework carefully
2. Check each section for:
   - Completeness
   - Clarity and specificity
   - Alignment with framework intent
   - Internal consistency
3. Provide structured feedback:
   - Strengths
   - Areas to clarify or expand
   - Specific suggestions
   - Related concepts to consider
4. Offer to help refine specific sections

### Pattern 4: Example Request

**Scenario:** User asks "Show me an example of a completed [TODO: framework name]"

**Workflow:**
1. Retrieve relevant example from references/
2. Present example with context about the organization
3. Highlight how each section was completed
4. Point out particularly effective elements
5. Note how example adapted framework to specific context
6. Offer additional examples if available

## Token Budget

| Operation | Estimated Tokens | Loading Strategy |
|-----------|------------------|------------------|
| Metadata scan | ~100 | Always loaded |
| SKILL.md body | ~2000-2500 | Loaded when framework keywords detected |
| Template delivery | ~200-500 | Template provided from assets |
| Guided completion | ~1500-2500 | Interactive session with examples |
| Framework review | ~1000-2000 | Analysis and feedback |
| Reference guides | ~1000-2000 each | Loaded per section as needed |
| Examples | ~500-1500 each | Loaded when requested |

## Workflow Overview

1. Detect framework-related request from user
2. Determine what user needs (template, guidance, review, example)
3. Gather context about user's situation
4. Provide appropriate support:
   - Templates from assets/
   - Guided completion with questions
   - Review with feedback
   - Examples from references/
5. Connect framework to user's specific context
6. Suggest next steps or related frameworks

## Available Scripts

[TODO: Add scripts if needed for template generation or validation]

## Available References

`references/framework-guide.md` - [TODO: Complete guide to framework with theory and best practices]

`references/examples.md` - [TODO: Real completed examples from various contexts]

`references/section-prompts.md` - [TODO: Clarifying questions for each framework section]

## Available Assets

`assets/templates/blank-template.md` - [TODO: Clean template ready for completion]

`assets/templates/annotated-template.md` - [TODO: Template with guidance notes in each section]

## Notes

[TODO: Add specific notes about framework origin, when to use it, common adaptations, etc.]

## Version

**Skill Version**: 1.0.0
**Last Updated**: [Date]
"""

TRANSLATION_TEMPLATE = """---
name: {skill_name}
description: [TODO: Translate markdown knowledge content while preserving structure, frontmatter, and links. Use when users request translation or mention target languages.]
---

# {skill_title}

## Purpose

Translate markdown knowledge base content between languages while preserving markdown syntax, YAML frontmatter, cross-references, and document structure.

## When to Use This Skill

- Users request translation of markdown documents
- Users specify target language for content
- Users mention translation keywords or language codes
- Users need multilingual knowledge base support

## Resource Organization

**Scripts**: Optional automation for batch translation or link updating

**References**: Translation patterns and frontmatter handling guides

**Assets**: Language-specific templates and formatting conventions

## Progressive Disclosure

- **Metadata**: Name and description always available (~100 tokens)
- **This file**: Loaded when translation requested (<5K words)
- **References**: Loaded as specific translation issues arise
- **Assets**: Language templates provided without context loading

## Core Capabilities

### 1. Markdown-Aware Translation

Translate content while preserving all markdown formatting.

**Process:**
1. Parse markdown to identify structure (headings, lists, tables, code blocks)
2. Extract translatable content vs. markup
3. Preserve code blocks, URLs, and technical identifiers unchanged
4. Translate natural language text
5. Reconstruct markdown with translated content and original structure
6. Validate output markdown is properly formatted

### 2. Frontmatter Preservation

Handle YAML frontmatter appropriately during translation.

**Process:**
1. Parse YAML frontmatter separately from content
2. Identify which fields to translate (title, description) vs. preserve (tags, dates, IDs)
3. Translate appropriate frontmatter fields
4. Add translation metadata (lang, original, translations)
5. Preserve technical fields unchanged
6. Reconstruct valid YAML frontmatter

### 3. Cross-Reference Management

Maintain and update links between documents across languages.

**Process:**
1. Identify all links in document (wikilinks [[page]], markdown links, hashtags)
2. Determine if linked documents have translations
3. Update links to point to translated versions when available
4. Preserve links to original when translation unavailable
5. Add bidirectional translation links in frontmatter
6. Maintain knowledge graph connections across languages

### 4. Locale-Specific Formatting

Apply locale conventions for dates, numbers, and cultural context.

**Process:**
1. Identify dates, numbers, and locale-specific content
2. Apply target language formatting conventions
3. Adapt cultural references appropriately
4. Handle idiomatic expressions with equivalent meaning
5. Preserve technical terminology consistently
6. Maintain glossary for domain-specific terms

## Usage Patterns

### Pattern 1: Single Document Translation

**Scenario:** User requests "Translate governance-guide.md to Spanish"

**Workflow:**
1. Read source document
2. Parse markdown structure and frontmatter
3. Translate content while preserving formatting
4. Update frontmatter with language metadata:
   - lang: es
   - original: governance-guide.md
   - translations: { en: governance-guide.md }
5. Save as governance-guide-es.md or in es/ directory
6. Update original document frontmatter with translation link

### Pattern 2: Batch Translation

**Scenario:** User requests "Translate all DAO framework docs to French"

**Workflow:**
1. Identify all documents in DAO framework category
2. Process each document:
   - Translate content
   - Update frontmatter
   - Maintain cross-references
3. Create consistent directory structure for translations
4. Update all bidirectional translation links
5. Validate all links work correctly
6. Provide summary of translated documents

### Pattern 3: Update Existing Translation

**Scenario:** Original document changed, translation needs update

**Workflow:**
1. Compare original with translated version
2. Identify changed sections
3. Translate only updated content
4. Merge updates into existing translation
5. Preserve any translation-specific adaptations
6. Update version metadata

## Token Budget

| Operation | Estimated Tokens | Loading Strategy |
|-----------|------------------|------------------|
| Metadata scan | ~100 | Always loaded |
| SKILL.md body | ~1500-2000 | Loaded when translation requested |
| Single doc translation | ~1000-2000 | Depends on document size |
| Batch translation | ~2000-4000 | Multiple documents |
| Reference guides | ~500-1000 each | Loaded as needed |

## Workflow Overview

1. Detect translation request from user
2. Identify source document(s) and target language
3. Parse markdown and frontmatter structure
4. Translate content while preserving formatting
5. Update frontmatter with translation metadata
6. Manage cross-references and links
7. Apply locale-specific formatting
8. Validate output and save

## Available Scripts

[TODO: Add scripts if needed for batch translation or link management]

## Available References

`references/translation-patterns.md` - [TODO: Common translation scenarios and approaches]

`references/frontmatter-handling.md` - [TODO: Which fields to translate vs. preserve]

## Available Assets

[TODO: Language-specific templates if needed]

## Notes

[TODO: Add specific notes about supported languages, glossaries, terminology conventions, etc.]

## Version

**Skill Version**: 1.0.0
**Last Updated**: [Date]
"""


def create_skill(skill_name, template_type, output_path):
    """Create a new skill directory with selected template."""

    # Validate skill name
    if not all(c.islower() or c.isdigit() or c == '-' for c in skill_name):
        print("Error: Skill name must contain only lowercase letters, numbers, and hyphens")
        return False

    if len(skill_name) > 64:
        print("Error: Skill name must be 64 characters or less")
        return False

    # Create skill directory
    skill_path = Path(output_path) / skill_name
    if skill_path.exists():
        print(f"Error: Directory {skill_path} already exists")
        return False

    skill_path.mkdir(parents=True)
    (skill_path / "scripts").mkdir()
    (skill_path / "references").mkdir()
    (skill_path / "assets" / "templates").mkdir(parents=True)

    # Select template
    skill_title = skill_name.replace('-', ' ').title()
    templates = {
        'generic': GENERIC_TEMPLATE,
        'knowledge-retrieval': KNOWLEDGE_RETRIEVAL_TEMPLATE,
        'framework-guidance': FRAMEWORK_GUIDANCE_TEMPLATE,
        'knowledge-translation': TRANSLATION_TEMPLATE
    }

    template = templates.get(template_type, GENERIC_TEMPLATE)
    skill_content = template.format(
        skill_name=skill_name,
        skill_title=skill_title
    )

    # Write SKILL.md
    (skill_path / "SKILL.md").write_text(skill_content)

    # Create example reference
    (skill_path / "references" / "quick-reference.md").write_text(
        f"# Quick Reference for {skill_title}\n\n"
        "[TODO: Add frequently-used patterns, API signatures, or common examples]\n"
    )

    # Create example asset if framework template
    if template_type == 'framework-guidance':
        (skill_path / "assets" / "templates" / "blank-template.md").write_text(
            f"# [TODO: Framework Name]\n\n"
            "[TODO: Add blank template sections]\n"
        )

    print(f"\n✓ Skill '{skill_name}' created successfully at: {skill_path}")
    print(f"\nDirectory structure:")
    print(f"  {skill_name}/")
    print(f"  ├── SKILL.md                 (Generated from {template_type} template)")
    print(f"  ├── scripts/                 (Add automation scripts here)")
    print(f"  ├── references/              (Add documentation here)")
    print(f"  │   └── quick-reference.md   (Example reference file)")
    print(f"  └── assets/                  (Add templates and output files here)")
    print(f"      └── templates/")

    if template_type == 'framework-guidance':
        print(f"          └── blank-template.md  (Example template)")

    print(f"\nNext steps:")
    print(f"  1. Edit {skill_path}/SKILL.md and replace [TODO] placeholders")
    print(f"  2. Add reference documents to {skill_path}/references/")
    print(f"  3. Add templates or assets to {skill_path}/assets/")
    print(f"  4. Run validate_skill.py to check your skill")
    print(f"  5. Run package_skill.py to create distributable ZIP\n")

    return True


def main():
    parser = argparse.ArgumentParser(
        description='Initialize a new knowledge-based skill from template',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('skill_name', help='Name of the skill (lowercase, hyphens only, max 64 chars)')
    parser.add_argument('--type', choices=['generic', 'knowledge-retrieval', 'framework-guidance', 'knowledge-translation'],
                        default='knowledge-retrieval', help='Template type (default: knowledge-retrieval)')
    parser.add_argument('--path', default='.', help='Output directory path (default: current directory)')

    args = parser.parse_args()

    if not create_skill(args.skill_name, args.type, args.path):
        sys.exit(1)


if __name__ == '__main__':
    main()
