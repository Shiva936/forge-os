# Launches Forge PreToolUse policy script with repo .venv (Windows).
$ErrorActionPreference = 'Stop'
$root = $env:CLAUDE_PROJECT_DIR
if (-not $root) { exit 0 }
$py = Join-Path $root '.venv\Scripts\python.exe'
$script = Join-Path $root '.forge\scripts\claude_pretooluse_forge.py'
if (-not (Test-Path $py)) { exit 0 }
& $py $script
