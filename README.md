# forge-os

Engineering and release workflow for **Forge**: requirement intake, normalized scratch, canonical releases, and versioned execution plans. Cursor slash commands live under **`.cursor/`**; on-disk artifacts and scripts under **`.forge/`**.

## First-time setup (Python / Forge tools)

1. **Python 3** on your `PATH` (`python` / `python3`, or on Windows the **`py`** launcher).
2. Create the repo virtual environment and install dependencies from **`requirements-forge.txt`** (not committed: **`.venv/`** is gitignored):
   * **Cursor:** run **`/init`** (see **`.cursor/commands/init.md`**).
   * **Windows (PowerShell), from repo root:**  
     `powershell -NoProfile -ExecutionPolicy Bypass -File .forge/scripts/setup_forge_venv.ps1`  
     To remove an existing venv and recreate: add **`-Force`**.
   * **macOS / Linux:**  
     `./.forge/scripts/setup_forge_venv.sh` (use **`--force`** to recreate).
3. Use **only** the venv interpreter for project Python (see **`.cursor/rules/python-runtime.mdc`**).  
   Example: `.\.venv\Scripts\python.exe` (Windows) or `./.venv/bin/python` (Unix).

Forge Python packages (e.g. **`markitdown[docx]`** for DOCX normalization) are listed in **`requirements-forge.txt`**. Add new dependencies there, then re-run **`/init`** or the setup script.

## Where to read next

| Topic | Location |
|--------|----------|
| Cursor commands (`/init`, `/plan`, …), skills, rules | **`.cursor/README.md`** |
| `.forge/` layout, pipeline, release vs plan truth | **`.forge/README.md`** |
| Sandbox (`projects/`) | **`.cursor/rules/sandbox-projects.mdc`**, **`skills/sandbox-execution/SKILL.md`** |
| Script-by-script usage (normalize, changelog, venv setup) | **`.forge/scripts/README.md`** |

## Repository layout (high level)

| Path | Role |
|------|------|
| **`requirements-forge.txt`** | Pinned list for the repo **`.venv`** (Forge scripts, `markitdown`, etc.) |
| **`.cursor/`** | Slash commands, `rules/`, `skills/`, `subagents/` |
| **`.forge/`** | `requirements/`, `tmp/`, `releases/`, `plans/`, `scripts/` |
| **`projects/`** | Sandbox for application builds and deps; see **`rules/sandbox-projects.mdc`**; contents under **`projects/*`** typically gitignored |
