# Changelog

All notable changes to the project-mgmt plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-01-31

### Initial Release

First release of the project management plugin.

### Added

#### Skill
- **project-mgmt**: Spec-driven development workflow with 6-phase progressive disclosure
  - Phase references: start, specify, plan, implement, pr, sync
  - Templates: plan, spec, findings, progress

#### Agent
- **pm-bookkeeper**: Background file update agent (Haiku, non-blocking)
  - Checks off plan steps, logs progress, records findings
  - Uses `acceptEdits` permission mode

#### Hooks
- **SessionStart**: Displays active project context on session start/resume
- **PreToolUse**: Reminds to re-read plan.md before Write/Edit operations
- **Stop**: Warns about unchecked items before stopping

---

**License**: CC0 1.0 Universal - Public Domain Dedication
