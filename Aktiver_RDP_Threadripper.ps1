#Requires -RunAsAdministrator
<#
.SYNOPSIS
    Aktiverer Remote Desktop og PowerShell Remoting på Threadripper
    slik at du kan styre den fra Acer.
#>

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  AKTIVERER EKSTERN TILGANG PÅ THREADRIPPER" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""

# 1. Aktiver Remote Desktop
Write-Host "[1/4] Aktiverer Remote Desktop..." -ForegroundColor Cyan
Set-ItemProperty -Path "HKLM:\System\CurrentControlSet\Control\Terminal Server" -Name "fDenyTSConnections" -Value 0
Enable-NetFirewallRule -DisplayGroup "Remote Desktop"
Write-Host "      [OK] Remote Desktop aktivert" -ForegroundColor Green

# 2. Aktiver PowerShell Remoting (WinRM)
Write-Host "[2/4] Aktiverer PowerShell Remoting..." -ForegroundColor Cyan
Enable-PSRemoting -Force -SkipNetworkProfileCheck | Out-Null
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" -Name "LocalAccountTokenFilterPolicy" -Value 1
Write-Host "      [OK] PowerShell Remoting aktivert" -ForegroundColor Green

# 3. Sett opp brannmur-regler
Write-Host "[3/4] Konfigurerer brannmur..." -ForegroundColor Cyan
New-NetFirewallRule -DisplayName "RDP-Inbound" -Direction Inbound -LocalPort 3389 -Protocol TCP -Action Allow -Enabled True -ErrorAction SilentlyContinue | Out-Null
New-NetFirewallRule -DisplayName "WinRM-Inbound" -Direction Inbound -LocalPort 5985 -Protocol TCP -Action Allow -Enabled True -ErrorAction SilentlyContinue | Out-Null
Write-Host "      [OK] Brannmur-regler satt opp" -ForegroundColor Green

# 4. Sett opp Docker-ekstern tilgang
Write-Host "[4/4] Konfigurerer Docker for ekstern tilgang..." -ForegroundColor Cyan
$dockerConfigPath = "$env:USERPROFILE\.docker\daemon.json"
$dockerConfig = @{
    "hosts" = @("tcp://0.0.0.0:2375", "npipe://")
}

if (!(Test-Path "$env:USERPROFILE\.docker")) {
    New-Item -ItemType Directory -Path "$env:USERPROFILE\.docker" -Force | Out-Null
}

$dockerConfig | ConvertTo-Json -Depth 10 | Out-File -FilePath $dockerConfigPath -Encoding UTF8
Write-Host "      [OK] Docker konfigurert for ekstern tilgang (port 2375)" -ForegroundColor Green
Write-Host "      [!] Husk: Start Docker Desktop på nytt etterpå!" -ForegroundColor Yellow

# Oppsummering
Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  EKSTERN TILGANG AKTIVERT!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "  FRA ACER KAN DU NÅ:" -ForegroundColor Cyan
Write-Host ""
Write-Host "  1. Remote Desktop (RDP)" -ForegroundColor White
Write-Host "     - IP: 192.168.1.200 (eller 192.168.1.16)" -ForegroundColor Gray
Write-Host "     - Port: 3389" -ForegroundColor Gray
Write-Host ""
Write-Host "  2. PowerShell Remoting" -ForegroundColor White
Write-Host "     - Enter-PSSession -ComputerName 192.168.1.200" -ForegroundColor Gray
Write-Host ""
Write-Host "  3. Docker-administrasjon" -ForegroundColor White
Write-Host "     - docker -H tcp://192.168.1.200:2375 ps" -ForegroundColor Gray
Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""

# Lag RDP-fil for enkel tilgang
$rdpContent = @"
screen mode id:i:2
use multimon:i:0
desktopwidth:i:1920
desktopheight:i:1080
session bpp:i:32
winposstr:s:0,1,100,100,1200,800
compression:i:1
keyboardhook:i:2
audiocapturemode:i:0
videoplaybackmode:i:1
connection type:i:7
networkautodetect:i:1
bandwidthautodetect:i:1
displayconnectionbar:i:1
enableworkspacereconnect:i:0
disable wallpaper:i:0
allow font smoothing:i:0
allow desktop composition:i:0
disable full window drag:i:1
disable menu anims:i:1
disable themes:i:0
disable cursor setting:i:0
bitmapcachepersistenable:i:1
full address:s:192.168.1.200
audiomode:i:0
redirectprinters:i:1
redirectcomports:i:0
redirectsmartcards:i:1
redirectclipboard:i:1
redirectposdevices:i:0
autoreconnection enabled:i:1
authentication level:i:2
prompt for credentials:i:0
negotiate security layer:i:1
remoteapplicationmode:i:0
alternate shell:s:
shell working directory:s:
gatewayhostname:s:
gatewayusagemethod:i:4
gatewaycredentialssource:i:4
gatewayprofileusagemethod:i:0
promptcredentialonce:i:0
gatewaybrokeringtype:i:0
use redirection server name:i:0
rdgiskdcproxy:i:0
kdcproxyname:s:
"@

$rdpPath = "C:\Users\$env:USERNAME\Desktop\Threadripper_Remote.rdp"
$rdpContent | Out-File -FilePath $rdpPath -Encoding ASCII
Write-Host "  RDP-fil lagret på: $rdpPath" -ForegroundColor Green
Write-Host ""
Write-Host "  DOBBELTKLIKK DENNE FILEN PÅ ACER FOR Å KOBLE TIL!" -ForegroundColor Yellow
Write-Host ""
