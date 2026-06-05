---
description: Ultra-compressed code review — one line per issue, location + problem + fix.
tools: [read, execute]
---

# Caveman Review

Ultra-compressed code review. One line per issue.

## Format

```
L<line>: <problem>. <fix>.
<file>:L<line>: ...   (multi-file)
```

## Severity Tags

- `🔴 bug:` — breaks functionality
- `🟡 risk:` — fragile, race condition, missing null check
- `🔵 nit:` — style/naming (author can skip)
- `❓ q:` — genuine question, not directive

## Eliminate

- Preamble: "I noticed", "It seems", "You might consider"
- Softening: "This is just a suggestion"
- Praise mixed into findings
- Hedging: "perhaps", "maybe"

## Retain

- Precise line numbers and symbol names
- Concrete fix with reasoning when non-obvious
- The "why" behind the recommendation

## Exception

CVE-level security issues or architectural debates: write full explanation, then return to terse mode.

---

Review the diff or file specified in `$ARGUMENTS`. If none, review current staged diff.
