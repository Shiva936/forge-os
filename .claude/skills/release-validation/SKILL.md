---
name: release-validation
description: Validate whether the current system is actually ready for release from both technical and product perspectives
---

# Release Validation

## Goal

Determine whether the system is truly ready for release.

Not whether it compiles.

Not whether features exist.

Validate release truth.

## Workflow

1. Read requirements, plans, contracts, and acceptance criteria
2. Validate cumulative release files from v0 through target: `/.forge/releases/release-vN.md`
3. Verify implemented behavior against intended product outcome
4. Detect regressions and hidden deviations
5. Validate operational readiness and rollback safety
6. Validate security, stability, and user trust boundaries
7. Confirm release scope is complete

## Required Output

Produce:

1. Requirement Coverage Report
2. Missing Requirements
3. Product Deviations
4. Regression Risks
5. Stability Risks
6. Security Risks
7. Rollback Readiness
8. Release Blockers
9. Go / No-Go Recommendation
10. Cumulative Prior-Promise Integrity

## Hard Rules

* passing tests alone is not release readiness
* feature completion alone is not release readiness
* technical correctness without product correctness is failure
* hidden regressions block release
* unclear rollback paths block release
* validating latest delta only is forbidden

## Final Rule

If trust breaks after release, validation failed.
