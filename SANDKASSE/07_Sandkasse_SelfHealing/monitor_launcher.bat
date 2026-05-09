@echo off
chcp 65001 >nul
title [ACER] Sandkasse Protokoll Monitor
cd /d "%~dp0"

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                                                           ║
echo ║   [ACER] → [LENOVO] Sandkasse Protokoll Monitor           ║
echo ║                                                           ║
echo ║   Starter overvåkingsvindu...                             ║
echo ║                                                           ║
echo ║   Lenovo:  100.108.91.44 (Tailscale)                      ║
echo ║   Port:    8765                                           ║
echo ║                                                           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

:: Sjekk Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [FEIL] Python ikke funnet! Installer Python 3.x
    pause
    exit /b 1
)

:: Sjekk/installer websockets
echo [INFO] Sjekker avhengigheter...
python -c "import websockets" 2>nul
if errorlevel 1 (
    echo [INFO] Installerer websockets...
    pip install websockets
)

:: Start monitor
echo [INFO] Starter monitor...
echo.
python protokoll_monitor.py

if errorlevel 1 (
    echo.
    echo [FEIL] Noe gikk galt. Sjekk feilmeldingen over.
    pause
)
