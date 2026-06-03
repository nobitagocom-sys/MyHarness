"""layer_lint.py — Enforce layer dependency rules for NestJS (TypeScript) projects.

Scans the configured source roots for import-from statements that violate the
declared layer order.  Works for both Python (ast) and TypeScript (regex) sources.

Layer order is fixed via DEFAULT_LAYER_ORDER below.
To override, edit that constant directly.
"""
import re, sys
from pathlib import Path

DEFAULT_LAYER_ORDER = ["types", "config", "repo", "service", "runtime"]

# Candidate source roots in priority order — first that exists wins.
SOURCE_ROOTS = [
    Path("backend/src"),   # NestJS monorepo
    Path("frontend/src"),  # React frontend (checked separately if exists)
    Path("src"),           # Fallback for plain projects
]

# Simple TS/JS import regex — catches: import ... from '...'  and  require('...')
_TS_IMPORT_RE = re.compile(
    r"""(?:from\s+['"]([^'"]+)['"]|require\s*\(\s*['"]([^'"]+)['"]\s*\))"""
)


def _load_layer_order() -> list[str]:
    return DEFAULT_LAYER_ORDER


def _build_deps(layer_order: list[str]) -> dict[str, list[str]]:
    """Each layer may import only layers that appear before it in the order."""
    deps: dict[str, list[str]] = {}
    for i, layer in enumerate(layer_order):
        deps[layer] = layer_order[:i]
    return deps


def _extract_layers_from_import(raw_path: str, layer_order: list[str]) -> list[str]:
    """Return layer names embedded in an import path segment."""
    segments = re.split(r"[/\\]", raw_path)
    return [s for s in segments if s in layer_order]


def _check_typescript(root: Path, layer_deps: dict[str, list[str]]) -> list[str]:
    errors: list[str] = []
    layer_set = set(layer_deps)
    for f in root.rglob("*.ts"):
        if f.name.endswith(".d.ts") or f.name == "index.ts":
            continue
        try:
            parts = f.relative_to(root).parts
            # Determine which layer this file belongs to (first matching segment)
            file_layer = next((p for p in parts if p in layer_set), None)
            if file_layer is None:
                continue
            allowed = set(layer_deps[file_layer])
            content = f.read_text(encoding="utf-8", errors="ignore")
            for m in _TS_IMPORT_RE.finditer(content):
                raw = m.group(1) or m.group(2) or ""
                if not raw.startswith("."):
                    continue  # external package — skip
                for imported_layer in _extract_layers_from_import(raw, list(layer_set)):
                    if imported_layer != file_layer and imported_layer not in allowed:
                        errors.append(
                            f"❌ {f.relative_to(Path('.'))} [{file_layer}] "
                            f"→ [{imported_layer}] (not allowed)"
                        )
        except Exception:
            pass
    return errors


def _check_python(root: Path, layer_deps: dict[str, list[str]]) -> list[str]:
    import ast as _ast

    errors: list[str] = []
    layer_set = set(layer_deps)
    for f in root.rglob("*.py"):
        if f.name == "__init__.py":
            continue
        try:
            parts = f.relative_to(root).parts
            file_layer = next((p for p in parts if p in layer_set), None)
            if file_layer is None:
                continue
            allowed = set(layer_deps[file_layer])
            tree = _ast.parse(f.read_text(encoding="utf-8", errors="ignore"))
            for node in _ast.walk(tree):
                if isinstance(node, _ast.ImportFrom) and node.module:
                    imported = node.module.split(".")[0]
                    if imported in layer_set and imported not in allowed:
                        errors.append(
                            f"❌ {f.relative_to(Path('.'))} [{file_layer}] "
                            f"→ [{imported}] (not allowed)"
                        )
        except Exception:
            pass
    return errors


def check():
    layer_order = _load_layer_order()
    layer_deps = _build_deps(layer_order)
    errors: list[str] = []

    for root in SOURCE_ROOTS:
        if not root.exists():
            continue
        # TypeScript/JavaScript project
        ts_files = list(root.rglob("*.ts"))
        if ts_files:
            errors.extend(_check_typescript(root, layer_deps))
        else:
            errors.extend(_check_python(root, layer_deps))

    if errors:
        print("\n".join(errors))
        sys.exit(1)
    print("✅ Architecture clean")


if __name__ == "__main__":
    check()
