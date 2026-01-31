# Implement Phase

Execute plan steps with progress tracking.

## Trigger

- Phase is "implement"
- plan.md has unchecked steps

## Loop

1. Find first `- [ ]` step in plan.md
2. If none: complete → read `references/pr.md`
3. Execute the step
4. Background update:
   ```
   Run the pm-bookkeeper agent in the background to check off step {N}
   ```
5. If error:
   ```
   Run the pm-bookkeeper agent in the background to log error: {description}
   ```
6. Continue immediately to next step

## 2-Action Rule

After every 2 search/view operations:
```
Run the pm-bookkeeper agent in the background to add to findings.md: {discoveries}
```

## Before Decisions

Re-read plan.md to refresh goals.
