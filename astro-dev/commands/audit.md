---
name: audit
description: Manual code audit with configurable rigor (light/medium/comprehensive/auto)
---

# /audit Command

Direct validation via astro-auditor agent with adaptive rigor levels.

## Usage

```bash
/audit [level] [files]
/audit [files]  # Uses auto level detection
```

## Audit Levels

### Auto (Default)
Let the auditor determine appropriate level based on:
- File count and line changes
- Critical areas touched (auth, security, payments)
- Position in task series
- Risk assessment

### Light (~30 seconds, 5 checks)
Quick validation for small changes:
```bash
/audit light src/components/Button.astro
```
**Checks**: Syntax, imports, module paths, breaking changes, basic TypeScript

### Medium (~2 minutes, 20 checks)
Standard validation for features:
```bash
/audit medium src/pages/blog/
```
**Checks**: All light checks + security, performance, best practices

### Comprehensive (~5 minutes, 50+ checks)
Full validation for complex work:
```bash
/audit comprehensive src/
```
**Checks**: All medium checks + architecture, accessibility, documentation, SEO

## Examples

### Auto Level Detection
```bash
/audit src/components/Footer.astro
# Small file → Light audit

/audit src/pages/
# Multiple files → Medium audit

/audit src/pages/auth/
# Auth-related → Comprehensive audit
```

### Explicit Level
```bash
# Force light for quick check
/audit light src/components/*.astro

# Force comprehensive for critical areas
/audit comprehensive src/lib/auth.ts

# Medium for standard work
/audit medium src/pages/blog/[slug].astro
```

### Patterns
```bash
# All Astro components
/audit **/*.astro

# Specific directory
/audit src/components/

# Multiple files
/audit src/pages/index.astro src/layouts/Layout.astro
```

## Audit Level Details

### Light Audit (5 Checks)
**Use for**: Small fixes, quick validation, iterative work

✓ Syntax validation
✓ Import correctness (file extensions)
✓ Module resolution (astro:content)
✓ No build-breaking issues
✓ Basic TypeScript validity

**Output**: Brief pass/fail summary

### Medium Audit (20 Checks)
**Use for**: Standard features, most development work

**Priority 1** (Build-Breaking):
- Component structure
- Import extensions
- Module prefixes
- Dynamic route requirements
- Directive syntax

**Priority 2** (Critical):
- Security issues (XSS, exposed secrets)
- Performance problems (over-hydration)
- Common mistakes (className, await location)
- Error handling
- Basic accessibility

**Output**: Structured report with fixes

### Comprehensive Audit (50+ Checks)
**Use for**: Large features, critical areas, refactoring, final validation

**All Medium checks plus**:
- Full security scan
- Performance analysis (bundle size, optimization)
- Architecture review
- Complete accessibility audit
- Documentation completeness
- SEO compliance
- i18n readiness
- Dependency analysis

**Output**: Detailed report with recommendations

## Report Format

### Light Audit Output
```markdown
## Light Audit Results

✅ Syntax valid
✅ Imports correct
✅ Module paths correct
✅ No build-breaking issues
✅ TypeScript basics pass

Files reviewed: 1 | Issues: 0 | Time: 15s
```

### Medium/Comprehensive Output
```markdown
# Audit Report: Medium

## Summary
- Audit Level: medium
- Files reviewed: 3
- Critical issues: 1
- Warnings: 2
- Suggestions: 0

## Priority 1: Build-Breaking ❌

**File**: `src/pages/blog/[slug].astro`
**Line**: 5
**Issue**: Missing file extension in import
**Current**: `import Layout from '../layouts/Layout'`
**Fix**: `import Layout from '../layouts/Layout.astro'`

## Priority 2: Important ⚠️

**File**: `src/components/Hero.astro`
**Line**: 12
**Issue**: Using className instead of class
**Fix**: Change `<div className="hero">` to `<div class="hero">`

## ✅ Good Patterns
- Proper TypeScript typing
- Good error handling
```

## When Each Level is Auto-Selected

```python
auto_selection:
  if lines < 20 and files == 1:
    → light
  elif is_last_in_series:
    → comprehensive
  elif "auth" or "security" or "payment" in description:
    → comprehensive
  elif files > 5 or lines > 100:
    → comprehensive
  else:
    → medium
```

## Comparison with /develop

| Aspect | /audit | /develop |
|--------|--------|----------|
| **Focus** | Validation only | Full workflow |
| **Output** | Audit report | Implementation + validation |
| **When** | After changes | During development |
| **Agent** | astro-auditor | orchestrator coordinates |

## Integration Examples

### After /implement
```bash
/implement Create blog listing
# ... implementation happens ...
/audit medium src/pages/blog/  # Manual validation
```

### Series Work
```bash
# Task 1
/implement Add component A
/audit light  # Quick check

# Task 2
/implement Add component B
/audit light  # Quick check

# Final
/audit comprehensive src/components/  # Full validation
```

### Critical Areas
```bash
/implement Add authentication
/audit comprehensive src/lib/auth.ts  # Always thorough for security
```

## Optimization Features

**Skip Redundant Checks**:
- File audited <5 mins ago at same/higher level → Skip
- No changes since last audit → Skip
- Only whitespace changes → Skip

**Batch Similar Issues**:
- All import issues together
- All accessibility issues together
- All performance issues together

**Prioritize Blockers**:
- Build-breaking issues always shown first

## Common Issues by Priority

### Priority 1 (Build-Breaking)
```typescript
// Missing extensions
import Layout from './Layout'  // ❌
import Layout from './Layout.astro'  // ✅

// Wrong module prefix
import { getCollection } from 'astro/content'  // ❌
import { getCollection } from 'astro:content'  // ✅
```

### Priority 2 (Critical)
```astro
<!-- className vs class -->
<div className="container">  <!-- ❌ -->
<div class="container">  <!-- ✅ -->

<!-- Async location -->
<div>{await fetchData()}</div>  <!-- ❌ -->
---
const data = await fetchData();  // ✅
---
<div>{data}</div>
```

### Priority 3 (Suggestions)
- Add TypeScript types
- Improve error handling
- Enhance accessibility
- Add documentation

## Tips

**Choose Right Level**:
- Small change? Use light
- Standard work? Let auto decide (usually medium)
- Critical code? Force comprehensive

**Fix in Order**:
1. Priority 1 (blocks build)
2. Priority 2 (causes bugs)
3. Priority 3 (improves quality)

**Learn Patterns**:
- Note recurring issues
- Update team practices
- Document solutions

## Version

**Command Version**: 2.0 (Adaptive)
**Compatible with**: astro-dev plugin v2.0+
**Last Updated**: 2025-10-18

Use `/audit` for intelligent, adaptive code validation.
