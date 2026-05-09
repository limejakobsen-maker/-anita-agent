@echo off
chcp 65001 >nul
echo ==========================================
echo    GIT PUSH - MANUAL COMMANDS
echo ==========================================
echo.

:: Gå til riktig mappe
cd /d "C:\Users\Emil\Desktop\PROSJEKTMAPPE AI"

echo [1/5] Sjekker git status...
git status
echo.

echo [2/5] Legger til filer...
git add .
echo ✅ Filer lagt til
echo.

echo [3/5] Committer endringer...
git commit -m "ci: Implement complete CI/CD pipeline"
echo ✅ Committed
echo.

echo [4/5] Pusher til GitHub...
git push -u origin main
echo ✅ Push fullført!
echo.

echo [5/5] Viser GitHub URL...
echo.
echo ==========================================
echo    ✅ FULLFØRT!
echo ==========================================
echo.
echo Gå til GitHub Actions for å se pipelinen:
echo https://github.com/emil/anita-agent/actions
echo.
echo (Bytt ut 'emil' med ditt GitHub brukernavn)
echo.

pause
