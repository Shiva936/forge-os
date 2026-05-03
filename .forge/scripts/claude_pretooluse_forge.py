#!/usr/bin/env python3
"""
Claude Code PreToolUse hook — stdin is hook JSON (see Anthropic hooks docs).

Enforces Forge sandbox policy: application dependency installs must not run from
repo harness directories (root, .forge, .cursor, etc.); use ``projects/<name>/``
or Forge ``.venv`` for ``requirements-forge.txt`` / ``.forge/scripts``.

Always exits 0. On violation, prints JSON with ``permissionDecision: deny`` to stdout.
If no violation, exits 0 with no stdout (allow).
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

_INSTALL_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"(?i)\bpip3?\s+install\b"),
    re.compile(r"(?i)\bpython(?:3)?(?:\.exe)?\s+-m\s+pip\s+install\b"),
    re.compile(r"(?i)\bpy(?:\.exe)?\s+-m\s+pip\s+install\b"),
    re.compile(r"(?i)\bnpm\s+install\b"),
    re.compile(r"(?i)\bnpm\s+ci\b"),
    re.compile(r"(?i)\bpnpm\s+install\b"),
    re.compile(r"(?i)\byarn\s+install\b"),
)


def _deny(reason: str) -> None:
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": reason,
                }
            }
        )
    )
    raise SystemExit(0)


def _cwd_under_projects(root: Path, cwd: Path) -> bool:
    proj = (root / "projects").resolve()
    try:
        cwd.resolve().relative_to(proj)
        return True
    except ValueError:
        return cwd.resolve() == proj


def _command_uses_repo_venv(cmd: str, root: Path) -> bool:
    norm = cmd.replace("\\", "/").lower()
    root_venv = (root / ".venv").as_posix().lower()
    if ".venv/" in norm or ".venv\\" in cmd.lower():
        return True
    if norm.startswith(root_venv):
        return True
    return False


def _matches_install(cmd: str) -> bool:
    return any(rx.search(cmd) for rx in _INSTALL_PATTERNS)


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError):
        return 0

    root_raw = os.environ.get("CLAUDE_PROJECT_DIR")
    if not root_raw:
        return 0

    root = Path(root_raw).resolve()
    tool_name = data.get("tool_name")
    if tool_name not in ("Bash", "PowerShell"):
        return 0

    ti = data.get("tool_input") or {}
    cmd = ti.get("command") or ti.get("script") or ""
    if not isinstance(cmd, str):
        return 0

    cwd_raw = data.get("cwd") or str(root)
    try:
        cwd = Path(cwd_raw).resolve()
    except (OSError, ValueError):
        cwd = root

    if _cwd_under_projects(root, cwd):
        return 0

    if not _matches_install(cmd):
        return 0

    if _command_uses_repo_venv(cmd, root):
        return 0

    _deny(
        "Forge: dependency installs from this working directory must use ``projects/<name>/`` "
        "for application trees, or invoke repo ``.venv`` (Forge) explicitly. "
        "Refuse bare pip/npm/pnpm/yarn install at repo harness roots. See ``.cursor/rules/sandbox-projects.mdc``."
    )
    return 0


if __name__ == "__main__":
    main()
