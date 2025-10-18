---
name: audit
description: Manually trigger comprehensive code audit
---

# Audit Astro Code

Performs a comprehensive audit of Astro/Starlight code with prioritized feedback.

## Usage

```bash
/audit [file-pattern]
```

## Examples

```bash
# Audit all files
/audit

# Audit specific file
/audit src/pages/blog/[slug].astro

# Audit directory
/audit src/components/

# Audit by pattern
/audit **/*.astro
```

## Audit Scope

The audit checks for:

### Priority 1: Build-Breaking Issues ❌
Issues that will cause build failures:
- Missing file extensions in imports
- Wrong module prefixes (`astro/content` vs `astro:content`)
- Invalid component structure (frontmatter fences)
- Missing `getStaticPaths()` in dynamic routes
- Malformed directives

### Priority 2: Critical Issues ⚠️
Security, performance, and common bugs:
- **Security**: XSS risks, exposed secrets, unsafe HTML
- **Performance**: Over-hydration, missing optimizations
- **Common Bugs**: `className` vs `class`, param access errors, unsorted collections

### Priority 3: Best Practices 💡
Code quality improvements:
- TypeScript usage and type coverage
- Error handling patterns
- Accessibility (ARIA, semantic HTML)
- Code organization and reusability
- Documentation and comments

## Audit Report Structure

```markdown
# Audit Report

## Summary
- Files reviewed: 5
- Critical issues: 2
- Warnings: 4
- Suggestions: 3

## Priority 1: Critical ❌

### Missing File Extension
**File**: `src/pages/index.astro`
**Line**: 2
**Issue**: Import missing file extension
**Current**: `import Layout from '../layouts/Layout'`
**Fix**: `import Layout from '../layouts/Layout.astro'`

## Priority 2: Important ⚠️

### Over-Hydration
**File**: `src/components/PostList.astro`
**Line**: 15
**Issue**: Static content using client:load
**Current**: `<PostCard client:load post={post} />`
**Recommendation**: Remove client directive or use client:visible

## Priority 3: Suggestions 💡

### Accessibility Improvement
**File**: `src/components/Nav.astro`
**Suggestion**: Add ARIA labels
**Recommendation**: Add `aria-label` to navigation links

## ✅ Good Patterns Observed
- Consistent TypeScript usage
- Proper error handling
- Good component organization
```

## When to Use

### Manual Audit
- Before committing changes
- After major refactoring
- When debugging issues
- Code review preparation

### Auto-Audit
Auto-audit runs automatically after:
- File edits (via hooks)
- Component creation
- Configuration changes

## Audit Process

1. **File Discovery**: Identifies files to audit
2. **Priority 1 Scan**: Critical build-breaking issues
3. **Priority 2 Scan**: Security and performance
4. **Priority 3 Scan**: Best practices
5. **Report Generation**: Structured feedback with fixes

## Integration with Tools

### With astro-developer Skill
After `/implement`, audit provides:
- Verification of implementation
- Common mistake detection
- Best practice validation

### With astro-auditor Agent
For complex audits:
- Run agent in background
- Parallel audit processing
- Detailed analysis reports

### With Hooks
Automatic auditing:
- PostToolUse triggers
- Non-blocking execution
- Quick validation checks

## Audit Configuration

Audits check against:
- `${CLAUDE_PLUGIN_ROOT}/knowledge-base/common-mistakes/`
- `${CLAUDE_PLUGIN_ROOT}/knowledge-base/best-practices/`
- `${CLAUDE_PLUGIN_ROOT}/knowledge-base/audit/`

## Common Issues Detected

### Import Issues
```typescript
// ❌ Missing extension
import Layout from './Layout'
// ✅ With extension
import Layout from './Layout.astro'

// ❌ Wrong prefix
import { getCollection } from 'astro/content'
// ✅ Correct prefix
import { getCollection } from 'astro:content'
```

### Component Issues
```astro
// ❌ Using className
<div className="container">
// ✅ Using class
<div class="container">

// ❌ Await in template
<div>{await fetchData()}</div>
// ✅ Fetch in frontmatter
---
const data = await fetchData();
---
<div>{data}</div>
```

### Route Issues
```typescript
// ❌ Accessing params in getStaticPaths
export async function getStaticPaths() {
  const { slug } = Astro.params; // Error!
}

// ✅ Using params from props
const { slug } = Astro.props;
```

## Quick Fixes

The audit provides actionable fixes:
- Exact code replacements
- Line number references
- Before/after examples
- Explanation of why

## Continuous Improvement

Audit results help:
- Update knowledge base
- Identify common patterns
- Improve team practices
- Document solutions

## Tips

1. **Run Early**: Audit before issues compound
2. **Fix Priority 1 First**: Build-breaking issues block progress
3. **Learn Patterns**: Note repeated issues
4. **Update Docs**: Document team-specific patterns
5. **Automate**: Let hooks handle routine checks
