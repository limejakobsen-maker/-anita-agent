# 🏗️ 07_Sandkasse_SelfHealing v3.0 - LOKAL EDITION

## 🚀 STATUS: KLAR FOR LOKAL BRUK

**System:** ✅ Kjører lokalt på Windows  
**Ollama:** ⏳ Krever lokal installasjon  
**Dato:** 2026-03-12

---

## Om dette systemet

Dette er **selvhelbredende sandkasse-systemet** som kjører lokalt på Windows.
Systemet lærer av sine egne feil og blir bedre over tid.

### Hva er en "sandkasse"?

En isolert test-omgivelse hvor vi kan:
- Teste farlig kode uten å ødelegge hovedsystemet
- La AI eksperimentere med fikser
- Lære av feil på en trygg måte

### System-plassering

| Komponent | Lokasjon | Status |
|-----------|----------|--------|
| **Hovedsystem** | C:\Users\Emil\Desktop\PROSJEKTMAPPE AI\SANDKASSE\07_Sandkasse_SelfHealing\ | ✅ Klar |
| **AI System** | C:\AI_System\ | ✅ Klar |
| **Ollama** | localhost:11434 | ⏳ Krever installasjon |

---

## 📦 Viktige filer

| Fil | Størrelse | Funksjon |
|-----|-----------|----------|
| `sandkasse_protokoll.py` | 24 KB | Hovedmotor Fase 1-3 |
| `sandkasse_protokoll_part2.py` | 13 KB | Hovedmotor Fase 4-6 |
| `protokoll_server.py` | 8 KB | WebSocket-server |
| `self_healing_wrapper.py` | 7.5 KB | @heal dekorator |
| `ai_fixer.py` | 10.5 KB | AI-integrasjon |
| `error_handler.py` | 10 KB | Feil-logging |

**Totalt:** ~73 KB

---

## 🚀 HURTIGSTART (Lokal installasjon)

### FORUTSETNINGER
- Python 3.10+ installert
- Ollama installert og kjørende på localhost:11434
- Git installert (valgfritt)

### STEG 1: Installer avhengigheter

```powershell
# Installer Python-pakker
pip install black flake8 pytest pytest-cov websockets pyyaml requests

# Hvis du bruker Ollama, sjekk at den kjører:
# http://localhost:11434
```

### STEG 2: Starte protokoll server lokalt

```powershell
cd "C:\AI_System\protokoll"
python enkel_server.py
```

Du skal se:
```
╔═══════════════════════════════════════════════════════════╗
║  ENKEL HTTP SERVER v2.0 - Lokal                            ║
║  Lytter på: http://0.0.0.0:8765                          ║
╚═══════════════════════════════════════════════════════════╝
```

### STEG 3: Kjør Sandkasse Monitor

```powershell
cd "Desktop\PROSJEKTMAPPE AI\SANDKASSE\07_Sandkasse_SelfHealing"
python mini_viewer.py
```

---

## 🔄 6-Fase Protokollen

```
Fase 1: INIT     → Research, krav, PROJECT.md
Fase 2: DISCUSS  → Låse beslutninger (CONTEXT.md)
Fase 3: PLAN     → Parallell research, XML-planer
Fase 4: EXECUTE  → Kode med @heal dekorator
Fase 5: VALIDATE → pytest >90%, linting
Fase 6: DEPLOY   → Git commit + arkivering
```

---

## 🧠 Hvordan @heal fungerer

```python
from self_healing_wrapper import heal

@heal  ← Denne dekoratoren fanger feil!
def min_funksjon():
    # Hvis feil oppstår:
    # 1. Logger feilen
    # 2. Ber AI om fiks
    # 3. Viser fiks i Acer GUI
    # 4. Venter på godkjenning
    # 5. Anvender fiks og prøver igjen
    pass
```

---

## 📁 Viktige dokumenter

| Fil | Beskrivelse |
|-----|-------------|
| `LENOVO_STATUS.md` | Aktuell status på Lenovo |
| `KOPIER_MANUELL.txt` | Steg-for-steg kopiering |
| `SANDKASSE_PROTOKOLL_README.md` | Full protokoll-dokumentasjon |
| `OPPSUMMERING_OPTIMAL_SANDKASSE.md` | System-oversikt |
| `IMPLEMENTERINGSPLAN.md` | Detaljert implementering |

---

## 🔒 Sikkerhet

- ✅ Alltid backup før kode-endringer
- ✅ Fikser testes før de anvendes
- ✅ Lenovo er isolert fra hovedsystem
- ✅ **Ingen auto-deploy** uten godkjenning fra Acer

---

## 📞 Support

**Hvis noe går galt:**
1. Sjekk HTTP-server: http://100.114.112.61:8000/
2. Sjekk logg: `~/self_healing_system/logs/` på Lenovo
3. Restart server: Ctrl+C, deretter `python3 protokoll_server.py`
4. Se `LENOVO_STATUS.md` for feilsøking

---

**Status:** 🚀 KOPIERING PÅGÅR  
**Sist oppdatert:** 2026-03-02  
**Versjon:** 3.0 (Optimal Sandkasse)
