#!/usr/bin/env python3
from flask import Flask, render_template, request, jsonify, session, redirect
import requests
import os
import json
import google.generativeai as genai
from functools import wraps
from datetime import timedelta

app = Flask(__name__)

# --- CONFIGURAZIONE SESSIONE OTTIMIZZATA PER INGRESS ---
app.secret_key = os.urandom(24)
app.config.update(
    SESSION_COOKIE_SAMESITE=None,  # Permetti cross-site per ingress
    SESSION_COOKIE_SECURE=False,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_PATH='/',
    SESSION_COOKIE_NAME='ha_ai_session',
    PERMANENT_SESSION_LIFETIME=timedelta(days=7)  # 7 giorni
)

# Configurazione Ambiente
SUPERVISOR_TOKEN = os.environ.get('SUPERVISOR_TOKEN', '')
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY', '')
PASSWORD = os.environ.get('PASSWORD', '')
HA_URL = 'http://supervisor/core/api'

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not PASSWORD:
            return f(*args, **kwargs)
        if not session.get('logged_in'):
            return redirect('./login')
        # Rinnova session ad ogni richiesta
        session.modified = True
        return f(*args, **kwargs)
    return decorated_function

def api_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not PASSWORD:
            return f(*args, **kwargs)
        if not session.get('logged_in'):
            return jsonify({'error': 'Non autenticato'}), 401
        # Rinnova session ad ogni richiesta
        session.modified = True
        return f(*args, **kwargs)
    return decorated_function

def get_entities():
    headers = {
        "Authorization": f"Bearer {SUPERVISOR_TOKEN}",
        "Content-Type": "application/json",
    }
    try:
        response = requests.get(f"{HA_URL}/states", headers=headers, timeout=10)
        return response.json()
    except Exception:
        return []

def generate_automation(description, entities):
    model = genai.GenerativeModel('gemini-3-flash-preview')
    entities_str = json.dumps(entities[:50], indent=2)
    prompt = f"""
    Sei un esperto di Home Assistant. Genera un'automazione YAML basata su: "{description}"
    Usa queste entità: {entities_str}
    Restituisci SOLO il codice YAML puro, senza blocchi markdown.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Errore generazione: {str(e)}"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if not PASSWORD:
        session.clear()
        session['logged_in'] = True
        session.permanent = True
        session.modified = True
        return redirect('./')
    
    if request.method == 'POST':
        password = request.json.get('password', '')
        if password == PASSWORD:
            # Pulisci completamente la sessione vecchia
            session.clear()
            # Imposta nuova sessione
            session['logged_in'] = True
            session.permanent = True
            session.modified = True
            
            # Aggiungi header per forzare il salvataggio cookie
            response = jsonify({'success': True})
            response.set_cookie(
                'ha_ai_session',
                value='logged_in',
                max_age=604800,  # 7 giorni
                path='/',
                samesite=None,
                secure=False,
                httponly=False  # Permetti accesso JS
            )
            return response
        return jsonify({'success': False, 'error': 'Password errata'}), 401
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    response = redirect('./login')
    response.delete_cookie('ha_ai_session', path='/')
    return response

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/api/entities', methods=['GET'])
@api_login_required
def api_entities():
    return jsonify(get_entities())

@app.route('/api/generate', methods=['POST'])
@api_login_required
def api_generate():
    data = request.json
    description = data.get('description', '')
    selected_entities = data.get('entities', [])
    if not description:
        return jsonify({'error': 'Descrizione mancante'}), 400
    automation = generate_automation(description, selected_entities)
    return jsonify({'automation': automation})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8099)
