---
name: astro-developer
description: Expert Astro/Starlight developer for implementing features, writing components, fixing bugs, and configuring projects. Use for all code implementation tasks in Astro projects, including components, pages, layouts, content collections, and configuration.
---

# Astro Developer Skill

This skill provides expert Astro/Starlight development capabilities with deep knowledge of best practices and common pitfalls.

## Core Capabilities

- **Component Development**: Write .astro components with proper syntax and directives
- **Page & Routing**: Implement dynamic routes with getStaticPaths
- **Content Collections**: Create and query collections with proper schemas
- **Configuration**: Modify astro.config.mjs and TypeScript configs
- **Bug Fixes**: Diagnose and fix common Astro errors

## Knowledge Base Access

When implementing, reference these knowledge files as needed:

### Syntax References
Access via `${CLAUDE_PLUGIN_ROOT}/knowledge-base/astro-syntax/`:
- `component-structure.md`: Component anatomy, frontmatter, templates
- `directives.md`: All client:*, is:*, set:* directives
- `imports.md`: Import patterns with required file extensions
- `routing.md`: Dynamic routes, getStaticPaths patterns
- `configuration.md`: Astro and Starlight config options

### Best Practices
Access via `${CLAUDE_PLUGIN_ROOT}/knowledge-base/best-practices/`:
- `common-mistakes.md`: Cataloged errors and fixes
- `typescript-patterns.md`: Type safety requirements
- `performance.md`: Hydration and optimization patterns
- `starlight-patterns.md`: Starlight-specific best practices

## Implementation Protocol

### Before Writing Code
1. Check `${CLAUDE_PLUGIN_ROOT}/knowledge-base/common-mistakes/` for known pitfalls
2. Review similar patterns in the project
3. Verify TypeScript strict mode requirements

### Critical Rules

**ALWAYS**:
- Include file extensions in imports (.astro, .ts, .tsx, .js, .jsx)
- Use `astro:content` not `astro/content`
- Type all Props interfaces
- Fetch data in frontmatter, not templates
- Sort collections when order matters
- Check entry existence before use

**NEVER**:
- Access Astro.params inside getStaticPaths()
- Use await in templates
- Expose server secrets to client
- Over-hydrate static content
- Use className (use class instead)

### Quick Reference

#### Component Template
```typescript
---
import type { Props } from './types';
import Layout from '../layouts/Layout.astro'; // ✅ Extension

export interface Props {
  title: string;
  showDate?: boolean;
}

const { title, showDate = true } = Astro.props;
// Fetch data here, not in template
---

<Layout title={title}>
  <!-- Template here, no await -->
</Layout>
```

#### Dynamic Route Template
```typescript
---
import { getCollection } from 'astro:content'; // ✅ astro: prefix

export async function getStaticPaths() {
  const posts = await getCollection('blog');

  // ✅ Sort collections
  const sorted = posts.sort((a, b) =>
    b.data.date.valueOf() - a.data.date.valueOf()
  );

  return sorted.map(post => ({
    params: { slug: post.id },
    props: { post }
  }));
}

const { post } = Astro.props; // ✅ From props, not params

if (!post) {
  return Astro.redirect('/404'); // ✅ Handle missing
}
---
```

## Working with Other Components

- **For API verification**: Request docs lookup with `/docs-lookup` command
- **For architecture planning**: Invoke @astro-architect agent
- **After implementation**: Auto-audit hook will check your code

## Error Handling Patterns

Always implement proper error boundaries:

```typescript
try {
  const data = await fetchAPI();
  // process data
} catch (error) {
  console.error('API fetch failed:', error);
  // graceful fallback
}
```

## Testing Checklist

Before considering implementation complete:
- [ ] All imports have extensions
- [ ] TypeScript types defined
- [ ] Collections sorted if needed
- [ ] Error handling in place
- [ ] No server secrets exposed
- [ ] Accessibility considered
- [ ] Component uses `class` not `className`
- [ ] Correct module prefix (`astro:content`)
