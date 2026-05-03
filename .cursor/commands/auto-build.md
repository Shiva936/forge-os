# auto-build.md

Use Builder Agent in autonomous loop mode with:

* explicit target from command argument
* command composition: **`/build` + `/test` + `/validate` + `/fix`**
* engineering
* failure-analysis
* release-validation
* guardrail-detection
* execution-loop
* corrective-action

Command supports explicit arguments.

Examples:

/auto-build task-001
/auto-build milestone-2
/auto-build plan-v0

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

## Runtime config bootstrap (mandatory first step)

Before loop start, refresh and read `/.forge/config.json`:

- Windows: `.\.venv\Scripts\python.exe .forge\scripts\refresh_runtime_config.py --repo-root .`
- Unix: `./.venv/bin/python .forge/scripts/refresh_runtime_config.py --repo-root .`

Use the runtime config as capability hints for host/WSL/docker/rancher/venv checks.

## Run Mode

Autonomous loop mode stays active until one of these terminal conditions:

1. Target validates successfully (task/milestone) or release-level validation reaches GO (plan).
2. User manually stops execution.
3. Guardrails trigger a mandatory stop.
4. Required input/decision is missing and user response is needed.

## Mandatory Loop

**`/build` -> `/test` -> `/validate` -> `/fix` (when needed) -> Repeat**

Command composition by target:

- `task-YYY` target:
  - run **`/build task-YYY`**
  - run **`/test win task-YYY`** and **`/test unix task-YYY`**
  - if `win` test fails, run **`/fix task-YYY-test-win`**; if `unix` test fails, run **`/fix task-YYY-test-unix`**
  - after any test fix, rerun **`/test win task-YYY`** and **`/test unix task-YYY`** before continuing
  - run **`/validate task-YYY`**
  - if validate is No-Go, run **`/fix task-YYY-validate`**, then rerun **`/test win task-YYY`** + **`/test unix task-YYY`** -> **`/validate task-YYY`** until pass
- `milestone-Z` target:
  - for each task in milestone order, run **`/build task-YYY`** -> **`/test win task-YYY`** -> **`/test unix task-YYY`**
  - on test failure, run **`/fix task-YYY-test-win`** or **`/fix task-YYY-test-unix`** (as applicable), then rerun both env tests
  - run **`/validate task-YYY`**
  - on validate no-go, run **`/fix task-YYY-validate`**, then rerun **`/test win`** + **`/test unix`** + **`/validate`**
  - then run **`/validate milestone-Z`**
- `plan-vX` target:
  - run tasks from `tasks/INDEX.md` dependency order with composed loop per task
  - on any task-level test/validate failure, run target-specific **`/fix`** and repeat checks
  - after task-level validation, run **`/validate plan-vX`**
  - if plan-level validate is No-Go, run **`/fix plan-vX-validate`**, then rerun **`/test win`** + **`/test unix`** and **`/validate`** evidence loop for the failing scope

## Cumulative Validation Law

`/auto-build` is cumulative by default:

* target `task-YYY` => validate dependency-prior tasks + `task-YYY`
* target `milestone-Z` => validate milestones/tasks from start through `milestone-Z`
* target `plan-vX` => validate plan execution and release truth cumulatively (`v0 -> vX`)

Never mark the target complete if earlier required scope is not validated.

## Stability Cache and Opt-Out

Use `/.forge/plans/plan-vX/08_STABILITY_TRACKER.md` as canonical task/milestone stability state.
Before task execution, refresh state from git changes using `/.forge/scripts/update_stability_from_git.py --plan-version vX` (initializes tracker if missing).

- A task marked `STABLE` may be skipped by `/auto-build` only when:
  - its tracked scope shows no file changes since last GO validation, and
  - none of its dependencies are currently `UNSTABLE`.
- If any file change touches a task's tracked scope, that task must be set to `UNSTABLE` before execution continues.
- A milestone may be treated as `STABLE` only when all its tasks are `STABLE`.
- If a previously stable task or milestone becomes `UNSTABLE` due to file changes, rerun full loop (`/build` -> `/test win/unix` -> `/validate`) before restoring `STABLE`.

Additional required behavior:

* after 2-3 failed fix attempts on the same issue, switch to instrumentation-first debugging (temporary logs/prints/probes), collect evidence, then remove temporary instrumentation after validation
* do not continue blind speculative patching
* preserve rollback safety for each iteration

## You Must

* stay inside declared target scope
* preserve architecture boundaries and contracts
* validate failure paths and regressions
* produce explicit evidence at each validation gate
* run all composed commands (`/build`, `/test`, `/validate`, `/fix` when failing) for every loop cycle
* escalate No-Go immediately when automatic No-Go conditions are hit

## Forbidden

* do not infer missing target/version
* do not run unplanned work outside selected scope
* do not skip `/build`, `/test`, `/validate`, or required `/fix` in autonomous loop mode
* do not skip guardrail or validation gates
* do not claim done without evidence

## Final Rule

Autonomy is allowed.
Unvalidated progress is not.
