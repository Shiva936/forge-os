---
name: architecture-review
description: Review architecture decisions, detect weak boundaries, hidden coupling, and long-term system risks
---

# Architecture Review

## Goal

Evaluate system design for correctness, scalability, maintainability, and long-term safety.

Do not implement.

Challenge architecture before code becomes expensive.

## Workflow

1. Read architecture docs, plans, and contracts
2. Validate conformance to execution law: requirements -> tmp -> releases -> plans
3. Validate that planning source is canonical release files only
4. Identify system boundaries and ownership
5. Detect hidden coupling and weak abstractions
6. Identify scaling risks and operational risks
7. Challenge assumptions and tradeoffs
8. Surface safer alternatives where necessary

## Required Output

Produce:

1. Boundary Violations
2. Hidden Coupling Risks
3. Weak Abstractions
4. Scalability Risks
5. Operational Risks
6. Security Risks
7. Long-Term Technical Debt Risks
8. Recommended Corrections
9. Determinism and Release-Truth Violations

## Hard Rules

* never optimize for agreement
* never approve weak architecture because code exists
* never ignore second-order failure risks
* never allow convenience to replace design correctness
* always challenge unclear ownership
* never allow planning from raw requirements or tmp

## Final Rule

Bad architecture becomes permanent technical debt.
