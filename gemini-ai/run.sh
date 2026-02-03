#!/usr/bin/with-contenv bashio

export GOOGLE_API_KEY=$(bashio::config 'google_api_key')
export SUPERVISOR_TOKEN="${SUPERVISOR_TOKEN}"

if [ -z "$GOOGLE_API_KEY" ]; then
    bashio::log.error "Google API Key non configurata!"
    bashio::log.error "Aggiungi la tua API key nella configurazione dell'addon"
    exit 1
fi

bashio::log.info "Avvio AI Automation Generator v2.7.3..."
bashio::log.info "Google API: OK ✅"
bashio::log.info "Lingua: Italiano 🇮🇹"
bashio::log.info "Autenticazione: Disabilitata (protetto da Ingress HA)"
bashio::log.info "Nuova feature: Editor YAML ✏️"

cd /
exec gunicorn --bind 0.0.0.0:8099 --workers 4 --timeout 300 app:app
