# Steps 5–7: Review Phase

> orchestrator MUST read this file before executing Steps 5–7.
> Protocols referenced: `protocols/gate-retry-protocol.md`, `protocols/report-gate-protocol.md`

---

## STEP 5 — Thorough Spec Review (Auto-Retry)

| Key | Value |
|-----|-------|
| Agent | `myharness.review.spec` |
| Model | `claude-sonnet-4-6` |
| Input | `spec.md`, `docs/output/design-docs/srs/srs-<MOD-ID>-<short-name>.md`, `constitution.md` |
| Report | `reports/05-review-spec-report.md` |
| Gate | REVIEW GATE (Auto-Retry) + REPORT HARD GATE |
| Fix agent | `myharness.specify` |
| Max retries | 5 |

**Gate logic:**

- ✅/⚠️ → proceed to Step 6
- ❌ REJECTED → invoke `myharness.specify` to fix CRITICAL issues → re-invoke `myharness.review.spec` → repeat until pass or retry > 5
- Escalation after 5 retries → continue to Step 6

> ⛔ **[REPORT GATE]** per `protocols/report-gate-protocol.md`

---

## STEP 6 — Implementation Planning

| Key | Value |
|-----|-------|
| Agent | `myharness.plan` |
| Model | `gpt-5-3-codex` |
| Input | `spec.md`, `constitution.md`, `docs/technical_architecture.md` |
| Output | `plan.md`, `data-model.md`, `contracts/` |
| Report | `reports/06-plan-report.md` |
| Gate | REPORT HARD GATE + Auto-Resolve |

**Delegation `$ARGUMENTS`:**

```yaml
feature-id: <feature-id>
module-id: <mod-id>
pipeline-context: docs/output/run-logs/<feature-id>/run-context.yaml
```

**After completion:** Auto-resolve any `[NEEDS CLARIFICATION]` markers in plan artifacts.

> ⛔ **[REPORT GATE]** per `protocols/report-gate-protocol.md`

---

## STEP 7 — Plan Conformance Review (Auto-Retry)

| Key | Value |
|-----|-------|
| Agent | `myharness.review.plan` |
| Model | `claude-sonnet-4-6` |
| Input | `plan.md`, `spec.md`, `data-model.md`, `docs/technical_architecture.md` |
| Report | `reports/07-review-plan-report.md` |
| Gate | REVIEW GATE (Auto-Retry) + REPORT HARD GATE |
| Fix agent | `myharness.plan` |
| Max retries | 5 |

**Gate logic:**

- ✅/⚠️ → proceed to Step 8
- ❌ REJECTED → invoke `myharness.plan` to fix → re-invoke `myharness.review.plan` → repeat
- Escalation after 5 retries → continue to Step 8

> ⛔ **[REPORT GATE]** per `protocols/report-gate-protocol.md`
