# 🎓 MyAriel Resource Manager

Un'applicazione web per accedere automaticamente alle risorse di **myAriel** (Università degli Studi di Milano) senza dover fare il login ogni volta!

## ✨ Funzionalità

- 🔐 **Login automatico** a myAriel con credenziali salvate
- 📚 **Organizzazione risorse** per corso e argomento
- 💾 **Sistema di cache** per evitare login continui
- 🔍 **Ricerca intelligente** tra corsi e risorse
- 📱 **Interfaccia responsive** e moderna
- ⚡ **Accesso veloce** a tutti i materiali didattici

## 🚀 Installazione

### Prerequisiti

- Python 3.8 o superiore
- pip (package manager Python)

### Setup

1. **Clona o scarica il progetto**
   ```bash
   cd myAriel
   ```

2. **Crea un ambiente virtuale** (consigliato)
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Su macOS/Linux
   # oppure
   venv\Scripts\activate  # Su Windows
   ```

3. **Installa le dipendenze**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura la chiave segreta** (opzionale)
   
   Copia il file `.env.example` in `.env`:
   ```bash
   cp .env.example .env
   ```
   
   Modifica il file `.env` con una chiave segreta casuale:
   ```env
   SECRET_KEY=una_chiave_segreta_casuale_molto_lunga_123456
   ```
   
   ⚠️ **NOTA**: 
   - Le credenziali MyAriel NON vanno più configurate qui
   - Il login viene fatto tramite interfaccia web
   - La sessione viene salvata in cache per 2 ore

## 🎯 Utilizzo

1. **Avvia l'applicazione**
   ```bash
   python app.py
   ```

2. **Apri il browser** e vai su:
   ```
   http://localhost:5000
   ```

3. **Usa l'applicazione**:
   - Al primo avvio, clicca su "Aggiorna Risorse" per caricare i dati
   - Le risorse vengono salvate in cache per 2 ore
   - Usa la barra di ricerca per trovare corsi o materiali specifici
   - Clicca sui corsi per espandere/comprimere le sezioni

## 📁 Struttura del Progetto

```
myAriel/
├── app.py                 # Backend Flask principale
├── requirements.txt       # Dipendenze Python
├── .env                   # Credenziali (da creare, NON committare!)
├── .env.example          # Template per credenziali
├── .gitignore            # File da ignorare in git
├── README.md             # Questa documentazione
├── templates/
│   └── index.html        # Template HTML principale
├── static/
│   ├── style.css         # Stili CSS
│   └── script.js         # Logica JavaScript frontend
└── cache/                # Directory cache (auto-generata)
    ├── session.pkl       # Sessione salvata
    └── resources.json    # Risorse in cache
```

## 🔧 Funzionalità Avanzate

### Sistema di Cache

- Le **sessioni** vengono salvate per 2 ore
- Le **risorse** vengono salvate in cache JSON
- Usa il pulsante "Aggiorna Risorse" per forzare l'aggiornamento

### API Endpoints

L'applicazione espone diverse API REST:

- `GET /` - Pagina principale
- `POST /api/login` - Login manuale
- `GET /api/courses` - Lista dei corsi
- `GET /api/resources` - Tutte le risorse (con cache)
- `GET /api/resources?refresh=true` - Forza aggiornamento
- `GET /api/course/<id>/resources` - Risorse di un corso specifico

### Ricerca

La ricerca funziona su:
- Nomi dei corsi
- Titoli delle sezioni
- Nomi delle risorse

## 🛡️ Sicurezza

- Le credenziali sono salvate **solo localmente** nel file `.env`
- Il file `.env` è escluso dal controllo versione (`.gitignore`)
- Le sessioni sono salvate in file locali (session_cache.pkl)
- La sessione viene mantenuta per 2 ore dopo il login

## ⚠️ Note Importanti

1. **Login**: Inserisci le tue credenziali alla prima apertura dell'app
2. **Dominio**: Seleziona il dominio corretto (@studenti.unimi.it o @unimi.it)
3. **Cache**: La sessione scade dopo 2 ore di inattività
4. **Rete**: Devi essere connesso a Internet per accedere a myAriel
5. **Privacy**: Le credenziali vengono usate solo per il login e non vengono salvate

## 🐛 Risoluzione Problemi

### "Login fallito"
- Verifica le credenziali inserite
- Prova ad accedere manualmente a myAriel per confermare la password
- Controlla che il dominio selezionato sia corretto
- L'email va inserita SENZA il dominio (es: `nome.cognome` non `nome.cognome@studenti.unimi.it`)

### "Sessione scaduta"
- Effettua nuovamente il login tramite la homepage
- La sessione dura 2 ore dall'ultimo utilizzo

### "Nessuna risorsa trovata"
- Clicca su "Aggiorna Risorse"
- Verifica di essere iscritto ad almeno un corso su myAriel
- Controlla la console del browser (F12) per eventuali errori

### Server non si avvia
- Verifica che le dipendenze siano installate: `pip install -r requirements.txt`
- Controlla che la porta 5000 non sia già in uso
- Attiva l'ambiente virtuale se ne hai creato uno

## 🚀 Sviluppi Futuri

Possibili miglioramenti:
- ⬇️ Download automatico dei file
- 📧 Notifiche per nuove risorse
- 📊 Dashboard con statistiche
- 🗓️ Calendario eventi/scadenze
- 🔔 Sistema di promemoria
- 📱 App mobile

## 📝 Licenza

Questo progetto è per uso personale ed educativo. Rispetta sempre i termini di servizio dell'Università degli Studi di Milano.

## 🤝 Contributi

Sentiti libero di migliorare questo progetto! Apri una issue o invia una pull request.

## ❓ Supporto

Per domande o problemi:
1. Controlla questa documentazione
2. Verifica i log nella console
3. Controlla le impostazioni in `.env`

---

**Fatto con ❤️ per gli studenti dell'Università degli Studi di Milano**
