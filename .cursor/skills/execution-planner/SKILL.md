---
name: execution-planner
description: Convert canonical release truth into deterministic execution plans
---

# Execution Planner

## Goal

Convert canonical release files into executable implementation plans with correct build order, milestones, validation gates, and definition of done.

Do not implement.

## Workflow

1. Read only `/.forge/releases/release-vX.md`
2. Identify dependencies and system boundaries
3. Determine correct build order
4. Build deterministic plan structure under `/.forge/plans/plan-vX/`
5. Break work into milestones and task files
6. Define validation gates for each milestone
7. Define acceptance criteria, rollback points, and escalation triggers
8. Ensure task sequence preserves requirement-declared stack constraints

## Required Output

Generate this required structure:

* `00_SCOPE.md`
* `01_SYSTEM_BOUNDARIES.md`
* `02_BUILD_ORDER.md`
* `03_MILESTONES.md`
* `04_VALIDATION_GATES.md`
* `05_RELEASE_CRITERIA.md`
* `06_ROLLBACK_STRATEGY.md`
* `07_ESCALATION_RULES.md`
* `tasks/TASK-*.md` and `tasks/INDEX.md`
* `contracts/API_CONTRACTS.md`
* `contracts/FAILURE_CONTRACTS.md`
* `contracts/SECURITY_CONTRACTS.md`
* `contracts/DATA_CONTRACTS.md`
* `architecture/SYSTEM_DESIGN.md`
* `architecture/COMPONENT_MAP.md`
* `architecture/DEPENDENCY_MAP.md`
* `architecture/FAILURE_BOUNDARIES.md`
* `validation/TEST_STRATEGY.md`
* `validation/ACCEPTANCE_CRITERIA.md`
* `validation/REGRESSION_RULES.md`

## Hard Rules

* never start implementation
* never ignore dependency order
* never create parallel work that risks architecture
* never optimize for visible progress over validated progress
* never create tasks without clear completion criteria
* never plan from requirements or tmp
* never create plan changelog files
* never plan work that violates explicit stack constraints from release truth

## Final Rule

Correct sequence before fast execution.
Release truth is the only planning input.
