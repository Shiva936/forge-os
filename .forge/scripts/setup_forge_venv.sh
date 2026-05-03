#!/usr/bin/env bash
# Create repository .venv and install requirements-forge.txt (Forge Python runtime).
# Usage: ./.forge/scripts/setup_forge_venv.sh [--force]
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

FORCE=0
if [[ "${1:-}" == "--force" ]] || [[ "${1:-}" == "-f" ]]; then
  FORCE=1
fi

if [[ "$FORCE" -eq 1 ]] && [[ -d .venv ]]; then
  rm -rf .venv
fi

if [[ ! -d .venv ]]; then
  if command -v python3 >/dev/null 2>&1; then
    python3 -m venv .venv
  else
    python -m venv .venv
  fi
fi

./.venv/bin/python -m pip install --upgrade pip
./.venv/bin/pip install -r requirements-forge.txt

echo "Forge venv ready: $ROOT/.venv/bin/python"
