#!/bin/bash

# Script per preparare il deploy su PythonAnywhere

echo "🎓 MyAriel - Preparazione Deploy"
echo "================================="
echo ""

# 1. Verifica che .env esista
if [ ! -f .env ]; then
    echo "❌ ERRORE: File .env non trovato!"
    echo "   Copia .env.example in .env e inserisci le tue credenziali:"
    echo "   cp .env.example .env"
    echo "   nano .env"
    exit 1
fi

# 2. Verifica che le dipendenze siano installate
echo "📦 Controllo dipendenze..."
if ! pip freeze | grep -q "Flask"; then
    echo "⚠️  Flask non installato. Installo dipendenze..."
    pip install -r requirements.txt
else
    echo "✓ Dipendenze OK"
fi

# 3. Crea cartella cache se non esiste
if [ ! -d "cache" ]; then
    echo "📁 Creo cartella cache..."
    mkdir cache
    echo "✓ Cartella cache creata"
else
    echo "✓ Cartella cache esiste"
fi

# 4. Test rapido dell'applicazione
echo ""
echo "🧪 Test applicazione..."
python -c "from app import app; print('✓ Importazione OK')" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✓ App importata correttamente"
else
    echo "❌ ERRORE nell'importazione dell'app!"
    echo "   Controlla gli errori con: python app.py"
    exit 1
fi

echo ""
echo "✅ Preparazione completata!"
echo ""
echo "📤 Prossimi passi per il deploy su PythonAnywhere:"
echo "1. Crea account su https://www.pythonanywhere.com (gratuito)"
echo "2. Carica i file o fai git clone del repository"
echo "3. Leggi DEPLOY.md per le istruzioni complete"
echo ""
echo "🚀 Per testare in locale:"
echo "   python app.py"
echo "   Apri http://localhost:5001"
