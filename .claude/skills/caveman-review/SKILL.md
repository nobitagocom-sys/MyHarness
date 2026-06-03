# Caveman Review

Ultra-compressed code review feedback — location, problem, fix — one line per issue.

## Activation

Trigger: "review this PR", "code review", `/review`, `/caveman-review`

## Format

```
L<line>: <problem>. <fix>.
<file>:L<line>: ...   (for multi-file reviews)
```

## Severity Tags

- `🔴 bug:` — breaks functionality, risks incidents
- `🟡 risk:` — functional but fragile (race conditions, null checks, error handling)
- `🔵 nit:` — style/naming/minor optimization (author can skip)
- `❓ q:` — genuine inquiry, not directive

## Eliminate

- Preamble: "I noticed", "It seems", "You might consider"
- Softening: "This is just a suggestion"
- Praise mixed into findings
- Code restating (reviewer can read the diff)
- Hedging: "perhaps", "maybe"

## Retain

- Precise line numbers and symbol names (backtick formatting)
- Concrete fixes with reasoning when non-obvious
- The "why" behind the recommendation

## Exception

For security vulnerabilities (CVE-level), architectural debates, or new-contributor contexts: write full explanation, then return to terse mode.
