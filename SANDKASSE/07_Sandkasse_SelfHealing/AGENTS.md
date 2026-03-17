# Sandkasse AI Agent - Lærdommer og Historikk

## 📅 2026-03-12 - SYSTEM ENDRET TIL LOKAL DRIFT

### Hva ble gjort:
- ✅ Alle Lenovo-referanser fjernet fra koden
- ✅ Ollama endret fra ekstern (100.108.91.44) til lokal (localhost:11434)
- ✅ System-paths oppdatert for Windows
- ✅ Dokumentasjon oppdatert
- ✅ AI Fixer oppdatert til å bruke lokale paths

### System-konfigurasjon:
```
Hoved-PC (Windows):    localhost:8765  (Protokoll server)
Ollama (Lokal):        localhost:11434 (AI-modeller)
Base path:             C:/AI_System/
```

### Endringer i hovedfiler:
**sandkasse_protokoll.py:**
- `LenovoOllamaClient` → `LocalOllamaClient`
- `lenovo_ollama_url` → `local_ollama_url`
- `lenovo_models` → `local_models`

**enkel_server.py:**
- `lenovo_tilkoblet` → `ollama_tilkoblet`
- `check_lenovo_connection` → `check_ollama_connection`

**ai_fixer.py:**
- Fjernet Linux-paths (`/home/emil/...`)
- Lagt til lokal Ollama fallback
- Oppdatert paths for Windows

### Neste steg:
1. Sjekk at Ollama er installert: `http://localhost:11434`
2. Installer Python-avhengigheter: `pip install requests websockets`
3. Test systemet: `python C:/AI_System/protokoll/enkel_server.py`

---

## 🎯 SYSTEMARKITEKTUR

### Komponenter:
1. **Acer (Windows)** - Overvåking og kontroll
   - GUI Monitor (protokoll_monitor.py)
   - HTTP-server for fil-distribusjon
   - Manuell godkjenning av AI-fikser

2. **Lenovo (Linux)** - Sandkasse og utvikling
   - WebSocket-server (protokoll_server.py)
   - 6-fase protokoll motor
   - @heal dekorator system
   - AI-integrasjon (Kimi/Gemini)

3. **Threadripper** - Lokal AI (fremtidig)
   - AnythingLLM med Ollama
   - Llama 3 eller annen lokal modell

### 6-Fase Protokoll:
1. **INIT** - Research og krav
2. **DISCUSS** - Låse beslutninger
3. **PLAN** - Parallell research
4. **EXECUTE** - Kode med @heal
5. **VALIDATE** - Testing >90%
6. **DEPLOY** - Arkivering

---

## 🔧 TEKNISKE DETALJER

### @heal Dekorator:
```python
@heal  # Fanger feil → Logger → AI-fiks → Godkjenning → Anvend
def min_funksjon():
    pass
```

### Kommunikasjon:
- Protokoll: WebSocket
- Port: 8765
- Retning: Acer ← → Lenovo

### Sikkerhet:
- Ingen auto-deploy uten godkjenning
- Backup før alle endringer
- Isolert miljø på Lenovo
- Manuell review av AI-kode

---

## 📚 DOKUMENTASJON

| Fil | Formål |
|-----|--------|
| README.md | Hoveddokumentasjon |
| LENOVO_STATUS.md | Aktuell status på Lenovo |
| SANDKASSE_PROTOKOLL_README.md | Full protokoll-docs |
| OPPSUMMERING_OPTIMAL_SANDKASSE.md | System-oversikt |
| IMPLEMENTERINGSPLAN.md | Detaljert plan |
| KOPIER_MANUELL.txt | Steg-for-steg kopiering |
| AGENTS.md | Denne filen |

---

## 🚀 STATUS

**Dato:** 2026-03-02  
**Versjon:** 3.0 (Optimal Sandkasse)  
**Fase:** Kopiering til Lenovo pågår  
**Neste:** Installasjon og testing

## 2026-03-12 15:56
**Funksjon:** prosess_data
**Feil:** IndexError: list index out of range
**Frekvens:** 1 ganger
**Fiks:** ✅ Suksess
**Lærdom:** IndexError kan fikses med 452 tegn kode
---

## 2026-03-12 15:56
**Funksjon:** prosess_data
**Feil:** IndexError: list index out of range
**Frekvens:** 2 ganger
**Fiks:** ✅ Suksess
**Lærdom:** IndexError kan fikses med 452 tegn kode
---

## 2026-03-12 15:56
**Funksjon:** hent_konfig
**Feil:** KeyError: 'finnes_ikke'
**Frekvens:** 1 ganger
**Fiks:** ✅ Suksess
**Lærdom:** KeyError kan fikses med 348 tegn kode
---

## 2026-03-12 15:56
**Funksjon:** hent_konfig
**Feil:** KeyError: 'finnes_ikke'
**Frekvens:** 2 ganger
**Fiks:** ✅ Suksess
**Lærdom:** KeyError kan fikses med 348 tegn kode
---

## 2026-03-12 15:56
**Funksjon:** parse_json
**Feil:** JSONDecodeError: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
**Frekvens:** 1 ganger
**Fiks:** ✅ Suksess
**Lærdom:** JSONDecodeError kan fikses med 350 tegn kode
---

## 2026-03-12 15:56
**Funksjon:** parse_json
**Feil:** JSONDecodeError: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
**Frekvens:** 2 ganger
**Fiks:** ✅ Suksess
**Lærdom:** JSONDecodeError kan fikses med 350 tegn kode
---
