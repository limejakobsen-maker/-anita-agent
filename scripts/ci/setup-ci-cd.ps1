#!/usr/bin/env pwsh
# CI/CD Setup Script for Anita Agent
# Run this script to initialize the CI/CD pipeline

param(
    [Parameter()]
    [ValidateSet("github", "gitlab", "azure")]
    [string]$Platform = "github",
    
    [Parameter()]
    [ValidateSet("flux", "argocd")]
    [string]$GitOpsTool = "flux",
    
    [Parameter()]
    [string]$GitHubUsername = "",
    
    [Parameter()]
    [switch]$SkipDocker,
    
    [Parameter()]
    [switch]$SkipK8s
)

$ErrorActionPreference = "Stop"

Write-Host @"
╔═══════════════════════════════════════════════════════════════╗
║           ANITA AGENT - CI/CD SETUP                           ║
║                                                               ║
║  Platform: $Platform                                          ║
║  GitOps: $GitOpsTool                                          ║
╚═══════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

# ============================================================================
# Step 1: Verify Prerequisites
# ============================================================================
Write-Host "`n📋 Step 1: Verifying Prerequisites..." -ForegroundColor Yellow

$prerequisites = @(
    @{ Name = "Git"; Command = "git --version" },
    @{ Name = "Docker"; Command = "docker --version" },
    @{ Name = "Kubectl"; Command = "kubectl version --client" }
)

foreach ($prereq in $prerequisites) {
    try {
        Invoke-Expression $prereq.Command | Out-Null
        Write-Host "  ✅ $($prereq.Name)" -ForegroundColor Green
    } catch {
        Write-Host "  ❌ $($prereq.Name) - Not installed" -ForegroundColor Red
        if ($prereq.Name -eq "Docker" -and $SkipDocker) {
            Write-Host "     (Skipped due to -SkipDocker)" -ForegroundColor Yellow
        } elseif ($prereq.Name -eq "Kubectl" -and $SkipK8s) {
            Write-Host "     (Skipped due to -SkipK8s)" -ForegroundColor Yellow
        }
    }
}

# ============================================================================
# Step 2: Initialize Git Repository
# ============================================================================
Write-Host "`n📁 Step 2: Initializing Git Repository..." -ForegroundColor Yellow

if (-not (Test-Path ".git")) {
    git init
    git add .
    git commit -m "Initial commit: CI/CD pipeline setup"
    Write-Host "  ✅ Git repository initialized" -ForegroundColor Green
} else {
    Write-Host "  ℹ️  Git repository already exists" -ForegroundColor Blue
}

# ============================================================================
# Step 3: Setup GitHub Repository
# ============================================================================
if ($Platform -eq "github") {
    Write-Host "`n🐙 Step 3: Setting up GitHub Repository..." -ForegroundColor Yellow
    
    if (-not $GitHubUsername) {
        $GitHubUsername = Read-Host "Enter your GitHub username"
    }
    
    $RepoName = "anita-agent"
    
    # Check if gh CLI is installed
    if (Get-Command gh -ErrorAction SilentlyContinue) {
        $repoExists = gh repo view "$GitHubUsername/$RepoName" 2>$null
        if (-not $repoExists) {
            Write-Host "  Creating GitHub repository..." -ForegroundColor Blue
            gh repo create "$RepoName" --public --source=. --remote=origin --push
        } else {
            Write-Host "  ℹ️  Repository already exists on GitHub" -ForegroundColor Blue
            git remote add origin "https://github.com/$GitHubUsername/$RepoName.git" 2>$null
        }
    } else {
        Write-Host "  ⚠️  GitHub CLI (gh) not installed. Please manually:" -ForegroundColor Yellow
        Write-Host "     1. Create repo: https://github.com/new" -ForegroundColor Yellow
        Write-Host "     2. Run: git remote add origin https://github.com/$GitHubUsername/$RepoName.git" -ForegroundColor Yellow
    }
}

# ============================================================================
# Step 4: Build Docker Image
# ============================================================================
if (-not $SkipDocker) {
    Write-Host "`n🐳 Step 4: Building Docker Image..." -ForegroundColor Yellow
    
    try {
        docker build --target testing -t anita-agent:local-test .
        Write-Host "  ✅ Docker image built successfully" -ForegroundColor Green
        
        Write-Host "`n  Testing Docker image..." -ForegroundColor Blue
        docker run --rm anita-agent:local-test pytest tests/unit -v --tb=short
        Write-Host "  ✅ Tests passed in Docker" -ForegroundColor Green
    } catch {
        Write-Host "  ❌ Docker build failed: $_" -ForegroundColor Red
    }
} else {
    Write-Host "`n🐳 Step 4: Skipping Docker build (-SkipDocker)" -ForegroundColor Yellow
}

# ============================================================================
# Step 5: Setup Kubernetes (K3d)
# ============================================================================
if (-not $SkipK8s) {
    Write-Host "`n☸️  Step 5: Setting up Kubernetes..." -ForegroundColor Yellow
    
    # Check for k3d
    if (Get-Command k3d -ErrorAction SilentlyContinue) {
        $clusterExists = k3d cluster list | Select-String "anita-agent"
        
        if (-not $clusterExists) {
            Write-Host "  Creating K3d cluster..." -ForegroundColor Blue
            k3d cluster create anita-agent `
                --agents 2 `
                --port "8080:80@loadbalancer" `
                --port "8765:8765@loadbalancer" `
                --wait
            Write-Host "  ✅ K3d cluster created" -ForegroundColor Green
        } else {
            Write-Host "  ℹ️  K3d cluster already exists" -ForegroundColor Blue
        }
        
        # Verify cluster
        kubectl cluster-info
        kubectl get nodes
        
        # Deploy testing environment
        Write-Host "`n  Deploying testing environment..." -ForegroundColor Blue
        kubectl apply -f k8s/namespaces/testing-namespace.yaml
        kubectl apply -k k8s/ci-cd/overlays/testing/
        
        Write-Host "  ⏳ Waiting for deployment..." -ForegroundColor Blue
        kubectl rollout status deployment/anita-agent -n testing-anita-agent --timeout=120s
        
        Write-Host "  ✅ Testing environment deployed" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  K3d not installed. Skipping Kubernetes setup." -ForegroundColor Yellow
        Write-Host "     Install: https://k3d.io/#installation" -ForegroundColor Yellow
    }
} else {
    Write-Host "`n☸️  Step 5: Skipping Kubernetes setup (-SkipK8s)" -ForegroundColor Yellow
}

# ============================================================================
# Step 6: Setup GitOps
# ============================================================================
Write-Host "`n🔄 Step 6: Setting up GitOps ($GitOpsTool)..." -ForegroundColor Yellow

if ($GitOpsTool -eq "flux") {
    if (Get-Command flux -ErrorAction SilentlyContinue) {
        $fluxInstalled = kubectl get namespaces | Select-String "flux-system"
        
        if (-not $fluxInstalled) {
            Write-Host "  Installing Flux..." -ForegroundColor Blue
            flux install
        }
        
        Write-Host "  Applying Flux configurations..." -ForegroundColor Blue
        kubectl apply -f gitops/flux/
        Write-Host "  ✅ Flux configured" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  Flux CLI not installed. Install: https://fluxcd.io/docs/installation/" -ForegroundColor Yellow
    }
} elseif ($GitOpsTool -eq "argocd") {
    $argocdInstalled = kubectl get namespaces | Select-String "argocd"
    
    if (-not $argocdInstalled) {
        Write-Host "  Installing ArgoCD..." -ForegroundColor Blue
        kubectl create namespace argocd
        kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
        
        Write-Host "  Waiting for ArgoCD to be ready..." -ForegroundColor Blue
        kubectl wait --for=condition=available --timeout=300s deployment/argocd-server -n argocd
    }
    
    Write-Host "  Applying ArgoCD applications..." -ForegroundColor Blue
    kubectl apply -f gitops/argocd/
    Write-Host "  ✅ ArgoCD configured" -ForegroundColor Green
}

# ============================================================================
# Summary
# ============================================================================
Write-Host @"

╔═══════════════════════════════════════════════════════════════╗
║                    SETUP COMPLETE!                            ║
╚═══════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Green

Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "  1. Push to GitHub: git push -u origin main" -ForegroundColor White
Write-Host "  2. Check GitHub Actions: https://github.com/$GitHubUsername/anita-agent/actions" -ForegroundColor White
Write-Host "  3. Verify deployment:" -ForegroundColor White

if (-not $SkipK8s) {
    Write-Host "     kubectl get pods -n testing-anita-agent" -ForegroundColor Yellow
}

Write-Host "`nDocumentation:" -ForegroundColor Cyan
Write-Host "  📖 CI_CD_GUIDE.md - Full CI/CD documentation" -ForegroundColor White
Write-Host "  📖 gitops/README.md - GitOps configuration" -ForegroundColor White
Write-Host "  📖 tests/ - Test suite" -ForegroundColor White

Write-Host ""
