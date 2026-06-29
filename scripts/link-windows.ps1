param(
    [ValidateSet("Codex", "Gemini", "Project")]
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
    "Codex" { $destRoot = Join-Path $env:USERPROFILE ".codex\skills" }
    "Gemini" { $destRoot = Join-Path $env:USERPROFILE ".gemini\antigravity-ide\skills" }
    "Project" { $destRoot = $ProjectSkillsRoot }
}

New-Item -ItemType Directory -Path $destRoot -Force | Out-Null

foreach ($skill in $skillNames) {
    $source = Join-Path $RepoRoot $skill
    $dest = Join-Path $destRoot $skill

    if (!(Test-Path -LiteralPath $source)) {
        throw "Missing source skill: $source"
    }

    if (Test-Path -LiteralPath $dest) {
        if (!$Force) {
            Write-Host "Skipping existing path: $dest"
            continue
        }

        $resolvedDest = (Resolve-Path -LiteralPath $dest).Path
        if ($resolvedDest -notlike "$destRoot*") {
            throw "Refusing to remove path outside destination root: $resolvedDest"
        }

        Remove-Item -LiteralPath $dest -Recurse -Force
    }

    New-Item -ItemType Junction -Path $dest -Target $source | Out-Null
    Write-Host "Linked $dest -> $source"
}
