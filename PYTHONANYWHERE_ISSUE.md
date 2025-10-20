# ⚠️ IMPORTANTE: PythonAnywhere ha RESTRIZIONI sui Domini

## 🚨 Problema Scoperto

**PythonAnywhere (piano gratuito) NON può accedere a `ariel.unimi.it`** a causa delle restrizioni sui domini.

Errore che vedrai:
```
HTTPSConnectionPool(host='ariel.unimi.it', port=443): Max retries exceeded 
ProxyError: Unable to connect to proxy - 403 Forbidden
```

---

## ✅ Soluzioni

### **Opzione 1: Render.com (CONSIGLIATA)** 🎯

✅ **GRATUITO** e **SENZA restrizioni**
✅ Deploy automatico da GitHub
✅ 750 ore/mese gratis
✅ Configurazione più semplice

👉 **Leggi la guida**: `RENDER_DEPLOY.md`

**Quick Start:**
1. Carica su GitHub
2. Vai su https://render.com
3. Connetti il repository
4. Deploy automatico! 🚀

---

### **Opzione 2: PythonAnywhere Pagato** 💳

- Account "Hacker": **$5/mese**
- Accesso illimitato a qualsiasi dominio
- 👉 https://www.pythonanywhere.com/pricing/

---

### **Opzione 3: Railway.app** 🚂

- **$5 credito gratuito/mese**
- Nessuna restrizione
- Deploy da GitHub con 1 click
- 👉 https://railway.app

---

### **Opzione 4: Vercel (Solo Frontend)** ⚡

- Frontend su Vercel (gratis)
- Backend su Render (gratis)
- Configurazione più complessa

---

## 🎯 Raccomandazione

**Usa Render.com** - È la soluzione più semplice e completamente gratuita per questo progetto!

Segui la guida: **`RENDER_DEPLOY.md`**

---

## 📋 File da Usare per Render

✅ `Procfile` - Già creato
✅ `render.yaml` - Configurazione automatica
✅ `requirements.txt` - Aggiornato con gunicorn
✅ `RENDER_DEPLOY.md` - Guida completa

---

## 🔄 Migrazione da PythonAnywhere a Render

1. **NON cancellare** il progetto su PythonAnywhere (tienilo come backup)
2. **Segui** `RENDER_DEPLOY.md`
3. **Testa** su Render
4. **Usa** l'URL di Render come principale

---

**Domande?** Leggi `RENDER_DEPLOY.md` per la guida completa! 🚀
