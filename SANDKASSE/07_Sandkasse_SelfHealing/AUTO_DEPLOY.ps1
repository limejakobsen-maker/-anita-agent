#requires -Version 5.1
<#
.SYNOPSIS
    Automatisk deploy av Sandkasse-system til Lenovo
.DESCRIPTION
    Starter HTTP-server, verifiserer filer, og viser instruksjoner for Lenovo
.AUTHOR
    Sandkasse AI Agent
.DATE
    2026-03-02
#>

[CmdletBinding()]
param(
    [string]$LenovoIP = "100.108.91.44",
    [string]$AcerIP = "100.114.112.61",
    [int]$HttpPort = 8000
)

# ═══════════════════════════════════════════════════════════════════
# FARGER OG HJELPEFUNKSJONER
# ═══════════════════════════════════════════════════════════════════
$Colors = @{
    Success = 'Green'
    Info = 'Cyan'
    Warning = 'Yellow'
    Error = 'Red'
    Normal = 'White'
}

function Write-Status($Message, $Type = 'Info') {
    $color = $Colors[$Type]
    Write-Host $Message -ForegroundColor $color
}

function Write-Separator() {
    Write-Host "═" * 70 -ForegroundColor DarkGray
}

# ═══════════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════════
Clear-Host
Write-Separator
Write-Status "  🚀 SANDKASSE AUTO-DEPLOY v3.0" 'Success'
Write-Status "  Dato: $(Get-Date -Format 'yyyy-MM-dd HH:mm')" 'Info'
Write-Separator
Write-Host ""

# ═══════════════════════════════════════════════════════════════════
# STEG 1: VERIFISER HTTP-SERVER
# ═══════════════════════════════════════════════════════════════════
Write-Status "📦 STEG 1: Verifiserer HTTP-server..." 'Info'

$HttpServerUrl = "http://${AcerIP}:${HttpPort}"
$ServerRunning = $false

try {
    $response = Invoke-WebRequest -Uri $HttpServerUrl -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        Write-Status "  ✅ HTTP-server kjører på $HttpServerUrl" 'Success'
        $ServerRunning = $true
    }
} catch {
    Write-Status "  ⚠️  HTTP-server ikke aktiv. Starter..." 'Warning'
    
    # Start HTTP-server i bakgrunnen
    $SourcePath = "C:\Users\limej\OneDrive\Desktop\SANDKASSE\07_Sandkasse_SelfHealing\for_lenovo"
    
    if (Test-Path $SourcePath) {
        Start-Process -FilePath "python" -ArgumentList "-m", "http.server", "$HttpPort", "--bind", "$AcerIP" -WorkingDirectory $SourcePath -WindowStyle Hidden
        Start-Sleep -Seconds 3
        
        # Verifiser at den startet
        try {
            $response = Invoke-WebRequest -Uri $HttpServerUrl -UseBasicParsing -TimeoutSec 5
            if ($response.StatusCode -eq 200) {
                Write-Status "  ✅ HTTP-server startet på $HttpServerUrl" 'Success'
                $ServerRunning = $true
            }
        } catch {
            Write-Status "  ❌ Kunne ikke starte HTTP-server" 'Error'
        }
    } else {
        Write-Status "  ❌ Kilde-mappe ikke funnet: $SourcePath" 'Error'
    }
}

Write-Host ""

# ═══════════════════════════════════════════════════════════════════
# STEG 2: VERIFISER FILER
# ═══════════════════════════════════════════════════════════════════
Write-Status "📁 STEG 2: Verifiserer filer..." 'Info'

$SourcePath = "C:\Users\limej\OneDrive\Desktop\SANDKASSE\07_Sandkasse_SelfHealing\for_lenovo"
$RequiredFiles = @(
    "sandkasse_protokoll.py",
    "sandkasse_protokoll_part2.py",
    "protokoll_server.py",
    "self_healing_wrapper.py",
    "error_handler.py",
    "ai_fixer.py",
    "install.sh"
)

$AllFilesPresent = $true
$TotalSize = 0

foreach ($file in $RequiredFiles) {
    $filePath = Join-Path $SourcePath $file
    if (Test-Path $filePath) {
        $size = (Get-Item $filePath).Length
        $TotalSize += $size
        $sizeKB = [math]::Round($size / 1KB, 2)
        Write-Status "  ✅ $file ($sizeKB KB)" 'Success'
    } else {
        Write-Status "  ❌ $file (MANGLER!)" 'Error'
        $AllFilesPresent = $false
    }
}

$TotalSizeKB = [math]::Round($TotalSize / 1KB, 2)
Write-Status "  📊 Totalt: $TotalSizeKB KB" 'Info'
Write-Host ""

# ═══════════════════════════════════════════════════════════════════
# STEG 3: NETTVERKSTEST
# ═══════════════════════════════════════════════════════════════════
Write-Status "🌐 STEG 3: Tester nettverk..." 'Info'

# Sjekk Tailscale
$TailscaleOnline = $false
try {
    $tailscaleOutput = & tailscale status 2>$null
    if ($tailscaleOutput -match $LenovoIP) {
        Write-Status "  ✅ Tailscale: Lenovo funnet ($LenovoIP)" 'Success'
        $TailscaleOnline = $true
    } else {
        Write-Status "  ⚠️  Tailscale: Lenovo ikke funnet i status" 'Warning'
    }
} catch {
    Write-Status "  ⚠️  Tailscale: Kunne ikke sjekke status" 'Warning'
}

# Ping-test
try {
    $pingResult = Test-Connection -ComputerName $LenovoIP -Count 2 -Quiet -ErrorAction Stop
    if ($pingResult) {
        Write-Status "  ✅ Ping til $LenovoIP: OK" 'Success'
    } else {
        Write-Status "  ⚠️  Ping til $LenovoIP: Ingen respons" 'Warning'
    }
} catch {
    Write-Status "  ⚠️  Ping til $LenovoIP: Feil" 'Warning'
}

Write-Host ""

# ═══════════════════════════════════════════════════════════════════
# STEG 4: GENERER LENOVO-KOMMANDOER
# ═══════════════════════════════════════════════════════════════════
Write-Status "📝 STEG 4: Lenovo kommandoer klare..." 'Info'
Write-Host ""

$LenovoCommands = @"
╔══════════════════════════════════════════════════════════════════════╗
  KOPIER OG LIM INN PÅ LENOVO (Terminal):                              
╚══════════════════════════════════════════════════════════════════════╝

# 1. Opprett mappe
mkdir -p ~/self_healing_system && cd ~/self_healing_system

# 2. Last ned alle filer
curl -O http://$AcerIP`:$HttpPort/sandkasse_protokoll.py
curl -O http://$AcerIP`:$HttpPort/sandkasse_protokoll_part2.py
curl -O http://$AcerIP`:$HttpPort/protokoll_server.py
curl -O http://$AcerIP`:$HttpPort/self_healing_wrapper.py
curl -O http://$AcerIP`:$HttpPort/error_handler.py
curl -O http://$AcerIP`:$HttpPort/ai_fixer.py
curl -O http://$AcerIP`:$HttpPort/install.sh

# 3. Verifiser filer
ls -la

# 4. Installer
chmod +x install.sh && ./install.sh

# 5. Start server
python3 protokoll_server.py

"@

Write-Host $LenovoCommands -ForegroundColor Cyan

# ═══════════════════════════════════════════════════════════════════
# STEG 5: ELLER - HELAUTOMATISK SSH (hvis nøkler er satt opp)
# ═══════════════════════════════════════════════════════════════════
Write-Status "🤖 STEG 5: Alternativ - SSH (hvis konfigurert)..." 'Info'
Write-Host ""

Write-Host "Hvis du har SSH-nøkler satt opp, kan du kjøre:"
Write-Host ""
Write-Host "  ssh emil@$LenovoIP 'bash -s' < deploy_to_lenovo_remote.sh" -ForegroundColor Yellow
Write-Host ""

# ═══════════════════════════════════════════════════════════════════
# OPPSUMMERING
# ═══════════════════════════════════════════════════════════════════
Write-Separator
Write-Status "  📋 OPPSUMMERING" 'Info'
Write-Separator
Write-Host ""

if ($AllFilesPresent -and $ServerRunning) {
    Write-Status "  ✅ ALLE FILER KLARE PÅ HTTP-SERVER!" 'Success'
    Write-Status "  ✅ Lenovo kan nå laste ned filer" 'Success'
    Write-Host ""
    Write-Status "  NESTE STEG:" 'Info'
    Write-Status "  1. Kopier kommandoene over til Lenovo terminal" 'Normal'
    Write-Status "  2. Kjør dem på Lenovo" 'Normal'
    Write-Status "  3. Når server starter, kjør på Acer:" 'Normal'
    Write-Status "     python protokoll_monitor.py" 'Normal'
    Write-Host ""
    Write-Status "  🎯 ELLER: Åpne http://$HttpServerUrl i nettleser for å se filene" 'Info'
} else {
    Write-Status "  ⚠️  NOE MANGER - Sjekk feilmeldinger over" 'Warning'
}

Write-Host ""
Write-Separator
Write-Status "  HTTP Server: $HttpServerUrl" 'Info'
Write-Status "  Lenovo IP:   $LenovoIP" 'Info'
Write-Status "  Acer IP:     $AcerIP" 'Info'
Write-Separator
Write-Host ""

# Hold vinduet åpent
Write-Host "Trykk ENTER for å lukke..." -ForegroundColor DarkGray
$null = Read-Host
