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

## Daily Update

Users with read access should update before TELUS task work:

```powershell
git -C "C:\Users\DELL\skills-source\telus-skills" pull --ff-only
```

Or run:

```powershell
.\scripts\update.ps1
```

## Windows Agent Links

Use junctions so Codex, Gemini/Antigravity, and project-local skill folders all point to this one repo.

```powershell
.\scripts\link-windows.ps1 -Target Codex
.\scripts\link-windows.ps1 -Target Gemini
```

Use `-Force` only when you intentionally want to replace existing copied skill folders with junctions. Existing folders are moved to a timestamped backup folder before the junction is created.

## Access Model

- Owner: write access.
- Friends/users: read access.
- Contributors should propose changes separately; only the owner updates this canonical repo.

Keep this repository private if it contains platform-specific or confidential guideline material.
