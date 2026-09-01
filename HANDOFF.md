# Handoff: Global AI Skills Library

This repo is a shared library of Agent Skills (`SKILL.md` format,
https://agentskills.io). Each person keeps their own clone and points their
AI tools at it with directory junctions — nobody copies files by hand, and
`git pull` updates everyone's agents at once.

## What the receiving person needs

1. **Nothing special — the repo is public.** Clone it freely. To *contribute*
   (push), ask the owner to add your GitHub username as a collaborator, or
   open a pull request.
2. **Windows 10/11** with built-in PowerShell (junctions are Windows links;
   macOS/Linux equivalent commands are at the bottom).
3. At least one of: **Cline**, **VS Code + GitHub Copilot Chat**, optionally
   **Claude Code** / **Antigravity (Gemini)**.

## Manual install (2 commands)

```powershell
git clone https://github.com/Non-invasive-Neuromodulation-Lab/skills.git
cd skills
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

Then restart/reload each AI tool (Cline: new chat + Skills menu;
VS Code: type `/` or `/skills` in Copilot Chat; Claude Code / Antigravity:
new session). `install.ps1` prints the per-tool checklist and validation counts.

The clone location is your choice — `install.ps1` auto-detects where it runs
from. If any of the target folders already exist on the machine, the script
backs them up (real folders) or replaces stale links; it never deletes content.

## Agent-assisted install (paste this into a fresh Cline or Copilot Chat)

```text
Set up my shared global AI skills library.
Repo: https://github.com/Non-invasive-Neuromodulation-Lab/skills (I have access).

Steps:
1. If %USERPROFILE%\skills does not exist, clone the repo there:
   git clone https://github.com/Non-invasive-Neuromodulation-Lab/skills.git "%USERPROFILE%\skills"
   If it already exists, run: git -C "%USERPROFILE%\skills" pull
2. Run the installer:
   powershell -ExecutionPolicy Bypass -File "%USERPROFILE%\skills\install.ps1"
3. Show me the installer's validation output and list exactly which AI tools
   need a restart/reload.

Constraints:
- Do NOT copy or move skill files into any agent folder (e.g. %USERPROFILE%\.cline\skills).
  The installer uses directory junctions; the cloned repo stays the single real copy.
- If a target folder already contains a real skills folder, let the installer back it up;
  do not delete anything.
- Do not commit or push anything.
```

## Keeping it up to date

```powershell
git -C "%USERPROFILE%\skills" pull
```

All agents see new/changed skills instantly (junctions are live).

## Contributing back

Edit skills only inside your clone, then:

```powershell
git -C "%USERPROFILE%\skills" add -A
git -C "%USERPROFILE%\skills" commit -m "Add/fix <skill-name>"
git -C "%USERPROFILE%\skills" push
```

Rules: one folder per skill; the SKILL.md frontmatter `name` must equal the
folder name; keep `description` specific so agents trigger the skill reliably.

## No GitHub access? Offline alternative

Send a zip (excludes `.git`, so the recipient loses history):

```powershell
Compress-Archive -Path C:\Users\<you>\skills\* -DestinationPath C:\Users\<you>\Desktop\skills-library.zip
```

Recipient: extract anywhere, run `install.ps1` from that folder, then `git init`
inside it if they want versioning.

## macOS / Linux (instead of install.ps1)

```bash
git clone https://github.com/Non-invasive-Neuromodulation-Lab/skills.git ~/.skills
ln -s ~/.skills ~/.cline/skills        # Cline
ln -s ~/.skills ~/.agents/skills       # VS Code Copilot Chat
ln -s ~/.skills ~/.claude/skills       # Claude Code
mkdir -p ~/.gemini/config && ln -s ~/.skills ~/.gemini/config/skills   # Antigravity/Gemini
```

(Adjust: skip tools you don't use; back up any existing folders first.)
