---
name: dev
description: Main development command for Astro/Starlight projects - implements features, fixes bugs, creates components
---

# /dev Command

The primary development command for Astro and Starlight projects. Handles everything from simple components to complex features with intelligent validation.

## Usage

```
/dev [description of what to build]
/dev [description] --audit=off          # Skip validation
/dev [description] --audit=light        # Quick validation (5 checks)
/dev [description] --audit=comprehensive # Full validation (50+ checks)
```

## Description

The `/dev` command loads the astro-coding skill (best practices, patterns, critical rules) and implements your request. It automatically validates code based on task complexity, or you can control validation with the `--audit` flag.

## What It Does

1. **Understands Your Request**: Analyzes what needs to be built
2. **Loads Relevant Patterns**: Brings in only the patterns you need (components, routes, collections, etc.)
3. **Implements Code**: Writes clean, standards-compliant Astro/Starlight code
4. **Validates**: Checks against critical rules and best practices
5. **Returns Result**: Complete implementation ready to use

## Examples

### Create a Component
```
/dev Add a Footer component with social links and copyright
```
**Result**: Footer.astro with proper TypeScript types, accessibility, and styling

### Build a Feature
```
/dev Add a blog with categories and pagination
```
**Result**: Content collection, dynamic routes, category pages, pagination component

### Fix Issues
```
/dev Fix all TypeScript errors in the components folder
```
**Result**: All type errors resolved following Astro best practices

### Complex Implementation
```
/dev Create a multi-language content system with external data integration
```
**Result**: Custom loaders, i18n routing, data transformation, full implementation

### Configuration
```
/dev Add Tailwind CSS integration to the project
```
**Result**: Updated astro.config with Tailwind, installed packages, example styles

## Auto-Validation

By default, `/dev` validates your code automatically:

| Task Size | Files Changed | Default Validation |
|-----------|---------------|-------------------|
| **Small** | 1 file, <20 lines | Light (5 critical checks) |
| **Medium** | 2-5 files, <100 lines | Medium (20 checks) |
| **Large** | >5 files or >100 lines | Comprehensive (50+ checks) |
| **Security** | Auth, payments, secrets | Always comprehensive |

### Override Validation

```bash
# Skip validation for quick experiments
/dev Add a test component --audit=off

# Force full validation for critical code
/dev Update API endpoint --audit=comprehensive

# Light validation for simple changes
/dev Fix typo in header --audit=light
```

## What Gets Loaded

The astro-coding skill loads patterns based on your request:

**Always loaded** (~100 tokens):
- Critical rules (extensions, module paths, async/await, security)

**Context-loaded** (~400 tokens):
- Component patterns → for component tasks
- Routing patterns → for pages/routes
- Collection patterns → for content collections
- Config patterns → for configuration changes
- Starlight patterns → when working with Starlight

**On-demand** (~800 tokens):
- Deep dive references for complex integrations
- Custom loader documentation
- Advanced architecture patterns

## Critical Rules (Always Applied)

Every implementation follows these rules:

1. ✅ **File extensions in imports**: `import './Header.astro'` not `import './Header'`
2. ✅ **Correct module paths**: `'astro:content'` not `'astro/content'`
3. ✅ **Use `class` not `className`** in .astro files
4. ✅ **Await in frontmatter only**, not in templates
5. ✅ **Never expose secrets** to client code
6. ✅ **Type all Props interfaces** with TypeScript
7. ✅ **Define getStaticPaths()** for dynamic routes

## Tips for Best Results

### Be Specific
```
❌ /dev make a blog
✅ /dev Create a blog collection with title, date, author, tags, and draft status
```

### Mention Constraints
```
✅ /dev Add authentication (using existing Supabase setup)
✅ /dev Create footer (must match existing header style)
```

### Batch Related Work
```
✅ /dev Add blog with categories, tags, RSS feed, and author pages
```
All parts will be implemented together efficiently.

### Reference Existing Code
```
✅ /dev Add pagination to blog (like the docs pagination)
✅ /dev Create Card component (similar to existing Button style)
```

## When to Use Other Commands

- **`/lookup [query]`** → Quick API reference lookup
  ```
  /lookup getCollection
  /lookup client directives
  /lookup getStaticPaths
  ```

- **`/design [system]`** → Architecture planning for complex systems
  ```
  /design multi-tenant content system with GitBook integration
  ```

## Output Format

```markdown
## Implementation Complete

### Files Created/Modified
- src/components/Footer.astro (created)
- src/pages/blog/[slug].astro (modified)
- src/content/config.ts (modified)

### Changes Made
[Clear description of what was implemented]

### Validation Results
✅ All imports have extensions
✅ TypeScript types defined correctly
✅ No security issues
✅ Performance optimized
✅ Accessibility considered

**Validation Level**: Medium (20 checks passed)

### Usage Example
\`\`\`astro
import Footer from '../components/Footer.astro';

<Footer />
\`\`\`

Ready to use! Test by running `npm run dev`
```

## Common Patterns

### Component with Props
```
/dev Create a Card component with title, description, image, and link props
```

### Dynamic Route
```
/dev Add dynamic route for blog posts with proper TypeScript types
```

### Content Collection
```
/dev Set up a docs collection with frontmatter validation
```

### API Endpoint
```
/dev Create API endpoint at /api/posts that returns published blog posts
```

### Configuration
```
/dev Add React integration and configure for client components
```

### Refactoring
```
/dev Refactor Header component to use Astro props instead of slots
```

## Troubleshooting

### If you get import errors:
Check that file extensions are included: `./Component.astro` not `./Component`

### If TypeScript complains:
Make sure Props interfaces are defined for all components

### If hydration doesn't work:
Verify client directives: `client:load`, `client:visible`, `client:idle`

### If collections fail:
Ensure `src/content/config.ts` exports collections and schema is valid

## Version

**Command Version**: 2.0 (v0.4.0)
**Replaces**: `/develop` and `/implement` from v0.3.x
**Compatible with**: astro-dev plugin v0.4.0+
**Last Updated**: 2025-11-05

Use `/dev` for all your Astro/Starlight development needs - from quick components to complex features.
