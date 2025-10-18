---
name: implement
description: Start Astro implementation with best practices loaded
---

# Implement Astro Feature

Initializes an implementation session with the astro-developer skill and best practices.

## Usage

```
/implement [feature-description]
```

## What This Does

1. Loads astro-developer skill context
2. Reviews project structure
3. Checks for similar patterns in codebase
4. References best practices and common mistakes
5. Enables audit hooks for automatic code review
6. Starts implementation with full context

## Examples

```bash
/implement Add a blog post listing page with pagination
/implement Create a custom content collection for team members
/implement Fix TypeScript errors in the Layout component
/implement Add dark mode toggle to Starlight site
```

## Pre-Implementation Checklist

Before implementing, the skill will:
- ✅ Load syntax references from knowledge base
- ✅ Review common mistakes to avoid
- ✅ Check TypeScript configuration
- ✅ Identify similar patterns in project
- ✅ Enable post-implementation audit

## Implementation Workflow

### Step 1: Analysis
- Understand the feature requirements
- Identify affected files and components
- Check for existing patterns

### Step 2: Planning
- Design component structure
- Plan data flow
- Identify dependencies

### Step 3: Implementation
- Write code following best practices
- Include proper TypeScript types
- Add error handling
- Implement accessibility features

### Step 4: Validation
- Auto-audit runs on save
- Check for common mistakes
- Verify TypeScript compliance
- Test functionality

## Options

While this command doesn't accept flags directly, you can specify requirements in your feature description:

```bash
/implement Add blog pagination --with-typescript --strict-mode
/implement Create contact form --with-validation --accessible
```

## What Gets Loaded

### Syntax References
- Component structure patterns
- Directive usage
- Import syntax
- Routing patterns

### Best Practices
- TypeScript patterns
- Performance optimization
- Security considerations
- Accessibility guidelines

### Common Mistakes
- Import extension requirements
- Module prefix corrections
- Component syntax pitfalls
- Hydration best practices

## Integration

- **Auto-Audit**: Code is automatically audited after changes
- **Docs Lookup**: Use `/docs-lookup` for API verification
- **Architecture**: Complex features can invoke @astro-architect
- **Error Fixes**: Automatic suggestions for common errors

## After Implementation

1. **Auto-Audit Runs**: Checks for issues automatically
2. **Review Report**: See any warnings or suggestions
3. **Fix Issues**: Address any critical problems
4. **Test**: Verify functionality works as expected

## Tips for Best Results

1. **Be Specific**: Include details about what you want to implement
2. **Mention Context**: Reference existing files or patterns
3. **State Requirements**: TypeScript, accessibility, performance needs
4. **Ask Questions**: If unsure about approach, ask before implementing

## Example Session

```
User: /implement Create a dynamic route for blog posts with proper TypeScript types