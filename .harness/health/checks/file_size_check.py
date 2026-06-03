"""Check file sizes against harness standards for agent readability."""
import yaml
from pathlib import Path
from typing import Any

SIZE_LIMITS: dict[str, dict[str, Any]] = {
    ".harness/roles/*.yaml":            {"max_lines": 150, "max_keys": 20},
    ".harness/workflows/*.yaml":        {"max_steps": 12},
    ".harness/registry/active/*.yaml":  {"max_lines": 200},
}


def check_file(filepath: Path, config: dict) -> list[str]:
    violations: list[str] = []
    try:
        content = filepath.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return violations

    if filepath.suffix == ".md":
        lines = len(content.splitlines())
        words = len(content.split())
        if lines > config.get("max_lines", float("inf")):
            violations.append(
                f"📏 {filepath.name}: {lines} lines > {config['max_lines']} limit — "
                "move details to docs/ and link"
            )
        if words > config.get("max_words", float("inf")):
            violations.append(
                f"📏 {filepath.name}: {words} words > {config['max_words']} limit — "
                "use progressive disclosure"
            )

    elif filepath.suffix == ".yaml":
        try:
            data = yaml.safe_load(content)
        except Exception:
            return violations
        if data is None:
            return violations
        steps = data.get("steps", []) if isinstance(data, dict) else []
        if steps and len(steps) > config.get("max_steps", float("inf")):
            violations.append(
                f"🔄 {filepath.name}: {len(steps)} steps > {config['max_steps']} limit — "
                "split into sub-workflows"
            )
        if isinstance(data, dict):
            key_count = len(data.keys())
            if key_count > config.get("max_keys", float("inf")):
                violations.append(
                    f"🎭 {filepath.name}: {key_count} keys > {config['max_keys']} limit"
                )
    return violations


def run(root: Path = Path(".")) -> dict:
    passed: list[str] = []
    warnings: list[str] = []

    for pattern, config in SIZE_LIMITS.items():
        for filepath in root.glob(pattern):
            v = check_file(filepath, config)
            if v:
                warnings.extend(v)
            else:
                passed.append(filepath.name)

    return {"passed": passed, "warnings": warnings, "warning_count": len(warnings)}
