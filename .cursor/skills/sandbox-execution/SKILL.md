---
name: sandbox-execution
description: Place all application builds and app-level deps under projects/; keep root .venv for Forge tooling only
---

# sandbox-execution

Use when **implementing** work that installs packages, compiles products, or creates app-local environments.

## Procedure

1. **Choose a directory** under **`projects/`** (e.g. **`projects/<task-id>-<slug>/`** or **`projects/<service>/`**). Create it if missing.
2. **Run toolchain initialization and installs only inside that tree** — never at forge-os root (`node_modules`, app `go.mod`, app `.venv`, etc.).
3. **Use root `.venv`** only for **`.forge/scripts/`** and **`requirements-forge.txt`** per **`python-runtime.mdc`** / **`/init`** — not for the application you are building.
4. **Document** in task notes or PR description which **`projects/...`** path holds the implementation.

## Hard stops

* Application **`pip install`** / **`npm install`** / equivalent at repository root (except **`/init`** / Forge scripts flow)
* Reusing root **`.venv`** for an application under development

## References

* **`rules/sandbox-projects.mdc`** — full policy
* **`commands/build.md`**, **`commands/init.md`**
