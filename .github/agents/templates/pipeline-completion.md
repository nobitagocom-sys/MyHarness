# Pipeline Completion Report Template

Use this template when all steps complete (with or without escalations).

```markdown
## ✅ Pipeline Complete (Autonomous Mode) — <feature-name>

**Feature Branch**: <branch>
**Date Completed**: <YYYY-MM-DD>
**Mode**: Built-in Autonomous (no human pauses)

| # | Step | Agent | Model | Status | Retries | Assumptions |
|---|------|-------|-------|--------|---------|-------------|
| 1 | SRS Generation | myharness.srs | GPT-5.4 | ✅ | 0 | N |
| 2 | BD Generation (External Design) | myharness.bd | GPT-5.4 | ✅ | 0 | N |
| 3 | Spec Creation | myharness.specify | GPT-5.4 | ✅ | 0 | N |
| 4 | Spec Clarification | myharness.clarify | GPT-5.4 | ✅ | 0 | N |
| 5 | Thorough Spec Review | myharness.review.spec | claude-sonnet-4-6 | ✅ | R | - |
| 6 | Implementation Planning | myharness.plan | GPT-5.3-Codex | ✅ | 0 | N |
| 7 | Plan Conformance Review | myharness.review.plan | claude-sonnet-4-6 | ✅ | R | - |
| 8 | DD Generation (Internal Design) | myharness.dd | GPT-5.3-Codex | ✅ | 0 | N |
| 8b | Test Case Generation | myharness.testkit | claude-sonnet-4-6 | ✅ | 0 | N |
| 9 | Task Generation | myharness.tasks | GPT-5.4 | ✅ | 0 | N |
| 10 | Implementation + Build & Fix | myharness.implement | GPT-5.3-Codex | ✅ | R | N |
| 11 | Code Review | myharness.review.code | claude-sonnet-4-6 | ✅ | R | - |
| 12 | Final QA Audit | myharness.testkit | claude-sonnet-4-6 | ✅ | R | - |
| 13 | Launch | orchestrator (direct) | claude-sonnet-4-6 | ✅ | R | - |

**Total auto-resolved assumptions:** N (High: X, Med: Y, Low: Z)
**Total gate retries:** N
**Escalated gates:** <list or "None">

> ⚠  Items requiring user review (Low-confidence assumptions):
> - <TBC-ID>: <question> ← Assumed: <answer>
> - (or "None — all assumptions were High/Med confidence")

**Artifacts**:
- SRS: `docs/output/design-docs/srs/srs-<MOD-ID>-<module-short-name>.md`
- BD: `docs/output/design-docs/bd/bd-<MOD-ID>-<module-short-name>.md`
- Spec: `specs/<feature-id>/spec.md`
- Clarification Q&A: `docs/output/run-logs/<feature-id>/reports/04-clarify-qa.md`
- Plan: `specs/<feature-id>/plan.md`
- DD: `docs/output/design-docs/dd/dd-<MOD-ID>-<module-short-name>.md`
- Tasks: `specs/<feature-id>/tasks.md`
- Implementation: `src/modules/<module>/`
- Verified: Feature accessible on screen ✅

**Execution Logs & Reports**: `docs/output/run-logs/<feature-id>/`

| # | Report File |
|---|-------------|
| 0 | `00-myharness.log.md` |
| 1 | `reports/01-srs-report.md` |
| 2 | `reports/02-bd-report.md` |
| 3 | `reports/03-specify-report.md` |
| 4 | `reports/04-clarify-report.md` |
| 5 | `reports/05-review-spec-report.md` |
| 6 | `reports/06-plan-report.md` |
| 7 | `reports/07-review-plan-report.md` |
| 8 | `reports/08-dd-report.md` |
| 8b | `reports/08b-testcases-report.md` |
| 9 | `reports/09-tasks-report.md` |
| 10 | `reports/10-implement-report.md` |
| 11 | `reports/11-review-code-report.md` |
| 12 | `reports/12-testkit-report.md` + `docs/output/design-docs/testreport/testreport-<MOD-ID>-*.md` |
| 13 | `reports/13-launch-report.md` |
```

---

## Next Actions

> orchestrator populates this from: failed tests, escalated gates, unresolved TBC items, KB updates pending.

- [ ] <action> (from: <source-step>)

---

## Token Summary

| Step | Agent | Model | Input Tokens | Output Tokens | Cost (USD) | Duration (ms) |
|------|-------|-------|-------------|--------------|-----------|---------------|
| 1 | myharness.srs | ... | ... | ... | ... | ... |

**Total:** input=N, output=N, cost=$N, wall_clock=Nms
