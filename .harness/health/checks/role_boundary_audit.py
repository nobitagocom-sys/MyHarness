"""Audit agent action logs for role boundary violations."""
import fnmatch, json, yaml
from pathlib import Path


def _load_roles(roles_dir: Path) -> dict[str, dict]:
    roles: dict[str, dict] = {}
    if not roles_dir.exists():
        return roles
    for f in roles_dir.glob("*.yaml"):
        try:
            data = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
            roles[f.stem.split(".")[0]] = data
        except Exception:
            pass
    return roles


def run(log_file: Path = Path(".harness/logs/agent.jsonl")) -> dict:
    if not log_file.exists():
        return {
            "status": "no_logs",
            "total_attempts": 0,
            "violation_rate": 0.0,
            "read": [],
            "write": [],
            "skill": [],
        }

    roles = _load_roles(Path(".harness/roles"))
    read_v: list[dict] = []
    write_v: list[dict] = []
    skill_v: list[dict] = []
    total = 0

    for line in log_file.read_text(encoding="utf-8").splitlines():
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        if entry.get("type") != "agent_action":
            continue

        total += 1
        role_id = entry.get("role", "")
        role_cfg = roles.get(role_id, {})
        action = entry.get("action", "")
        fp = entry.get("filepath", "")

        if action == "read_file":
            globs = role_cfg.get("read_globs", [])
            if fp and globs and not any(fnmatch.fnmatch(fp, g) for g in globs):
                read_v.append({"call_id": entry.get("call_id"), "filepath": fp, "role": role_id})

        elif action == "write_file":
            globs = role_cfg.get("write_globs", [])
            if fp and globs and not any(fnmatch.fnmatch(fp, g) for g in globs):
                write_v.append({"call_id": entry.get("call_id"), "filepath": fp, "role": role_id, "severity": "error"})

        elif action == "call_skill":
            allowed = role_cfg.get("skills", [])
            skill = entry.get("skill_id", "")
            if skill and allowed and skill not in allowed:
                skill_v.append({"call_id": entry.get("call_id"), "skill": skill, "role": role_id})

    total_v = len(read_v) + len(write_v) + len(skill_v)
    return {
        "total_attempts": total,
        "violation_rate": round(total_v / max(1, total), 4),
        "read": read_v[:10],
        "write": write_v[:10],
        "skill": skill_v[:10],
        "total_violations": total_v,
    }
