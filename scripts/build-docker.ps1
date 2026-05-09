#!/usr/bin/env pwsh
# Build script for Docker images

param(
    [Parameter()]
    [ValidateSet("production", "development", "testing")]
    [string]$Target = "production",
    
    [Parameter()]
    [string]$Tag = "latest",
    
    [Parameter()]
    [string]$Registry = "ghcr.io",
    
    [Parameter()]
    [switch]$Push,
    
    [Parameter()]
    [switch]$NoCache
)

$ErrorActionPreference = "Stop"

$ImageName = "anita-agent"
$FullImageName = "$Registry/emil/$ImageName`:$Tag"

Write-Host @"
╔═══════════════════════════════════════════════════════════════╗
║           DOCKER BUILD SCRIPT                                ║
║                                                              ║
║  Target:  $Target                                            ║
║  Tag:     $Tag                                               ║
║  Image:   $FullImageName                                     ║
╚═══════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

# Sjekk at Docker er installert
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Error "Docker er ikke installert!"
    exit 1
}

# Build arguments
$buildArgs = @(
    "build",
    "-f", "Dockerfile",
    "--target", $Target,
    "-t", "$ImageName`:$Tag"
)

if ($NoCache) {
    $buildArgs += "--no-cache"
}

$buildArgs += "."

Write-Host "`n📦 Bygger Docker image..." -ForegroundColor Yellow
& docker @buildArgs

if ($LASTEXITCODE -ne 0) {
    Write-Error "Docker build feilet!"
    exit 1
}

Write-Host "✅ Build fullført!" -ForegroundColor Green

# Tag for registry
if ($Push) {
    Write-Host "`n🏷️  Tagger image..." -ForegroundColor Yellow
    docker tag "$ImageName`:$Tag" $FullImageName
    
    Write-Host "`n📤 Pusher til registry..." -ForegroundColor Yellow
    docker push $FullImageName
    
    Write-Host "✅ Push fullført!" -ForegroundColor Green
}

# Vis image info
Write-Host "`n📊 Image Info:" -ForegroundColor Cyan
docker images $ImageName`:$Tag --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"

Write-Host "`n✅ Ferdig!" -ForegroundColor Green

if (-not $Push) {
    Write-Host "`nFor å pushe til registry, kjør:" -ForegroundColor Yellow
    Write-Host "  .\scripts\build-docker.ps1 -Target $Target -Tag $Tag -Push" -ForegroundColor White
}
