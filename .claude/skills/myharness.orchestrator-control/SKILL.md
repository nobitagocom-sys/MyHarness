# Orchestrator Step-Range Controller

Controls the orchestrator to run the pipeline from step A to step B, then stop. Allows selective execution of pipeline portions instead of running all 13 steps.

## Syntax

```text
/myharness.orchestrator-control from=<N> to=<M> --N <path-to-spec-file>
/myharness.orchestrator-control from=<N> to=<M> --CR <feature-id> <path-to-cr-file>
/myharness.orchestrator-control from=<N> to=<M> <existing-feature-id>
```

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `from` / `N` | Yes | Starting step (0-13) |
| `to` / `M` | Yes | Ending step (0-13), must be >= `from` |
| `--N <spec-path>` | New features | **New spec**: path to input spec file (e.g. `docs/input/new-spec/foo.md`). Triggers CREATE mode. Orchestrator reads the file to extract system name and identify modules. |
| `--CR <feature-id> <cr-path>` | Change requests | **Change request**: existing feature-id + path to CR file (e.g. `docs/input/change-request/cr-foo.md`). Triggers UPDATE mode on existing specs. |
| `<feature-id>` | Resume/re-run | Existing feature-id in `specs/` — resumes from where it left off or re-runs the given range. |
| `--dry-run` | No | Show planned steps only, do not execute |

`--N` and `--CR` are mutually exclusive. Omit both only when resuming an existing feature by ID.

## Pipeline Steps Reference

```text
STEP 0  — Existing Spec Detection
STEP 1  — SRS Generation (myharness.srs.system → then myharness.srs)
STEP 1c — SRS Compression ⚡ (myharness.compress — runs auto after 1b, SOFT GATE)
STEP 2  — BD Generation (myharness.bd)
STEP 2c — BD Compression ⚡ (myharness.compress — runs auto after 2, SOFT GATE)
STEP 3  — Spec Creation (myharness.specify)
STEP 4  — Spec Clarification ⚡ (myharness.clarify — Haiku model)
STEP 5  — Spec Review 🔄 (myharness.review.spec)
STEP 6  — Implementation Planning (myharness.plan)
STEP 7  — Plan Review 🔄⚡ (myharness.review.plan — Haiku model)
STEP 8  — DD Generation ∥ (myharness.dd)
STEP 9  — Task Generation ∥ (myharness.tasks)
STEP 8b — Test Case Generation (myharness.testkit: gen-testcases)
STEP 10 — Implementation 🔄 (myharness.implement)
STEP 11 — Code Review 🔄 (myharness.review.code)
STEP 12 — Test Execution 🔄 (myharness.testkit: run-tests)
STEP 13 — Launch UI (orchestrator direct)
```

> ∥ = runs in parallel. 🔄 = auto-retry gate.

### Step Grouping

| Phase | Steps | Definition File |
|-------|-------|-----------------|
| Design | 0-4 | `.harness/agents/steps/steps-01-04-design.md` |
| Review | 5-7 | `.harness/agents/steps/steps-05-07-review.md` |
| Detail | 8, 8b, 9 | `.harness/agents/steps/steps-08-09-detail.md` |
| Implement | 10-12 | `.harness/agents/steps/steps-10-12-implement.md` |
| Launch | 13 | `.harness/agents/steps/step-13-launch.md` |

## Execution Flow

When invoked, execute sequentially:

### 1. Parse & Validate Input

```text
1. Extract from_step and to_step from user input
2. Validate: 0 <= from_step <= to_step <= 13
3. If from_step > to_step → error, prompt user to re-enter

4. Detect pipeline mode from flags:

   CASE A — --N <spec-path> present:
     → pipeline-mode = CREATE (new spec)
     → input-spec-path = <spec-path>
     → Read the spec file to extract system/feature name
     → DO NOT derive module-id or module-keyword from the file name
     → Let myharness.srs.system analyse the file and identify modules
     → feature-id = auto-generated from system name in file content (e.g. FEA-b2b-trade)
     → NEVER treat the file path or file name as the feature description

   CASE B — --CR <feature-id> <cr-path> present:
     → pipeline-mode = UPDATE (change request)
     → feature-id = <feature-id> (must exist in specs/)
     → cr-path = path to change-request file
     → Read existing specs/<feature-id>/spec.md and state.yaml
     → Read cr-path to understand what changed
     → Pass both to downstream agents as context

   CASE C — plain <feature-id> only (no flag):
     → Look up specs/<feature-id>/ and state.yaml
     → If not found → ERROR: "Feature ID not found. Use --N to start a new spec."
     → If found → pipeline-mode = RESUME
     → Read state.yaml:
         safe_from = last_completed_step + 1
         If user-provided from_step > safe_from:
           → Use user-provided from_step (user knows what they want to re-run)
         If user-provided from_step <= last_completed_step:
           → WARN: "Steps N through M already completed per state.yaml."
           → Ask: "Re-run from step <from_step> anyway? (y/n)"
           → If yes → continue with user from_step (overwrite mode)
           → If no  → auto-correct: from_step = safe_from
         If context was compacted mid-run (state=RUNNING, last_completed_step < to_step):
           → WARN: "Previous run was interrupted at step <last_completed_step>."
           → Auto-set from_step = safe_from, inform user
     → Write [RESUME] log entry:
         previous last_completed_step, auto-corrected from_step, skipped steps list

5. Validate prerequisites per mode:
   - CREATE: spec file must exist and be readable
   - UPDATE: specs/<feature-id>/spec.md must exist
   - RESUME: specs/<feature-id>/state.yaml must exist
```

### 2. Step Range Validation

Some step combinations require special handling:

| Range | Rule |
|-------|------|
| from_step = 1 | STEP 1 has two sub-steps: run `myharness.srs.system` first (generates `docs/output/srs-systems/`), then run `myharness.srs`. If `srs-overview-system.md` already exists, skip `srs.system` and run `myharness.srs` directly. |
| from_step ∈ {8,9} | Always run BOTH 8 AND 9 in parallel (Parallel Group A) |
| from_step = 8b | Requires output from Step 8 AND Step 9 beforehand |
| from_step > 0 and no state.yaml | Must run Step 0 first to initialize context, then run the range |
| from_step ∈ {6,8,9,10} | Requires `specs/<feature-id>/screens/` from Step 3. If missing, warn and suggest re-running Step 3. |
| from_step ∈ {10,11,12} | Requires tasks.md to exist from Step 9 |
| from_step = 12 | Requires implemented code from Step 10 |
| from_step = 13 | Requires tests passed from Step 12 |

If prerequisites are not met:

- Warn the user clearly
- Suggest running the necessary prerequisite steps
- Ask user whether to auto-run prerequisite steps
- If user agrees → expand the range to include prerequisites

### 3. Initialize Pipeline Context

```text
1. Read .harness/agents/protocols/pipeline-context.md

2. If run-context.yaml does NOT exist (new pipeline):
   - Run STEP 0: create run-context.yaml and state.yaml
   - state.yaml schema (MUST include all fields):
       run_id: RUN-<YYYYMMDD>-<feature-id>
       feature_id: <feature-id>
       pipeline_mode: CREATE | UPDATE | RESUME
       state: RUNNING
       last_completed_step: 0
       completed_steps: []
       failed_step: null
       interrupted_step: null      ← NEW: set if context compact detected
       token_summary:
         total_input: 0
         total_output: 0
         estimated_cost_usd: 0.0

3. If state.yaml EXISTS (resume or continuation):
   - Read state.yaml → get last_completed_step, completed_steps, state, interrupted_step
   - Read run-context.yaml → get all artifact paths from prior steps
   - Set state: RUNNING, clear interrupted_step if set
   - Verify key artifacts exist for step (from_step - 1):
       If artifact missing → WARN user, suggest re-running the missing step
   - Write [RESUME] entry to 00-myharness.log.md:
       Timestamp, resuming-from, last_completed_step, skipped steps list

4. Before delegating EACH step:
   - Mark step as IN_PROGRESS in state.yaml:
       interrupted_step: <N>    ← written BEFORE agent is spawned
       state: RUNNING
   - After step completes successfully:
       Append N to completed_steps
       Set last_completed_step: N
       Clear interrupted_step: null
   - This way: if context compacts mid-step, interrupted_step survives
     and next resume knows exactly which step was cut off
```

### 4. Execute Steps in Range

For each step from `from_step` to `to_step`:

```text
1. Read the corresponding phase definition file
2. Read required protocols:
   - report-gate-protocol.md (every step)
   - auto-resolve-protocol.md (steps 1,2,3,4,6,8,9)
   - gate-retry-protocol.md (steps 5,7,10,11,12)
3. Execute step per Step Execution Checklist below
4. Write log to 00-myharness.log.md
```

**Special handling for Parallel Group (Steps 8 ∥ 9):**

- If range includes 8 or 9 → always run both in parallel
- If range has only 8 or only 9 → warn and auto-include both
- Step 8b only runs if in range AND Step 8+9 have completed

---

### Parallel Execution Rules

> ⛔ MANDATORY — read before executing any per-module step.

Steps 1b, 1c, 2, 2c, 3, 4, 5, 6, 7 each run **once per module**. With N modules:

```text
WRONG — sequential (N× slower):
  mod01 done → mod02 done → mod03 done → next step

CORRECT — parallel (same time as 1 module):
  mod01 ┐
  mod02 ├─ all dispatched together → wait for all → next step
  mod03 ┘
```

**How to dispatch in parallel (Claude Code Agent mechanism):**
In a single response, make multiple Agent tool calls at the same time — one per module.
The runtime executes them concurrently. Do NOT issue them one at a time.

**Barrier rule:** Every step has a hard barrier — do NOT start the next step until ALL
modules from the current step have returned results. Example:
- Start STEP 2 only after ALL Step 1b + Step 1c results are received
- Start STEP 3 only after ALL Step 2 + Step 2c results are received

**Retry independence:** If mod02 STEP 5 is REJECTED, its retry loop runs without
blocking mod01 or mod03 which already passed. Collect all module verdicts, then handle
each failed module's retry individually (sequentially within that module).

**run-context.yaml write conflicts:** Multiple parallel agents may finish at different
times. Orchestrator writes results to run-context.yaml only after receiving each
agent's STEP-RESULT block — never pre-write. Use per-module keys
(e.g. `step-2-bd.mod01`, `step-2-bd.mod02`) so entries never overwrite each other.

**Single-module projects:** If srs-system.modules[] has exactly 1 entry, parallel
dispatch degenerates to a single agent call — no special handling needed.

---

### Step Execution Checklist

> ⛔ MANDATORY: Follow exactly for each step. Do NOT skip sub-steps.
> All steps use `Invoke Agent` — NOT `Invoke Skill`. Read the agent definition
> file from `.claude/agents/<agent-name>.md` before spawning each agent.

#### STEP 1 — SRS Generation (TWO mandatory sub-steps)

```text
SUB-STEP 1a — Agent: myharness.srs.system
  Agent definition: .claude/agents/myharness.srs.system.md

  1. Check if docs/output/srs-systems/srs-overview-system.md EXISTS
  2. IF NOT EXISTS:
     a. Write [PROCESSING] STEP 1a — myharness.srs.system to log
     b. Invoke Agent: myharness.srs.system
        ARGUMENTS:
          feature-id: <feature-id>
          pipeline-context: docs/output/run-logs/<feature-id>/run-context.yaml
          input-spec: <input-spec-path from --N flag>
        ⛔ DO NOT pass module-id or module-keyword — the agent reads the
           spec file and identifies ALL modules autonomously.
     c. Wait for result → parse <!-- STEP-RESULT -->
     d. Extract from result: module-count, list of module-ids, keywords, srs-paths
     e. Set srs-system.status: PRE_GENERATED in run-context.yaml
     f. Store discovered modules in run-context.yaml under srs-system.modules[]
     g. Write [PROCESSING] STEP 1a — COMPLETE to log
  3. IF EXISTS:
     a. Read srs-overview-system.md → re-extract full module list
     b. Set srs-system.status: PRE_GENERATED (already done)
     c. Write [STEP 1a SKIPPED — srs-overview-system.md already exists] to log

SUB-STEP 1b — Agent: myharness.srs ∥ PARALLEL across all modules
  Agent definition: .claude/agents/myharness.srs.md

  ⛔ PARALLEL DISPATCH — dispatch ALL modules simultaneously in a single invocation batch.
  Do NOT wait for mod01 to finish before starting mod02.

  1. Write [PROCESSING] STEP 1b — dispatching <N> modules in parallel to log
  2. Dispatch ALL agents simultaneously (one Agent call per module, all in same batch):
     For mod01: Invoke Agent myharness.srs with ARGUMENTS:
       feature-id: <feature-id>
       module-id: mod01
       module-keyword: <keyword-from-1a>
       pipeline-context: docs/output/run-logs/<feature-id>/run-context.yaml
       input-spec: <input-spec-path>
       srs-system-overview: docs/output/srs-systems/srs-overview-system.md
       srs-module-dir: docs/output/srs-systems/mod01-<keyword>/
     For mod02: Invoke Agent myharness.srs with ARGUMENTS: (same pattern, mod02 values)
     For modNN: ... (repeat for every module discovered in 1a)
  3. Wait for ALL parallel agents to complete
  4. For each completed module result:
     a. Parse <!-- STEP-RESULT -->
     b. Update run-context.yaml: step-1-srs.<mod-id>.status, path, fea-count, tbc-count
     c. Apply REPORT HARD GATE per module
     d. Write [PROCESSING] STEP 1b (<mod-id>) — COMPLETE to log
  5. Write [PROCESSING] STEP 1b — ALL <N> modules complete to log
```

#### STEP 1c — SRS Compression ⚡ ∥ PARALLEL (SOFT GATE — after ALL Step 1b complete)

```text
Agent definition: .claude/agents/myharness.compress.md

  ⛔ PARALLEL DISPATCH — dispatch ALL modules simultaneously.

  1. Write [PROCESSING] STEP 1c — compressing <N> SRS files in parallel to log
  2. Dispatch ALL compress agents simultaneously:
     For each module in srs-system.modules[]:
       Invoke Agent myharness.compress with ARGUMENTS:
         feature-id: <feature-id>
         module-id: <mod-id>
         srs-full-path: <step-1-srs.<mod-id>.path from run-context>
         bd-full-path: null
         output-dir: docs/output/design-docs/summaries/
         pipeline-context: docs/output/run-logs/<feature-id>/run-context.yaml
  3. Wait for ALL to complete (failures do NOT block — soft gate)
  4. For each result:
     - If SUCCESS: update run-context.yaml summaries.<mod-id>.srs-summary-path, srs-reduction-pct
     - If FAILED: write [WARN] STEP 1c <mod-id> compress failed — full path used downstream
  5. Write [PROCESSING] STEP 1c — COMPLETE (<N> compressed, <F> failed/skipped) to log
NOTE: Any number of failures is acceptable. Pipeline always continues to STEP 2.
```

#### STEP 2 — BD Generation ∥ PARALLEL across all modules

```text
Agent definition: .claude/agents/myharness.bd.md

  ⛔ PARALLEL DISPATCH — dispatch ALL modules simultaneously.

  1. Write [PROCESSING] STEP 2 — dispatching <N> BD agents in parallel to log
  2. Dispatch ALL agents simultaneously:
     For each module in srs-system.modules[]:
       Resolve: srs-path = summaries.<mod-id>.srs-summary-path ?? step-1-srs.<mod-id>.path
       Invoke Agent myharness.bd with ARGUMENTS:
         feature-id: <feature-id>
         module-id: <mod-id>
         module-keyword: <keyword>
         pipeline-context: docs/output/run-logs/<feature-id>/run-context.yaml
         srs-path: <resolved>
         srs-full-path: <step-1-srs.<mod-id>.path>
         srs-system-overview: docs/output/srs-systems/srs-overview-system.md
         srs-module-dir: docs/output/srs-systems/<mod-id>-<keyword>/
  3. Wait for ALL to complete
  4. For each result:
     a. Parse <!-- STEP-RESULT -->
     b. Update run-context.yaml: step-2-bd.<mod-id>.status, path, screen-count
     c. Auto-resolve any [NEEDS CLARIFICATION] markers in BD output
     d. Apply REPORT HARD GATE
     e. Write [PROCESSING] STEP 2 (<mod-id>) — COMPLETE to log
  5. Write [PROCESSING] STEP 2 — ALL <N> modules complete to log
```

#### STEP 2c — BD Compression ⚡ ∥ PARALLEL (SOFT GATE — after ALL Step 2 complete)

```text
Agent definition: .claude/agents/myharness.compress.md

  ⛔ PARALLEL DISPATCH — dispatch ALL modules simultaneously.

  1. Write [PROCESSING] STEP 2c — compressing <N> BD files in parallel to log
  2. Dispatch ALL compress agents simultaneously:
     For each module in srs-system.modules[]:
       Invoke Agent myharness.compress with ARGUMENTS:
         feature-id: <feature-id>
         module-id: <mod-id>
         srs-full-path: null
         bd-full-path: <step-2-bd.<mod-id>.path from run-context>
         output-dir: docs/output/design-docs/summaries/
         pipeline-context: docs/output/run-logs/<feature-id>/run-context.yaml
  3. Wait for ALL to complete (failures do NOT block)
  4. For each result:
     - If SUCCESS: update run-context.yaml summaries.<mod-id>.bd-summary-path, bd-reduction-pct
     - If FAILED: write [WARN] STEP 2c <mod-id> compress failed — full path used downstream
  5. Write [PROCESSING] STEP 2c — COMPLETE to log
NOTE: Any number of failures is acceptable. Pipeline always continues to STEP 3.
```

#### STEP 3 — Spec Creation ∥ PARALLEL across all modules

```text
Agent definition: .claude/agents/myharness.specify.md

  ⛔ PARALLEL DISPATCH — dispatch ALL modules simultaneously.

  1. Write [PROCESSING] STEP 3 — dispatching <N> specify agents in parallel to log
  2. Dispatch ALL agents simultaneously:
     For each module in srs-system.modules[]:
       Resolve:
         srs-path = summaries.<mod-id>.srs-summary-path ?? step-1-srs.<mod-id>.path
         bd-path  = summaries.<mod-id>.bd-summary-path  ?? step-2-bd.<mod-id>.path
       Invoke Agent myharness.specify with ARGUMENTS:
         feature-id: <feature-id>
         module-id: <mod-id>
         pipeline-context: docs/output/run-logs/<feature-id>/run-context.yaml
         srs-path: <resolved>
         bd-path: <resolved>
         srs-full-path: <step-1-srs.<mod-id>.path>
         bd-full-path: <step-2-bd.<mod-id>.path>
  3. Wait for ALL to complete
  4. For each result:
     a. Parse <!-- STEP-RESULT -->
     b. Update run-context.yaml: step-3-spec.<mod-id>.status, path, branch
     c. POST-CHECK: scan spec.md for [NEEDS CLARIFICATION] → auto-resolve each
     d. Apply REPORT HARD GATE
     e. Write [PROCESSING] STEP 3 (<mod-id>) — COMPLETE to log
  5. Write [PROCESSING] STEP 3 — ALL <N> modules complete to log
```

#### STEP 4 — Spec Clarification ⚡ Haiku ∥ PARALLEL across all modules

```text
Agent definition: .claude/agents/myharness.clarify.md  [model: claude-haiku-4-5-20251001]

  ⛔ PARALLEL DISPATCH — dispatch ALL modules simultaneously.

  1. Write [PROCESSING] STEP 4 — dispatching <N> clarify agents in parallel to log
  2. Dispatch ALL agents simultaneously:
     For each module in srs-system.modules[]:
       Resolve:
         srs-path = summaries.<mod-id>.srs-summary-path ?? step-1-srs.<mod-id>.path
         bd-path  = summaries.<mod-id>.bd-summary-path  ?? step-2-bd.<mod-id>.path
       Invoke Agent myharness.clarify with ARGUMENTS:
         feature-id: <feature-id>
         module-id: <mod-id>
         pipeline-context: docs/output/run-logs/<feature-id>/run-context.yaml
         spec-path: <step-3-spec.<mod-id>.path>
         srs-path: <resolved>
         bd-path: <resolved>
  3. Wait for ALL to complete
  4. For each result:
     a. Parse <!-- STEP-RESULT -->
     b. Apply Auto-Resolve Protocol to ALL questions → encode into spec
     c. Write 04-clarify-qa-<mod-id>.md with Q&A table
     d. Update run-context.yaml: step-4-clarify.<mod-id>.status, tbc-resolved
     e. Apply REPORT HARD GATE
     f. Write [PROCESSING] STEP 4 (<mod-id>) — COMPLETE to log
  5. Write [PROCESSING] STEP 4 — ALL <N> modules complete to log
```

#### STEP 5 — Spec Review ∥ PARALLEL across all modules (Auto-Retry Gate per module)

```text
Agent definition: .claude/agents/myharness.review.spec.md

  ⛔ PARALLEL DISPATCH — dispatch ALL modules simultaneously.
  Retry loops run independently per module — a retry on mod02 does NOT block mod01.

  1. Write [PROCESSING] STEP 5 — dispatching <N> review.spec agents in parallel to log
  2. Dispatch ALL agents simultaneously:
     For each module in srs-system.modules[]:
       Resolve:
         srs-path = summaries.<mod-id>.srs-summary-path ?? step-1-srs.<mod-id>.path
         bd-path  = summaries.<mod-id>.bd-summary-path  ?? step-2-bd.<mod-id>.path
       Invoke Agent myharness.review.spec with ARGUMENTS:
         feature-id: <feature-id>
         module-id: <mod-id>
         pipeline-context: docs/output/run-logs/<feature-id>/run-context.yaml
         spec-path: <step-3-spec.<mod-id>.path>
         srs-path: <resolved>
         bd-path: <resolved>
  3. Wait for ALL to complete
  4. For each result (handle independently):
     a. Parse <!-- STEP-RESULT --> → check verdict
     b. IF APPROVED or APPROVED_WITH_CONDITIONS → mark module done
     c. IF REJECTED → enter retry loop for THIS module only:
          i.   Extract CRITICAL issues
          ii.  Write [ISSUE] STEP 5 <mod-id> — REJECTED (Retry N/5) to log
          iii. Invoke Agent myharness.specify (fix, targeted to this module)
          iv.  Invoke Agent myharness.review.spec (re-review this module)
          v.   Repeat until APPROVED or retry > 5
          vi.  If retry > 5 → [ESCALATION], mark module as partial-pass
     d. Update run-context.yaml: step-5-review-spec.<mod-id>.verdict, retries
     e. Apply REPORT HARD GATE
     f. Write [PROCESSING] STEP 5 (<mod-id>) — COMPLETE to log
  5. Write [PROCESSING] STEP 5 — ALL <N> modules complete to log
```

#### STEP 6 — Implementation Planning ∥ PARALLEL across all modules

```text
Agent definition: .claude/agents/myharness.plan.md

  ⛔ PARALLEL DISPATCH — dispatch ALL modules simultaneously.

  1. Write [PROCESSING] STEP 6 — dispatching <N> plan agents in parallel to log
  2. Dispatch ALL agents simultaneously:
     For each module in srs-system.modules[]:
       Resolve:
         srs-path = summaries.<mod-id>.srs-summary-path ?? step-1-srs.<mod-id>.path
         bd-path  = summaries.<mod-id>.bd-summary-path  ?? step-2-bd.<mod-id>.path
       Invoke Agent myharness.plan with ARGUMENTS:
         feature-id: <feature-id>
         module-id: <mod-id>
         pipeline-context: docs/output/run-logs/<feature-id>/run-context.yaml
         spec-path: <step-3-spec.<mod-id>.path>
         srs-path: <resolved>
         bd-path: <resolved>
         srs-full-path: <step-1-srs.<mod-id>.path>
         bd-full-path: <step-2-bd.<mod-id>.path>
  3. Wait for ALL to complete
  4. For each result:
     a. Parse <!-- STEP-RESULT -->
     b. Update run-context.yaml: step-6-plan.<mod-id>.path, data-model, contracts
     c. Auto-resolve any [NEEDS CLARIFICATION] markers in plan artifacts
     d. Apply REPORT HARD GATE
     e. Write [PROCESSING] STEP 6 (<mod-id>) — COMPLETE to log
  5. Write [PROCESSING] STEP 6 — ALL <N> modules complete to log
```

#### STEP 7 — Plan Review ⚡ Haiku ∥ PARALLEL across all modules (Auto-Retry Gate per module)

```text
Agent definition: .claude/agents/myharness.review.plan.md  [model: claude-haiku-4-5-20251001]

  ⛔ PARALLEL DISPATCH — dispatch ALL modules simultaneously.
  Retry loops run independently per module.

  1. Write [PROCESSING] STEP 7 — dispatching <N> review.plan agents in parallel to log
  2. Dispatch ALL agents simultaneously:
     For each module in srs-system.modules[]:
       Resolve:
         srs-path = summaries.<mod-id>.srs-summary-path ?? step-1-srs.<mod-id>.path
       Invoke Agent myharness.review.plan with ARGUMENTS:
         feature-id: <feature-id>
         module-id: <mod-id>
         pipeline-context: docs/output/run-logs/<feature-id>/run-context.yaml
         plan-path: <step-6-plan.<mod-id>.path>
         spec-path: <step-3-spec.<mod-id>.path>
         srs-path: <resolved>
         data-model-path: <step-6-plan.<mod-id>.data-model>
  3. Wait for ALL to complete
  4. For each result (handle independently):
     a. Parse <!-- STEP-RESULT --> → check verdict
     b. IF APPROVED or APPROVED_WITH_CONDITIONS → mark module done
     c. IF REJECTED → enter retry loop for THIS module only:
          i.   Extract CRITICAL issues
          ii.  Write [ISSUE] STEP 7 <mod-id> — REJECTED (Retry N/5) to log
          iii. Invoke Agent myharness.plan (fix, targeted to this module)
          iv.  Invoke Agent myharness.review.plan (re-review this module)
          v.   Repeat until APPROVED or retry > 5
     d. Update run-context.yaml: step-7-review-plan.<mod-id>.verdict, retries
     e. Apply REPORT HARD GATE
     f. Write [PROCESSING] STEP 7 (<mod-id>) — COMPLETE to log
  5. Write [PROCESSING] STEP 7 — ALL <N> modules complete to log
```

### 5. Stop at to_step

```text
1. After to_step completes → STOP
2. Write [RANGE-STOP] log entry:
   - Executed range: from_step → to_step
   - Last completed step: to_step
   - Status: COMPLETED (or FAILED if gate did not pass)
   - Do NOT run remaining steps
3. Update state.yaml:
   - state: PAUSED (not COMPLETED)
   - last_completed_step: to_step
   - Note: "Pipeline paused by orchestrator-control. Range: N-M."
4. Display summary to user:
   - Steps executed and their results
   - Artifacts created
   - Issues requiring attention (if any)
   - Command to continue from the next step
```

### 6. Dry Run Mode

If `--dry-run` is specified:

```text
1. Display the list of steps that would run
2. For each step: show agent, input, expected output
3. Check prerequisites
4. Estimate time (based on step count)
5. Do NOT execute any step
6. Do NOT create any new files
```

## Resuming from a Range Stop or Context Compact

### Normal resume (pipeline paused at planned stop)

Pass the feature-id directly — no flag needed. The orchestrator reads `state.yaml`
and auto-detects `last_completed_step` to resume from the correct step:

```text
# Orchestrator auto-detects where to resume from state.yaml
/myharness.orchestrator-control from=<next> to=13 <feature-id>

# Example: pipeline stopped at step 7, continue to end
/myharness.orchestrator-control from=8 to=13 FEA-b2b-trade
```

### Context compacted mid-run (interrupted mid-step)

If Claude's context was compacted while a step was running, `state.yaml` will show:

```yaml
state: RUNNING
last_completed_step: 5      # last fully completed step
interrupted_step: 6         # step that was cut off
```

In this case, simply re-invoke with the feature-id and the orchestrator will:

1. Detect `interrupted_step: 6` in state.yaml
2. Warn: "Previous run was interrupted during step 6. Re-running from step 6."
3. Auto-set `from_step = interrupted_step` (NOT last_completed_step + 1)
4. Check if step 6 artifacts were partially written → overwrite safely
5. Clear `interrupted_step` after step 6 completes successfully

```text
# Same command works for both normal resume and interrupted-step recovery
/myharness.orchestrator-control from=6 to=13 FEA-b2b-trade

# Or let the orchestrator decide the correct from_step automatically
/myharness.orchestrator-control to=13 FEA-b2b-trade
```

### If you don't know where the pipeline stopped

Read `state.yaml` — it always has the answer:

```text
cat docs/output/run-logs/<feature-id>/state.yaml
```

| `state` | `interrupted_step` | Action |
| ------- | ----------------- | ------ |
| `PAUSED` | null | Normal stop — run from `last_completed_step + 1` |
| `RUNNING` | null | Likely a crash — run from `last_completed_step + 1` |
| `RUNNING` | N | Context compact mid-step — re-run from step N |
| `FAILED` | null | Gate failure — check log, fix, re-run from `last_completed_step` |

## Output Language

All output documents in English. Technical IDs remain as-is.

## Logging

Write logs to `docs/output/run-logs/<feature-id>/00-myharness.log.md` with format:

```markdown
## [RANGE-START] — {timestamp}
- Range: STEP {from} → STEP {to}
- Mode: {CREATE|UPDATE}
- Feature: {feature-id}

## [RANGE-STOP] — {timestamp}
- Completed: STEP {from} → STEP {to}
- Status: {COMPLETED|PARTIAL|FAILED}
- Next: Run `/myharness.orchestrator-control from={to+1} to=13 {feature-id}` to continue
```

## Protocols to Read

| Protocol | File | When to Read |
|----------|------|-------------|
| Pipeline Context | `.harness/agents/protocols/pipeline-context.md` | Pipeline initialization |
| Auto-Resolve | `.harness/agents/protocols/auto-resolve-protocol.md` | Before steps with [NEEDS CLARIFICATION] |
| Gate Retry | `.harness/agents/protocols/gate-retry-protocol.md` | Before review gates (5,7,11) |
| Report Hard Gate | `.harness/agents/protocols/report-gate-protocol.md` | After EVERY step |
| Timestamp | `.harness/agents/protocols/timestamp-protocol.md` | Before each log entry |
| Log Formats | `.harness/agents/protocols/log-formats.md` | When writing logs |
| Step Result Block | `.harness/agents/protocols/step-result-block.md` | After each sub-agent returns |
| Scope Guard | `.harness/agents/protocols/scope-guard-protocol.md` | Before Step 10 |
| Run State | `.harness/agents/protocols/run-state-protocol.md` | STEP 0 + after each step |
| Implement Delegation | `.harness/agents/protocols/implement-delegation.md` | Before Step 10 |
| Health Check | `.harness/agents/protocols/health-check-protocol.md` | After Step 13 (if in range) |

## Usage Examples

```bash
# NEW SPEC — full design phase (steps 1-7) from a spec file
# --N tells the orchestrator this is a new spec file to analyse and split into modules
/myharness.orchestrator-control from=1 to=7 --N docs/input/new-spec/ai_b2b_trade_flow_requirements.md

# NEW SPEC — full pipeline end to end
/myharness.orchestrator-control from=1 to=13 --N docs/input/new-spec/my_feature.md

# NEW SPEC — dry run to preview what would execute before committing
/myharness.orchestrator-control from=1 to=7 --dry-run --N docs/input/new-spec/my_feature.md

# CHANGE REQUEST — update existing feature with a CR file
# --CR tells the orchestrator to update FEA-001 based on the CR document
/myharness.orchestrator-control from=1 to=7 --CR FEA-001 docs/input/change-request/cr-add-approval-flow.md

# CHANGE REQUEST — re-run only planning steps after a CR
/myharness.orchestrator-control from=6 to=7 --CR FEA-001 docs/input/change-request/cr-add-approval-flow.md

# RESUME — continue an existing feature from where it stopped (no flag needed)
/myharness.orchestrator-control from=8 to=13 FEA-001

# RESUME — re-run review steps only for an existing feature
/myharness.orchestrator-control from=5 to=7 FEA-001

# RESUME — launch only
/myharness.orchestrator-control from=13 to=13 FEA-001
```

## Mandatory Rules

1. **Never pause for [NEEDS CLARIFICATION]** — auto-resolve all
2. **Never halt on REJECTED** — auto-fix and retry until pass or retries exhausted
3. **Parallel done right** — Steps 8+9 always dispatched simultaneously
4. **Full logging** — every decision, assumption, retry recorded
5. **Stop at the right step** — never run past to_step even if gate passes
6. **Check prerequisites** — never run a step if input artifacts are missing
