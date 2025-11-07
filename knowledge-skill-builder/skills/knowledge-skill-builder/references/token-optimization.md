# Token Optimization for Skills

Best practices for creating token-efficient skills that load quickly and use context effectively.

## Why Token Optimization Matters

**Performance:**
- Faster skill loading
- Quicker response times
- Better user experience

**Cost:**
- Tokens consume API quota
- Efficient skills cost less to run
- Matters at scale

**Context Management:**
- Leave room for actual work
- Avoid hitting context limits
- Better multi-skill scenarios

## Token Estimation

### Quick Estimates

**Rule of thumb:**
- 1 word ≈ 1.3 tokens (English)
- 100 words ≈ 130 tokens
- 1000 words ≈ 1300 tokens

**Markdown overhead:**
- Headers, lists, code blocks add ~10-20% overhead
- YAML frontmatter: ~20-40 tokens typically

**Measuring actual tokens:**
Use Claude or token counting tools for precise measurements.

### Common File Sizes

| Content Type | Words | Tokens (est.) |
|--------------|-------|---------------|
| Skill metadata | 20-40 | ~50-100 |
| Quick reference | 300-400 | ~400-600 |
| Standard guide | 1000-1500 | ~1300-2000 |
| Comprehensive doc | 3000-4000 | ~4000-5500 |
| Large knowledge base | 10000+ | ~13000+ |

## Progressive Disclosure Strategy

Load content in layers, from minimal to comprehensive as needed.

### Layer 1: Metadata Only (~50-100 tokens)

**Always loaded:** At session startup for skill discovery

```yaml
---
name: dao-knowledge
description: Search DAO governance documentation covering voting, treasury, and organizational primitives. Use when asked about DAOs or decentralized governance.
---
```

**Optimization:**
- Keep description under 500 characters
- Include essential keywords only
- Be specific, not verbose

### Layer 2: SKILL.md Body (~2000-4000 tokens)

**Loaded when:** Skill is triggered by relevant task

**Content:**
- Core capabilities overview
- Brief usage patterns
- Workflow descriptions
- References to detailed content

**Optimization:**
- Target 2500-3500 words
- Summarize, don't explain everything
- Point to references for details
- Use tables and lists (more concise than paragraphs)

### Layer 3: References (~500-2000 tokens each)

**Loaded when:** Specific topic or detail needed

**Content:**
- Topic-specific guides
- Detailed examples
- API documentation
- Pattern libraries

**Optimization:**
- One topic per file
- Keep frequently-used refs small (~500 words)
- Larger refs for rare deep-dives (~2000 words)
- Cross-reference instead of duplicating

### Layer 4: Assets (0 tokens)

**Never loaded:** Files used without context

**Content:**
- Templates for users to fill out
- Configuration examples
- Schemas for validation
- Media files

**Optimization:**
- Move anything that's used as-is (not read for understanding)
- Blank templates always go here
- Configuration examples go here

## Consolidation Strategies

### Before: Redundant Content

```
knowledge-base/
├── voting-intro.md        (500 words, overview)
├── voting-detailed.md     (2000 words, includes same overview)
├── voting-examples.md     (1000 words, includes same overview)
├── treasury-intro.md      (500 words, overview)
├── treasury-detailed.md   (2000 words, includes same overview)
└── treasury-examples.md   (1000 words, includes same overview)

Total: 7000 words, ~30% redundancy
```

### After: Consolidated

```
references/
├── quick-reference.md     (800 words, all overviews + common patterns)
├── voting-guide.md        (1500 words, detailed unique content)
├── treasury-guide.md      (1500 words, detailed unique content)
└── examples.md            (1000 words, examples for all topics)

Total: 4800 words, 0% redundancy (~32% reduction)
```

**Benefits:**
- Eliminated redundant overviews
- Combined all examples into one file
- Easier to maintain
- Faster loading

### Cross-Referencing

Instead of duplicating, reference:

**Before:**
```markdown
# voting-guide.md
## Treasury Integration
[2000 words explaining treasury...]

# treasury-guide.md
## Voting Integration
[2000 words explaining voting...]
```

**After:**
```markdown
# voting-guide.md
## Treasury Integration
Votes can trigger treasury operations. See `treasury-guide.md` for details on treasury management.

# treasury-guide.md
## Voting Integration
Treasury proposals require voting approval. See `voting-guide.md` for voting mechanisms.
```

## File Organization Patterns

### Pattern 1: Quick Reference + Topic Guides

**Best for:** Medium-sized knowledge bases

```
references/
├── quick-reference.md       (~500 tokens - common patterns)
├── topic-a-guide.md         (~1500 tokens - deep dive)
├── topic-b-guide.md         (~1500 tokens - deep dive)
└── examples.md              (~1000 tokens - real examples)
```

**Loading:**
- quick-reference.md loads frequently (~500 tokens)
- Topic guides load when that topic needed (~1500 tokens)
- Examples load when requested (~1000 tokens)

### Pattern 2: Tiered Depth

**Best for:** Large knowledge bases with varying detail needs

```
references/
├── overview.md              (~300 tokens - high-level map)
├── topic-a-quick.md         (~400 tokens - essentials)
├── topic-a-deep.md          (~2000 tokens - comprehensive)
├── topic-b-quick.md         (~400 tokens - essentials)
└── topic-b-deep.md          (~2000 tokens - comprehensive)
```

**Loading:**
- overview.md loads first (300 tokens)
- Quick guides for rapid lookup (400 tokens)
- Deep guides only when needed (2000 tokens)

### Pattern 3: Consolidated Single File

**Best for:** Small, cohesive knowledge bases

```
references/
└── complete-guide.md        (~2000 tokens - everything)
```

**Loading:**
- One file, complete context
- Only works if total <3000 words
- Better than splitting artificially

## Content Reduction Techniques

### Use Tables Instead of Prose

**Before (verbose):**
```markdown
The quorum requirement is calculated by taking the total number of tokens
and multiplying by the quorum percentage, then dividing by 100. The voting
power is calculated by taking the token balance and multiplying it by the
time held multiplier.
```

**After (concise table):**
```markdown
| Calculation | Formula |
|-------------|---------|
| Quorum | `(total_tokens * quorum_pct) / 100` |
| Voting Power | `token_balance * time_multiplier` |
```

**Savings:** ~60% fewer tokens for same information

### Use Code Blocks Instead of Explanation

**Before:**
```markdown
First, you import the getCollection function from astro:content. Then you
call it with the collection name to get all entries. Finally, you can filter
the results using the second parameter to only get entries where draft is
not true.
```

**After:**
```typescript
import { getCollection } from 'astro:content';

const published = await getCollection('blog', ({ data }) =>
  data.draft !== true
);
```

**Savings:** ~50% fewer tokens, clearer meaning

### Use Lists Instead of Paragraphs

**Before:**
```markdown
The skill can search using full-text search across all markdown files. It
can also search using tags that are defined in the frontmatter or hashtags
in the content. Additionally, it can follow wikilinks to navigate between
related documents.
```

**After:**
```markdown
Search strategies:
- Full-text across markdown files
- Tags from frontmatter or hashtags
- Wikilinks for related documents
```

**Savings:** ~40% fewer tokens

### Remove Fluff Words

**Before:**
```markdown
In order to ensure that the skill works correctly, it is very important
that you should make sure to validate the structure before you proceed
with packaging. This helps to identify any potential issues.
```

**After:**
```markdown
Validate structure before packaging to identify issues early.
```

**Savings:** ~75% fewer tokens

## Example Optimization: Before and After

### Before: Unoptimized Skill

```yaml
---
name: dao-knowledge
description: This skill helps users by searching through and retrieving knowledge from documentation about DAO governance.
---

# DAO Knowledge Skill

## Introduction

This is a skill designed to help users find information about DAOs.
It provides capabilities for searching, retrieving, and understanding
decentralized governance concepts.

## What Are DAOs?

DAOs are decentralized autonomous organizations that operate on blockchain
technology. They use smart contracts to encode rules and enable collective
decision-making without centralized authority. [500 more words...]

## How This Skill Works

When you ask a question about DAOs, this skill will search through the
knowledge base to find relevant information. It will then read the
documents and extract the key points... [300 more words...]

## Search Capabilities

The skill can perform full-text search. This means it looks through all
the words in all the documents to find matches. It can also use tags...
[400 more words...]

[Continues for 5000 more words with examples, detailed explanations, etc.]
```

**Estimated tokens:** ~8000 tokens for SKILL.md alone

### After: Optimized Skill

```yaml
---
name: dao-knowledge
description: Search DAO governance documentation covering voting mechanisms, treasury management, and organizational primitives. Use when asked about DAOs or decentralized governance.
---

# DAO Knowledge

Search and retrieve knowledge from DAO governance documentation.

## Core Capabilities

1. **Search Knowledge Base**
   - Full-text search across markdown files
   - Tag-based filtering
   - Wikilink navigation

2. **Parse Content**
   - Extract information from multiple sources
   - Synthesize across documents
   - Cite sources properly

3. **Navigate Knowledge Graph**
   - Follow backlinks and forward links
   - Traverse tag relationships
   - Suggest related topics

## Usage Patterns

### Direct Question
User asks about governance → Search knowledge base → Synthesize answer → Cite sources

### Topic Exploration
User requests topic overview → Find main docs → Map relationships → Present structure

See `references/search-patterns.md` for detailed strategies.
See `references/governance-guide.md` for DAO governance details.

## Token Budget

| Operation | Tokens | Strategy |
|-----------|--------|----------|
| Metadata | ~100 | Always loaded |
| SKILL.md | ~1000 | Loaded when triggered |
| Quick ref | ~500 | Loaded frequently |
| Topic guide | ~1500 | Loaded as needed |
```

**Estimated tokens:** ~1000 tokens for SKILL.md + selective reference loading

**Improvements:**
- SKILL.md reduced from 8000 to 1000 tokens (87% reduction)
- Moved DAO intro to `references/dao-overview.md`
- Moved detailed search strategies to `references/search-patterns.md`
- Moved governance details to `references/governance-guide.md`
- Used tables and lists for conciseness
- Removed fluff and repetition

## Measuring and Testing

### Before Publishing

1. **Count words:** Target <3500 words for SKILL.md
2. **Estimate tokens:** words * 1.3 + overhead
3. **Check references:** Each should have clear purpose and token budget
4. **Test loading:** Verify only necessary content loads

### After Publishing

1. **Monitor actual usage:** Which references load most often?
2. **Identify patterns:** What content is rarely accessed?
3. **Refactor:** Move frequent content to smaller files
4. **Consolidate:** Merge rarely-used content into comprehensive guides

## Common Optimization Wins

### 1. Extract Examples to Separate File

**Impact:** ~1000-2000 token reduction in SKILL.md

**Before:** 10 detailed examples in SKILL.md
**After:** Brief examples in SKILL.md, comprehensive examples in `references/examples.md`

### 2. Create Quick Reference

**Impact:** 70% fewer tokens for frequent lookups

**Before:** Load full 3000-token guide each time
**After:** Load 500-token quick reference for most queries, full guide rarely

### 3. Move Templates to Assets

**Impact:** ~500-1000 tokens saved per template

**Before:** Template in references/, loaded to context
**After:** Template in assets/, provided without loading

### 4. Consolidate Redundant Content

**Impact:** 20-40% overall reduction

**Before:** Same concepts explained in multiple files
**After:** Explain once, cross-reference elsewhere

### 5. Use Markdown Efficiently

**Impact:** 30-50% reduction in content size

**Before:** Long paragraphs of explanation
**After:** Tables, code blocks, lists

## Anti-Patterns

### ❌ Embedding Full API Docs

```markdown
## Complete API Reference

[10,000 words of API documentation copied verbatim]
```

**Fix:** Summary in SKILL.md, full docs in `references/api.md`, use MCP for real-time lookup

### ❌ Repeating Critical Rules

```markdown
# SKILL.md
CRITICAL RULE 1: Always validate input
[300 words explaining why]

# references/validation-guide.md
CRITICAL RULE 1: Always validate input
[Same 300 words repeated]
```

**Fix:** State once in SKILL.md, reference from guide

### ❌ Prose When Code Would Work

```markdown
To create a proposal, first initialize a proposal object with the
title, description, and voting options. Then set the voting period...
[500 words of explanation]
```

**Fix:**
```typescript
const proposal = {
  title: "Add new feature",
  description: "Proposal to implement X",
  votingPeriod: 7 * 24 * 60 * 60, // 7 days in seconds
  options: ["approve", "reject"]
};
```

## Token Budget Template

Include this in your SKILL.md to document optimization:

```markdown
## Token Budget

| Operation | Estimated Tokens | Loading Strategy |
|-----------|------------------|------------------|
| Skill metadata | ~100 | Always loaded at startup |
| SKILL.md body | ~2500 | Loaded when skill triggered |
| Quick reference | ~500 | Loaded for most operations |
| Detailed guide (topic A) | ~1500 | Loaded when topic A needed |
| Detailed guide (topic B) | ~1500 | Loaded when topic B needed |
| Comprehensive examples | ~2000 | Loaded rarely, on request |
| **Total (typical operation)** | **~3000-4000** | Metadata + SKILL.md + quick ref |
| **Total (deep dive)** | **~5000-7000** | Add 1-2 detailed guides |
```

## Checklist

Before finalizing skill, verify:

- ✅ SKILL.md is under 3500 words
- ✅ Frequently-used content is in small files (<500 words)
- ✅ Detailed content is in topic-specific references
- ✅ Templates and outputs are in assets/ (not references/)
- ✅ No redundant content across files
- ✅ Tables and code blocks used instead of prose where possible
- ✅ Token budget is documented
- ✅ Cross-references are used instead of duplication
- ✅ Actual token counts measured (not just estimated)

## Version

**Version:** 1.0.0
**Last Updated:** 2025-11-07
