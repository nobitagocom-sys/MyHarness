# Timestamp Protocol — MANDATORY

Every `Timestamp:` field in the orchestrator log MUST use the real system clock.

## How to get the real timestamp

**ALWAYS** run via the `Bash` tool immediately before writing any orchestrator log entry:

```bash
date '+%Y-%m-%d %H:%M:%S'
```

Use the exact output as the `Timestamp:` value. **Never hardcode, estimate, or pre-calculate.**

## Incremental Writing Rule — ⛔ STRICTLY ENFORCED

```
BEFORE delegating to agent N:
    1. Bash: date '+%Y-%m-%d %H:%M:%S'
    2. Append [PROCESSING] STEP N entry to orchestrator log
    3. Delegate to agent N

AFTER agent N returns:
    4. Bash: date '+%Y-%m-%d %H:%M:%S'
    5. Append [PROCESSING] STEP N — COMPLETE entry
    6. Proceed to gate check
```

**⛔ PROHIBITED:** Pre-writing multiple future step entries or writing the full orchestrator log in one batch.
