@echo off
chcp 65001 >nul
echo ==========================================
echo LENOVO KONTROLLPANEL (Fra Acer)
echo ==========================================
echo.
echo 1. [SETT OPP] Lenovo (Installer SSH + Server)
echo 2. [KOBL TIL] Lenovo via SSH
echo 3. [SJEKK] Er Lenovo online?
echo 4. [START] Sandkasse Monitor (GUI)
echo 5. [AVSLUTT]
echo.
echo Lenovo IP: 100.108.91.44
echo Tailscale: tailscale status
echo ==========================================
echo.

set /p valg="Velg (1-5): "

if "%valg%"=="1" goto setup
if "%valg%"=="2" goto ssh
if "%valg%"=="3" goto ping
if "%valg%"=="4" goto monitor
if "%valg%"=="5" goto exit

echo Ugyldig valg
goto end

:setup
echo.
echo === SETUP LENOVO ===
echo 1. Ga til Lenovo
echo 2. Apne terminal
echo 3. Kjor denne kommandoen:
echo.
echo    curl http://100.114.112.61:8000/setup_lenovo_ssh.sh ^| bash
echo.
echo 4. Vent til den sier "SSH er aktivert!"
echo 5. Deretter velg "2" i dette menyen for SSH
echo.
pause
goto end

:ssh
echo.
echo === KOBLER TIL LENOVO ===
ssh emil@100.108.91.44
goto end

:ping
echo.
echo === SJEKKER LENOVO ===
ping -n 2 100.108.91.44
echo.
echo Sjekker SSH-port...
timeout /t 1 >nul
echo.
echo Hvis du ser "Reply from" over, er Lenovo online.
echo Hvis du vil sjekke SSH, kjor: ssh emil@100.108.91.44
echo.
pause
goto end

:monitor
echo.
echo === STARTER SANDKASSE MONITOR ===
cd /d "C:\Users\limej\OneDrive\Desktop\SANDKASSE\07_Sandkasse_SelfHealing"
python protokoll_monitor.py
pause
goto end

:exit
exit

:end
echo.
echo Trykk en tast for aa lukke...
pause >nul
