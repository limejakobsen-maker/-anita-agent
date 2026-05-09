@echo off
:: Auto-start script for Self-Healing System
:: Kan legges i Oppgaveplanlegger for automatisk kj?ring

cd /d "C:\Users\limej\OneDrive\Desktop\self_healing_system"

:: Kj?r med logging
python main.py >> logs\autorun.log 2>&1

:: Send varsel ved kritiske feil (valgfritt)
if %errorlevel% neq 0 (
    echo %date% %time% - Kritisk feil oppstod >> logs\critical.log
    
    # Her kan du legge til e-post-varsel eller lignende
    # powershell -Command "Send-MailMessage -To 'emil@example.com' -From 'system@lenovo' -Subject 'Kritisk feil' -Body 'Sjekk logs/critical.log'"
)
