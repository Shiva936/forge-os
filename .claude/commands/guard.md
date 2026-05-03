# /guard (Claude Code)

> **Canonical spec:** `.cursor/commands/guard.md` — load and execute that file in full. If this header disagrees, **the Cursor file wins.**

---

# guard.md

Use Guardrail Agent with:

* explicit target from command argument
* guardrail-detection
* architecture rules
* engineering rules
* current execution context

Command supports explicit arguments.

Examples:

/guard task-004
/guard milestone-2
/guard plan-v1

## Argument Rules

If target is provided:

guard only that explicit target

If no target is provided:

stop immediately
do not guess
ask explicitly for task, milestone, or plan target

Never silently choose guard scope.

## Runtime config bootstrap (mandatory first step)

Before `/guard`, refresh and read `/.forge/config.json`:

- Windows: `.\.venv\Scripts\python.exe .forge\scripts\refresh_runtime_config.py --repo-root .`
- Unix: `./.venv/bin/python .forge/scripts/refresh_runtime_config.py --repo-root .`

Use runtime config hints as part of execution context evidence for Stop/Proceed decisions.

## Your Task

Stop unsafe execution before implementation damage occurs.

You must detect and block:

* version ambiguity
* planning from non-release sources
* rollback-unsafe changes
* architecture boundary violations
* contract violations
* changelog law violations
* hidden coupling or scope drift
* application dependency installs or product build trees at repository root — must use **`projects/`** (see **`rules/sandbox-projects.mdc`**)

## Required Output

Every guard run must produce:

1. Guardrail Violations Report
2. Risk Severity Classification
3. Stop / Proceed Decision
4. Required Corrections
5. Escalation Trigger Decision

## Final Rule

Guardrails are hard stops, not advice.
