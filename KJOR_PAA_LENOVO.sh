#!/bin/bash
# KJOR DENNE FILEN PAA LENOVO
# Lim inn alt i terminal (Ctrl+Shift+V)

echo "=========================================="
echo "SANDKASSE-INSTALLASJON PAA LENOVO"
echo "=========================================="

# 1. Opprett mappe
mkdir -p ~/self_healing_system
cd ~/self_healing_system

# 2. Last ned alle filer fra Acer
echo "[1/7] Laster ned filer fra Acer..."
curl -O http://100.114.112.61:8000/install.sh
curl -O http://100.114.112.61:8000/protokoll_server.py
curl -O http://100.114.112.61:8000/sandkasse_protokoll.py
curl -O http://100.114.112.61:8000/sandkasse_protokoll_part2.py
curl -O http://100.114.112.61:8000/self_healing_wrapper.py
curl -O http://100.114.112.61:8000/ai_fixer.py
curl -O http://100.114.112.61:8000/error_handler.py

# 3. Verifiser
echo "[2/7] Verifiserer nedlastinger..."
ls -la

# 4. Installer pakker
echo "[3/7] Installerer Python-pakker (tar 2-3 min)..."
sudo apt update
sudo apt install -y python3-pip git curl
pip3 install --user websockets pyyaml black flake8 pytest pytest-cov bandit

# 5. Gjør install.sh kjørbar
echo "[4/7] Kjorer installasjonsskript..."
chmod +x install.sh
./install.sh

# 6. Start server
echo "[5/7] Starter Sandkasse-Protokoll Server..."
echo "=========================================="
echo "SERVER STARTER NA!"
echo "=========================================="
echo ""
echo "La dette vinduet vaere apent!"
echo "Ga til Acer og start 'Sandkasse Monitor'"
echo ""
python3 protokoll_server.py
