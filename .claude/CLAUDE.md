# ForgeOS — Claude Code operating charter

You are executing inside **forge-os**: a **deterministic engineering and release operating system**. This file lives at **`.claude/CLAUDE.md`** and is **project memory and law** for Claude Code. It does **not** replace canonical rules under **`.cursor/rules/`**, canonical automation under **`.forge/scripts/`**, or canonical truth under **`.forge/releases/`** and **`.forge/plans/`**.

**Discovery:** Claude Code loads **`CLAUDE.md`** from the repository root **or** under **`.claude/`**; this repo keeps the charter **only** here (**`.claude/CLAUDE.md`**) alongside **`.claude/AGENTS.md`**.

**Interfaces, one OS:** **Cursor** (`.cursor/`) and **Claude Code** (`.claude/` including this file) are **different UIs** on the **same** Forge machine. **Never** invent a parallel workflow, parallel planning source, or parallel changelog.

---

## System philosophy

* **Operational truth over documentation aesthetics.** Artifacts must earn their place by supporting execution.
* **Evidence over optimism.** “Passing tests” and “it builds” are insufficient completion signals where Forge demands proof.
* **Explicit over implicit.** Versions, targets, environments, and scopes are **never** guessed.
* **Release truth before execution truth.** No synthesized **`release-vX.md`**, no durable **`plan-vX/`** generation.
* **Cumulative responsibility.** Shipping **`vN`** inherits every promise from **`v0…vN`**.

---

## Canonical directory roles

| Path | Role |
|------|------|
| **`.cursor/`** | Cursor-native commands, rules (`*.mdc`), skills, subagent contracts. **Normative rules for humans and agents:** treat **`.cursor/rules/*.mdc`** as the **canonical law text**. |
| **`.claude/`** | Claude Code-native settings, agents, skills, commands, hooks, **this file**, **`.claude/AGENTS.md`**. **Must obey the same laws**; see **`.claude/README.md`**. |
| **`.forge/requirements/`** | Raw intake only. **Not** a planning source for durable plans. |
| **`.forge/tmp/`** | Normalization scratch **only**. **Not** a planning source. |
| **`.forge/releases/release-vX.md`** | **Only** canonical input to **generate** **`plan-vX/`**. |
| **`.forge/releases/changelog.json`** | **Sole** changelog store; **append-only**; never rewrite history. |
| **`.forge/plans/plan-vX/`** | **Execution truth** for builders: tasks, contracts, architecture, validation artifacts. |
| **`.forge/scripts/`** | Repeatable automation (**`.venv`** Python). Prefer scripts over ad-hoc terminal one-liners. |
| **`projects/`** | **Sandbox** for application dependency trees and product builds. **Forbidden** at repo root: app `node_modules`, app `.venv`, product `go.mod` roots, etc. Root **`.venv`** is **Forge tooling only** (`requirements-forge.txt`). |

---

## Mandatory global workflow

```text
requirements → tmp → releases → plans → build → validate → review → release-check
```

* **`/plan -vX`** (see **`.cursor/commands/plan.md`** or **`.claude/commands/plan.md`**) owns **normalization + release synthesis + plan generation**. There is **no** separate normalize command.
* **Planning** (durable `plan-vX` contents) is **forbidden** until **`release-vX.md`** exists and contradictions are handled per pipeline.
* **Planning must never** read directly from raw binaries, **`.forge/requirements/`**, or **`.forge/tmp/`** for synthesis of execution truth. **Planner input** for generated plan structure is **`/.forge/releases/release-vX.md` only**.

---

## Python runtime (non-negotiable)

* All repository Python for Forge tooling, **`.forge/scripts/*.py`**, normalization, and repo tests **must** use **`/.venv`**.
* **Windows:** `.\.venv\Scripts\python.exe` (and `pip` from the same directory).
* **Unix:** `./.venv/bin/python` (and `./.venv/bin/pip`).
* **Never** use system Python, global `pip`, or unconstrained `python` / `py` for Forge work.
* **Application** Python environments live under **`projects/<project>/`**, not the root **`.venv`**.

---

## Engineering execution model

1. **Anchor** explicit **`-vX`**, **task id**, **milestone**, **environment** (`win` \| `unix` for **`/test`**), and **project sandbox** (**`/p`** in Cursor; same scope contract in Claude when the user declares **`projects/<name>/`**).
2. **Bootstrap runtime hints:** refresh **`/.forge/config.json`** via **`.forge/scripts/refresh_runtime_config.py`** using **`.venv`** (when the active command requires it).
3. **Execute one scoped unit** (task/milestone/plan slice) with **Build → Test → Validate → Refine/Fix → Repeat**.
4. **Stop** on guardrail violations, missing evidence, unsafe rollback, or ambiguous version/target.
5. **Instrumentation rule:** if the same issue survives **2–3** failed fix attempts, switch to **temporary** logging/instrumentation, prove root cause, then **remove** instrumentation after a validated fix.

---

## Validation expectations

Validation is **reality-based**, not vibe-based. Produce **evidence** (commands, outputs, traced code paths, risk statements). Prefer the structured outputs required by **`.cursor/commands/validate.md`**.

**Automatic No-Go** when: acceptance criteria incomplete, regressions present, rollback unsafe, trust boundaries unclear, failure handling unproven, or “confidence” substituted for proof.

**`/release-check -vX`** is **cumulative**: validate **`release-v0.md` … `release-vX.md`** (and corresponding plan realities) against the **current** system—not the latest diff only.

---

## Approval model

* **Hard stops** are encoded in **guardrail-detection** and **`.cursor/commands/guard.md`**. Treat **Stop** as final unless the user explicitly changes inputs or scope.
* **Do not** “reinterpret” a No-Go as a soft warning.
* **Do not** merge version scopes or infer release targets.

---

## Anti-pattern prevention (hard)

* Planning directly from requirements/tmp.
* Changelog writes outside **`/.forge/releases/changelog.json`**, or mutating/rewriting prior changelog entries.
* Silent version inference (`“latest”`, “the plan”, unnamed `vX`).
* Application installs/build artifacts at **repository root** (use **`projects/`**).
* Symptom-only fixes without **failure-analysis** grounding.
* Declaring completion without **validation** evidence and explicit rollback story where required.

---

## Command discipline (Claude)

Use **`.claude/commands/`** (slash commands) as the primary Claude-native entry points. Each command file instructs you to execute the **same** procedure as **`.cursor/commands/<same-name>.md`**. If a user types a Cursor-style slash out of habit, **normalize to the same law**.

**Explicit arguments only.** If a required argument is missing: **stop and ask**—never guess.

---

## Subagents and skills

* **Agents:** **`.claude/agents/*.md`** — specialized personas (planner, builder, reviewer, validator, release, architecture, security, guardrail, debugging).
* **Skills:** **`.claude/skills/*/SKILL.md`** — procedures aligned to **`.cursor/skills/`**.
* **Coordination:** subagents **do not** relax global laws; they **specialize** work under them.

---

## Cross-tool compatibility

* **`AGENTS.md`** at **`.claude/AGENTS.md`** summarizes agent roles for humans and other tools.
* **Canonical rule prose** remains in **`.cursor/rules/*.mdc`**. If **`.claude/rules/`** contains pointers, treat those pointers as mandatory loads for normative wording.

---

## Final law

**Forge is the operating system.** **Claude Code is an interface.** When in doubt, open **`.cursor/rules/architecture.mdc`**, **`.cursor/rules/anti-patterns.mdc`**, and **`.cursor/rules/execution-loop.mdc`**, then obey them.
