#!/bin/bash
# Setup Script für Surf Camp Buchungsmanagement App

echo "🏄 Surf Camp App Setup"
echo "====================="
echo ""

# Farben für bessere Lesbarkeit
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Schritt 1: Python Version prüfen
echo "📋 Schritt 1: Python Version prüfen..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓${NC} $PYTHON_VERSION gefunden"
else
    echo -e "${RED}✗${NC} Python 3 nicht gefunden. Bitte installiere Python 3.9 oder höher."
    exit 1
fi
echo ""

# Schritt 2: Virtuelle Umgebung erstellen
echo "📋 Schritt 2: Virtuelle Umgebung erstellen..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓${NC} Virtuelle Umgebung erstellt"
else
    echo -e "${YELLOW}!${NC} Virtuelle Umgebung existiert bereits"
fi
echo ""

# Schritt 3: Virtuelle Umgebung aktivieren
echo "📋 Schritt 3: Virtuelle Umgebung aktivieren..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi
echo -e "${GREEN}✓${NC} Virtuelle Umgebung aktiviert"
echo ""

# Schritt 4: Dependencies installieren
echo "📋 Schritt 4: Dependencies installieren..."
pip install --upgrade pip
pip install -r requirements.txt
echo -e "${GREEN}✓${NC} Alle Pakete installiert"
echo ""

# Schritt 5: Ordnerstruktur erstellen
echo "📋 Schritt 5: Ordnerstruktur erstellen..."
mkdir -p .streamlit
echo -e "${GREEN}✓${NC} .streamlit Ordner erstellt"
echo ""

# Schritt 6: Credentials generieren
echo "📋 Schritt 6: Login-Credentials generieren..."
echo -e "${YELLOW}!${NC} Führe jetzt das Credential-Generator-Script aus:"
echo ""
echo "   python generate_credentials.py"
echo ""

# Schritt 7: Nächste Schritte
echo "====================="
echo "✅ Setup abgeschlossen!"
echo "====================="
echo ""
echo "🔧 Nächste Schritte:"
echo ""
echo "1️⃣  Generiere deine Login-Credentials:"
echo "   python generate_credentials.py"
echo ""
echo "2️⃣  Erstelle die secrets.toml Datei:"
echo "   cp secrets.toml.example .streamlit/secrets.toml"
echo "   nano .streamlit/secrets.toml  # oder dein bevorzugter Editor"
echo ""
echo "3️⃣  Konfiguriere Google Sheets API (siehe KONFIGURATION.md)"
echo ""
echo "4️⃣  Erstelle ein Gmail App-Passwort (siehe KONFIGURATION.md)"
echo ""
echo "5️⃣  Starte die App:"
echo "   streamlit run app.py"
echo ""
echo "📖 Detaillierte Anleitung: Lies KONFIGURATION.md"
echo ""
echo "🏄 Viel Erfolg!"
