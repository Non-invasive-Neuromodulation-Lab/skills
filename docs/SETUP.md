# Setup: One Folder + Pointers (Global Skills for Cline, VS Code Copilot Chat, Claude Code, Antigravity/Gemini)

Date: 2026-08-31

## Why

Skills were previously scattered across per-tool stores, and an older setup that
junction-pointed VS Code and Claude Code at a skills repo
(`D:\GitHub\.github-private-org\skills`) was **broken** because that repo had been
deleted — 35 dangling junctions in `~\.agents\skills` and `~\.claude\skills`.

## Architecture

```
C:\Users\Admin\skills\            <- ONE master folder (git repo, source of truth)
   ├─ <skill-name>\SKILL.md       <- 44 skills
   └─ docs\SETUP.md               <- this file

C:\Users\Admin\.cline\skills    --junction--> C:\Users\Admin\skills   (Cline, global)
C:\Users\Admin\.agents\skills   --junction--> C:\Users\Admin\skills   (VS Code Copilot Chat, personal)
C:\Users\Admin\.claude\skills   --junction--> C:\Users\Admin\skills   (Claude Code, personal)
C:\Users\Admin\.gemini\config\skills --junction--> C:\Users\Admin\skills   (Antigravity/Gemini, global)
```

Junctions are transparent: every tool reads/writes normally, and all three see
changes made in the master folder instantly.

## What was done

1. **Backup**: full copy of the original Cline store was saved at
   `C:\Users\Admin\.cline\skills.backup` (42 items). Removed 2026-08-31 after
   all four pointers were verified, per user request — the master folder is now
   the only copy (commit it to git to have a real backup).
2. **Migration**: moved all 42 skill folders from `C:\Users\Admin\.cline\skills`
   into `C:\Users\Admin\skills` (same volume — instant renames, nothing copied).
3. **Pointer 1 (Cline)**: replaced the emptied real folder with a junction.
4. **Pointer 2 (VS Code)**: replaced the dead 35-junction farm at
   `C:\Users\Admin\.agents\skills` with a single junction to the master.
5. **Pointer 3 (Claude Code)**: replaced the dead 35-junction farm at
   `C:\Users\Admin\.claude\skills` with a single junction to the master.
6. **Versioning**: `git init` in the master folder.
7. **Pointer 4 (Antigravity/Gemini)**: created a junction at Antigravity's
   documented global skills location `~\.gemini\config\skills` → master
   (per https://antigravity.google/docs — Skills: global scope). Also cleaned
   `~\.gemini\config\skills.json`, which held 4 dead entries pointing at the
   deleted `D:\GitHub\.github-private-org` repo (original saved as
   `skills.json.bak`).

## Notes

- **Restored skills (2026-08-31)**: `claude-handoff` and `git-guardrails-claude-code`
  were recovered from their upstream source
  [mattpocock/skills](https://github.com/mattpocock/skills) — the public origin of
  the deleted `.github-private-org` store. Note: the org repo
  `Non-invasive-Neuromodulation-Lab/.github-private` still exists but is only a
  stub (README + empty `agents/` folder, no skills).
- **VS Code skill discovery**: skills are read from `.agents/skills` (user level =
  this junction) plus `.github/skills` (per project). In Copilot Chat, type `/` to
  see skills as slash commands; if they ever stop appearing, verify the
  `chat.useAgentSkills` setting is enabled.
- **Cline**: per-skill on/off toggles may have reset after the folder swap —
  re-enable as needed in Cline's Skills menu (scale icon next to the model selector).
- **Antigravity/Gemini**: global skills load from `~\.gemini\config\skills`
  (this junction); workspace-level skills come from `<workspace>\.agents\skills\`.
  Per-skill toggles live in `~\.gemini\config\skills.json`. Antigravity's
  built-in skills (~\.gemini\antigravity\builtin\skills) are separate and untouched.

## Maintenance

- New/edit/delete skills: **only in `C:\Users\Admin\skills`**.
- One folder per skill; frontmatter `name` must equal the folder name.
- Commit here regularly (backup + history).
- Rollback (if ever needed): delete any/all four junctions — deleting a junction
  removes only the pointer, never the master content. To return to the old
  layout, move the skill folders out of the master folder into `.cline\skills`
  as a real directory. No backup copy exists anymore — the master folder is the
  single source of truth, so keep it committed to git.
