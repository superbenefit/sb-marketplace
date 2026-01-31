# Start Phase

Initialize project directory and files.

## Trigger

- `/project-mgmt start #123`
- Complex task detected (>5 tool calls estimated)
- User says "work on issue"

## Steps

1. If issue number provided: `gh issue view {n} --json title,body,labels`
2. Create `.project/{issue#}/` directory
3. Copy templates from `assets/`
4. Fill Goal section from issue body
5. Set phase to "specify" in plan.md

## Next

Read `references/specify.md`
