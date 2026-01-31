# Changelog

All notable changes to the sb-marketplace project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.5.0] - 2026-01-31

### Added
- **project-mgmt v0.1.0** - Spec-driven development plugin with persistent markdown planning
  - Single skill (`project-mgmt`) with 6-phase progressive disclosure workflow
  - Background subagent (`pm-bookkeeper`) for file updates using Haiku
  - Hooks for session init, plan refresh, and completion checking
  - Templates for plan, spec, findings, and progress files
  - See [project-mgmt/CHANGELOG.md](./project-mgmt/CHANGELOG.md) for details

### Removed
- **knowledge-skill-builder** - Removed entirely (hallucinated plugin from previous session)
  - Deleted plugin directory and all contents
  - Purged all references from marketplace.json, CLAUDE.md, README.md

### Changed
- Marketplace version bumped to 0.5.0
- Updated CLAUDE.md and README.md to reflect 3-plugin marketplace

## [0.4.0] - 2026-01-30

### Added
- **cloudflare-dev v0.1.0** - Cloudflare developer platform toolkit
  - 8 audited knowledge base reference files (Agents SDK, MCP, Vectorize, Workflows, Workers Platform, Auth/Deploy, Observability, Agent Patterns)
  - 4 commands (cf-dev, validate, deploy-check, test-mcp)
  - 3 agents (cf-validator, cloudflare-helper, docs-writer)
  - cloudflare-knowledge skill with SKILL.md quick reference
  - MCP integration (docs.mcp.cloudflare.com)
  - See [cloudflare-dev/CHANGELOG.md](./cloudflare-dev/CHANGELOG.md) for details

### Changed
- **astro-dev v0.4.0** - Major simplification of plugin architecture
  - See [astro-dev/CHANGELOG.md](./astro-dev/CHANGELOG.md) for details
- Marketplace version bumped to 0.4.0
- Updated CLAUDE.md with cloudflare-dev section and astro-dev updates

## [0.3.1] - 2025-10-20

### Fixed
- **Critical plugin loading issue** - Added required YAML frontmatter to agent files
  - Added frontmatter to `astro-developer.md` with name, description, and model fields
  - Added frontmatter to `astro-orchestrator.md` with name, description, and model fields
- **plugin.json schema** - Fixed incorrect format for agents and commands fields
  - Removed incorrect object-based `commands` field (was using `{"name": "path"}` format)
  - Removed incorrect object-based `agents` field (was using nested objects)
  - Now relies on auto-discovery from default `commands/` and `agents/` directories
- All slash commands, agents, and skills now load correctly when plugin is installed

### Changed
- Plugin.json now uses auto-discovery for agents and commands instead of explicit paths
- Agents use consistent YAML frontmatter format across all 4 agent files

### Documentation
- Updated plugin-diagnostic-report.md with root cause analysis and fixes
- Added testing instructions for verifying plugin functionality

## [0.3.0] - 2025-10-20

### Breaking Changes
- **Transitioned to GitHub-based plugin loading** - Directory-based installation no longer supported
- Removed `setup.sh` installation script
- Installation now requires GitHub source in settings.json

### Changed
- Plugin now loads from GitHub repository: `superbenefit/sb-marketplace`
- Installation simplified to 2 steps: add to settings.json and restart Claude Code
- Documentation completely rewritten for GitHub-based workflow
- Marketplace description updated to be more descriptive

### Added
- Repository field in plugin.json pointing to GitHub repo
- CONTRIBUTING.md with community contribution guidelines
- Root-level LICENSE file (CC0 1.0 Universal)

### Removed
- `setup.sh` script (obsolete with GitHub loading)
- All directory-based installation documentation
- References to local/project-local installation methods

## [0.2.0] - 2025-10-19

### Added
- Comprehensive `claude.md` context file for rapid Claude Code initialization
- Root CHANGELOG.md with marketplace version history
- Documentation reorganization in README with audience-specific sections

### Changed
- README.md: Added claude.md reference callout for AI assistants
- README.md: Replaced Architecture section with Documentation section

## [0.1.0] - 2025-10-18

### Added
- Initial marketplace structure with plugin registry
- `.claude-plugin/marketplace.json` - Marketplace manifest
- `setup.sh` - Installation script with auto-detection and jq support
- `.gitignore` - Configuration for `.claude/` directory
- Documentation structure (README.md)

### Plugins Included
- **astro-dev v0.2.0** - Astro/Starlight development toolkit
  - See [astro-dev/CHANGELOG.md](./astro-dev/CHANGELOG.md) for plugin-specific changes

---

## Version Summary

| Component | Version | Status |
|-----------|---------|--------|
| **sb-marketplace** | 0.5.0 | Production |
| **astro-dev** | 0.4.0 | Production |
| **cloudflare-dev** | 0.1.0 | Production |
| **project-mgmt** | 0.1.0 | Initial Release |

## Links

- [astro-dev Changelog](./astro-dev/CHANGELOG.md)
- [cloudflare-dev Changelog](./cloudflare-dev/CHANGELOG.md)
- [project-mgmt Changelog](./project-mgmt/CHANGELOG.md)
- [Contributing Guide](./CONTRIBUTING.md)

---

**License**: CC0 1.0 Universal - Public Domain Dedication
**Maintainer**: rathermercurial.eth
**Community**: SuperBenefit
