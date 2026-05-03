# Cursor execution system (`.cursor/`)

This folder is not general IDE configuration. It is the **operational intelligence layer** for building this product: deterministic workflows, explicit versioning, requirement-driven truth, and release-safe guardrails.

If you treat it as "prompts," you will bypass the laws and produce invisible drift. Use it as an **execution operating system**.

---

## What this is

| Concept | Meaning |
|--------|---------|
| **requirements** | Raw source input under `.forge/requirements/requirements-vX/` |
| **tmp** | Temporary normalization only under `.forge/tmp/` (`parsed_index.json` + normalized markdown) |
| **releases** | Canonical release truth: `.forge/releases/release-vX.md` |
| **plans** | Execution truth: `.forge/plans/plan-vX/` |
| **changelog** | Historical release ledger: **only** `.forge/releases/changelog.json` (append-only) |
| **`.cursor/`** | Commands, rules, skills, and subagents that enforce the flow |

**Mandatory global flow:**

```text
requirements -> tmp -> releases -> plans -> build -> validate -> review -> release-check
```

Planning and normalization happen **inside one command**: `/plan -vX`. There is no separate normalize step.

---

## Repository layout this system assumes

```text
(requirements-forge.txt)        <- venv package list for Forge Python; install via /init
.forge/
├── requirements/
│   └── requirements-vX/
├── tmp/
│   ├── (normalized markdown only)
│   └── parsed_index.json
├── releases/
│   ├── release-vX.md
│   └── changelog.json          <- sole changelog; append-only
├── scripts/                    <- persisted automation (venv Python); prefer these over ad-hoc snippets
│   ├── README.md
│   ├── setup_forge_venv.ps1
│   ├── setup_forge_venv.sh
│   └── *.py
└── plans/
    └── plan-vX/
```

**Hard rules:**

- Do **not** plan directly from raw requirements, tmp, or binary files. Planning input is **`.forge/releases/release-vX.md` only** (after synthesis in `/plan`).
- Do **not** put changelog history anywhere except `.forge/releases/changelog.json`.
- Do **not** add top-level `.forge/PLAN.md`, `.forge/AGENT.md`, `.forge/VALIDATION.md`, `.forge/GUARDRAILS.md`, or separate `.forge/contracts/` / `.forge/architecture/` roots — those concerns live here under `.cursor/` and inside each `plan-vX/` tree.

---

## What lives under `.cursor/`

| Path | Role |
|------|------|
| `commands/` | Slash-command specs: what to run, with **explicit arguments** |
| `rules/` | Always-on laws (`*.mdc`) — version truth, planning source, changelog, rollback |
| `skills/` | Reusable procedure modules (parse requirements, plan from release, validate release, etc.) |
| `subagents/` | Role contracts for Planner, Builder, Validator, Reviewer, Release, Guardrail |

---

## Commands (explicit arguments only)

Most commands **must** receive an explicit target. If the argument is missing: **stop and ask** — never infer version or scope. **Exception:** **`/init`** takes no arguments (see **`commands/init.md`**).

| Command | Typical args | What it does |
|---------|----------------|---------------|
| `/init` | *(none)* | Create **`.venv`** at repo root and **`pip install -r requirements-forge.txt`** (see **`commands/init.md`**) |
| `/plan` | `-v0`, `-v1`, `-vX` | Parse requirements -> normalize to `tmp` -> write `release-vX.md` -> append `changelog.json` -> generate `plan-vX/` **from release file only** |
| `/build` | `task-001`, `milestone-2`, ... | Execute **one** scoped task from the active plan |
| `/auto-build` | `task-001`, `milestone-2`, `plan-v0`, ... | Run autonomous Build->Test->Validate->Refine/Fix loops with cumulative validation up to target scope (task deps, prior milestones, or release v0->vX), until success/GO, guardrail stop, or manual stop |
| `/validate` | `task-001`, `release-v0`, `plan-v1`, ... | Evidence-based validation (not "tests passed") |
| `/review` | `plan-v0`, ... | Review dependency order, boundaries, contracts, rollback |
| `/release-check` | `-v3`, ... | **Cumulative** validation: `release-v0` ... `release-vX` vs current system |
| `/guard` | `task-004`, `plan-v1`, ... | Hard stop if execution laws would be violated |
| `/test` | **`win`** \| **`unix`**, then **`task-001`**, **`forge-scripts`**, … | **`/test win …`** / **`/test unix …`** — **`.venv`** Python only; see `commands/test.md` |

Read the canonical wording in each file under `commands/`.

---

## Python runtime (`.venv`)

All Python used for this repository — including `/plan` normalization (`markitdown`), **`.forge/scripts/*.py`**, tests, and package installs — **must** run inside **`/.venv`** at the repo root.

**First clone or broken venv:** run **`/init`** (or **`.forge/scripts/setup_forge_venv.ps1`** / **`setup_forge_venv.sh`** from the repo root — see **`commands/init.md`**). That creates **`.venv`** and installs **`requirements-forge.txt`** (Forge dependencies such as **`markitdown[docx]`**). Add new Python deps by editing **`requirements-forge.txt`**, then re-run **`/init`** or the setup script. **`.venv/`** is gitignored and is not committed.

| Platform | Interpreter | Package installs |
|----------|----------------|------------------|
| Windows | `.venv\Scripts\python.exe` | `.venv\Scripts\pip.exe` |
| macOS / Linux | `.venv/bin/python` | `.venv/bin/pip` |

Do not use bare `python`, `pip`, or `py` for project work unless you have verified they point at `.venv` (default: assume they do not). Full rules: `rules/python-runtime.mdc`.

---

## `.forge/scripts/` (repeatable automation)

Deterministic steps used during **`/plan`** (DOCX->tmp, changelog append, previews, etc.) **must** use scripts from **`.forge/scripts/`** when available.

* If the script you need **does not exist**, **add it under `.forge/scripts/`**, document usage in **`.forge/scripts/README.md`**, run it with **`.venv`**, and reuse it from then on.
* Do not leave the only copy of repeatable logic in a one-off terminal session.

Full rules: `rules/forge-scripts.mdc`.

---

## How to use this optimally

### 1. Always anchor version and scope

- Pass **explicit** `-vX` for planning and release-check.
- Pass **explicit** task or milestone for build, validate, guard.
- Never rely on "current context" or implicit "latest" unless your team has a separate written convention (this repo does not).

### 2. Run `/plan -vX` as the single front door for a release line

Optimal sequence when requirements change:

1. Put or update raw inputs under `.forge/requirements/requirements-vX/`.
2. Run **`/plan -vX`** once per meaningful release synthesis (not per typo — batch coherent changes).
3. Inspect **`.forge/releases/release-vX.md`** — if it is wrong, fix synthesis inputs or contradictions before any implementation.

### 3. Treat `release-vX.md` as law for planners; treat `plan-vX/` as law for builders

- **Planners** must not skip to tasks without a synthesized release file.
- **Builders** must not implement outside **`.forge/plans/plan-vX/tasks/`** scope.

### 4. Use `/guard` before high-risk or ambiguous work

Run **`/guard`** with the same target you are about to execute when:

- Touching boundaries between components or ownership
- Changing persistence, auth, or failure semantics
- You feel scope creep — guardrails exist to **stop**, not to rubber-stamp

### 5. Validate cumulatively before shipping

For "are we safe to ship vN?" use **`/release-check -vN`**, not only "what changed last week." Production holds **all prior promises** from v0 through N.

### 6. Keep changelog append-only

- New release -> **append** one object to `.forge/releases/changelog.json`.
- Never rewrite or reorder historical entries.

### 7. Align skills with the phase you are in

| Phase | Primary skills |
|-------|----------------|
| Ingest / normalize | `requirement-parser` |
| Plan from release truth | `execution-planner` |
| Implement | `engineering` (+ `sandbox-execution` when installing app-level deps or builds) |
| Review design | `architecture-review` |
| Incidents / bugs | `failure-analysis` |
| Ship readiness | `release-validation` |
| Hard stops | `guardrail-detection` |

Skills are invoked by commands and subagents; follow their `SKILL.md` files literally.

---

## Typical workflows

### New version line (e.g. v2)

1. Ensure **`.venv`** is initialized (**`/init`** if needed).
2. Create `.forge/requirements/requirements-v2/` and add sources.
3. **`/plan -v2`** -> produces `.forge/tmp/*`, `.forge/releases/release-v2.md`, changelog append, `.forge/plans/plan-v2/`.
4. **`/review plan-v2`** before coding if scope or boundaries are non-trivial.
5. **`/build task-...`** per task in order.
6. **`/validate task-...`** or **`/validate plan-v2`** at meaningful checkpoints.
7. **`/release-check -v2`** before release.

### Day-to-day implementation

1. Pick the **next** task from `.forge/plans/plan-vX/tasks/` (respect `INDEX.md` / milestone order).
2. **`/guard task-...`** if risky.
3. **`/build task-...`**
4. **`/validate task-...`**

### Post-incident or regression

1. **`failure-analysis`** mindset: root cause, blast radius, rollback path.
2. If the same issue fails after **2-3** fix attempts, switch to **instrumentation-first debugging** (temporary logs/prints/probes) to pinpoint the break.
3. Remove temporary instrumentation after validated fix; keep evidence in validation output.
4. Fix with minimal scope; **`/validate`** the same target plus regression surfaces.

---

## Anti-patterns (will burn you)

- Running repo Python or `pip` outside `.venv`.
- Installing app dependencies or doing product builds at repository root instead of **`projects/`** (see `sandbox-projects.mdc`).
- Planning from `.forge/requirements/` or `.forge/tmp/` directly.
- Creating `changelog.json` under `plans/` or anywhere except `.forge/releases/`.
- Skipping **`release-vX.md`** synthesis and "going straight to tasks."
- **`/release-check`** only for the latest version instead of cumulative v0->N.
- Marking work done without **evidence** (tests alone are not completion).

---

## Rules are not suggestions

Files in `rules/` are **always applied**. They encode:

- explicit version truth
- planning source = release files only
- append-only changelog
- proof before completion
- rollback safety and guardrail stops

When in doubt, open `rules/architecture.mdc`, `rules/anti-patterns.mdc`, and `rules/execution-loop.mdc` first.

---

## Quick reference: where to look

| I need to... | Open |
|------------|------|
| Set up **`.venv`** and Forge packages (`markitdown`, etc.) | `commands/init.md`, root **`requirements-forge.txt`**, `.forge/scripts/setup_forge_venv.ps1` / `setup_forge_venv.sh` |
| Persisted `/plan` helpers (normalize, changelog) | `.forge/scripts/` + `rules/forge-scripts.mdc` |
| Run the exact `/plan` pipeline | `commands/plan.md` |
| Run autonomous execution pipeline | `commands/auto-build.md` |
| See build vs validation expectations | `commands/build.md`, `commands/validate.md` |
| Cumulative release gate | `commands/release-check.md` |
| Hard-stop guard semantics | `commands/guard.md` |
| Always-on laws | `rules/*.mdc` (includes `python-runtime.mdc`, `forge-scripts.mdc`, `sandbox-projects.mdc`) |
| Project sandbox (`projects/`) | `rules/sandbox-projects.mdc`, `skills/sandbox-execution/SKILL.md` |
| Procedure detail | `skills/*/SKILL.md` |
| Agent behavior contract | `subagents/*.md` |

This README is the map; the **`commands/`** and **`rules/`** files are the source of truth.
