# Changelog

All notable changes to the Astro Dev plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-18

### Added

#### Skills
- **astro-developer**: Expert Astro/Starlight developer skill for implementation tasks
  - Component development patterns
  - Dynamic routing templates
  - Content collections expertise
  - TypeScript integration
  - Critical rules and common mistakes reference

- **astro-docs**: Documentation specialist skill for API verification
  - Quick API lookups
  - Current syntax verification
  - Common usage patterns
  - Integration with MCP server support

#### Agents
- **astro-auditor**: Comprehensive code auditor with 3-priority system
  - Priority 1: Build-breaking issues
  - Priority 2: Security, performance, and common bugs
  - Priority 3: Best practices and code quality
  - Automated audit reports with fixes

- **astro-architect**: Content architecture specialist
  - Content collection design
  - Custom loader architecture
  - Multi-source content systems
  - Routing strategy planning

#### Commands
- **/implement**: Start implementation with best practices loaded
- **/audit**: Manual comprehensive code audit trigger
- **/docs-lookup**: Quick Astro API documentation lookup

#### Hooks
- **PostToolUse**: Auto-audit after Write|Edit operations on Astro files
- **PreToolUse**: Notify about upcoming audits

#### Scripts
- **audit-runner.sh**: Automated quick validation for Astro files
  - Checks for `astro/content` vs `astro:content`
  - Detects `className` usage in Astro components
  - Validates import extensions
  - Identifies common mistakes

#### Knowledge Base
- **astro-syntax/**: Core Astro syntax references
  - Component structure
  - Directives (client:*, is:*, set:*)
  - Import patterns
  - Routing patterns
  - Configuration

- **common-mistakes/**: Cataloged errors and fixes
- **best-practices/**: Recommended patterns
  - Astro best practices
  - Starlight patterns
  - TypeScript patterns

- **architecture-patterns/**: System design references
  - Content collections
  - Routing architecture

- **loader-examples/**: Custom loader implementations
- **integration-guides/**: External system integration
- **starlight/**: Starlight-specific documentation
- **audit/**: Code quality and audit checklists

### Plugin Structure
- Marketplace manifest configuration
- Plugin manifest with all components registered
- Organized directory structure following Claude Code plugin spec
- Comprehensive documentation and READMEs

### License
- CC0 1.0 Universal - Public Domain Dedication

---

## Release Notes

### Version 1.0.0 - Initial Release

This is the first complete release of the Astro Dev plugin for Claude Code. It provides a comprehensive toolkit for Astro and Starlight development with:

- **Skills** for frequently-used capabilities
- **Agents** for complex parallel tasks
- **Commands** for quick access
- **Hooks** for automated workflows
- **Knowledge Base** for progressive disclosure

The plugin follows the Claude Code plugin architecture specification with optimized context usage through progressive loading.

### Installation

See README.md for installation instructions.

### Compatibility

- Claude Code: Latest version
- Astro: v4.x and later
- Starlight: v0.21.x and later

### Future Roadmap

See README.md for planned enhancements.
