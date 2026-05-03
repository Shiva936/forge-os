---
name: guardrail-detection
description: Detect and stop execution that violates deterministic release-safe laws
---

# Guardrail Detection

## Goal

Block unsafe execution before code or planning drift occurs.

## Detect

* Repeatable automation implemented only as ephemeral terminal snippets instead of `/.forge/scripts/` when the step is deterministic and reused (see `.cursor/rules/forge-scripts.mdc`)
* Python invoked outside `.venv` (system `python`, global `pip`, or IDE default interpreter for repo tasks)
* missing explicit version or target arguments
* planning from `/.forge/requirements` or `/.forge/tmp`
* missing canonical release synthesis before planning
* changelog writes outside `/.forge/releases/changelog.json`
* changelog history mutation (non-append behavior)
* cumulative validation omissions in `/release-check`
* unsafe rollback and boundary violations
* application installs or product builds at repository root instead of **`projects/`** (see **`.cursor/rules/sandbox-projects.mdc`**)

## Enforcement

1. Stop execution when a hard law is violated
2. Return explicit violation with evidence
3. Require correction path before resume
4. Escalate when architecture or release truth is at risk

## Final Rule

Guardrails are mandatory execution gates.
