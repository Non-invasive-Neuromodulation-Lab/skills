# install.ps1
# Wires a cloned copy of this skills library into the local AI agents
# (Cline, VS Code Copilot Chat, Claude Code, Antigravity/Gemini) using
# directory junctions. The library stays where you cloned it; the agent
# folders become transparent pointers to it.
#
# Usage (from inside the cloned repo):
#   powershell -ExecutionPolicy Bypass -File .\install.ps1
#
# Optional switches:  -SkipCline -SkipVSCode -SkipClaudeCode -SkipAntigravity
#
# Safe by design:
#   - already-correct junctions are left untouched
#   - an existing junction pointing elsewhere is replaced (link only, never content)
#   - an existing REAL folder is moved aside to <path>.backup-<timestamp>
#
# Background and architecture: docs/SETUP.md

param(
    [switch]$SkipCline,
    [switch]$SkipVSCode,
    [switch]$SkipClaudeCode,
    [switch]$SkipAntigravity
)

$ErrorActionPreference = 'Stop'
$master = $PSScriptRoot

if (-not (Test-Path (Join-Path $master 'README.md'))) {
    throw "Run this script from inside the cloned skills repo (README.md not found next to it)."
}
if (-not (Test-Path (Join-Path $master 'docs\SETUP.md'))) {
    Write-Warning "docs/SETUP.md not found - continuing anyway."
}

function Install-Junction {
    param([string]$LinkPath, [string]$Label)

    $parent = Split-Path $LinkPath -Parent
    if (-not (Test-Path $parent)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }

    if (Test-Path $LinkPath) {
        $item = Get-Item $LinkPath -Force
        if ($item.LinkType -eq 'Junction' -and (($item.Target -join '') -eq $master)) {
            Write-Host "[OK]      $Label : already linked -> $master"
            return
        }
        if ($item.LinkType) {
            Write-Host "[REPLACE] $Label : replacing old link ($($item.Target -join ''))"
            cmd /c rmdir /q "$LinkPath"
        } else {
            $backup = "$LinkPath.backup-" + (Get-Date -Format 'yyyyMMdd-HHmmss')
            Write-Host "[BACKUP]  $Label : existing real folder found; moved to $backup"
            Move-Item $LinkPath $backup -Force
        }
    }

    New-Item -ItemType Junction -Path $LinkPath -Target $master | Out-Null
    Write-Host "[CREATED] $Label : $LinkPath -> $master"
}

$targets = @()
if (-not $SkipCline)       { $targets += @{ Path = Join-Path $env:USERPROFILE '.cline\skills';       Label = 'Cline (global)' } }
if (-not $SkipVSCode)      { $targets += @{ Path = Join-Path $env:USERPROFILE '.agents\skills';      Label = 'VS Code Copilot Chat (personal skills)' } }
if (-not $SkipClaudeCode)  { $targets += @{ Path = Join-Path $env:USERPROFILE '.claude\skills';      Label = 'Claude Code (personal skills)' } }
if (-not $SkipAntigravity) { $targets += @{ Path = Join-Path $env:USERPROFILE '.gemini\config\skills'; Label = 'Antigravity / Gemini (global)' } }

Write-Host "Master library: $master"
Write-Host ""

foreach ($t in $targets) {
    Install-Junction -LinkPath $t.Path -Label $t.Label
}

Write-Host ""
Write-Host "--- validation ---"
foreach ($t in $targets) {
    $n = (Get-ChildItem $t.Path -Directory -ErrorAction SilentlyContinue |
          Where-Object { Test-Path (Join-Path $_.FullName 'SKILL.md') }).Count
    Write-Host ("[CHECK]   {0} : {1} skills visible (expect 44+)" -f $t.Label, $n)
}

Write-Host ""
Write-Host "--- final step: restart/reload each tool so it rescans ---"
Write-Host "  Cline:         open a new chat; enable skills in the Skills menu (scale icon)"
Write-Host "  VS Code:       in Copilot Chat type / (or /skills) to see the list"
Write-Host "  Claude Code:   start a new session"
Write-Host "  Antigravity:   start a new conversation"
Write-Host ""
Write-Host ("To get future skill updates:  git -C `"$master`" pull")
