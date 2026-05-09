# 99_Backup - INVENTORY
## Rydding av PROSJEKTMAPPE AI (Fase 1)

### Dato: 02.03.2026
### Utført av: System-rydding
### Status: Fase 1 fullført - Backup opprettet

---

## 📁 Struktur

```
99_Backup/
├── Gamle_Kontrollpanel/     # GUI-er med encoding-feil
├── Gamle_Scripts/           # Duplikater og utdaterte filer
└── INVENTORY.md            # Denne filen
```

---

## 🗂️ Gamle_Kontrollpanel/

| Fil | Grunn til flytting |
|-----|-------------------|
| Rigg_Kontrollpanel.ps1 | ❌ Encoding-feil (kræsjet). Inneholdt `æøå` lagret som ANSI |
| Rigg_Kontrollpanel_Complete.ps1 | ❌ Samme encoding-feil + duplikat funksjon |

**Erstattes av:** `Rigg_Kontrollpanel_Simple.ps1` (fungerer, ingen æøå)

---

## 🗂️ Gamle_Scripts/

### Duplikate snarvei-scripts
| Fil | Grunn |
|-----|-------|
| Lag_Snarvei.ps1 | Duplikat funksjon |
| Lag_Snarvei_Enkel.ps1 | Duplikat funksjon |
| Oppdater_Snarvei_Complete.ps1 | Duplikat funksjon |
| Update_Shortcut.ps1 | Duplikat funksjon |

**Merk:** Snarveier på skrivebordet beholdes! Dette var kun scriptene som laget dem.

### Utdaterte Threadripper-filer
| Fil | Grunn |
|-----|-------|
| Enkel_Threadripper_Kontroll.ps1 | Utdatert - Threadripper er nå filserver |
| FIKS_Threadripper_Autostart.ps1 | Utdatert - AnythingLLM kjører på Acer |
| SETUP_AUTOSTART_Threadripper.ps1 | Utdatert - Autostart satt opp på Acer |
| Threadripper_AnythingLLM_Autostart.ps1 | Utdatert - Gammel autostart for Docker |
| Start_AnythingLLM_Silently.bat | Utdatert - For gammel Threadripper-setup |

**Ny status:** AnythingLLM kjører på Acer (localhost:3001)

### Andre
| Fil | Grunn |
|-----|-------|
| rigg_kontrollpanel.sh | WSL/Linux-versjon, sjelden brukt |
| DEPLOY_Til_Lenovo.ps1 | Duplikat - finnes i Sandkasse_System/ |

---

## ✅ Beholdt i PROSJEKTMAPPE AI (hovedmappe)

### Dokumentasjon
- README.txt ✅ (oppdatert - Acer er hovedmaskin)
- THREADRIPPER_INFO.txt ✅ (oppdatert - Threadripper = filserver)
- README.md ✅
- AGENTS.md ✅
- README_FULLSTENDIG_SETUP.md ✅
- AUTOSTART_VEILEDNING.md ✅
- AI_SNARVEIER_README.txt ✅

### Funksjonelle scripts
- Rigg_Kontrollpanel_Simple.ps1 ✅ (skal oppdateres med riktige IP-er)
- Rigg_Monitor.ps1 ✅ (tekstbasert, fungerer)
- Setup_SSH_Lenovo.ps1 ✅ (nyttig for Lenovo-tilkobling)
- Aktiver_RDP_Threadripper.ps1 ✅ (kan være nyttig hvis du vil ha RDP)

### Andre filer
- KODE_AGENT_ANYTHINGLLM.html ✅ (nyttig verktøy)
- DEN DIGITALE RIGGEN.pdf ✅ (dokumentasjon)
- DEN DIGITALE RIGGEN.docx ✅ (dokumentasjon)
- kode protokoll.txt ✅ (viktig protokoll)

### Mapper
- Sandkasse_System/ ✅ (viktig for Lenovo-deploy)

---

## 📝 Snarveier på SKRIVEBORDET (beholdt)

Disse er IKKE berørt av ryddingen:

- `Den Digitale Riggen.lnk` (hvis finnes)
- `THREADRIPPER (Skrivebordet).lnk` ✅ 
- `Lokal AI.url` ✅
- `Lenovo Sandkasse.lnk` ✅
- `Sandkasse Monitor.lnk` ✅

---

## 🔄 Gjenoppretting

Hvis du trenger noe fra backup:

```powershell
# Eksempel: Gjenopprett en fil
Copy-Item "99_Backup\Gamle_Scripts\FILENAME.ps1" "."
```

---

## 🎯 Neste steg (Fase 2)

1. Oppdatere `Rigg_Kontrollpanel_Simple.ps1` med riktige IP-er
2. Teste at alt fungerer
3. (Valgfritt) Slette backup permanent etter verifisering

---

**Alt er sikkert lagret i 99_Backup/** 🗄️
