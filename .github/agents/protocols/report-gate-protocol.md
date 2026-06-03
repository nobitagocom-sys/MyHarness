# Report Hard Gate Protocol

## ⛔ MANDATORY BEFORE NEXT STEP

After each step completes, the orchestrator MUST enforce this gate before proceeding:

```
STEP N completes
    │
    ▼
CHECK: Does docs/output/run-logs/<feature-id>/reports/<NN>-<phase>-report.md EXIST?
    │
    ├─ NO → BLOCKED. Generate the report NOW using data already produced.
    │        Write orchestrator log: [REPORT GATE] STEP N — report generated (late).
    │
    └─ YES → CHECK: Does report contain ALL required sections?
                │
                ├─ NO → ADD missing section inline. Re-write file.
                │        Write orchestrator log: [REPORT GATE] STEP N — patched missing section: <name>.
                │
                └─ YES → CHECK: Any unresolved [NEEDS CLARIFICATION] markers?
                            │
                            ├─ YES → Auto-resolve every item. Patch report.
                            │        Write orchestrator log: [REPORT GATE] STEP N — auto-resolved N TBC items.
                            │
                            └─ NO → ✅ GATE PASSED → Advance to STEP N+1
```

## Required Report Sections (all steps)

1. `## Summary` — brief phase outcome
2. `## Artifacts Produced` — list of all files written (with paths)
3. `## [AUTO-RESOLVED] Assumptions` — auto-resolved clarifications
4. `## [NEEDS CLARIFICATION] Items` — remaining unresolved items (should be empty in built-in mode)
5. `## Issues & Retries` — record of rejected verdicts and retry attempts
6. `## Next Step` — what step follows and what inputs it will receive

## Step-Specific Additional Sections

| Step | Additional Required Section |
|------|-----------------------------|
| STEP 4 | `## QA Summary` — full table of questions + auto-resolved answers |
| STEP 10 | `## Test Results` — pass/fail table per test class, Istanbul/c8 coverage % | `## Screen Verification` — per-screen: ID, HTTP status, render OK/FAIL |
| STEP 13 | `## Launch Status` — FE/BE startup, DB seed count, screen accessibility |
