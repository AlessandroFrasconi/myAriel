# 🚀 DEPLOY RENDER - 5 MINUTI

## ⚡ Deploy Veloce (Senza Leggere Guide Lunghe)

### 1. GitHub (2 minuti)
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

### 2. Render (3 minuti)

1. **Vai su** https://render.com → Registrati con GitHub
2. **New +** → **Web Service**
3. **Connect** repository `myariel`
4. **Configura**:
   ```
   Build Command:  pip install -r requirements.txt
   Start Command:  gunicorn app:app
   ```
5. **Add Environment Variable** (4 volte):
   ```
   MYARIEL_EMAIL     = alessandro.frasconi
   MYARIEL_PASSWORD  = EniUP31!
   MYARIEL_DOMAIN    = @studenti.unimi.it
   SECRET_KEY        = stringa-casuale-lunga-123456
   ```
6. **Create Web Service**

### 3. FATTO! ✨

URL: `https://tuoapp.onrender.com`

---

## 🐛 Se Non Funziona

**Errore durante build:**
- Controlla che `requirements.txt` contenga `gunicorn>=21.2.0`

**App non risponde:**
- Aspetta 5-10 minuti per il primo deploy
- Controlla i log: Dashboard → Logs

**Login fallisce:**
- Verifica le variabili d'ambiente su Render
- Password corretta? Email corretta?

---

## 📖 Guide Dettagliate

- **Guida completa**: `RENDER_DEPLOY.md`
- **Problema PythonAnywhere**: `PYTHONANYWHERE_ISSUE.md`

---

**Fatto in 5 minuti!** 🎉
