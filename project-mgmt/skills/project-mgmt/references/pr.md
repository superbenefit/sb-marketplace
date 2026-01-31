# PR Phase

Create pull request for completed implementation.

## Trigger

- Phase is "implement" and all steps checked
- `/project-mgmt pr`
- Ready to submit work for review

## Prerequisites

- All implementation steps in plan.md are checked off
- Tests pass
- Code follows project conventions

## Steps

1. Read plan.md to get issue number and summary
2. Ensure on feature branch (create if needed):
   ```bash
   git checkout -b {issue#}-{brief-description}
   ```
3. Stage and commit changes:
   ```bash
   git add -A
   git commit -m "feat(scope): description

   Closes #{issue}"
   ```
4. Push branch:
   ```bash
   git push -u origin HEAD
   ```
5. Create PR using gh CLI:
   ```bash
   gh pr create --title "{title}" --body "{body}" --base main
   ```
6. Update plan.md phase → "review"

## PR Body Template

```
## Summary

{Brief description from plan.md Goal section}

## Related Issue

Closes #{issue}

## Changes

{List main changes from implementation steps}

## Spec Compliance

- [x] Spec exists at `.project/{issue#}/spec.md`
- [x] Implementation matches spec requirements

## Checklist

- [x] Code follows project conventions
- [x] Self-review completed
- [x] plan.md steps are checked off
```

## If gh CLI unavailable

Output the PR body for manual creation and provide instructions.

## Next

Read `references/sync.md`
