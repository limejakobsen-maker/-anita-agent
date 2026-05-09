#!/bin/bash
# ═══════════════════════════════════════════════════════════════════
# AUTO-INSTALL FOR LENOVO - Hentet fra Acer HTTP-server
# Dato: 2026-03-02
# Acer IP: 100.114.112.61:8000
# ═══════════════════════════════════════════════════════════════════

set -e  # Stopp ved feil

# Farger
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Konfigurasjon
ACER_IP="100.114.112.61"
ACER_PORT="8000"
INSTALL_DIR="$HOME/self_healing_system"

# ═══════════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════════
echo ""
echo -e "${BLUE}╔══════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  🚀 AUTO-INSTALL - Optimal Sandkasse v3.0                       ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# ═══════════════════════════════════════════════════════════════════
# STEG 1: SJEKK AVHENGIGHETER
# ═══════════════════════════════════════════════════════════════════
echo -e "${BLUE}📦 Steg 1: Sjekker avhengigheter...${NC}"

# Sjekk curl
if ! command -v curl &> /dev/null; then
    echo -e "${YELLOW}⚠️  curl ikke funnet. Installerer...${NC}"
    sudo apt update && sudo apt install -y curl
fi

# Sjekk python3
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ python3 ikke funnet! Installerer...${NC}"
    sudo apt update && sudo apt install -y python3 python3-pip
fi

echo -e "${GREEN}✅ Avhengigheter OK${NC}"
echo ""

# ═══════════════════════════════════════════════════════════════════
# STEG 2: OPPRETT MAPPE
# ═══════════════════════════════════════════════════════════════════
echo -e "${BLUE}📁 Steg 2: Oppretter mappestruktur...${NC}"

mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

echo -e "${GREEN}✅ Mappe opprettet: $INSTALL_DIR${NC}"
echo ""

# ═══════════════════════════════════════════════════════════════════
# STEG 3: LAST NED FILER
# ═══════════════════════════════════════════════════════════════════
echo -e "${BLUE}📥 Steg 3: Laster ned filer fra Acer ($ACER_IP:$ACER_PORT)...${NC}"
echo ""

FILES=(
    "sandkasse_protokoll.py"
    "sandkasse_protokoll_part2.py"
    "protokoll_server.py"
    "self_healing_wrapper.py"
    "error_handler.py"
    "ai_fixer.py"
    "install.sh"
)

SUCCESS_COUNT=0
for file in "${FILES[@]}"; do
    echo -n "  Laster ned $file... "
    if curl -s -O "http://$ACER_IP:$ACER_PORT/$file"; then
        echo -e "${GREEN}✓${NC}"
        ((SUCCESS_COUNT++))
    else
        echo -e "${RED}✗${NC}"
    fi
done

echo ""
if [ $SUCCESS_COUNT -eq ${#FILES[@]} ]; then
    echo -e "${GREEN}✅ Alle ${#FILES[@]} filer lastet ned!${NC}"
else
    echo -e "${YELLOW}⚠️  $SUCCESS_COUNT/${#FILES[@]} filer lastet ned${NC}"
fi
echo ""

# ═══════════════════════════════════════════════════════════════════
# STEG 4: VERIFISER
# ═══════════════════════════════════════════════════════════════════
echo -e "${BLUE}🔍 Steg 4: Verifiserer nedlastning...${NC}"
echo ""

ls -la
echo ""

# ═══════════════════════════════════════════════════════════════════
# STEG 5: GJØR INSTALL.SH KJØRBAR
# ═══════════════════════════════════════════════════════════════════
if [ -f "install.sh" ]; then
    chmod +x install.sh
    echo -e "${GREEN}✅ install.sh er nå kjørbar${NC}"
    echo ""
    
    # ═══════════════════════════════════════════════════════════════════
    # STEG 6: KJØR INSTALLASJON
    # ═══════════════════════════════════════════════════════════════════
    echo -e "${BLUE}🔧 Steg 6: Kjører installasjon...${NC}"
    echo ""
    
    read -p "Vil du kjøre install.sh nå? (y/n): " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        ./install.sh
        
        # ═══════════════════════════════════════════════════════════════════
        # STEG 7: START SERVER
        # ═══════════════════════════════════════════════════════════════════
        echo ""
        echo -e "${BLUE}🚀 Steg 7: Klar til å starte server!${NC}"
        echo ""
        
        read -p "Vil du starte protokoll_server.py nå? (y/n): " -n 1 -r
        echo ""
        
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo -e "${GREEN}🚀 Starter server...${NC}"
            echo -e "${YELLOW}💡 Trykk Ctrl+C for å stoppe${NC}"
            echo ""
            python3 protokoll_server.py
        else
            echo -e "${BLUE}ℹ️  Du kan starte server senere med:${NC}"
            echo -e "   cd $INSTALL_DIR && python3 protokoll_server.py"
        fi
    else
        echo -e "${BLUE}ℹ️  Du kan kjøre installasjon senere med:${NC}"
        echo -e "   cd $INSTALL_DIR && ./install.sh"
    fi
else
    echo -e "${RED}❌ install.sh ikke funnet!${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  ✅ AUTO-INSTALL FULLFØRT!                                       ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}📋 Neste steg på Acer (Windows):${NC}"
echo "   1. Kjør: python protokoll_monitor.py"
echo "   2. Eller dobbeltklikk: Sandkasse Monitor.lnk"
echo "   3. Test systemet med et prosjekt!"
echo ""
