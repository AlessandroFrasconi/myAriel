#!/bin/bash

# Script di avvio rapido per MyAriel Resource Manager

echo "🎓 MyAriel Resource Manager - Avvio"
echo "===================================="
echo ""

# Verifica Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 non trovato. Installalo prima di continuare."
    exit 1
fi

echo "✓ Python trovato: $(python3 --version)"

# Verifica se esiste venv
if [ ! -d "venv" ]; then
    echo "→ Creazione ambiente virtuale..."
    python3 -m venv venv
    echo "✓ Ambiente virtuale creato"
fi

# Attiva venv
echo "→ Attivazione ambiente virtuale..."
source venv/bin/activate

# Installa dipendenze
if [ ! -f "venv/.installed" ]; then
    echo "→ Installazione dipendenze..."
    pip install -r requirements.txt
    touch venv/.installed
    echo "✓ Dipendenze installate"
else
    echo "✓ Dipendenze già installate"
fi

# Verifica .env
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  File .env non trovato!"
    echo "→ Copia .env.example in .env e inserisci le tue credenziali"
    echo ""
    cp .env.example .env
    echo "✓ File .env creato. MODIFICA IL FILE .env CON LE TUE CREDENZIALI!"
    echo ""
    read -p "Premi INVIO dopo aver configurato .env per continuare..."
fi

# Avvia l'applicazione
echo ""
echo "🚀 Avvio server..."
echo "→ Apri il browser su: http://localhost:5000"
echo "→ Premi CTRL+C per fermare"
echo ""

python app.py
