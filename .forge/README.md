# `.forge/` — release and plan truth

This directory holds **requirement intake, normalized scratch, canonical releases, execution plans, and deterministic scripts** for **Forge**. It is the on-disk partner to **both** execution interfaces:

* **Cursor** — **`.cursor/commands/`** (`/plan`, `/build`, `/test`, …)
* **Claude Code** — **`.claude/commands/`** (same procedures; see **`.claude/README.md`**)

**One pipeline:** there is **no** Cursor-only or Claude-only fork of releases, changelog, or plans. **Normative laws** remain in **`.cursor/rules/*.mdc`**.

---

## Harness vs product

This repository is the **engineering workflow** (rules, **`.forge/`**, scripts). The **application or system you ship** is a separate concern; drive it through this pipeline and implement it under **`projects/`** (separate tree, usually its own Git history and **gitignored** under **`projects/*`** here). Do not treat forge-os as the product codebase unless a task explicitly says otherwise.

---

## Python and `.venv`

Scripts under **`scripts/`** expect a repository virtual environment at the repo root (**`.venv/`**). Do not use system Python for them.

On a fresh clone:

* **Cursor:** **`/init`** — **`.cursor/commands/init.md`**
* **Claude Code:** same flow — **`.claude/commands/init.md`**; session charter **`.claude/CLAUDE.md`**

Also: **root `README.md`**, **`requirements-forge.txt`**, and **`.forge/scripts/setup_forge_venv.*`**.

---

## Scope boundary for `scripts/`

**`/.forge/scripts/`** is **only** for Forge harness automation (requirements normalization, release/changelog helpers, planning support, **Claude Code `PreToolUse` policy** — **`claude_pretooluse_forge.py`**). Project-specific build/test scripts must live under **`projects/<project>/scripts/`**, documented in **`projects/<project>/README.md`**. Project-local outputs (logs, captures, temp exports) go under **`projects/<project>/tmp/`** and stay out of Git.

Full script index: **`scripts/README.md`**.

---

## Git and tracking

Parts of **`.forge/`** are **gitignored** at the repo root (see **`.gitignore`**): typically **`tmp/`**, **`requirements/*`**, **`releases/*`**, **`plans/*`**, and **`.forge/config.json`**, with **`.gitkeep`** exceptions where the repo keeps empty anchors. Clones may not ship every generated artifact — align tracking with your team. **`.venv/`** is never committed.

---

## Sandbox

All **built projects** (app dependencies, installs, experimental trees) MUST live under **`<repo-root>/projects/`** only — **`.cursor/rules/sandbox-projects.mdc`**, **`.cursor/skills/sandbox-execution/SKILL.md`** (Claude mirror: **`.claude/skills/sandbox-execution/`**). Root **`.venv`** is **Forge tooling only** (`requirements-forge.txt`, **`.forge/scripts/`**), not for arbitrary applications.

---

## Layout

| Path | Role |
|------|------|
| **`requirements/requirements-vX/`** | Raw inputs (e.g. DOCX) per version |
| **`tmp/`** | Normalized markdown + **`parsed_index.json`** — scratch only; not a planning source for durable **`plan-vX/`** |
| **`releases/`** | **`release-vX.md`** (canonical synthesis) and **`changelog.json`** (**sole** changelog; **append-only**) |
| **`plans/plan-vX/`** | Execution plans derived **only** from **`releases/release-vX.md`** |
| **`scripts/`** | Venv Python, venv setup, normalize/changelog/plan helpers — **`scripts/README.md`** |

---

## Pipeline (mandatory order)

```text
requirements -> tmp -> releases -> plans -> build -> validate -> review -> release-check
```

* **`/plan -vX`** owns **normalization + release + plan generation** in one command (no separate normalize command).
* **Durable planning input** for **`plans/plan-vX/`** is **`releases/release-vX.md` only** — not raw **`requirements/`** or **`tmp/`** text.

**Where to read next:** **root `README.md`**, **`.cursor/README.md`**, **`.claude/README.md`**, **`.cursor/commands/plan.md`**, **`.cursor/commands/init.md`**, **`.cursor/rules/sandbox-projects.mdc`**, **`.cursor/rules/architecture.mdc`**, **`.cursor/rules/forge-scripts.mdc`**.
