# Forge canonical laws (read `.cursor/rules`)

**Normative always-on rules** for this repository live in **`.cursor/rules/*.mdc`**. Claude Code loads **`.claude/rules/*.md`**, but **Forge does not fork law text** here.

## Mandatory reads before risky work

Open and obey (at minimum):

* **`.cursor/rules/architecture.mdc`** — version boundaries, planning source, changelog, folder depth, sandbox
* **`.cursor/rules/anti-patterns.mdc`** — forbidden planning/execution/version behaviors
* **`.cursor/rules/execution-loop.mdc`** — global loop and instrumentation escalation
* **`.cursor/rules/python-runtime.mdc`** — **`.venv`**-only Forge Python
* **`.cursor/rules/sandbox-projects.mdc`** — **`projects/`** sandbox for application work
* **`.cursor/rules/forge-scripts.mdc`** — persisted automation under **`.forge/scripts/`**
* **`.cursor/rules/validation.mdc`** — evidence and completion definition
* **`.cursor/rules/engineering.mdc`** — minimal diffs, root cause, rollback
* **`.cursor/rules/git-safety.mdc`** — destructive git and history safety
* **`.cursor/rules/wsl-vwsl-testing.mdc`** — when **`win`** vs **`unix`** test evidence matters

If any instruction in chat conflicts with the above, **the `.mdc` files win**.
