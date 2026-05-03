# `.claude/` — Claude Code interface for ForgeOS

This directory makes **Claude Code** a **first-class execution interface** for the same **Forge** operating system that **Cursor** configures under **`.cursor/`**.

**Pointers:** session charter → **`.claude/CLAUDE.md`** · agent role map → **`.claude/AGENTS.md`** (both live **only** here, copy these to your repository root).

## Non-duplication contract

* **Normative laws** (always-on): **`.cursor/rules/*.mdc`**
* **Release truth:** **`.forge/releases/release-vX.md`**
* **Execution truth:** **`.forge/plans/plan-vX/`**
* **Repeatable automation:** **`.forge/scripts/`** (run with **`.venv`** only)

**`.claude/`** adds Claude-native **settings**, **agents**, **skills**, **commands**, and optional **hooks**. It does **not** create alternate planning sources, alternate changelogs, or alternate “truth” trees.

## How Claude should load Forge context

1. **Session charter:** **`.claude/CLAUDE.md`**
2. **Agent map:** **`.claude/AGENTS.md`**
3. **This README** for directory semantics
4. **Slash commands:** **`.claude/commands/*.md`** — each command tells Claude to execute the **same procedure** documented in **`.cursor/commands/<same>.md`** (single operating system; two markdown entry points).

## Skills vs commands (Claude Code)

Claude Code loads **`.claude/skills/*/SKILL.md`** and **`.claude/commands/*.md`** as invocable **`/name`** capabilities. If a name collides, **skills take precedence** per Claude Code docs—**this repo uses distinct names** for stable commands (`plan`, `build`, …).

## Relationship to `.cursor/`

| Concern | Cursor | Claude Code |
|--------|--------|-------------|
| Always-on rules | `.cursor/rules/*.mdc` | Same files (read explicitly); optional pointers in `.claude/rules/` |
| Slash workflows | `.cursor/commands/` | `.claude/commands/` + pointer to `.cursor/commands/` |
| Procedures | `.cursor/skills/` | `.claude/skills/` (mirrored for native Claude loading) |
| Personas | `.cursor/subagents/` | `.claude/agents/` |

## Relationship to `.forge/`

* **`.forge/requirements/`** → intake
* **`.forge/tmp/`** → normalization output only
* **`.forge/releases/`** → synthesized release + **append-only** `changelog.json`
* **`.forge/plans/`** → generated plans from **release** only

## Approval and guardrails

**`/guard`** (see commands) wraps **guardrail-detection** and **hard stops**. Treat **deny** outcomes as blocking unless the user changes scope/inputs.

## Hooks

**`hooks/`** holds optional hook scripts and documentation. Project-wide hook **registration** belongs in **`settings.json`** / **`settings.local.json`** under the `"hooks"` key per [Claude Code hooks](https://code.claude.com/en/hooks). The `hooks/` folder is for **repo-owned scripts** you reference from those settings.

## Memory

**`memory/`** is for **non-canonical** human notes (onboarding tips, local service URLs). **Never** store release/plan truth here. Forge truth remains under **`.forge/`**.

## Python

Follow **`.claude/CLAUDE.md`** and **`.cursor/rules/python-runtime.mdc`**: **`.venv`** at repo root for Forge; **`projects/`** for application trees.
