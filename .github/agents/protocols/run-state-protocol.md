# Run State Protocol

orchestrator creates and maintains `state.yaml` for every pipeline run. This file enables resume, idempotency checks, and cost tracking.

## Path

```
docs/output/run-logs/<feature-id>/state.yaml
```

## Full Schema

```yaml
run_id: RUN-<YYYYMMDD>-<feature-id>      # e.g. RUN-20260603-001-auth
feature_id: <feature-id>                  # e.g. 001-auth
state: RUNNING | PAUSED | FAILED | COMPLETE
last_completed_step: <N>                  # 0 = nothing done yet
completed_steps: []                       # e.g. [0, 1, 2]
failed_step: null                         # step number where pipeline stopped on FAILED state
token_summary:
  total_input: 0
  total_output: 0
  estimated_cost_usd: 0.0
```

## Lifecycle

| Event | orchestrator Action |
|-------|-------------|
| STEP 0 starts | Create file with `state: RUNNING`, `last_completed_step: 0` |
| Step N completes | Append N to `completed_steps`, set `last_completed_step: N`, accumulate token fields |
| Step N fails (unrecoverable after retries) | Set `state: FAILED`, set `failed_step: N` |
| Pipeline completes | Set `state: COMPLETE` |
| Resume requested | Read file, set `state: RUNNING`, clear `failed_step` |

## orchestrator Update Rules

- Write `state.yaml` at STEP 0 creation.
- After every `<!-- STEP-RESULT -->` parse: update `last_completed_step`, append to `completed_steps`, accumulate `token_summary` from step metrics.
- On `[ESCALATION]` after max retries: set `state: FAILED`, `failed_step: <N>` — pipeline continues but state reflects the failure.
- At `[END]`: set `state: COMPLETE`.

## Token Accumulation

After each step, add to `token_summary`:

```yaml
total_input:        += metrics.input_tokens      (skip if "N/A")
total_output:       += metrics.output_tokens     (skip if "N/A")
estimated_cost_usd: += metrics.estimated_cost_usd (skip if "N/A")
```

## Resume Protocol

See `myharness.orchestrator.agent.md` § Resume Mode. Summary:

- If `$ARGUMENTS` contains `mode: resume` and `resume_from_step: <N>`: read `completed_steps`, skip all steps already in that list, continue from `last_completed_step + 1`.
- If `state: FAILED`: set back to `RUNNING`, clear `failed_step`, resume from `last_completed_step + 1`.
- Write `[RESUME]` log entry: timestamp, resuming-from step, skipped steps list.
