# /auto-plan (Claude Code)

> **Canonical spec:** `.cursor/commands/auto-plan.md` — load and execute that file in full. If this header disagrees, **the Cursor file wins.**

---

# auto-plan.md

Use Planner Agent in autonomous loop mode with:

* explicit plan version target from command argument
* command composition: **`/plan` + `/review` + `/guard` + `/fix`**
* requirement-parser
* execution-planner
* guardrail-detection
* failure-analysis
* corrective-action
* review command (`/review plan-vX`) as a mandatory quality gate
* guard command (`/guard plan-vX`) as a mandatory safety gate
* fix command (`/fix <failing-target>`) as mandatory recovery path after any No-Go

Command supports explicit arguments.

Examples:

/auto-plan -v0
/auto-plan -v3
/auto-plan -vX

## Argument Rules

If version is provided:

map strictly:

requirements-vX -> release-vX -> plan-vX

run autonomous planning loop only for that explicit version until integrity checks pass.

If version is missing:

stop immediately
do not guess
ask explicitly for target version

Never silently infer release boundaries.
Version truth must remain explicit.

## Runtime config bootstrap (mandatory first step)

Before loop start, refresh and read `/.forge/config.json`:

- Windows: `.\.venv\Scripts\python.exe .forge\scripts\refresh_runtime_config.py --repo-root .`
- Unix: `./.venv/bin/python .forge/scripts/refresh_runtime_config.py --repo-root .`

Use config values as runtime capability hints only; do not treat them as executable command storage.

## Scope Law (single-version only)

`/auto-plan` is **not cumulative across versions**.

For target `-vX`, operate only on:

* `/.forge/requirements/requirements-vX/`
* `/.forge/tmp/*` (only as normalization output)
* `/.forge/releases/release-vX.md`
* `/.forge/plans/plan-vX/`

Forbidden:

* editing `release-vY.md` where `Y != X`
* editing `plan-vY/` where `Y != X`
* reading prior plan versions as planning input

## Mandatory Autonomous Flow

For `/auto-plan -vX`, execute this sequence in loop-safe deterministic mode:

1. Run **`/plan -vX`** (this command owns normalize -> release -> plan generation flow)
2. Normalize generated outputs to remove append/duplication drift (prefer `/.forge/scripts/normalize_plan_outputs.py --version vX`)
3. Validate plan integrity (prefer `/.forge/scripts/validate_plan_integrity.py --version vX`)
4. Run **`/review plan-vX`** and require evidence-based review output
5. If review is No-Go, run **`/fix plan-vX-review`**, then restart from step 4
6. Run **`/guard plan-vX`** and require explicit Stop/Proceed output
7. If guard is Stop/No-Go, run **`/fix plan-vX-guard`**, then restart from step 4
8. Repeat until review + guard both pass, guardrails stop execution, or user manually stops

## Run Mode

Autonomous loop remains active until one terminal condition:

1. `release-vX` and `plan-vX` integrity checks pass.
2. `review plan-vX` returns no no-go conditions.
3. `guard plan-vX` returns Proceed with no hard-stop violations.
4. User manually stops execution.
5. Guardrails trigger mandatory stop.
6. Required input is missing and user response is needed.

## You Must

* stay inside target version scope only
* preserve release-truth-first law (`requirements -> tmp -> releases -> plans`)
* keep plan generation deterministic and merge-safe
* produce evidence for normalization + integrity steps
* treat **`/plan -vX`**, **`/review plan-vX`**, **`/guard plan-vX`**, and **`/fix ...`** as mandatory composed commands
* treat `/review plan-vX` as mandatory before completion
* treat `/guard plan-vX` as mandatory before completion
* invoke `/fix` after any review/guard no-go and restart from `/review plan-vX`
* stop immediately on no-go guardrail violations

## Forbidden

* do not infer version
* do not touch prior/future plan versions
* do not skip normalize/integrity checks
* do not skip mandatory `/plan -vX` composition step
* do not skip mandatory `/review plan-vX` gate
* do not skip mandatory `/guard plan-vX` gate
* do not skip mandatory `/fix` after any no-go detection
* do not plan from raw requirements/tmp after release synthesis step
* do not claim done without integrity evidence

## Final Rule

Autonomy is allowed.
Cross-version drift is not.
