---
name: design
description: Architecture planning and system design for complex Astro/Starlight systems - provides design docs without implementation
---

# /design Command

Architecture planning and system design for complex Astro and Starlight projects. Provides structured design documents, schemas, and implementation roadmaps.

## Usage

```
/design [architecture or system description]
```

## Description

The `/design` command helps you plan complex system architectures before implementation. It loads architecture patterns from the astro-coding skill and creates comprehensive design documents with schemas, routing strategies, and implementation roadmaps.

**Note**: This command focuses on planning and documentation only. Use `/dev` to implement the designs.

## What It Does

1. **Analyzes Requirements**: Understands your system needs and constraints
2. **Designs Architecture**: Creates collection structures, routing strategies, data flow
3. **Provides Schemas**: Defines TypeScript schemas and data models
4. **Plans Implementation**: Creates step-by-step implementation roadmap
5. **Documents Decisions**: Explains architectural choices and trade-offs

## When to Use

Use `/design` when you need:
- **Complex content architecture** for multi-collection systems
- **Multi-source content** strategy (API + local files + external CMS)
- **Custom loader** architecture planning
- **Integration strategies** for external services
- **Refactoring guidance** for existing systems
- **Team documentation** for complex features

**Don't use** for simple components or standard features - just use `/dev` directly.

## Examples

### Content Collections Design
```
/design Blog system with categories, tags, authors, and related posts
```
**Output**: Collection schemas, relationship structures, query patterns, implementation steps

### Multi-Source Content
```
/design System that combines local MDX, GitBook API content, and PostgreSQL data
```
**Output**: Loader architecture, data transformation patterns, caching strategies, integration approach

### Complex Routing
```
/design Multi-language documentation with versioning and fallbacks
```
**Output**: Route structure, content organization, i18n strategy, implementation roadmap

### Integration Planning
```
/design Authentication system with Supabase and role-based access
```
**Output**: System architecture, data flow, security considerations, implementation phases

### Refactoring Strategy
```
/design How to refactor 100+ MDX files to use content collections
```
**Output**: Migration strategy, schema design, automation approach, rollback plan

## Output Format

The design command provides structured architecture documents:

```markdown
# [System Name] Architecture

## Overview
[High-level description of the system and its goals]

## Requirements Analysis
- [Functional requirement 1]
- [Functional requirement 2]
- [Non-functional requirements: performance, security, scalability]
- [Constraints and considerations]

## System Design

### Collection Structure
[Content collection definitions with relationships and data flow]

### Schema Definitions
```typescript
// Fully-typed TypeScript schemas
import { defineCollection, z } from 'astro:content';

export const collections = {
  blog: defineCollection({
    type: 'content',
    schema: z.object({
      title: z.string(),
      // ... full schema
    }),
  }),
};
```

### Loader Architecture (if custom loaders needed)
[Design for custom content loaders with caching, error handling, incremental updates]

### Routing Strategy
[URL patterns, dynamic routes, static generation approach]

### Data Flow
[How data moves through the system, from source to output]

## Implementation Roadmap

### Phase 1: Foundation (1-2 hours)
- Step 1: Set up collection schemas
- Step 2: Create base layouts

### Phase 2: Core Features (3-5 hours)
- Step 3: Implement dynamic routes
- Step 4: Build query patterns

### Phase 3: Integration (2-4 hours)
- Step 5: Connect external data sources
- Step 6: Add caching and optimization

## Architectural Decisions

### Decision 1: [Choice Made]
**Why**: [Rationale]
**Trade-offs**: [What we gain vs what we lose]
**Alternatives considered**: [Other options and why they were not chosen]

### Decision 2: [Choice Made]
...

## Technical Considerations

### Performance
[Build time, bundle size, runtime performance implications]

### Security
[Authentication, authorization, secret management, XSS prevention]

### Maintainability
[Code organization, testing strategy, documentation needs]

### Scalability
[How the system handles growth in content, users, or complexity]

## Next Steps

Ready to implement? Use:
```
/dev Implement the [system name] architecture we just designed
```

Or implement in phases:
```
/dev Implement Phase 1 of the [system] architecture
```
```

## Integration with /dev

After designing, implement with `/dev`:

```bash
# 1. Design the system
/design Multi-language blog with external API integration

# 2. Review the architecture document

# 3. Implement it
/dev Implement the multi-language blog architecture

# Or implement in phases:
/dev Implement Phase 1: collection schemas and base structure
/dev Implement Phase 2: dynamic routes and i18n
/dev Implement Phase 3: API integration and caching
```

## Common Use Cases

### Pre-Implementation Planning
```
Step 1: /design [describe complex system]
Step 2: Review and discuss architecture
Step 3: /dev [implement the system]
```

### Refactoring Guidance
```
/design Strategy to refactor content from pages/ to collections
```
**Output**: Migration plan, schema design, compatibility approach

### Decision Support
```
/design Compare content collections vs custom loaders for my use case
```
**Output**: Analysis of both approaches with pros/cons and recommendation

### Team Documentation
```
/design Document the architecture of our multi-tenant docs system
```
**Output**: Comprehensive architecture document for team reference

### Integration Planning
```
/design How to integrate Supabase auth with existing Astro app
```
**Output**: Integration architecture, data flow, security considerations

## Tips for Best Results

### Be Specific About Requirements
```
❌ /design a blog
✅ /design Blog with 10 categories, tag taxonomy, author profiles, related posts, and RSS feeds
```

### Mention Constraints
```
✅ /design Content system (must work with existing PostgreSQL database)
✅ /design Routing (SEO-friendly URLs required, sub-100ms page loads)
✅ /design Authentication (using Supabase, needs role-based access)
```

### Ask for Alternatives
```
✅ /design Compare approaches for multi-language content: collections vs loaders vs both
✅ /design Evaluate SSR vs SSG for this e-commerce catalog
```

### Include Scale Information
```
✅ /design Blog system (expecting 1000+ posts, 50+ categories)
✅ /design API integration (10k requests/day, 1-second response time max)
```

## When to Skip Design

**Don't use `/design` for**:
- Simple components (just use `/dev Create a Button component`)
- Standard blog setups (use `/dev Add a blog with categories`)
- One-off pages (use `/dev Create an about page`)
- Quick fixes (use `/dev Fix the header alignment`)

**Use `/design` for**:
- Multi-collection systems with relationships
- Custom content loaders
- External API integrations
- Multi-language systems
- Complex routing strategies
- Large refactoring projects

## Example Workflows

### Complex Feature
```bash
# 1. Design first
/design Multi-tenant documentation system with org-based access control

# 2. Review architecture
# Read the design doc, discuss with team

# 3. Implement
/dev Implement the multi-tenant docs architecture --audit=comprehensive
```

### Integration Project
```bash
# 1. Design the integration
/design Integrate Stripe payments with existing Astro site

# 2. Implement in phases
/dev Implement Phase 1: Stripe client setup and config
/dev Implement Phase 2: Payment routes and webhooks
/dev Implement Phase 3: User dashboard and receipts
```

### Refactoring
```bash
# 1. Plan the refactor
/design Refactor 200 markdown pages to content collections with categories

# 2. Execute the plan
/dev Implement the refactoring strategy with migration scripts
```

## Comparison with /dev

| Aspect | /design | /dev |
|--------|---------|------|
| **Output** | Architecture documents | Working code |
| **Use Case** | Complex system planning | Implementation |
| **Time** | 2-5 minutes | 1-20 minutes |
| **When** | Before complex builds | For all implementation |
| **Focus** | Planning and decisions | Code and validation |

## Version

**Command Version**: 2.0 (v0.4.0)
**Replaces**: `/architect` from v0.3.x
**Compatible with**: astro-dev plugin v0.4.0+
**Last Updated**: 2025-11-05

Use `/design` when you need thoughtful system architecture before diving into implementation.
