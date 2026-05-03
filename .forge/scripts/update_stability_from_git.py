#!/usr/bin/env python3
"""Auto-mark plan task stability rows UNSTABLE based on git changes."""

from __future__ import annotations

import argparse
import fnmatch
import re
import subprocess
from pathlib import Path


TASK_ROW_RE = re.compile(
    r"^\|\s*(TASK-\d+)\s*\|\s*(UNSTABLE|STABLE)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*$"
)

DEFAULT_TRACKER = """# 08_STABILITY_TRACKER

Auto-generated bootstrap tracker.

## Task checklist

| Task | Status | Tracked scope (change detection) | Last GO evidence | Last validated at |
|------|--------|----------------------------------|------------------|-------------------|
"""


def _git_changed_files(repo_root: Path) -> list[str]:
    cmd = ["git", "-C", str(repo_root), "status", "--porcelain"]
    completed = subprocess.run(cmd, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or "git status failed")
    paths: list[str] = []
    for raw in completed.stdout.splitlines():
        line = raw.rstrip()
        if not line:
            continue
        path = line[3:] if len(line) > 3 else ""
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        path = path.replace("\\", "/")
        if path:
            paths.append(path)
    return paths


def _normalize_pattern(pattern: str) -> str:
    p = pattern.strip().strip("`")
    if not p:
        return p
    if p.endswith("/**"):
        return p + "*"
    return p


def _matches_any_scope(file_path: str, scope_cell: str) -> bool:
    patterns = [_normalize_pattern(part.strip()) for part in scope_cell.split(",")]
    for pattern in patterns:
        if not pattern:
            continue
        if fnmatch.fnmatch(file_path, pattern):
            return True
    return False


def update_tracker(repo_root: Path, tracker_path: Path, dry_run: bool) -> int:
    changed_files = _git_changed_files(repo_root)
    content = tracker_path.read_text(encoding="utf-8")
    updated_lines: list[str] = []
    changed_rows = 0

    for line in content.splitlines():
        match = TASK_ROW_RE.match(line)
        if not match:
            updated_lines.append(line)
            continue

        task_id, status, scope_cell, evidence, validated = match.groups()
        should_unstable = any(_matches_any_scope(path, scope_cell) for path in changed_files)

        if should_unstable and status != "UNSTABLE":
            changed_rows += 1
            updated_lines.append(
                f"| {task_id} | UNSTABLE | {scope_cell} | AUTO-UNSTABLE: git change detected | — |"
            )
        else:
            updated_lines.append(line)

    if dry_run:
        print(f"Dry run: would update {changed_rows} row(s) in {tracker_path}")
        return 0

    tracker_path.write_text("\n".join(updated_lines) + "\n", encoding="utf-8", newline="\n")
    print(f"Updated {changed_rows} row(s) in {tracker_path}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Update stability tracker from git file changes")
    parser.add_argument("--repo-root", default=".", help="Repository root path")
    parser.add_argument("--plan-version", required=True, help="Plan version, e.g. v0")
    parser.add_argument("--dry-run", action="store_true", help="Show updates without writing")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    tracker_path = repo_root / ".forge" / "plans" / f"plan-{args.plan_version}" / "08_STABILITY_TRACKER.md"
    if not tracker_path.exists():
        tracker_path.parent.mkdir(parents=True, exist_ok=True)
        tracker_path.write_text(DEFAULT_TRACKER, encoding="utf-8", newline="\n")
        print(f"Initialized missing tracker: {tracker_path}")

    return update_tracker(repo_root, tracker_path, args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
