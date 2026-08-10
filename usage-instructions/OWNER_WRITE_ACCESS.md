# Owner Usage Guide

Use this guide if you own the private TELUS skills repo and have write access.

## Golden Rule

The GitHub repo is the source of truth. Make TELUS skill changes in the canonical repo, then commit and push them.

Canonical repo folder on this machine:

```powershell
C:\Users\$env:USERNAME\Desktop\projects\train-ai\telus-ai-skills
```

Private GitHub repo:

```text
https://github.com/chiizzy1/telus-ai-skills
```

## Daily Workflow

Before editing, pull the latest version:

```powershell
git -C "C:\Users\$env:USERNAME\Desktop\projects\train-ai\telus-ai-skills" pull --ff-only
```

Edit the skill files in the canonical repo folder.

Check what changed:

```powershell
git -C "C:\Users\$env:USERNAME\Desktop\projects\train-ai\telus-ai-skills" status
git -C "C:\Users\$env:USERNAME\Desktop\projects\train-ai\telus-ai-skills" diff
```

Commit and push:

```powershell
git -C "C:\Users\$env:USERNAME\Desktop\projects\train-ai\telus-ai-skills" add .
git -C "C:\Users\$env:USERNAME\Desktop\projects\train-ai\telus-ai-skills" commit -m "Improve TELUS skill guidance"
git -C "C:\Users\$env:USERNAME\Desktop\projects\train-ai\telus-ai-skills" push
```

## Adding Users

Add friends as read-only collaborators in GitHub:

1. Open the private repo on GitHub.
2. Go to `Settings`.
3. Open `Collaborators and teams`.
4. Add their GitHub usernames.
5. Give them read access only.

Only give write access to someone you trust to directly modify the canonical skill source.

## Agent Setup

Use junction links so each agent reads this canonical repo instead of stale copied folders.

The linking script installs every canonical TELUS skill, including `maps-search-evaluator`.

Link Codex:

```powershell
.\scripts\link-windows.ps1 -Target Codex
```

Link Gemini/Antigravity:

```powershell
.\scripts\link-windows.ps1 -Target Gemini
```

Link a local project TELUS skills folder:

```powershell
.\scripts\link-windows.ps1 -Target Project
```

Use `-Force` only when you intentionally want to replace an existing copied skill folder with a junction. The script backs up existing folders before linking.

## Updating Skills Through Codex

You can ask Codex:

```text
Update the TELUS Search SBS skill with this new rule...
```

Codex should:

1. Edit files in the canonical repo.
2. Show or summarize the diff.
3. Commit the change.
4. Push to GitHub.

You can also edit files yourself and ask:

```text
Commit and push my TELUS skill changes.
```

## What Not To Do

Do not keep manually copying skill folders between agents.

Do not treat these paths as separate sources of truth:

```text
C:\Users\$env:USERNAME\.codex\skills
C:\Users\$env:USERNAME\.gemini\antigravity-ide\skills
C:\Users\$env:USERNAME\Desktop\projects\train-ai\TELUS-TASKS\skills
```

After linking, those folders should point back to this canonical repo.

## Token Safety

Do not commit tokens, API keys, `.env`, or `local.env` files.

If a token is ever exposed in a config file, rotate it in GitHub and replace it with a new token.
