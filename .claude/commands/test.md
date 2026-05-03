# /test (Claude Code)

> **Canonical spec:** `.cursor/commands/test.md` — load and execute that file in full. If this header disagrees, **the Cursor file wins.**

---

# test.md

Run **automated or scripted checks** for an explicit **environment** and **target**. Do not infer either argument.

The repository’s published scope is **Forge** (`.cursor/` + `.forge/`). Do not assume other products, languages, or trees exist unless they are present in this checkout.

## Command shape

```text
/test <environment> <target>
```

| Argument | Allowed values | Meaning |
|----------|----------------|--------|
| **environment** | `win` | Run on the **Windows host** using the repo **`.venv`** Python only. |
| **environment** | `unix` | Run on a **Unix-like** environment (Linux, macOS, or **WSL** on Windows): repo **`.venv`** Python only. On Windows, use **WSL when available**. |
| **target** | `task-001`, `forge-scripts`, … | Scope from **`.forge/plans/plan-vX/tasks/`**, or **`forge-scripts`** to smoke-test **`.forge/scripts/*.py`**. |

## Examples

```text
/test win task-001
/test unix forge-scripts
```

## Argument rules

**Both** `environment` and `target` are required.

If either is missing:

stop immediately

do not guess

ask for both in order: **`win` or `unix`**, then **target**

Never silently choose environment or scope.

## Runtime config bootstrap (mandatory first step)

Before `/test`, refresh and read `/.forge/config.json`:

- Windows: `.\.venv\Scripts\python.exe .forge\scripts\refresh_runtime_config.py --repo-root .`
- Unix: `./.venv/bin/python .forge/scripts/refresh_runtime_config.py --repo-root .`

For `unix` on Windows, use config hint `wsl_available` to decide WSL execution path; if unavailable, report explicitly.

## Mapping target → commands

Use **only** the repository **`.venv`** interpreter (see **`.cursor/rules/python-runtime.mdc`**).

### Target **`forge-scripts`**

From repo root:

* **Windows:** `.\.venv\Scripts\python.exe -m compileall .forge\scripts -q` and invoke each script with **`--help`** as a smoke check; run **`normalize_requirements_to_tmp.py`** only when inputs exist under **`.forge/requirements/`**.
* **Unix:** `./.venv/bin/python -m compileall .forge/scripts -q` and the same **`--help`** passes.

### Target **`task-XXX`**

Resolve **`task-XXX`** against **`.forge/plans/plan-vX/tasks/`**. Run checks that the task’s acceptance criteria imply **within Forge** (e.g. **`pytest`** via **`.venv`** if tests exist, scripts under **`.forge/scripts/`**, or documented manual verification).

### Environment **`win`** vs **`unix`**

* **`win`:** Windows paths and shells.
* **`unix`:** use when verification needs POSIX paths, shell semantics, or cross-host parity with Linux/macOS/WSL.
* On **Windows hosts**, `unix` means: **run in WSL if available**. If WSL is unavailable, report that explicitly and do not claim Unix parity from a Windows-only run.

**Evidence label:** record **environment**, **target**, exact commands, and output (pass/fail).

## Forbidden

* do not run **`/test`** without **both** environment and target
* do not claim **`unix`** parity after only a **`win`** run when the task requires Unix semantics
* do not use system Python outside **`.venv`**
* do not invoke compilers, crates, or runners for components that are not part of **Forge** in this repo

## Final Rule

Same proof standard as **`/build`**: checks mean nothing without the chosen environment and recorded output.
