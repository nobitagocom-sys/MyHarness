"""Validate cross-references: workflows→skills, roles→glob paths, docs→doc links."""
import re, yaml
from pathlib import Path


def run(root: Path = Path(".")) -> dict:
    broken: list[str] = []

    # Index active skills
    active_skills = {
        f.stem.split(".")[0]
        for f in (root / ".harness/registry/active").glob("*.yaml")
    } if (root / ".harness/registry/active").exists() else set()

    # 1. Workflow → skill refs
    wf_dir = root / ".harness/workflows"
    if wf_dir.exists():
        for wf_path in wf_dir.glob("*.yaml"):
            try:
                wf = yaml.safe_load(wf_path.read_text(encoding="utf-8"))
                for step in (wf or {}).get("steps", []):
                    if not isinstance(step, dict):
                        continue
                    skill = step.get("skill")
                    if skill and skill not in active_skills:
                        broken.append(
                            f"🔗 {wf_path.name}: step '{step.get('id', '?')}' "
                            f"references unknown skill '{skill}'"
                        )
            except Exception:
                pass

    # 2. Role → read/write glob sanity (non-glob paths must exist)
    roles_dir = root / ".harness/roles"
    if roles_dir.exists():
        for role_path in roles_dir.glob("*.yaml"):
            try:
                role = yaml.safe_load(role_path.read_text(encoding="utf-8")) or {}
                for key in ("read_globs", "write_globs"):
                    for glob in role.get(key, []):
                        if "**" in glob or "*" in glob:
                            continue  # skip wildcard globs
                        target = root / glob
                        if not target.exists():
                            broken.append(
                                f"🔗 {role_path.name}: {key} path '{glob}' does not exist"
                            )
            except Exception:
                pass

    # 3. Docs internal markdown links
    docs_dir = root / "docs"
    if docs_dir.exists():
        for doc in docs_dir.rglob("*.md"):
            try:
                content = doc.read_text(encoding="utf-8", errors="ignore")
                for _, link in re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content):
                    if link.startswith(("#", "http", "mailto:")):
                        continue
                    target = (doc.parent / link).resolve()
                    if not target.exists():
                        broken.append(
                            f"🔗 {doc.relative_to(root)}: broken link → {link}"
                        )
            except Exception:
                pass

    return {"broken": broken, "broken_count": len(broken)}
