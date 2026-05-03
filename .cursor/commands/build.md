# build.md

Use Builder Agent with:

* active task from current plan
* guardrail-agent
* engineering
* execution-loop

Command supports explicit arguments.

Examples:

/build task-001
/build milestone-2

## Argument Rules

If task is provided:

execute only that task

If milestone is provided:

identify active task inside that milestone

execute one task at a time

If no target is provided:

stop immediately

do not guess

ask explicitly for:

* task id
  or
* milestone target

Never silently choose execution scope.

Execution truth must remain explicit.

## Your Task

Execute only approved planned work.
Source of execution truth is `/.forge/plans/plan-vX/`.

Follow strict loop:

Build → Test → Validate → Refine/Fix → Repeat

Do not expand scope.

Do not solve future tasks early.

Do not perform unrelated refactors.

Do not create invisible architecture drift.

## You Must

* preserve previous stable behavior
* protect rollback safety
* validate failure paths
* validate regression safety
* verify product correctness
* stop on unsafe architecture boundaries
* escalate hidden dependency conflicts

## Validation Requirements

Completion requires:

* implementation exists
* tests pass
* validation succeeds
* acceptance criteria are satisfied
* no regressions exist
* rollback safety exists where required

Without proof, task is incomplete.

## Forbidden

* do not execute unplanned work
* do not guess active task
* do not optimize for visible progress
* do not patch symptoms without root cause
* do not skip failure-path validation
* do not mark incomplete work as done

## Final Rule

Execute one thing correctly.
Proof before completion.
