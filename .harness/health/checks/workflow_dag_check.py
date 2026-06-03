"""Validate workflow DAGs: no cycles, all step IDs unique, no orphan depends_on refs."""
import yaml
from pathlib import Path
from collections import defaultdict


def check_workflow(filepath: Path) -> list[str]:
    violations: list[str] = []
    try:
        wf = yaml.safe_load(filepath.read_text(encoding="utf-8"))
    except Exception as e:
        return [f"❌ {filepath.name}: YAML parse error — {e}"]

    if not isinstance(wf, dict):
        return []
    steps = wf.get("steps", [])
    if not steps:
        violations.append(f"🔄 {filepath.name}: Workflow has no steps")
        return violations

    step_ids = {s["id"] for s in steps if isinstance(s, dict) and "id" in s}

    # Unique IDs
    all_ids = [s["id"] for s in steps if isinstance(s, dict) and "id" in s]
    dupes = {sid for sid in all_ids if all_ids.count(sid) > 1}
    for d in dupes:
        violations.append(f"🔄 {filepath.name}: Duplicate step id: '{d}'")

    # Unknown depends_on refs
    graph: dict[str, list[str]] = defaultdict(list)
    for step in steps:
        if not isinstance(step, dict):
            continue
        sid = step.get("id", "?")
        for dep in step.get("depends_on", []):
            if dep not in step_ids:
                violations.append(
                    f"🔄 {filepath.name}: Step '{sid}' depends_on unknown '{dep}'"
                )
            graph[dep].append(sid)

    # Cycle detection via DFS
    def _has_cycle(node: str, visited: set, stack: set) -> bool:
        visited.add(node)
        stack.add(node)
        for nb in graph[node]:
            if nb not in visited:
                if _has_cycle(nb, visited, stack):
                    return True
            elif nb in stack:
                return True
        stack.discard(node)
        return False

    visited: set = set()
    for sid in step_ids:
        if sid not in visited:
            if _has_cycle(sid, visited, set()):
                violations.append(
                    f"🔄 {filepath.name}: Cycle detected in workflow DAG — "
                    "add explicit termination condition or split workflow"
                )
                break

    return violations


def run(workflows_dir: Path = Path(".harness/workflows")) -> dict:
    issues: list[str] = []
    checked = 0
    for wf in workflows_dir.glob("*.yaml"):
        issues.extend(check_workflow(wf))
        checked += 1
    return {"checked": checked, "issues": issues, "issue_count": len(issues)}
