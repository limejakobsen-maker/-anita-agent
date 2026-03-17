#Requires -Version 5.1
<#
.SYNOPSIS
    Den Digitale Riggen - System Monitor (Acer)
    Overvaker alle maskiner og tjenester i nettverket
#>

[CmdletBinding()]
param(
    [switch]$Watch,
    [int]$WatchInterval = 30,
    [switch]$StartThreadripperServices
)

# Konfigurasjon
$Config = @{
    Threadripper = @{
        Name = "Threadripper"
        IPs = @("192.168.1.200", "192.168.1.16")
        Services = @{
            AnythingLLM = @{ Port = 3001; Name = "AnythingLLM" }
            Ollama = @{ Port = 11434; Name = "Ollama" }
            SMB = @{ Port = 445; Name = "Fildeling (Z:)" }
        }
    }
    Lenovo = @{
        Name = "Lenovo Sandkasse"
        TailscaleIP = "100.108.91.44"
        LocalIP = "192.168.1.120"
        Services = @{
            SSH = @{ Port = 22; Name = "SSH" }
            AnythingLLM = @{ Port = 3001; Name = "AnythingLLM" }
        }
    }
    Acer = @{
        Name = "Acer (Denne maskinen)"
        TailscaleIP = "100.114.112.61"
    }
}

# Farger
$Colors = @{
    Success = "Green"
    Warning = "Yellow"
    Error = "Red"
    Info = "Cyan"
    Header = "Magenta"
}

# Funksjoner
function Write-StatusLine {
    param(
        [string]$Label,
        [string]$Status,
        [string]$Color = "White"
    )
    Write-Host "  " -NoNewline
    Write-Host $Label.PadRight(25) -NoNewline
    Write-Host $Status -ForegroundColor $Color
}

function Test-HostOnline {
    param([string]$IPAddress)
    $result = Test-Connection -ComputerName $IPAddress -Count 1 -Quiet -ErrorAction SilentlyContinue
    return $result
}

function Test-PortOpen {
    param([string]$IPAddress, [int]$Port)
    try {
        $tcp = New-Object System.Net.Sockets.TcpClient
        $tcp.Connect($IPAddress, $Port)
        $tcp.Close()
        return $true
    }
    catch {
        return $false
    }
}

function Get-TailscaleStatus {
    try {
        $status = tailscale status 2>$null
        return $status
    }
    catch {
        return $null
    }
}

function Show-Header {
    Clear-Host
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor $Colors.Header
    Write-Host "         DEN DIGITALE RIGGEN - SYSTEM MONITOR" -ForegroundColor $Colors.Header
    Write-Host "============================================================" -ForegroundColor $Colors.Header
    Write-Host "  Tid: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor $Colors.Info
    Write-Host ""
}

function Show-ThreadripperStatus {
    Write-Host "THREADRIPPER (192.168.1.200)" -ForegroundColor $Colors.Header
    Write-Host "------------------------------------------------------------" -ForegroundColor $Colors.Header
    
    $anyOnline = $false
    foreach ($ip in $Config.Threadripper.IPs) {
        if (Test-HostOnline -IPAddress $ip) {
            $anyOnline = $true
            Write-StatusLine -Label "  Nettverk ($ip)" -Status "[OK] ONLINE" -Color $Colors.Success
        }
    }
    
    if (!$anyOnline) {
        Write-StatusLine -Label "  Nettverk" -Status "[X] OFFLINE" -Color $Colors.Error
        Write-Host ""
        return
    }
    
    # Sjekk tjenester
    foreach ($service in $Config.Threadripper.Services.GetEnumerator() | Sort-Object Key) {
        $port = $service.Value.Port
        $name = $service.Value.Name
        $open = $false
        
        foreach ($ip in $Config.Threadripper.IPs) {
            if (Test-PortOpen -IPAddress $ip -Port $port) {
                $open = $true
                break
            }
        }
        
        if ($open) {
            Write-StatusLine -Label "  $name (:$port)" -Status "[OK] KJORER" -Color $Colors.Success
        }
        else {
            Write-StatusLine -Label "  $name (:$port)" -Status "[X] STOPPET" -Color $Colors.Error
        }
    }
    
    Write-Host "------------------------------------------------------------" -ForegroundColor $Colors.Header
}

function Show-LenovoStatus {
    Write-Host ""
    Write-Host "LENOVO SANDKASSE (100.108.91.44)" -ForegroundColor $Colors.Header
    Write-Host "------------------------------------------------------------" -ForegroundColor $Colors.Header
    
    $localOnline = Test-HostOnline -IPAddress $Config.Lenovo.LocalIP
    $tailscaleOnline = Test-HostOnline -IPAddress $Config.Lenovo.TailscaleIP
    
    if ($localOnline) {
        Write-StatusLine -Label "  Lokal nettverk" -Status "[OK] ONLINE (192.168.1.120)" -Color $Colors.Success
    }
    else {
        Write-StatusLine -Label "  Lokal nettverk" -Status "[!] Utilgjengelig" -Color $Colors.Warning
    }
    
    if ($tailscaleOnline) {
        Write-StatusLine -Label "  Tailscale VPN" -Status "[OK] ONLINE" -Color $Colors.Success
    }
    else {
        Write-StatusLine -Label "  Tailscale VPN" -Status "[X] OFFLINE" -Color $Colors.Error
    }
    
    # Sjekk tjenester
    foreach ($service in $Config.Lenovo.Services.GetEnumerator() | Sort-Object Key) {
        $port = $service.Value.Port
        $name = $service.Value.Name
        $open = Test-PortOpen -IPAddress $Config.Lenovo.TailscaleIP -Port $port
        
        if ($open) {
            Write-StatusLine -Label "  $name (:$port)" -Status "[OK] KJORER" -Color $Colors.Success
        }
        else {
            Write-StatusLine -Label "  $name (:$port)" -Status "[X] STOPPET" -Color $Colors.Error
        }
    }
    
    Write-Host "------------------------------------------------------------" -ForegroundColor $Colors.Header
}

function Show-ZDriveStatus {
    Write-Host ""
    Write-Host "Z: DISK (Bygg_Arkiv)" -ForegroundColor $Colors.Header
    Write-Host "------------------------------------------------------------" -ForegroundColor $Colors.Header
    
    $zDrive = Get-PSDrive Z -ErrorAction SilentlyContinue
    
    if ($zDrive -and (Test-Path "Z:\")) {
        try {
            $used = (Get-ChildItem Z:\ -ErrorAction SilentlyContinue | Measure-Object).Count
            Write-StatusLine -Label "  Tilkobling" -Status "[OK] TILKOBL" -Color $Colors.Success
            Write-StatusLine -Label "  Nettverkssti" -Status "$($zDrive.DisplayRoot)" -Color $Colors.Info
        }
        catch {
            Write-StatusLine -Label "  Tilkobling" -Status "[!] Tilkoblet men tom?" -Color $Colors.Warning
        }
    }
    else {
        Write-StatusLine -Label "  Tilkobling" -Status "[X] FRADISKET" -Color $Colors.Error
        Write-Host ""
        Write-Host "  Tips: Kjor: net use Z: \\\\192.168.1.200\\Bygg_Arkiv" -ForegroundColor $Colors.Warning
    }
    
    Write-Host "------------------------------------------------------------" -ForegroundColor $Colors.Header
}

function Show-TailscaleStatus {
    Write-Host ""
    Write-Host "TAILSCALE VPN" -ForegroundColor $Colors.Header
    Write-Host "------------------------------------------------------------" -ForegroundColor $Colors.Header
    
    $tsStatus = Get-TailscaleStatus
    
    if ($tsStatus) {
        Write-StatusLine -Label "  Din IP" -Status $Config.Acer.TailscaleIP -Color $Colors.Info
        
        $lines = $tsStatus -split "`n" | Where-Object { $_ -match "^100\." }
        
        foreach ($line in $lines) {
            if ($line -match "(\d+\.\d+\.\d+\.\d+)\s+(\S+)\s+.*(online|offline|idle)") {
                $ip = $Matches[1]
                $name = $Matches[2]
                $status = $Matches[3]
                
                if ($status -eq "online" -or $status -eq "idle") {
                    Write-StatusLine -Label "  $name" -Status "[OK] $status ($ip)" -Color $Colors.Success
                }
                else {
                    Write-StatusLine -Label "  $name" -Status "[X] $status ($ip)" -Color $Colors.Error
                }
            }
        }
    }
    else {
        Write-StatusLine -Label "  Status" -Status "[X] Kunne ikke hente" -Color $Colors.Error
    }
    
    Write-Host "------------------------------------------------------------" -ForegroundColor $Colors.Header
}

function Show-Actions {
    Write-Host ""
    Write-Host "RASKE HANDLINGER" -ForegroundColor $Colors.Header
    Write-Host "------------------------------------------------------------" -ForegroundColor $Colors.Header
    Write-Host "  1. Apne AnythingLLM (lokal)     http://192.168.1.200:3001" -ForegroundColor $Colors.Info
    Write-Host "  2. Apne AnythingLLM (Tailscale) http://100.108.91.44:3001" -ForegroundColor $Colors.Info
    Write-Host "  3. Apne Z: Disk                 Z:\" -ForegroundColor $Colors.Info
    Write-Host "  4. Koble til Z: (hvis frakoblet)" -ForegroundColor $Colors.Info
    Write-Host ""
    Write-Host "  Trykk Ctrl+C for a avslutte" -ForegroundColor $Colors.Warning
    Write-Host "------------------------------------------------------------" -ForegroundColor $Colors.Header
}

function Start-ZDriveConnection {
    Write-Host "Kobler til Z: disk..." -ForegroundColor $Colors.Info
    try {
        net use Z: \\192.168.1.200\Bygg_Arkiv /persistent:yes 2>&1 | Out-Null
        Write-Host "[OK] Z: disk tilkoblet!" -ForegroundColor $Colors.Success
    }
    catch {
        Write-Host "[X] Kunne ikke koble til Z: $_" -ForegroundColor $Colors.Error
    }
}

# ==================== HOVEDPROGRAM ====================

if ($StartThreadripperServices) {
    Write-Host "Starter tjenester pa Threadripper..." -ForegroundColor $Colors.Info
    Write-Host "MERK: Dette krever at du kjorer skriptet pa Threadripper!" -ForegroundColor $Colors.Warning
    Write-Host ""
    Write-Host "Kopier disse filene til Threadripper:" -ForegroundColor $Colors.Info
    Write-Host "  1. Threadripper_AnythingLLM_Autostart.ps1 -> C:\Tools\" -ForegroundColor $Colors.Info
    Write-Host "  2. Start_AnythingLLM_Silently.bat -> Skrivebord eller Startup" -ForegroundColor $Colors.Info
    exit 0
}

if ($Watch) {
    # Kontinuerlig overvaking
    while ($true) {
        Show-Header
        Show-ThreadripperStatus
        Show-LenovoStatus
        Show-ZDriveStatus
        Show-TailscaleStatus
        Show-Actions
        
        Write-Host ""
        Write-Host "Oppdaterer om $WatchInterval sekunder... (Ctrl+C for a avslutte)" -ForegroundColor $Colors.Info
        Start-Sleep -Seconds $WatchInterval
    }
}
else {
    # Enkel sjekk
    Show-Header
    Show-ThreadripperStatus
    Show-LenovoStatus
    Show-ZDriveStatus
    Show-TailscaleStatus
    Show-Actions
}
