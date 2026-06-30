param(
    [ValidateSet("Agents", "Codex", "Gemini", "Project")]
    [string]$Target,

    [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path,

    [string]$ProjectSkillsRoot = "C:\Users\DELL\Downloads\train-ai\train-ai\TELUS-TASKS\skills",

    [switch]$Force
)

$skillNames = @(
    "telus-evaluator",
    "search-sbs-evaluator",
    "telus-bot-reply-validator",
    "text-response-evaluator",
    "web-images-satisfaction-evaluator",
    "close-variants-evaluator",
    "search-ads-relevance"
)

switch ($Target) {
    "Agents" { $destRoot = Join-Path $env:USERPROFILE ".agents\skills" }
    "Codex" { $destRoot = Join-Path $env:USERPROFILE ".codex\skills" }
    "Gemini" { $destRoot = Join-Path $env:USERPROFILE ".gemini\antigravity-ide\skills" }
    "Project" { $destRoot = $ProjectSkillsRoot }
}

New-Item -ItemType Directory -Path $destRoot -Force | Out-Null
$backupRoot = Join-Path $destRoot ("_backup_before_junction_" + (Get-Date -Format "yyyyMMdd-HHmmss"))

foreach ($skill in $skillNames) {
    $source = Join-Path $RepoRoot $skill
    $dest = Join-Path $destRoot $skill

    if (!(Test-Path -LiteralPath $source)) {
        throw "Missing source skill: $source"
    }

    if (Test-Path -LiteralPath $dest) {
        $item = Get-Item -LiteralPath $dest
        $resolvedDest = (Resolve-Path -LiteralPath $dest).Path

        if ($item.LinkType -eq "Junction" -and $item.Target -contains $source) {
            Write-Host "Already linked $dest -> $source"
            continue
        }

        if (!$Force) {
            Write-Host "Skipping existing path: $dest"
            continue
        }

        if ($resolvedDest -notlike "$destRoot*") {
            throw "Refusing to move path outside destination root: $resolvedDest"
        }

        New-Item -ItemType Directory -Path $backupRoot -Force | Out-Null
        $backupDest = Join-Path $backupRoot $skill
        Move-Item -LiteralPath $dest -Destination $backupDest
        Write-Host "Backed up $dest -> $backupDest"
    }

    New-Item -ItemType Junction -Path $dest -Target $source | Out-Null
    Write-Host "Linked $dest -> $source"
}
