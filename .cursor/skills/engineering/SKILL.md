---
name: engineering
description: Execute tasks with deterministic, requirement-driven, release-safe discipline
---

# Engineering

## Goal

Deliver implementation safely from plan truth with proof-based completion.

## Workflow

1. Read explicit target task from `/.forge/plans/plan-vX/tasks/TASK-YYY.md`
2. Build only in declared scope; put **application** installs, app venvs, and product build trees under **`projects/`** (see **`rules/sandbox-projects.mdc`**, **`sandbox-execution`** skill) — root **`.venv`** is for Forge scripts only
3. Run tests and validation: use root **`.venv`** only for Forge scripts/tooling (`python-runtime.mdc`); for implementation under **`projects/`**, use that subtree’s toolchain and test commands
4. Verify rollback safety and failure handling
5. Confirm product correctness, not just technical correctness

## Hard Rules

* never guess target task or version
* never execute outside approved plan scope
* never skip build-test-validate loop
* never mark complete without evidence
* never break prior release guarantees
* never bypass guardrails
* never run project tests, scripts, or tools with system Python when `.venv` is the project runtime

## Final Rule

Implementation speed is irrelevant without validated correctness.
