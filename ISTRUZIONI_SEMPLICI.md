# 🎓 MyAriel Resource Manager - Istruzioni Semplificate

Il sistema di login di myAriel è molto complesso (usa SAML/Shibboleth). Ecco **due metodi** per usare l'applicazione:

## Metodo 1: Login Manuale nel Browser (CONSIGLIATO) ⭐

1. **Avvia l'applicazione**:
   ```bash
   cd /Users/alessandrofrasconi/Desktop/myAriel
   source venv/bin/activate
   python app.py
   ```

2. **Apri** http://localhost:5001 nel browser

3. **Fai login manualmente** a myAriel in un'altra scheda del browser:
   - Vai su https://myariel.unimi.it
   - Fai login normalmente
   
4. **Copia i cookie** (FACILE):
   - Apri gli Strumenti Sviluppatore (F12 o Cmd+Option+I su Mac)
   - Vai nella tab "Console"
   - Incolla questo codice e premi Invio:
   ```javascript
   copy(document.cookie)
   ```
   
5. **Torna all'app** su http://localhost:5001 e:
   - Clicca su "Usa Cookie Browser"
   - Incolla i cookie
   - Clicca "Salva"

6. **Clicca su "Aggiorna Risorse"** e goditi le tue risorse organizzate!

---

## Metodo 2: Estensione Browser (PIÙ AUTOMATICO)

Posso creare un'estensione browser che:
- Si connette automaticamente a myAriel
- Scarica le risorse
- Le salva localmente

Vuoi che crei questa estensione? Dimmi pure!

---

## ❓ Problemi?

### "Credenziali errate"
- Il login SAML di myAriel è complesso
- Usa il Metodo 1 (cookie manuali) per sicuro funzionamento

### "Nessuna risorsa"
- Verifica di essere loggato su myAriel
- Controlla che i cookie siano validi (durano ~2 ore)

### Altro
- Apri una issue su GitHub
- Contattami!

---

💡 **Suggerimento**: Il Metodo 1 è il più affidabile e richiede solo 2 minuti di setup!
