from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml


@dataclass
class RunMetrics:
    run_name: str
    run_dir: Path
    duration_seconds: int | None
    completed_steps: int
    retry_total: int
    token_input: int | None
    token_output: int | None
    token_cost_usd: float | None


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data if isinstance(data, dict) else {}


def parse_dt(value: Any) -> datetime | None:
    if isinstance(value, datetime):
        return value
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip().replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        return None


def collect_metrics(run_dir: Path, run_name: str) -> RunMetrics:
    state = load_yaml(run_dir / "state.yaml")
    context = load_yaml(run_dir / "run-context.yaml")

    steps_obj = context.get("steps", {})
    steps = steps_obj.values() if isinstance(steps_obj, dict) else []

    starts: list[datetime] = []
    finishes: list[datetime] = []
    retry_total = 0

    for step in steps:
        if not isinstance(step, dict):
            continue
        started = parse_dt(step.get("started_at"))
        finished = parse_dt(step.get("finished_at"))
        if started:
            starts.append(started)
        if finished:
            finishes.append(finished)
        retries = step.get("retries")
        if isinstance(retries, int):
            retry_total += retries

    duration_seconds: int | None = None
    if starts and finishes:
        duration_seconds = int((max(finishes) - min(starts)).total_seconds())

    completed_steps = 0
    completed = state.get("completed_steps")
    if isinstance(completed, list):
        completed_steps = len(completed)

    token_summary = state.get("token_summary", {})
    if not isinstance(token_summary, dict):
        token_summary = {}

    token_input = token_summary.get("total_input")
    token_output = token_summary.get("total_output")
    token_cost_usd = token_summary.get("estimated_cost_usd")

    token_input = token_input if isinstance(token_input, int) else None
    token_output = token_output if isinstance(token_output, int) else None
    token_cost_usd = float(token_cost_usd) if isinstance(token_cost_usd, (int, float)) else None

    return RunMetrics(
        run_name=run_name,
        run_dir=run_dir,
        duration_seconds=duration_seconds,
        completed_steps=completed_steps,
        retry_total=retry_total,
        token_input=token_input,
        token_output=token_output,
        token_cost_usd=token_cost_usd,
    )


def pct_improvement(baseline: float | int | None, backup: float | int | None) -> str:
    if baseline is None or backup is None:
        return "N/A"
    if baseline == 0:
        return "N/A"
    pct = ((baseline - backup) / baseline) * 100.0
    return f"{pct:.2f}%"


def delta_text(baseline: float | int | None, backup: float | int | None) -> str:
    if baseline is None or backup is None:
        return "N/A"
    return str(baseline - backup)


def fmt_num(value: float | int | None) -> str:
    return "N/A" if value is None else str(value)


def build_report(backup: RunMetrics, baseline: RunMetrics | None) -> str:
    now = datetime.now().isoformat(timespec="seconds")

    lines = [
        f"# Backup Effectiveness Auto Report - {backup.run_name}",
        "",
        f"Generated at: {now}",
        "",
        "## Inputs",
        "",
        f"- Backup run dir: {backup.run_dir.as_posix()}",
    ]

    if baseline:
        lines.append(f"- Baseline run dir: {baseline.run_dir.as_posix()}")
    else:
        lines.append("- Baseline run dir: N/A")

    lines += [
        "",
        "## Metrics",
        "",
        "| Metric | Baseline | With Backup | Delta (Base - Backup) | Improvement |",
        "|---|---:|---:|---:|---:|",
    ]

    def b(field: str) -> float | int | None:
        if not baseline:
            return None
        return getattr(baseline, field)

    rows = [
        ("Duration (seconds)", b("duration_seconds"), backup.duration_seconds),
        ("Completed steps (count)", b("completed_steps"), backup.completed_steps),
        ("Retries (count)", b("retry_total"), backup.retry_total),
        ("Input tokens", b("token_input"), backup.token_input),
        ("Output tokens", b("token_output"), backup.token_output),
        ("Estimated cost (USD)", b("token_cost_usd"), backup.token_cost_usd),
    ]

    for label, base_val, backup_val in rows:
        lines.append(
            f"| {label} | {fmt_num(base_val)} | {fmt_num(backup_val)} | {delta_text(base_val, backup_val)} | {pct_improvement(base_val, backup_val)} |"
        )

    lines += [
        "",
        "## Notes",
        "",
        "- Improvement is positive when backup run uses less time/tokens/cost than baseline.",
        "- If baseline is missing, this report is a backup-only snapshot.",
        "- If token fields are 0 or N/A, telemetry is incomplete; compare duration and retries first.",
        "",
    ]

    if not baseline:
        lines += [
            "## Next step",
            "",
            "- Run one baseline scenario without backup resume, then re-run this script with --baseline-run.",
            "",
        ]

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate backup effectiveness report from run logs.")
    parser.add_argument("--backup-run", required=True, help="Path to backup-enabled run log directory")
    parser.add_argument("--baseline-run", required=False, help="Path to baseline run log directory")
    parser.add_argument("--output", required=True, help="Output markdown report path")
    parser.add_argument("--run-name", default="run", help="Display name for report")
    args = parser.parse_args()

    backup_dir = Path(args.backup_run).resolve()
    baseline_dir = Path(args.baseline_run).resolve() if args.baseline_run else None
    output_path = Path(args.output).resolve()

    backup_metrics = collect_metrics(backup_dir, args.run_name)
    baseline_metrics = collect_metrics(baseline_dir, "baseline") if baseline_dir else None

    report = build_report(backup_metrics, baseline_metrics)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
