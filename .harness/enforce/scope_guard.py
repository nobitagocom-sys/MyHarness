"""
scope_guard.py — Harness Scope Enforcement

Reads write_globs from .harness/roles/<role>.yaml and checks that
changed files do not exceed the role's allowed write scope.
Exits non-zero if any violation is found.

Usage:
    python3 .harness/enforce/scope_guard.py --role implement
    python3 .harness/enforce/scope_guard.py --role implement --files src/foo.py docs/bar.md
    python3 .harness/enforce/scope_guard.py --role implement --staged
"""

import argparse
import fnmatch
import subprocess
import sys
from pathlib import Path

import yaml

ROLES_DIR = Path(".harness/roles")


def load_write_globs(role_name: str) -> list:
    role_file = ROLES_DIR / f"{role_name}.yaml"
    if not role_file.exists():
        print(f"[scope_guard] ERROR: Role file not found: {role_file}")
        sys.exit(2)
    data = yaml.safe_load(role_file.read_text(encoding="utf-8"))
    return data.get("context", {}).get("write_globs", [])


def get_changed_files(staged_only: bool = False) -> list:
    args = ["git", "diff", "--name-only"]
    if staged_only:
        args.append("--cached")
    try:
        out = subprocess.check_output(args, stderr=subprocess.DEVNULL).decode()
        files = [f.strip() for f in out.splitlines() if f.strip()]
        # If staged returned nothing, fall back to unstaged
        if not files and staged_only:
            out = subprocess.check_output(
                ["git", "diff", "--name-only"], stderr=subprocess.DEVNULL
            ).decode()
            files = [f.strip() for f in out.splitlines() if f.strip()]
        return files
    except subprocess.CalledProcessError:
        return []


def allowed(filepath: str, globs: list) -> bool:
    fp = filepath.replace("\\", "/")
    for pattern in globs:
        pat = pattern.replace("\\", "/")
        if "**" in pat:
            # Split pattern on **
            # e.g. "docs/reqs/**/*.md" → prefix="docs/reqs/", suffix="*.md"
            before, _, after = pat.partition("**")
            prefix = before.rstrip("/")
            # suffix is the part after **/, e.g. "*.md" or "*.json"
            suffix = after.lstrip("/")
            if fp.startswith(prefix + "/"):
                remainder = fp[len(prefix) + 1:]  # strip prefix
                # match the filename (or last segment) against suffix
                if not suffix:
                    return True  # pattern like "src/**" — match everything under prefix
                filename = remainder.split("/")[-1]
                if fnmatch.fnmatch(filename, suffix) or fnmatch.fnmatch(remainder, suffix):
                    return True
        else:
            if fnmatch.fnmatch(fp, pat):
                return True
    return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--role", required=True, help="Role name: pm, ba, dev, test, devops")
    parser.add_argument("--files", nargs="*", help="Explicit file list to check")
    parser.add_argument("--staged", action="store_true", help="Check git staged files only")
    args = parser.parse_args()

    write_globs = load_write_globs(args.role)
    if not write_globs:
        print(f"[scope_guard] WARNING: No write_globs defined for role '{args.role}'")
        sys.exit(0)

    files = args.files if args.files else get_changed_files(staged_only=args.staged)
    if not files:
        print(f"[scope_guard] OK: No changed files to check")
        sys.exit(0)

    violations = [f for f in files if not allowed(f, write_globs)]

    if violations:
        print(f"[scope_guard] VIOLATION — role '{args.role}' attempted to write outside scope:")
        for v in violations:
            print(f"  ✗  {v}")
        print(f"\n  Allowed write_globs for '{args.role}':")
        for g in write_globs:
            print(f"  ✓  {g}")
        sys.exit(1)

    print(f"[scope_guard] OK — {len(files)} file(s) within scope for role '{args.role}'")
    sys.exit(0)


if __name__ == "__main__":
    main()
