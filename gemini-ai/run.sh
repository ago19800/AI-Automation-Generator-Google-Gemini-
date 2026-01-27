#!/usr/bin/with-contenv bashio

export GOOGLE_API_KEY=$(bashio::config 'google_api_key')
export PASSWORD=$(bashio::config 'password')
export SUPERVISOR_TOKEN="${SUPERVISOR_TOKEN}"

bashio::log.info "Starting AI Automation Generator v2.1.5..."
bashio::log.info "Google API: $(if [ -n "$GOOGLE_API_KEY" ]; then echo 'OK'; else echo 'MISSING!'; fi)"
bashio::log.info "Password: $(if [ -n "$PASSWORD" ]; then echo 'Enabled'; else echo 'Disabled'; fi)"

exec gunicorn -w 4 -b 0.0.0.0:8099 app:app
