# project-mgmt

Spec-driven development with persistent markdown planning for Claude Code.

**Version**: 0.1.0
**License**: CC0 1.0 Universal

## What It Does

Provides a structured workflow for complex development tasks. Uses the filesystem as persistent memory — plan.md, spec.md, findings.md, and progress.md live in `.project/{issue#}/` and survive context window resets.

## Workflow

1. **Start** — Initialize from a GitHub issue or description
2. **Specify** — Define requirements in spec.md (what & why, no tech stack)
3. **Plan** — Create implementation steps with checkboxes in plan.md
4. **Implement** — Execute steps, track progress via pm-bookkeeper agent
5. **PR** — Create pull request from completed work
6. **Sync** — Update GitHub issue with progress

## Components

| Component | Type | Purpose |
|-----------|------|---------|
| `project-mgmt` | Skill | Core workflow with phase-based references |
| `pm-bookkeeper` | Subagent | Background file updates (Haiku, non-blocking) |

## Project Files

Created in `.project/{issue#}/`:

| File | Purpose |
|------|---------|
| plan.md | Implementation steps + session context |
| spec.md | Requirements (what & why) |
| findings.md | Research, technical decisions |
| progress.md | Session log, errors, test results |

## Requirements

- **GitHub CLI** (`gh`) — Required for issue integration. Falls back to manual mode if unavailable.

## Installation

Add to your Claude Code settings (`~/.claude/settings.json` or `.claude/settings.local.json`):

```json
{
  "extraKnownMarketplaces": {
    "sb-marketplace": {
      "source": {
        "source": "github",
        "repo": "superbenefit/sb-marketplace"
      }
    }
  },
  "enabledPlugins": {
    "project-mgmt@sb-marketplace": true
  }
}
```

Restart Claude Code after editing settings.

## Usage

The skill auto-invokes for complex tasks, or invoke manually:

```
/project-mgmt start #123
/project-mgmt sync
```

## Token Budget

| Load Stage | Content | Tokens |
|------------|---------|--------|
| Startup | name + description | ~100 |
| On match | SKILL.md body | ~200 |
| On demand | One phase reference | ~150 |
| Never loaded | assets/, scripts/ | 0 |

Typical usage: ~450 tokens per task.

## Author

rathermercurial.eth — [SuperBenefit](https://superbenefit.org)

## License

CC0 1.0 Universal — Public Domain Dedication
