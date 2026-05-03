#!/usr/bin/env python3
"""
Append one entry to .forge/releases/changelog.json (append-only ledger).

The repository uses **format 1**:
  { "format": 1, "entries": [ { "id", "date", "summary", "components" }, ... ] }

Run (from repo root):
  .venv\\Scripts\\python.exe .forge/scripts/append_changelog_entry.py ^
    --id v0-2026-05-03-my-entry --summary "Short description" --component .forge/plans

Legacy JSON array format at the root is rejected with an error (migrate manually).
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def main() -> int:
    p = argparse.ArgumentParser(
        description="Append entry to .forge/releases/changelog.json (format 1)"
    )
    p.add_argument("--id", required=True, help="Unique entry id, e.g. v0-2026-05-03-scope-fix")
    p.add_argument("--summary", required=True)
    p.add_argument(
        "--date",
        help="ISO date YYYY-MM-DD (default: today's UTC date)",
    )
    p.add_argument(
        "--component",
        action="append",
        default=[],
        dest="components",
        help="Repeatable component path or label",
    )
    args = p.parse_args()

    root = repo_root()
    changelog_path = root / ".forge" / "releases" / "changelog.json"

    if args.date:
        date_str = args.date.strip()
    else:
        date_str = datetime.now(timezone.utc).date().isoformat()

    entry = {
        "id": args.id.strip(),
        "date": date_str,
        "summary": args.summary.strip(),
        "components": list(args.components),
    }

    if changelog_path.exists():
        raw = json.loads(changelog_path.read_text(encoding="utf-8"))
        if isinstance(raw, list):
            print(
                "ERROR: changelog.json uses legacy root array format. "
                "Convert to { \"format\": 1, \"entries\": [ ... ] } then retry.",
                file=sys.stderr,
            )
            return 1
        if not isinstance(raw, dict):
            print("ERROR: changelog.json must be a JSON object", file=sys.stderr)
            return 1
        if raw.get("format") != 1:
            print(
                "ERROR: changelog.json format must be 1 for this script.",
                file=sys.stderr,
            )
            return 1
        entries = raw.get("entries")
        if not isinstance(entries, list):
            print('ERROR: changelog.json must have an "entries" array', file=sys.stderr)
            return 1
        existing_ids = {e.get("id") for e in entries if isinstance(e, dict)}
        if entry["id"] in existing_ids:
            print(f"ERROR: duplicate entry id: {entry['id']}", file=sys.stderr)
            return 1
        entries.append(entry)
        out = {"format": 1, "entries": entries}
    else:
        changelog_path.parent.mkdir(parents=True, exist_ok=True)
        out = {"format": 1, "entries": [entry]}

    changelog_path.write_text(json.dumps(out, indent=4) + "\n", encoding="utf-8")
    n = len(out["entries"])
    print(f"Appended entry; total records: {n} -> {changelog_path.relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
