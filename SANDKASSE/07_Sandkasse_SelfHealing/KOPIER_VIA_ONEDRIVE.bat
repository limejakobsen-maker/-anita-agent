@echo off
chcp 65001 >nul
title Kopier via OneDrive (Alternativ metode)
cd /d "%~dp0"

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                                                                  ║
echo ║   📤 KOPIER VIA ONEDRIVE (Alternativ)                           ║
echo ║                                                                  ║
echo ║   Hvis SSH ikke fungerer, kan du bruke OneDrive:                ║
echo ║                                                                  ║
echo ║   1. Filene kopieres automatisk til OneDrive                    ║
echo ║   2. Du henter dem på Lenovo fra nettleser/OneDrive             ║
echo ║                                                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

set SOURCE=C:\Users\limej\OneDrive\Desktop\SANDKASSE\07_Sandkasse_SelfHealing\for_lenovo
set DEST=%USERPROFILE%\OneDrive\Desktop\TIL_LENOVO

echo 📁 Kilde: %SOURCE%
echo 🎯 Mål:  %DEST%
echo.

:: Opprett målmappe
if not exist "%DEST%" (
    mkdir "%DEST%"
    echo ✅ Opprettet mappe: %DEST%
) else (
    echo ℹ️  Mappen finnes allerede
)

echo.
echo 📋 Kopierer filer...
echo.

:: Kopier filer
xcopy /Y /I "%SOURCE%\*.py" "%DEST%\" 2>nul
xcopy /Y /I "%SOURCE%\*.sh" "%DEST%\" 2>nul
xcopy /Y /I "%SOURCE%\*.md" "%DEST%\" 2>nul

echo ✅ Filer kopiert til OneDrive!
echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║  📋 INSTRUKSJONER FOR LENOVO:                                    ║
echo ╠══════════════════════════════════════════════════════════════════╣
echo ║                                                                  ║
echo ║  1. Åpne nettleser på Lenovo                                     ║
echo ║  2. Gå til: onedrive.live.com                                    ║
echo ║  3. Logg inn med din Microsoft-konto                             ║
echo ║  4. Gå til: Desktop ▶ TIL_LENOVO                                 ║
echo ║  5. Last ned alle filer                                          ║
echo ║  6. På Lenovo, kjør:                                             ║
echo ║                                                                  ║
echo ║     mkdir -p ~/self_healing_system                               ║
echo ║     # Flytt nedlastede filer hit                                 ║
echo ║     cd ~/self_healing_system                                     ║
echo ║     bash install.sh                                              ║
echo ║                                                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
pause
