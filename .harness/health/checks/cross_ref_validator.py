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
    # Only flag paths that contain no glob characters AND no path separators
    # (i.e. are plain filenames, not directory prefixes).  Directory-style paths
    # like "docs/output/run-logs" legitimately don't exist on a fresh project —
    # they are created at runtime.  Skip anything that looks like a directory
    # prefix (ends with /, contains a trailing segment without an extension, or
    # would be created by agents during the first pipeline run).
    roles_dir = root / ".harness/roles"
    if roles_dir.exists():
        for role_path in roles_dir.glob("*.yaml"):
            try:
                role = yaml.safe_load(role_path.read_text(encoding="utf-8")) or {}
                for key in ("read_globs", "write_globs"):
                    for glob in role.get(key, []):
                        # Skip patterns with any wildcard character
                        if any(c in glob for c in ("*", "?", "[")):
                            continue
                        # Skip directory-style paths (no file extension in last segment)
                        last_seg = glob.rstrip("/").split("/")[-1]
                        if "." not in last_seg:
                            continue  # looks like a directory prefix — runtime-created
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
