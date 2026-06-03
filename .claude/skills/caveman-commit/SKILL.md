# Caveman Commit

Ultra-compressed commit message generator using Conventional Commits format.

## Activation

Trigger: "write a commit", "commit message", "generate commit", `/commit`, `/caveman-commit`

## Format

```
<type>(<scope>): <summary>
```

- Subject line ≤50 chars ideally, hard cap 72
- Imperative mood: "add", "fix", "remove" (not past tense)
- Body only when reasoning isn't self-evident

## Prohibited

- "This commit does X"
- First-person language
- "Generated with Claude Code" attribution
- Unnecessary emoji (unless project convention demands)

## Always include body for

- Breaking changes
- Security fixes
- Data migrations
- Anything reverting a prior commit

## Scope

Generates message text only — does not execute git operations, stage files, or amend commits. Output as code block ready to paste.
