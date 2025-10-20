# 🎯 GUIDA RAPIDA: Deploy Online

## ⚠️ IMPORTANTE: PythonAnywhere NON Funziona!

**PythonAnywhere gratuito** ha restrizioni e **NON può accedere a ariel.unimi.it**.

## ✅ SOLUZIONE: Usa Render.com (GRATIS)

**Render.com** è:
- ✅ Completamente **GRATUITO**
- ✅ **Nessuna restrizione** sui domini
- ✅ Deploy **automatico da GitHub**
- ✅ **Più semplice** di PythonAnywhere

---

## 📦 Cosa hai ora:

✅ **Backend Flask** (`app.py`) - Funzionante
✅ **Frontend** (`templates/`, `static/`) - Responsive
✅ **Procfile** - Configurazione Render
✅ **render.yaml** - Deploy automatico
✅ **Requirements** - Con gunicorn incluso
✅ **Guide complete** - 3 guide disponibili

---

## 🚀 QUICK START - Deploy su Render (5 minuti)

### 1️⃣ GitHub (2 minuti)

```bash
cd /Users/alessandrofrasconi/Desktop/myAriel
git init
git add .
git commit -m "Deploy to Render"
```

Vai su https://github.com/new → Crea repo "myariel"

```bash
git remote add origin https://github.com/TUOUSERNAME/myariel.git
git push -u origin main
```

### 2️⃣ Render (3 minuti)

1. **Registrati**: https://render.com (con GitHub)
2. **New +** → **Web Service**
3. **Connect repository**: Seleziona `myariel`
4. **Configura**:
   ```
   Name:           myariel-app
   Build Command:  pip install -r requirements.txt
   Start Command:  gunicorn app:app
   Plan:           Free
   ```
5. **Environment Variables** (Add 4 volte):
   ```
   MYARIEL_EMAIL     = alessandro.frasconi
   MYARIEL_PASSWORD  = EniUP31!
   MYARIEL_DOMAIN    = @studenti.unimi.it
   SECRET_KEY        = stringa-casuale-lunga-123456
   ```
6. **Create Web Service**

### 3️⃣ Aspetta (5-10 minuti)

Render fa il build e deploy automaticamente. Guarda i log in tempo reale.

---

## 🎉 FATTO!

Visita: `https://myariel-app-abc123.onrender.com`

⚠️ **Primo accesso**: Può impiegare 30-60 secondi (cold start)

---

## 🐛 Se Qualcosa Va Male

### Controlla i Log:
- Dashboard Web → **Error log**
- Dashboard Web → **Server log**

### Problemi Comuni:

**1. "ModuleNotFoundError: No module named 'flask'"**
```bash
workon myariel
pip install -r requirements.txt
```

**2. "Login fallito"**
- Verifica che `.env` esista in `/home/TUOUSERNAME/myAriel/.env`
- Controlla le credenziali nel file `.env`

**3. "ImportError: cannot import name 'app'"**
- Verifica il path in `wsgi.py`: `/home/TUOUSERNAME/myAriel`
- Sostituisci `TUOUSERNAME` con il TUO username PythonAnywhere

**4. "Permission denied"**
```bash
cd ~/myAriel
chmod 755 cache
```

### Test Manuale:
```bash
cd ~/myAriel
workon myariel
python
>>> from app import app
>>> # Se non ci sono errori, è OK!
```

---

## 📝 File Importanti da NON Dimenticare

Su PythonAnywhere, crea manualmente `.env`:
```bash
cd ~/myAriel
nano .env
```

Incolla (con le TUE credenziali):
```
MYARIEL_EMAIL=alessandro.frasconi
MYARIEL_PASSWORD=EniUP31!
MYARIEL_DOMAIN=@studenti.unimi.it
SECRET_KEY=cambia-con-stringa-casuale-lunga-123456789
```

Salva: `CTRL+X`, `Y`, `ENTER`

---

## 🔄 Aggiornamenti Futuri

```bash
# Sul tuo computer
git add .
git commit -m "Update"
git push

# Su PythonAnywhere
cd ~/myAriel
git pull
workon myariel
pip install -r requirements.txt

# Reload dalla dashboard Web
```

---

## 💡 Alternative a PythonAnywhere

### Render.com (Più Facile)
- Deploy automatico da GitHub
- Free tier più generoso
- Vai su https://render.com → New → Web Service
- Connetti GitHub → Deploy automatico ✨

### Railway.app
- $5 credito gratuito/mese
- Deploy con 1 click da GitHub
- https://railway.app

### Vercel + Serverless
- Frontend GRATIS su Vercel
- Backend come Serverless Functions
- Più complesso ma molto veloce

---

## 📞 Serve Aiuto?

1. Leggi `DEPLOY.md` per guide dettagliate
2. Controlla i log di errore su PythonAnywhere
3. Verifica che tutte le dipendenze siano installate
4. Testa in locale prima: `python app.py`

---

**🎓 Buon Deploy!** 🚀
