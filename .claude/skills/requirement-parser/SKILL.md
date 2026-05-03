---
name: requirement-parser
description: Parse raw requirements into temporary normalized release inputs
---

# Requirement Parser

## Goal

Convert raw requirement sources into normalized markdown under `/.forge/tmp/`.
This skill prepares release synthesis input only.

## Version Awareness

Input directory must be explicit:
`/.forge/requirements/requirements-vX/*`
Never guess version boundaries.

## Workflow

1. Read all raw requirement sources for one explicit version only
2. **Prefer** persisted tooling: run `.forge/scripts/normalize_requirements_to_tmp.py --version vX` via `.venv` when it exists (see `.cursor/rules/forge-scripts.mdc`). If that script is missing or insufficient, **add or extend** a script under `/.forge/scripts/` and document it, then run it — do not rely on throwaway one-liners as the only artifact.
3. Use **only** the project venv Python to run `markitdown` (or any parser). Examples: Windows `.\.venv\Scripts\python.exe`, Unix `./.venv/bin/python`. Install deps with that same venv's `pip` (e.g. `pip install "markitdown[docx]"`). Never use bare `python` / system Python for normalization.
4. Use Python `markitdown` first for binary docs (DOCX/PDF)
5. Parse explicit functional and non-functional requirements
6. Parse explicit stack and boundary constraints
7. Surface contradictions and unresolved ambiguity
8. Write normalized markdown files to `/.forge/tmp/`
9. Update `/.forge/tmp/parsed_index.json`
10. Do not synthesize execution plans in this skill

## Required Output

Produce temporary normalized files only:

* markdown files in `/.forge/tmp/`
* `/.forge/tmp/parsed_index.json`
* contradiction report section per normalized file

## Hard Rules

* prefer `/.forge/scripts/` for repeatable normalize/changelog steps; extend there if missing (`.cursor/rules/forge-scripts.mdc`)
* never run normalization or any Python without the repo `.venv` interpreter
* never start coding
* never generate execution plans
* never write release changelog entries
* never plan from raw files
* never invent requirements
* never hide contradictions
* never guess missing version boundaries

## Final Rule

Normalize for release synthesis fidelity, not documentation aesthetics.
