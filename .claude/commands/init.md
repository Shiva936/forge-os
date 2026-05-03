# /init (Claude Code)

> **Canonical spec:** `.cursor/commands/init.md` — load and execute that file in full. If this header disagrees, **the Cursor file wins.**

---

# init.md

Initialize the **Forge Python environment** at the repository root: create **`.venv`** and install packages from **`requirements-forge.txt`** (including **`markitdown[docx]`** and other listed deps).

This command has **no version arguments**. Run **`/init`** once per clone (or after a broken venv).

## Runtime config bootstrap (mandatory first step)

Before `/init`, read `/.forge/config.json` when present for host/runtime hints. If missing, proceed with setup and create runtime cache afterward using:

- Windows: `.\.venv\Scripts\python.exe .forge\scripts\refresh_runtime_config.py --repo-root .`
- Unix: `./.venv/bin/python .forge/scripts/refresh_runtime_config.py --repo-root .`

## Mandatory execution flow

1. **Working directory:** repository root (`forge-os` / this repo’s root).
2. **Prefer persisted scripts** (do not hand-roll venv paths unless scripts are missing):
   * **Windows (PowerShell):**  
     `powershell -NoProfile -ExecutionPolicy Bypass -File .forge/scripts/setup_forge_venv.ps1`  
     Clean recreate: add **`-Force`**.
   * **macOS / Linux:**  
     `chmod +x .forge/scripts/setup_forge_venv.sh` (once if needed), then  
     `./.forge/scripts/setup_forge_venv.sh`  
     Clean recreate: **`--force`**.
3. **Verify:**  
   * Windows: `.\.venv\Scripts\python.exe -c "import markitdown; print('ok')"`  
   * Unix: `./.venv/bin/python -c "import markitdown; print('ok')"`
4. **If script fails:** create **`python -m venv .venv`** (or **`py -3 -m venv .venv`** on Windows), then install with the venv’s **pip**:  
   `pip install -r requirements-forge.txt`  
   (always use the venv interpreter’s pip — see **`rules/python-runtime.mdc`**).

## Hard constraints

* Do **not** install Forge packages with system **`pip`** or global Python for ongoing repo work.
* After **`/init`**, all Python for this repo MUST use **`.venv`** only (`rules/python-runtime.mdc`).
* **`requirements-forge.txt`** is the single source of truth for Forge venv packages; extend it when new script dependencies are added, then re-run **`/init`** or the setup script.
* Root **`.venv`** is **Forge tooling only**. Application-level Python environments and other product installs belong under **`projects/`** per **`.cursor/rules/sandbox-projects.mdc`** — do not reuse **`.venv`** for sandbox apps.

## References

* **`requirements-forge.txt`** — package pins / list  
* **`.forge/scripts/README.md`** — script index  
* **`rules/python-runtime.mdc`** — venv-only execution  
* **`.cursor/rules/sandbox-projects.mdc`**, **`skills/sandbox-execution`** — **`projects/`** sandbox for built work  
