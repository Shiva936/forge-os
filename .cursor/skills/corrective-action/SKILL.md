---
name: corrective-action
description: Apply minimal, validated corrections after root-cause analysis
---

# Corrective Action

## Goal

Apply the smallest safe correction that resolves a validated root cause.

## Workflow

1. Consume failure-analysis output (root cause, impact, rollback).
2. Define one correction unit tied to explicit target scope.
3. Apply minimal change set only for that correction unit.
4. Preserve architecture boundaries and release/version truth.
5. Validate correction against the failing gate/check.
6. If validation fails 2-3 times, require temporary instrumentation before more edits.
7. Remove temporary instrumentation after a validated fix.

## Required Output

Produce:

1. Correction Target
2. Applied Change Summary
3. Why This Fix Addresses Root Cause
4. Rollback Safety Statement
5. Re-validation Evidence
6. Residual Risk

## Hard Rules

* never fix without failure-analysis output
* never apply broad speculative rewrites
* never change unrelated files
* never bypass guardrails or validation gates
* never claim fixed without evidence from rerun checks

## Final Rule

Corrective actions are only complete when the failing gate turns green with evidence.
