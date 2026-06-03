"""Orchestrate all harness health checks and produce a consolidated report."""
import argparse, json, sys, yaml
from datetime import datetime, timezone
from pathlib import Path

# Modular checks
from harness.health.checks.file_size_check      import run as run_file_size
from harness.health.checks.workflow_dag_check    import run as run_dag
from harness.health.checks.cross_ref_validator   import run as run_cross_ref
from harness.health.checks.context_coverage      import run as run_context
from harness.health.checks.token_efficiency      import run as run_tokens
from harness.health.checks.role_boundary_audit   import run as run_role_audit
from harness.health.checks.hallucination_detector import run as run_hallucination
from harness.health.checks.human_override_rate   import run as run_override

DEFAULT_LOG    = Path(".harness/logs/agent.jsonl")
THRESHOLDS_CFG = Path(".harness/health/thresholds.yaml")
METRICS_DIR    = Path(".harness/metrics")


def _load_thresholds() -> dict:
    defaults = {
        "file_size":  {"max_warnings": 5},
        "workflow":   {"max_issues": 0},
        "context":    {"min_coverage": 0.60, "max_waste_percent": 40},
        "behavior":   {"max_violation_rate": 0.05, "max_hallucinations_per_100": 2},
        "evolution":  {"max_override_rate": 0.15},
    }
    if THRESHOLDS_CFG.exists():
        try:
            loaded = yaml.safe_load(THRESHOLDS_CFG.read_text(encoding="utf-8")) or {}
            for k, v in loaded.items():
                if k in defaults and isinstance(v, dict):
                    defaults[k].update(v)
        except Exception:
            pass
    return defaults


def _compute_score(alerts: list[dict]) -> int:
    score = 100
    for a in alerts:
        score -= 15 if a["severity"] == "error" else 5
    return max(0, min(100, score))


def _recommendations(checks: dict, thresholds: dict) -> list[str]:
    recs: list[str] = []
    fs = checks.get("file_size", {})
    if fs.get("warning_count", 0) > 0:
        recs.append("Split large files — move details to docs/ and reference from AGENTS.md")
    ctx = checks.get("context_coverage", {})
    if ctx.get("missing_context_incidents"):
        top = ctx["missing_context_incidents"][0]
        recs.append(f"Add missing files to role read_globs: {top.get('suggestion', '')}")
    rb = checks.get("role_boundary_audit", {})
    if rb.get("write"):
        recs.append("Review write boundary violations — agents wrote outside declared globs")
    ov = checks.get("human_override_rate", {})
    if ov.get("reasons"):
        top_reason = max(ov["reasons"], key=lambda k: ov["reasons"][k])
        recs.append(f"Human override trend: most common reason = '{top_reason}' — update rules")
    return recs


def run_all(
    log_file: Path = DEFAULT_LOG,
    checks_filter: list[str] | None = None,
) -> dict:
    thresholds = _load_thresholds()
    alerts: list[dict] = []
    checks: dict = {}

    def _enabled(name: str) -> bool:
        return checks_filter is None or name in checks_filter

    # --- Static checks ---
    if _enabled("static"):
        checks["file_size"] = run_file_size()
        if checks["file_size"]["warning_count"] > thresholds["file_size"]["max_warnings"]:
            alerts.append({
                "severity": "warning",
                "check": "file_size",
                "message": f"{checks['file_size']['warning_count']} files exceed size limits",
            })

        checks["workflow_dag"] = run_dag()
        if checks["workflow_dag"]["issue_count"] > thresholds["workflow"]["max_issues"]:
            alerts.append({
                "severity": "error",
                "check": "workflow_dag",
                "message": f"{checks['workflow_dag']['issue_count']} workflow DAG issues",
            })

        checks["cross_refs"] = run_cross_ref()
        if checks["cross_refs"]["broken_count"] > 0:
            alerts.append({
                "severity": "warning",
                "check": "cross_refs",
                "message": f"{checks['cross_refs']['broken_count']} broken cross-references",
            })

    # --- Runtime checks ---
    if _enabled("runtime"):
        checks["context_coverage"] = run_context(log_file)
        cov = checks["context_coverage"].get("avg_coverage", 1.0)
        if cov < thresholds["context"]["min_coverage"]:
            alerts.append({
                "severity": "warning",
                "check": "context_coverage",
                "message": f"Avg context coverage {cov:.1%} < threshold {thresholds['context']['min_coverage']:.1%}",
            })

        checks["token_efficiency"] = run_tokens(log_file)

    # --- Behavior checks ---
    if _enabled("behavior"):
        checks["role_boundary_audit"] = run_role_audit(log_file)
        vr = checks["role_boundary_audit"].get("violation_rate", 0.0)
        if vr > thresholds["behavior"]["max_violation_rate"]:
            alerts.append({
                "severity": "error",
                "check": "role_boundary_audit",
                "message": f"Role violation rate {vr:.1%} exceeds threshold {thresholds['behavior']['max_violation_rate']:.1%}",
            })

        checks["hallucinations"] = run_hallucination(log_file)
        h_count = checks["hallucinations"].get("count", 0)
        total_calls = checks.get("context_coverage", {}).get("total_calls", 100) or 100
        h_rate_per_100 = (h_count / total_calls) * 100
        if h_rate_per_100 > thresholds["behavior"]["max_hallucinations_per_100"]:
            alerts.append({
                "severity": "warning",
                "check": "hallucinations",
                "message": f"{h_count} hallucinations detected ({h_rate_per_100:.1f} per 100 calls)",
            })

    # --- Evolution checks ---
    if _enabled("evolution"):
        checks["human_override_rate"] = run_override(log_file)
        ovr = checks["human_override_rate"].get("override_rate", 0.0)
        if ovr > thresholds["evolution"]["max_override_rate"]:
            alerts.append({
                "severity": "warning",
                "check": "human_override_rate",
                "message": (
                    f"Override rate {ovr:.1%} > threshold "
                    f"({checks['human_override_rate'].get('trending', '')})"
                ),
            })

    score = _compute_score(alerts)
    recs  = _recommendations(checks, thresholds)

    result = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "health_score": score,
            "total_checks": len(checks),
            "total_alerts": len(alerts),
            "error_count": sum(1 for a in alerts if a["severity"] == "error"),
        },
        "alerts": alerts,
        "checks": checks,
        "recommendations": recs,
    }

    # Always persist JSON snapshot
    METRICS_DIR.mkdir(parents=True, exist_ok=True)
    (METRICS_DIR / "health.json").write_text(
        json.dumps(result, indent=2, default=str, ensure_ascii=False),
        encoding="utf-8",
    )
    return result


def main():
    parser = argparse.ArgumentParser(description="Run harness health checks")
    parser.add_argument("--format", choices=["cli", "json", "dashboard"], default="cli")
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--log-file", type=Path, default=DEFAULT_LOG)
    parser.add_argument(
        "--checks",
        default=None,
        help="Comma-separated subset: static,runtime,behavior,evolution",
    )
    args = parser.parse_args()

    checks_filter = [c.strip() for c in args.checks.split(",")] if args.checks else None
    results = run_all(log_file=args.log_file, checks_filter=checks_filter)

    from harness.health import reporter
    if args.format == "cli":
        reporter.cli_report(results)
    elif args.format == "json":
        out = args.output or METRICS_DIR / "health.json"
        reporter.json_report(results, out)
    elif args.format == "dashboard":
        out = args.output or METRICS_DIR / "dashboard.html"
        reporter.html_dashboard(results, out)

    score = results["summary"]["health_score"]
    try:
        print(f"[Score] Health Score: {score}/100")
    except UnicodeEncodeError:
        pass
    sys.exit(0 if score >= 70 else 1)


if __name__ == "__main__":
    main()

