---
name: implement
description: Direct implementation with astro-developer agent (bypasses orchestration)
---

# /implement Command

Direct code implementation via the astro-developer agent.

## Usage

```
/implement [implementation request]
```

## Description

The `/implement` command directly invokes the **astro-developer** agent for code implementation, bypassing the orchestrator. Use this when you want straightforward implementation without orchestration overhead.

## What It Does

1. Loads astro-coding skill with relevant patterns
2. Implements requested code
3. Performs self-review
4. Returns implementation

## When to Use

Use `/implement` for:
- **Direct implementation** without planning
- **Quick changes** where orchestration isn't needed
- **Specific code tasks** with clear requirements
- **Bypassing orchestration** for speed

Use `/develop` instead when you want:
- Intelligent agent coordination
- Automatic architecture planning for complex features
- Adaptive audit level determination

## Examples

### Component Creation
```
/implement Create a Card component with title, description, and image
```

### Route Implementation
```
/implement Add a dynamic route for blog posts with TypeScript types
```

### Configuration
```
/implement Add Tailwind CSS integration to astro.config
```

### Bug Fixes
```
/implement Fix TypeScript errors in the Layout component
```

## What Gets Loaded

The astro-coding skill loads relevant patterns based on your request:

- **Components**: Component patterns, TypeScript patterns
- **Routes**: Routing patterns, TypeScript patterns
- **Collections**: Collection patterns, schema patterns
- **Config**: Configuration patterns

Critical rules always loaded:
- File extensions in imports
- Correct module prefixes (astro:content)
- Class vs className
- Async operation location
- Environment variable security

## Output

Direct implementation result:
```markdown
## Implementation Complete

### Files Modified/Created
- src/components/Card.astro (created)
- src/pages/blog/[slug].astro (modified)

### Changes Made
[Description of implementation]

### Self-Review
✅ All imports have extensions
✅ TypeScript types defined
✅ Patterns followed
✅ No critical issues

Ready for use.
```

## Comparison with Other Commands

| Command | Agent(s) | Planning | Audit | Use Case |
|---------|----------|----------|-------|----------|
| **/implement** | developer only | No | No | Direct implementation |
| **/develop** | orchestrator coordinates | Yes | Adaptive | Full workflow |
| **/architect** | architect only | Yes | No | Design only |

## Tips

### Be Specific
```
❌ /implement Make a blog
✅ /implement Create a blog collection schema with title, date, and tags
```

### Mention Requirements
```
✅ /implement Add footer component (must match existing header style)
✅ /implement Create API endpoint (with error handling)
```

### Reference Existing Code
```
✅ /implement Add pagination to blog listing (like the docs pagination)
```

## After Implementation

Manually validate if needed:
```
/audit [files]  # Optional manual validation
```

Or test directly and fix issues as they arise.

## Version

**Command Version**: 2.0
**Compatible with**: astro-dev plugin v2.0+
**Last Updated**: 2025-10-18

Use `/implement` for direct, no-frills code implementation.
