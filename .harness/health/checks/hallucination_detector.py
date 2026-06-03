"""Detect agent hallucinations: referencing files or skills that don't exist."""
import json, re
from pathlib import Path


def run(log_file: Path = Path(".harness/logs/agent.jsonl")) -> dict:
    if not log_file.exists():
        return {"status": "no_logs", "count": 0, "samples": []}

    # Index valid resources
    valid_files = {
        str(p.relative_to(Path("."))).replace("\\", "/")
        for p in Path(".").rglob("*")
        if p.is_file()
    }
    # Index skills by both the role file stem (e.g. "implement") and the full
    # agent name convention (e.g. "myharness.implement") so skill references in
    # agent logs are not falsely flagged as hallucinations.
    _roles_dir = Path(".harness/roles")
    if _roles_dir.exists():
        _stems = {f.stem for f in _roles_dir.glob("*.yaml")}
        valid_skills = _stems | {f"myharness.{s}" for s in _stems}
    else:
        valid_skills = set()

    hallucinations: list[dict] = []

    for line in log_file.read_text(encoding="utf-8").splitlines():
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        if entry.get("type") != "agent_thought":
            continue

        content = entry.get("content", "")
        file_refs = re.findall(r"`?([a-zA-Z0-9_/\\.\\-]+\\.(?:py|md|yaml|json|txt))`?", content)
        skill_refs = re.findall(r"skill[:\s]+([a-zA-Z0-9_-]+)", content, re.I)

        for fp in file_refs:
            fp_norm = fp.replace("\\", "/")
            if fp_norm not in valid_files and not fp_norm.startswith(("http", "https")):
                hallucinations.append(
                    {
                        "call_id": entry.get("call_id"),
                        "type": "file_hallucination",
                        "referenced": fp_norm,
                        "context": content[:150],
                    }
                )

        for skill in skill_refs:
            if skill not in valid_skills:
                hallucinations.append(
                    {
                        "call_id": entry.get("call_id"),
                        "type": "skill_hallucination",
                        "referenced": skill,
                        "suggestion": f"Available: {sorted(valid_skills)[:5]}",
                    }
                )

    return {
        "count": len(hallucinations),
        "samples": hallucinations[:10],
    }
