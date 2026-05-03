# `.claude/skills/` — Claude-native procedures

These directories mirror **`.cursor/skills/`** so Claude Code can load **`/skill-name`** workflows without depending on Cursor’s skill discovery.

**Canonical law text** remains in **`.cursor/rules/*.mdc`**. Skills reference those paths explicitly where relevant.

When updating a procedure, change **`.cursor/skills/<name>/SKILL.md`** first, then copy/sync to **`.claude/skills/<name>/SKILL.md`** (or edit both in one commit) so both interfaces stay aligned.
