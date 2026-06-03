"""Track token efficiency: cost vs value of context injected per session."""
import json
from collections import defaultdict
from pathlib import Path


def run(log_file: Path = Path(".harness/logs/agent.jsonl")) -> dict:
    if not log_file.exists():
        return {
            "status": "no_logs",
            "avg_tokens_per_call": 0,
            "avg_tokens_per_success": 0,
            "context_reuse_rate": 0.0,
            "high_cost_low_value_calls": [],
        }

    sessions: dict[str, list[dict]] = defaultdict(list)
    for line in log_file.read_text(encoding="utf-8").splitlines():
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        if entry.get("type") == "agent_call":
            sessions[entry.get("session_id", "default")].append(entry)

    total_tokens = 0
    total_calls = 0
    successful_actions = 0
    reuse_rates: list[float] = []
    high_cost_low_value: list[dict] = []

    for calls in sessions.values():
        seen_ctx: set[int] = set()
        reused = 0

        for call in calls:
            tokens = call.get("input_tokens", 0) + call.get("output_tokens", 0)
            total_tokens += tokens
            total_calls += 1

            if not call.get("error") and call.get("sensors_passed", True):
                successful_actions += 1

            ctx_hash = hash(tuple(sorted(call.get("context_files", []))))
            if ctx_hash in seen_ctx:
                reused += 1
            seen_ctx.add(ctx_hash)

            if tokens > 5000 and (call.get("error") or not call.get("sensors_passed", True)):
                high_cost_low_value.append(
                    {
                        "call_id": call.get("call_id"),
                        "tokens": tokens,
                        "error": call.get("error"),
                        "suggestion": "Over-provisioned context? Review injected files.",
                    }
                )

        if len(seen_ctx) > 0:
            reuse_rates.append(reused / len(seen_ctx))

    avg_reuse = round(sum(reuse_rates) / len(reuse_rates), 3) if reuse_rates else 0.0

    return {
        "total_calls": total_calls,
        "avg_tokens_per_call": round(total_tokens / total_calls) if total_calls else 0,
        "avg_tokens_per_success": round(total_tokens / successful_actions) if successful_actions else 0,
        "context_reuse_rate": avg_reuse,
        "high_cost_low_value_calls": high_cost_low_value[:5],
    }
