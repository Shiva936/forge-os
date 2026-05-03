#!/usr/bin/env python3
"""
Validate plan integrity for /.forge/plans/plan-vX.

Checks:
1) No duplicate top-level H1 headers in any markdown file.
2) All referenced TASK-XXX.md files in tasks/INDEX.md exist.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


H1_RE = re.compile(r"(?m)^#\s+.+$")
TASK_REF_RE = re.compile(r"TASK-(\d{3})\.md")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def check_duplicate_h1(plan_dir: Path) -> list[str]:
    violations: list[str] = []
    for md in sorted(plan_dir.rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        h1s = H1_RE.findall(text)
        if len(h1s) > 1:
            violations.append(f"{md}: multiple H1 headers ({len(h1s)})")
    return violations


def check_task_index(plan_dir: Path) -> list[str]:
    violations: list[str] = []
    idx = plan_dir / "tasks" / "INDEX.md"
    if not idx.exists():
        return [f"{idx}: missing tasks index"]
    text = idx.read_text(encoding="utf-8")
    refs = sorted({f"TASK-{m}.md" for m in TASK_REF_RE.findall(text)})
    for ref in refs:
        path = plan_dir / "tasks" / ref
        if not path.exists():
            violations.append(f"{idx}: references missing {path.name}")
    return violations


def check_release_header(root: Path, version: str) -> list[str]:
    violations: list[str] = []
    rel = root / ".forge" / "releases" / f"release-{version}.md"
    if not rel.exists():
        return [f"{rel}: missing canonical release file"]
    text = rel.read_text(encoding="utf-8")
    headers = re.findall(rf"(?m)^#\s+Release\s+{re.escape(version)}\b.*$", text)
    if len(headers) != 1:
        violations.append(f"{rel}: expected exactly one release H1, found {len(headers)}")
    return violations


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate plan-vX markdown integrity")
    parser.add_argument("--version", required=True, help="Version tag, e.g. v0")
    args = parser.parse_args()

    tag = args.version.strip()
    if not tag.startswith("v"):
        tag = f"v{tag}"

    root = repo_root()
    plan_dir = root / ".forge" / "plans" / f"plan-{tag}"
    if not plan_dir.is_dir():
        print(f"ERROR: plan directory not found: {plan_dir}", file=sys.stderr)
        return 1

    violations = []
    violations.extend(check_duplicate_h1(plan_dir))
    violations.extend(check_task_index(plan_dir))
    violations.extend(check_release_header(root, tag))

    if violations:
        print("PLAN INTEGRITY: FAIL")
        for v in violations:
            print(f"- {v}")
        return 2

    print("PLAN INTEGRITY: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
