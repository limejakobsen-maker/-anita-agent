@echo off
chcp 65001 >nul
title Kopier til Lenovo Sandkasse
cd /d "%~dp0"

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                                                                  ║
echo ║   🚀 KOPIERER OPTIMAL SANDKASSE TIL LENOVO                      ║
echo ║                                                                  ║
echo ║   Denne filen kopierer automatisk alle nødvendige filer         ║
echo ║   til Lenovo (100.108.91.44) via SSH/SCP                        ║
echo ║                                                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

:: Sjekk om PowerShell er tilgjengelig
where powershell >nul 2>&1
if errorlevel 1 (
    echo ❌ FEIL: PowerShell ikke funnet!
    pause
    exit /b 1
)

echo 📦 Starter kopiering...
echo.

:: Kjør PowerShell-script
powershell -ExecutionPolicy Bypass -File "kopier_til_lenovo.ps1"

if errorlevel 1 (
    echo.
    echo ❌ Noe gikk galt. Sjekk feilmeldingen over.
    pause
    exit /b 1
)

echo.
echo ✅ Fullført!
echo.
pause
