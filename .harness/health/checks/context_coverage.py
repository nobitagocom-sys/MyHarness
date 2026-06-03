"""Analyze agent context coverage: how much of the injected context is actually used."""
import json
from collections import defaultdict
from pathlib import Path


def run(log_file: Path = Path(".harness/logs/agent.jsonl")) -> dict:
    if not log_file.exists():
        return {
            "status": "no_logs",
            "total_calls": 0,
            "avg_coverage": 1.0,
            "avg_waste_percent": 0.0,
            "missing_context_incidents": [],
            "coverage_by_role": {},
        }

    total = 0
    sum_coverage = 0.0
    sum_waste = 0.0
    missing_incidents: list[dict] = []
    by_role: dict[str, list[float]] = defaultdict(list)

    for line in log_file.read_text(encoding="utf-8").splitlines():
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        if entry.get("type") != "agent_call":
            continue

        total += 1
        injected = set(entry.get("context_files", []))
        accessed = set(entry.get("accessed_files", []))
        attempted = set(entry.get("attempted_reads", []))

        coverage = len(accessed & injected) / len(injected) if injected else 1.0
        waste = len(injected - accessed) / len(injected) if injected else 0.0
        missing = attempted - injected

        sum_coverage += coverage
        sum_waste += waste

        role = entry.get("role", "unknown")
        by_role[role].append(coverage)

        if missing:
            missing_incidents.append(
                {
                    "call_id": entry.get("call_id"),
                    "role": role,
                    "missing_files": sorted(missing),
                    "suggestion": f"Add to {role} read_globs: {sorted(missing)[:3]}",
                }
            )

    avg_cov = round(sum_coverage / total, 3) if total else 1.0
    avg_waste = round((sum_waste / total) * 100, 1) if total else 0.0

    return {
        "total_calls": total,
        "avg_coverage": avg_cov,
        "avg_waste_percent": avg_waste,
        "missing_context_incidents": missing_incidents[:10],
        "coverage_by_role": {
            r: round(sum(v) / len(v), 3) for r, v in by_role.items()
        },
    }
