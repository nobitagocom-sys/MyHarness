#!/usr/bin/env python3
"""
pre-commit hook for Harness scope enforcement.

Reads active role from .harness-role (root of repo) or HARNESS_ROLE env var,
then runs scope_guard.py against staged files.

Install: copy/symlink this file to .git/hooks/pre-commit and make it executable
         (chmod +x .git/hooks/pre-commit).
"""

import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ROLE_FILE = REPO_ROOT / ".harness-role"
SCOPE_GUARD = REPO_ROOT / ".harness" / "enforce" / "scope_guard.py"


def get_role() -> str | None:
    if role := os.environ.get("HARNESS_ROLE"):
        return role.strip()
    if ROLE_FILE.exists():
        return ROLE_FILE.read_text().strip()
    return None


def main():
    role = get_role()
    if not role:
        # No role set — skip silently (not all commits are agent commits)
        sys.exit(0)

    result = subprocess.run(
        [sys.executable, str(SCOPE_GUARD), "--role", role, "--staged"],
        cwd=str(REPO_ROOT),
    )
    if result.returncode != 0:
        print(
            f"\n[pre-commit] Blocked: scope violation for role '{role}'.\n"
            f"  To bypass (use with caution): git commit --no-verify\n"
            f"  To change role: echo <role> > .harness-role"
        )
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
