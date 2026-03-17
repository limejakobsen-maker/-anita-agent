#!/bin/bash
# ═══════════════════════════════════════════════════════════════════
# INSTALLASJONSSKRIPT - Optimal Sandkasse v3.0
# Kjør dette på Lenovo for å sette opp systemet
# ═══════════════════════════════════════════════════════════════════

set -e  # Stopp ved feil

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║  🚀 INSTALLERER OPTIMAL SANDKASSE v3.0                          ║"
echo "║                                                                  ║"
echo "║  Dette skriptet installerer:                                     ║"
echo "║  • python3-pip, git, verktøy                                     ║"
echo "║  • Python-pakker (black, flake8, pytest, etc.)                   ║"
echo "║  • Oppretter self_healing_system/                                ║"
echo "║  • Initialiserer Git-repo                                        ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

# ═══════════════════════════════════════════════════════════════════
# STEG 1: System-oppdatering og pakker
# ═══════════════════════════════════════════════════════════════════
echo "📦 Steg 1: Installerer system-pakker..."
sudo apt update
sudo apt install -y \
    python3-pip \
    git \
    tree \
    htop \
    tmux \
    curl \
    jq \
    vim \
    nano \
    make

echo "✅ System-pakker installert"
echo ""

# ═══════════════════════════════════════════════════════════════════
# STEG 2: Python-pakker
# ═══════════════════════════════════════════════════════════════════
echo "🐍 Steg 2: Installerer Python-pakker..."
pip3 install --user --upgrade pip

pip3 install --user \
    black \
    flake8 \
    bandit \
    pytest \
    pytest-cov \
    pytest-xdist \
    mypy \
    websockets \
    pyyaml \
    requests

echo "✅ Python-pakker installert"
echo ""

# ═══════════════════════════════════════════════════════════════════
# STEG 3: Opprette mappestruktur
# ═══════════════════════════════════════════════════════════════════
echo "📁 Steg 3: Oppretter mappestruktur..."

mkdir -p ~/self_healing_system
cd ~/self_healing_system

# Opprett sub-mapper
mkdir -p {logs,backups,fixes,sandkasse_produksjon}

echo "✅ Mappestruktur opprettet"
echo ""

# ═══════════════════════════════════════════════════════════════════
# STEG 4: Git konfigurasjon
# ═══════════════════════════════════════════════════════════════════
echo "🌿 Steg 4: Initialiserer Git..."

if [ ! -d .git ]; then
    git init
    git config user.name "Sandkasse Agent"
    git config user.email "sandkasse@local"
    echo "✅ Git initialisert"
else
    echo "ℹ️  Git eksisterer allerede"
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
.pytest_cache/
.mypy_cache/
sandkasse_produksjon/
EOF

echo "✅ .gitignore opprettet"
echo ""

# ═══════════════════════════════════════════════════════════════════
# STEG 5: Kopiere Python-filer
# ═══════════════════════════════════════════════════════════════════
echo "🐍 Steg 5: Kopierer Python-filer..."

echo "⚠️  VIKTIG: Kopier disse filene fra Acer til ~/self_healing_system/:"
echo "   • sandkasse_protokoll.py"
echo "   • sandkasse_protokoll_part2.py"
echo "   • protokoll_server.py"
echo "   • self_healing_wrapper.py"
echo "   • error_handler.py"
echo "   • ai_fixer.py"
echo ""
echo "Du kan bruke: scp, USB, eller OneDrive til å kopiere filene"
echo ""

# ═══════════════════════════════════════════════════════════════════
# STEG 6: Første Git-commit
# ═══════════════════════════════════════════════════════════════════
echo "📝 Steg 6: Første Git-commit..."

if [ -f sandkasse_protokoll.py ]; then
    git add .
    git commit -m "Initial: Optimal Sandkasse v3.0" || echo "Ingen endringer å committe"
    echo "✅ Første commit fullført"
else
    echo "⚠️  Python-filer ikke funnet - commit utsatt"
fi

echo ""

# ═══════════════════════════════════════════════════════════════════
# STEG 7: Verifisering
# ═══════════════════════════════════════════════════════════════════
echo "🔍 Steg 7: Verifisering..."

echo ""
echo "Python: $(python3 --version)"
echo "Pip: $(pip3 --version | head -1)"
echo "Git: $(git --version)"
echo ""

echo "Installerte Python-pakker:"
pip3 list --user | grep -E "black|flake8|bandit|pytest|websockets|yaml" || true
echo ""

# ═══════════════════════════════════════════════════════════════════
# STEG 8: Neste steg
# ═══════════════════════════════════════════════════════════════════
echo ""
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║  ✅ INSTALLASJON FULLFØRT!                                       ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""
echo "📋 Neste steg:"
echo ""
echo "1. Kopier Python-filene fra Acer til ~/self_healing_system/"
echo ""
echo "2. Start serveren:"
echo "   cd ~/self_healing_system"
echo "   python3 protokoll_server.py"
echo ""
echo "3. På Acer: Dobbelklikk 'Sandkasse Monitor.lnk'"
echo ""
echo "4. Test systemet med et enkelt prosjekt!"
echo ""
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║  🎯 STATUS                                                       ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""
echo "System-pakker:   ✅ Installert"
echo "Python-pakker:   ✅ Installert"
echo "Mappestruktur:   ✅ Opprettet"
echo "Git-repo:        ✅ Initialisert"
echo "Python-filer:    ⏳ Venter på kopiering fra Acer"
echo ""
echo "Klar til bruk når filene er kopiert!"
echo ""
