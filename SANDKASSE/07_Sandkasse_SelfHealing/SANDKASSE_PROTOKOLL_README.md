# 🏗️ Sandkasse-Protokollen v2.0

**Integrert 5-fase selvhelbredende kodegenerering for Lenovo Sandkasse**

---

## 📋 Oversikt

Dette systemet kombinerer:
- **5-fase protokollen** (TDD, iterativ utvikling)
- **@heal dekorator** (auto-fiks av feil)
- **AI-integrasjon** (Kimi/Gemini)
- **Sanntidsovervåking** (fra Acer)

```
┌─────────────────────────────────────────────────────────┐
│  ACER (Overvåking) ──► LENOVO (Utvikling)              │
│  ├─ GUI Monitor         ├─ 5-fase protokoll            │
│  ├─ Start/Stopp         ├─ @heal system                │
│  ├─ Se kode LIVE        ├─ AI-fikser                   │
│  └─ Godkjenn fikser     └─ Automatisk testing          │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Hurtigstart

### Steg 1: På Lenovo (Sandkasse)

```bash
# 1. SSH til Lenovo (eller fysisk tilgang)
ssh emil@100.108.91.44

# 2. Gå til prosjektmappen
cd ~/self_healing_system

# 3. Kopier nye filer (fra USB/nettverk)
cp /mnt/usb/for_lenovo/* ./

# 4. Installer avhengigheter
pip3 install websockets pyyaml requests pytest pytest-cov black flake8 bandit

# 5. Start serveren
python3 protokoll_server.py
```

Du skal se:
```
╔═══════════════════════════════════════════════════════════╗
║  [LENOVO] Sandkasse-Protokoll Server v2.0                  ║
║  Lytter på: 0.0.0.0:8765                                  ║
║  Tailscale: 100.108.91.44                                 ║
╚═══════════════════════════════════════════════════════════╝
```

### Steg 2: På Acer (Overvåking)

```powershell
# 1. Gå til prosjektmappen
cd "C:\Users\limej\OneDrive\Desktop\PROSJEKTMAPPE AI\07_Sandkasse_SelfHealing"

# 2. Klikk på: monitor_launcher.bat
#    ELLER kjør direkte:
python protokoll_monitor.py
```

---

## 📁 Filstruktur

### På Lenovo (`~/self_healing_system/`)

```
self_healing_system/
├── protokoll_server.py       [NY] WebSocket-server
├── sandkasse_protokoll.py    [NY] 5-fase protokoll
├── self_healing_wrapper.py   [EKS] @heal dekorator
├── ai_fixer.py               [EKS] AI-integrasjon
├── error_handler.py          [EKS] Feil-logging
├── mini_viewer.py            [EKS] Lokal GUI
├── main.py                   [EKS] Test-program
├── config.yaml               [EKS] Konfigurasjon
└── AGENTS.md                 [AUTO] Lærdommer
```

### På Acer (`07_Sandkasse_SelfHealing/`)

```
07_Sandkasse_SelfHealing/
├── protokoll_monitor.py      [NY] Overvåkingsvindu
├── monitor_launcher.bat      [NY] Enkel start
├── SANDKASSE_PROTOKOLL_README.md  [NY] Denne filen
└── for_lenovo/               [NY] Filer for Lenovo
    ├── protokoll_server.py
    └── sandkasse_protokoll.py
```

---

## 🎮 Brukergrensesnitt (Acer)

### Fase-indikatorer

| Indikator | Betydning |
|-----------|-----------|
| ⚫ Grå | Venter på start |
| 🔵 Blå | Aktiv fase |
| 🟢 Grønn | Fullført |

### Kontroller

| Knapp | Funksjon |
|-------|----------|
| **▶ START** | Start ny protokoll |
| **⏹ STOPP** | Stopp pågående |
| **🗑 TØM** | Tøm logg/kode-visning |
| **✅ GODKJENN** | Godkjenn AI-fiks |
| **❌ AVVIS** | Avvis AI-fiks |

### Input-felter

- **Prosjektnavn**: Navn på prosjektet (f.eks. "RegnskapV2")
- **Krav**: Beskrivelse av hva koden skal gjøre

---

## 🔄 5-Fase Protokollen

### Fase 1: SPECS
- Opprett prosjektmappe
- Generer `spesifikasjon.json`
- Definer akseptansekriterier

### Fase 2: SKELETT  
- Lag mappestruktur (src/, tests/, docs/)
- Generer **test-mal først** (TDD!)
- Lag `main.py` skelett med @heal

### Fase 3: KODE
- AI genererer kode
- Kjør med @heal dekorator
- Ved feil → AI genererer fiks
- **Manuell godkjenning** fra Acer
- Iterer maks 10 ganger

### Fase 4: VALIDER
- **Tester**: pytest (>90% dekning påkrevd)
- **Linting**: flake8 + black
- **Sikkerhet**: bandit

### Fase 5: DEPLOY
- Versjonering: `v_YYYYMMDD_HHMMSS`
- Kopier til `/home/emil/kode_arkiv/`
- Generer `manifest.json`

---

## 🔌 Kommunikasjon

### Nettverk

- **Protokoll**: WebSocket
- **Lenovo IP**: 100.108.91.44 (Tailscale)
- **Port**: 8765

### Meldingstyper

| Type | Retning | Beskrivelse |
|------|---------|-------------|
| `start_protokoll` | Acer → Lenovo | Start ny prosess |
| `stopp_protokoll` | Acer → Lenovo | Stopp prosess |
| `log` | Lenovo → Acer | Logg-melding |
| `status` | Lenovo → Acer | Fase/progress |
| `code` | Lenovo → Acer | Kode for visning |
| `approval_request` | Lenovo → Acer | Be om godkjenning |
| `approval_response` | Acer → Lenovo | Godkjenn/avvis |

---

## ⚙️ Konfigurasjon

### På Lenovo (`config.yaml`)

```yaml
# Viktige innstillinger
healing:
  max_attempts: 3           # AI-fiks forsøk
  enable_ai_fixes: true     # Bruk AI
  
safety:
  allow_auto_apply: false   # KREV manuell godkjenning!
  require_validation: true  # Må validere fikser
  
ai:
  prefer_kimi: true         # Prioriter Kimi over Gemini
  timeout_seconds: 30       # Timeout for AI-kall
```

### Viktig: `allow_auto_apply: false`

Dette betyr at **alle fikser må godkjennes manuelt på Acer** før de anvendes.

---

## 🐛 Feilsøking

### Problem: "Kan ikke koble til Lenovo"

**Sjekkliste:**
1. ✅ Er Lenovo påslått?
2. ✅ Kjører `protokoll_server.py`?
3. ✅ Er Tailscale aktiv på begge?
   ```bash
   tailscale status
   ```
4. ✅ Kan du pinge Lenovo?
   ```powershell
   ping 100.108.91.44
   ```

### Problem: "AI ikke tilgjengelig"

På Lenovo:
```bash
# Sjekk at API-nøkler er satt
export KIMI_API_KEY="din-nøkkel"
export GOOGLE_API_KEY="din-nøkkel"

# Eller i .env-fil
```

### Problem: "Tester feiler"

Sjekk testdekning:
```bash
cd ~/sandkasse_produksjon/[prosjekt]
pytest tests/ -v --cov=src
```

---

## 📝 Eksempel-arbeidsflyt

### Scenario: Lage nytt regnskapssystem

1. **Acer**: Åpne `monitor_launcher.bat`
2. **Acer**: Fyll inn:
   - Prosjektnavn: `RegnskapV2`
   - Krav: `Et regnskapssystem for håndtering av byggprosjekter med moms og fakturering`
3. **Acer**: Klikk **▶ START**
4. **Lenovo**: Starter Fase 1-2 automatisk
5. **Acer**: Ser fase-indikatorer endre seg
6. **Lenovo**: Fase 3 - Genererer kode
7. **Acer**: Ser kode vises i sanntid
8. **Lenovo**: Oppdager feil, genererer fiks
9. **Acer**: Får popup "Godkjenning kreves"
10. **Acer**: Ser på foreslått fiks, klikker **✅ GODKJENN**
11. **Lenovo**: Anvender fiks, fortsetter
12. **Acer**: Ser valideringsrapport
13. **Lenovo**: Fase 5 - Arkiverer
14. **Acer**: Mottar "Prosjekt fullført"

---

## 🔒 Sikkerhet

- ✅ **Ingen auto-deploy** uten godkjenning
- ✅ **Backup** før hver fiks
- ✅ **Validering** av all kode
- ✅ **Isolert miljø** på Lenovo
- ✅ **Manuell review** av AI-generert kode

---

## 📊 Statistikk

Monitor viser:
- Kjøringer totalt
- Antall feil
- Antall fikset
- Suksessrate (%)

Logges også i `logs/protokoll_YYYYMMDD.log` på Lenovo.

---

## 🔄 Synkronisering

### Acer → Lenovo (oppdater system)

```bash
# På Lenovo
cd ~/self_healing_system
git pull  # Hvis git-repo
# ELLER
rsync -avz /mnt/usb/for_lenovo/ ./
```

### Lenovo → Acer (hent lærdom)

```bash
# Kopier AGENTS.md tilbake
cp ~/self_healing_system/AGENTS.md /mnt/usb/
```

---

## 🎯 Neste steg / Videreutvikling

- [ ] E-post-varsling ved feil
- [ ] Automatisk deploy til test-server
- [ ] Integrasjon med Git/GitHub
- [ ] Støtte for flere språk (JS, Go, Rust)
- [ ] Web-grensesnitt (istedenfor tkinter)

---

**Laget:** 2026-03-02  
**Versjon:** 2.0  
**Forfatter:** Din lokale AI 🤖
