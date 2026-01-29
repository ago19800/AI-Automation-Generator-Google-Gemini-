#!/usr/bin/with-contenv bashio

# Leggi configurazione
export GOOGLE_API_KEY=$(bashio::config 'google_api_key')

# Verifica API key
if [ -z "$GOOGLE_API_KEY" ]; then
    bashio::log.error "Google API Key non configurata!"
    bashio::log.error "Inserisci la tua API key nelle opzioni dell'addon"
    exit 1
fi

bashio::log.info "Starting AI Automation Generator v2.7.3..."
bashio::log.info "Google API: OK"
bashio::log.info "Password: Disabled ✅"

# Avvia applicazione
cd /
exec gunicorn --bind 0.0.0.0:8099 --workers 4 --timeout 300 app:app
