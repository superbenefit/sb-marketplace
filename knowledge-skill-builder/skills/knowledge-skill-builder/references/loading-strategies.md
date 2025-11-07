# Loading Strategies for Skills

Guide to when and how skills are loaded into Claude's context.

## Overview

Skills use **model-invoked loading** - Claude automatically decides when to load a skill based on the task context and skill description. The skill creator's job is to write a clear description that helps Claude know when the skill is relevant.

## Progressive Disclosure

All skills use progressive disclosure to manage context efficiently:

### Layer 1: Metadata (Always Loaded)
- **Content:** name + description from YAML frontmatter
- **Tokens:** ~50-150 tokens per skill
- **When:** At session startup
- **Purpose:** Let Claude know what skills are available without loading full content

### Layer 2: SKILL.md Body (Conditional)
- **Content:** Complete markdown content after frontmatter
- **Tokens:** Recommended <5000 words (~6000-8000 tokens)
- **When:** Claude determines skill is relevant to task
- **Purpose:** Provide capabilities, patterns, workflows

### Layer 3: References (As Needed)
- **Content:** Files in references/ directory
- **Tokens:** Varies by file (500-5000 tokens each)
- **When:** Claude determines specific reference is needed
- **Purpose:** Detailed documentation, examples, guides

### Layer 4: Assets (Never Loaded)
- **Content:** Files in assets/ directory
- **Tokens:** 0 (not loaded to context)
- **When:** Provided to user or used without context
- **Purpose:** Templates, configurations, output files

## Writing Effective Descriptions

The description field is critical for automatic loading. It should include:

### 1. What the Skill Does

Clear, specific statement of capabilities.

**Good:**
- "Search and retrieve knowledge from DAO governance documentation"
- "Guide users through Social Lean Canvas completion with templates and examples"
- "Translate markdown content while preserving structure and frontmatter"

**Avoid:**
- "Helps with documentation" (too vague)
- "A skill for working with files" (too generic)

### 2. When to Use It

Specific triggers and scenarios.

**Good:**
- "Use when users ask about decentralized governance, DAO primitives, or voting mechanisms"
- "Use when users mention 'social lean canvas' or request business model templates"
- "Use when translation is requested or target language is specified"

**Avoid:**
- "Use when needed" (not helpful)
- No trigger keywords mentioned

### 3. Domain or Context

Relevant topics, frameworks, or technologies.

**Good:**
- "Covers voting mechanisms, treasury management, proposal systems, and token economics"
- "Includes business model canvas, value proposition, and lean startup methodology"
- "Supports markdown, YAML frontmatter, wikilinks, and cross-references"

**Avoid:**
- No domain specification
- Overly broad ("everything about X")

## Example Descriptions

### Knowledge Retrieval Skill

```yaml
---
name: dao-knowledge
description: Search and retrieve knowledge from DAO governance documentation covering voting mechanisms, treasury management, and organizational primitives. Use when users ask about decentralized governance, DAOs, or coordination frameworks.
---
```

**Analysis:**
- ✅ Clear capability: "search and retrieve"
- ✅ Specific domain: "DAO governance documentation"
- ✅ Topics listed: "voting mechanisms, treasury management, organizational primitives"
- ✅ Trigger keywords: "decentralized governance, DAOs, coordination frameworks"
- Character count: 267 (well under 1024 limit)

### Framework Guidance Skill

```yaml
---
name: social-lean-canvas
description: Guide users through Social Lean Canvas completion with interactive prompts, templates, and examples. Use when users mention 'social lean canvas', 'business model', or need help with social enterprise planning and value proposition design.
---
```

**Analysis:**
- ✅ Clear capability: "guide through completion"
- ✅ Tools provided: "interactive prompts, templates, examples"
- ✅ Trigger keywords: explicit phrases in quotes
- ✅ Related concepts: "business model", "social enterprise", "value proposition"
- Character count: 256

### Translation Skill

```yaml
---
name: knowledge-translator
description: Translate markdown knowledge base content between languages while preserving formatting, YAML frontmatter, and cross-references. Use when translation is requested or users specify target languages for documentation.
---
```

**Analysis:**
- ✅ Clear capability: "translate markdown content"
- ✅ Preservation features: "formatting, frontmatter, cross-references"
- ✅ Trigger: "translation is requested" or "target languages specified"
- Character count: 234

## Loading Triggers

Skills are loaded when Claude detects relevant context. Help Claude by including:

### Keyword Triggers

Explicit keywords users might say:

```yaml
description: "... Use when users mention 'DAO', 'governance', 'voting', or 'treasury'."
```

### Task Patterns

Types of tasks the skill handles:

```yaml
description: "... Use when users need to complete worksheets, review templates, or design business models."
```

### File Patterns

Relevant file types or extensions:

```yaml
description: "... Use when working with markdown (.md) files containing YAML frontmatter."
```

### Domain Context

Specific frameworks or technologies:

```yaml
description: "... Covers Astro, Starlight, and SSG documentation frameworks."
```

## Token Optimization Strategies

### Keep SKILL.md Lean

**Problem:** SKILL.md with 10,000 words loads too much context

**Solution:**
- Keep SKILL.md under 5000 words
- Move detailed examples to references/
- Move comprehensive guides to references/
- Use references/ for topic-specific documentation

**Example:**

```markdown
# In SKILL.md (brief)
### Search Knowledge Base
Search across markdown files using full-text, tags, or wikilinks.
See `references/search-patterns.md` for detailed strategies.

# In references/search-patterns.md (detailed)
[2000 words of detailed search strategies, regex patterns, etc.]
```

### Organize References by Topic

**Problem:** One massive reference file loaded all or nothing

**Solution:**
- Split into topic-specific files
- Claude loads only relevant topic
- Better granularity

**Example:**

Instead of:
```
references/
└── everything.md  (10,000 words)
```

Use:
```
references/
├── quick-reference.md      (~500 words - common patterns)
├── voting-mechanisms.md    (~1500 words - specific topic)
├── treasury-management.md  (~1500 words - specific topic)
└── examples.md             (~1000 words - real examples)
```

### Create Quick References

**Strategy:** Frequently-used content in small files

**Example:**

```markdown
# references/quick-reference.md

## Common DAO Patterns

**Basic Proposal Flow:**
1. Submit proposal
2. Discussion period
3. Voting period
4. Execution (if passed)

**Quorum Calculation:**
`quorum = (total_tokens * quorum_percentage) / 100`

**Token Weight:**
`voting_power = token_balance * time_held_multiplier`

[Keep under 500 words for frequent loading]
```

### Use Assets for Non-Context Content

**Strategy:** Files meant for output go in assets/, not references/

**Example:**

```
assets/
└── templates/
    ├── proposal-template.md      # User fills this out
    ├── governance-charter.md     # Ready-to-use template
    └── voting-config.json        # Configuration example
```

These are **not loaded** into context, just provided to users when needed.

## Real-World Examples

### Astro-Coding Skill (from sb-marketplace)

```yaml
---
name: astro-coding
description: Smart context provider for Astro/Starlight code implementation. Provides patterns, best practices, and critical rules to agents performing coding tasks.
---
```

**Loading Strategy:**
- Metadata always available
- SKILL.md (~2000 words) loaded when coding task detected
- Critical rules section always in SKILL.md (small, essential)
- Detailed patterns in knowledge-base/ (loaded as needed)

**Token Budget:**
- Light context: ~200 tokens (critical rules + quick templates)
- Medium context: ~400 tokens (relevant pattern + common mistakes)
- Full context: ~800 tokens (multiple patterns + full knowledge base)

### Astro-Knowledge Skill (from sb-marketplace)

```yaml
---
name: astro-knowledge
description: API documentation and reference provider for Astro/Starlight. Provides on-demand documentation lookup, API verification, and feature availability checks.
---
```

**Loading Strategy:**
- On-demand: Loaded only when API lookup needed
- SKILL.md (~1500 words) explains capabilities
- References/ contains cached API docs (loaded per topic)
- MCP integration for real-time docs (when available)

**Token Budget:**
- Quick lookup: ~100 tokens (API signature + example)
- Standard lookup: ~300 tokens (full documentation + patterns)
- Comprehensive: ~600 tokens (multiple related APIs + guides)

## Anti-Patterns to Avoid

### ❌ Overly Generic Description

```yaml
description: "Helps with documentation tasks"
```

**Problem:** Too vague, Claude won't know when to load

**Fix:**
```yaml
description: "Search Python standard library documentation and provide code examples. Use when working with Python built-in modules or standard library functions."
```

### ❌ Everything in SKILL.md

```
skill-name/
└── SKILL.md  (15,000 words, all content embedded)
```

**Problem:** Loads too much context every time

**Fix:**
```
skill-name/
├── SKILL.md          (3,000 words - core capabilities)
└── references/
    ├── quick-ref.md  (500 words - frequent)
    ├── topic-1.md    (1,500 words - as needed)
    └── topic-2.md    (1,500 words - as needed)
```

### ❌ No Trigger Keywords

```yaml
description: "A skill for working with organizational frameworks"
```

**Problem:** No specific keywords for Claude to match

**Fix:**
```yaml
description: "Guide users through organizational frameworks including Social Lean Canvas and DAO Primitives. Use when users mention 'lean canvas', 'DAO governance', 'business model', or organizational design."
```

### ❌ Templates in References

```
references/
└── blank-template.md  # User will fill this out
```

**Problem:** Template loaded to context unnecessarily

**Fix:**
```
assets/
└── templates/
    └── blank-template.md  # Provided without loading
```

## Testing Loading Strategy

### Manual Testing

1. **Start Claude session** - Check if skill metadata loads
2. **Use trigger keywords** - Verify skill loads when expected
3. **Check token usage** - Ensure reasonable context consumption
4. **Test edge cases** - Verify skill doesn't load inappropriately

### Validation Questions

- ✅ Does description clearly state what skill does?
- ✅ Does description include trigger keywords?
- ✅ Is SKILL.md under 5000 words?
- ✅ Are detailed docs in references/, not SKILL.md?
- ✅ Are templates and outputs in assets/?
- ✅ Is token budget documented and reasonable?

## Recommended Token Budgets

### Small Knowledge Base
- **Skill metadata:** ~100 tokens
- **SKILL.md body:** ~1500-2000 tokens
- **Quick reference:** ~300-500 tokens
- **Total typical load:** ~2000-2500 tokens

### Medium Knowledge Base
- **Skill metadata:** ~100 tokens
- **SKILL.md body:** ~2500-3000 tokens
- **Quick reference:** ~500 tokens
- **Topic reference:** ~1500 tokens
- **Total typical load:** ~3000-4000 tokens

### Large Knowledge Base
- **Skill metadata:** ~100 tokens
- **SKILL.md body:** ~3000-4000 tokens
- **Quick reference:** ~500 tokens
- **Topic reference 1:** ~2000 tokens
- **Topic reference 2:** ~2000 tokens
- **Total typical load:** ~5000-8000 tokens
- **Strategy:** Load references selectively, not all at once

## Best Practices Summary

1. ✅ Write clear, specific descriptions with trigger keywords
2. ✅ Keep SKILL.md under 5000 words
3. ✅ Move detailed content to references/
4. ✅ Organize references by topic
5. ✅ Create quick reference files for frequent content
6. ✅ Put templates and outputs in assets/
7. ✅ Document token budgets
8. ✅ Test with real usage scenarios
9. ✅ Iterate based on actual loading behavior
10. ✅ Trust Claude to load appropriately when description is clear

## Version

**Version:** 1.0.0
**Last Updated:** 2025-11-07
