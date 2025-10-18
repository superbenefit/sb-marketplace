# Astro Content Specialist Agent Usage Guide

This guide explains when and how to use the `astro-content-specialist` agent, and how it works with the `astro-docs-specialist` agent for optimal results.

## Agent Roles

### astro-content-specialist (Architecture Agent)
**Purpose:** Planning and architecting Astro content systems

**Strengths:**
- Content collection design and architecture
- Custom loader implementation planning
- Routing and page strategy design
- External data integration patterns
- Starlight-specific content architecture
- Performance and caching strategies

**Knowledge Base:**
- Comprehensive cached reference materials
- Pre-researched patterns and best practices
- Implementation blueprints and examples
- Architecture decision guides

### astro-docs-specialist (Research Agent)
**Purpose:** Fetching current Astro/Starlight documentation

**Strengths:**
- Real-time MCP documentation access
- API syntax verification
- Current feature availability checking
- Authoritative source URLs
- Latest documentation updates

## When to Use Each Agent

### Use astro-content-specialist When:

1. **Designing Content Architecture**
   - "How should I structure my content collections?"
   - "What's the best way to organize docs with versioning?"
   - "How do I handle multiple languages in Starlight?"

2. **Planning External Data Integration**
   - "I need to integrate GitBook content - what's the approach?"
   - "How do I fetch data from our CMS API?"
   - "What's the best caching strategy for external content?"

3. **Architecting Routing Patterns**
   - "How should I structure dynamic routes for products?"
   - "What pagination strategy should I use?"
   - "How do I implement nested routing?"

4. **Planning Custom Loaders**
   - "I need to design a loader for our external API"
   - "How should I handle authentication in loaders?"
   - "What's the best error handling strategy?"

5. **Starlight Content Strategy**
   - "How do I organize Starlight docs with custom pages?"
   - "What frontmatter strategy should I use?"
   - "How do I customize the sidebar structure?"

### Use astro-docs-specialist When:

1. **Verifying API Syntax**
   - "What are the exact parameters for getCollection()?"
   - "Show me the current LoaderContext API"
   - "What methods are available on the store object?"

2. **Checking Feature Availability**
   - "Does Starlight support X feature?"
   - "Is there a built-in loader for Y?"
   - "What's the latest pagination API?"

3. **Finding Documentation**
   - "Where's the docs on content layer API?"
   - "Show me examples of custom loaders"
   - "Find the Starlight frontmatter reference"

4. **Researching Specific Topics**
   - "How does Astro handle i18n?"
   - "What are the server-side rendering options?"
   - "Research Astro's image optimization features"

## Complementary Workflow Patterns

### Pattern 1: Architecture First, Then Verify

**Scenario:** Integrating external CMS content

```
Step 1: Use astro-content-specialist
"I need to integrate content from our headless CMS. Design the architecture."

Agent provides:
- Collection structure design
- Custom loader architecture
- Authentication pattern
- Caching strategy
- Error handling approach

Step 2: Use astro-docs-specialist
"Verify the current LoaderContext API methods for:
- parseData()
- renderMarkdown()
- generateDigest()
- meta.set() and meta.get()"

Agent provides:
- Current API documentation
- Exact method signatures
- Source URLs
- Usage examples
```

### Pattern 2: Research Then Architect

**Scenario:** Implementing new Astro feature

```
Step 1: Use astro-docs-specialist
"Research Astro's live content collections feature. Is it stable? How does it work?"

Agent provides:
- Feature status (experimental/stable)
- Documentation URLs
- API overview
- Requirements

Step 2: Use astro-content-specialist
"Based on live content collections, design an architecture for real-time docs updates from our API."

Agent provides:
- Architecture plan using live collections
- Integration with existing content
- Performance considerations
- Implementation roadmap
```

### Pattern 3: Iterative Architecture and Verification

**Scenario:** Complex multi-source content system

```
Step 1: astro-content-specialist
"Design content architecture for:
- Local markdown docs
- GitBook external content
- API-sourced tutorials
- Multiple languages"

Step 2: astro-docs-specialist
"Verify syntax for:
- Collection references
- i18n configuration
- Multiple loaders in one collection"

Step 3: astro-content-specialist
"Refine architecture based on API verification, add implementation details"

Step 4: astro-docs-specialist
"Find Starlight i18n best practices and fallback behavior docs"

Step 5: astro-content-specialist
"Finalize architecture with i18n fallback strategy"
```

## Best Practices

### For astro-content-specialist:

1. **Be Specific About Requirements**
   - Describe data sources clearly
   - Mention performance requirements
   - Specify scalability needs
   - Note any constraints

2. **Ask for Complete Architecture**
   - Collection structures
   - Loader designs
   - Error handling
   - Caching strategies
   - Implementation roadmap

3. **Request Knowledge Base References**
   - Agent should cite which knowledge files were used
   - Ensures comprehensive coverage
   - Helps you understand the approach

### For astro-docs-specialist:

1. **Request Specific APIs**
   - Name exact functions/methods
   - Mention specific features
   - Ask for current syntax

2. **Ask for Source URLs**
   - Always request documentation links
   - Helps with deeper research
   - Provides authoritative reference

3. **Verify Before Implementation**
   - Check APIs before coding
   - Confirm feature availability
   - Validate syntax assumptions

## Example Scenarios

### Scenario 1: GitBook Integration

**User Request:** "I need to integrate our GitBook documentation into this Starlight site."

**Optimal Workflow:**

1. **astro-content-specialist:**
   ```
   "Design a GitBook integration architecture including:
   - Loader design with authentication
   - Data transformation from GitBook to Starlight format
   - Caching strategy to minimize API calls
   - Error handling for API failures
   - Update strategy (incremental vs full)"
   ```

   **Agent Response:**
   - Reads `external-data-integration.md`
   - Provides GitBook loader architecture
   - Designs collection schema
   - Plans authentication with env vars
   - Outlines caching with meta store
   - Recommends digest-based incremental updates

2. **astro-docs-specialist:**
   ```
   "Verify current API for:
   - Environment variable configuration
   - LoaderContext.meta methods
   - generateDigest() function
   - renderMarkdown() availability"
   ```

   **Agent Response:**
   - Provides current env var setup
   - Shows meta store API
   - Confirms digest and render methods
   - Includes documentation URLs

3. **Implement** based on architecture and verified APIs

### Scenario 2: Dynamic Product Documentation

**User Request:** "We need versioned docs for multiple products with dynamic routing."

**Optimal Workflow:**

1. **astro-content-specialist:**
   ```
   "Design routing architecture for:
   - Multiple products (/products/[product-id]/...)
   - Version support (/products/[product]/[version]/...)
   - Pagination for large doc sets
   - Breadcrumb generation"
   ```

   **Agent Response:**
   - Reads `routing-pages-reference.md`
   - Designs nested dynamic routes
   - Plans getStaticPaths() structure
   - Outlines pagination strategy
   - Provides route priority considerations

2. **astro-docs-specialist:**
   ```
   "Verify:
   - Nested pagination API
   - Route priority rules for /[product]/[version]
   - getStaticPaths return format for complex params"
   ```

   **Agent Response:**
   - Current pagination syntax
   - Route priority documentation
   - Params structure examples

### Scenario 3: Multi-Collection Content System

**User Request:** "Setup collections for blog posts, docs, and authors with relationships."

**Optimal Workflow:**

1. **astro-content-specialist:**
   ```
   "Design collection architecture with:
   - Blog posts collection (from markdown)
   - Docs collection (from GitBook)
   - Authors collection (from JSON)
   - Cross-references between them"
   ```

   **Agent Response:**
   - Reads `content-collections-reference.md`
   - Designs three collections with schemas
   - Plans reference() usage for relationships
   - Outlines loader choices (glob, custom, file)
   - Shows query patterns for referenced data

2. **astro-docs-specialist:**
   ```
   "Verify:
   - reference() function syntax
   - getEntry() with references
   - getEntries() for arrays of references"
   ```

## Summary

**Content Specialist:**
- Architecture and planning
- Design and strategy
- Cached knowledge base
- Implementation blueprints

**Docs Specialist:**
- Documentation research
- API verification
- Current syntax
- Real-time MCP access

**Together they provide:**
- Well-architected solutions
- Current, verified APIs
- Comprehensive implementation plans
- Authoritative documentation references

**Pro Tip:** Start with content specialist for architecture, then use docs specialist to verify specific APIs before implementation. This minimizes token usage while ensuring current, accurate implementations.
