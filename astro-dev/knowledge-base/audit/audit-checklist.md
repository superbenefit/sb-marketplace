# Code Audit Checklist

This document provides a prioritized checklist for auditing code changes. Use this as the master checklist when reviewing implementations.

## How to Use This Checklist

1. **Start with Priority 1** (Critical) - These will break builds or cause runtime errors
2. **Move to Priority 2** (Important) - Common bugs, security risks, performance issues
3. **Finish with Priority 3** (Best Practices) - Code quality improvements

## Priority 1: Critical Issues

These issues will cause build failures, runtime errors, or broken functionality.

### Astro Syntax
- [ ] Component has `---` code fences (frontmatter/template separation)
- [ ] Template section is below code fence
- [ ] No code outside frontmatter section
- [ ] No `await` in template section (must be in frontmatter)

### Imports
- [ ] All relative imports include file extensions
- [ ] Using `astro:` prefix (not `astro/`) for built-ins
- [ ] Glob patterns are string literals (not variables)
- [ ] Glob patterns start with `./`, `../`, or `/`

### Routing
- [ ] `getStaticPaths()` exported for dynamic routes (static mode)
- [ ] `getStaticPaths()` returns array of objects with `params`
- [ ] `params` is an object (not primitive)
- [ ] Only ONE rest parameter per route

### Directives
- [ ] `client:media` has required media query value
- [ ] `client:only` has required framework hint
- [ ] No imports in `is:inline` scripts
- [ ] Directives visible (not in spread attributes)

### Configuration
- [ ] `output: 'server'` has `adapter` configured
- [ ] `site` uses `http://` or `https://` protocol
- [ ] `i18n.defaultLocale` is in `locales` array
- [ ] `env` fields have required `context` and `access`

### TypeScript
- [ ] Function parameters are typed
- [ ] No unsafe double assertions (`as unknown as Type`)
- [ ] Props interfaces defined for components

## Priority 2: Important Issues

These issues cause common bugs, security vulnerabilities, or performance problems.

### Security
- [ ] No `set:html` with user input (use `set:text`)
- [ ] No exposed secrets in client code
- [ ] No hard-coded API keys
- [ ] User input validated and sanitized

### Performance
- [ ] Images have width/height attributes
- [ ] Heavy components use lazy loading (`client:visible`)
- [ ] Not importing entire libraries (use specific imports)
- [ ] No unnecessary hydration (avoid `client:load` on static content)

### Astro Patterns
- [ ] Using `class` not `className` for HTML attributes
- [ ] No event handlers on static HTML elements
- [ ] Framework components have `client:*` directive if interactive
- [ ] Collection entries checked for existence before use
- [ ] Collections sorted if order matters
- [ ] Using `render()` for markdown content

### Props & Parameters
- [ ] Props accessed via `Astro.props` (not global)
- [ ] NOT accessing `Astro.params` inside `getStaticPaths()`
- [ ] Default values provided for optional props
- [ ] No functions/complex objects passed to hydrated components

### Error Handling
- [ ] API calls wrapped in try/catch
- [ ] Null checks for potentially undefined values
- [ ] Graceful fallbacks for failures
- [ ] User-friendly error messages (not stack traces)

### TypeScript
- [ ] No `any` types (or justified with comment)
- [ ] Using `unknown` instead of `any` for uncertain types
- [ ] Type-only imports (`import type`) for types
- [ ] Return types specified for public functions

### Accessibility
- [ ] Images have meaningful `alt` text
- [ ] Form inputs have associated labels
- [ ] Interactive elements are keyboard accessible
- [ ] Semantic HTML elements used appropriately

## Priority 3: Best Practices

These improve code quality, maintainability, and optimization.

### Code Organization
- [ ] Functions are focused (single responsibility)
- [ ] Function length reasonable (~50 lines max)
- [ ] Descriptive variable/function names
- [ ] Boolean variables use `is`/`has`/`should`/`can` prefix

### TypeScript Quality
- [ ] Using utility types where applicable (`Partial`, `Pick`, etc.)
- [ ] Type guards for narrowing
- [ ] Discriminated unions for variants
- [ ] Generic constraints where appropriate

### Import Organization
- [ ] Imports follow logical order (built-ins, packages, local)
- [ ] No unused imports
- [ ] Consistent use of path aliases (if configured)

### Comments
- [ ] Comments explain "why" not "what"
- [ ] Complex logic has explanatory comments
- [ ] No commented-out code (use version control)
- [ ] Public APIs have JSDoc comments

### CSS
- [ ] Styles scoped to components
- [ ] No `!important` (indicates specificity issues)
- [ ] Efficient selectors (not overly specific)
- [ ] Responsive design considerations

### Accessibility
- [ ] Color contrast meets WCAG AA (4.5:1 normal, 3:1 large text)
- [ ] ARIA attributes used appropriately (not redundant)
- [ ] Focus indicators visible
- [ ] Touch targets sufficient size (44x44px minimum)

### Performance
- [ ] Images lazy-loaded (`loading="lazy"`) when below fold
- [ ] Code split by route
- [ ] Critical CSS inlined
- [ ] Modern image formats (WebP/AVIF)

## Audit Workflow

### 1. Initial Review
Start with file structure and imports:
- [ ] Read all changed files
- [ ] Check file locations and naming
- [ ] Verify imports syntax

### 2. Astro-Specific Checks
Reference `.claude/astro-knowledge/`:
- [ ] Check syntax against `astro-syntax-reference.md`
- [ ] Verify directives against `astro-directives-reference.md`
- [ ] Validate routing against `astro-routing-reference.md`
- [ ] Check imports against `astro-imports-reference.md`
- [ ] Verify config against `astro-configuration-reference.md`

### 3. Common Mistakes
Reference `.claude/developer-knowledge/common-mistakes.md`:
- [ ] Check against cataloged error patterns
- [ ] Verify fixes match recommendations

### 4. Code Quality
Reference `.claude/auditor-knowledge/`:
- [ ] Apply `code-quality-standards.md` checks
- [ ] Apply `typescript-standards.md` checks

### 5. Report Findings
Organize findings by priority:
```markdown
## Priority 1: Critical Issues
- [File:Line] Issue description and fix

## Priority 2: Important Issues
- [File:Line] Issue description and fix

## Priority 3: Suggestions
- [File:Line] Improvement suggestion
```

## Issue Reporting Format

For each issue found, report:

```markdown
**[Priority Level] Issue Type**
- **File**: `path/to/file.astro:42`
- **Issue**: Clear description of what's wrong
- **Why**: Why this is a problem
- **Fix**: How to fix it (with code example if helpful)
```

### Example Report

```markdown
**[Priority 1] Missing getStaticPaths**
- **File**: `src/pages/blog/[slug].astro:1`
- **Issue**: Dynamic route without `getStaticPaths()` export
- **Why**: In static mode, dynamic routes require `getStaticPaths()` to generate all route paths at build time
- **Fix**: Add `export async function getStaticPaths()` to frontmatter:
  ```typescript
  export async function getStaticPaths() {
    const posts = await getCollection('blog');
    return posts.map(post => ({
      params: { slug: post.id },
      props: { post }
    }));
  }
  ```

**[Priority 2] Missing alt text**
- **File**: `src/components/Hero.astro:15`
- **Issue**: `<img>` tag without `alt` attribute
- **Why**: Screen readers can't describe image to visually impaired users
- **Fix**: Add descriptive alt text: `<img src={hero} alt="Team collaboration on project planning" />`
```

## Quick Reference

### Most Common Issues

1. Missing file extensions in imports
2. Using `className` instead of `class`
3. Missing `getStaticPaths()` for dynamic routes
4. Event handlers on static HTML elements
5. No type definitions for props
6. Missing collection entry existence checks
7. Over-hydration (`client:load` on static content)
8. Exposed secrets in client code
9. Missing alt text on images
10. No error handling for API calls

### Files to Always Check

- `astro.config.mjs` - Configuration validity
- `src/content.config.ts` - Schema definitions
- `[...slug].astro` - Dynamic route patterns
- Any `client:*` directives - Hydration necessity
- Environment variable usage - Secret exposure
- Image elements - Optimization and accessibility

### Red Flags

These patterns almost always indicate problems:

- `any` type without justification
- `as unknown as` double assertion
- `innerHTML` with dynamic content
- `dangerouslySetInnerHTML` equivalent
- Hard-coded credentials
- No error handling around fetch
- Missing null checks
- `!important` in CSS
- Overly deep CSS nesting
- `@ts-ignore` without comment
