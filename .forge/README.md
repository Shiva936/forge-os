# `.forge/` — release and plan truth

This directory holds **requirement intake, normalized scratch, canonical releases, execution plans, and deterministic scripts** for **Forge**. It is the on-disk partner to **`.cursor/`** commands (`/plan`, `/build`, etc.).

**Python:** Scripts under **`scripts/`** expect a repository virtual environment at the repo root (**`.venv/`**). Do not use system Python for them. On a fresh clone, run Cursor **`/init`** or the setup scripts (see **root `README.md`**, **`requirements-forge.txt`**, and **`.cursor/commands/init.md`**) so **`requirements-forge.txt`** is installed into **`.venv`**.

**Git:** Parts of **`.forge/`** are listed in **`.gitignore`** (see repo root); clones may not ship every artifact by default — align tracking with your team. The **`.venv/`** directory is gitignored and is never committed.

## Layout

| Path | Role |
|------|------|
| **`requirements/requirements-vX/`** | Raw inputs (e.g. DOCX) per version |
| **`tmp/`** | Normalized markdown + **`parsed_index.json`** — ephemeral vs **`release-vX.md`** |
| **`releases/`** | **`release-vX.md`** (canonical truth) and **`changelog.json`** (append-only ledger) |
| **`plans/plan-vX/`** | Execution plans derived **only** from **`releases/release-vX.md`** |
| **`scripts/`** | Venv Python, venv setup (`setup_forge_venv.*`), helpers (normalize, changelog, previews) — see **`scripts/README.md`** |

## Pipeline (mandatory order)

```text
requirements -> tmp -> releases -> plans -> build
```

Details and guardrails: **`.cursor/README.md`**, **`commands/plan.md`**, **`commands/init.md`** (environment setup), **`rules/architecture.mdc`**, **`rules/forge-scripts.mdc`**.
