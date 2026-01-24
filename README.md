# 🤖 AI Automation Generator for Home Assistant

<div align="center">

![Version](https://img.shields.io/badge/version-3.0.0-blue.svg)
![Home Assistant](https://img.shields.io/badge/Home%20Assistant-Compatible-green.svg)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-AI%20Powered-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

**Genera automazioni per Home Assistant usando l'intelligenza artificiale**

*Descrivi in linguaggio naturale cosa vuoi automatizzare e lascia che l'AI generi il codice YAML per te!*

[🚀 Installazione](#-installazione) • [📖 Documentazione](#-utilizzo) • [❓ FAQ](#-faq) • [🐛 Issues](https://github.com/ago1980/ha-ai-automation-generator/issues)

</div>

---

## 📋 Indice

- [Cos'è AI Automation Generator](#-cosè-ai-automation-generator)
- [Caratteristiche Principali](#-caratteristiche-principali)
- [Prerequisiti](#-prerequisiti)
- [Installazione](#-installazione)
- [Configurazione](#️-configurazione)
- [Utilizzo](#-utilizzo)
- [Esempi](#-esempi)
- [FAQ](#-faq)
- [Troubleshooting](#-troubleshooting)
- [Licenza](#-licenza)

---

## 🎯 Cos'è AI Automation Generator

**AI Automation Generator** è un addon per Home Assistant che utilizza l'intelligenza artificiale di **Google Gemini** per generare automazioni in formato YAML partendo da semplici descrizioni in linguaggio naturale.

### Il Problema

Creare automazioni in Home Assistant può essere complesso:
- 📚 Sintassi YAML difficile da ricordare
- 🔍 Documentazione frammentata
- ⏱️ Tempo necessario per scrivere e testare
- 🐛 Errori di sintassi frequenti

### La Soluzione

Con AI Automation Generator:
1. **Descrivi** cosa vuoi fare in italiano
2. **Seleziona** le entità coinvolte (opzionale)
3. **Genera** l'automazione con un click
4. **Carica** direttamente in Home Assistant!

**Niente più YAML da scrivere a mano!** ✨

---

## ✨ Caratteristiche Principali

### 🧠 Intelligenza Artificiale
- Powered by **Google Gemini 2.0 Flash** (gratuito!)
- Comprensione del linguaggio naturale italiano
- Generazione di automazioni complete e funzionanti
- Utilizzo intelligente delle entità selezionate

### 🎨 Interfaccia Moderna
- Design dark elegante con animazioni
- Responsive per desktop e mobile
- Integrazione nativa nella sidebar di Home Assistant
- Tema personalizzato con gradienti cyan/viola

### 🚀 Funzionalità Complete
- **Caricamento entità** automatico da Home Assistant
- **Ricerca e filtro** entità in tempo reale
- **Selezione multipla** di dispositivi e sensori
- **Generazione YAML** istantanea
- **Copia negli appunti** con un click
- **Caricamento diretto** in Home Assistant

### 🔐 Sicurezza
- Autenticazione con password (opzionale)
- Cookie sicuri con HTTPS
- Session management protette
- Compatibile con DuckDNS/SSL

---

## 📋 Prerequisiti

### Obbligatori

- **Home Assistant** v2023.1.0 o superiore
- **Home Assistant OS** o **Supervised**
- **Chiave API Google Gemini** (gratuita)

### Opzionali

- **Password** per proteggere l'accesso
- **DuckDNS** per accesso HTTPS remoto

---

## 📥 Come Ottenere la Chiave API Google

Google Gemini offre una **quota gratuita generosa**:
- ✅ **1500 richieste al giorno** GRATIS
- ✅ Nessuna carta di credito richiesta
- ✅ Perfetto per uso personale

**Steps:**
1. Vai su [Google AI Studio](https://aistudio.google.com/apikey)
2. Accedi con il tuo account Google
3. Click su **"Create API Key"**
4. Copia la chiave (es: `AIzaSyAbc123...`)
5. Incollala nella configurazione dell'addon

---

## 🚀 Installazione

### Metodo 1: Da Repository (Consigliato)

1. **Aggiungi il Repository**
   - Vai in Home Assistant
   - **Impostazioni** → **Componenti aggiuntivi** → **Store**
   - Click **⋮** (tre puntini) → **Repositories**
   - Aggiungi:
     ```
     https://github.com/ago19800/AI-Automation-Generator-Google-Gemini-
     ```
   - Click **"Aggiungi"**

2. **Installa l'Addon**
   - Cerca **"AI Automation Generator"** nello Store
   - Click sull'addon
   - Click **"INSTALLA"**
   - ⏳ Aspetta 5-10 minuti (scarica dipendenze)

3. **Configurazione Iniziale**
   - Vai in **"Configurazione"**
   - Inserisci la tua **Chiave API Google**
   - (Opzionale) Inserisci una **password**
   - Click **"SALVA"**

4. **Avvio**
   - Vai in **"Info"**
   - Abilita:
     - ☑️ **"Avvia all'avvio"**
     - ☑️ **"Mostra nella barra laterale"**
     - ☑️ **"Watchdog"**
   - Click **"AVVIA"**
   - Aspetta stato verde **"Running"**

---

### Metodo 2: Installazione Manuale

Se preferisci installare manualmente:

1. **Scarica** questo repository
2. **Carica** i file in `/addons/ai_automation_generator_google/`

   Struttura:
   ```
   /addons/ai_automation_generator_google/
   ├── config.yaml
   ├── Dockerfile
   ├── build.yaml
   ├── run.sh
   ├── app.py
   ├── requirements.txt
   ├── templates/
   │   ├── index.html
   │   └── login.html
   └── translations/
       └── it.json
   ```

3. **Riavvia** Home Assistant
4. Segui i **passi 2-4** dell'installazione da repository

---

## ⚙️ Configurazione

### Parametri

| Parametro | Tipo | Obbligatorio | Descrizione |
|-----------|------|--------------|-------------|
| `google_api_key` | String | ✅ Sì | Chiave API di Google Gemini ([Ottienila qui](https://aistudio.google.com/apikey)) |
| `password` | String | ⚪ No | Password per proteggere l'accesso (lascia vuoto per accesso libero) |

### Esempio

```yaml
google_api_key: "AIzaSyAbc123def456..."
password: "MiaPasswordSicura2024!"
```

---

## 📖 Utilizzo

### Accesso all'Addon

#### Via Sidebar (Consigliato)
1. Cerca l'icona **🤖** nella sidebar sinistra di Home Assistant
2. Click → Si apre con HTTPS automatico

#### Via Porta Diretta
Accedi a:
```
http://homeassistant.local:8099
```

---

### Creare un'Automazione

#### 1️⃣ Descrivi l'Automazione

Nella casella di testo, descrivi in **italiano** cosa vuoi automatizzare.

**Esempi:**

```
"Quando la temperatura del salotto scende sotto 18 gradi, 
accendi il riscaldamento e inviami una notifica"
```

```
"Ogni mattina alle 7:00 apri le tapparelle della camera 
e accendi la caffettiera"
```

```
"Se rilevo movimento in salotto dopo le 22:00, 
accendi le luci al 30%"
```

```
"Quando la porta del garage rimane aperta per più di 10 minuti, 
inviami una notifica urgente sul telefono"
```

#### 2️⃣ Seleziona le Entità (Opzionale)

- Usa la **barra di ricerca** per trovare dispositivi
- **Click** sulle entità per selezionarle
- Le entità selezionate si evidenziano in **cyan**
- L'AI userà queste entità nella generazione

**Tip:** Seleziona solo le entità rilevanti per risultati più precisi!

#### 3️⃣ Genera

- Click su **"✨ Genera Automazione"**
- Aspetta qualche secondo
- Vedi il codice YAML generato

#### 4️⃣ Usa l'Automazione

Hai **3 opzioni**:

**A) 🚀 Carica Direttamente in Home Assistant**
- Click su **"🚀 Carica in Home Assistant"**
- L'automazione viene creata automaticamente
- Vai in **Impostazioni** → **Automazioni** per vederla
- **Il modo più veloce!** ⚡

**B) 📋 Copia negli Appunti**
- Click su **"📋 Copia negli Appunti"**
- Vai in **Impostazioni** → **Automazioni**
- Click **"+ Crea Automazione"** → **"Modifica in YAML"**
- Incolla il codice

**C) ✏️ Modifica e Personalizza**
- Modifica il YAML nell'editor
- Personalizza secondo le tue esigenze
- Copia e incolla in Home Assistant

---

## 💡 Esempi

### Automazione Temperatura

**Descrizione:**
> "Quando la temperatura scende sotto 18 gradi accendi il riscaldamento"

**YAML Generato:**
```yaml
alias: Accensione Automatica Riscaldamento
trigger:
  - platform: numeric_state
    entity_id: sensor.temperatura_salotto
    below: 18
action:
  - service: climate.turn_on
    target:
      entity_id: climate.riscaldamento
  - service: notify.mobile_app
    data:
      message: "Riscaldamento acceso - temperatura: {{ states('sensor.temperatura_salotto') }}°C"
```

---

### Automazione Movimento Notturno

**Descrizione:**
> "Accendi le luci del salotto quando rilevo movimento dopo le 20:00"

**YAML Generato:**
```yaml
alias: Luci con Movimento Notturno
trigger:
  - platform: state
    entity_id: binary_sensor.movimento_salotto
    to: 'on'
condition:
  - condition: time
    after: '20:00:00'
    before: '06:00:00'
action:
  - service: light.turn_on
    target:
      entity_id: light.salotto
    data:
      brightness_pct: 50
```

---

### Automazione Temporizzata

**Descrizione:**
> "Ogni mattina alle 7:00 apri le tapparelle e accendi la caffettiera"

**YAML Generato:**
```yaml
alias: Risveglio Mattutino
trigger:
  - platform: time
    at: '07:00:00'
action:
  - service: cover.open_cover
    target:
      entity_id: cover.tapparelle_camera
  - delay:
      seconds: 5
  - service: switch.turn_on
    target:
      entity_id: switch.caffettiera
  - service: notify.mobile_app
    data:
      message: "Buongiorno! Caffè in preparazione ☕"
```

---

## ❓ FAQ

### Come ottengo una chiave API Google?

1. Vai su https://aistudio.google.com/apikey
2. Accedi con account Google
3. Click "Create API Key"
4. Copia e incolla nella configurazione

### La chiave API è gratuita?

Sì! Google offre **1500 richieste gratuite al giorno** per Gemini Flash.

### Posso usarlo senza password?

Sì, la password è opzionale. Lascia vuoto per accesso libero.

### Funziona con DuckDNS?

Sì, l'addon supporta HTTPS tramite DuckDNS.

### Posso modificare le automazioni?

Certo! Il YAML generato è completamente modificabile.

### Quante automazioni posso generare?

Illimitate! Limitato solo dalla quota Google (1500/giorno).

### Funziona offline?

No, serve connessione internet per l'API Google Gemini.

### Quali lingue sono supportate?

L'interfaccia è in italiano. Gemini comprende italiano, inglese e molte altre lingue.

---

## 🔧 Troubleshooting

### L'addon non si avvia

**Soluzione:**
1. Controlla i **log** dell'addon
2. **Ricostruisci** l'addon (⋮ → Ricostruisci)
3. Aspetta 10 minuti per build completa

### Errore 404 dalla sidebar

**Soluzione:**
1. Verifica che `ingress: true` sia nel config.yaml
2. Riavvia Home Assistant

### Le entità non si caricano

**Soluzione:**
1. Ricarica la pagina (F5)
2. Controlla log addon
3. Riavvia Home Assistant se necessario

### Errore generazione

**Causa:** Chiave API non valida o quota esaurita

**Soluzione:**
1. Verifica chiave API
2. Controlla quota su https://aistudio.google.com
3. Riprova tra qualche minuto

### Pulsante carica non funziona

**Soluzione:**
1. Verifica che il YAML sia valido
2. Controlla log per errori
3. Usa copia/incolla come alternativa

---

## 🤝 Contribuire

Contributi benvenuti! 

1. **Fork** questo repository
2. Crea un **branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit** (`git commit -m 'Add AmazingFeature'`)
4. **Push** (`git push origin feature/AmazingFeature`)
5. Apri una **Pull Request**

---

## 📄 Licenza

Questo progetto è rilasciato sotto licenza **MIT**. Vedi `LICENSE` per dettagli.

---

## ❤️ Credits

**Progettato con ❤️ da [ago19800](https://github.com/ago19800)**

### Tecnologie

- **[Home Assistant](https://www.home-assistant.io/)** - Piattaforma domotica
- **[Google Gemini](https://ai.google.dev/)** - AI Model
- **[Flask](https://flask.palletsprojects.com/)** - Web Framework
- **[PyYAML](https://pyyaml.org/)** - YAML Parser

### Ringraziamenti

Grazie a:
- La community di **Home Assistant**
- **Google** per l'API Gemini gratuita
- Tutti i **contributors**

---

## 📞 Supporto

Hai problemi o domande?


- ⭐ **Metti una stella** se ti piace!

---

<div align="center">

**Made with ❤️ for the Home Assistant Community**

[⬆ Torna su](#-ai-automation-generator-for-home-assistant)

</div>
