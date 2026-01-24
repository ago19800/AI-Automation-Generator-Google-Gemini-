#!/usr/bin/with-contenv bashio

# Get configuration
GOOGLE_API_KEY=$(bashio::config 'google_api_key')
PASSWORD=$(bashio::config 'password')

# Export environment variables
export GOOGLE_API_KEY="${GOOGLE_API_KEY}"
export PASSWORD="${PASSWORD}"
export SUPERVISOR_TOKEN="${SUPERVISOR_TOKEN}"

# Log startup
bashio::log.info "Starting AI Automation Generator v3.0 - Dual Mode (Ingress + Port)"
bashio::log.info "Ingress: Enabled (Sidebar HTTPS)"
bashio::log.info "Port: 8099 (Direct Access)"

# Start application
cd /app
exec gunicorn --bind 0.0.0.0:8099 --workers 2 --timeout 120 --access-logfile - --error-logfile - app:app
