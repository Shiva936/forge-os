#!/usr/bin/env sh
# Launches Forge PreToolUse policy script with repo .venv (Unix or Windows layout).
set -eu
ROOT="${CLAUDE_PROJECT_DIR:?}"
SCRIPT="$ROOT/.forge/scripts/claude_pretooluse_forge.py"
if [ -x "$ROOT/.venv/bin/python" ]; then
  exec "$ROOT/.venv/bin/python" "$SCRIPT"
fi
if [ -f "$ROOT/.venv/Scripts/python.exe" ]; then
  exec "$ROOT/.venv/Scripts/python.exe" "$SCRIPT"
fi
exit 0
