# Astro Dev Plugin Architecture Specification v2.0

## Executive Summary

This document specifies a complete architectural reorganization of the astro-dev Claude Code plugin to implement an intelligent, orchestrator-based system with clear separation between agents (who do work) and skills (what capabilities they have).

**Key Changes:**
- Introduction of an intelligent orchestrator agent for task coordination
- Clear agent/skill separation with smart context loading
- Adaptive audit system with three rigor levels
- 40-50% token reduction through consolidation
- Removal of broken components and redundancies

---

## 1. Architecture Overview

### 1.1 Core Principles

1. **Agents perform actions** - They implement, audit, design, and orchestrate
2. **Skills provide capabilities** - They inject context and patterns when needed
3. **Orchestrator coordinates** - Central intelligence for task management
4. **Adaptive rigor** - Audit intensity scales with task complexity
5. **Token efficiency** - Load only what's needed, when it's needed

### 1.2 System Flow

```
User Request
    ↓
/develop Command (primary entry)
    ↓
┌─────────────────────────────┐
│   astro-orchestrator        │
│   (Analyzes & Plans)        │
└──────────┬──────────────────┘
           ↓
    Task Execution Plan
           ↓
┌──────────┴───────────────────┬────────────────┬──────────────┐
│                              │                │              │
▼                              ▼                ▼              ▼
astro-architect            astro-developer   astro-auditor   [Future]
(Design complex systems)   (Write code)      (Validate)
│                              │                │
└──────────────────────────────┴────────────────┘
                               │
                        Skills Layer
                               │
           ┌───────────────────┴────────────────────┐
           ▼                                        ▼
      astro-coding                            astro-knowledge
   (Implementation patterns)                  (API documentation)
```

---

## 2. Agent Specifications

### 2.1 astro-orchestrator Agent (NEW)

**File:** `astro-dev/agents/astro-orchestrator.md`
**Purpose:** Intelligent task coordinator and resource optimizer
**Size:** ~300 lines

#### Responsibilities
- Analyze user requests and break into execution steps
- Determine which agents to invoke and in what order
- Calibrate audit rigor based on task complexity
- Optimize token usage through selective context loading
- Manage parallel execution and agent handoffs
- Aggregate results and present to user

#### Decision Matrix

| Task Type | Execution Plan | Audit Level |
|-----------|---------------|-------------|
| Quick Fix (<10 lines) | developer → auditor | Light (5 checks) |
| Single Feature | developer → auditor | Medium (20 checks) |
| Complex Feature | architect → developer → auditor | Comprehensive (50+ checks) |
| Task Series | (dev + light) × N → comprehensive | Light each, full at end |
| Refactoring | auditor → developer(parallel) → auditor | Pre-scan + comprehensive |

#### Implementation Logic

```markdown
## Execution Planning Algorithm

1. PARSE REQUEST
   - Identify task type and scope
   - Estimate complexity (lines, files, risk)
   - Detect series vs. single task

2. DETERMINE AGENTS
   if complex_architecture_needed:
       agents.add(astro-architect)
   agents.add(astro-developer)
   if validation_needed:
       agents.add(astro-auditor)

3. SET AUDIT RIGOR
   if lines < 20 and files == 1:
       audit_level = "light"
   elif is_last_in_series:
       audit_level = "comprehensive"
   elif touches_critical_areas:
       audit_level = "comprehensive"
   else:
       audit_level = "medium"

4. OPTIMIZE TOKENS
   - Load only relevant skill sections
   - Share context between parallel agents
   - Clear after task completion

5. EXECUTE
   - Launch agents per plan
   - Monitor progress
   - Handle failures
   - Aggregate results
```

### 2.2 astro-developer Agent (NEW)

**File:** `astro-dev/agents/astro-developer.md`
**Purpose:** Primary code implementation specialist
**Size:** ~200 lines

#### Responsibilities
- Receive implementation requests from orchestrator
- Load relevant astro-coding skill sections
- Write Astro/Starlight code following best practices
- Self-review against patterns before submission
- Pass to auditor for validation

#### Workflow
1. Receive task from orchestrator with context
2. Analyze requirements and identify needed patterns
3. Request relevant astro-coding skill sections
4. Implement solution using enhanced context
5. Perform self-check against loaded patterns
6. Return implementation to orchestrator

### 2.3 astro-auditor Agent (ENHANCED)

**File:** `astro-dev/agents/astro-auditor.md`
**Purpose:** Adaptive code validation with configurable rigor
**Size:** ~200 lines (reorganized)

#### Three Audit Levels

##### Light Audit (5 checks, ~30 seconds)
- Syntax validation
- Import path correctness
- Module resolution (`astro:content` vs `astro/content`)
- Breaking change detection
- Basic TypeScript validity

##### Medium Audit (20 checks, ~2 minutes)
- All Light checks plus:
- Best practices compliance
- Performance patterns
- Security basics
- Component structure
- Routing patterns
- State management
- Error handling
- Basic accessibility
- Code duplication
- Naming conventions

##### Comprehensive Audit (50+ checks, ~5 minutes)
- All Medium checks plus:
- Architecture review
- Full accessibility scan
- Complete security audit
- Documentation completeness
- Test coverage analysis
- Bundle size impact
- SEO compliance
- i18n readiness
- Performance metrics
- Dependency analysis

#### Adaptive Triggers

```markdown
## Auto-Level Selection

def determine_audit_level(task_context):
    # Explicit override
    if task_context.user_specified_level:
        return task_context.user_specified_level

    # Small changes
    if task_context.lines_changed < 20 and task_context.files_count == 1:
        return "light"

    # End of series
    if task_context.is_last_in_series:
        return "comprehensive"

    # Critical areas
    if any(area in task_context.touched_areas for area in
           ['auth', 'payments', 'user_data', 'security']):
        return "comprehensive"

    # Large changes
    if task_context.files_count > 5 or task_context.lines_changed > 100:
        return "comprehensive"

    # Default
    return "medium"
```

### 2.4 astro-architect Agent (EXISTING)

**File:** `astro-dev/agents/astro-architect.md`
**Purpose:** Complex system design and architecture planning
**Size:** ~250 lines (optimized from 340)

No major changes, but:
- Make discoverable via `/architect` command
- Optimize token usage by removing redundant examples
- Better integration with orchestrator

---

## 3. Skill Specifications

### 3.1 astro-coding Skill (RENAMED from astro-developer)

**Directory:** `astro-dev/skills/astro-coding/`
**Purpose:** Smart context injection for code implementation
**Loading:** Task-based automatic when code writing detected

#### Structure
```
astro-coding/
├── SKILL.md (50 lines - loading logic)
├── patterns/
│   ├── components.md (component patterns)
│   ├── routing.md (routing patterns)
│   ├── collections.md (collection patterns)
│   ├── configuration.md (config patterns)
│   ├── typescript.md (TS patterns)
│   └── common-mistakes.md (error prevention)
└── index.json (task-to-pattern mapping)
```

#### Smart Loading System

```json
// index.json
{
  "task_patterns": {
    "component": ["patterns/components.md", "patterns/typescript.md"],
    "route": ["patterns/routing.md", "patterns/typescript.md"],
    "page": ["patterns/routing.md", "patterns/components.md"],
    "collection": ["patterns/collections.md", "patterns/typescript.md"],
    "config": ["patterns/configuration.md"],
    "layout": ["patterns/components.md", "patterns/routing.md"],
    "api": ["patterns/routing.md", "patterns/typescript.md"],
    "integration": ["patterns/configuration.md", "patterns/typescript.md"],
    "all": ["patterns/*.md"]
  },

  "auto_detection": {
    "keywords_to_patterns": {
      "getStaticPaths": ["patterns/routing.md"],
      "defineCollection": ["patterns/collections.md"],
      "astro.config": ["patterns/configuration.md"],
      "client:": ["patterns/components.md"],
      ".astro": ["patterns/components.md"]
    }
  }
}
```

#### SKILL.md Content

```markdown
# astro-coding Skill

## Purpose
Provide smart, context-aware implementation patterns for Astro/Starlight development

## Loading Strategy
This skill uses selective loading based on task detection:

1. Task keyword analysis
2. File extension detection
3. Import statement scanning
4. Pattern matching

## Usage by Agents
- astro-developer: Primary consumer for implementation
- astro-architect: Uses for example generation
- astro-auditor: References for fix suggestions
- astro-orchestrator: Determines which sections to load

## Critical Rules (Always Loaded)
1. ALWAYS use file extensions in imports (.astro, .ts, .js)
2. Use `astro:content` NOT `astro/content` for content imports
3. Use `class` NOT `className` in .astro files
4. Await async operations outside template literals
5. Never expose secrets in client-side code

[Modular patterns loaded as needed below...]
```

### 3.2 astro-knowledge Skill (RENAMED from astro-docs)

**Directory:** `astro-dev/skills/astro-knowledge/`
**Purpose:** API documentation and reference lookup
**Loading:** On-demand when verification needed

#### Structure
```
astro-knowledge/
├── SKILL.md (50 lines - lookup logic)
├── api-index.json (searchable API index)
├── references/
│   ├── llms-full.md (comprehensive docs)
│   ├── docs-index.md (navigation)
│   └── mcp-integration.md (MCP server usage)
└── cache/ (frequently accessed items)
```

---

## 4. Command Specifications

### 4.1 /develop Command (NEW - Primary Entry)

**File:** `astro-dev/commands/develop.md`
**Purpose:** Main entry point for orchestrated development
**Size:** 50 lines

```markdown
# /develop Command

Intelligent development orchestration for any Astro task.

## Usage
/develop [any development request]

## Examples
- /develop Add a blog with pagination
- /develop Fix all TypeScript errors
- /develop Refactor components to use TypeScript
- /develop Create a multi-language setup

## What Happens
1. Request analyzed by astro-orchestrator
2. Execution plan created
3. Agents invoked as needed
4. Results aggregated and presented

## When to Use
Use /develop for any development task where you want intelligent orchestration.
For direct agent access, use specific commands (/implement, /audit, /architect).
```

### 4.2 Other Commands (Updated)

| Command | Purpose | Invokes | Size |
|---------|---------|---------|------|
| /implement | Direct implementation | astro-developer | 50 lines |
| /architect | Direct architecture planning | astro-architect | 50 lines |
| /audit [level] | Direct validation | astro-auditor | 50 lines |
| /lookup | Quick API reference | astro-knowledge | 50 lines |

---

## 5. Knowledge Base Consolidation

### Current State
- 17 files across multiple directories
- ~2,500 lines total
- 20-30% redundancy
- Token usage: ~6,000-8,000 when loaded

### Target State
- 5 consolidated files
- ~1,500 lines total
- No redundancy
- Token usage: ~3,000-4,000 when loaded

### Consolidation Plan

| Original Files | New File | Content | Lines |
|---------------|----------|---------|-------|
| common-mistakes.md, astro-best-practices.md | error-catalog.md | Merged error patterns and solutions | ~400 |
| astro-syntax/*, architecture-patterns/* | astro-patterns.md | Core Astro patterns and syntax | ~400 |
| starlight/*, starlight-patterns.md | starlight-guide.md | Starlight-specific patterns | ~300 |
| integration-guides.md, loader-examples.md | integrations.md | External integrations and loaders | ~300 |
| README.md | README.md | Navigation and overview | ~100 |

**To Remove:**
- `code-quality-standards.md` - Generic web standards, not Astro-specific
- Redundant examples across files
- Duplicate pattern descriptions

---

## 6. File Structure (Final)

```
sb-marketplace/
├── ARCHITECTURE_SPEC.md (this document)
├── README.md (user-facing docs)
├── .gitignore
├── .claude-plugin/
│   └── marketplace.json
├── astro-dev/
│   ├── .claude-plugin/
│   │   └── plugin.json
│   ├── .mcp.json (MCP server config)
│   ├── agents/
│   │   ├── astro-orchestrator.md (NEW ~300 lines)
│   │   ├── astro-developer.md (NEW ~200 lines)
│   │   ├── astro-auditor.md (UPDATED ~200 lines)
│   │   └── astro-architect.md (EXISTING ~250 lines)
│   ├── skills/
│   │   ├── astro-coding/ (RENAMED)
│   │   │   ├── SKILL.md (~50 lines)
│   │   │   ├── patterns/ (6 files, modular)
│   │   │   └── index.json (pattern mapping)
│   │   └── astro-knowledge/ (RENAMED)
│   │       ├── SKILL.md (~50 lines)
│   │       ├── api-index.json
│   │       └── references/ (3 files)
│   ├── commands/
│   │   ├── develop.md (NEW ~50 lines)
│   │   ├── implement.md (~50 lines)
│   │   ├── architect.md (NEW ~50 lines)
│   │   ├── audit.md (~50 lines)
│   │   └── lookup.md (~50 lines, renamed)
│   ├── knowledge-base/
│   │   ├── error-catalog.md (~400 lines)
│   │   ├── astro-patterns.md (~400 lines)
│   │   ├── starlight-guide.md (~300 lines)
│   │   ├── integrations.md (~300 lines)
│   │   └── README.md (~100 lines)
│   ├── hooks/
│   │   └── hooks.json (simplified, no shell scripts)
│   ├── LICENSE
│   ├── CHANGELOG.md
│   └── README.md
└── setup.sh
```

**Files to Remove:**
- `astro-dev/scripts/audit-runner.sh` - Broken with syntax errors
- `astro-dev/commands/docs-lookup.md` - Renamed to lookup.md
- 12 knowledge-base files - Consolidated into 5

---

## 7. Implementation Sequence

### Phase 1: Core Architecture (Priority 1)
1. Create astro-orchestrator agent
2. Create astro-developer agent
3. Update astro-auditor with adaptive levels
4. Create /develop command

### Phase 2: Skill Reorganization (Priority 2)
5. Rename astro-developer skill → astro-coding
6. Reorganize astro-coding for modular loading
7. Rename astro-docs skill → astro-knowledge
8. Create pattern index files

### Phase 3: Command Updates (Priority 3)
9. Add /architect command
10. Update existing commands
11. Rename /docs-lookup → /lookup

### Phase 4: Cleanup (Priority 4)
12. Consolidate knowledge base (17→5 files)
13. Remove audit-runner.sh script
14. Update all manifests
15. Update documentation

---

## 8. Token Efficiency Analysis

### Current Token Usage (Worst Case)
- Full knowledge base load: ~8,000 tokens
- All skills loaded: ~2,000 tokens
- Commands/agents: ~1,500 tokens
- **Total:** ~11,500 tokens per request

### Optimized Token Usage

#### Simple Task (e.g., "Add Footer component")
- Orchestrator: 300 tokens
- Developer agent: 200 tokens
- Coding skill (components only): 200 tokens
- Light audit: 100 tokens
- **Total:** ~800 tokens (93% reduction)

#### Medium Task (e.g., "Add blog listing")
- Orchestrator: 300 tokens
- Developer agent: 200 tokens
- Coding skill (routes + collections): 400 tokens
- Medium audit: 300 tokens
- **Total:** ~1,200 tokens (89% reduction)

#### Complex Task (e.g., "Refactor all components")
- Orchestrator: 300 tokens
- Architect: 250 tokens
- Developer: 200 tokens
- Full coding skill: 1,000 tokens
- Comprehensive audit: 500 tokens
- **Total:** ~2,250 tokens (80% reduction)

---

## 9. Testing Strategy

### Validation Checkpoints

1. **Orchestrator Logic**
   - Test task parsing accuracy
   - Verify agent selection
   - Validate audit level determination
   - Check parallel execution

2. **Agent Coordination**
   - Test handoffs between agents
   - Verify context sharing
   - Check error handling
   - Validate result aggregation

3. **Skill Loading**
   - Test pattern detection
   - Verify selective loading
   - Check context relevance
   - Measure token usage

4. **Audit Levels**
   - Test light audit (5 checks)
   - Test medium audit (20 checks)
   - Test comprehensive audit (50+ checks)
   - Verify adaptive triggers

---

## 10. Migration Notes

### Breaking Changes
1. `/docs-lookup` renamed to `/lookup`
2. `astro-developer` skill renamed to `astro-coding`
3. `astro-docs` skill renamed to `astro-knowledge`
4. Hooks no longer use shell scripts

### User Impact
- Primary workflow now through `/develop`
- More intelligent task handling
- Faster execution for simple tasks
- Better audit coverage without over-checking

### Backward Compatibility
- Old commands still work but bypass orchestrator
- Skills can be referenced by old names (aliased)
- Knowledge base remains accessible

---

## 11. Success Metrics

### Quantitative
- 40-50% average token reduction
- 70% reduction for simple tasks
- 3x faster execution for small changes
- 50% fewer false positive audit warnings

### Qualitative
- Clearer agent/skill separation
- More discoverable features
- Intelligent task handling
- Adaptive quality assurance

---

## 12. Example Workflows

### Example 1: Quick Component Fix
```
User: /develop Fix Footer component spacing

Orchestrator Analysis:
- Task: Simple style fix
- Scope: 1 file, <10 lines
- Risk: Low

Execution:
1. astro-developer (with components pattern)
2. astro-auditor (light check - syntax only)

Result: Fixed in 30 seconds with 800 tokens
```

### Example 2: Blog Implementation
```
User: /develop Add a blog with categories and tags

Orchestrator Analysis:
- Task: Multi-part feature
- Scope: Collections, routing, components
- Risk: Medium

Execution:
1. astro-architect (design collection structure)
2. astro-developer (parallel):
   - Create collections
   - Build listing pages
   - Add tag cloud component
3. astro-auditor (medium check)

Result: Implemented in 5 minutes with 2,500 tokens
```

### Example 3: Codebase Refactor
```
User: /develop Convert all .js files to TypeScript

Orchestrator Analysis:
- Task: Large refactoring
- Scope: Multiple files
- Risk: High (breaking changes possible)

Execution:
1. astro-auditor (scan all type issues)
2. Group files by directory
3. astro-developer × N (parallel conversion)
4. astro-auditor (comprehensive validation)

Result: Refactored in 10 minutes with 4,000 tokens
```

---

## Appendix A: Removed Components

### audit-runner.sh Issues
- Line 61: Broken regex for import detection
- Line 76: Unreliable awk pattern for await detection
- Line 83: Syntax error in environment variable regex
- Only performs 6 checks vs 50+ in agent
- Cannot invoke agents (shell vs Claude boundary)
- No user feedback mechanism

### Redundant Knowledge Base Files
1. `code-quality-standards.md` - Generic web dev, not Astro
2. `audit-checklist.md` - Duplicated in agent
3. `astro-imports.md` - Merged into patterns
4. `astro-components.md` - Merged into patterns
5. `astro-routing.md` - Merged into patterns
6. `astro-configuration.md` - Merged into patterns
7. Multiple overlapping best practice files

---

## Appendix B: Configuration Updates

### plugin.json Changes
```json
{
  "skills": {
    "astro-coding": "...",  // renamed
    "astro-knowledge": "..." // renamed
  },
  "agents": {
    "astro-orchestrator": "...", // new
    "astro-developer": "...",    // new
    "astro-auditor": "...",      // updated
    "astro-architect": "..."     // existing
  },
  "commands": {
    "develop": "...",    // new primary
    "implement": "...",  // updated
    "architect": "...",  // new
    "audit": "...",     // updated
    "lookup": "..."     // renamed
  }
}
```

### hooks.json Simplification
```json
{
  "hooks": {
    "PostToolUse": [],  // Removed broken shell script
    "PreToolUse": []    // Simplified
  }
}
```

---

## Document Version

**Version:** 2.0
**Date:** 2025-10-18
**Author:** Claude (Anthropic)
**Status:** Ready for Implementation

This specification represents a complete architectural overhaul designed to create an intelligent, efficient, and user-friendly development assistant for Astro and Starlight projects.