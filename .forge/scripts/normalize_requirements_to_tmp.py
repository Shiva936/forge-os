#!/usr/bin/env python3
"""
Convert DOCX (and other supported sources) under .forge/requirements/requirements-v{X}/ to
normalized markdown under .forge/tmp/, and write .forge/tmp/parsed_index.json.

Requires project venv (run Cursor /init or .forge/scripts/setup_forge_venv.*) so
requirements-forge.txt is installed (includes markitdown[docx]).

Run (from repo root):
  .venv\\Scripts\\python.exe .forge/scripts/normalize_requirements_to_tmp.py --version v0
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
    parser = argparse.ArgumentParser(description="Normalize requirement DOCX to .forge/tmp")
    parser.add_argument(
        "--version",
        required=True,
        help="Version tag, e.g. v0 (uses .forge/requirements/requirements-v0/)",
    )
    args = parser.parse_args()
    raw = args.version.strip()
    # Accept "0", "v0", "v12"
    tag = raw if raw.startswith("v") else f"v{raw}"

    root = repo_root()
    req_dir = root / ".forge" / "requirements" / f"requirements-{tag}"
    out_dir = root / ".forge" / "tmp"
    index_path = root / ".forge" / "tmp" / "parsed_index.json"

    if not req_dir.is_dir():
        print(f"ERROR: requirement directory not found: {req_dir}", file=sys.stderr)
        return 1

    try:
        from markitdown import MarkItDown
    except ImportError as e:
        print(
            "ERROR: markitdown not installed in this interpreter. "
            'Install with: pip install "markitdown[docx]"',
            file=sys.stderr,
        )
        print(e, file=sys.stderr)
        return 1

    out_dir.mkdir(parents=True, exist_ok=True)
    md_converter = MarkItDown()
    normalized_rel: list[str] = []

    docx_files = sorted(req_dir.glob("*.docx"))
    if not docx_files:
        print(f"ERROR: no .docx files under {req_dir}", file=sys.stderr)
        return 1

    for docx in docx_files:
        out_file = out_dir / f"requirements-{tag}__{docx.stem}.md"
        result = md_converter.convert(str(docx))
        out_file.write_text(result.text_content, encoding="utf-8")
        rel = out_file.relative_to(root / ".forge")
        normalized_rel.append(str(rel).replace("\\", "/"))

    idx = {
        "version": tag,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "sources": sorted(d.name for d in docx_files),
        "normalized_files": normalized_rel,
    }
    index_path.write_text(json.dumps(idx, indent=2), encoding="utf-8")

    print(f"Normalized {len(docx_files)} file(s) -> {out_dir}")
    print(f"Wrote {index_path.relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
