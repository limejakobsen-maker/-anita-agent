# 🚀 IMPLEMENTERINGSPLAN - Optimal Sandkasse

**Mål:** Kombinere GSD's beste med vårt system  
**Hvor:** Lenovo (Linux Sandkasse)  
**Overvåking:** Acer (Windows GUI)  
**Status:** KLAR FOR BYGGING

---

## 📋 Systemarkitektur (Endelig Versjon)

```
┌─────────────────────────────────────────────────────────────────────┐
│  ACER (Overvåking & Kontroll)                                       │
│  ├─ Sandkasse Monitor.lnk → GUI for sanntidsovervåking             │
│  ├─ Lokal AI.url → AnythingLLM (Threadripper)                      │
│  └─ Lenovo Sandkasse.lnk → RDP til Lenovo                          │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  LENOVO (100.108.91.44) - "Den Optimale Sandkassen"                │
│  ├─ protokoll_server.py ← WebSocket-server (port 8765)             │
│  ├─ sandkasse_protokoll.py ← Hovedmotoren (6 faser)                │
│  ├─ self_healing_wrapper.py ← @heal dekorator                      │
│  ├─ ai_fixer.py ← AI-integrasjon (Kimi/Gemini)                     │
│  ├─ error_handler.py ← Logging & læring                            │
│  ├─ Git repo ← Versjonskontroll                                    │
│  └─ ~/sandkasse_produksjon/ ← Kode genereres her                   │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  THREADRIPPER (192.168.1.200)                                       │
│  └─ AnythingLLM (Ollama/Llama 3) ← "Anita AI"                       │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Z: DRIVE (Bygg_Arkiv)                                              │
│  └─ Kode_arkiv/ ← Ferdige prosjekter arkiveres her                 │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🎯 6-FASE PROTOTYPE (Forbedret fra 5 til 6 faser)

Basert på GSD + vårt system:

| Fase | Navn | Fra | Beskrivelse |
|------|------|-----|-------------|
| 1 | **INIT** | GSD | Omfattende spørsmål, research, krav |
| 2 | **DISCUSS** | GSD | Kontekst-fase før koding (CONTEXT.md) |
| 3 | **PLAN** | GSD | Parallell research, XML planer |
| 4 | **EXECUTE** | VÅR | @heal + fresh context per plan |
| 5 | **VALIDATE** | VÅR | pytest + linting + security (>90%) |
| 6 | **DEPLOY** | VÅR | Git commit + arkivering på Z: |

---

## 🛠️ STEG-FOR-STEG IMPLEMENTERING

### 🔴 FASE 1: GRUNNMUR (Gjør dette FØRST!)

#### 1.1 Sjekke hva som finnes på Lenovo
**På Lenovo, kjør:**
```bash
# Python & verktøy
python3 --version
pip3 list | head -30

# Systempakker
dpkg -l | grep -E 'python|git|docker|node|npm'

# Prosjektmappe
ls -la ~/self_healing_system/ 2>/dev/null || echo "Mangler!"

# Disk & minne
df -h /home
free -h

# Nettverk (Tailscale)
tailscale status
```

#### 1.2 Installere manglende verktøy
**På Lenovo, kjør:**
```bash
# Essential
sudo apt update
sudo apt install -y git tree htop tmux curl jq vim nano

# Python utvikling
pip3 install --user black flake8 bandit pytest pytest-cov pytest-xdist mypy

# Git konfigurering (hvis ikke gjort)
git config --global user.name "Sandkasse Agent"
git config --global user.email "sandkasse@local"

# Sjekk at alt er installert
echo "=== SJEKKLISTE ==="
which git && echo "✓ git"
which python3 && echo "✓ python3"
which black && echo "✓ black"
```

#### 1.3 Sette opp Git-repo i self_healing_system
**På Lenovo, kjør:**
```bash
cd ~/self_healing_system

# Init git hvis ikke eksisterer
if [ ! -d .git ]; then
    git init
    echo "Git initialisert"
fi

# Lag .gitignore
cat > .gitignore << 'EOF'
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info/
dist/
build/
*.log
logs/*.log
backups/*.bak
fixes/*.py
.planning/
*.tmp
.coverage
htmlcov/
EOF

# Første commit
git add .
git commit -m "Initial: Sandkasse-Protokoll v2.0"

echo "Git-repo klart!"
```

**Status etter 1.3:** ✅ Grunnmur på plass

---

### 🟡 FASE 2: KJERNEKODE (Hovedmotoren)

#### 2.1 Kopiere filer til Lenovo
**På Acer:** Kopier `for_lenovo/` til Lenovo (via USB/SCP/OneDrive)

**Filene som skal kopieres:**
- `sandkasse_protokoll.py` (oppdatert versjon)
- `protokoll_server.py` (WebSocket-server)
- `requirements.txt` (ny)

#### 2.2 Oppdaterte kjerne-filer
Jeg skal lage oppdaterte versjoner med:
- ✅ 6-fase flyt (inkludert DISCUSS)
- ✅ Fresh context management
- ✅ Parallell kjøring (ThreadPoolExecutor)
- ✅ Git integrasjon (atomic commits)
- ✅ Beholder @heal og GUI-monitorering

#### 2.3 Teste serveren
**På Lenovo:**
```bash
cd ~/self_healing_system
pip3 install --user websockets pyyaml
python3 protokoll_server.py
```

**Forventet output:**
```
╔═══════════════════════════════════════════════════════════╗
║  [LENOVO] Sandkasse-Protokoll Server v2.0                  ║
║  Lytter på: 0.0.0.0:8765                                  ║
╚═══════════════════════════════════════════════════════════╝
```

**Status etter 2.3:** ✅ Kjernen kjører

---

### 🟢 FASE 3: OVERVÅKING (Acer)

#### 3.1 Verifisere på Acer
**Dobbeltklikk:** `Sandkasse Monitor.lnk` på skrivebordet

**Forventet:**
- Python-vindu åpnes
- Kobler til Lenovo (100.108.91.44:8765)
- Viser "Tilkoblet Lenovo"

#### 3.2 Første testkjøring
**I GUI:**
1. Prosjektnavn: `TestProsjekt`
2. Krav: `Et enkelt Python-program som skriver "Hei Verden"`
3. Klikk **START**
4. Observer fase 1-6

**Status etter 3.3:** ✅ System fungerer!

---

### 🔵 FASE 4: FORBEDRINGER (Avansert)

#### 4.1 Parallell kjøring
Implementere ThreadPoolExecutor for uavhengige oppgaver

#### 4.2 Fresh context management
- Splitte store planer i atomiske oppgaver
- Tømme logger underveis
- Summaries istedenfor full historikk

#### 4.3 Ollama integrasjon (lokal LLM)
**På Lenovo:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3
```

**Status etter 4.3:** ✅ Avanserte funksjoner

---

## 📁 FILSTRUKTUR (Endelig)

### På Lenovo (`~/self_healing_system/`):
```
self_healing_system/
├── .git/                           # Versjonskontroll
├── .gitignore                      # Ignorerte filer
│
├── config.yaml                     # Konfigurasjon
├── README.md                       # Dokumentasjon
├── AGENTS.md                       # Lærdommer (auto-generert)
│
├── protokoll_server.py             # WebSocket server
├── sandkasse_protokoll.py          # Hovedmotoren (6 faser)
│
├── self_healing_wrapper.py         # @heal dekorator
├── ai_fixer.py                     # AI-integrasjon
├── error_handler.py                # Feil-logging
│
├── utils/
│   ├── context_manager.py          # Fresh context (GSD-inspirert)
│   ├── parallel_runner.py          # Parallell kjøring
│   └── git_helper.py               # Git integrasjon
│
├── logs/                           # Logger (git-ignored)
├── backups/                        # Backups (git-ignored)
├── fixes/                          # Auto-fikser (git-ignored)
└── .planning/                      # Planlegging (git-ignored)
    ├── research/                   # Research (GSD-stil)
    └── contexts/                   # CONTEXT.md per fase
```

### På Acer (kun snarveier):
```
Skrivebord/
├── Sandkasse Monitor.lnk           # GUI overvåking
├── Lenovo Sandkasse.lnk            # RDP til Lenovo
├── Lokal AI.url                    # AnythingLLM
└── AI_SNARVEIER_README.txt         # Instruksjoner
```

### På Z: (arkiv):
```
Kode_arkiv/
└── [prosjektnavn]/
    └── v_YYYYMMDD_HHMMSS/          # Versjonert arkiv
        ├── manifest.json
        └── [prosjektfiler]
```

---

## ✅ SJEKKLISTE - Før vi starter

### Du må gjøre:
- [ ] Logge på Lenovo (fysisk eller via RDP)
- [ ] Kjøre kommandoene i FASE 1.1
- [ ] Sende meg resultatet så jeg vet hva som mangler

### Jeg skal gjøre (etter din info):
- [ ] Lage oppdaterte Python-filer med 6-fase systemet
- [ ] Integrere GSD's beste praksiser
- [ ] Beholde våre unike styrker (@heal, GUI, manuell godkjenning)

---

## 🎯 NESTE STEG

**Din oppgave NÅ:**

1. Koble til Lenovo (dobbeltklikk "Lenovo Sandkasse.lnk")
2. Logg inn med ditt brukernavn/passord
3. Åpne terminal
4. Kjør kommandoene fra "FASE 1.1"
5. Kopier resultatet og lim det inn her

**Så tar jeg over:**
- Lager ferdig kode
- Guider deg gjennom installasjon
- Tester systemet

---

**Klar? Send meg output fra Lenovo!** 🚀
