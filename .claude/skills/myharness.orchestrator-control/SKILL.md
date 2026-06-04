# Orchestrator Step-Range Controller

Controls the orchestrator to run the pipeline from step A to step B, then stop. Allows selective execution of pipeline portions instead of running all 13 steps.

## Syntax

```
/myharness.orchestrator-control from=<N> to=<M> <feature-description | feature-id>
```

or

```
/myharness.orchestrator-control <N>-<M> <feature-description | feature-id>
```

or simplified:

```
/myharness.orchestrator-control steps <N> <M> -- <feature-description>
```

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `from` / `N` | Yes | Starting step (0-13) |
| `to` / `M` | Yes | Ending step (0-13), must be >= `from` |
| feature | Yes* | Feature description OR existing feature-id |
| `--dry-run` | No | Show planned steps only, do not execute |

\* If feature-id already exists in `specs/` with a `state.yaml`, the feature description may be omitted.

## Pipeline Steps Reference

```
STEP 0  — Existing Spec Detection
STEP 1  — SRS Generation (myharness.srs.system → then myharness.srs)
STEP 2  — BD Generation (myharness.bd)
STEP 3  — Spec Creation (myharness.specify)
STEP 4  — Spec Clarification (myharness.clarify)
STEP 5  — Spec Review 🔄 (myharness.review.spec)
STEP 6  — Implementation Planning (myharness.plan)
STEP 7  — Plan Review 🔄 (myharness.review.plan)
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

```
1. Extract from_step and to_step from user input
2. Validate: 0 <= from_step <= to_step <= 13
3. If from_step > to_step → error, prompt user to re-enter
4. If feature-id already exists → pipeline-mode = UPDATE
5. If new feature → pipeline-mode = CREATE, ask for feature description if missing
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

```
1. Read .harness/agents/protocols/pipeline-context.md
2. STEP 0 (always run even if from_step > 0, when no run-context.yaml exists):
   - Scan specs/ to find feature-id
   - Create docs/output/run-logs/<feature-id>/run-context.yaml
   - Create docs/output/run-logs/<feature-id>/state.yaml
3. If from_step > 0 AND state.yaml already exists:
   - Read state.yaml to get completed_steps
   - Read run-context.yaml to get artifact paths
   - Verify artifacts for step from_step - 1 exist
```

### 4. Execute Steps in Range

For each step from `from_step` to `to_step`:

```
1. Read the corresponding phase definition file
2. Read required protocols:
   - report-gate-protocol.md (every step)
   - auto-resolve-protocol.md (steps 1,2,3,4,6,8,9)
   - gate-retry-protocol.md (steps 5,7,10,11,12)
3. Execute step:
   a. If parallel group (8 ∥ 9) → dispatch both agents simultaneously
   b. If regular step → dispatch the corresponding agent
   c. Read STEP-RESULT block
   d. Update run-context.yaml and state.yaml
   e. Apply REPORT HARD GATE
   f. If gate REJECTED:
      - Steps 5,7,11: auto-retry with fix agent (max 5 attempts)
      - Step 10: auto-retry build & fix (max 5 attempts)
      - Step 12: BACK-TO-PLAN (max 3 cycles)
4. Write log to 00-myharness.log.md
```

**Special handling for Parallel Group (Steps 8 ∥ 9):**
- If range includes 8 or 9 → always run both in parallel
- If range has only 8 or only 9 → warn and auto-include both
- Step 8b only runs if in range AND Step 8+9 have completed

### 5. Stop at to_step

```
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

```
1. Display the list of steps that would run
2. For each step: show agent, input, expected output
3. Check prerequisites
4. Estimate time (based on step count)
5. Do NOT execute any step
6. Do NOT create any new files
```

## Resuming from a Range Stop

After the range stops, the user can:

```
# Continue from the next step
/myharness.orchestrator-control from=<to_step+1> to=13 <feature-id>

# Or use the original orchestrator with resume mode
/myharness.orchestrator mode: resume resume_from_step: <N> <feature-id>
```

## Output Language

All output documents in Vietnamese. Technical IDs remain as-is.

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
# Run from design through review (steps 1-7)
/myharness.orchestrator-control from=1 to=7 Add Google login feature

# Re-run review steps (5-7) for an existing feature
/myharness.orchestrator-control 5-7 FEA-001

# Run only implement + test (10-12)
/myharness.orchestrator-control steps 10 12 -- FEA-001

# Dry run to see what would execute
/myharness.orchestrator-control from=1 to=5 --dry-run Add search feature

# Run from start through DD (1-9)
/myharness.orchestrator-control from=1 to=9 MOD-01

# Launch only (13)
/myharness.orchestrator-control from=13 to=13 FEA-001
```

## Mandatory Rules

1. **Never pause for [NEEDS CLARIFICATION]** — auto-resolve all
2. **Never halt on REJECTED** — auto-fix and retry until pass or retries exhausted
3. **Parallel done right** — Steps 8+9 always dispatched simultaneously
4. **Full logging** — every decision, assumption, retry recorded
5. **Stop at the right step** — never run past to_step even if gate passes
6. **Check prerequisites** — never run a step if input artifacts are missing
