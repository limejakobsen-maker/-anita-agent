@echo off
chcp 65001 >nul
title Kopier til Lenovo - Automatisk
cd /d "%~dp0"

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                                                                  ║
echo ║   🚀 AUTO-KOPIER TIL LENOVO                                      ║
echo ║                                                                  ║
echo ║   Denne filen vil:                                               ║
echo ║   1. Starte Python-server på Acer (port 8000)                   ║
echo ║   2. Kople til Lenovo via SSH (100.108.91.44)                   ║
echo ║   3. Laste ned alle filer automatisk                            ║
echo ║   4. Installere med install.sh                                  ║
echo ║   5. Starte serveren på Lenovo                                  ║
echo ║                                                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo 📍 Fra: C:\Users\limej\...\for_lenovo\
echo 📍 Til: emil@100.108.91.44:~/self_healing_system/
echo.

:: Sjekk at vi er i riktig mappe
if not exist "for_lenovo\sandkasse_protokoll.py" (
    echo ❌ FEIL: Fant ikke filene i for_lenovo\
    echo    Sjekk at du kjører denne filen fra SANDKASSE\07_Sandkasse_SelfHealing\
    pause
    exit /b 1
)

echo ✅ Filene funnet!
echo.

:: Sjekk at Python er tilgjengelig
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ FEIL: Python ikke funnet!
    echo    Installer Python fra python.org
    pause
    exit /b 1
)

echo ✅ Python fungerer!
echo.

:: Sjekk at SSH er tilgjengelig
ssh -V >nul 2>&1
if errorlevel 1 (
    echo ❌ FEIL: SSH ikke funnet!
    echo    Installerer OpenSSH...
    dism /online /Add-Capability /CapabilityName:OpenSSH.Client~~~~0.0.1.0
)

echo ✅ SSH fungerer!
echo.

echo 🔍 Sjekker tilkobling til Lenovo...
ping -n 1 -w 3000 100.108.91.44 >nul 2>&1
if errorlevel 1 (
    echo ⚠️  ADVARSEL: Kan ikke pinge Lenovo
    echo    Sjekk at:
    echo    • Lenovo er påslått
    echo    • Tailscale kjører på begge maskiner
    echo.
    set /p fortsett="Vil du prøve likevel? (j/n): "
    if /I not "%fortsett%"=="j" exit /b 1
)

echo ✅ Lenovo er tilgjengelig!
echo.

echo ╔══════════════════════════════════════════════════════════════════╗
echo ║  STEG 1: Starter Python-server på Acer...                        ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

:: Start Python-server i bakgrunnen
start "Python Server for Lenovo" cmd /c "cd /d "%~dp0for_lenovo" && echo Server starter på port 8000... && python -m http.server 8000"

:: Vent på at server starter
echo ⏳ Venter 3 sekunder på at server starter...
timeout /t 3 /nobreak >nul

echo ✅ Python-server kjører!
echo.

echo ╔══════════════════════════════════════════════════════════════════╗
echo ║  STEG 2: Kopierer filer til Lenovo...                            ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

:: Lag midlertidig script for Lenovo
set "TEMP_SCRIPT=%TEMP%\lenovo_kopier_%RANDOM%.sh"
(
echo #!/bin/bash
echo echo "🔗 Koblet til Lenovo!"
echo echo "📁 Oppretter mappe..."
echo mkdir -p ~/self_healing_system
echo cd ~/self_healing_system
echo.
echo echo "📥 Laster ned filer fra Acer..."
echo curl -s -O http://100.114.112.61:8000/sandkasse_protokoll.py ^&^& echo "✅ sandkasse_protokoll.py"
echo curl -s -O http://100.114.112.61:8000/sandkasse_protokoll_part2.py ^&^& echo "✅ sandkasse_protokoll_part2.py"
echo curl -s -O http://100.114.112.61:8000/protokoll_server.py ^&^& echo "✅ protokoll_server.py"
echo curl -s -O http://100.114.112.61:8000/install.sh ^&^& echo "✅ install.sh"
echo curl -s -O http://100.114.112.61:8000/self_healing_wrapper.py ^&^& echo "✅ self_healing_wrapper.py"
echo curl -s -O http://100.114.112.61:8000/error_handler.py ^&^& echo "✅ error_handler.py"
echo curl -s -O http://100.114.112.61:8000/ai_fixer.py ^&^& echo "✅ ai_fixer.py"
echo.
echo echo "📋 Verifiserer filer..."
echo ls -la ~/self_healing_system/
echo.
echo echo "🔧 Gjør install.sh kjørbar..."
echo chmod +x install.sh
echo.
echo echo "╔══════════════════════════════════════════════════════════════════╗"
echo echo "║  ✅ KOPIERING FULLFØRT!                                          ║"
echo echo "╚══════════════════════════════════════════════════════════════════╝"
echo.
echo echo "📋 Neste steg:"
echo echo "   1. Kjør: cd ~/self_healing_system"
echo echo "   2. Kjør: bash install.sh"
echo echo "   3. Kjør: python3 protokoll_server.py"
) > "%TEMP_SCRIPT%"

:: Kjør script på Lenovo via SSH
echo 🔐 Kobler til Lenovo (100.108.91.44)...
echo    Du kan bli spurt om passord for emil@100.108.91.44
echo.

ssh emil@100.108.91.44 < "%TEMP_SCRIPT%"

if errorlevel 1 (
    echo.
    echo ❌ FEIL: SSH-tilkobling feilet!
    echo    Sjekk:
    echo    • Passord er riktig
    echo    • Lenovo er på
    echo    • SSH-server kjører på Lenovo
    echo.
    echo 🛑 Stopper Python-server...
    taskkill /FI "WINDOWTITLE eq Python Server for Lenovo" /F >nul 2>&1
    del "%TEMP_SCRIPT%" 2>nul
    pause
    exit /b 1
)

del "%TEMP_SCRIPT%" 2>nul

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║  STEG 3: Rydde opp...                                            ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

echo 🛑 Stopper Python-server på Acer...
taskkill /FI "WINDOWTITLE eq Python Server for Lenovo" /F >nul 2>&1
echo ✅ Server stoppet!

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║  ✅ ALLE FILER KOPIERT!                                          ║
echo ╠══════════════════════════════════════════════════════════════════╣
echo ║                                                                  ║
echo ║  📋 NESTE STEG PÅ LENOVO:                                        ║
echo ║                                                                  ║
echo ║  1. Koble til Lenovo:                                            ║
echo ║     ssh emil@100.108.91.44                                       ║
echo ║                                                                  ║
echo ║  2. Installer systemet:                                          ║
echo ║     cd ~/self_healing_system                                     ║
echo ║     bash install.sh                                              ║
echo ║                                                                  ║
echo ║  3. Start serveren:                                              ║
echo ║     python3 protokoll_server.py                                  ║
echo ║                                                                  ║
echo ║  📋 PÅ ACER:                                                     ║
echo ║     Dobbeltklikk: "Sandkasse Monitor.lnk"                        ║
echo ║                                                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
pause
