#!/usr/bin/env pwsh
# Deploy script for Kubernetes

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("production", "testing")]
    [string]$Environment,
    
    [Parameter()]
    [string]$Context = "",
    
    [Parameter()]
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

Write-Host @"
╔═══════════════════════════════════════════════════════════════╗
║           KUBERNETES DEPLOY SCRIPT                           ║
║                                                              ║
║  Environment: $Environment                                      ║
╚═══════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

# Sett context hvis spesifisert
if ($Context) {
    Write-Host "Switching to context: $Context" -ForegroundColor Yellow
    kubectl config use-context $Context
}

# Verifiser tilkobling
Write-Host "`nVerifying cluster connection..." -ForegroundColor Yellow
kubectl cluster-info

if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to connect to cluster!"
    exit 1
}

# Deploy
$overlayPath = "k8s/overlays/$Environment"

Write-Host "`nDeploying from: $overlayPath" -ForegroundColor Yellow

if ($DryRun) {
    Write-Host "`n[DRY RUN] Would execute:" -ForegroundColor Magenta
    Write-Host "  kubectl apply -k $overlayPath" -ForegroundColor Gray
    
    Write-Host "`n[DRY RUN] Generated manifests:" -ForegroundColor Magenta
    kubectl kustomize $overlayPath
} else {
    Write-Host "`nApplying manifests..." -ForegroundColor Yellow
    kubectl apply -k $overlayPath
    
    Write-Host "`nWaiting for rollout..." -ForegroundColor Yellow
    kubectl rollout status deployment/anita-agent -n anita-agent --timeout=300s
    
    Write-Host "`nDeployment status:" -ForegroundColor Green
    kubectl get all -n anita-agent
}

Write-Host "`n✅ Done!" -ForegroundColor Green
