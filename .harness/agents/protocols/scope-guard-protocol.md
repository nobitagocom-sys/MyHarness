# Scope Guard Protocol

orchestrator MUST run scope_guard before dispatching Step 10 (implement).

## When to Run

- Before ANY `myharness.implement` delegation
- Before Step 10 BE and FE parallel dispatch

## Command

```bash
python3 .harness/enforce/scope_guard.py --role implement --staged
```

## Log Entry

Write `[SCOPE-CHECK]` entry in `00-myharness.log.md`:

```markdown
## [SCOPE-CHECK] STEP 10 — Pre-dispatch
- **Timestamp:** <real timestamp>
- **Role:** implement
- **Result:** PASS / FAIL
- **Violations:** <list or "None">
- **Action:** PROCEED / BLOCK
```

## On FAIL

- Block dispatch
- Write `[SCOPE-VIOLATION]` entry
- Request implement agent to revert offending files
- Re-run scope_guard after revert
