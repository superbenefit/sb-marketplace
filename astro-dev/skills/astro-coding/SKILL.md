---
name: astro-coding
description: Smart context provider for Astro/Starlight code implementation. Provides patterns, best practices, and critical rules to agents performing coding tasks.
---

# astro-coding Skill

This skill provides smart, context-aware implementation patterns for Astro and Starlight development. It injects relevant coding knowledge to agents based on task analysis.

## Purpose

The astro-coding skill is a **capability provider** that enhances agents with Astro-specific coding knowledge. It does not implement code itself - instead, it provides the patterns and rules that agents (primarily astro-developer) use when writing code.

## Loading Strategy

This skill uses **selective loading** based on task detection:

1. **Task Keyword Analysis**: Detects what type of code is being written
2. **File Extension Detection**: Identifies target file types  
3. **Import Statement Scanning**: Recognizes required patterns
4. **Pattern Matching**: Loads only relevant sections

## Usage by Agents

- **astro-developer** (Primary): Loads relevant patterns for implementation
- **astro-architect**: Uses for code examples in designs
- **astro-auditor**: References when suggesting fixes
- **astro-orchestrator**: Determines which sections to load

## Critical Rules (Always Loaded)

These rules apply to ALL Astro/Starlight code:

### 1. File Extensions in Imports (MANDATORY)
\`\`\`typescript
// ✅ CORRECT
import Header from './Header.astro';
import { formatDate } from '../utils/dates.ts';

// ❌ WRONG - Will cause build errors
import Header from './Header';
\`\`\`

### 2. Module Prefix (MANDATORY)
\`\`\`typescript
// ✅ CORRECT
import { getCollection } from 'astro:content';

// ❌ WRONG
import { getCollection } from 'astro/content';
\`\`\`

### 3. Class Attribute (MANDATORY)
\`\`\`astro
<!-- ✅ CORRECT -->
<div class="container">

<!-- ❌ WRONG -->
<div className="container">
\`\`\`

### 4. Async Operations Location (MANDATORY)
\`\`\`astro
---
// ✅ CORRECT: Await in frontmatter
const posts = await getCollection('blog');
---
<ul>{posts.map(post => <li>{post.data.title}</li>)}</ul>
\`\`\`

### 5. Environment Variables Security (MANDATORY)
\`\`\`typescript
// ✅ CORRECT: Server-side only for secrets
const apiKey = import.meta.env.SECRET_API_KEY;

// ❌ WRONG: PUBLIC_ exposes to client
const apiKey = import.meta.env.PUBLIC_API_KEY;
\`\`\`

## Quick Reference Templates

### Basic Component
\`\`\`astro
---
interface Props {
  title: string;
  description?: string;
}

const { title, description } = Astro.props;
---

<div class="component">
  <h2>{title}</h2>
  {description && <p>{description}</p>}
</div>
\`\`\`

### Dynamic Route
\`\`\`astro
---
import { getCollection } from 'astro:content';
import type { CollectionEntry } from 'astro:content';

export async function getStaticPaths() {
  const posts = await getCollection('blog');
  return posts.map(post => ({
    params: { slug: post.slug },
    props: { post },
  }));
}

interface Props {
  post: CollectionEntry<'blog'>;
}

const { post } = Astro.props;
const { Content } = await post.render();
---

<article>
  <h1>{post.data.title}</h1>
  <Content />
</article>
\`\`\`

## Knowledge Base Integration

Reference comprehensive knowledge base for detailed patterns:
- \`\${CLAUDE_PLUGIN_ROOT}/knowledge-base/astro-syntax/*\` - Syntax details
- \`\${CLAUDE_PLUGIN_ROOT}/knowledge-base/common-mistakes/*\` - Error catalog
- \`\${CLAUDE_PLUGIN_ROOT}/knowledge-base/best-practices/*\` - Standards

## Token Optimization

**Light context** (simple tasks): Critical rules + quick templates (~200 tokens)
**Medium context** (standard tasks): Relevant pattern + common mistakes (~400 tokens)
**Full context** (complex tasks): Multiple patterns + full knowledge base (~800 tokens)

## Version

**Skill Version**: 2.0 (Smart Loading)
**Last Updated**: 2025-10-18
