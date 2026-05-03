# plan.md

Use Planner Agent with:

* requirement-parser
* execution-planner
* guardrail-detection

Command supports explicit arguments.

Examples:

/plan -v0
/plan -v1
/plan -vX

## Argument Rules

If version is provided:

map:

requirements-vX -> release-vX -> plan-vX

If version is missing:

stop immediately
do not guess
ask explicitly for target version

Never silently infer release boundaries.
Version truth must remain explicit.

## Runtime config bootstrap (mandatory first step)

Before running `/plan`, refresh and read `/.forge/config.json`:

- Windows: `.\.venv\Scripts\python.exe .forge\scripts\refresh_runtime_config.py --repo-root .`
- Unix: `./.venv/bin/python .forge/scripts/refresh_runtime_config.py --repo-root .`

Use config values only as runtime capability hints (`host_os`, `wsl_available`, docker/rancher, `.venv` availability). Do not store runnable procedures in this file.

## Mandatory Execution Flow

The `/plan` command owns BOTH normalization and planning.
There is no `/normalize`.

Execution order is mandatory:

requirements -> tmp -> releases -> plans

For `/plan -vX`, run this exact sequence:

**Python runtime:** Any Python used for parsing or tooling MUST run via the repository `.venv` only — Windows `.\.venv\Scripts\python.exe`, Unix `./.venv/bin/python` (see `rules/python-runtime.mdc`). Never use system Python.

**Persisted scripts:** For deterministic steps (DOCX->tmp, changelog append, previews), **use existing scripts under `/.forge/scripts/`** when present. If a needed script does **not** exist, **add it under `/.forge/scripts/`**, document it in `.forge/scripts/README.md`, then run it — same rule for this run and future runs (see `rules/forge-scripts.mdc`).

1. Parse raw files from `/.forge/requirements/requirements-vX/*`
2. Normalize to temporary markdown only in `/.forge/tmp/*` (prefer `.forge/scripts/normalize_requirements_to_tmp.py --version vX` when applicable)
3. Update `/.forge/tmp/parsed_index.json` (included by the normalize script above when used)
4. Synthesize canonical `/.forge/releases/release-vX.md`
5. Validate contradictions and unresolved conflicts
6. Append entry to `/.forge/releases/changelog.json` (append-only) (prefer `.forge/scripts/append_changelog_entry.py` when applicable)
7. Generate `/.forge/plans/plan-vX/` from `release-vX.md` only
8. Normalize generated outputs to avoid append/duplication drift (prefer `.forge/scripts/normalize_plan_outputs.py --version vX`)
9. Validate plan integrity before completion (prefer `.forge/scripts/validate_plan_integrity.py --version vX`)

## Hard Constraints

Planning is forbidden until release synthesis is complete.

Planning must NEVER read directly from:

* raw binary files (DOCX/PDF/PNG)
* `/.forge/requirements/*`
* `/.forge/tmp/*`

Planning is ONLY allowed from:

* `/.forge/releases/release-vX.md`

## Plan Output Contract

Generate this deterministic plan structure exactly:

`/.forge/plans/plan-vX/`
* `00_SCOPE.md`
* `01_SYSTEM_BOUNDARIES.md`
* `02_BUILD_ORDER.md`
* `03_MILESTONES.md`
* `04_VALIDATION_GATES.md`
* `05_RELEASE_CRITERIA.md`
* `06_ROLLBACK_STRATEGY.md`
* `07_ESCALATION_RULES.md`
* `08_STABILITY_TRACKER.md`
* `tasks/TASK-001.md` ... `tasks/INDEX.md`
* `contracts/API_CONTRACTS.md`
* `contracts/FAILURE_CONTRACTS.md`
* `contracts/SECURITY_CONTRACTS.md`
* `contracts/DATA_CONTRACTS.md`
* `architecture/SYSTEM_DESIGN.md`
* `architecture/COMPONENT_MAP.md`
* `architecture/DEPENDENCY_MAP.md`
* `architecture/FAILURE_BOUNDARIES.md`
* `validation/TEST_STRATEGY.md`
* `validation/ACCEPTANCE_CRITERIA.md`
* `validation/REGRESSION_RULES.md`

Max folder depth is 2.
Plans must never contain changelog files.
Plan and release markdown must not contain duplicate top-level canonical headers.
`tasks/INDEX.md` must not reference missing `TASK-*.md` files.

## Final Rule

Release truth before execution truth.
No proof, no plan.
