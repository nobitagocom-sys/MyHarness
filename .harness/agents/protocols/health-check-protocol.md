# Health Check Protocol

orchestrator runs the health runner after Step 13 (pipeline complete).

## Command

```bash
python3 .harness/health/runner.py --format cli
```

## Log Entry

Write `[HEALTH-REPORT]` entry in `00-myharness.log.md`:

```markdown
## [HEALTH-REPORT] Pipeline Complete
- **Timestamp:** <real timestamp>
- **Health Score:** <N>/100
- **Alerts:** <count> (<error_count> errors)
- **Token Efficiency:** avg <N> tokens/call
- **Violations:** <violation_rate>
- **Recommendations:** <list or "None">
```

## Threshold (from .harness/health/thresholds.yaml)

Score < 60 → write [ESCALATION] and document known issues in final report.
