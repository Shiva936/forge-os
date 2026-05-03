#!/usr/bin/env python3
"""
Normalize generated release/plan markdown files to a single canonical section.

This repairs append-style generation drift where files accidentally contain
an initial generic section and then a later canonical `— plan-vX` (or release)
section in the same file.

Run from repo root:
  .venv\\Scripts\\python.exe .forge\\scripts\\normalize_plan_outputs.py --version v0
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def keep_from_marker(path: Path, marker_regex: re.Pattern[str], use_last: bool) -> bool:
    text = path.read_text(encoding="utf-8")
    matches = list(marker_regex.finditer(text))
    if not matches:
        return False
    keep_from = matches[-1].start() if use_last else matches[0].start()
    normalized = text[keep_from:].lstrip()
    if normalized == text:
        return False
    path.write_text(normalized, encoding="utf-8")
    return True


def normalize_release(root: Path, version: str) -> bool:
    rel = root / ".forge" / "releases" / f"release-{version}.md"
    if not rel.exists():
        return False
    # If multiple top-level "Release vX" headers exist, keep the last one.
    marker = re.compile(rf"(?m)^#\s+Release\s+{re.escape(version)}\b")
    return keep_from_marker(rel, marker, use_last=True)


def normalize_plan_files(root: Path, version: str) -> int:
    plan_dir = root / ".forge" / "plans" / f"plan-{version}"
    if not plan_dir.is_dir():
        return 0
    marker = re.compile(rf"(?m)^#\s+.*—\s+plan-{re.escape(version)}\s*$")
    changed = 0
    for md in sorted(plan_dir.rglob("*.md")):
        if keep_from_marker(md, marker, use_last=False):
            changed += 1
    # Task files can have duplicate H1 headers; prefer canonical em-dash task heading.
    task_marker = re.compile(r"(?m)^#\s+TASK-\d{3}\s+—\s+.+$")
    for md in sorted((plan_dir / "tasks").glob("TASK-*.md")):
        if keep_from_marker(md, task_marker, use_last=True):
            changed += 1
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize duplicated plan/release markdown outputs")
    parser.add_argument("--version", required=True, help="Version tag, e.g. v0")
    args = parser.parse_args()

    raw = args.version.strip()
    tag = raw if raw.startswith("v") else f"v{raw}"

    root = repo_root()
    release_changed = normalize_release(root, tag)
    plan_changed = normalize_plan_files(root, tag)

    print(
        f"Normalized outputs for {tag}: "
        f"release_changed={int(release_changed)} plan_files_changed={plan_changed}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
