# 🤖 AI Automation Generator for Home Assistant

[![GitHub](https://img.shields.io/badge/GitHub-ago1980-blue?logo=github)](https://github.com/ago1980)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-Addon-blue?logo=homeassistant)](https://www.home-assistant.io/)
[![Version](https://img.shields.io/badge/version-2.7.2-green.svg)](https://github.com/ago1980/ha-ai-automation-builder)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> **Genera automazioni Home Assistant con l'intelligenza artificiale di Google Gemini!**  
> Descrivi cosa vuoi in linguaggio naturale, l'AI crea l'automazione, la visualizza con un grafo animato, la testa e la installa automaticamente in Home Assistant!

---

<div align="center">

## ☕ Supporta il Progetto

**Se questo addon ti è utile, offrimi un caffè!**

[![PayPal](https://img.shields.io/badge/PayPal-Dona%20Ora-00457C?logo=paypal&style=for-the-badge)](https://paypal.me/ago19800)

**[paypal.me/ago19800](https://paypal.me/ago19800)**

*Ogni donazione mi aiuta a continuare a sviluppare e migliorare questo addon!* 🙏

</div>

---

## ✨ Caratteristiche Principali

### 🎨 **Interfaccia Premium**
- Design moderno e intuitivo
- Dark mode ottimizzato per Home Assistant
- Animazioni fluide e responsive
- Icone emoji per ogni funzione

### 🤖 **Generazione AI (Google Gemini)**
- Descrivi l'automazione in linguaggio naturale italiano
- AI genera YAML perfetto per Home Assistant
- Supporto per trigger, condition e action complessi
- Intelligenza contestuale basata sulle tue entità

### 🎯 **Grid Entità Visuale**
- Visualizza tutte le entità disponibili
- Filtro intelligente per tipo (light, switch, sensor, ecc.)
- Ricerca testuale rapida
- Selezione multipla con click
- Badge colorati per ogni dominio

### 📊 **AUTOMATION VISION™**
- Grafo animato interattivo con vis.js
- Visualizza flusso dell'automazione
- Nodi colorati per trigger, condition, action
- Collegamenti animati tra i componenti
- Indicatori di stato (verde/rosso)

### 🧪 **Test e Validazione**
- Validazione YAML sintattica
- Verifica esistenza entità in tempo reale
- Controllo disponibilità servizi
- Evidenzia errori critici e warning
- Colora nodi rossi se problemi

### ⚡ **Esecuzione Reale**
- Esegui l'automazione SUBITO (senza installare)
- Testa azioni su dispositivi reali
- Vedi risultati immediati
- Perfetto per debug rapido

### 🧠 **AI Analysis**
- Analisi intelligente dell'automazione
- Spiegazione in linguaggio naturale
- Suggerimenti per miglioramenti
- Powered by Google Gemini

### 💾 **Installazione Automatica**
- Installa automazione direttamente in Home Assistant
- Usa API REST (nessun accesso filesystem richiesto)
- Validazione strict: solo automazioni perfette
- Fallback manuale con copia YAML
- Ricarica automatica in HA

### 🔍 **Debug Avanzato**
- Diagnostica sistema completa
- Conta automazioni attive
- Verifica metodo installazione
- Dettagli tecnici collapsabili

### 🔒 **Sicurezza**
- Password opzionale per protezione
- Token HA sicuro tramite Supervisor
- Ingress integrato (nessuna porta esposta)
- Validazione strict prima installazione
- Impossibile installare automazioni con errori

---

## 🚀 Installazione

### Requisiti

- **Home Assistant** OS, Supervised o Container
- **Google API Key** (Gemini) - [Ottienila qui](https://aistudio.google.com/app/apikey)
- **Supervisor** (per addon)

### Step 1: Aggiungi Repository

1. Vai in **Home Assistant** → **Settings** → **Add-ons**
2. Click **⋮** (tre puntini in alto a destra)
3. Click **Repositories**
4. Aggiungi questo URL:
   ```
   https://github.com/ago1980/ha-ai-automation-builder
   ```
5. Click **ADD**

### Step 2: Installa Addon

1. Cerca **"AI Automation Generator (Google)"**
2. Click sull'addon
3. Click **INSTALL**
4. Attendi il completamento (può richiedere alcuni minuti)

### Step 3: Configurazione

1. Vai nella scheda **Configuration**
2. Inserisci la tua **Google API Key**:
   ```yaml
   google_api_key: "YOUR_GEMINI_API_KEY_HERE"
   ```
3. (Opzionale) Imposta una password:
   ```yaml
   password: "tua_password_sicura"
   ```
4. Click **SAVE**

### Step 4: Avvio

1. Vai nella scheda **Info**
2. Abilita **"Start on boot"** (consigliato)
3. Abilita **"Show in sidebar"** (consigliato)
4. Click **START**
5. Attendi che lo stato diventi **"Running"** (verde)

### Step 5: Accesso

- Click **"OPEN WEB UI"** nell'addon
- Oppure cerca **"AI Automation"** nella sidebar di Home Assistant

---

## 📖 Guida Utilizzo

### 1️⃣ Seleziona Entità (Opzionale ma Consigliato)

1. Nella schermata principale, vedi il **Grid Entità**
2. Usa i **filtri** per tipo: `All`, `Light`, `Switch`, `Sensor`, ecc.
3. Usa la **ricerca** per trovare entità specifiche
4. **Click** sulle entità che vuoi usare (diventano blu)
5. Le entità selezionate vengono inviate all'AI come contesto

**Tip:** Selezionare le entità aiuta l'AI a generare automazioni più accurate!

### 2️⃣ Descrivi l'Automazione

Nella textarea in alto, descrivi cosa vuoi in **linguaggio naturale italiano**:

**Esempi:**

```
Accendi la luce del soggiorno alle ore 20:00
```

```
Quando il sensore di movimento in cucina rileva presenza, 
accendi la luce della cucina se è buio
```

```
Se la temperatura scende sotto 18 gradi, 
accendi il riscaldamento e inviami una notifica su Telegram
```

```
Quando esco di casa (alarm inserito), 
spegni tutte le luci e abbassa il termostato
```

**L'AI capisce:**
- ✅ Orari e date
- ✅ Condizioni (se... allora...)
- ✅ Stati di entità
- ✅ Azioni multiple
- ✅ Notifiche
- ✅ Logica complessa

### 3️⃣ Genera Automazione

1. Click **"🤖 Genera con AI"**
2. Attendi elaborazione (2-5 secondi)
3. L'AI genera il YAML dell'automazione
4. Visualizzi automaticamente il **grafo animato**

### 4️⃣ Visualizza AUTOMATION VISION™

Il grafo mostra:

- **🟢 START:** Inizio automazione
- **🔵 TRIGGER:** Eventi che attivano (es. ore 20:00, movimento rilevato)
- **🟡 CONDITION:** Condizioni da verificare (es. se buio)
- **🟠 ACTION:** Azioni da eseguire (es. accendi luce)
- **⚫ END:** Fine automazione

**Interattivo:**
- Zoom con rotella mouse
- Drag per spostare vista
- Click su nodi per dettagli
- Collegamenti animati mostrano flusso

### 5️⃣ Testa l'Automazione

1. Click **"🧪 Testa Automazione"**
2. Il sistema verifica:
   - ✅ YAML valido sintatticamente
   - ✅ Entità esistono in Home Assistant
   - ✅ Servizi disponibili
   - ✅ Struttura corretta

**Risultati:**

- **✅ VERDE:** Tutto OK, pronta per installazione
- **❌ ROSSO:** Errori critici (entità mancanti, servizi invalidi)
- **⚠️ GIALLO:** Warning (consigliati ma non bloccanti)

**Grafo si aggiorna:**
- Nodi con errori diventano **ROSSI** 🔴
- Nodi OK diventano **VERDI** ✅

### 6️⃣ Esegui Ora (Opzionale)

Prima di installare, puoi **testare dal vivo**:

1. Click **"⚡ Esegui Ora"**
2. L'automazione viene eseguita SUBITO
3. Vedi risultati in tempo reale
4. Perfetto per verificare che funzioni

**Esempio:** Se hai creato "Accendi luce soggiorno", la luce si accende!

### 7️⃣ AI Analysis (Opzionale)

Vuoi capire meglio cosa fa l'automazione?

1. Click **"🧠 Chiedi ad AI"**
2. L'AI analizza l'automazione
3. Spiega in linguaggio naturale:
   - Cosa fa
   - Quando si attiva
   - Quali dispositivi usa
   - Suggerimenti miglioramento

### 8️⃣ Installa in Home Assistant

**IMPORTANTE:** Il pulsante **"💾 Installa in HA"** si abilita **SOLO** se:
- ✅ Test completato
- ✅ ZERO errori critici
- ✅ Tutto VERDE

**Installazione:**

1. Click **"💾 Installa in HA"**
2. Conferma nel popup
3. L'addon usa **API Home Assistant**
4. Automazione installata!

**Verifica:**

1. Vai in **Settings → Automations & Scenes**
2. Cerca l'automazione appena creata
3. È presente e attiva! ✅

**Se installazione automatica fallisce:**

1. Appare pulsante **"📋 Copia YAML"**
2. Click per copiare negli appunti
3. Vai in **Settings → Automations**
4. **Add Automation → Skip**
5. **⋮ → Edit in YAML**
6. Incolla (Ctrl+V)
7. **SAVE**

Fatto! 🎉

### 9️⃣ Debug (Se Problemi)

Se qualcosa non funziona:

1. Click **"🔍 Debug Installazione"**
2. Vedi diagnostica completa:
   - Metodo installazione usato
   - Automazioni attive in HA
   - Stato funzionamento
   - Dettagli tecnici avanzati

---

## 🏗️ Struttura del Progetto

```
ai_automation_generator_google/
│
├── 📄 config.yaml              # Configurazione addon
├── 📄 Dockerfile              # Container Docker
├── 📄 build.yaml              # Build config
├── 📄 run.sh                  # Startup script
├── 📄 requirements.txt        # Dipendenze Python
├── 📄 README.md               # Questa guida
│
├── 🐍 app.py                  # Backend Flask (API)
│   ├── /api/entities          # Lista entità HA
│   ├── /api/services          # Lista servizi HA
│   ├── /api/generate          # Genera automazione con AI
│   ├── /api/test              # Testa validità
│   ├── /api/execute           # Esegui automazione
│   ├── /api/analyze           # Analisi AI
│   ├── /api/install           # Installa in HA
│   └── /api/debug_automations # Diagnostica
│
└── 📁 templates/              # Frontend HTML/JS
    ├── index.html             # Pagina principale
    ├── visualize.html         # Grafo + test + install
    └── login.html             # Login (se password)
```

### File Chiave

#### `config.yaml`
Configurazione dell'addon per Home Assistant:
```yaml
name: AI Automation Generator (Google)
version: "2.7.2"
slug: ai_automation_generator_google
description: Genera automazioni con AI
ingress: true                   # Usa ingress HA
ingress_port: 8099             # Porta interna
homeassistant_api: true        # Accesso API HA
hassio_api: true               # Accesso Supervisor
hassio_role: manager           # Permessi gestione
options:
  google_api_key: ""           # API Key Gemini
  password: ""                 # Password opzionale
```

#### `app.py`
Backend Python Flask:
- Comunica con Home Assistant via **API REST**
- Chiama **Google Gemini** per generazione AI
- Valida YAML e entità
- Installa automazioni via API HA
- Serve frontend HTML/JS

#### `templates/index.html`
Interfaccia principale:
- Grid entità con filtri
- Textarea descrizione
- Pulsante generazione AI
- Design responsive

#### `templates/visualize.html`
Visualizzazione e controlli:
- Grafo animato (vis.js)
- Test validazione
- Esecuzione immediata
- AI Analysis
- Installazione automatica
- Debug sistema

---

## 🔧 Configurazione Avanzata

### Variabili d'Ambiente

L'addon usa queste variabili (gestite automaticamente):

```bash
SUPERVISOR_TOKEN    # Token per API Home Assistant
HA_URL             # URL API HA (http://supervisor/core)
GOOGLE_API_KEY     # Chiave API Gemini (da config)
PASSWORD           # Password opzionale (da config)
```

### Permessi Richiesti

```yaml
homeassistant_api: true   # Leggi/scrivi entità
hassio_api: true         # Accesso Supervisor
hassio_role: manager     # Permessi installazione
```

### Porta e Networking

- **Porta interna:** `8099`
- **Accesso:** Via **Ingress** (nessuna porta esposta)
- **URL:** `http://homeassistant.local:8123/api/hassio_ingress/...`
- **Sicurezza:** Token automatico via Supervisor

### Supporto HTTPS

L'addon **supporta automaticamente HTTPS** tramite Ingress di Home Assistant:

- ✅ Se HA usa HTTPS → Addon usa HTTPS
- ✅ Se HA usa HTTP → Addon usa HTTP
- ✅ Certificati gestiti da Home Assistant
- ✅ Nessuna configurazione necessaria

**Esempio accesso:**
```
https://tuo-homeassistant.duckdns.org:8123/api/hassio_ingress/ai_automation_generator_google
```

---

## 🎯 Esempi Pratici

### Esempio 1: Luce Temporizzata

**Input:**
```
Accendi la luce del soggiorno alle ore 20:00 ogni sera
```

**Output YAML:**
```yaml
alias: Accendi luce soggiorno ore 20
description: Accensione automatica serale
trigger:
  - platform: time
    at: '20:00:00'
condition: []
action:
  - service: light.turn_on
    target:
      entity_id: light.living_room
mode: single
```

**Grafo:**
```
START → ⏰ Time 20:00 → 💡 Turn On Light → END
```

---

### Esempio 2: Movimento con Condizione

**Input:**
```
Quando rilevo movimento in cucina, se è buio (sotto 20 lux), 
accendi la luce della cucina
```

**Output YAML:**
```yaml
alias: Luce cucina con movimento
description: Accensione automatica se buio
trigger:
  - platform: state
    entity_id: binary_sensor.kitchen_motion
    to: 'on'
condition:
  - condition: numeric_state
    entity_id: sensor.kitchen_illuminance
    below: 20
action:
  - service: light.turn_on
    target:
      entity_id: light.kitchen
mode: single
```

**Grafo:**
```
START → 🚶 Motion ON → ❓ Light < 20 → 💡 Turn On → END
```

---

### Esempio 3: Notifica Temperature

**Input:**
```
Se la temperatura scende sotto 18 gradi in camera, 
inviami notifica su Telegram e accendi riscaldamento
```

**Output YAML:**
```yaml
alias: Allarme temperatura bassa
description: Notifica e riscaldamento
trigger:
  - platform: numeric_state
    entity_id: sensor.bedroom_temperature
    below: 18
condition: []
action:
  - service: notify.telegram
    data:
      message: "⚠️ Temperatura camera sotto 18°C!"
  - service: climate.turn_on
    target:
      entity_id: climate.bedroom_heater
mode: single
```

**Grafo:**
```
START → 🌡️ Temp < 18 → 📱 Telegram → 🔥 Heater ON → END
```

---

## ❓ FAQ - Domande Frequenti

### Q: L'addon è gratis?
**A:** Sì! Completamente gratuito e open source. Se ti piace, considera una [donazione ☕](#-supporta-il-progetto)

### Q: Serve Google Gemini API Key?
**A:** Sì, è richiesta. Puoi ottenerla gratuitamente su [Google AI Studio](https://aistudio.google.com/app/apikey). Il tier gratuito include 60 richieste/minuto.

### Q: Funziona offline?
**A:** No, serve connessione internet per:
- Chiamate API Google Gemini
- Comunicazione con Home Assistant (se remoto)

### Q: Supporta altri modelli AI?
**A:** Attualmente solo Google Gemini. Supporto per OpenAI/Claude in futuro.

### Q: Posso modificare il YAML generato?
**A:** Sì! Il YAML è completamente visibile ed editabile prima dell'installazione.

### Q: Le automazioni create sono permanenti?
**A:** Sì! Vengono salvate in Home Assistant come qualsiasi altra automazione.

### Q: Posso cancellare automazioni create?
**A:** Sì, vai in Settings → Automations, trova l'automazione e cancellala.

### Q: Supporta blueprint?
**A:** No, genera automazioni YAML standard, non blueprint.

### Q: Funziona con Home Assistant Core?
**A:** No, richiede Supervisor (HA OS, Supervised, o Container con Supervisor).

### Q: Serve aprire porte sul router?
**A:** No! Usa Ingress, nessuna porta esposta.

### Q: È sicuro?
**A:** Sì! Password opzionale, token HA sicuro, nessun accesso esterno diretto.

### Q: Quante automazioni posso creare?
**A:** Illimitate! Limitato solo da:
- Quota API Gemini (60/min gratuito)
- Spazio Home Assistant

### Q: Posso usare con DuckDNS/Nabu Casa?
**A:** Sì! Funziona con qualsiasi setup HA, anche remoto.

### Q: Supporta altre lingue oltre l'italiano?
**A:** Sì! Puoi descrivere in inglese, spagnolo, francese, ecc. Gemini è multilingua.

---

## 🐛 Risoluzione Problemi

### Problema: Addon non si avvia

**Sintomi:** Stato "Error" o "Stopped"

**Soluzioni:**
1. Controlla i **Logs** dell'addon
2. Verifica che **Google API Key** sia corretta
3. Riavvia l'addon
4. Ricostruisci l'addon: Settings → Add-ons → AI Automation → ⋮ → Rebuild

---

### Problema: "Impossibile verificare entità"

**Sintomi:** Errore durante test automazione

**Soluzioni:**
1. Verifica che **Home Assistant** sia online
2. Controlla permessi addon: `homeassistant_api: true`
3. Riavvia Home Assistant
4. Controlla che token Supervisor sia valido

---

### Problema: Pulsante "Installa" disabilitato

**Sintomi:** Pulsante grigio, non cliccabile

**Cause possibili:**
- ❌ Non hai fatto il test
- ❌ Ci sono errori nell'automazione
- ❌ Entità non esistono

**Soluzioni:**
1. Click **"🧪 Testa Automazione"**
2. Correggi errori evidenziati in rosso
3. Ritest fino a tutto verde
4. Pulsante si abilita automaticamente

---

### Problema: Automazione non appare in HA

**Sintomi:** Installazione OK ma non vedo automazione

**Soluzioni:**
1. Vai in Settings → Automations
2. Click **⋮ → Reload Automations**
3. Fai **F5** sulla pagina
4. Cerca per nome automazione
5. Se ancora non appare, usa **"🔍 Debug"** per diagnostica

---

## 🔄 Aggiornamenti

### Come Aggiornare

1. Vai in **Settings → Add-ons**
2. Cerca **"AI Automation Generator"**
3. Se disponibile aggiornamento, appare badge **"Update available"**
4. Click sull'addon
5. Click **"Update"**
6. Attendi completamento
7. Riavvia addon

### Changelog

#### v2.7.2 (Latest) - 26/01/2025
- 🐛 **Fix:** Bug validazione inconsistente
- 🐛 **Fix:** entity_ids vuoto saltava controlli
- 🔒 **Security:** Impossibile installare con errori
- 📊 **Improved:** Debug positivo e chiaro
- ✨ **Added:** Logging dettagliato caricamento entità

#### v2.7.1 - 26/01/2025
- 🔒 **Security:** Validazione strict pre-installazione
- ⚠️ **Added:** Box rosso blocco installazione
- 💬 **Improved:** Alert specifici per errori
- 🔧 **Changed:** Pulsante abilita solo senza errori

#### v2.7.0 - 26/01/2025
- 📊 **Changed:** Debug ridisegnato (positivo)
- 🎨 **Removed:** X rosse confuse
- ✅ **Added:** Focus su cosa funziona
- 🔧 **Improved:** Dettagli tecnici collassabili

---

## 📄 Licenza

Questo progetto è rilasciato sotto licenza **MIT**.

---

## 🤝 Contributi

I contributi sono benvenuti! 

### Come Contribuire

1. **Fork** il repository
2. Crea **branch** per feature: `git checkout -b feature/NuovaFeature`
3. **Commit** modifiche: `git commit -am 'Add NuovaFeature'`
4. **Push** al branch: `git push origin feature/NuovaFeature`
5. Apri **Pull Request**

---

## 📞 Supporto

### Hai bisogno di aiuto?

- 📖 **Documentazione:** Leggi questa guida
- 🐛 **Bug Report:** [GitHub Issues](https://github.com/ago1980/ha-ai-automation-builder/issues)
- 💬 **Discussioni:** [GitHub Discussions](https://github.com/ago1980/ha-ai-automation-builder/discussions)
- ☕ **Supporto:** [PayPal](https://paypal.me/ago19800)

---

## 🌟 Ringraziamenti

Un grande grazie a:

- **Google** per Gemini API
- **Home Assistant** team per la piattaforma
- **vis.js** per il grafo
- **Flask** per il backend
- **Tutti i contributors** al progetto
- **Tu** per usare questo addon! 🎉

---

<div align="center">

## ☕ Supporta lo Sviluppo

**Se questo addon ti ha fatto risparmiare tempo, considera di offrirmi un caffè!**

[![PayPal](https://img.shields.io/badge/PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/ago19800)

### **[paypal.me/ago19800](https://paypal.me/ago19800)**

Ogni donazione, anche piccola, mi aiuta a:
- 💻 Continuare lo sviluppo
- 🐛 Fixare bug velocemente
- ✨ Aggiungere nuove feature
- 📖 Migliorare documentazione
- ☕ Comprare caffè per coding notturno!

**Grazie di cuore!** ❤️

</div>

---

<div align="center">

**Made with ❤️ by [ago1980](https://github.com/ago1980)**

**Powered by Google Gemini AI**

**For Home Assistant Community**

[![GitHub](https://img.shields.io/badge/GitHub-ago1980-blue?logo=github&style=for-the-badge)](https://github.com/ago1980)
[![PayPal](https://img.shields.io/badge/PayPal-Dona-blue?logo=paypal&style=for-the-badge)](https://paypal.me/ago19800)

</div>
