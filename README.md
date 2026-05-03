# forge-os

**Forge** is a deterministic **engineering and release operating system**: requirement intake, normalized scratch, canonical releases, versioned plans, evidence-based validation, and guardrailed execution.

This repository is the **harness** (rules, automation, plans pipeline). **Product implementation** belongs under **`projects/`** (separate trees; usually gitignored here). Do not treat forge-os as the application codebase unless a task explicitly says otherwise.

---

## One operating system, two interfaces

| Interface | On disk | Role |
|-----------|---------|------|
| **Cursor** | **`.cursor/`** | Slash commands, always-on **`rules/*.mdc`**, **`skills/`**, **`subagents/`** |
| **Claude Code** | **`.claude/`** | Slash **`commands/`**, **`agents/`**, **`skills/`**, **`settings.json`**, hooks, rules pointers; charter **`CLAUDE.md`** and **`AGENTS.md`** live **only** under **`.claude/`** (not at repository root) |

**Single source of law:** **`.cursor/rules/*.mdc`**. **Single pipeline truth:** **`.forge/releases/`** and **`.forge/plans/`** (generated artifacts are mostly **gitignored**; see below). **No parallel "Claude-only" or "Cursor-only" release or changelog.**

---

## Mandatory workflow (global)

```text
requirements → tmp → releases → plans → build → validate → review → release-check
```

* **`/plan -vX`** owns **normalization + `release-vX.md` + `plan-vX/`** together. There is **no** separate normalize command.
* **Planning input** for durable plan files is **`/.forge/releases/release-vX.md` only** — not raw requirements or tmp markdown.
* **`/.forge/releases/changelog.json`** is the **only** changelog store and is **append-only**.
* **`/release-check -vX`** is **cumulative** (`v0` ... `vX`).
* **Python for Forge** runs only in repo **`.venv`** (see **`.cursor/rules/python-runtime.mdc`**). **Application** toolchains and installs live under **`projects/<name>/`** (see **`.cursor/rules/sandbox-projects.mdc`**).

Cursor and Claude use the **same** command semantics: **`.cursor/commands/*.md`** is the canonical procedure text; **`.claude/commands/*.md`** carries the same flows with a short pointer header.

---

## First-time setup (Forge `.venv`)

1. **Python 3** on your `PATH` (`python` / `python3`, or on Windows the **`py`** launcher).
2. Create **`.venv/`** at the repository root and install **`requirements-forge.txt`** (`.venv/` is gitignored):
   * **Cursor:** **`/init`** — **`.cursor/commands/init.md`**
   * **Claude Code:** same flow — **`.claude/commands/init.md`** (and **`.claude/CLAUDE.md`** for session law)
   * **Windows (PowerShell), from repo root:**  
     `powershell -NoProfile -ExecutionPolicy Bypass -File .forge/scripts/setup_forge_venv.ps1`  
     Recreate cleanly: **`-Force`**
   * **macOS / Linux:**  
     `./.forge/scripts/setup_forge_venv.sh` (`--force` to recreate)
3. Invoke Forge scripts only with the venv interpreter, e.g.  
   **Windows:** `.\.venv\Scripts\python.exe ...`  
   **Unix:** `./.venv/bin/python ...`

Add new **Forge** Python dependencies in **`requirements-forge.txt`**, then re-run **`/init`** or the setup script.

---

## Everyday entry points

| If you… | Use |
|--------|-----|
| Normalize, synthesize release, generate plan | **`/plan -vX`** |
| Implement one scoped unit | **`/build`** with explicit task or milestone |
| Run scripted checks | **`/test`** with **`win`** or **`unix`** and explicit target (see **`.cursor/commands/test.md`**) |
| Evidence-based gate | **`/validate`**, **`/review`**, **`/guard`**, **`/release-check`** |
| Bind the session to sandbox product tree(s) | **`/p`** (see **`.cursor/commands/p.md`**) — product edits/installs under **`projects/<name>/`** |

Details, tables, and anti-patterns: **`.cursor/README.md`**. Claude-specific wiring: **`.claude/README.md`**.

---

## Where to read next

| Topic | Location |
|--------|----------|
| Cursor commands, skills, rules, subagents | **`.cursor/README.md`** |
| Claude Code bundle (commands, agents, skills, settings, hooks) | **`.claude/README.md`** |
| Session charter & agent map (Claude) | **`.claude/CLAUDE.md`**, **`.claude/AGENTS.md`** |
| `.forge/` layout and pipeline | **`.forge/README.md`** |
| Sandbox policy (`projects/`) | **`.cursor/rules/sandbox-projects.mdc`**, **`.cursor/skills/sandbox-execution/SKILL.md`** (and **`.claude/skills/sandbox-execution/`** mirror) |
| Script index (normalize, changelog, venv, **Claude PreToolUse** policy script) | **`.forge/scripts/README.md`** |

---

## Repository layout (high level)

| Path | Role |
|------|------|
| **`requirements-forge.txt`** | Pins for repo **`.venv`** (Forge tooling: `markitdown`, plan helpers, etc.) |
| **`.cursor/`** | Cursor: **`commands/`**, **`rules/*.mdc`**, **`skills/`**, **`subagents/`** |
| **`.claude/`** | Claude: **`commands/`**, **`agents/`**, **`skills/`**, **`settings.json`**, **`settings.local.example.json`**, **`hooks/`**, **`memory/`**, **`rules/`** pointers, **`CLAUDE.md`**, **`AGENTS.md`** |
| **`.forge/`** | **`requirements/`**, **`tmp/`**, **`releases/`**, **`plans/`**, **`scripts/`** — see **`.forge/README.md`** |
| **`projects/`** | Application sandbox (deps, builds, product repos). **`projects/*`** is gitignored except **`projects/.gitkeep`** |

---

## What stays out of Git (by design)

Per **`.gitignore`** (adjust only with team agreement):

| Path | Why |
|------|-----|
| **`.venv/`** | Local interpreter and packages |
| **`.forge/config.json`** | Machine/runtime capability cache (not procedure storage) |
| **`.forge/tmp/*`**, **`.forge/requirements/*`**, **`.forge/releases/*`**, **`.forge/plans/*`** | Generated or local inputs (tracked exceptions: **`*.gitkeep`** where present) |
| **`.claude/settings.local.json`** | Personal Claude overrides (example: **`settings.local.example.json`**) |
| **`projects/*`** | Product trees and dependency graphs |

Do **not** commit secrets, API keys, or credentials. Use OS secret stores or ignored env files.

---

## Runtime config cache

* **`/.forge/config.json`** — refreshed by **`.forge/scripts/refresh_runtime_config.py`** using **`.venv`**; hints for host/WSL/docker/venv, **not** executable runbooks.
* **Windows:** `.\.venv\Scripts\python.exe .forge\scripts\refresh_runtime_config.py --repo-root .`
* **Unix:** `./.venv/bin/python .forge/scripts/refresh_runtime_config.py --repo-root .`
* If missing, the refresh script creates it. Many commands expect you to refresh/read it before autonomous work (see command docs).

---

## Claude Code safety note

Project **`.claude/settings.json`** enables a **`PreToolUse`** hook (via **`.claude/hooks/`** launchers) that runs **`.forge/scripts/claude_pretooluse_forge.py`**: it blocks obvious **bare package installs** when the shell **`cwd`** is **outside** **`projects/`** unless the command references repo **`.venv`**. Tune or extend in **`settings.local.json`** if your workflow needs exceptions.
