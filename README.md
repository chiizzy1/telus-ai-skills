# TELUS Skills

Canonical private repository for TELUS evaluator skills.

## Source Of Truth

Edit TELUS skills here, then commit and push. Do not manually edit copied skill folders inside agent-specific directories.

Included skills:

- `telus-evaluator`
- `search-sbs-evaluator`
- `telus-bot-reply-validator`
- `text-response-evaluator`
- `web-images-satisfaction-evaluator`
- `close-variants-evaluator`
- `search-ads-relevance`
- `maps-search-evaluator`
- `related-results-evaluation-evaluator`

## Daily Update

Users with read access should update before TELUS task work:

```powershell
git -C "C:\Users\$env:USERNAME\Desktop\projects\train-ai\telus-ai-skills" pull --ff-only
```

Or run:

```powershell
.\scripts\update.ps1
```

## Windows Agent Links

Use junctions so `.agents`, Codex, Gemini/Antigravity, and project-local skill folders all point to this one repo.

```powershell
.\scripts\link-windows.ps1 -Target Agents
.\scripts\link-windows.ps1 -Target Codex
.\scripts\link-windows.ps1 -Target Gemini
```

Use `-Force` only when you intentionally want to replace existing copied skill folders with junctions. Existing folders are moved to a timestamped backup folder before the junction is created.

## Read-Only Setup

For friends or users who should only install and update the skills, send them:

```text
usage-instructions/USER_READ_ACCESS.md
```

They should clone this full repo, link their agent skill folders to it, and pull updates. They should not edit local skill files.

## Access Model

- Owner: write access.
- Friends/users: read access.
- Contributors should propose changes separately; only the owner updates this canonical repo.

Keep this repository private if it contains platform-specific or confidential guideline material.
