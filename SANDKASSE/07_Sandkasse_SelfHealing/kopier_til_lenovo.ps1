#!/usr/bin/env pwsh
# ═══════════════════════════════════════════════════════════════════
# KOPERE TIL LENOVO - Automatisk filoverføring
# Kopierer Optimal Sandkasse v3.0 til Lenovo via SSH/SCP
# ═══════════════════════════════════════════════════════════════════

param(
    [string]$LenovoIP = "100.108.91.44",
    [string]$LenovoUser = "emil",
    [string]$SourcePath = "C:\Users\limej\OneDrive\Desktop\SANDKASSE\07_Sandkasse_SelfHealing\for_lenovo",
    [string]$DestPath = "/home/emil/self_healing_system"
)

Write-Host "╔══════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  🚀 KOPIERER OPTIMAL SANDKASSE TIL LENOVO                       ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Sjekk at kilde finnes
if (-not (Test-Path $SourcePath)) {
    Write-Host "❌ FEIL: Fant ikke kilde-mappe: $SourcePath" -ForegroundColor Red
    Write-Host "   Sjekk at du kjører skriptet fra 07_Sandkasse_SelfHealing/" -ForegroundColor Yellow
    exit 1
}

Write-Host "📁 Kilde: $SourcePath" -ForegroundColor Gray
Write-Host "🎯 Mål: $LenovoUser@${LenovoIP}:$DestPath" -ForegroundColor Gray
Write-Host ""

# Liste over filer som skal kopieres
$filer = @(
    "sandkasse_protokoll.py",
    "sandkasse_protokoll_part2.py", 
    "protokoll_server.py",
    "install.sh",
    "self_healing_wrapper.py",
    "error_handler.py",
    "ai_fixer.py"
)

Write-Host "📋 Filer som skal kopieres:" -ForegroundColor Yellow
foreach ($fil in $filer) {
    $sti = Join-Path $SourcePath $fil
    if (Test-Path $sti) {
        $size = (Get-Item $sti).Length
        Write-Host "   ✅ $fil ($size bytes)" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  $fil (ikke funnet i for_lenovo/)" -ForegroundColor Yellow
    }
}
Write-Host ""

# Sjekk om scp er tilgjengelig
$scp = Get-Command scp -ErrorAction SilentlyContinue
if (-not $scp) {
    Write-Host "❌ SCP ikke funnet. Installerer OpenSSH..." -ForegroundColor Yellow
    
    # Sjekk om Windows har OpenSSH
    $openSsh = Get-Command ssh -ErrorAction SilentlyContinue
    if (-not $openSsh) {
        Write-Host "📦 Installerer OpenSSH Client..." -ForegroundColor Cyan
        Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0
    }
}

# Sjekk tilkobling til Lenovo
Write-Host "🔍 Sjekker tilkobling til Lenovo ($LenovoIP)..." -ForegroundColor Cyan
$ping = Test-Connection -ComputerName $LenovoIP -Count 1 -Quiet -ErrorAction SilentlyContinue

if (-not $ping) {
    Write-Host "⚠️  Kan ikke pinge Lenovo. Sjekk at:" -ForegroundColor Yellow
    Write-Host "   • Lenovo er påslått" -ForegroundColor White
    Write-Host "   • Tailscale kjører på begge maskiner" -ForegroundColor White
    Write-Host "   • Du er koblet til internett" -ForegroundColor White
    Write-Host ""
    
    $fortsett = Read-Host "Vil du prøve å kopiere likevel? (j/n)"
    if ($fortsett -ne "j") {
        Write-Host "❌ Avbrutt" -ForegroundColor Red
        exit 1
    }
}

Write-Host "✅ Lenovo er tilgjengelig!" -ForegroundColor Green
Write-Host ""

# Kopier filer
Write-Host "📤 Starter kopiering..." -ForegroundColor Cyan
Write-Host ""

# Opprett destinasjonsmappe først (via SSH)
Write-Host "📁 Oppretter mappe på Lenovo..." -ForegroundColor Gray
ssh $LenovoUser@$LenovoIP "mkdir -p $DestPath"

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Kunne ikke koble til Lenovo via SSH" -ForegroundColor Red
    Write-Host "   Sjekk at:" -ForegroundColor Yellow
    Write-Host "   • Du kan logge inn på Lenovo med: ssh $LenovoUser@$LenovoIP" -ForegroundColor White
    Write-Host "   • SSH-server kjører på Lenovo" -ForegroundColor White
    exit 1
}

Write-Host "✅ SSH-tilkobling OK!" -ForegroundColor Green
Write-Host ""

# Kopier hver fil
$kopiert = 0
$feil = 0

foreach ($fil in $filer) {
    $kilde = Join-Path $SourcePath $fil
    
    if (-not (Test-Path $kilde)) {
        Write-Host "⏭️  Hopper over $fil (finnes ikke)" -ForegroundColor Gray
        continue
    }
    
    Write-Host "📤 Kopierer $fil..." -ForegroundColor Gray -NoNewline
    
    scp $kilde "${LenovoUser}@${LenovoIP}:${DestPath}/"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host " ✅ OK" -ForegroundColor Green
        $kopiert++
    } else {
        Write-Host " ❌ FEIL" -ForegroundColor Red
        $feil++
    }
}

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  KOPIERING FULLFØRT!                                             ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 Resultat:" -ForegroundColor Yellow
Write-Host "   ✅ Kopiert: $kopiert filer" -ForegroundColor Green
if ($feil -gt 0) {
    Write-Host "   ❌ Feil: $feil filer" -ForegroundColor Red
}
Write-Host ""

if ($kopiert -gt 0) {
    Write-Host "📋 Neste steg på Lenovo:" -ForegroundColor Yellow
    Write-Host "   1. SSH til Lenovo: ssh $LenovoUser@$LenovoIP" -ForegroundColor White
    Write-Host "   2. Kjør: cd $DestPath" -ForegroundColor White
    Write-Host "   3. Kjør: bash install.sh" -ForegroundColor White
    Write-Host "   4. Start server: python3 protokoll_server.py" -ForegroundColor White
    Write-Host ""
    Write-Host "📋 På Acer:" -ForegroundColor Yellow
    Write-Host "   5. Dobbelklikk 'Sandkasse Monitor.lnk'" -ForegroundColor White
}

Write-Host ""
