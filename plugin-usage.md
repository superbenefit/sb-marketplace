# Astro-Dev Plugin Usage Issues

## Summary

Attempted to use the astro-dev plugin (v2.0) from sb-marketplace to architect a multi-collection content structure. Encountered multiple issues preventing the plugin's slash commands from being recognized by Claude Code.

## Context

- **Plugin Location**: `F:/projects/sb-marketplace/astro-dev/`
- **Project Location**: `F:/projects/sb-governance-starlight/`
- **Plugin Version**: 2.0.0
- **Installation Status**: Plugin shows as "installed" in Claude Code UI

## Issues Encountered

### 1. Missing `enabledPlugins` Configuration

**Issue**: The project's `.claude/settings.local.json` had the marketplace configured but was missing the `enabledPlugins` section.

**Original State**:
```json
{
  "extraKnownMarketplaces": {
    "sb-marketplace": {
      "source": {
        "source": "local",
        "path": "F:/projects/sb-marketplace"
      }
    }
  }
}
```

**Fixed By**: Adding the missing section:
```json
{
  "enabledPlugins": {
    "astro-dev@sb-marketplace": true
  },
  "extraKnownMarketplaces": {
    "sb-marketplace": { ... }
  }
}
```

**Result**: Still didn't make slash commands available.

### 2. Setup Script Configuration

**Issue**: Ran the setup script at `F:/projects/sb-marketplace/setup.sh` which configured global settings but couldn't automatically update JSON because `jq` is not installed.

**Setup Script Output** (at time of issue):
- Backed up settings to `/c/Users/r_lyn/.claude/settings.json.backup.20251018_232150`
- Configured marketplace in global settings

**Note**: Setup script has since been updated to v2.0 - it now correctly lists all 5 commands and no longer references the non-existent audit-runner.sh script.

### 2a. Marketplace Version Mismatch

**Issue**: The marketplace manifest at `.claude-plugin/marketplace.json` advertised the plugin as version "1.0.0" while the plugin's own `plugin.json` specified "2.0.0".

**Impact**: This version mismatch could cause Claude Code to load outdated plugin information or not recognize v2.0 capabilities.

**Fixed By**: Updated marketplace.json to advertise plugin version as "2.0.0" to match the actual plugin version.

### 3. Commands Not Recognized

**Issue**: SlashCommand tool consistently returns "Unknown slash command" error for all plugin commands.

**Commands Attempted**:
- `/architect` - Unknown slash command
- Various other invocations - All failed

**Command Files Verified**:
All 5 command files exist in the marketplace:
```
F:/projects/sb-marketplace/astro-dev/commands/
├── architect.md
├── audit.md
├── develop.md
├── implement.md
└── lookup.md
```

### 4. Local Command Copy

**Issue**: Marketplace plugin commands weren't automatically available to the project.

**Attempted Fix**: Copied all command files to project's `.claude/commands/` directory:
```bash
mkdir -p .claude/commands
cp F:/projects/sb-marketplace/astro-dev/commands/*.md .claude/commands/
```

**Result**: Commands still not recognized by SlashCommand tool.

## Plugin Manifest Configuration

From `F:/projects/sb-marketplace/astro-dev/.claude-plugin/plugin.json`:

```json
{
  "name": "astro-dev",
  "version": "2.0.0",
  "commands": {
    "develop": "commands/develop.md",
    "implement": "commands/implement.md",
    "architect": "commands/architect.md",
    "audit": "commands/audit.md",
    "lookup": "commands/lookup.md"
  },
  "agents": {
    "astro-orchestrator": { "path": "agents/astro-orchestrator.md" },
    "astro-developer": { "path": "agents/astro-developer.md" },
    "astro-auditor": { "path": "agents/astro-auditor.md" },
    "astro-architect": { "path": "agents/astro-architect.md" }
  }
}
```

## Root Cause Analysis

### Identified Issues (Fixed)

1. **Marketplace Version Mismatch** (FIXED): The marketplace.json advertised v1.0.0 while plugin.json specified v2.0.0 - now corrected
2. **Outdated Setup Script** (FIXED): Setup script showed old v1.0 information - now updated to v2.0

### Remaining Possible Causes

1. **Claude Code Restart Required**: Marketplace plugins might require Claude Code to be restarted after enabling or after version updates

2. **Command Format/Structure**: The command `.md` files might need specific frontmatter or structure that wasn't preserved when copying

3. **Marketplace Plugin Limitations**: Marketplace plugins might not support slash commands in the same way as project-local commands

4. **Plugin Loading Mechanism**: The plugin might load agents and skills correctly but not expose slash commands through the SlashCommand tool

5. **Configuration Propagation**: Changes to settings files might not propagate without restart

## Attempted Workarounds

### 1. Direct Agent Invocation (Interrupted by User)
Attempted to use Task tool with `general-purpose` subagent type to directly invoke the astro-architect agent logic by:
- Reading the agent file from marketplace
- Providing it with the architecture task
- Having it act as the architect agent

**Status**: Interrupted before completion - deemed too slow

### 2. Skills vs Commands
Plugin manifest defines both:
- **Skills**: `astro-coding`, `astro-knowledge`
- **Commands**: The 5 slash commands

Neither the Skill tool nor SlashCommand tool successfully invoked plugin functionality.

## Current State

- Plugin is "installed" according to UI
- Settings files configured (both local and global)
- Command files copied to project `.claude/commands/`
- Commands still not accessible via SlashCommand tool
- No way to invoke plugin functionality discovered

## Required to Proceed

One of the following is needed:

1. **Restart Claude Code** to reload plugin configuration
2. **Alternative invocation method** for marketplace plugin commands
3. **Direct agent usage** without slash command wrapper (via Task tool)
4. **Manual architecture design** without plugin assistance
5. **Plugin reinstallation** or different installation method

## CLAUDE.md Implications

The CLAUDE.md file contains extensive enforcement rules requiring use of the astro-dev plugin's slash commands (`/develop`, `/architect`, `/implement`, `/audit`, `/lookup`) for all Astro work.

**Problem**: These enforcement rules cannot be followed if the plugin commands are not accessible.

**Options**:
1. Fix plugin installation/configuration
2. Update CLAUDE.md to reflect actual available tooling
3. Create alternative workflow using Task tool with agent files directly

## Recommendation

**Short-term**: Use the Task tool to directly invoke agents by reading their agent files from the marketplace and providing them with context. This bypasses the slash command system.

**Long-term**: Investigate why marketplace plugin commands aren't loading and either:
- Fix the plugin installation process
- Update plugin to work with current Claude Code version
- Create project-local commands that invoke the marketplace agents
- Simplify CLAUDE.md to not require specific slash commands

## Files Modified

### In sb-marketplace Repository
- `.claude-plugin/marketplace.json` - Updated plugin version from 1.0.0 to 2.0.0 (FIXED)
- `setup.sh` - Previously updated to show v2.0 architecture (FIXED in earlier session)
- `plugin-usage.md` - This document, updated with corrected information

### In Project Repository
- `.claude/settings.local.json` - Added `enabledPlugins` section and `Bash(bash:*)` permission
- `.claude/commands/*.md` - Copied 5 command files from marketplace (not in git yet)

## Timeline

1. User requested architecture planning for multi-collection restructure
2. I attempted to use `/architect` command - failed
3. Checked for command files - not in project
4. Read marketplace README - confirmed commands should exist
5. Checked local settings - missing `enabledPlugins`
6. Added `enabledPlugins` - still failed
7. User suggested running setup script
8. Ran `F:/projects/sb-marketplace/setup.sh` - configured global settings
9. Copied command files to `.claude/commands/` - still failed
10. Attempted Task tool workaround - interrupted as too slow
11. Created this summary document

## Next Steps

**Issues Fixed**: Marketplace version mismatch and setup script have been corrected.

**Critical Next Step**: **Restart Claude Code** to ensure it loads the updated marketplace.json (v2.0.0) and recognizes plugin commands.

After restart, verify:
1. `/architect` and other plugin commands are recognized
2. Plugin skills can be invoked via Skill tool
3. Plugin agents are accessible

If commands still don't work after restart:
- A) Investigate Claude Code version compatibility with plugin marketplace feature
- B) Use Task tool with agent files directly (slower but functional)
- C) Create project-local commands that invoke marketplace agents
- D) Update CLAUDE.md to use Task tool instead of slash commands
