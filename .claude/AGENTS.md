# ForgeOS agent map (cross-tool)

This repository defines **one** engineering OS with **two** first-class interfaces:

* **Cursor:** `.cursor/subagents/*.md`
* **Claude Code:** `.claude/agents/*.md`

Subagents **must not** contradict **`.cursor/rules/*.mdc`**, **`.forge/releases/`**, or **`.forge/plans/`**. They **specialize** behavior under the same laws.

## Role matrix

| Responsibility | Cursor contract | Claude Code contract |
|----------------|-----------------|----------------------|
| Normalize, synthesize release, generate plan | `.cursor/subagents/planner-agent.md` | `.claude/agents/planner-agent.md` |
| Implement one explicit plan task with proof | `.cursor/subagents/builder-agent.md` | `.claude/agents/builder-agent.md` |
| Plan/release quality, dependency and rollback safety | `.cursor/subagents/reviewer-agent.md` | `.claude/agents/reviewer-agent.md` |
| Evidence-based Go / No-Go for explicit targets | `.cursor/subagents/validation-agent.md` | `.claude/agents/validation-agent.md` |
| Cumulative release validation `v0 → vX` | `.cursor/subagents/release-agent.md` | `.claude/agents/release-agent.md` |
| Architecture boundaries, coupling, drift vs release truth | *(architecture-review skill + review command)* | `.claude/agents/architecture-agent.md` |
| Trust boundaries, security contracts, unsafe exposure | *(SECURITY_CONTRACTS + validation)* | `.claude/agents/security-agent.md` |
| Hard-stop law violations before damage | `.cursor/subagents/guardrail-agent.md` | `.claude/agents/guardrail-agent.md` |
| Root-cause debugging after repeated fix failures | *(failure-analysis + engineering loop)* | `.claude/agents/debugging-agent.md` |

## Invocation expectations

* **Slash commands** (`.claude/commands/` or `.cursor/commands/`) select **workflow** and mandatory sequencing.
* **Agents** supply **persona, focus, and reporting shape** for delegated work.
* **Skills** (`.claude/skills/` / `.cursor/skills/`) supply **repeatable procedures**.

## Source of truth order

1. **`.cursor/rules/*.mdc`** — normative laws (always apply in this repo).
2. **`.forge/releases/release-vX.md`** — canonical release line truth.
3. **`.forge/plans/plan-vX/`** — execution truth for implementation.
4. **`.forge/scripts/`** — deterministic automation contracts.

When **Claude-specific** settings conflict with the above (for example permissive tool defaults), **the Forge sources win**. Adjust **`.claude/settings.local.json`**, not the release/plan pipeline, to resolve personal friction.
