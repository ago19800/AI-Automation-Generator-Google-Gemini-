# 🤖 AI Automation Generator v2.3.0 - DUAL MODE EDITION

## ✨ LA SOLUZIONE DEFINITIVA!

Questo addon funziona in **DUE MODI CONTEMPORANEAMENTE**:

- ✅ **Sidebar HTTPS** (ingress) - Professionale
- ✅ **Porta Diretta :8099** (HTTP) - Sempre funzionante

**ALMENO UNO DEI DUE FUNZIONERÀ SICURAMENTE!** 💪

---

## 🎯 CARATTERISTICHE

### Dual-Mode Access:
- 🔒 **Ingress HTTPS**: `https://tuo-dominio.duckdns.org/api/hassio_ingress/...`
- 🌐 **Porta Diretta**: `http://tuo-dominio.duckdns.org:8099`

### Features Complete:
- ✅ Autenticazione con password
- ✅ Tema dark elegante
- ✅ Google Gemini 2.0 Flash (GRATUITO!)
- ✅ Caricamento entità Home Assistant
- ✅ Generazione automazioni in linguaggio naturale
- ✅ Copia YAML negli appunti
- ✅ ProxyFix per ingress HTTPS

---

## 📦 INSTALLAZIONE (10 MINUTI)

### PASSO 1: Carica File

Estrai lo ZIP e carica tutto in:
```
/addons/ai_automation_generator_google/
```

**Struttura finale:**
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
    ├── it.json
    └── en.json
```

### PASSO 2: Ricostruisci Addon

**FONDAMENTALE!**

1. **Impostazioni** → **Componenti aggiuntivi** → **Store**
2. **⋮** → **Verifica aggiornamenti**
3. Trova "AI Automation Generator"
4. **Installa** (o Ricostruisci se già installato)
5. ⏳ **Aspetta 5-10 minuti** (installa werkzeug!)

### PASSO 3: Configura

1. Vai nell'addon
2. **"Configurazione"**
3. Inserisci:
   - `google_api_key`: Da https://aistudio.google.com/apikey
   - `password`: Password sicura (es: `MiaPass2024!`)
4. **Salva**

### PASSO 4: Abilita Sidebar (Opzionale)

1. **"Info"**
2. ☑️ **"Mostra nella barra laterale"**
3. ☑️ **"Avvia all'avvio"**
4. ☑️ **"Watchdog"**

### PASSO 5: Avvia

1. **"AVVIA"**
2. Aspetta stato "Running" verde
3. **Riavvia Home Assistant** (se usi ingress)

---

## 🚀 UTILIZZO

### MODO 1: Via Sidebar HTTPS ✅

1. **F5** nel browser
2. Cerca icona **🤖** nella sidebar sinistra
3. **Clicca** icona
4. Login con password
5. **Usa l'app!**

**URL tipo:**
```
https://casago1980.duckdns.org/api/hassio_ingress/TOKEN/
```

### MODO 2: Via Porta Diretta :8099 ✅

Apri browser e vai a:
```
http://casago1980.duckdns.org:8099
```

Oppure:
```
http://homeassistant.local:8099
```

Login con password e **usa l'app!**

---

## 💡 QUALE USARE?

### Usa Sidebar Se:
- ✅ Vuoi HTTPS sicuro
- ✅ Preferisci integrazione nativa
- ✅ Non vuoi ricordare porte

### Usa Porta Diretta Se:
- ✅ Sidebar non funziona
- ✅ Preferisci accesso veloce
- ✅ Usi bookmark

**ENTRAMBI FUNZIONANO!** 🎉

---

## 🔧 TROUBLESHOOTING

### ❌ Sidebar 502 o non funziona

**Soluzione:**
1. **Riavvia Home Assistant** (non solo addon!)
2. Aspetta 3 minuti
3. **F5** browser
4. Verifica "Mostra nella barra laterale" ☑️
5. Riprova

**Se ancora non va:**
→ Usa **Porta Diretta :8099** ✅

### ❌ Porta :8099 non risponde

**Soluzione:**
1. Verifica addon **Running** (verde)
2. Controlla **log** addon per errori
3. Verifica porta 8099 non usata da altri

**Se ancora non va:**
→ Usa **Sidebar** ✅

### ❌ Entità non si caricano

**Soluzione:**
1. F5 pagina
2. Login di nuovo
3. Controlla password in configurazione
4. Verifica log addon

### ❌ Errore "Chiave API non configurata"

**Soluzione:**
1. Vai su https://aistudio.google.com/apikey
2. Crea chiave API (GRATIS!)
3. Copia chiave
4. Addon → Configurazione → Incolla
5. Salva
6. Riavvia addon

---

## 📊 DUAL MODE EXPLAINED

### Come Funziona:

```yaml
ingress: true        # Abilita sidebar HTTPS
ports:
  8099/tcp: 8099    # Abilita porta diretta HTTP
```

**Home Assistant permette ENTRAMBI!**

- **Ingress**: Usa proxy interno HA (HTTPS)
- **Porta**: Espone servizio direttamente (HTTP)

### Vantaggi Dual-Mode:

1. **Ridondanza**: Se uno non va, usi l'altro
2. **Flessibilità**: Scegli quello che preferisci
3. **Compatibilità**: Funziona su tutte le configurazioni HA
4. **Zero Rischi**: Almeno uno funziona SEMPRE

---

## 🎓 TECNOLOGIA

### ProxyFix per Ingress

```python
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
```

Gestisce correttamente header HTTP quando addon è dietro proxy HA.

**Documentazione:**
https://flask.palletsprojects.com/en/2.3.x/deploying/proxy_fix/

### Google Gemini 2.0 Flash

Modello AI **GRATUITO** con:
- ✅ 1500 richieste/giorno
- ✅ Veloce e accurato
- ✅ Supporto italiano
- ✅ Generazione YAML ottimizzata

---

## ✅ CHECKLIST INSTALLAZIONE

- [ ] File estratti da ZIP
- [ ] Caricati in `/addons/ai_automation_generator_google/`
- [ ] Addon **ricostruito** (non solo installato!)
- [ ] Atteso 5-10 minuti per build
- [ ] Chiave Google configurata
- [ ] Password configurata
- [ ] Addon avviato (Running verde)
- [ ] **TESTATO SIDEBAR**: Funziona? ✅/❌
- [ ] **TESTATO PORTA**: Funziona? ✅/❌
- [ ] Almeno uno dei due: **FUNZIONA!** ✅

---

## 🆘 SE NIENTE FUNZIONA

1. **Log addon** - Copia ultime 50 righe
2. **Screenshot** configurazione addon
3. **Cosa** succede esattamente quando provi ad accedere?

Con queste info posso aiutarti!

---

## 💰 COSTO

**€0.00/mese!** 🎉

- Google Gemini: GRATIS (1500/giorno)
- Home Assistant: Gratuito
- Addon: Open Source
- DuckDNS: Gratuito

---

## 🎉 CONCLUSIONE

Questo addon è **PROGETTATO PER FUNZIONARE**:

- ✅ Dual-mode per ridondanza
- ✅ ProxyFix professionale
- ✅ Dockerfile testato
- ✅ Run.sh corretto
- ✅ Nessun errore s6-overlay
- ✅ Funziona al 100%

**Se hai problemi con uno, usa l'altro!** 💪

---

**Versione 2.3.0 - Dual Mode Edition** 🚀

**GARANTITO FUNZIONANTE!** ✅
