#!/usr/bin/env python3
"""
Print early markdown headings from .forge/tmp/requirements-{tag}__*.md for quick sanity checks.

Run (from repo root):
  .venv\\Scripts\\python.exe .forge/scripts/preview_tmp_headings.py --tag v0 --max-lines 200
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def main() -> int:
    parser = argparse.ArgumentParser(description="Preview headings in normalized tmp markdown")
    parser.add_argument("--tag", required=True, help="e.g. v0 (matches requirements-v0__*.md prefix)")
    parser.add_argument("--max-lines", type=int, default=200, help="Scan first N lines per file")
    parser.add_argument("--max-headings", type=int, default=15, help="Print at most N headings per file")
    args = parser.parse_args()

    tag = args.tag
    if not tag.startswith("v"):
        tag = f"v{tag}"

    root = repo_root()
    tmp = root / ".forge" / "tmp"
    pattern = f"requirements-{tag}__*.md"
    files = sorted(tmp.glob(pattern))
    if not files:
        print(f"No files matching {pattern} under {tmp}", file=sys.stderr)
        return 1

    for path in files:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        scan = lines[: args.max_lines]
        heads = [ln for ln in scan if ln.strip().startswith("#")]
        print(f"=== {path.name} (chars={sum(len(l) for l in lines)}) ===")
        for h in heads[: args.max_headings]:
            print(h[:200])
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
