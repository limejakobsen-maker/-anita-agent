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

## Cursor Cloud specific instructions

### Codebase overview

Anita Agent is a self-healing AI system. The core Python code lives in `SANDKASSE/07_Sandkasse_SelfHealing/`. Tests are in `tests/`. A Next.js frontend skeleton is in `frontend-starter/` (no pages yet). The HTTP API server is `enkel_server_NY.py` at the repo root.

### Important: Branch structure

All source code lives on the `master` branch. The `main` branch is nearly empty (only README, .gitignore, MIT License). When setting up, merge `origin/master` to get the actual code.

### Running tests

```bash
export PATH="$HOME/.local/bin:$PATH"
export PYTHONPATH=/workspace:/workspace/SANDKASSE/07_Sandkasse_SelfHealing
pytest tests/unit -v --tb=short --no-cov -k "not test_initialization_without_ai"
```

The `test_initialization_without_ai` test has a pre-existing failure: it mocks `ai_fixer.AIAgent` but the module doesn't export `AIAgent` directly. Skip it with `-k "not test_initialization_without_ai"`.

Integration tests (`tests/integration/`) require a running server and gracefully skip when servers are unavailable.

### Running linting

```bash
flake8 SANDKASSE/07_Sandkasse_SelfHealing/ --max-line-length=120
black --check SANDKASSE/07_Sandkasse_SelfHealing/*.py
isort --check-only SANDKASSE/07_Sandkasse_SelfHealing/*.py
```

The existing codebase has pre-existing lint violations (whitespace, formatting). These are not regressions.

### Running the self-healing demo

```bash
cd SANDKASSE/07_Sandkasse_SelfHealing && python3 main.py
```

Runs test scenarios exercising the `@heal` decorator. Some failures are intentional (empty lists, division by zero, invalid JSON).

### Running the HTTP server

```bash
export PYTHONPATH=/workspace:/workspace/SANDKASSE/07_Sandkasse_SelfHealing:/workspace/SANDKASSE/07_Sandkasse_SelfHealing/for_lenovo
python3 enkel_server_NY.py
```

Serves on port 8765 with endpoints: `GET /health`, `GET /status`, `POST /start`, `POST /stopp`. Runs in limited mode without external AI (Ollama/Kimi/Gemini). The `sandkasse_protokoll` import warning is expected — `enkel_server_NY.py` references the old `LenovoOllamaClient` name which was renamed to `LocalOllamaClient`.

### Frontend (skeleton)

```bash
cd frontend-starter && npm install && npm run dev
```

The frontend is a Next.js 15.1 skeleton. It has dependencies but **no `pages/` or `app/` directory**, so `next dev` will fail with "Couldn't find any pages or app directory." This is the expected state of the starter project.

### Key gotchas

- `pip install psycopg-binary` is needed alongside `requirements-test.txt` because `pytest-postgresql` requires the psycopg binary adapter (system `libpq` is not installed).
- `$HOME/.local/bin` must be on `PATH` for `pytest`, `flake8`, `black`, `isort` etc.
- `PYTHONPATH` must include both `/workspace` and `/workspace/SANDKASSE/07_Sandkasse_SelfHealing` for tests and imports to work.
