---
description: Generate an ultra-compressed conventional commit message for staged changes.
tools: [execute]
---

# Caveman Commit

Generate conventional commit message. Terse. Accurate.

## Steps

1. Run `git diff --staged` to see staged changes
2. Analyze: what changed, why, scope
3. Output commit message as code block

## Format

```
<type>(<scope>): <summary>
```

- Subject ≤50 chars (hard cap 72)
- Imperative mood: "add", "fix", "remove"
- Body only when reasoning non-obvious

## Always include body for

- Breaking changes
- Security fixes
- Data migrations
- Reverts

## Prohibited

- "This commit does X"
- First-person language
- Unnecessary emoji
- Attribution lines

Output message only. No git execution.
