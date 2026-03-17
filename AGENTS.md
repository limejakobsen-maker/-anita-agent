# AGENTS.md - PROSJEKTMAPPE AI

## System-arkitektur

`
PROSJEKTMAPPE AI/
├── 00_Hovedsystem/           # Kjernen på Acer (AI, filsortering)
├── 01_Sandkasse/            # Test-miljø (isolert)
├── 02_Verktoy/              # Reusable scripts
├── 03_Maler/                # Templates
├── 04_Dokumentasjon/        # Docs
├── 05_Logger/               # System-logging
├── 06_Backup/               # Sikkerhetskopier
└── 07_Sandkasse_SelfHealing/ # SELVHELBREDENDE SYSTEM [NY]
`

## 07_Sandkasse_SelfHealing - Lokalt!

Dette er et **selvhelbredende subsystem** som kjører lokalt på Windows.
Det lærer av feil og oppdaterer seg selv automatisk.

### Kommunikasjon
- **GUI (Hovedsystem)** ← → **Lokal Protokoll Server**
- Via localhost:8765
- Bruker lokal Ollama på localhost:11434

### Filstruktur i 07_Sandkasse_SelfHealing/

| Fil | Beskrivelse |
|-----|-------------|
| mini_viewer.py | GUI-vindu (kompakt) |
| code_viewer_gui.py | GUI-vindu (full) |
| self_healing_wrapper.py | @heal dekorator |
| error_handler.py | Feil-logging |
| i_fixer.py | AI-integrasjon |
| main.py | Test-program |
| AGENTS.md | Systemets læring |

### Bruk

**På Acer (Windows):**
`powershell
cd "07_Sandkasse_SelfHealing"
python mini_viewer.py
`

**På Lenovo (Linux):**
`ash
cd /home/emil/self_healing_system
python3 mini_viewer.py
`

---

*Oppdatert: 2026-03-01*
