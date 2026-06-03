# Gate Retry Protocol (No-Halt Mode)

When any review gate returns **REJECTED**, the pipeline does NOT stop.

## Gate Retry Loop

```
REJECTED verdict received
    │
    ├─ Extract CRITICAL issues list from review report
    ├─ Write [ISSUE] entry in orchestrator log
    ├─ Increment retry counter for this gate
    │
    ├─ If retry counter = 3 (model escalation threshold):
    │      Check .harness/models/catalog.yaml escalation section
    │      If fix agent is synthesis or coding tier → escalate to review tier for this retry
    │      Write [MODEL-ESCALATION] entry in orchestrator log
    │      Continue retry loop with escalated model
    │
    ├─ If retry counter ≤ 5:
    │      Invoke fix agent with CRITICAL issues list
    │      Re-invoke review agent
    │      Evaluate new verdict → repeat if still REJECTED
    │
    └─ If retry counter > 5:
           Write [ESCALATION] entry in orchestrator log
           Mark step as "ESCALATED — Partial Pass"
           Continue pipeline with known limitations documented
```

## Model Escalation Policy

Read `.harness/models/catalog.yaml` for tier definitions and `escalation.synthesis_fail_after` / `escalation.coding_fail_after` thresholds.

| Fix Agent Tier | Escalates To | Threshold |
|---------------|-------------|-----------|
| synthesis (GPT-5.4) | review (claude-sonnet-4-6) | retry 3 |
| coding (GPT-5.3-Codex) | review (claude-sonnet-4-6) | retry 3 |
| review tier | no escalation | — |

Escalation applies to the **fix agent only** — the review agent remains unchanged.

## Fix Agent Selection per Gate

| Gate Step | Review Agent | Fix Agent | Fix Instruction |
|-----------|-------------|-----------|-----------------|
| Step 5  | `myharness.review.spec` | `myharness.specify` | "Fix CRITICAL spec issues: <list>. Re-generate affected sections of spec.md." |
| Step 7  | `myharness.review.plan` | `myharness.plan` | "Fix CRITICAL plan conformance issues: <list>. Update plan.md." |
| Step 11 | `myharness.review.code` | `myharness.implement` | "Fix CRITICAL code review issues: <list>. Apply minimal targeted fixes." |
| Step 12 | `myharness.testkit` | `myharness.implement` | "Fix CRITICAL test failures tracing to SRS/BD/DD: <failed test list>." |

## BACK-TO-PLAN Fix Cycle (Step 12 only)

When Step 12 tests FAIL, unlike other gates, this triggers a **full fix cycle** from STEP 6:

1. Extract ALL failed test cases with design document references
2. Write `[BACK-TO-PLAN]` entry in orchestrator log
3. Re-invoke pipeline from STEP 6 → 7 → 8 → 8b → 9 → 10 → 11 → 12
4. Max **3 full cycles**. After 3 cycles: write `[ESCALATION]`, proceed to Step 13 anyway.
