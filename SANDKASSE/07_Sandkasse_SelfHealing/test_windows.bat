@echo off
chcp 65001 >nul
title Self-Healing System - Windows Test
cls

echo ========================================
echo   ?? SELVHELBREDENDE SYSTEM - WINDOWS
echo ========================================
echo.

:: Sjekk Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ? Python ikke funnet!
    echo    Installer Python 3.10 eller nyere
    pause
    exit /b 1
)

echo ? Python funnet
echo.

:: Installer avhengigheter
echo ?? Installerer avhengigheter...
pip install pyyaml requests -q

:: Kj?r systemet
echo.
echo ?? Starter systemet...
echo ========================================
echo.

python main.py

echo.
echo ========================================
echo ?? Se logs/errors.log for feildetaljer
echo ?? Se AGENTS.md for l?rdommer
echo.
pause
