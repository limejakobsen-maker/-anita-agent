@echo off
title Self-Healing Sandkasse - GUI
cls

echo ========================================
echo   ?? Self-Healing Sandkasse
echo   (Del av PROSJEKTMAPPE AI)
echo ========================================
echo.

:: Finn PROSJEKTMAPPE AI-stien
set "BASEPATH=C:\Users\limej\OneDrive\Desktop\PROSJEKTMAPPE AI\07_Sandkasse_SelfHealing"

cd /d "%BASEPATH%"
if errorlevel 1 (
    echo FEIL: Finner ikke %BASEPATH%
    pause
    exit /b 1
)

echo [OK] Plassering: %CD%
echo.

:: Sjekk Python
python --version >nul 2>&1
if errorlevel 1 (
    echo FEIL: Python ikke funnet!
    pause
    exit /b 1
)

echo [OK] Python funnet
echo.

:: Meny
echo Velg visning:
echo   [1] Mini Viewer (kompakt, 600x450)
echo   [2] Full Viewer (stor, 900x650)
echo.

set /p choice="Valg (1/2): "

if "%choice%"=="1" (
    echo.
    echo Starter Mini Viewer...
    python mini_viewer.py
) else if "%choice%"=="2" (
    echo.
    echo Starter Full Viewer...
    python code_viewer_gui.py
) else (
    echo.
    echo Ugyldig valg, starter Mini Viewer...
    python mini_viewer.py
)

echo.
echo [Ferdig] Vinduet er lukket.
pause
