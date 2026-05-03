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
