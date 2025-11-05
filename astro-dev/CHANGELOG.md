# Changelog

All notable changes to the Astro Dev plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-10-18

### Added

#### Agents
- **astro-orchestrator**: Intelligent task coordinator with complexity analysis
  - Agent coordination and parallel execution
  - Audit rigor calibration (auto/light/medium/comprehensive)
  - Token optimization via selective loading
  - Task analysis and execution planning

#### Commands
- **/develop**: Orchestrated workflow (primary command for 90% of tasks)
- **/architect**: Architecture planning without implementation
- Adaptive **/audit** levels: auto, light, medium, comprehensive

#### Features
- Progressive disclosure pattern for knowledge loading
- Knowledge base consolidation (17 files → 5 files, ~50% token reduction)
- Parallel agent execution when beneficial
- Selective pattern loading based on task keywords
- 3-priority validation system (P1: Breaking, P2: Security, P3: Best practices)

### Changed

#### Breaking Changes
- **/docs-lookup** command renamed to **/lookup**
- **astro-developer** skill renamed to **astro-coding**
- **astro-docs** skill renamed to **astro-knowledge**
- Auto-audit hooks removed (manual `/audit` preferred for user control)

#### Skills Reorganization
- **astro-coding**: Implementation patterns with selective loading
- **astro-knowledge**: API documentation and reference lookup

#### Knowledge Base
- Consolidated into 5 core files (~1500 lines total):
  - `error-catalog.md` - Indexed by symptom
  - `astro-patterns.md` - Components, routing, collections
  - `starlight-guide.md` - Starlight-specific features
  - `integrations.md` - Loaders, external data, TypeScript
  - `content-knowledge/` - Detailed references

### Improved
- Token usage reduced by ~50% through consolidation
- Task complexity analysis algorithm
- Rigor calibration for appropriate validation depth
- Documentation organization and clarity

### Removed
- Redundant knowledge base files (17 → 5)
- Auto-audit hooks (replaced with explicit `/audit` command)
- Broken components (Phase 4a cleanup)

---

## [0.1.0] - 2025-10-18 (Internal Development Version)

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

### Version 0.2.0 - Orchestration Architecture

Initial development release introducing orchestration-based architecture with intelligent task coordination.

**Key Improvements**:
- Orchestrator-driven workflows with automatic task analysis
- Adaptive validation rigor based on task complexity
- Consolidated knowledge base with selective loading
- Parallel agent execution when beneficial

**Note**: This is an initial development version (v0.x). Breaking changes may occur frequently as the plugin evolves toward v1.0 stability.

**Migration from v0.1.0**:
- Replace `/docs-lookup` with `/lookup`
- Use `/develop` as primary command (replaces direct `/implement` for most tasks)
- Invoke `astro-coding` skill instead of `astro-developer`
- Invoke `astro-knowledge` skill instead of `astro-docs`
- Use explicit `/audit` command (auto-hooks removed)

### Version 0.1.0 - Initial Implementation

Internal development version with basic agent system and comprehensive knowledge base.

### Compatibility

- **Claude Code**: Latest version
- **Astro**: v4.x and later
- **Starlight**: v0.21.x and later

### Links

- [Architecture Specification](../ARCHITECTURE_SPEC.md)
- [Implementation Status](../IMPLEMENTATION_STATUS.md)
- [Knowledge Base Consolidation](../KNOWLEDGE_BASE_CONSOLIDATION.md)
- [Root Changelog](../CHANGELOG.md)

---

**License**: CC0 1.0 Universal - Public Domain Dedication
**Author**: rathermercurial.eth
**Community**: SuperBenefit
