# auto-build.md

Use Builder Agent in autonomous loop mode with:

* explicit target from command argument
* engineering
* failure-analysis
* release-validation
* guardrail-detection
* execution-loop

Command supports explicit arguments.

Examples:

/auto-build task-001
/auto-build milestone-2
/auto-build plan-v0
/auto-build task-007
/auto-build milestone-01
/auto-build plan-v3

## Argument Rules

If task is provided:

run continuous Build -> Test -> Validate loops for that task until validated

also run cumulative validation for all prerequisite tasks (dependency chain) up to that task before final success

If milestone is provided:

run one active task at a time in milestone order

advance only after current task is validated

before declaring milestone success, validate all prior milestones and tasks up to and including the requested milestone

If plan is provided:

run tasks in `/.forge/plans/plan-vX/tasks/INDEX.md` dependency order

continue through plan tasks until release validation is GO

and perform cumulative release validation from `release-v0` through target `release-vX` (same cumulative truth model as `/release-check`)

If no target is provided:

stop immediately

do not guess

ask explicitly for:

* task id
* milestone target
  or
* plan target

Never silently choose execution scope.
Execution truth must remain explicit.

## Run Mode

Autonomous loop mode stays active until one of these terminal conditions:

1. Target validates successfully (task/milestone) or release-level validation reaches GO (plan).
2. User manually stops execution.
3. Guardrails trigger a mandatory stop.
4. Required input/decision is missing and user response is needed.

## Mandatory Loop

Build -> Test -> Validate -> Refine/Fix -> Repeat

## Cumulative Validation Law

`/auto-build` is cumulative by default:

* target `task-YYY` => validate dependency-prior tasks + `task-YYY`
* target `milestone-Z` => validate milestones/tasks from start through `milestone-Z`
* target `plan-vX` => validate plan execution and release truth cumulatively (`v0 -> vX`)

Never mark the target complete if earlier required scope is not validated.

Additional required behavior:

* after 2-3 failed fix attempts on the same issue, switch to instrumentation-first debugging (temporary logs/prints/probes), collect evidence, then remove temporary instrumentation after validation
* do not continue blind speculative patching
* preserve rollback safety for each iteration

## You Must

* stay inside declared target scope
* preserve architecture boundaries and contracts
* validate failure paths and regressions
* produce explicit evidence at each validation gate
* escalate No-Go immediately when automatic No-Go conditions are hit

## Forbidden

* do not infer missing target/version
* do not run unplanned work outside selected scope
* do not skip guardrail or validation gates
* do not claim done without evidence

## Final Rule

Autonomy is allowed.
Unvalidated progress is not.
