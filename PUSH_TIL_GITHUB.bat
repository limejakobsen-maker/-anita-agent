@echo off
chcp 65001 >nul
title Push til GitHub - Anita Agent
cls

echo ========================================
echo    PUSH TIL GITHUB - ANITA AGENT
echo ========================================
echo.

:: Gaa til prosjektmappen
cd /d "C:\Users\Emil\Desktop\PROSJEKTMAPPE AI"

echo [1/5] Sjekker om Git er installert...
git --version >nul 2>&1
if errorlevel 1 (
    echo FEIL: Git er ikke installert!
    echo Last ned fra: https://git-scm.com/download/win
    pause
    exit /b 1
)
echo OK: Git er installert
echo.

echo [2/5] Initialiserer Git repository...
if not exist .git (
    git init
    echo OK: Nytt repo opprettet
) else (
    echo OK: Repo finnes allerede
)
echo.

echo [3/5] Legger til filer...
git add .
echo OK: Filer lagt til
echo.

echo [4/5] Committer endringer...
git commit -m "ci: Implement complete CI/CD pipeline"
if errorlevel 1 (
    echo Ingen endringer aa commite ^(allerede oppdatert^)
) else (
    echo OK: Committed
echo.
)

echo [5/5] Sjekker GitHub remote...
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo.
    echo ========================================
    echo    INGEN GITHUB REMOTE FUNNET!
    echo ========================================
    echo.
    echo Du maa koble dette repoet til GitHub.
    echo.
    set /p github_user="Skriv ditt GitHub brukernavn: "
    set /p repo_name="Skriv repository navn (f.eks. anita-agent): "
    echo.
    echo Legger til remote...
    git remote add origin https://github.com/%github_user%/%repo_name%.git
    echo.
    echo VIKTIG: Pass paa at repoet finnes paa GitHub!
    echo Hvis ikke, opprett det her: https://github.com/new
    echo.
    pause
)

echo Pusher til GitHub...
git push -u origin main 2>nul
if errorlevel 1 (
    git push -u origin master 2>nul
    if errorlevel 1 (
        echo.
        echo FEIL: Push feilet!
        echo Sjekk at du har riktig brukernavn/repo
        echo og at du har skrivetilgang.
        pause
        exit /b 1
    ) else (
        echo OK: Pushed til master branch
    )
) else (
    echo OK: Pushed til main branch
)

echo.
echo ========================================
echo    ✅ FULLFORT!
echo ========================================
echo.
echo Din kode er na pushet til GitHub!
echo.
echo Gaa til GitHub Actions for aa se CI/CD pipelinen:
echo.

:: Hent brukernavn og repo fra remote
for /f "tokens=*" %%a in ('git remote get-url origin 2^>nul') do set remote_url=%%a

:: Ekstraher brukernavn og repo fra URL
:: Stotter bade HTTPS og SSH format
setlocal enabledelayedexpansion
set url=%remote_url%
set url=!url:git@github.com:=https://github.com/!
set url=!url:.git=/!

echo !url!actions
echo.
echo Kopier URLen over og aapne i nettleseren.
echo.

pause
