# /architect Command

Direct architecture planning for complex Astro and Starlight systems.

## Usage

```
/architect [architecture request]
```

## Description

The `/architect` command directly invokes the **astro-architect** agent for system design and architecture planning. Use this when you need architectural guidance without immediate implementation.

## What It Does

1. **Analyzes Requirements**: Understands your system needs
2. **Designs Architecture**: Creates collection structures, routing strategies
3. **Provides Schemas**: Defines TypeScript schemas and data models
4. **Plans Implementation**: Creates step-by-step implementation roadmap
5. **Documents Patterns**: Explains architectural decisions

## When to Use

Use `/architect` when you need:
- **Complex content architecture** design
- **Multi-source content systems** planning
- **Custom loader** architecture
- **Collection structure** design
- **Integration strategies** planning
- **Architectural guidance** before implementation

## Examples

### Content Collections Design
```
/architect Design a blog system with categories, tags, and authors
```
**Output**:
- Collection schemas
- Relationship structures
- Query patterns
- Implementation steps

### Multi-Source Content
```
/architect Create a system that combines local MDX with GitBook API content
```
**Output**:
- Loader architecture
- Data transformation patterns
- Caching strategies
- Integration approach

### Complex Routing
```
/architect Design routing for multi-language docs with versioning
```
**Output**:
- Route structure
- Content organization
- Fallback strategies
- Implementation roadmap

### Integration Planning
```
/architect Plan integration with external CMS and authentication
```
**Output**:
- System architecture
- Data flow design
- Security considerations
- Implementation phases

## Output Format

The architect provides structured design documents:

```markdown
# [System Name] Architecture

## Overview
[High-level description]

## Requirements Analysis
- [Requirement 1]
- [Requirement 2]
- [Constraints and considerations]

## System Design

### Collection Structure
[Collection definitions with relationships]

### Schema Definitions
\`\`\`typescript
[TypeScript schemas]
\`\`\`

### Loader Architecture
[Custom loader design if needed]

### Routing Strategy
[URL patterns and dynamic routes]

## Implementation Roadmap

### Phase 1: [Foundation]
- Step 1
- Step 2

### Phase 2: [Core Features]
- Step 3
- Step 4

### Phase 3: [Integration]
- Step 5
- Step 6

## Architectural Decisions
[Explanation of key design choices]

## Next Steps
[How to proceed with implementation]
```

## Comparison with /develop

| Aspect | /architect | /develop |
|--------|-----------|----------|
| **Focus** | Planning only | Planning + Implementation |
| **Output** | Architecture documents | Working code |
| **Use Case** | Complex design first | End-to-end delivery |
| **Agents** | astro-architect only | orchestrator coordinates all |

## Integration with Implementation

After architecture planning, you can:

1. **Use /develop** to implement the architecture:
   ```
   /develop Implement the blog architecture we just designed
   ```

2. **Use /implement** for specific pieces:
   ```
   /implement Create the blog collection schema
   ```

3. **Refer to the architecture** as you build:
   The architecture serves as a blueprint for development

## Common Use Cases

### Pre-Implementation Planning
```
Step 1: /architect [design the system]
Step 2: Review and refine architecture
Step 3: /develop [implement the system]
```

### Refactoring Guidance
```
/architect How should I refactor my content collections for better scalability?
```

### Decision Support
```
/architect Should I use a custom loader or content collections for GitBook integration?
```

### Team Collaboration
```
/architect Document the architecture for our multi-tenant docs system
```

## Tips

### Be Specific About Requirements
```
❌ /architect Design a blog
✅ /architect Design a blog with 5 categories, tag taxonomy, author profiles, and RSS feeds
```

### Mention Constraints
```
✅ /architect Design content system (must work with existing PostgreSQL database)
✅ /architect Plan routing (SEO-friendly URLs required)
```

### Ask for Alternatives
```
✅ /architect Compare approaches for multi-language content: collections vs loaders
```

## Version

**Command Version**: 1.0
**Compatible with**: astro-dev plugin v2.0+
**Last Updated**: 2025-10-18

Use `/architect` when you need thoughtful system design before diving into implementation.
