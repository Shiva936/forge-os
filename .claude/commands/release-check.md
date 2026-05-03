# /release-check (Claude Code)

> **Canonical spec:** `.cursor/commands/release-check.md` — load and execute that file in full. If this header disagrees, **the Cursor file wins.**

---

# release-check.md

Use Release Agent with:

* target version from command argument
* release-validation
* guardrail-detection
* all release files up to target version
* all relevant plans up to target version
* current implementation state
* current production-ready code state

Command supports explicit arguments.

Examples:

/release-check -v1
/release-check -v2
/release-check -v3

## Argument Rules

If version is provided:

load cumulative release scope:

release-v0.md -> release-vX.md

and corresponding:

plan-v0 → plan-vX

Example:

/release-check -v3

means validate cumulative canonical release truth:

/.forge/releases/release-v0.md
/.forge/releases/release-v1.md
/.forge/releases/release-v2.md
/.forge/releases/release-v3.md

against:

current codebase and production-ready system state

If version is missing:

stop immediately

do not guess

ask explicitly for target release version

Never silently infer release boundaries.

Release truth must remain explicit.

## Runtime config bootstrap (mandatory first step)

Before `/release-check`, refresh and read `/.forge/config.json`:

- Windows: `.\.venv\Scripts\python.exe .forge\scripts\refresh_runtime_config.py --repo-root .`
- Unix: `./.venv/bin/python .forge/scripts/refresh_runtime_config.py --repo-root .`

Use runtime config hints to ensure cumulative checks run in a supported environment.

## Your Task

Validate cumulative system truth.

Not latest delta only.

Not isolated milestone correctness.

Release validation must prove:

Does the current system satisfy everything promised from v0 to target version?

This includes:

* prior guarantees
* backward compatibility
* old contracts
* regression safety
* architecture preservation
* trust boundaries
* operational readiness
* current release expectations

## You Must

* validate cumulative requirement coverage
* verify no prior guarantees were broken
* detect regressions across releases
* verify architecture integrity
* verify rollback safety
* verify release readiness
* verify product correctness
* produce final Go / No-Go decision

## Required Output

Every release check must produce:

1. Cumulative Requirement Coverage Report
2. Regression Report
3. Architecture Integrity Report
4. Rollback Safety Report
5. Product Correctness Report
6. Release Recommendation

Decision must be:

GO
or
NO-GO

Evidence only.

No optimism.

## Automatic No-Go Conditions

* any prior guarantee is broken
* regressions exist
* rollback path is unsafe
* architecture guarantees are broken
* trust boundaries are violated
* failure handling is incomplete
* hidden deviations exist
* product correctness is uncertain
* release readiness is incomplete

No-Go must be explicit.

## Forbidden

* do not validate latest release only
* do not ignore old guarantees
* do not approve based on confidence
* do not hide regressions
* do not skip rollback verification
* do not silently accept partial completion

## Final Rule

Release validation is cumulative.
Production contains all prior promises.
If proof does not exist, release must not happen.
