# Changelog

All notable changes to the sb-marketplace project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed
- Marketplace manifest name corrected from "astro-dev-marketplace" to "sb-marketplace"
- Marketplace description updated to accurately reflect general-purpose nature

### Changed
- setup.sh: Added claude.md and CHANGELOG.md references

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
- Documentation structure (README.md, ARCHITECTURE_SPEC.md, etc.)

### Features
- Auto-detects project-local vs global installation
- Automatic Claude Code settings configuration
- Settings backup on installation
- Manual fallback when jq is unavailable
- Support for multiple plugins in marketplace

### Plugins Included
- **astro-dev v0.2.0** - Astro/Starlight development toolkit
  - See [astro-dev/CHANGELOG.md](./astro-dev/CHANGELOG.md) for plugin-specific changes

---

## Commit History

### 2025-10-19
- Add comprehensive claude.md context file and update README

### 2025-10-18
- `599851a` - Fix marketplace source type from 'local' to 'directory'
- `0955540` - Fix plugin version inconsistencies and document usage issues
- `553af3a` - Update setup.sh to reflect v2.0 architecture
- `02c6b7e` - Add claude.md snippet to READMEs
- `0f65f4b` - Add .claude/ to .gitignore
- `9d7061d` - Fix: Update README and manifest with understated tone
- `da1cafa` - 🎉 v2.0 Implementation Complete
- `f50732d` - Phase 4c: Final manifest and documentation updates
- `5da0376` - Phase 4b: Knowledge base consolidation (17→5 files)
- `df7a26b` - Phase 4a: Remove broken components
- `0fe33e6` - Phase 3b: Complete command layer updates
- `6834349` - Add implementation status tracking document
- `4a2b7d0` - Phase 3a: Command layer updates
- `cd903cc` - Phase 2a: Skill reorganization and renaming
- `0e642f0` - Phase 1: Core architecture with intelligent orchestration
- `6f9b667` - Initial commit with architecture specification v2.0

---

## Version Summary

| Component | Version | Status |
|-----------|---------|--------|
| **sb-marketplace** | 0.2.0 | Initial Development |
| **astro-dev plugin** | 0.2.0 | Initial Development |

## Links

- [Plugin Changelog](./astro-dev/CHANGELOG.md) - Plugin-specific version history
- [Architecture Specification](./ARCHITECTURE_SPEC.md) - System design documentation
- [Implementation Status](./IMPLEMENTATION_STATUS.md) - Development progress tracking
- [Claude Context](./claude.md) - Repository context for AI assistants

---

**License**: CC0 1.0 Universal - Public Domain Dedication
**Maintainer**: rathremercurial.eth
**Community**: SuperBenefit
