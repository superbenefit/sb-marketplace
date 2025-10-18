# Knowledge Base Consolidation Plan

## Current State (17 files, ~2500 lines)

### Files by Category:
1. **astro-syntax/** (5 files)
   - component-structure.md
   - configuration.md
   - directives.md
   - imports.md
   - routing.md

2. **common-mistakes/** (1 file)
   - common-mistakes.md (~720 lines)

3. **best-practices/** (3 files)
   - astro-best-practices.md (~605 lines)
   - starlight-patterns.md
   - typescript-patterns.md

4. **architecture-patterns/** (2 files)
   - content-collections-reference.md
   - routing-pages-reference.md

5. **loader-examples/** (1 file)
   - content-loader-api.md

6. **integration-guides/** (1 file)
   - external-data-integration.md

7. **audit/** (2 files)
   - audit-checklist.md
   - code-quality-standards.md (GENERIC - TO REMOVE)

8. **starlight/** (1 file)
   - starlight-specific.md

9. **Root** (1 file)
   - README.md

## Target State (5 files, ~1500 lines)

### 1. error-catalog.md (~400 lines)
**Merges**: common-mistakes.md + parts of astro-best-practices.md + audit-checklist.md
**Content**:
- Critical errors with fixes
- Common pitfalls indexed by symptom
- Error prevention patterns
- Quick fixes reference

### 2. astro-patterns.md (~400 lines)
**Merges**: astro-syntax/* + architecture-patterns/* + parts of best-practices
**Content**:
- Component patterns
- Routing patterns
- Collection patterns
- Configuration patterns
- Directive usage
- Import patterns

### 3. starlight-guide.md (~300 lines)
**Merges**: starlight-specific.md + starlight-patterns.md
**Content**:
- Starlight configuration
- Starlight components
- Starlight-specific patterns
- Theme customization

### 4. integrations.md (~300 lines)
**Merges**: integration-guides/ + loader-examples/ + TypeScript patterns
**Content**:
- External data integration
- Custom loaders
- TypeScript configuration
- Integration patterns

### 5. README.md (~100 lines)
**Purpose**: Navigation and quick reference
**Content**:
- Knowledge base overview
- File index
- Quick links
- Common lookup paths

## Files to Remove

- audit/code-quality-standards.md (generic web standards, not Astro-specific)
- All original category directories after consolidation

## Token Reduction Strategy

### Current Issues:
- **30-40% redundancy** across files
- Common mistakes shown in 3+ different files
- Best practices duplicated with different examples
- Syntax references repeated in multiple places

### Consolidation Benefits:
- **Single source of truth** for each pattern
- **Cross-referenced** instead of duplicated
- **Indexed by symptom** for faster lookup
- **~50% token reduction** when loaded

## Implementation Steps

1. Create error-catalog.md (merge mistakes + fixes)
2. Create astro-patterns.md (merge syntax + architecture)
3. Create starlight-guide.md (merge starlight files)
4. Create integrations.md (merge loaders + integrations)
5. Update README.md (navigation)
6. Remove old directories
7. Update references in skills/agents

## Validation Checklist

- [ ] All critical errors preserved
- [ ] All patterns accessible
- [ ] Cross-references work
- [ ] No information lost
- [ ] Token count reduced
- [ ] Skills/agents updated
- [ ] README accurate

## Expected Outcome

**Before**: 17 files, ~8000 tokens when fully loaded
**After**: 5 files, ~4000 tokens when fully loaded
**Reduction**: 50% token efficiency gain
