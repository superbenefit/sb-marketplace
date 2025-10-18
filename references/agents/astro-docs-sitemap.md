# Astro Documentation Sitemap Reference

This file provides a structured reference to the comprehensive Astro documentation sitemap for the astro-docs-specialist agent. The complete sitemap is maintained in `.claude/astro-docs/astro-sitemap.md` and MUST be consulted before making any MCP searches.

## MANDATORY Usage Instructions for astro-docs-specialist

1. **ALWAYS read sitemap first** - Read `.claude/astro-docs/astro-sitemap.md` completely before ANY MCP searches
2. **Map queries to sections** - Identify 2-3 relevant sitemap sections for each query
3. **Extract precise terms** - Use exact section titles and URLs for targeted MCP queries
4. **Reference URLs** - Include specific documentation URLs from sitemap in all responses

## Comprehensive Documentation Categories (113 sections total)

### **Core Categories:**
- **Basics** (4): Components, Pages, Layouts, Project Structure
- **Concepts** (2): Islands, Why Astro
- **Guides** (72): Implementation guides, integrations, configuration, styling, testing
- **Recipes** (6): Practical implementation examples
- **Reference** (29): Complete API documentation, modules, configuration

### **Key Reference Sections (29 total):**
- Configuration Reference, API Reference, CLI Commands
- Content Layer API, Content Loader Reference, Content Collection APIs
- All astro: modules (actions, assets, config, content, env, i18n, middleware, transitions)
- Experimental Flags, Legacy Flags, TypeScript Reference
- Error Reference, Directives Reference, Routing Reference

### **Critical Guides for Starlight Projects:**
- **Configuration**: Configuring Astro, Content Collections, Data Fetching
- **Styling**: Styling, Tailwind Integration, Syntax Highlighting
- **Content**: Content Collections, Markdown Content, MDX
- **Performance**: Testing, Troubleshooting, TypeScript
- **Deployment**: Cloudflare deployment (only deployment guide included)
- **Integrations**: Starlight (check integrations guide for Starlight-specific docs)

### **Strategic Exclusions Maintained:**
- CMS guides (except main CMS page) - not using CMS
- Most deployment guides except Cloudflare - focus on relevant platform

## Starlight-Specific Documentation Priorities

When working with Starlight documentation sites, prioritize searches in this order:

1. **Starlight Integration Guide** - For Starlight-specific features and configuration
2. **Content Collections** - For documentation content management
3. **Markdown/MDX guides** - For content authoring patterns
4. **Configuration Reference** - For Astro and Starlight config options
5. **Reference sections** - For API syntax and configuration details
6. **Specific feature guides** - For implementation guidance
7. **Recipes** - For practical examples and patterns
8. **Troubleshooting** - For debugging and issues

## Search Strategy for astro-docs-specialist

For any documentation request:
1. Read full sitemap to understand available sections
2. Identify 2-3 most relevant sections based on query
3. Use section titles as search terms in MCP queries
4. Reference specific sitemap URLs in responses
5. Cross-reference multiple relevant sections
6. For Starlight questions, include both Astro core docs and Starlight-specific resources

## Local Fallback Resources

When MCP server is unavailable:
- `.claude/astro-docs/llms.txt` - Concise overview and documentation set links
- `.claude/astro-docs/llms-full.md` - Complete Astro documentation (71,962 lines)
- Use sitemap to locate relevant sections within llms-full.md

This comprehensive reference ensures efficient, targeted documentation searches that support all implementation work with precise, current Astro and Starlight documentation.
