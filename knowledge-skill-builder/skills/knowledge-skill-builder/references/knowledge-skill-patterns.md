# Knowledge Skill Patterns

Common patterns for knowledge-based skills with real examples from the community.

## Overview

Knowledge skills help Claude work with markdown-based documentation, frameworks, and knowledge repositories. This guide covers proven patterns for different types of knowledge skills.

## Pattern Categories

1. **Knowledge Retrieval** - Search and cite from knowledge bases
2. **Framework Guidance** - Interactive help with templates and worksheets
3. **Translation** - Multilingual content transformation
4. **Documentation Lookup** - API and reference documentation access

## Pattern 1: Knowledge Retrieval Skills

### Purpose

Search, retrieve, and synthesize information from markdown knowledge repositories with proper citations.

### When to Use

- Knowledge gardens (personal or team documentation)
- Technical documentation collections
- Research notes and literature bases
- Community wikis

### Core Capabilities Structure

```markdown
### 1. Search Knowledge Base
Full-text search, tag filtering, wikilink navigation

### 2. Parse and Interpret Content
Extract information, parse frontmatter, synthesize across sources

### 3. Navigate Knowledge Graph
Follow backlinks, traverse tags, map relationships

### 4. Cite Sources
Attribute information with file paths, sections, metadata
```

### Real Example: DAO Knowledge Skill

```yaml
---
name: dao-knowledge
description: Search DAO governance documentation covering voting mechanisms, treasury management, and organizational primitives. Use when asked about decentralized governance, DAOs, or coordination frameworks.
---
```

**Structure:**
```
dao-knowledge/
├── SKILL.md                      (~2000 words)
├── references/
│   ├── quick-reference.md        (~500 tokens - common patterns)
│   ├── voting-mechanisms.md      (~1500 tokens - detailed)
│   ├── treasury-management.md    (~1500 tokens - detailed)
│   └── examples.md               (~1000 tokens - real DAOs)
└── assets/
    └── citations/
        └── citation-format.md    (How to cite DAO resources)
```

**Key Features:**
- Wikilink resolution for navigating related concepts
- Tag-based filtering (e.g., #governance, #voting, #treasury)
- Frontmatter parsing for metadata (author, date, category)
- Multi-document synthesis with source attribution

**Usage Pattern:**

```markdown
User: "What are the common voting mechanisms in DAOs?"

→ Search for "voting mechanisms" + #voting tag
→ Find relevant documents in knowledge base
→ Parse content and extract voting types
→ Synthesize information across sources
→ Present answer with citations:

"Common DAO voting mechanisms include:

1. **Token-weighted voting**: Voting power proportional to token holdings
   (Source: voting-mechanisms.md:45)

2. **Quadratic voting**: Voting power grows with square root of tokens
   (Source: governance-patterns.md:112)

3. **Conviction voting**: Voting power increases with time
   (Source: voting-mechanisms.md:78)

Related concepts: [[quorum]], [[delegation]], [[snapshot-voting]]"
```

### Implementation Tips

**Frontmatter Schema:**
```yaml
---
title: Document title
date: 2025-11-07
tags: [governance, voting, daos]
related: [[quorum]], [[delegation]]
author: Community
status: active
---
```

**Search Strategy Priority:**
1. Exact phrase matches in titles or headings
2. Full-text search for keywords
3. Tag-based filtering for related content
4. Wikilink traversal for connected concepts

**Citation Format:**
```markdown
(Source: file-name.md:line-number)
(Source: folder/file-name.md, section "Heading Name")
```

## Pattern 2: Framework Guidance Skills

### Purpose

Guide users through completing structured frameworks, templates, or worksheets with interactive support.

### When to Use

- Business model canvases
- Strategic planning frameworks
- Assessment worksheets
- Structured brainstorming tools

### Core Capabilities Structure

```markdown
### 1. Deliver Templates
Provide blank and annotated templates

### 2. Guide Interactive Completion
Walk through sections with contextual prompts

### 3. Adapt to Context
Translate generic framework to user's situation

### 4. Review Completed Work
Assess completeness and suggest improvements
```

### Real Example: Social Lean Canvas Skill

```yaml
---
name: social-lean-canvas
description: Guide users through Social Lean Canvas completion with interactive prompts, templates, and examples. Use when users mention 'social lean canvas', 'business model', or need help with social enterprise planning.
---
```

**Structure:**
```
social-lean-canvas/
├── SKILL.md                          (~2500 words)
├── references/
│   ├── canvas-guide.md               (~2000 tokens - section explanations)
│   ├── examples.md                   (~1500 tokens - completed canvases)
│   └── section-prompts.md            (~800 tokens - questions for each section)
└── assets/
    └── templates/
        ├── blank-canvas.md           (Empty template)
        ├── annotated-canvas.md       (With guidance notes)
        └── example-nonprofit.md      (Filled example)
```

**Template Structure:**

```markdown
# Social Lean Canvas: [Organization Name]

## Problem
[What social problem are you solving?]

**Prompts:**
- What is the root cause?
- Who is most affected?
- What is the current solution gap?

## Solution
[How does your solution address the problem?]

[... continues for all sections ...]
```

**Usage Pattern:**

```markdown
User: "Help me complete a social lean canvas for my food waste reduction nonprofit"

→ Provide overview of canvas structure
→ Start interactive completion:

"Let's complete your Social Lean Canvas step by step.

## Step 1: Problem
What social problem is your nonprofit solving?

**Context questions:**
- What's the scale of food waste in your target area?
- Who is currently affected by this waste?
- What existing solutions are insufficient?

Take your time to articulate the core problem..."

→ Continue through each section with:
  - Explanation of section purpose
  - Context-specific prompts
  - Relevant examples from similar nonprofits
  - Validation and refinement suggestions
```

### Implementation Tips

**Section Prompt Pattern:**
```markdown
## [Section Name]

**Purpose:** [Why this section matters]

**Prompts:**
- [Question 1 to help user think through this]
- [Question 2 for deeper insight]
- [Question 3 for specificity]

**Example:** [Relevant example from similar context]

**Common Mistakes:**
- [Avoid X - too vague]
- [Avoid Y - too broad]
```

**Context Adaptation:**
- Ask about organization type (nonprofit, cooperative, social enterprise)
- Ask about scale (local, regional, national)
- Ask about stage (idea, prototype, established)
- Adapt examples and prompts accordingly

**Review Checklist:**
```markdown
Reviewing your completed canvas:

✓ Each section is specific and measurable
✓ Problem and solution are clearly connected
✓ Unique value proposition is distinctive
✓ Customer segments are well-defined
✓ Channels are appropriate for segments
✓ Cost structure aligns with revenue model
✓ Key metrics are actionable
✓ Unfair advantage is sustainable
```

## Pattern 3: Translation Skills

### Purpose

Translate markdown knowledge content while preserving structure, frontmatter, and links.

### When to Use

- Multilingual documentation
- Knowledge base internationalization
- Cross-language research notes
- Collaborative global teams

### Core Capabilities Structure

```markdown
### 1. Markdown-Aware Translation
Translate content, preserve syntax

### 2. Frontmatter Preservation
Handle YAML metadata appropriately

### 3. Cross-Reference Management
Maintain links across languages

### 4. Locale-Specific Formatting
Apply cultural conventions
```

### Real Example: Knowledge Translator Skill

```yaml
---
name: knowledge-translator
description: Translate markdown knowledge base content between languages while preserving formatting, YAML frontmatter, and cross-references. Use when translation is requested or users specify target languages.
---
```

**Structure:**
```
knowledge-translator/
├── SKILL.md                       (~1800 words)
├── references/
│   ├── translation-patterns.md    (~1200 tokens - common scenarios)
│   └── frontmatter-handling.md    (~800 tokens - metadata rules)
└── assets/
    └── templates/
        └── multilingual-index.md  (Cross-language index template)
```

**Frontmatter Translation Strategy:**

```markdown
# Original (English)
---
title: "Decentralized Governance Guide"
description: "Comprehensive guide to DAO governance"
date: 2025-11-07
tags: [governance, daos, voting]
lang: en
translations:
  es: governance-es.md
  fr: governance-fr.md
---

# Translated (Spanish)
---
title: "Guía de Gobernanza Descentralizada"
description: "Guía integral de gobernanza de DAOs"
date: 2025-11-07
tags: [gobernanza, daos, votación]
lang: es
original: governance.md
translations:
  en: governance.md
  fr: governance-fr.md
---
```

**Usage Pattern:**

```markdown
User: "Translate dao-primitives.md to Spanish"

→ Read source document
→ Parse structure (frontmatter, headings, lists, code, links)
→ Translate content:
  - Translate: title, description, body text
  - Preserve: dates, technical terms, code blocks, URLs
  - Adapt: tags (optional), cultural references
→ Update frontmatter:
  - Set lang: es
  - Add original: dao-primitives.md
  - Maintain cross-references
→ Save as dao-primitives-es.md
→ Update original with translation link

"Translation complete. Saved as dao-primitives-es.md
- Preserved all markdown structure
- Maintained wikilinks and code blocks
- Updated frontmatter with cross-language references"
```

### Implementation Tips

**What to Translate:**
- Natural language text (headings, paragraphs, lists)
- Frontmatter: title, description
- Alt text for images
- Table content
- Optionally: tags (normalize or translate)

**What to Preserve:**
- Code blocks (keep code as-is)
- URLs and paths
- Dates and numbers (format per locale)
- Technical identifiers
- Wikilinks (update if translated version exists)

**Link Management:**
```markdown
# If linked document has translation:
[[governance]] → [[governance-es]] (in Spanish version)

# If no translation exists:
[[treasury]] → [[treasury]] (keep original link, add note)

# Preserve external links:
[Official Docs](https://example.com) → [Documentación Oficial](https://example.com)
```

## Pattern 4: Documentation Lookup Skills

### Purpose

Provide on-demand access to API documentation, reference materials, and technical specs.

### When to Use

- Framework API documentation
- Standard library references
- Protocol specifications
- Technical glossaries

### Core Capabilities Structure

```markdown
### 1. API Verification
Confirm current syntax and signatures

### 2. Feature Lookup
Check availability and usage patterns

### 3. Documentation Search
Find relevant docs quickly

### 4. Example Provision
Provide code examples
```

### Real Example: Astro Knowledge Skill (from sb-marketplace)

```yaml
---
name: astro-knowledge
description: API documentation and reference provider for Astro/Starlight. Provides on-demand documentation lookup, API verification, and feature availability checks.
---
```

**Structure:**
```
astro-knowledge/
├── SKILL.md                  (~1500 words)
├── references/
│   ├── docs-index.md         (~500 tokens - quick API reference)
│   └── llms-full.md          (~3000 tokens - comprehensive docs)
└── .mcp.json                 (MCP integration for real-time docs)
```

**Usage Pattern:**

```markdown
User: "How do I use getCollection in Astro?"

→ Lookup API in references/docs-index.md
→ Find getCollection signature and common usage
→ Provide answer with code example:

"Use `getCollection()` to retrieve content collection entries:

\`\`\`typescript
import { getCollection } from 'astro:content';

// Get all entries
const posts = await getCollection('blog');

// Filter entries
const published = await getCollection('blog', ({ data }) =>
  data.draft !== true
);
\`\`\`

Available since: Astro 2.0
See also: getEntry(), getEntries()
Docs: https://docs.astro.build/en/reference/api-reference/#getcollection
```

### Implementation Tips

**Quick Index Pattern:**
```markdown
# API Quick Reference

## Collections

**getCollection(collection, filter?)**
- Returns: Promise<CollectionEntry[]>
- Example: `await getCollection('blog')`

**getEntry(collection, id)**
- Returns: Promise<CollectionEntry>
- Example: `await getEntry('blog', 'post-1')`

[Keep concise - full docs in separate file or MCP]
```

**MCP Integration:**
For real-time documentation, integrate with MCP servers:

```json
{
  "mcpServers": {
    "astro-docs": {
      "type": "http",
      "url": "https://docs.astro.build/mcp"
    }
  }
}
```

**Versioning:**
Include version info in responses:
- "Available since: vX.X"
- "Deprecated in: vY.Y (use Z instead)"
- "Experimental - may change"

## Cross-Cutting Patterns

### Wikilink Resolution

**Format:** `[[Page Title]]` or `[[page-slug]]`

**Resolution Strategy:**
1. Look for exact filename match
2. Look for title match in frontmatter
3. Look for slug match in frontmatter
4. Fuzzy match on filename

**Example:**
```markdown
User sees: [[DAO Primitives]]
Resolve to: dao-primitives.md or primitives/daos.md
```

### Tag Taxonomy

**Hierarchical Tags:**
```yaml
tags: [governance/voting, governance/treasury, technical/smart-contracts]
```

**Tag Search:**
```markdown
#governance → all governance topics
#governance/voting → specific subtopic
```

### Frontmatter Schemas

**Minimal Schema:**
```yaml
---
title: Page title
date: 2025-11-07
tags: [tag1, tag2]
---
```

**Extended Schema:**
```yaml
---
title: Page title
description: Brief summary
date: 2025-11-07
updated: 2025-11-08
author: Name
tags: [tag1, tag2]
related: [[page1]], [[page2]]
status: draft | active | archived
lang: en
---
```

### Citation Formats

**File and Line:**
```markdown
(Source: dao-primitives.md:142)
```

**File and Section:**
```markdown
(Source: governance.md, "Voting Mechanisms")
```

**With Metadata:**
```markdown
(Source: governance.md, by Author Name, updated 2025-11-07)
```

**Multiple Sources:**
```markdown
(Sources: voting.md:45, governance.md:112, primitives.md:23)
```

## Testing Patterns

### Test Scenarios

For each skill type, test:

**Knowledge Retrieval:**
- Single-file lookup
- Multi-file synthesis
- Link navigation
- Tag filtering
- Citation accuracy

**Framework Guidance:**
- Template delivery
- Section-by-section completion
- Context adaptation
- Review and feedback

**Translation:**
- Structure preservation
- Frontmatter handling
- Link updating
- Locale formatting

**Documentation Lookup:**
- API signature lookup
- Version checking
- Example provision
- Related concept suggestion

### Sample Test Cases

**Knowledge Retrieval:**
```markdown
Test 1: "What is token-weighted voting?"
Expected: Definition from voting-mechanisms.md with citation

Test 2: "Compare voting mechanisms"
Expected: Synthesis from multiple docs with multiple citations

Test 3: "What's related to treasury management?"
Expected: Backlinks and forward links from treasury docs
```

**Framework Guidance:**
```markdown
Test 1: "I need a social lean canvas template"
Expected: Blank template from assets/

Test 2: "Help me complete the problem section"
Expected: Section explanation + context prompts

Test 3: "Review my completed canvas"
Expected: Feedback on completeness and specificity
```

## Version

**Version:** 1.0.0
**Last Updated:** 2025-11-07
