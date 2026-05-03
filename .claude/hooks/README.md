# `.claude/hooks/` — optional automation hooks

Forge’s **deterministic** automation belongs in **`/.forge/scripts/`** and is invoked explicitly by commands (`/plan`, `/build`, `/test`, …).

This folder is for **Claude Code lifecycle hooks** (for example **PreToolUse** / **PostToolUse**) that you wire through **`.claude/settings.json`** or **`.claude/settings.local.json`** using the `"hooks"` object.

## Active project hooks (committed)

**`PreToolUse`** — before **Bash** or **PowerShell** tool calls:

* **`pretooluse_forge_launch.sh`** (default shell) runs **`.forge/scripts/claude_pretooluse_forge.py`** with repo **`.venv`** on Unix or Windows Python paths.
* **`pretooluse_forge_launch.ps1`** is used for **PowerShell** tool invocations on Windows (`shell: powershell` in settings).

Policy: bare **`pip install`**, **`npm install`**, **`npm ci`**, **`pnpm install`**, **`yarn install`**, etc. are **denied** when **`cwd`** is **not** under **`projects/`**, unless the command references repo **`.venv`** (Forge tooling). See **`claude_pretooluse_forge.py`** for the exact patterns.

## Design guidance for Forge repos

* Prefer **narrow** hooks (format on save, lint staged files) over “policy engines” that duplicate **`.cursor/rules/`**.
* Hooks should **fail closed** only when they can **prove** a violation with fast checks; otherwise they become friction without evidence.
* Never use hooks to **rewrite** **`/.forge/releases/changelog.json`** history or bypass the append-only law.

## Registration

See Anthropic documentation: [Hooks](https://code.claude.com/en/hooks) and [Hooks reference](https://code.claude.com/docs/en/hooks.md).

Example pattern (illustrative only — adjust to your platform and policies):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{ "type": "command", "command": "echo 'audit bash'" }]
      }
    ]
  }
}
```

Place reusable hook scripts in this directory and reference them with stable repo-relative paths from settings.
