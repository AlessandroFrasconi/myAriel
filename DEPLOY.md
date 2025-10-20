# MyAriel Resource Manager - Deploy su PythonAnywhere

## 📝 Guida Completa al Deploy

### 1️⃣ Crea un Account PythonAnywhere

1. Vai su https://www.pythonanywhere.com
2. Clicca su "Pricing & signup"
3. Scegli il piano **gratuito** (Beginner)
4. Registrati con email

---

### 2️⃣ Carica i File su PythonAnywhere

#### Opzione A: Upload tramite interfaccia web
1. Nel dashboard, vai su **Files**
2. Crea una cartella `myAriel`
3. Carica tutti i file del progetto:
   - `app.py`
   - `wsgi.py`
   - `requirements.txt`
   - `.env` (con le tue credenziali)
   - Cartella `templates/` (con `index.html`)
   - Cartella `static/` (con `style.css` e `script.js`)

#### Opzione B: Upload tramite Git (consigliato)
```bash
# Sul tuo computer locale, inizializza git (se non l'hai già fatto)
cd /Users/alessandrofrasconi/Desktop/myAriel
git init
git add .
git commit -m "Initial commit"

# Crea un repository su GitHub e push
git remote add origin https://github.com/TUOUSERNAME/myariel.git
git push -u origin main

# Su PythonAnywhere, apri una Bash console e clona
cd ~
git clone https://github.com/TUOUSERNAME/myariel.git
```

⚠️ **IMPORTANTE**: NON caricare il file `.env` su GitHub! Aggiungi un file `.gitignore`:
```
.env
venv/
__pycache__/
*.pyc
cache/
debug_*.html
```

---

### 3️⃣ Configura l'Ambiente Python

1. Nel dashboard, vai su **Consoles** → Apri una **Bash console**
2. Esegui questi comandi:

```bash
# Naviga nella cartella del progetto
cd ~/myAriel

# Crea un virtual environment con Python 3.10
mkvirtualenv --python=/usr/bin/python3.10 myariel

# Installa le dipendenze
pip install -r requirements.txt

# Crea la cartella cache
mkdir -p cache
```

---

### 4️⃣ Configura il File .env

Nella Bash console di PythonAnywhere:

```bash
cd ~/myAriel
nano .env
```

Incolla questo contenuto (con le TUE credenziali):
```
MYARIEL_EMAIL=alessandro.frasconi
MYARIEL_PASSWORD=EniUP31!
MYARIEL_DOMAIN=@studenti.unimi.it
SECRET_KEY=una-chiave-segreta-casuale-molto-lunga-123456789
```

Premi `CTRL+X`, poi `Y`, poi `ENTER` per salvare.

---

### 5️⃣ Configura la Web App

1. Nel dashboard, vai su **Web**
2. Clicca su **Add a new web app**
3. Scegli **Manual configuration** (non "Flask")
4. Scegli **Python 3.10**

#### Configurazione:

**A. Source code:**
```
/home/TUOUSERNAME/myAriel
```

**B. Working directory:**
```
/home/TUOUSERNAME/myAriel
```

**C. WSGI configuration file:**
Clicca sul link del file WSGI e sostituisci TUTTO il contenuto con:

```python
import sys
import os
from dotenv import load_dotenv

# Path del progetto
project_home = '/home/TUOUSERNAME/myAriel'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Carica variabili d'ambiente
dotenv_path = os.path.join(project_home, '.env')
load_dotenv(dotenv_path)

# Importa l'applicazione Flask
from app import app as application
```

⚠️ **Sostituisci TUOUSERNAME** con il tuo username PythonAnywhere!

**D. Virtualenv:**
```
/home/TUOUSERNAME/.virtualenvs/myariel
```

**E. Static files:**
- URL: `/static/`
- Directory: `/home/TUOUSERNAME/myAriel/static`

---

### 6️⃣ Modifica app.py per PythonAnywhere

Nel file `app.py`, trova questa riga alla fine:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

E commentala o rimuovila (PythonAnywhere non usa `app.run()`):
```python
# app.run(debug=True, host='0.0.0.0', port=5001)  # Non necessario su PythonAnywhere
```

---

### 7️⃣ Modifica il Frontend

Nel file `static/script.js`, modifica gli URL delle API.

Cambia da:
```javascript
const url = '/api/resources' + (refresh ? '?refresh=true' : '');
const response = await fetch(url);
```

A:
```javascript
const BASE_URL = ''; // Lascia vuoto se stesso dominio
const url = BASE_URL + '/api/resources' + (refresh ? '?refresh=true' : '');
const response = await fetch(url);
```

Oppure, se vuoi mantenere il backend su PythonAnywhere ma il frontend altrove:
```javascript
const BASE_URL = 'https://TUOUSERNAME.pythonanywhere.com';
```

---

### 8️⃣ Ricarica la Web App

1. Nella pagina **Web**, clicca il grosso pulsante verde **Reload TUOUSERNAME.pythonanywhere.com**
2. Aspetta qualche secondo

---

### 9️⃣ Testa l'Applicazione

Visita: `https://TUOUSERNAME.pythonanywhere.com`

Se tutto funziona, dovresti vedere la tua applicazione! 🎉

---

## 🐛 Debug

### Se vedi errori:

1. **Controlla i log degli errori**:
   - Nella pagina Web, clicca sui link:
     - **Error log**
     - **Server log**

2. **Problemi comuni**:

   **Errore: ModuleNotFoundError**
   ```bash
   workon myariel
   pip install -r requirements.txt
   ```

   **Errore: Permission denied (cache/)**
   ```bash
   cd ~/myAriel
   chmod 755 cache
   ```

   **Errore: ImportError: cannot import name 'app'**
   - Verifica che `app.py` sia nella directory corretta
   - Verifica il path in `wsgi.py`

   **Login fallisce**
   - Verifica che il file `.env` esista e contenga le credenziali corrette
   - Controlla che `python-dotenv` sia installato

3. **Testa manualmente**:
   ```bash
   cd ~/myAriel
   workon myariel
   python app.py
   ```
   Se vedi errori, risolvili prima di ricaricare la web app.

---

## 🔄 Aggiornamenti Futuri

Quando modifichi il codice in locale:

```bash
# Sul tuo computer
git add .
git commit -m "Descrizione modifiche"
git push

# Su PythonAnywhere (Bash console)
cd ~/myAriel
git pull
workon myariel
pip install -r requirements.txt  # Se hai aggiunto dipendenze

# Ricarica la web app dal dashboard Web
```

---

## 📊 Limiti del Piano Gratuito

- **CPU**: 100 secondi/giorno
- **Storage**: 512 MB
- **Dominio**: `tuousername.pythonanywhere.com` (non personalizzabile)
- **HTTPS**: Incluso ✓
- **Sleep**: L'app va in sleep dopo 3 mesi di inattività (basta visitarla per riattivarla)

---

## 🎯 Alternativa: Render.com

Se PythonAnywhere ha problemi o limiti troppo stretti, prova **Render.com**:
- Deploy automatico da GitHub
- 750 ore/mese gratuite
- Dominio personalizzato gratuito
- Più semplice da configurare

Ti serve aiuto anche per Render? 🚀
