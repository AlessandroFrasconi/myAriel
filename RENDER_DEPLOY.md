# 🚀 Deploy su Render.com (GRATUITO & SENZA RESTRIZIONI)

## ✨ Perché Render invece di PythonAnywhere?

✅ **NESSUNA restrizione sui domini** (può accedere a ariel.unimi.it)
✅ **Deploy automatico da GitHub** (1 click)
✅ **750 ore/mese GRATIS** (sempre attivo)
✅ **HTTPS incluso** con certificato SSL
✅ **Più semplice da configurare**

---

## 📋 Requisiti

- Account GitHub (gratuito)
- Account Render.com (gratuito)

---

## 🎯 GUIDA RAPIDA (10 minuti)

### **1️⃣ Carica il Progetto su GitHub**

```bash
cd /Users/alessandrofrasconi/Desktop/myAriel

# Se non hai ancora inizializzato Git
git init

# Aggiungi tutti i file
git add .
git commit -m "Ready for Render deployment"

# Crea un repository su GitHub e collegalo
# Vai su https://github.com/new
# Crea repo chiamato "myariel" (pubblico o privato)
git remote add origin https://github.com/TUOUSERNAME/myariel.git
git branch -M main
git push -u origin main
```

⚠️ **IMPORTANTE**: NON caricare il file `.env`! È già nel `.gitignore`

---

### **2️⃣ Registrati su Render**

1. Vai su https://render.com
2. Clicca **"Get Started"**
3. Registrati con **GitHub** (autorizza Render ad accedere ai tuoi repo)

---

### **3️⃣ Crea Web Service**

1. Nel dashboard Render, clicca **"New +"** → **"Web Service"**

2. **Connetti il Repository**:
   - Cerca e seleziona `myariel`
   - Clicca **"Connect"**

3. **Configura il Service**:
   ```
   Name:              myariel-app (o quello che vuoi)
   Region:            Frankfurt (EU) - più vicino all'Italia
   Branch:            main
   Runtime:           Python 3
   Build Command:     pip install -r requirements.txt
   Start Command:     gunicorn app:app
   Instance Type:     Free
   ```

4. **Aggiungi Variabili d'Ambiente** (Environment Variables):
   
   Clicca **"Advanced"** → **"Add Environment Variable"**
   
   Aggiungi queste variabili (una per una):
   ```
   MYARIEL_EMAIL=alessandro.frasconi
   MYARIEL_PASSWORD=EniUP31!
   MYARIEL_DOMAIN=@studenti.unimi.it
   SECRET_KEY=una-chiave-segreta-casuale-molto-lunga-123456789
   ```

5. **Deploy!**
   - Clicca **"Create Web Service"**
   - Aspetta 5-10 minuti per il primo deploy
   - Vedrai i log in tempo reale

---

### **4️⃣ Testa l'Applicazione**

Render ti darà un URL tipo:
```
https://myariel-app-abc123.onrender.com
```

Visitalo e dovresti vedere la tua app funzionante! 🎉

---

## ⚙️ Configurazioni Avanzate (Opzionale)

### Auto-Deploy da GitHub

Render fa deploy automaticamente quando fai push su GitHub:

```bash
# Fai modifiche in locale
git add .
git commit -m "Update"
git push

# Render fa deploy automaticamente! 🚀
```

### Health Check

Aggiungi un endpoint di health check in `app.py`:

```python
@app.route('/health')
def health():
    return jsonify({'status': 'ok'}), 200
```

Poi in Render Settings → Health Check:
```
Health Check Path: /health
```

### Dominio Personalizzato (Gratis)

1. Settings → Custom Domain
2. Aggiungi il tuo dominio
3. Configura DNS secondo le istruzioni

---

## 🐛 Troubleshooting

### Deploy fallisce

**Errore: ModuleNotFoundError**
- Verifica `requirements.txt` completo
- Controlla i log di build

**Errore: Application failed to respond**
- Verifica che `gunicorn` sia in `requirements.txt`
- Controlla Start Command: `gunicorn app:app`

### Login fallisce

- Verifica le Environment Variables su Render
- Controlla i log: Dashboard → Logs

### App molto lenta

Il piano free ha **cold starts** (si spegne dopo 15 min di inattività):
- Prima richiesta dopo inattività: 30-60 secondi
- Richieste successive: veloce

Soluzioni:
- Upgrade a piano pagato ($7/mese, sempre attivo)
- Usa un servizio di ping (es. UptimeRobot) per mantenerla attiva

---

## 📊 Limiti Piano Gratuito

- **750 ore/mese** (sempre attivo)
- **Cold starts** dopo 15 minuti di inattività
- **512 MB RAM**
- **Nessun limite sui domini** ✅
- **HTTPS gratuito** ✅

---

## 💡 Alternative

### Railway.app
- $5 credito gratuito/mese
- Deploy con 1 click
- https://railway.app

### Vercel + Serverless
- Frontend gratis
- Backend come Serverless Functions
- Più complesso ma molto veloce

### Fly.io
- 3 VM gratuite
- Buone performance
- https://fly.io

---

## 🔐 Sicurezza

⚠️ **NON committare mai `.env` su GitHub pubblico!**

Se l'hai fatto per errore:
1. Cambia la password su myAriel
2. Rigenera le credenziali
3. Rimuovi il file dalla history Git:
```bash
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all
git push origin --force --all
```

---

## ✅ Checklist Deploy

- [ ] Progetto su GitHub (senza `.env`)
- [ ] Account Render.com creato
- [ ] Repository connesso a Render
- [ ] Environment variables configurate
- [ ] Deploy completato
- [ ] App testata e funzionante
- [ ] Auto-deploy attivato

---

## 🎉 FATTO!

Ora hai la tua app MyAriel su Render, **senza restrizioni sui domini** e con deploy automatico da GitHub!

URL della tua app: `https://tuoapp.onrender.com`

---

**Domande? Problemi?** Controlla i log su Render Dashboard! 🚀
