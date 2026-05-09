#!/usr/bin/env pwsh
# Enkel GitHub setup og push - Windows-vennlig versjon
# Bruker ASCII-tegn for aa unngaa encoding-problemer

param(
    [string]$CommitMessage = "ci: Implement complete CI/CD pipeline",
    [switch]$OpenBrowser
)

Write-Host "========================================"
Write-Host "    GITHUB SETUP & PUSH"
Write-Host "========================================"
Write-Host ""

# Sjekk git
Write-Host "[1/6] Sjekker Git..."
try {
    $gitVersion = git --version 2>$null
    Write-Host "      OK: $gitVersion"
} catch {
    Write-Host "      FEIL: Git er ikke installert!"
    Write-Host "      Last ned fra: https://git-scm.com/download/win"
    exit 1
}

# Sjekk/init git repo
Write-Host ""
Write-Host "[2/6] Sjekker Git repository..."
if (Test-Path .git) {
    Write-Host "      OK: Git repo finnes"
} else {
    Write-Host "      Initierer nytt repo..."
    git init
    Write-Host "      OK: Repo initiert"
}

# Sjekk GitHub remote
Write-Host ""
Write-Host "[3/6] Sjekker GitHub remote..."
$remote = git remote get-url origin 2>$null

if ($remote) {
    Write-Host "      OK: Remote funnet"
    Write-Host "      URL: $remote"
} else {
    Write-Host "      Ingen remote funnet"
    Write-Host ""
    Write-Host "      Du maa koble til GitHub."
    Write-Host ""
    
    # Spor etter brukernavn og repo
    $username = Read-Host "      Ditt GitHub brukernavn"
    $repoName = Read-Host "      Repository navn (trykk Enter for 'anita-agent')"
    
    if ([string]::IsNullOrWhiteSpace($repoName)) {
        $repoName = "anita-agent"
    }
    
    $remoteUrl = "https://github.com/$username/$repoName.git"
    
    Write-Host ""
    Write-Host "      Legger til remote: $remoteUrl"
    git remote add origin $remoteUrl
    Write-Host "      OK: Remote lagt til"
    
    Write-Host ""
    Write-Host "      VIKTIG: Sjekk at repoet finnes paa GitHub!"
    Write-Host "      Hvis ikke, opprett det her:"
    Write-Host "      https://github.com/new"
    Write-Host ""
    
    $continue = Read-Host "      Trykk Enter for aa fortsette (eller Ctrl+C for aa avbryte)"
}

# Git add
Write-Host ""
Write-Host "[4/6] Legger til filer..."
git add .
$status = git status --short
if ($status) {
    $count = ($status | Measure-Object).Count
    Write-Host "      OK: $count fil(er) lagt til"
} else {
    Write-Host "      Ingen endringer aa commite"
}

# Git commit
Write-Host ""
Write-Host "[5/6] Committer..."
$hasChanges = git diff --cached --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host "      Ingen endringer aa commite"
} else {
    git commit -m "$CommitMessage"
    Write-Host "      OK: Committed"
}

# Git push
Write-Host ""
Write-Host "[6/6] Pusher til GitHub..."
try {
    git push -u origin main 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "      OK: Push fullfort!"
    } else {
        # Prov master hvis main feiler
        git push -u origin master 2>$null
        Write-Host "      OK: Push fullfort (master branch)!"
    }
} catch {
    Write-Host "      FEIL: Push feilet"
    Write-Host "      Sjekk at du har skrivetilgang til repoet"
    exit 1
}

# Vis info
Write-Host ""
Write-Host "========================================"
Write-Host "    ✅ FULLFORT!"
Write-Host "========================================"
Write-Host ""

# Hent brukernavn og repo for URL
$remoteUrl = git remote get-url origin 2>$null
if ($remoteUrl -match "github.com[:/]([^/]+)/([^/]+?)(\.git)?$") {
    $user = $Matches[1]
    $repo = $Matches[2]
    $actionsUrl = "https://github.com/$user/$repo/actions"
    
    Write-Host "GitHub Repository:"
    Write-Host "  https://github.com/$user/$repo"
    Write-Host ""
    Write-Host "GitHub Actions (sjekk pipelinen her):"
    Write-Host "  $actionsUrl"
    Write-Host ""
    
    if ($OpenBrowser) {
        Write-Host "Aapner nettleser..."
        Start-Process $actionsUrl
    } else {
        Write-Host "Tips: Kjor scriptet med -OpenBrowser for aa aapne automatisk"
    }
}

Write-Host ""
Write-Host "Trykk en tast for aa lukke..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
