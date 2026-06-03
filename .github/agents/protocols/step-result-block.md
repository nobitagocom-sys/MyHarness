# Step Result Block — Handoff Contract

Every sub-agent MUST include a structured result block at the end of their response.
The orchestrator parses this block to extract status, artifacts, and metrics without reading the full report.

## Format

```yaml
<!-- STEP-RESULT
step: <step-number>
agent: <agent-name>
status: SUCCESS | FAILED
feature-id: <feature-id>
module-id: <mod-id>
artifacts:
  <key>: <file-path>
metrics:
  <key>: <value>
verdict: APPROVED | APPROVED_WITH_CONDITIONS | REJECTED | N/A
critical-issues: []
next-inputs:
  <key>: <file-path>
/STEP-RESULT -->
```

## Examples

### STEP 1 — myharness.srs

```yaml
<!-- STEP-RESULT
step: 1
agent: myharness.srs
status: SUCCESS
feature-id: 001-xxx
module-id: mod01
artifacts:
  srs: docs/output/design-docs/srs/srs-mod01-xxx.md
  report: docs/output/run-logs/001-xxx/reports/01-srs-report.md
metrics:
  fea-count: 12
  tbc-count: 3
verdict: N/A
critical-issues: []
next-inputs:
  srs-path: docs/output/design-docs/srs/srs-mod01-xxx.md
/STEP-RESULT -->
```

### STEP 5 — myharness.review.spec (with rejection)

```yaml
<!-- STEP-RESULT
step: 5
agent: myharness.review.spec
status: SUCCESS
feature-id: 001-xxx
module-id: mod01
artifacts:
  report: docs/output/run-logs/001-xxx/reports/05-review-spec-report.md
metrics:
  critical-count: 2
  minor-count: 3
verdict: REJECTED
critical-issues:
  - "Missing BR-KR-002 boundary validation in spec §5"
  - "SCR-mod01-02 wireframe missing target field"
next-inputs: {}
/STEP-RESULT -->
```

## orchestrator Parsing Rule

After each sub-agent returns, the orchestrator:

1. Extracts `<!-- STEP-RESULT ... /STEP-RESULT -->` block
2. Parses YAML content
3. Updates `run-context.yaml` with artifacts and metrics
4. Checks `verdict` for gate decisions — no need to read the full report file
5. If `critical-issues` is non-empty and verdict is REJECTED → invoke gate retry protocol

## Token & Time Fields (added in MyHarness)

All STEP-RESULT blocks MUST include these additional fields under `metrics:`:

```yaml
metrics:
  input_tokens: <N or "N/A">
  output_tokens: <N or "N/A">
  estimated_cost_usd: <N or "N/A">
  duration_ms: <N>
```

orchestrator accumulates these into `run-context.yaml` under `token_summary:`.
