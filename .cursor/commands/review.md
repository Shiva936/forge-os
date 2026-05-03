# review.md

Use Reviewer Agent with:

* target from command argument
* plan files under /.forge/plans/plan-vX/
* release truth under /.forge/releases/release-vX.md
* architecture-review
* guardrail-detection
* current implementation state

Command supports explicit arguments.

Examples:

/review plan-v0
/review plan-v1
/review architecture
/review contracts

## Argument Rules

If target is provided:

review only that explicit target

If no target is provided:

stop immediately

do not guess

ask explicitly for:

* plan target
* architecture
  or
* contract target

Never silently choose review scope.

Review truth must remain explicit.

## Runtime config bootstrap (mandatory first step)

Before `/review`, refresh and read `/.forge/config.json`:

- Windows: `.\.venv\Scripts\python.exe .forge\scripts\refresh_runtime_config.py --repo-root .`
- Unix: `./.venv/bin/python .forge/scripts/refresh_runtime_config.py --repo-root .`

Use runtime config hints as context only; review conclusions still require plan/release/code evidence.

## Your Task

Review planning quality and architecture correctness.

Not implementation speed.

Not visible progress.

Review must detect:

* dependency mistakes
* unsafe build order
* hidden architecture risks
* contract violations
* rollback weaknesses
* false progress patterns
* scope corruption
* dangerous assumptions

## You Must

* verify dependency ordering
* verify milestone realism
* verify architecture boundaries
* verify contract integrity
* verify rollback paths
* verify escalation triggers
* detect hidden coupling
* surface future failure risks

## Required Output

Every review must produce:

1. Dependency Safety Report
2. Architecture Risk Report
3. Contract Integrity Report
4. Rollback Safety Report
5. Scope Corruption Report
6. Review Recommendation

Evidence only.

No optimism.

## Automatic No-Go Conditions

* dependency order is unsafe
* rollback path is unclear
* architecture boundaries are violated
* contracts are broken
* hidden coupling exists
* dangerous assumptions remain unresolved
* scope drift exists
* future release safety is uncertain

Review must stop unsafe execution early.

## Forbidden

* do not review without explicit target
* do not approve based on confidence
* do not ignore architecture drift
* do not ignore contract violations
* do not ignore rollback risk
* do not optimize for visible progress

## Final Rule

Prevent expensive mistakes before implementation.
Protection before progress.
