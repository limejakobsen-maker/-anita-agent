# ðŸš€ AnythingLLM Autostart - Veiledning

Denne guiden forklarer hvordan du setter opp automatisk oppstart av AnythingLLM pÃ¥ Threadripper.

## ðŸ“ Filer i denne mappen

| Fil | Beskrivelse | Hvor den skal ligge |
|-----|-------------|---------------------|
| `Threadripper_AnythingLLM_Autostart.ps1` | Hovedskript for autostart | **Threadripper:** `C:\Tools\` |
| `Start_AnythingLLM_Silently.bat` | Enkel batch-wrapper | **Threadripper:** Startup-mappe |
| `SETUP_AUTOSTART_Threadripper.ps1` | Installasjonsskript | KjÃ¸res pÃ¥ Threadripper |
| `Rigg_Monitor.ps1` | OvervÃ¥king fra Acer | **Acer:** KjÃ¸r herfra |

---

## ðŸ”§ Oppsett pÃ¥ Threadripper (STEG 1)

### Alternativ A: Automatisk installasjon (Anbefalt)

1. Kopier disse filene til Threadripper (f.eks. pÃ¥ USB):
   - `Threadripper_AnythingLLM_Autostart.ps1`
   - `SETUP_AUTOSTART_Threadripper.ps1`

2. PÃ¥ **Threadripper**, hÃ¸yreklikk PowerShell â†’ "KjÃ¸r som Administrator"

3. KjÃ¸r:
   ```powershell
   cd C:\Users\[bruker]\Desktop  # eller hvor du la filene
   .\SETUP_AUTOSTART_Threadripper.ps1
   ```

4. FÃ¸lg instruksjonene pÃ¥ skjermen

### Alternativ B: Manuell installasjon

1. **Opprett mapper** pÃ¥ Threadripper:
   ```
   C:\Tools\
   C:\Logs\
   ```

2. **Kopier filen**:
   - `Threadripper_AnythingLLM_Autostart.ps1` â†’ `C:\Tools\`

3. **Ã…pne Oppgaveplanlegger** (Task Scheduler):
   - Trykk `Win + R`, skriv `taskschd.msc`, trykk Enter

4. **Opprett ny oppgave**:
   - Navn: `AnythingLLM_Autostart`
   - Trigger: "Ved pÃ¥logging" (At logon)
   - Handling: Start et program
   - Program: `powershell.exe`
   - Argument: `-ExecutionPolicy Bypass -WindowStyle Hidden -File "C:\Tools\Threadripper_AnythingLLM_Autostart.ps1"`
   - Huk av "KjÃ¸r med hÃ¸yeste privilegier"

---

## ðŸ–¥ï¸ OvervÃ¥king fra Acer (STEG 2)

NÃ¥r oppsettet er ferdig pÃ¥ Threadripper, kan du overvÃ¥ke alt fra Acer:

### Enkel statussjekk:
```powershell
cd "C:\Users\limej\OneDrive\Desktop\PROSJEKTMAPPE AI"
.\Rigg_Monitor.ps1
```

### Kontinuerlig overvÃ¥king:
```powershell
.\Rigg_Monitor.ps1 -Watch
```

Dette viser:
- âœ… Om Threadripper er online
- âœ… Om AnythingLLM kjÃ¸rer (port 3001)
- âœ… Om Ollama kjÃ¸rer (port 11434)
- âœ… Om Z: disk er tilkoblet
- âœ… Tailscale-status for alle maskiner

---

## ðŸŒ Tilgang til AnythingLLM

Etter at autostart er satt opp og Threadripper har startet:

| Fra hvor | URL | Status |
|----------|-----|--------|
| Threadripper (lokal) | http://localhost:3001 | âœ… Funksjonelt |
| Acer (lokalt nett) | http://192.168.1.200:3001 | âœ… Funksjonelt |
| Utenfor huset | http://100.103.79.103:3001* | âš ï¸ Krever Tailscale-rute |

\* For Ã¥ fÃ¥ tilgang utenfra mÃ¥ du sette opp **subnet routes** pÃ¥ Threadripper:
```bash
# PÃ¥ Threadripper (kjÃ¸r i PowerShell/CMD)
tailscale up --advertise-routes=192.168.1.0/24 --accept-routes
```

---

## ðŸ› FeilsÃ¸king

### "Docker kjÃ¸rer ikke"
- Sjekk at Docker Desktop er installert
- PrÃ¸v Ã¥ starte Docker Desktop manuelt fÃ¸rst
- Sjekk logg: `C:\Logs\anythingllm_autostart.log`

### "Container startet ikke"
- Sjekk om port 3001 er i bruk: `netstat -an | findstr 3001`
- Sjekk Docker-logger: `docker logs anythingllm`

### "Z: disk er frakoblet"
```powershell
# Koble til manuelt:
net use Z: \\192.168.1.200\Bygg_Arkiv /persistent:yes
```

### Vil du deaktivere autostart?
1. Ã…pne Oppgaveplanlegger (`taskschd.msc`)
2. Finn "AnythingLLM_Autostart"
3. HÃ¸yreklikk â†’ Deaktiver

---

## ðŸ“ Viktige stier

| Hva | Sti |
|-----|-----|
| Autostart-skript | `C:\Tools\Threadripper_AnythingLLM_Autostart.ps1` |
| Logger | `C:\Logs\anythingllm_autostart.log` |
| Startup-mappe | `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup` |
| Z: Disk | `\\192.168.1.200\Bygg_Arkiv` |

---

## âœ… Sjekkliste

- [ ] Docker Desktop installert pÃ¥ Threadripper
- [ ] Autostart-skript kopiert til `C:\Tools\`
- [ ] Planlagt oppgave opprettet
- [ ] Testet ved Ã¥ logge av/pÃ¥ Threadripper
- [ ] Z: disk tilkoblet fra Acer
- [ ] Rigg_Monitor.ps1 fungerer fra Acer

---

**Opprettet:** 2026-03-02  
**For:** Den Digitale Riggen

