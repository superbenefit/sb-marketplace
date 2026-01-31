# Plan Phase

Create implementation approach in plan.md.

## Trigger

- Phase is "plan"
- spec.md exists

## Steps

1. Read spec.md
2. Update plan.md:
   - Approach summary
   - Tech stack (record decisions in findings.md)
   - Numbered implementation steps with checkboxes
   - Validation criteria
3. Update plan.md phase → "implement"

## Step Format

```
### Phase 1: {name}
- [ ] 1.1: {description}
  - Files: {paths}
  - Depends: {steps or "none"}
- [ ] 1.2: {description} [P]  ← parallelizable
```

## Next

Read `references/implement.md`
