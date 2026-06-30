param(
    [string]$Message = "",
    [switch]$SkipImport,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -LiteralPath $RepoRoot

function Invoke-Step {
    param(
        [string]$Label,
        [scriptblock]$Command
    )

    Write-Host ""
    Write-Host "==> $Label"
    if ($DryRun) {
        Write-Host "[dry-run] skipped"
        return
    }
    & $Command
}

function Get-GitPorcelain {
    return @(git status --porcelain)
}

Write-Host "Repository: $RepoRoot"
git rev-parse --is-inside-work-tree | Out-Null

Write-Host ""
Write-Host "Current status:"
git status --short --branch

if (-not $SkipImport) {
    Invoke-Step "Import Super Productivity data" {
        python -B scripts/import_superproductivity.py
    }
} else {
    Write-Host ""
    Write-Host "==> Import Super Productivity data"
    Write-Host "Skipped by -SkipImport"
}

$Changes = Get-GitPorcelain
if ($Changes.Count -eq 0) {
    Write-Host ""
    Write-Host "No changes to commit."
    exit 0
}

if ([string]::IsNullOrWhiteSpace($Message)) {
    $Message = "Update progress $(Get-Date -Format 'yyyy-MM-dd HHmm')"
}

Write-Host ""
Write-Host "Changes to publish:"
git status --short

if ($DryRun) {
    Write-Host ""
    Write-Host "[dry-run] would run:"
    Write-Host "git add -A"
    Write-Host "git commit -m `"$Message`""
    Write-Host "git push"
    exit 0
}

Invoke-Step "Stage changes" {
    git add -A
}

$StagedChanges = @(git diff --cached --name-only)
if ($StagedChanges.Count -eq 0) {
    Write-Host ""
    Write-Host "No staged changes to commit."
    exit 0
}

Invoke-Step "Commit changes" {
    git commit -m $Message
}

Invoke-Step "Push to GitHub" {
    git push
}

Write-Host ""
Write-Host "Done."
