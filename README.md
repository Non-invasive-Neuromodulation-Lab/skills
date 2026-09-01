# Global AI Skills — Single Source of Truth

This folder is the **one master store** of Agent Skills (`SKILL.md` format, per the
open standard at https://agentskills.io). It is shared by multiple AI agents through
Windows directory junctions (transparent folder links):

| Consumer | Path (junction → this folder) |
|---|---|
| Cline — global, all workspaces | `C:\Users\Admin\.cline\skills` |
| VS Code — Copilot Chat, personal skills | `C:\Users\Admin\.agents\skills` |
| Claude Code — personal skills | `C:\Users\Admin\.claude\skills` |
| Google Antigravity (Gemini) — global, all workspaces | `C:\Users\Admin\.gemini\config\skills` |

## Rules

1. **Add / edit / delete skills only here.** Every consumer sees changes instantly —
   never edit skills through the junction paths.
2. **One folder per skill**: `<skill-name>/SKILL.md`. The `name` field in the YAML
   frontmatter **must exactly match the folder name** (required by Cline and VS Code).
3. **Project-specific skills stay inside the project** (`.cline/skills/` or
   `.agents/skills/` in the repo) — they override/complement global ones per project.
4. This folder is a **git repository** — commit and push regularly as backup.

## New machine / sharing this library

1. `git clone https://github.com/Non-invasive-Neuromodulation-Lab/skills.git`
2. `powershell -ExecutionPolicy Bypass -File .\install.ps1`
3. Restart/reload your AI tools — full details and an agent-ready install
   prompt: see **`HANDOFF.md`**.

See `docs/SETUP.md` for the full setup log, verification steps, and rollback plan.

Created: 2026-08-31
