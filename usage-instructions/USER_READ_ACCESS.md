# Read-Only User Guide

Use this guide if you have read access to the private TELUS skills repo but should not edit or push changes.

## What This Installs

This repo is a skill source folder. You need the full folder structure locally, not just one `SKILL.md` file.

Each skill can include:

- `SKILL.md` - the main trigger and workflow instructions.
- `references/rubric.md` - detailed task rules loaded when needed.
- `agents/openai.yaml` - display metadata for agent skill UIs.
- shared scripts for linking and updating skills.

Your agent reads the skills from your local clone. The local clone stays current by pulling owner-approved updates from GitHub.

The skills are the method. The guidelines they apply are separate, and arrive as a `TELUS-TASKS` zip from the owner. You need both, sitting side by side. See Unpack The Task Material below.

## Access Model

You can:

- clone the private repo;
- pull updates from the owner;
- link your local agent skill folders to the clone;
- use the skills for TELUS task work.

You cannot:

- push changes to the official repo;
- edit the official skill source;
- share the private repo or its contents with people who do not have permission;
- share the `TELUS-TASKS` guideline material, which is TELUS's own and carries the same restriction as this repo.

## Prerequisites

Before setup:

1. Accept the GitHub repository invite from the owner.
2. Install Git for Windows if it is not already installed.
3. Install Python 3.9 or newer from python.org. Several skills call a URL checker that ships with this repo. On Windows the command is usually `python`, not `python3`.
4. Sign in to GitHub with the account the owner invited.
5. Use PowerShell on Windows.

Private repo:

```text
https://github.com/chiizzy1/telus-ai-skills
```

## First-Time Setup

1. Create a folder for skill source repos:

```powershell
New-Item -ItemType Directory -Path "C:\Users\$env:USERNAME\Desktop\projects\train-ai" -Force
```

2. Clone the repo:

```powershell
git clone https://github.com/chiizzy1/telus-ai-skills.git "C:\Users\$env:USERNAME\Desktop\projects\train-ai\telus-ai-skills"
```

3. Open the repo folder:

```powershell
cd "C:\Users\$env:USERNAME\Desktop\projects\train-ai\telus-ai-skills"
```

## Unpack The Task Material

The skills are only half of what you need. The official TELUS guidelines, the extracted page renders, and the blank task templates live in a separate folder called `TELUS-TASKS`, which the owner sends you as a zip. It is not in this repo, because it is large binary material that changes rarely.

**It has to unzip as a sibling of this repo, not inside it:**

```text
C:\Users\<you>\Desktop\projects\train-ai\
    telus-ai-skills\        <- the clone
    TELUS-TASKS\            <- the unzipped folder
```

```powershell
Expand-Archive -Path "$env:USERPROFILE\Downloads\TELUS-TASKS-<date>.zip" -DestinationPath "C:\Users\$env:USERNAME\Desktop\projects\train-ai"
```

This matters more than it looks. Every skill resolves its guideline as `TELUS-TASKS/...` relative to the workspace root. Put the folder anywhere else and the skills still load, still run, and still produce ratings, but every source-of-truth path silently misses and the agent falls back to its own reference files. Nothing announces the problem.

Check it landed correctly:

```powershell
Test-Path "C:\Users\$env:USERNAME\Desktop\projects\train-ai\TELUS-TASKS\task-templates"
```

Expected: `True`.

What is inside:

- One folder per TELUS task type, holding that task's official guideline PDF and any extracted text or page renders.
- `task-templates\` - a blank template per task type. Copy the one you need into `TELUS-TASKS\task.md`, fill it in, and give that to the agent.
- `task.md` - the live working file. This is the only file you edit.

You will not have a `url_content` folder at first. The URL checker creates it the first time it runs and writes its evidence there. That folder is yours, is regenerated as you work, and is never shared back.

## Install The URL Checker Dependencies

Several skills call `tools\check_urls.py`. It runs with no setup at all, but without its packages it falls back to the standard library, prints `DEGRADED MODE`, and extracts less text, which pushes more results into manual review.

For full quality, run from the repo folder:

```powershell
python -m pip install --user -r tools\requirements.txt
python -m playwright install chromium
```

The chromium download is about 90 MB. It is what lets the checker read JavaScript-heavy or bot-protected pages.

Confirm it worked:

```powershell
python tools\check_urls.py --check-deps
```

Expected: `All core dependencies present.`

## Link Your Agent Skills

Run the link command for the agent app you use.

### Shared `.agents` Skills

Use this when your workspace uses `.agents/skills`:

```powershell
.\scripts\link-windows.ps1 -Target Agents
```

### Codex

Use this when you want Codex to read the skills from this repo:

```powershell
.\scripts\link-windows.ps1 -Target Codex
```

### Gemini / Antigravity

Use this when you want Gemini or Antigravity to read the skills from this repo:

```powershell
.\scripts\link-windows.ps1 -Target Gemini
```

### Project-Local Skills

Use this only if a specific project has its own skill folder:

```powershell
.\scripts\link-windows.ps1 -Target Project -ProjectSkillsRoot "C:\path\to\project\skills"
```

## When To Use `-Force`

Use `-Force` only if a destination skill folder already exists and you intentionally want to replace that local copy with a junction to this repo.

Example:

```powershell
.\scripts\link-windows.ps1 -Target Agents -Force
.\scripts\link-windows.ps1 -Target Codex -Force
.\scripts\link-windows.ps1 -Target Gemini -Force
```

The script backs up existing folders into a timestamped `_backup_before_junction_...` folder before creating links.

## Verify Installation

After linking, check that the skill folders exist at the target location.

For `.agents`:

```powershell
Get-ChildItem "$env:USERPROFILE\.agents\skills" | Where-Object { $_.Target -like "*telus-ai-skills*" } | Select-Object Name, LinkType
```

For Codex:

```powershell
Get-ChildItem "$env:USERPROFILE\.codex\skills" | Where-Object { $_.Target -like "*telus-ai-skills*" } | Select-Object Name, LinkType
```

For Gemini / Antigravity:

```powershell
Get-ChildItem "$env:USERPROFILE\.gemini\antigravity-ide\skills" | Where-Object { $_.Target -like "*telus-ai-skills*" } | Select-Object Name, LinkType
```

These commands match on the link target rather than on a list of names, so they keep working as skills are added or renamed. Every row should show `LinkType` of `Junction`. A plain directory instead of a junction means the link step did not work; run the link command again with `-Force`.

You should see one row per skill folder in your clone. New skills are added over time, so rather than checking against a fixed list, compare the two counts:

```powershell
$linked = (Get-ChildItem "$env:USERPROFILE\.agents\skills" | Where-Object { $_.Target -like "*telus-ai-skills*" }).Count
$inRepo = (Get-ChildItem "C:\Users\$env:USERNAME\Desktop\projects\train-ai\telus-ai-skills" -Directory | Where-Object { Test-Path "$($_.FullName)\SKILL.md" }).Count
"linked: $linked  in repo: $inRepo"
```

The two numbers should match. If `linked` is lower, run the link command again. If you think `inRepo` is lower than it should be, your clone is behind: run the daily update below and check again.

Restart the agent after linking so it can discover the skills.

## Daily Update

Before TELUS task work, pull the latest owner-approved version:

```powershell
git -C "C:\Users\$env:USERNAME\Desktop\projects\train-ai\telus-ai-skills" pull --ff-only
```

Or run this from the repo folder:

```powershell
.\scripts\update.ps1
```

Restart the agent if the update changed skill files.

## How To Use The Skills

Ask the agent to use the TELUS evaluator or a specific TELUS skill.

Examples:

```text
Use the TELUS evaluator on this task.
```

```text
Use the TELUS Search SBS evaluator for this result.
```

```text
Use the TELUS Close Variants evaluator for this query pair.
```

```text
Use the TELUS Maps Search evaluator for this Search 2.0 task.
```

```text
Use the TELUS Related Results evaluator for this query and result.
```

Expected routing flow:

```text
telus-evaluator
  -> identifies the TELUS task type
  -> routes to the right task-specific skill
  -> loads that skill's rubric
  -> applies the task rules
```

## Do Not Edit Local Skill Files

Do not edit files inside your local clone unless the owner specifically asks you to test a change.

If you edit local files, future updates may fail or your changes may be overwritten.

If you accidentally edit files, discard the local changes before updating:

```powershell
git -C "C:\Users\$env:USERNAME\Desktop\projects\train-ai\telus-ai-skills" status
git -C "C:\Users\$env:USERNAME\Desktop\projects\train-ai\telus-ai-skills" restore .
git -C "C:\Users\$env:USERNAME\Desktop\projects\train-ai\telus-ai-skills" pull --ff-only
```

## Troubleshooting

If `git clone` or `git pull` asks you to sign in, sign in with the GitHub account the owner invited.

If you see `Repository not found`, check:

- you accepted the repo invite;
- you are signed into the correct GitHub account;
- the owner gave you read access.

If the agent still uses old skill behavior:

- run `git pull --ff-only`;
- confirm the agent skill folder is linked to this repo;
- restart the agent.

If the link script says a path already exists:

- run the command again with `-Force` only if you are okay with backing up the existing folder and replacing it with a junction.

If the agent rates a task but never quotes the official guideline, or says a guideline file could not be found:

- check `TELUS-TASKS` sits beside `telus-ai-skills`, not inside it;
- run the `Test-Path` check in Unpack The Task Material.

If the checker prints `DEGRADED MODE`:

- it still works, with coarser text extraction;
- run the two install commands in Install The URL Checker Dependencies for full quality.

If you are unsure which target to use:

- use `Agents` for `.agents/skills`;
- use `Codex` for `.codex/skills`;
- use `Gemini` for Gemini / Antigravity;
- use `Project` only for a project-specific skills folder.
