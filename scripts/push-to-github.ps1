#!/usr/bin/env pwsh
# Push to GitHub Script for Anita Agent CI/CD
# Automatiserer git push og viser GitHub Actions status

param(
    [Parameter()]
    [string]$CommitMessage = "ci: Implement complete CI/CD pipeline",
    
    [Parameter()]
    [string]$Branch = "main",
    
    [Parameter()]
    [string]$RemoteName = "origin",
    
    [Parameter()]
    [switch]$FirstPush,
    
    [Parameter()]
    [switch]$OpenBrowser
)

$ErrorActionPreference = "Stop"

# Farger
$Cyan = "Cyan"
$Green = "Green"
$Yellow = "Yellow"
$Red = "Red"
$Magenta = "Magenta"

function Write-Banner {
    Write-Host @"
╔═══════════════════════════════════════════════════════════════╗
║           PUSH TO GITHUB - CI/CD ACTIVATION                  ║
║                                                              ║
║  This script will:                                           ║
║  1. Check/Initialize git repository                          ║
║  2. Add all changes                                          ║
║  3. Commit with message                                      ║
║  4. Push to GitHub                                           ║
║  5. Show GitHub Actions URL                                  ║
╚═══════════════════════════════════════════════════════════════╝
"@ -ForegroundColor $Cyan
}

function Test-GitInstalled {
    try {
        $null = Get-Command git -ErrorAction Stop
        return $true
    } catch {
        return $false
    }
}

function Get-GitHubUsername {
    try {
        $username = git config user.name
        if ($username) { return $username }
        
        # Prøv å hente fra remote URL
        $remoteUrl = git remote get-url origin 2>$null
        if ($remoteUrl -match "github.com[:/]([^/]+)") {
            return $Matches[1]
        }
        return $null
    } catch {
        return $null
    }
}

function Get-RepoName {
    try {
        $remoteUrl = git remote get-url origin 2>$null
        if ($remoteUrl) {
            # Håndter både HTTPS og SSH
            if ($remoteUrl -match "/([^/]+)\.git$") {
                return $Matches[1]
            } elseif ($remoteUrl -match "/([^/]+)$") {
                return $Matches[1]
            }
        }
        
        # Fallback til mappe-navn
        return (Get-Item .).Name
    } catch {
        return (Get-Item .).Name
    }
}

# ═══════════════════════════════════════════════════════════════════════
# MAIN SCRIPT
# ═══════════════════════════════════════════════════════════════════════

Write-Banner

# Step 1: Verifiser at git er installert
Write-Host "`n📋 Step 1: Checking prerequisites..." -ForegroundColor $Yellow

if (-not (Test-GitInstalled)) {
    Write-Host "❌ ERROR: Git is not installed!" -ForegroundColor $Red
    Write-Host "   Install from: https://git-scm.com/download/win" -ForegroundColor $Yellow
    exit 1
}

Write-Host "   ✅ Git is installed" -ForegroundColor $Green

# Step 2: Sjekk om vi er i et git repo
Write-Host "`n📁 Step 2: Checking git repository..." -ForegroundColor $Yellow

if (-not (Test-Path .git)) {
    Write-Host "   ⚠️  No git repository found. Initializing..." -ForegroundColor $Yellow
    git init
    Write-Host "   ✅ Git repository initialized" -ForegroundColor $Green
    
    $FirstPush = $true
} else {
    Write-Host "   ✅ Git repository exists" -ForegroundColor $Green
}

# Step 3: Sjekk remote
Write-Host "`n🌐 Step 3: Checking remote repository..." -ForegroundColor $Yellow

$remote = git remote get-url $RemoteName 2>$null
if (-not $remote) {
    Write-Host "   ⚠️  No remote '$RemoteName' configured." -ForegroundColor $Yellow
    
    $username = Read-Host "   Enter your GitHub username"
    $repoName = Read-Host "   Enter repository name (default: $(Get-RepoName))"
    
    if (-not $repoName) {
        $repoName = Get-RepoName
    }
    
    $remoteUrl = "https://github.com/$username/$repoName.git"
    
    Write-Host "   Adding remote: $remoteUrl" -ForegroundColor $Cyan
    git remote add $RemoteName $remoteUrl
    Write-Host "   ✅ Remote added" -ForegroundColor $Green
    
    $FirstPush = $true
} else {
    Write-Host "   ✅ Remote '$RemoteName' exists: $remote" -ForegroundColor $Green
}

# Step 4: Sjekk branch
Write-Host "`n🌿 Step 4: Checking branch '$Branch'..." -ForegroundColor $Yellow

$currentBranch = git branch --show-current 2>$null
if ($currentBranch -ne $Branch) {
    Write-Host "   Switching from '$currentBranch' to '$Branch'..." -ForegroundColor $Cyan
    
    # Sjekk om branch eksisterer
    $branchExists = git branch --list $Branch
    if (-not $branchExists) {
        git checkout -b $Branch
    } else {
        git checkout $Branch
    }
    Write-Host "   ✅ Now on branch '$Branch'" -ForegroundColor $Green
} else {
    Write-Host "   ✅ Already on branch '$Branch'" -ForegroundColor $Green
}

# Step 5: Git add
Write-Host "`n📦 Step 5: Adding files to git..." -ForegroundColor $Yellow

git add .
$addedFiles = git diff --cached --name-only

if (-not $addedFiles) {
    Write-Host "   ⚠️  No changes to commit!" -ForegroundColor $Yellow
    Write-Host "`n   Your working directory is clean." -ForegroundColor $Green
} else {
    $fileCount = ($addedFiles | Measure-Object).Count
    Write-Host "   ✅ Added $fileCount file(s) to staging:" -ForegroundColor $Green
    $addedFiles | ForEach-Object { Write-Host "      - $_" -ForegroundColor $Cyan }
}

# Step 6: Commit
Write-Host "`n💾 Step 6: Committing changes..." -ForegroundColor $Yellow

$hasChanges = git diff --cached --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host "   ⚠️  No changes to commit" -ForegroundColor $Yellow
} else {
    Write-Host "   Commit message: $CommitMessage" -ForegroundColor $Cyan
    git commit -m "$CommitMessage"
    Write-Host "   ✅ Changes committed" -ForegroundColor $Green
}

# Step 7: Push
Write-Host "`n🚀 Step 7: Pushing to GitHub..." -ForegroundColor $Yellow

try {
    if ($FirstPush) {
        Write-Host "   First push - setting upstream..." -ForegroundColor $Cyan
        git push -u $RemoteName $Branch
    } else {
        git push $RemoteName $Branch
    }
    Write-Host "   ✅ Successfully pushed to GitHub!" -ForegroundColor $Green
} catch {
    Write-Host "   ❌ Push failed: $_" -ForegroundColor $Red
    Write-Host "`n   Troubleshooting:" -ForegroundColor $Yellow
    Write-Host "   1. Check your internet connection" -ForegroundColor $Yellow
    Write-Host "   2. Verify GitHub credentials" -ForegroundColor $Yellow
    Write-Host "   3. Ensure you have write access to the repository" -ForegroundColor $Yellow
    exit 1
}

# Step 8: Vis GitHub info
Write-Host "`n📊 Step 8: Repository Information..." -ForegroundColor $Yellow

$username = Get-GitHubUsername
$repoName = Get-RepoName

if ($username) {
    $repoUrl = "https://github.com/$username/$repoName"
    $actionsUrl = "$repoUrl/actions"
    
    Write-Host "   Repository: $repoUrl" -ForegroundColor $Cyan
    Write-Host "   Actions:    $actionsUrl" -ForegroundColor $Cyan
    
    if ($OpenBrowser) {
        Write-Host "`n   Opening browser..." -ForegroundColor $Green
        Start-Process $actionsUrl
    } else {
        Write-Host "`n   💡 Tip: Run with -OpenBrowser to automatically open GitHub Actions" -ForegroundColor $Magenta
    }
} else {
    Write-Host "   ⚠️  Could not determine GitHub username" -ForegroundColor $Yellow
}

# ═══════════════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════════════

Write-Host @"

╔═══════════════════════════════════════════════════════════════╗
║                    ✅ PUSH COMPLETED!                         ║
╚═══════════════════════════════════════════════════════════════╝
"@ -ForegroundColor $Green

Write-Host "Next steps:" -ForegroundColor $Yellow
Write-Host "  1. Visit GitHub Actions to see your pipeline running" -ForegroundColor $White
if ($username) {
    Write-Host "     URL: https://github.com/$username/$repoName/actions" -ForegroundColor $Cyan
}
Write-Host "  2. Wait for the CI/CD pipeline to complete (2-5 minutes)" -ForegroundColor $White
Write-Host "  3. Check that all stages pass: Code Quality → Testing → Build → Deploy" -ForegroundColor $White
Write-Host "`nYour CI/CD pipeline is now active! 🎉" -ForegroundColor $Green

# Vent på brukerinput
Write-Host "`nPress any key to continue..." -ForegroundColor $Magenta
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
