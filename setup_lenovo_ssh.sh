#!/bin/bash
# SETUP SSH OG SERVER PAA LENOVO
# Kjor: curl http://100.114.112.61:8000/setup_lenovo_ssh.sh | bash

echo "=========================================="
echo "AKTIVERER SSH OG SANDKASSE SERVER"
echo "=========================================="

# 1. Installer SSH
sudo apt update
sudo apt install -y openssh-server

# 2. Start SSH
sudo systemctl start ssh
sudo systemctl enable ssh

# 3. Sjekk at SSH kjorer
if systemctl is-active --quiet ssh; then
    echo "[OK] SSH er aktivert!"
else
    echo "[FEIL] SSH kunne ikke startes"
    exit 1
fi

# 4. Sjekk IP
echo ""
echo "Din IP: $(hostname -I)"
echo "Tailscale IP: $(tailscale ip -4 2>/dev/null || echo 'Sjekk: tailscale status')"

# 5. Last ned og start Sandkasse Server
cd ~
if [ ! -d "self_healing_system" ]; then
    mkdir -p self_healing_system
fi

cd self_healing_system

echo ""
echo "[OK] Laster ned server-filer..."
curl -s -O http://100.114.112.61:8000/protokoll_server.py
curl -s -O http://100.114.112.61:8000/sandkasse_protokoll.py
curl -s -O http://100.114.112.61:8000/self_healing_wrapper.py
curl -s -O http://100.114.112.61:8000/ai_fixer.py
curl -s -O http://100.114.112.61:8000/error_handler.py

# 6. Installer Python-pakker
pip3 install --user websockets pyyaml black flake8 pytest 2>/dev/null

echo ""
echo "=========================================="
echo "STARTER SERVER..."
echo "=========================================="
echo ""
echo "Du kan na koble fra Acer med:"
echo "  ssh emil@100.108.91.44"
echo ""
echo "Starter server..."
python3 protokoll_server.py
