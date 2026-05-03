# `.forge/scripts/`

Deterministic, repeatable commands for Forge documentation and validation flows.

Scope: this folder is for Forge harness automation only. Project-specific build/test scripts belong under `projects/<project>/scripts/` and should be documented in that project's `README.md`.
Project-specific script outputs must go to `projects/<project>/tmp/` (for example logs, test result snapshots, temporary generated reports) and be excluded from Git tracking.

## Prerequisites

**Python virtualenv:** Forge **`*.py`** scripts expect **`/.venv`** at the repository root, with packages from **`requirements-forge.txt`** installed.

1. Run Cursor **`/init`** (see **`.cursor/commands/init.md`**), **or** from repo root:
   * Windows: `powershell -NoProfile -ExecutionPolicy Bypass -File .forge/scripts/setup_forge_venv.ps1` (`-Force` to delete and recreate **`.venv`**)
   * Unix: `./.forge/scripts/setup_forge_venv.sh` (`--force` to recreate)
2. Invoke scripts with the venv interpreter only (see **`.cursor/rules/python-runtime.mdc`**).

## Scripts

| Script | Purpose |
|--------|---------|
| `setup_forge_venv.ps1` | **Windows:** create `.venv` and install `requirements-forge.txt`. Repo root: `powershell -NoProfile -ExecutionPolicy Bypass -File .forge/scripts/setup_forge_venv.ps1` (`-Force` to wipe existing `.venv`). Prefer Cursor **`/init`**. |
| `setup_forge_venv.sh` | **Unix:** same as above: `./.forge/scripts/setup_forge_venv.sh` (`--force` to recreate). |
| `normalize_requirements_to_tmp.py` | Convert `.forge/requirements/requirements-vX/*.docx` → `.forge/tmp/requirements-vX__*.md` and refresh `.forge/tmp/parsed_index.json`. Requires `.venv` (run **`/init`** first). Example: `.\.venv\Scripts\python.exe .forge\scripts\normalize_requirements_to_tmp.py --version v0` |
| `append_changelog_entry.py` | Append to `.forge/releases/changelog.json` (**`format`: 1** with `id`, `date`, `summary`, `components`). Example: `.\.venv\Scripts\python.exe .forge\scripts\append_changelog_entry.py --id v0-2026-05-03-foo --summary "…" --component .forge/plans` |
| `preview_tmp_headings.py` | Preview headings in normalized tmp markdown (see script `--help`). |
| `normalize_plan_outputs.py` | Normalize append-style generation drift in `release-vX.md` and `plan-vX/**/*.md` by keeping the final canonical section (e.g. `# ... — plan-vX`). Example: `.\.venv\Scripts\python.exe .forge\scripts\normalize_plan_outputs.py --version v0` |
| `validate_plan_integrity.py` | Validate generated plans: no duplicate top-level headers and no missing task files referenced by `tasks/INDEX.md`. Example: `.\.venv\Scripts\python.exe .forge\scripts\validate_plan_integrity.py --version v0` |
| `refresh_runtime_config.py` | Refresh runtime capability cache in `.forge/config.json` (`host_os`, `wsl_available`, docker/rancher availability, forge `.venv` presence). Creates `.forge/config.json` if missing. Example: `.\.venv\Scripts\python.exe .forge\scripts\refresh_runtime_config.py --repo-root .` |
| `update_stability_from_git.py` | Auto-mark `STABLE` task rows back to `UNSTABLE` in `08_STABILITY_TRACKER.md` when tracked scope files changed in git status. Initializes tracker file when missing. Example: `.\.venv\Scripts\python.exe .forge\scripts\update_stability_from_git.py --plan-version v0` |
| `claude_pretooluse_forge.py` | **Claude Code only:** `PreToolUse` hook policy (stdin = hook JSON). Blocks bare `pip`/`npm`/`pnpm`/`yarn` installs when `cwd` is **not** under `projects/` unless the command references repo **`.venv`**. Invoked by **`.claude/hooks/pretooluse_forge_launch.*`** from **`.claude/settings.json`**. |
