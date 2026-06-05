---
description: Execute only a selected step range of the MyHarness pipeline using start_step and end_step parameters.
model: GPT-5.4
tools: [agent, read, search, edit, run, todo, web]
handoffs:
  - label: Resume Full Orchestration
    agent: myharness.orchestrator
    prompt: Continue the pipeline from the requested step range
    send: true
---

## Scope

Use this agent when you want to run only part of the MyHarness pipeline instead of the full 13-step flow.

### Supported parameters

```yaml
start_step: 5
end_step: 7
feature_id: 001-simple-login-app
mode: partial
```

- `start_step`: first step to execute, inclusive
- `end_step`: last step to execute, inclusive
- `feature_id`: target run folder / feature context
- `mode`: use `partial` for step-range execution

If `start_step` or `end_step` is missing, infer the narrowest safe range from the request and the current run state.

## Execution Rules

1. Read the current `run-context.yaml`, `state.yaml`, and latest reports before doing anything else.
2. Validate that `start_step <= end_step`.
3. Only execute steps inside the requested range.
4. Do not re-run steps outside the range unless the user explicitly requests a rollback.
5. Preserve step artifacts and update run logs after each completed step.
6. If the selected range starts after a review gate or implementation boundary, continue from the nearest valid handoff file.

## Range Handling

- Step range may span design, review, detail, implementation, QA, or launch phases.
- If the range includes Step 10, follow implement scope guard rules before any file writes.
- If the range includes Step 12 or Step 13, run the required verification / launch checks for that step only.

## Output Expectations

- Update the existing run log for the feature.
- Record which steps were executed and which were skipped.
- Write a short report stating the requested range, the actual executed range, and any skipped steps.
