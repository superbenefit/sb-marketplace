# /develop Command

Intelligent development orchestration for Astro and Starlight projects.

## Usage

```
/develop [any development request]
```

## Description

The `/develop` command invokes the **astro-orchestrator** agent to intelligently coordinate your development workflow. It analyzes your request, creates an optimal execution plan, manages multiple agents in parallel when beneficial, and ensures appropriate quality validation.

## What It Does

1. **Analyzes Request**: Understands task scope, complexity, and requirements
2. **Creates Plan**: Determines which agents to invoke and in what order
3. **Optimizes Resources**: Loads only necessary context to minimize token usage
4. **Coordinates Agents**: Manages astro-developer, astro-architect, and astro-auditor
5. **Calibrates Rigor**: Sets appropriate audit level (light/medium/comprehensive)
6. **Presents Results**: Aggregates outputs into coherent report

## Examples

### Simple Component
```
/develop Add a Footer component with social links
```
**What happens**:
- astro-developer creates the component
- astro-auditor performs light validation
- Complete in ~1 minute

### Feature Implementation
```
/develop Add a blog with categories and pagination
```
**What happens**:
- astro-architect designs collection structure
- astro-developer implements features
- astro-auditor performs medium validation
- Complete in ~5 minutes

### Complex Architecture
```
/develop Create a multi-language content system with GitBook integration
```
**What happens**:
- astro-architect designs full architecture
- astro-developer implements in stages
- astro-auditor performs comprehensive validation
- Complete in ~15 minutes

### Bug Fixes
```
/develop Fix all TypeScript errors in components folder
```
**What happens**:
- astro-auditor scans and catalogs issues
- astro-developer fixes in parallel batches
- astro-auditor validates all fixes
- Complete in ~10 minutes

## Benefits

### Intelligent Planning
No need to decide which agents to use - the orchestrator determines the optimal approach based on your request.

### Token Efficiency
Loads only the patterns and context needed for your specific task, reducing token usage by 40-70% compared to loading everything.

### Adaptive Quality
Audit rigor scales with task complexity:
- Small fixes → Quick validation (5 checks)
- Standard features → Standard validation (20 checks)
- Critical areas → Full validation (50+ checks)

### Parallel Execution
When beneficial, multiple agents work simultaneously to reduce total execution time.

## When to Use

Use `/develop` as your primary command for:
- Any implementation task
- Feature additions
- Refactoring work
- Bug fixes
- Architecture planning + implementation

## When to Use Direct Commands Instead

Skip orchestration and invoke agents directly when you need specific behavior:

- `/implement` → Direct to astro-developer (bypass planning)
- `/architect` → Direct to astro-architect (planning only, no implementation)
- `/audit [level]` → Direct to astro-auditor (validation only)
- `/lookup` → Direct to astro-knowledge (documentation only)

## Agent Coordination

The orchestrator may invoke:

**astro-architect** for:
- Complex system design
- Collection architecture
- Multi-source content planning
- Integration strategies

**astro-developer** for:
- All code implementation
- Component creation
- Route/page development
- Configuration changes

**astro-auditor** for:
- Code validation (at appropriate rigor level)
- Security review
- Performance analysis
- Best practices verification

## Examples by Complexity

### Trivial (<1 minute)
```
/develop Fix typo in header
/develop Add padding to button
/develop Update copyright year
```

### Simple (1-3 minutes)
```
/develop Create a Card component
/develop Add a 404 page
/develop Update navigation menu
```

### Medium (3-8 minutes)
```
/develop Add blog with pagination
/develop Create category taxonomy
/develop Implement search functionality
```

### Complex (8-20 minutes)
```
/develop Build multi-language system
/develop Add authentication flow
/develop Create custom content loader
/develop Refactor entire components folder
```

## Tips

### Be Specific
```
❌ /develop make it better
✅ /develop Add pagination to the blog listing page
```

### Mention Constraints
```
✅ /develop Add authentication (using existing auth library)
✅ /develop Create blog (following existing component structure)
```

### Batch Related Tasks
```
✅ /develop Add blog with categories, tags, and RSS feed
```
Orchestrator will handle all parts efficiently.

## Output Format

The orchestrator provides updates throughout:

```markdown
✓ Task analyzed: Adding blog with pagination
✓ Execution plan: architect → developer → auditor (medium)
✓ Invoking astro-architect for collection design
✓ astro-architect completed: Schema and structure defined
✓ Invoking astro-developer for implementation
✓ astro-developer completed: 4 files created
✓ Invoking astro-auditor for validation (medium level)
✓ astro-auditor completed: No issues found

## Implementation Summary

Blog system with pagination successfully implemented.

### Files Created
- src/content/config.ts (collection schema)
- src/pages/blog/index.astro (listing with pagination)
- src/pages/blog/[slug].astro (single post)
- src/components/Pagination.astro (pagination component)

### Validation Results
- Audit level: Medium
- Issues found: 0
- Status: ✅ Passed

All components follow best practices and are ready for use.
```

## Version

**Command Version**: 1.0
**Compatible with**: astro-dev plugin v2.0+
**Last Updated**: 2025-10-18

Use `/develop` as your primary development command for intelligent, efficient Astro/Starlight development.
