#Requires -Version 5.1
<#
.SYNOPSIS
    Setter opp SSH-nøkkel for passordfri innlogging til Lenovo
    fra Acer (Windows) og WSL/Linux
#>

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  SSH-NOKKEL SETUP FOR LENOVO" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""

# Sjekk om OpenSSH er installert
$sshPath = (Get-Command ssh -ErrorAction SilentlyContinue).Source
if (-not $sshPath) {
    Write-Host "[FEIL] OpenSSH ikke funnet!" -ForegroundColor Red
    Write-Host "Installer OpenSSH via: Innstillinger -> Apper -> Valgfrie funksjoner" -ForegroundColor Yellow
    exit 1
}

Write-Host "[OK] OpenSSH funnet: $sshPath" -ForegroundColor Green

# Opprett .ssh-mappe hvis den ikke finnes
$sshDir = "$env:USERPROFILE\.ssh"
if (!(Test-Path $sshDir)) {
    New-Item -ItemType Directory -Path $sshDir -Force | Out-Null
    Write-Host "[OK] Opprettet .ssh-mappe" -ForegroundColor Green
}

# Sjekk om nøkkel allerede finnes
$keyPath = "$sshDir\id_ed25519_lenovo"
if (Test-Path $keyPath) {
    Write-Host "[INFO] SSH-nokkel finnes allerede: $keyPath" -ForegroundColor Yellow
    $response = Read-Host "Vil du lage ny nokkel? (j/n)"
    if ($response -ne "j") {
        Write-Host "Bruker eksisterende nokkel..." -ForegroundColor Cyan
    }
    else {
        Remove-Item $keyPath -Force
        Remove-Item "$keyPath.pub" -Force -ErrorAction SilentlyContinue
    }
}

# Generer ny nøkkel hvis nødvendig
if (!(Test-Path $keyPath)) {
    Write-Host "[INFO] Genererer ny SSH-nokkel (ED25519)..." -ForegroundColor Cyan
    ssh-keygen -t ed25519 -f $keyPath -N '""' -C "acer-to-lenovo"
    Write-Host "[OK] Nokkel generert!" -ForegroundColor Green
}

# Kopier offentlig nokkel til Lenovo
Write-Host ""
Write-Host "============================================================" -ForegroundColor Yellow
Write-Host "  KOPIERER NOKKEL TIL LENOVO" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Yellow
Write-Host ""
Write-Host "Du vil bli bedt om passord til Lenovo (emil@100.108.91.44)" -ForegroundColor Cyan
Write-Host "Dette er SISTE gang du trenger a skrive passord!" -ForegroundColor Green
Write-Host ""

$publicKey = Get-Content "$keyPath.pub"

# Bruk ssh-copy-id hvis tilgjengelig, ellers manuell metode
try {
    # Forsøk a legge til nokkel via SSH
    $command = "echo '$publicKey' | ssh emil@100.108.91.44 'mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys'"
    Invoke-Expression $command
    
    Write-Host ""
    Write-Host "[OK] Nokkel kopiert til Lenovo!" -ForegroundColor Green
}
catch {
    Write-Host "[FEIL] Kunne ikke kopiere nokkel automatisk" -ForegroundColor Red
    Write-Host "Manuell metode:" -ForegroundColor Yellow
    Write-Host "1. ssh emil@100.108.91.44" -ForegroundColor Cyan
    Write-Host "2. mkdir -p ~/.ssh && chmod 700 ~/.ssh" -ForegroundColor Cyan
    Write-Host "3. Legg til denne i ~/.ssh/authorized_keys:" -ForegroundColor Cyan
    Write-Host $publicKey -ForegroundColor White
}

# Opprett SSH-config for enkel tilgang
$configPath = "$sshDir\config"
$configEntry = @"

# Lenovo Sandkasse ( automatisk oppsatt )
Host lenovo
    HostName 100.108.91.44
    User emil
    IdentityFile ~/.ssh/id_ed25519_lenovo
    IdentitiesOnly yes

# Lenovo via lokal IP
Host lenovo-local
    HostName 192.168.1.120
    User emil
    IdentityFile ~/.ssh/id_ed25519_lenovo
    IdentitiesOnly yes

"@

if (Test-Path $configPath) {
    $existing = Get-Content $configPath -Raw
    if ($existing -notcontains "Host lenovo") {
        Add-Content -Path $configPath -Value $configEntry
        Write-Host "[OK] SSH-config oppdatert" -ForegroundColor Green
    }
}
else {
    $configEntry | Out-File -FilePath $configPath -Encoding utf8
    Write-Host "[OK] SSH-config opprettet" -ForegroundColor Green
}

# Test tilkobling
Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  TESTER TILKOBLING..." -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""

Write-Host "Prover a koble til med ssh lenovo..." -ForegroundColor Cyan
Write-Host "(Hvis alt er OK, skal du logge inn UTEN passord)" -ForegroundColor Green
Write-Host ""

Start-Process powershell.exe -ArgumentList "-NoExit -Command ssh lenovo" -Wait

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  SETUP FULLFORT!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Fremover kan du bruke:" -ForegroundColor Cyan
Write-Host "  ssh lenovo         (koble til Lenovo)" -ForegroundColor White
Write-Host "  ssh lenovo-local   (hvis pa samme nettverk)" -ForegroundColor White
Write-Host ""
Write-Host "Ingen passord behoves lenger!" -ForegroundColor Green
Write-Host ""

Read-Host "Trykk ENTER for a avslutte"
