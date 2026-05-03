# /fix (Claude Code)

> **Canonical spec:** `.cursor/commands/fix.md` — load and execute that file in full. If this header disagrees, **the Cursor file wins.**

---

# fix.md

Use Fix Agent with:

* explicit failure target from command argument
* failure-analysis
* corrective-action
* guardrail-detection
* current execution context and failing evidence

Command supports explicit arguments.

Examples:

/fix plan-v0-review
/fix plan-v0-guard
/fix task-003-test-win
/fix task-003-validate

## Argument Rules

If target is provided:

fix only that explicit failing target

If no target is provided:

stop immediately
do not guess
ask explicitly for failing target and gate/check name

Never silently choose fix scope.

## Runtime config bootstrap (mandatory first step)

Before `/fix`, refresh and read `/.forge/config.json`:

- Windows: `.\.venv\Scripts\python.exe .forge\scripts\refresh_runtime_config.py --repo-root .`
- Unix: `./.venv/bin/python .forge/scripts/refresh_runtime_config.py --repo-root .`

Use runtime config hints to select safe execution paths (e.g., host vs WSL) during corrective actions.

## Your Task

Resolve a detected failure safely, then hand control back to the caller loop.

Execution order is mandatory:

1. Failure analysis first (root cause, blast radius, rollback path)
2. Corrective action second (minimal scoped fix)
3. Re-validation evidence capture for the failed gate/check

## Required Output

Every fix run must produce:

1. Failure Description
2. Root Cause
3. Fix Scope
4. Applied Correction
5. Rollback Safety
6. Re-validation Evidence
7. Residual Risk + next gate/check to rerun

## You Must

* fix root cause, not symptom
* keep edits minimal and scoped to the failing target
* preserve release/version/architecture boundaries
* stop and escalate when no-go remains after correction
* require instrumentation-first debugging after 2-3 failed fix attempts on same issue

## Forbidden

* do not fix without explicit failing target
* do not stack speculative fixes
* do not skip re-validation of the failed gate/check
* do not mark fixed without evidence

## Final Rule

Fixes are complete only when the previously failing gate/check passes with evidence.
