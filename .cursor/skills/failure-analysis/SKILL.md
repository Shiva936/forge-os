---
name: failure-analysis
description: Identify root causes of failures and prevent symptom-based fixes
---

# Failure Analysis

## Goal

Find the true root cause of failures before any fix is applied.

Do not patch symptoms.

Do not guess.

Investigate first.

## Workflow

1. Identify what failed
2. Identify where failure originated
3. Separate symptom from root cause
4. Determine whether failure is local or architectural
5. Identify blast radius and affected systems
6. Define safe correction path and rollback path
7. Check whether failure is caused by execution-law violation (version guessing, wrong planning source, changelog mutation)

## Required Output

Produce:

1. Failure Description
2. Root Cause
3. Symptom vs Cause Separation
4. Impact Scope
5. Blast Radius
6. Safe Fix Path
7. Rollback Path
8. Regression Risks
9. Validation Plan After Fix
10. Execution-Law Compliance Findings

## Hard Rules

* never apply speculative fixes
* never stack multiple unverified fixes
* never hide uncertainty
* never mark issue resolved without validation
* never optimize for fast patching over correct resolution

## Final Rule

Fix causes, not symptoms.
