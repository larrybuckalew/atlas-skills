# Atlas Skills Sync Script
# Run this after installing new skills to auto-sync to GitHub

param(
    [string]$Message = ""
)

$SKILLS_DIR = "C:\Users\larry\AppData\Roaming\npm\node_modules\openclaw\skills"
$REPO_DIR = "C:\Users\larry\atlas-skills"
$GITHUB_REPO = "larrybuckalew/atlas-skills"

# Color output
function Write-Success { param($m) Write-Host "[✓] $m" -ForegroundColor Green }
function Write-Info { param($m) Write-Host "[*] $m" -ForegroundColor Cyan }
function Write-Error { param($m) Write-Host "[✗] $m" -ForegroundColor Red }

Write-Info "Atlas Skills Sync starting..."
Write-Info "Skills directory: $SKILLS_DIR"
Write-Info "Repo directory: $REPO_DIR"

# Check git status
Set-Location $REPO_DIR
$status = git status --porcelain

if ($status) {
    Write-Info "Changes detected. Committing..."
    
    # Stage all changes
    git add .
    
    # Create commit message
    if (-not $Message) {
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"
        $changed = ($status | ForEach-Object { $_.Split(" ")[1] }) -join ", "
        $Message = "Sync: $changed | $timestamp"
    }
    
    # Commit and push
    git commit -m $Message
    git push origin main
    
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Synced to GitHub: $Message"
    } else {
        Write-Error "Push failed"
    }
} else {
    Write-Info "No changes to sync"
}

Write-Success "Done!"
