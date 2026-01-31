# Sync Phase

Update GitHub issue with progress.

## Trigger

- `/project-mgmt sync`
- Stopping work
- Implementation complete

## Steps

1. Read plan.md, findings.md, progress.md
2. Generate status summary
3. If `gh` available:
   - `gh issue comment {n} --body "{summary}"`
   - `gh issue edit {n} --add-label "{phase}"`
4. Else: output markdown for manual posting

## Manual Format

```
## Progress Update

**Phase**: {phase}
**Completed**: {x}/{total} steps

### Summary
{brief}

### Next Steps
{remaining}
```
