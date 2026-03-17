# INSTALLASJONSINSTRUKSJONER - Ny Sandkasse-Protokoll

**Dato:** 05.03.2026  
**Versjon:** 3.1 - Threadripper Edition  
**Mål:** Integrere sandkasse_protokoll med Lenovos Ollama

---

## 📋 OVERSIKT

Du skal erstatte den gamle `enkel_server.py` på Threadripper med nye filer som:
1. Har full 6-fase protokoll (INIT → DISCUSS → PLAN → EXECUTE → VALIDATE → DEPLOY)
2. Bruker Lenovos Ollama (100.108.91.44:11434) for AI-generering
3. Fungerer med eksisterende `enkel_monitor.py` på Acer

---

## 🗂️ FILER DU SKAL KOPIERE

Fra Acer (`C:\Users\limej\OneDrive\Desktop\PROSJEKTMAPPE AI\`):
1. `sandkasse_protokoll_NY.py` → Threadripper: `sandkasse_protokoll.py`
2. `enkel_server_NY.py` → Threadripper: `enkel_server.py`

---

## 🚀 STEG-FOR-STEG INSTALLASJON

### STEG 1: Forberedelser på Threadripper (Gjør dette FØRST!)

1. **Åpne RDP til Threadripper:**
   ```
   mstsc /v:100.103.79.103
   ```

2. **Stopp eksisterende server:**
   - Finn vinduet hvor `enkel_server.py` kjører
   - Trykk **Ctrl+C**
   - Eller åpne Task Manager → finn `python.exe` → Avslutt oppgave

3. **Verifiser at serveren er stoppet:**
   ```powershell
   # På Threadripper, kjør:
   netstat -an | findstr 8765
   # Skal IKKE vise noe (hvis den viser "LISTENING", vent litt og prøv igjen)
   ```

---

### STEG 2: Sikkerhetskopi (VIKTIG!)

**På Threadripper, i PowerShell:**
```powershell
cd C:\AI_System\protokoll

# Sjekk hva som finnes
ls

# Lag backup
copy enkel_server.py enkel_server.py.BACKUP.20250305

# Hvis sandkasse_protokoll.py finnes, backup den også
if (Test-Path sandkasse_protokoll.py) {
    copy sandkasse_protokoll.py sandkasse_protokoll.py.BACKUP.20250305
}

# Verifiser backup
ls *.BACKUP.*
```

---

### STEG 3: Kopier nye filer

**Alternativ A: Via OneDrive (hvis synkronisert)**
```powershell
# På Threadripper
copy "C:\Users\dittbrukernavn\OneDrive\Desktop\PROSJEKTMAPPE AI\sandkasse_protokoll_NY.py" C:\AI_System\protokoll\sandkasse_protokoll.py
copy "C:\Users\dittbrukernavn\OneDrive\Desktop\PROSJEKTMAPPE AI\enkel_server_NY.py" C:\AI_System\protokoll\enkel_server.py
```

**Alternativ B: Via USB**
1. Kopier filene fra Acer til USB
2. Sett USB inn i Threadripper
3. Kopier filer til `C:\AI_System\protokoll\`

**Alternativ C: Via nettverksdeling**
```powershell
# Hvis du har satt opp deling
copy "\\acer-ip\share\sandkasse_protokoll_NY.py" C:\AI_System\protokoll\sandkasse_protokoll.py
```

---

### STEG 4: Verifiser filene

**På Threadripper:**
```powershell
cd C:\AI_System\protokoll

# Sjekk at filene finnes
ls sandkasse_protokoll.py
ls enkel_server.py

# Sjekk filstørrelse (skal være ~27KB og ~8KB)
ls -l sandkasse_protokoll.py, enkel_server.py
```

---

### STEG 5: Installer avhengigheter

**På Threadripper, i PowerShell som Administrator:**
```powershell
# Sjekk om requests er installert
python -c "import requests; print('OK')"

# Hvis den feiler, installer:
pip install requests
```

---

### STEG 6: Test protokollen (valgfritt, men anbefalt)

**På Threadripper:**
```powershell
cd C:\AI_System\protokoll

# Test at protokollen laster
python -c "from sandkasse_protokoll import SandkasseProtokoll; print('Protokoll OK')"

# Test tilkobling til Lenovo
python -c "from sandkasse_protokoll import LenovoOllamaClient; c = LenovoOllamaClient(); print('Lenovo tilkoblet:', c.is_available())"
```

**Hvis dette fungerer, fortsett til Steg 7!**

---

### STEG 7: Start serveren

**På Threadripper:**
```powershell
cd C:\AI_System\protokoll
python enkel_server.py
```

Du skal se:
```
✅ sandkasse_protokoll.py funnet og lastet

╔═══════════════════════════════════════════════════════════╗
║  ENKEL HTTP SERVER v2.0 - Threadripper                     ║
║                                                            ║
║  Lytter på: http://0.0.0.0:8765                          ║
...
```

---

### STEG 8: Test fra Acer

**På Acer, åpne ny PowerShell:**
```powershell
# Test at serveren svarer
Invoke-WebRequest -Uri "http://100.103.79.103:8765/health" -UseBasicParsing

# Test status
Invoke-WebRequest -Uri "http://100.103.79.103:8765/status" -UseBasicParsing
```

**Start monitoren:**
```powershell
cd C:\Users\limej\Desktop
python enkel_monitor.py
```

---

### STEG 9: Test et prosjekt (valgfritt)

**Fra Acer, send test-prosjekt:**
```powershell
$body = @{
    project = "TestProsjekt"
    description = "Et enkelt Python-program som skriver 'Hei Verden'"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://100.103.79.103:8765/start" -Method POST -Body $body -ContentType "application/json"
```

---

## 🐛 FEILSØKING

### Problem: "ModuleNotFoundError: No module named 'requests'"
**Løsning:**
```powershell
pip install requests
```

### Problem: "Lenovo Ollama er IKKE tilgjengelig"
**Sjekk:**
1. Er Lenovo på? (ping 100.108.91.44)
2. Kjører Ollama på Lenovo? (`systemctl status ollama` på Lenovo)
3. Er port 11434 åpen? (`curl http://100.108.91.44:11434/api/tags`)

### Problem: "Port 8765 er i bruk"
**Løsning:**
```powershell
# Finn prosess som bruker porten
netstat -ano | findstr 8765

# Drepe prosess (bytt ut <PID> med faktisk nummer)
taskkill /F /PID <PID>
```

### Problem: Serveren starter ikke
**Løsning:**
```powershell
# Sjekk Python-versjon
python --version  # Skal være 3.8+

# Kjør med debug
python enkel_server.py 2>&1
```

---

## 🔄 ROLLBACK (hvis noe går galt)

Hvis nye filene ikke fungerer:

```powershell
cd C:\AI_System\protokoll

# Stopp server (Ctrl+C)

# Gjenopprett gamle filer
copy enkel_server.py.BACKUP.20250305 enkel_server.py

# Hvis du hadde sandkasse_protokoll.py før:
copy sandkasse_protokoll.py.BACKUP.20250305 sandkasse_protokoll.py

# Start gammel server
python enkel_server.py
```

---

## ✅ SJEKKLISTE

- [ ] Server stoppet på Threadripper
- [ ] Backup opprettet
- [ ] Nye filer kopiert til `C:\AI_System\protokoll\`
- [ ] `requests` modul installert (`pip install requests`)
- [ ] Protokollen laster uten feil
- [ ] Server starter uten feil
- [ ] Server svarer på `http://100.103.79.103:8765/health`
- [ ] Monitor på Acer viser status
- [ ] Test-prosjekt kan startes

---

**Spørsmål? Stopp hvis noe er uklart!** 🛡️
