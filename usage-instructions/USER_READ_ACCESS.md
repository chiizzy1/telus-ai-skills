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

## Access Model

You can:

- clone the private repo;
- pull updates from the owner;
- link your local agent skill folders to the clone;
- use the skills for TELUS task work.

You cannot:

- push changes to the official repo;
- edit the official skill source;
- share the private repo or its contents with people who do not have permission.

## Prerequisites

Before setup:

1. Accept the GitHub repository invite from the owner.
2. Install Git for Windows if it is not already installed.
3. Sign in to GitHub with the account the owner invited.
4. Use PowerShell on Windows.

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
Get-ChildItem "$env:USERPROFILE\.agents\skills" | Where-Object { $_.Name -like "telus-*" -or $_.Name -in @("search-sbs-evaluator","search-ads-relevance","close-variants-evaluator","text-response-evaluator","web-images-satisfaction-evaluator","maps-search-evaluator") }
```

For Codex:

```powershell
Get-ChildItem "$env:USERPROFILE\.codex\skills" | Where-Object { $_.Name -like "telus-*" -or $_.Name -in @("search-sbs-evaluator","search-ads-relevance","close-variants-evaluator","text-response-evaluator","web-images-satisfaction-evaluator","maps-search-evaluator") }
```

For Gemini / Antigravity:

```powershell
Get-ChildItem "$env:USERPROFILE\.gemini\antigravity-ide\skills" | Where-Object { $_.Name -like "telus-*" -or $_.Name -in @("search-sbs-evaluator","search-ads-relevance","close-variants-evaluator","text-response-evaluator","web-images-satisfaction-evaluator","maps-search-evaluator") }
```

You should see folders such as:

- `telus-evaluator`
- `search-sbs-evaluator`
- `telus-bot-reply-validator`
- `text-response-evaluator`
- `web-images-satisfaction-evaluator`
- `close-variants-evaluator`
- `search-ads-relevance`
- `maps-search-evaluator`

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

If you are unsure which target to use:

- use `Agents` for `.agents/skills`;
- use `Codex` for `.codex/skills`;
- use `Gemini` for Gemini / Antigravity;
- use `Project` only for a project-specific skills folder.
