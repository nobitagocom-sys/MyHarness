# Pipeline Context File

The orchestrator maintains a running context file updated after each step.
Sub-agents read this file instead of re-reading large source files.

## Path

```
docs/output/run-logs/<feature-id>/run-context.yaml
```

## Schema

```yaml
# --- Immutable (set at STEP 0) ---
feature-id: <feature-id>
pipeline-mode: CREATE | UPDATE | RESUME   # CREATE=--N, UPDATE=--CR, RESUME=feature-id only
input-spec: <path>                        # set only when pipeline-mode=CREATE (from --N flag)
cr-path: <path>                           # set only when pipeline-mode=UPDATE (from --CR flag)
mode: autonomous
language: English

# --- SRS System Output (set after STEP 1 = myharness.srs.system) ---
# Populated by myharness.srs.system after analysing the input spec.
# Sub-agents MUST read these paths instead of re-generating from scratch.
srs-system:
  status: PRE_GENERATED | NONE   # PRE_GENERATED = myharness.srs.system completed
  overview-path: docs/output/srs-systems/srs-overview-system.md
  modules-dir: docs/output/srs-systems/
  module-count: <N>
  fea-count: <N>
  # Discovered modules — populated by STEP 1 (myharness.srs.system), consumed by STEP 1b (one run per module)
  modules:
    - module-id: mod01
      module-keyword: <keyword>
      module-short-name: <short-name>
      module-folder: docs/output/srs-systems/mod01-<slug>/   # raw system-SRS module folder (STEP 1 output)
    - module-id: mod02
      module-keyword: <keyword>
      module-short-name: <short-name>
      module-folder: docs/output/srs-systems/mod02-<slug>/

# --- Compressed Summaries (set after STEP 1c) ---
# myharness.compress runs after Step 1b and creates lightweight summaries.
# Steps 2-7 SHOULD read summary paths instead of full paths to reduce token load.
# If a summary path is null, fall back to the full path.
summaries:
  srs-summary-path: docs/output/design-docs/summaries/srs-<mod-id>-summary.md   # null until Step 1c
  bd-summary-path: docs/output/design-docs/summaries/bd-<mod-id>-summary.md     # null until Step 2+1c
  srs-reduction-pct: <N>   # e.g. 68 means summary is 32% of original size
  bd-reduction-pct: <N>

# --- Tech stack summary (extracted once from docs/technical_architecture.md) ---
tech-stack:
  backend: "NestJS 10, Node.js 22, TypeScript 5"
  frontend: "React 18.3, Vite 6.0"
  db: "PostgreSQL 17"
  cache: "Redis 7.4"
  css: "Bootstrap 5 (utility classes only)"

# --- Updated after each step ---
steps:
  step-0:
    status: COMPLETE
    pipeline-mode: UPDATE | CREATE
  step-1-srs:                     # STEP 1 = myharness.srs.system (system-wide, runs once)
    status: COMPLETE | SKIPPED | FAILED
    started_at: <ISO-timestamp>
    finished_at: <ISO-timestamp>
    path: docs/output/srs-systems/srs-overview-system.md   # system overview (NOT per-module)
    report: docs/output/run-logs/<feature-id>/reports/00-genallreqsrs-report.md
    module-count: <N>
    fea-count: <N>
  step-1b-srs:                    # STEP 1b = myharness.srs (per-module) — one entry per module
    mod01:
      status: COMPLETE | FAILED
      path: docs/output/design-docs/srs/srs-mod01-<short-name>.md   # the formal per-module SRS downstream reads
      report: docs/output/run-logs/<feature-id>/reports/01b-srs-mod01-report.md
      fea-count: <N>
      tbc-count: <N>
    # mod02: { ... }             # add one block per discovered module
  step-2-bd:
    status: COMPLETE
    started_at: <ISO-timestamp>
    finished_at: <ISO-timestamp>
    path: docs/output/design-docs/bd/bd-<mod-id>-<short-name>.md
    report: docs/output/run-logs/<feature-id>/reports/02-bd-report.md
    screen-count: <N>
  step-3-spec:
    status: COMPLETE
    started_at: <ISO-timestamp>
    finished_at: <ISO-timestamp>
    path: specs/<feature-id>/spec.md
    report: docs/output/run-logs/<feature-id>/reports/03-specify-report.md
    branch: <branch-name>
  step-4-clarify:
    status: COMPLETE
    started_at: <ISO-timestamp>
    finished_at: <ISO-timestamp>
    qa-path: docs/output/run-logs/<feature-id>/reports/04-clarify-qa.md
    report: docs/output/run-logs/<feature-id>/reports/04-clarify-report.md
    tbc-resolved: <N>
  step-5-review-spec:
    status: COMPLETE
    started_at: <ISO-timestamp>
    finished_at: <ISO-timestamp>
    verdict: APPROVED | APPROVED_WITH_CONDITIONS | REJECTED
    report: docs/output/run-logs/<feature-id>/reports/05-review-spec-report.md
    retries: <N>
  step-6-plan:
    status: COMPLETE
    started_at: <ISO-timestamp>
    finished_at: <ISO-timestamp>
    path: specs/<feature-id>/plan.md
    data-model: specs/<feature-id>/data-model.md
    contracts: specs/<feature-id>/contracts/
    report: docs/output/run-logs/<feature-id>/reports/06-plan-report.md
  step-7-review-plan:
    status: COMPLETE
    started_at: <ISO-timestamp>
    finished_at: <ISO-timestamp>
    verdict: APPROVED
    report: docs/output/run-logs/<feature-id>/reports/07-review-plan-report.md
    retries: <N>
  step-8-dd:
    status: COMPLETE
    started_at: <ISO-timestamp>
    finished_at: <ISO-timestamp>
    path: docs/output/design-docs/dd/dd-<mod-id>-<short-name>.md
    report: docs/output/run-logs/<feature-id>/reports/08-dd-report.md
  step-8b-testcases:
    status: COMPLETE
    started_at: <ISO-timestamp>
    finished_at: <ISO-timestamp>
    path: docs/output/design-docs/testcase/testcase-<mod-id>-<short-name>.md
    report: docs/output/run-logs/<feature-id>/reports/08b-testcases-report.md
  step-9-tasks:
    status: COMPLETE
    started_at: <ISO-timestamp>
    finished_at: <ISO-timestamp>
    path: specs/<feature-id>/tasks.md
    report: docs/output/run-logs/<feature-id>/reports/09-tasks-report.md
  step-10-implement:
    status: COMPLETE
    started_at: <ISO-timestamp>
    finished_at: <ISO-timestamp>
    report: docs/output/run-logs/<feature-id>/reports/10-implement-report.md
    retries: <N>
  step-11-review-code:
    status: COMPLETE
    started_at: <ISO-timestamp>
    finished_at: <ISO-timestamp>
    verdict: APPROVED
    report: docs/output/run-logs/<feature-id>/reports/11-review-code-report.md
    retries: <N>
  step-12-testkit:
    status: COMPLETE
    started_at: <ISO-timestamp>
    finished_at: <ISO-timestamp>
    verdict: PASS | FAIL
    report: docs/output/run-logs/<feature-id>/reports/12-testkit-report.md
    ipa-report: docs/output/design-docs/testreport/testreport-<mod-id>-<short-name>.md
    back-to-plan-cycles: <N>
  step-13-launch:
    status: COMPLETE
    started_at: <ISO-timestamp>
    finished_at: <ISO-timestamp>
    fe-url: "http://localhost:5173"
    be-url: "http://localhost:8081"
    report: docs/output/run-logs/<feature-id>/reports/13-launch-report.md
```

## orchestrator Update Rules

1. **After STEP 0**: Create file with immutable section + tech-stack (read from `docs/technical_architecture.md` once)
2. **Before delegating each step**: Write `started_at: <ISO-timestamp>` for that step entry (per `protocols/timestamp-protocol.md`)
3. **After each step**: Parse the sub-agent's `<!-- STEP-RESULT -->` block, write `finished_at: <ISO-timestamp>`, and update the remaining fields of the corresponding `steps.step-N` section
4. **Before delegating**: Sub-agents receive the pipeline-context path in `$ARGUMENTS` and can read it for all prior step outputs

## Sub-Agent Read Rules

Sub-agents SHOULD read `run-context.yaml` at startup to discover:

- `feature-id`, `module-id`, `module-keyword` (no need to re-detect)
- Artifact paths from prior steps (no need to guess)
- Tech stack (no need to re-read `docs/technical_architecture.md` for basics)
