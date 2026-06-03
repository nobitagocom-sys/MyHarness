"""Track human override rate to detect harness rule misalignment."""
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path


def run(
    log_file: Path = Path(".harness/logs/agent.jsonl"),
    window_days: int = 7,
) -> dict:
    if not log_file.exists():
        return {
            "status": "no_logs",
            "total_decisions": 0,
            "override_count": 0,
            "override_rate": 0.0,
            "reasons": {},
            "trending": "stable",
        }

    cutoff = datetime.now(timezone.utc) - timedelta(days=window_days)
    total = 0
    overrides = 0
    reasons: dict[str, int] = {}
    timeline: list[tuple[datetime, bool]] = []

    for line in log_file.read_text(encoding="utf-8").splitlines():
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        if entry.get("type") != "decision_point":
            continue

        ts_raw = entry.get("timestamp", "")
        try:
            ts = datetime.fromisoformat(ts_raw)
            if ts.tzinfo is None:
                ts = ts.replace(tzinfo=timezone.utc)
        except ValueError:
            continue
        if ts < cutoff:
            continue

        total += 1
        is_override = bool(entry.get("overridden_by_human"))
        if is_override:
            overrides += 1
            reason = entry.get("override_reason", "unspecified")
            reasons[reason] = reasons.get(reason, 0) + 1
        timeline.append((ts, is_override))

    override_rate = round(overrides / max(1, total), 4)

    # Trend: compare first half vs second half of window
    trend = "stable"
    if len(timeline) >= 10:
        mid = len(timeline) // 2
        early = sum(1 for _, v in timeline[:mid] if v) / mid
        late = sum(1 for _, v in timeline[mid:] if v) / (len(timeline) - mid)
        if late > early * 1.2:
            trend = "increasing ⚠️"
        elif late < early * 0.8:
            trend = "decreasing ✅"

    return {
        "total_decisions": total,
        "override_count": overrides,
        "override_rate": override_rate,
        "reasons": reasons,
        "trending": trend,
    }
