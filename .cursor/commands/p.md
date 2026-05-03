# p.md

**Project context** — bind this chat session to one or more application trees under **`projects/`** so that **substantive** work (edits, installs, builds, tests, new files) runs **only** inside those roots until context changes.

This command does not change the IDE’s working directory automatically; it is a **scope contract** for the agent. After `/p`, the agent must **honor** that scope for all follow-on instructions in this thread unless the user overrides in plain language.

The repository’s **Forge harness** (`.cursor/`, `.forge/` planning and scripts, root **`.venv`** for Forge tooling) remains the system of record for plans and automation. **Product** execution belongs under **`projects/<name>/`** per **`rules/sandbox-projects.mdc`** and **`skills/sandbox-execution`**.

## Command shape

```text
/p <projects>
```

Where **`<projects>`** is either:

* a **single** directory name immediately under **`projects/`** (e.g. `example-app`), or
* **multiple** names separated by **commas** (optional spaces), e.g. `example-app,other-app`.

**No argument:**

```text
/p
```

List **top-level** child directories of **`projects/`** (excluding non-directories), then stop. Do not enter project-only mode.

**Clear context:**

```text
/p clear
```

Exit project-only mode for this thread: subsequent work may span the repo again unless the user sets a new `/p` scope.

## Resolution rules

1. Split **`<projects>`** on commas, **trim** whitespace from each segment; drop empty segments.
2. Reject path separators, `..`, absolute paths, and hidden-only names (e.g. a segment equal to `.` or `..`). **Project id** is a single path segment: **`^[a-zA-Z0-9._-]+$`** (adjust only if a real on-disk name requires it; if in doubt, verify existence below).
3. For each id, require **`projects/<id>/`** to exist **from repo root** and be a **directory**. If any id is missing or not a directory: **stop**, list which ids failed, and suggest **`/p`** alone to discover valid names.
4. **Active set** = the ordered list of validated **`projects/<id>/`** roots (dedupe by id, preserve first occurrence order).
5. Invoking **`/p`** with a new non-empty list **replaces** the previous active set (it does not merge unless the user explicitly asks to add projects in natural language after listing multiple names in one `/p` command including all intended ids).

## Session contract (until `/p clear` or a new `/p`)

Until context is cleared or replaced, the agent must:

* **Default all product work** to paths under **`projects/<id>/`** for **`<id>`** in the active set — source, configs, app virtualenvs, **`node_modules`**, lockfiles, and build outputs for the product live there only.
* **Not** install application dependencies, create app **`go.mod`**, product **`Cargo.toml`** roots, or application **Python venvs** at **repository root**; root **`.venv`** stays **Forge-only** (**`python-runtime.mdc`**).
* **Prefer** terminal **`cd`** (or per-command paths) into the relevant **`projects/<id>/`** when running product toolchains; when multiple ids are active, state **which** tree each command targets before running it.
* **Restrict edits and new files** for product/feature work to the active **`projects/<id>/`** trees. Do not change unrelated **`projects/<other>/`** trees without explicit user instruction.
* **Searching and reading** may still use the wider repo when needed (e.g. plan tasks under **`.forge/plans/`**, shared contracts). **Writing** outside the active set requires an explicit user override in the same thread.

**Multi-project:** when more than one id is active, treat the scope as the **union** of those directories. Any change must be attributable to one of them; do not use multi-project mode as an excuse to touch arbitrary paths.

## Evidence and handoff

At the start of each **non-trivial** response after `/p`, briefly state the **active project context** (ids and absolute or repo-relative roots) so scope stays obvious across long threads.

## Forbidden

* Silently expanding scope to **`projects/`** siblings not in the active set
* Guessing project names when validation fails
* Treating a **`/p`** invocation as completed without verifying directories exist

## Optional bootstrap

When another command (e.g. **`/build`**, **`/test`**) expects **`.forge/config.json`**, you may still run **`refresh_runtime_config.py`** from repo root and read that file — **read-only** harness bootstrap only; product commands themselves remain under the active **`projects/<id>/`** roots.

## Final rule

**`/p`** sets **where product truth lives** for this conversation. If scope and directory layout disagree, **stop** and reconcile with the user before changing files.
