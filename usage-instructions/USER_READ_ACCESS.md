# Read-Only User Guide

Use this guide if you have read access to the private TELUS skills repo.

## What You Can Do

You can:

- Clone the private TELUS skills repo.
- Pull updates from the owner.
- Link your agent skill folders to your local clone.
- Use the skills for TELUS task work.

You cannot:

- Push changes to the repo.
- Update the official skill source.
- Share the private repo or its contents with people who do not have permission.

## First-Time Setup

Accept the GitHub repository invite from the owner.

Clone the repo:

```powershell
New-Item -ItemType Directory -Path "C:\Users\$env:USERNAME\skills-source" -Force
git clone https://github.com/chiizzy1/telus-ai-skills.git "C:\Users\$env:USERNAME\skills-source\telus-ai-skills"
```

Open the repo:

```powershell
cd "C:\Users\$env:USERNAME\skills-source\telus-ai-skills"
```

## Link Your Agent Skills

Run these from the cloned repo folder.

Link Codex:

```powershell
.\scripts\link-windows.ps1 -Target Codex
```

Link Gemini/Antigravity:

```powershell
.\scripts\link-windows.ps1 -Target Gemini
```

Use `-Force` only if you are replacing an existing copied skill folder:

```powershell
.\scripts\link-windows.ps1 -Target Codex -Force
.\scripts\link-windows.ps1 -Target Gemini -Force
```

Restart the agent after linking so it can discover the skills.

## Daily Update

Before TELUS work, pull the latest owner-approved version:

```powershell
git -C "C:\Users\$env:USERNAME\skills-source\telus-ai-skills" pull --ff-only
```

Or run:

```powershell
cd "C:\Users\$env:USERNAME\skills-source\telus-ai-skills"
.\scripts\update.ps1
```

Restart the agent if the update changed skill files.

## Using The Skills

Ask the agent to use the TELUS evaluator or work from a TELUS task file.

The expected routing flow is:

```text
telus-evaluator
  -> identifies the TELUS task type
  -> routes to the right task-specific evaluator
  -> applies that evaluator's rubric
```

Examples:

```text
Evaluate this TELUS Search SBS task.
```

```text
Use the TELUS evaluator on TELUS-TASKS/task.md.
```

## Local Changes

Do not edit the skill files unless the owner asks you to test something.

If you accidentally edit files, discard your local changes before updating:

```powershell
git -C "C:\Users\$env:USERNAME\skills-source\telus-ai-skills" status
git -C "C:\Users\$env:USERNAME\skills-source\telus-ai-skills" restore .
git -C "C:\Users\$env:USERNAME\skills-source\telus-ai-skills" pull --ff-only
```

## Troubleshooting

If `git pull` asks you to sign in, sign in with the GitHub account the owner added to the private repo.

If you see `Repository not found`, confirm:

- You accepted the repo invite.
- You are signed into the correct GitHub account.
- The owner added you with read access.

If the agent still uses old skill behavior:

- Run `git pull --ff-only`.
- Confirm the agent skill folder is linked to the repo.
- Restart the agent.
