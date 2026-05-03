# validate.md

Use Validation Agent with:

* target from command argument
* release-validation
* guardrail-detection
* current implementation state
* release truth from /.forge/releases/release-vX.md

Command supports explicit arguments.

Examples:

/validate task-001
/validate milestone-2
/validate release-v0
/validate plan-v1

## Argument Rules

If target is provided:

validate only that explicit target

If no target is provided:

stop immediately

do not guess

ask explicitly for:

* task
* milestone
* release
  or
* plan target

Never silently choose validation scope.

Validation truth must remain explicit.

## Your Task

Validate reality.

Not code alone.

Not passing tests alone.

Not assumptions.

Validation must prove that the implementation satisfies:

* technical correctness
* product correctness
* architecture correctness
* release readiness

## You Must

* validate requirement coverage
* validate acceptance criteria
* detect regressions
* verify rollback safety
* verify failure handling
* detect product deviations
* surface architecture drift
* produce Go / No-Go recommendation

## Required Output

Every validation must produce:

1. Requirement Coverage Report
2. Regression Report
3. Failure Path Report
4. Product Deviation Report
5. Release Recommendation

Evidence only.

No optimism.

## Automatic No-Go Conditions

* incomplete acceptance criteria
* regressions exist
* rollback path is unsafe
* architecture guarantees are broken
* trust boundaries are violated
* failure handling is incomplete
* hidden deviations exist
* product correctness is uncertain

No-Go must be explicit.

## Forbidden

* do not validate without explicit target
* do not approve based on confidence
* do not ignore failure paths
* do not ignore regressions
* do not validate code without validating outcome
* do not hide uncertainty

## Final Rule

Reality wins.
If proof does not exist, validation failed.
