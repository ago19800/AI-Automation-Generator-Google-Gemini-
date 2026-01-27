#!/usr/bin/env python3
from flask import Flask, render_template, request, jsonify, session, redirect
import requests
import os
import json
import google.generativeai as genai
from functools import wraps
from datetime import timedelta
import yaml

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configurazione Sessione per Ingress
app.config.update(
    SESSION_COOKIE_SAMESITE='None',
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_PATH='/',
    SESSION_COOKIE_NAME='ha_ai_session',
    PERMANENT_SESSION_LIFETIME=timedelta(days=7)
)

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
        session.modified = True
        return f(*args, **kwargs)
    return decorated_function

def get_entities():
    """Carica entità da Home Assistant"""
    headers = {
        "Authorization": f"Bearer {SUPERVISOR_TOKEN}",
        "Content-Type": "application/json",
    }
    try:
        response = requests.get(f"{HA_URL}/states", headers=headers, timeout=10)
        return response.json()
    except Exception as e:
        print(f"Errore caricamento entità: {e}")
        return []

def get_services():
    """Carica lista servizi disponibili da HA e converte in dizionario"""
    headers = {
        "Authorization": f"Bearer {SUPERVISOR_TOKEN}",
        "Content-Type": "application/json",
    }
    try:
        response = requests.get(f"{HA_URL}/services", headers=headers, timeout=10)
        services_data = response.json()
        
        # L'API ritorna lista o dizionario a seconda della versione HA
        # Convertiamo sempre in dizionario {domain: {service: data}}
        services_dict = {}
        
        if isinstance(services_data, list):
            # Formato lista (HA più recente)
            for item in services_data:
                domain = item.get('domain', '')
                services = item.get('services', {})
                if domain:
                    services_dict[domain] = services
        elif isinstance(services_data, dict):
            # Formato dizionario (HA più vecchio)
            services_dict = services_data
        
        return services_dict
    except Exception as e:
        print(f"Errore caricamento servizi: {e}")
        return {}

def generate_automation(description, entities):
    """Genera automazione con Gemini"""
    try:
        model = genai.GenerativeModel('gemini-3-flash-preview')
        entities_str = json.dumps(entities[:50], indent=2) if entities else "Nessuna entità selezionata"
        
        prompt = f"""Sei un esperto di Home Assistant. Genera un'automazione YAML basata su questa descrizione:

DESCRIZIONE: {description}

ENTITÀ DISPONIBILI: {entities_str}

REGOLE IMPORTANTI:
1. Restituisci SOLO il codice YAML puro (senza markdown o backticks)
2. Includi sempre: alias, description, trigger, action, mode
3. Per Telegram usa SEMPRE: telegram_bot.send_message (NON notify.telegram!)
4. Per notifiche generiche usa: notify.mobile_app o notify.persistent_notification
5. Usa le entità fornite quando possibile
6. Il YAML deve essere valido e completo

ESEMPI FORMATI CORRETTI:

Telegram (IMPORTANTE - usa telegram_bot.send_message):
action:
  - service: telegram_bot.send_message
    data:
      message: "Il tuo messaggio qui"
      
Telegram con target specifico:
action:
  - service: telegram_bot.send_message
    data:
      message: "Il tuo messaggio"
      target: 123456789

Notifica Mobile App:
action:
  - service: notify.mobile_app
    data:
      message: "Il tuo messaggio qui"
      title: "Titolo opzionale"

Notifica Persistente:
action:
  - service: notify.persistent_notification
    data:
      message: "Notifica visibile in HA"

Luce:
action:
  - service: light.turn_on
    entity_id: light.cucina
    data:
      brightness_pct: 80

Clima:
action:
  - service: climate.set_temperature
    entity_id: climate.riscaldamento
    data:
      temperature: 20

ATTENZIONE: Per Telegram usa SEMPRE "telegram_bot.send_message", MAI "notify.telegram"!

Genera ora l'automazione (SOLO YAML, no markdown):"""
        
        response = model.generate_content(prompt)
        yaml_text = response.text.strip()
        
        # Rimuovi eventuali blocchi markdown
        yaml_text = yaml_text.replace('```yaml', '').replace('```', '').strip()
        
        # Fix automatico se ha usato notify.telegram invece di telegram_bot.send_message
        if 'notify.telegram' in yaml_text:
            print("WARN: Gemini ha usato notify.telegram, correggo in telegram_bot.send_message")
            yaml_text = yaml_text.replace('notify.telegram', 'telegram_bot.send_message')
        
        return yaml_text
    except Exception as e:
        print(f"Errore generazione: {e}")
        import traceback
        traceback.print_exc()
        return f"Errore generazione: {str(e)}"

def test_automation(yaml_text):
    """Testa validità automazione"""
    errors = []
    warnings = []
    entity_errors = {}  # {entity_id: error_message}
    service_errors = {}  # {service: error_message}
    
    try:
        # 1. Valida YAML sintattico
        try:
            automation = yaml.safe_load(yaml_text)
        except yaml.YAMLError as e:
            errors.append(f"YAML non valido: {str(e)}")
            return {
                'valid': False,
                'errors': errors,
                'warnings': warnings,
                'entity_errors': {},
                'service_errors': {}
            }
        
        # 2. Carica entità disponibili
        entity_ids = None  # None = non caricato, [] = caricato ma vuoto
        try:
            available_entities = get_entities()
            entity_ids = [e['entity_id'] for e in available_entities if isinstance(e, dict) and 'entity_id' in e]
            print(f"Caricate {len(entity_ids)} entità da Home Assistant")
        except Exception as e:
            print(f"ERRORE caricamento entità: {e}")
            import traceback
            traceback.print_exc()
            # NON impostare entity_ids = [] perché vogliamo sapere se il caricamento è fallito
            entity_ids = None
            errors.append(f"Impossibile verificare entità: {str(e)}. Il test potrebbe non essere accurato.")
        
        # 3. Carica servizi disponibili
        try:
            available_services = get_services()
        except Exception as e:
            print(f"Errore caricamento servizi: {e}")
            warnings.append(f"Impossibile verificare servizi: {str(e)}")
            available_services = {}
        
        # 4. Controlla triggers
        triggers = automation.get('trigger', [])
        if not isinstance(triggers, list):
            triggers = [triggers]
        
        for trigger in triggers:
            if not isinstance(trigger, dict):
                continue
            entity_id = trigger.get('entity_id')
            if entity_id:
                # Se entity_ids è None, non possiamo verificare (errore già aggiunto sopra)
                # Se entity_ids è lista (anche vuota), verifichiamo
                if entity_ids is not None and entity_id not in entity_ids:
                    entity_errors[entity_id] = f"Entità non trovata in Home Assistant"
                    errors.append(f"Trigger: entità '{entity_id}' non esiste")
        
        # 5. Controlla conditions
        conditions = automation.get('condition', [])
        if conditions:
            if not isinstance(conditions, list):
                conditions = [conditions]
            
            for condition in conditions:
                if not isinstance(condition, dict):
                    continue
                entity_id = condition.get('entity_id')
                if entity_id:
                    if entity_ids is not None and entity_id not in entity_ids:
                        entity_errors[entity_id] = f"Entità non trovata in Home Assistant"
                        errors.append(f"Condition: entità '{entity_id}' non esiste")
        
        # 6. Controlla actions
        actions = automation.get('action', [])
        if not isinstance(actions, list):
            actions = [actions]
        
        for action in actions:
            if not isinstance(action, dict):
                continue
            
            # Controlla entity_id nelle actions
            entity_id = action.get('entity_id')
            if isinstance(entity_id, str):
                if entity_ids is not None and entity_id not in entity_ids:
                    entity_errors[entity_id] = f"Entità non trovata in Home Assistant"
                    errors.append(f"Action: entità '{entity_id}' non esiste")
            elif isinstance(entity_id, list):
                for eid in entity_id:
                    if entity_ids is not None and eid not in entity_ids:
                        entity_errors[eid] = f"Entità non trovata"
                        errors.append(f"Action: entità '{eid}' non esiste")
            
            # Controlla target
            target = action.get('target', {})
            if isinstance(target, dict):
                target_entities = target.get('entity_id')
                if isinstance(target_entities, str):
                    if entity_ids is not None and target_entities not in entity_ids:
                        entity_errors[target_entities] = f"Entità non trovata"
                        errors.append(f"Action target: '{target_entities}' non esiste")
                elif isinstance(target_entities, list):
                    for eid in target_entities:
                        if entity_ids is not None and eid not in entity_ids:
                            entity_errors[eid] = f"Entità non trovata"
                            errors.append(f"Action target: '{eid}' non esiste")
            
            # Controlla servizi (solo se disponibili)
            service = action.get('service')
            if service and available_services:
                # Estrai dominio e servizio (es: light.turn_on)
                if '.' in service:
                    domain, service_name = service.split('.', 1)
                    # Controlla se il servizio esiste
                    domain_services = available_services.get(domain, {})
                    if domain_services and service_name not in domain_services:
                        service_errors[service] = f"Servizio non disponibile"
                        errors.append(f"Servizio '{service}' non disponibile in Home Assistant")  # ✅ ERROR critico!
        
        # 7. Controlla campi obbligatori
        if not automation.get('trigger'):
            errors.append("Manca il campo 'trigger'")
        
        if not automation.get('action'):
            errors.append("Manca il campo 'action'")
        
        # 8. Determina validità
        valid = len(errors) == 0
        
        return {
            'valid': valid,
            'errors': errors,
            'warnings': warnings,
            'entity_errors': entity_errors,
            'service_errors': service_errors
        }
        
    except Exception as e:
        print(f"Errore test_automation: {e}")
        import traceback
        traceback.print_exc()
        return {
            'valid': False,
            'errors': [f"Errore durante il test: {str(e)}"],
            'warnings': [],
            'entity_errors': {},
            'service_errors': {}
        }

def parse_automation_to_graph(yaml_text):
    """Converte YAML automazione in struttura grafo per visualizzazione"""
    try:
        automation = yaml.safe_load(yaml_text)
        
        nodes = []
        edges = []
        node_id = 0
        
        # Nodo START
        nodes.append({
            'id': node_id,
            'label': 'START',
            'type': 'start',
            'icon': '▶️',
            'description': 'Inizio automazione'
        })
        start_id = node_id
        node_id += 1
        
        # TRIGGERS
        triggers = automation.get('trigger', [])
        if not isinstance(triggers, list):
            triggers = [triggers]
        
        trigger_ids = []
        for i, trigger in enumerate(triggers):
            platform = trigger.get('platform', 'unknown')
            entity_id = trigger.get('entity_id', '')
            label = f"{platform}"
            
            # Dettagli specifici per tipo trigger
            if platform == 'time':
                at_time = trigger.get('at', '')
                label = f"⏰ Time\n{at_time}"
            elif platform == 'state':
                to_state = trigger.get('to', '')
                label = f"🔄 State\n{entity_id}\n→ {to_state}"
            elif platform == 'numeric_state':
                above = trigger.get('above', '')
                below = trigger.get('below', '')
                label = f"📊 Numeric\n{entity_id}"
                if above:
                    label += f"\n> {above}"
                if below:
                    label += f"\n< {below}"
            elif platform == 'event':
                event = trigger.get('event_type', '')
                label = f"⚡ Event\n{event}"
            else:
                label = f"🔔 {platform}"
            
            nodes.append({
                'id': node_id,
                'label': label,
                'type': 'trigger',
                'icon': '⏰',
                'entity_id': entity_id,
                'description': json.dumps(trigger, indent=2)
            })
            edges.append({
                'from': start_id,
                'to': node_id,
                'label': 'quando'
            })
            trigger_ids.append(node_id)
            node_id += 1
        
        # Merge triggers se multipli
        if len(trigger_ids) > 1:
            nodes.append({
                'id': node_id,
                'label': 'OR',
                'type': 'logic',
                'icon': '🔀',
                'description': 'Uno qualsiasi dei trigger'
            })
            merge_id = node_id
            for tid in trigger_ids:
                edges.append({
                    'from': tid,
                    'to': merge_id,
                    'label': 'o'
                })
            node_id += 1
            last_node = merge_id
        else:
            last_node = trigger_ids[0] if trigger_ids else start_id
        
        # CONDITIONS
        conditions = automation.get('condition', [])
        if conditions:
            if not isinstance(conditions, list):
                conditions = [conditions]
            
            condition_ids = []
            for i, condition in enumerate(conditions):
                cond_type = condition.get('condition', 'unknown')
                entity_id = condition.get('entity_id', '')
                label = f"✅ {cond_type}"
                
                if cond_type == 'time':
                    after = condition.get('after', '')
                    before = condition.get('before', '')
                    label = f"⏰ Time\n{after} - {before}"
                elif cond_type == 'state':
                    state = condition.get('state', '')
                    label = f"✅ State\n{entity_id}\n= {state}"
                elif cond_type == 'numeric_state':
                    above = condition.get('above', '')
                    below = condition.get('below', '')
                    label = f"✅ Numeric\n{entity_id}"
                    if above:
                        label += f"\n > {above}"
                    if below:
                        label += f"\n < {below}"
                elif cond_type == 'sun':
                    label = f"☀️ Sun\n{condition.get('after', condition.get('before', ''))}"
                
                nodes.append({
                    'id': node_id,
                    'label': label,
                    'type': 'condition',
                    'icon': '✅',
                    'entity_id': entity_id,
                    'description': json.dumps(condition, indent=2)
                })
                edges.append({
                    'from': last_node,
                    'to': node_id,
                    'label': 'se'
                })
                condition_ids.append(node_id)
                node_id += 1
            
            # Merge conditions (AND)
            if len(condition_ids) > 1:
                nodes.append({
                    'id': node_id,
                    'label': 'AND',
                    'type': 'logic',
                    'icon': '🔗',
                    'description': 'Tutte le condizioni devono essere vere'
                })
                merge_id = node_id
                for cid in condition_ids:
                    edges.append({
                        'from': cid,
                        'to': merge_id,
                        'label': 'e'
                    })
                node_id += 1
                last_node = merge_id
            else:
                last_node = condition_ids[0] if condition_ids else last_node
        
        # ACTIONS
        actions = automation.get('action', [])
        if not isinstance(actions, list):
            actions = [actions]
        
        for i, action in enumerate(actions):
            if isinstance(action, dict):
                service = action.get('service', action.get('scene', 'unknown'))
                entity = action.get('entity_id', action.get('target', {}).get('entity_id', ''))
                
                # Determina icona e label
                if 'light' in service:
                    icon = '💡'
                    action_name = 'turn_on' if 'on' in service else 'turn_off'
                elif 'climate' in service or 'heater' in service:
                    icon = '🔥'
                    action_name = service.split('.')[-1]
                elif 'notify' in service:
                    icon = '📱'
                    action_name = 'notify'
                elif 'switch' in service:
                    icon = '🔌'
                    action_name = service.split('.')[-1]
                elif 'cover' in service:
                    icon = '🚪'
                    action_name = service.split('.')[-1]
                elif 'media_player' in service:
                    icon = '🎵'
                    action_name = service.split('.')[-1]
                else:
                    icon = '🎯'
                    action_name = service
                
                label = f"{icon} {action_name}"
                if entity:
                    if isinstance(entity, list):
                        label += f"\n{entity[0]}"
                        if len(entity) > 1:
                            label += f"\n+{len(entity)-1} more"
                    else:
                        label += f"\n{entity}"
                
                nodes.append({
                    'id': node_id,
                    'label': label,
                    'type': 'action',
                    'icon': icon,
                    'entity_id': entity if isinstance(entity, str) else (entity[0] if entity else ''),
                    'service': service,
                    'description': json.dumps(action, indent=2)
                })
                edges.append({
                    'from': last_node,
                    'to': node_id,
                    'label': 'esegui' if i == 0 else 'poi'
                })
                last_node = node_id
                node_id += 1
        
        # Nodo END
        nodes.append({
            'id': node_id,
            'label': 'END',
            'type': 'end',
            'icon': '✅',
            'description': 'Automazione completata'
        })
        edges.append({
            'from': last_node,
            'to': node_id,
            'label': 'fine'
        })
        
        return {
            'nodes': nodes,
            'edges': edges,
            'info': {
                'alias': automation.get('alias', 'Automazione'),
                'description': automation.get('description', ''),
                'mode': automation.get('mode', 'single')
            }
        }
        
    except Exception as e:
        return {
            'error': str(e),
            'nodes': [],
            'edges': []
        }

def explain_automation_with_ai(yaml_text):
    """Usa Gemini per spiegare l'automazione"""
    try:
        # Prova a parsare prima per dare info all'AI
        automation = yaml.safe_load(yaml_text)
        alias = automation.get('alias', 'Automazione')
        description = automation.get('description', '')
        
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        prompt = f"""Analizza questa automazione Home Assistant in modo semplice e chiaro.

AUTOMAZIONE:
{yaml_text}

Rispondi SOLO con un oggetto JSON valido (senza markdown):
{{
    "summary": "Breve spiegazione di cosa fa (1-2 frasi)",
    "triggers": ["lista quando si attiva"],
    "conditions": ["lista condizioni necessarie"],
    "actions": ["lista azioni eseguite"],
    "suggestions": ["2-3 suggerimenti miglioramento"]
}}

IMPORTANTE: Rispondi SOLO con il JSON, senza testo aggiuntivo o markdown."""
        
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        # Rimuovi markdown code blocks se presenti
        if '```json' in text:
            text = text.split('```json')[1].split('```')[0].strip()
        elif '```' in text:
            text = text.split('```')[1].split('```')[0].strip()
        
        # Rimuovi eventuali spazi o newline iniziali/finali
        text = text.strip()
        
        # Prova a parsare
        result = json.loads(text)
        
        # Valida che abbia i campi necessari
        if 'summary' not in result:
            result['summary'] = f"Automazione: {alias}"
        if 'triggers' not in result:
            result['triggers'] = []
        if 'conditions' not in result:
            result['conditions'] = []
        if 'actions' not in result:
            result['actions'] = []
        if 'suggestions' not in result:
            result['suggestions'] = []
        
        return result
        
    except json.JSONDecodeError as e:
        print(f"Errore parsing JSON AI: {e}")
        print(f"Testo ricevuto: {text[:200] if 'text' in locals() else 'N/A'}")
        return {
            'summary': 'L\'automazione sembra valida ma non ho potuto analizzarla in dettaglio.',
            'triggers': ['Verifica i trigger nel YAML'],
            'conditions': [],
            'actions': ['Verifica le azioni nel YAML'],
            'suggestions': ['Usa il test per verificare la validità']
        }
    except Exception as e:
        print(f"Errore AI analysis: {e}")
        import traceback
        traceback.print_exc()
        return {
            'summary': 'Automazione presente ma analisi non disponibile al momento.',
            'triggers': [],
            'conditions': [],
            'actions': [],
            'suggestions': ['Riprova più tardi']
        }

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
            session.clear()
            session['logged_in'] = True
            session.permanent = True
            session.modified = True
            return jsonify({'success': True})
        return jsonify({'success': False, 'error': 'Password errata'}), 401
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('./login')

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/visualize')
@login_required
def visualize():
    return render_template('visualize.html')

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

@app.route('/api/test', methods=['POST'])
@api_login_required
def api_test():
    """Endpoint per testare validità automazione"""
    data = request.json
    yaml_text = data.get('automation', '')
    
    if not yaml_text:
        return jsonify({'error': 'YAML mancante'}), 400
    
    # Testa automazione
    test_result = test_automation(yaml_text)
    
    return jsonify(test_result)

@app.route('/api/execute', methods=['POST'])
@api_login_required
def api_execute():
    """Endpoint per eseguire automazione in modalità test"""
    data = request.json
    yaml_text = data.get('automation', '')
    
    if not yaml_text:
        return jsonify({'error': 'YAML mancante'}), 400
    
    headers = {
        "Authorization": f"Bearer {SUPERVISOR_TOKEN}",
        "Content-Type": "application/json",
    }
    
    try:
        # Parse automazione
        automation = yaml.safe_load(yaml_text)
        
        # Estrai le azioni
        actions = automation.get('action', [])
        if not isinstance(actions, list):
            actions = [actions]
        
        if not actions:
            return jsonify({
                'success': False,
                'error': 'Nessuna azione da eseguire'
            })
        
        # Esegui le azioni una per una
        results = []
        all_success = True
        
        for i, action in enumerate(actions):
            if not isinstance(action, dict):
                # Salta azioni non dict (probabilmente errori di parsing)
                print(f"WARN: Azione {i+1} non è un dizionario, skip")
                continue
            
            # Estrai servizio (supporta vari formati)
            service = action.get('service') or action.get('action')
            
            if not service:
                # Prova a inferire dal tipo di azione
                if 'scene' in action:
                    service = 'scene.turn_on'
                elif 'event' in action:
                    service = 'event.fire'
                else:
                    # Salta silenziosamente azioni senza servizio valido
                    # (probabilmente azioni di delay, wait, ecc)
                    if 'delay' in action or 'wait_template' in action or 'wait_for_trigger' in action:
                        print(f"INFO: Azione {i+1} è wait/delay, skip esecuzione")
                        continue
                    
                    print(f"WARN: Azione {i+1} senza servizio riconosciuto: {action}")
                    # Non aggiungiamo più errore, skippiamo solo
                    continue
            
            # Prepara dati per chiamata servizio
            service_data = {}
            
            # Entity ID (vari formati)
            if 'entity_id' in action:
                service_data['entity_id'] = action['entity_id']
            
            # Target (nuovo formato HA)
            if 'target' in action:
                # Il target va dentro service_data
                target = action['target']
                if isinstance(target, dict):
                    if 'entity_id' in target:
                        service_data['entity_id'] = target['entity_id']
                    if 'device_id' in target:
                        service_data['device_id'] = target['device_id']
                    if 'area_id' in target:
                        service_data['area_id'] = target['area_id']
            
            # Data aggiuntivi (per notifiche, ecc.)
            if 'data' in action:
                # Merge dei data
                action_data = action['data']
                if isinstance(action_data, dict):
                    for key, value in action_data.items():
                        service_data[key] = value
            
            # Scene specifico
            if 'scene' in action:
                service_data['entity_id'] = action['scene']
            
            # Event specifico
            if 'event' in action:
                service_data['event_type'] = action['event']
            
            # Chiama il servizio
            try:
                if '.' in service:
                    domain, service_name = service.split('.', 1)
                else:
                    results.append({
                        'action': service,
                        'success': False,
                        'error': 'Formato servizio non valido (manca dominio)'
                    })
                    all_success = False
                    continue
                
                print(f"Chiamata servizio: {domain}/{service_name}")
                print(f"Dati: {service_data}")
                
                # Timeout dinamico basato sul servizio
                timeout = 30  # Default 30 secondi
                if domain == 'camera':
                    timeout = 60  # Camera record/snapshot possono richiedere più tempo
                elif domain == 'media_player':
                    timeout = 20  # Media player può essere lento
                
                response = requests.post(
                    f"{HA_URL}/services/{domain}/{service_name}",
                    headers=headers,
                    json=service_data,
                    timeout=timeout
                )
                
                print(f"Response status: {response.status_code}")
                print(f"Response text: {response.text[:200] if response.text else 'empty'}")
                
                if response.status_code == 200:
                    # Determina descrizione azione
                    action_desc = service
                    if 'entity_id' in service_data:
                        entity = service_data['entity_id']
                        if isinstance(entity, list):
                            entity = f"{entity[0]} (+{len(entity)-1})" if len(entity) > 1 else entity[0]
                        action_desc = f"{service} → {entity}"
                    elif 'message' in service_data:
                        msg = service_data['message'][:30] + "..." if len(service_data['message']) > 30 else service_data['message']
                        action_desc = f"{service} → \"{msg}\""
                    
                    results.append({
                        'action': action_desc,
                        'success': True,
                        'response': 'Eseguito con successo'
                    })
                else:
                    error_msg = response.text if response.text else f'HTTP {response.status_code}'
                    results.append({
                        'action': service,
                        'success': False,
                        'error': error_msg
                    })
                    all_success = False
                    
            except requests.exceptions.Timeout:
                results.append({
                    'action': service,
                    'success': False,
                    'error': f'Timeout (>{timeout}s) - Il servizio ha impiegato troppo tempo. Potrebbe essere riuscito comunque, controlla i dispositivi.'
                })
                all_success = False
            except requests.exceptions.RequestException as e:
                results.append({
                    'action': service,
                    'success': False,
                    'error': f'Errore connessione: {str(e)}'
                })
                all_success = False
            except Exception as e:
                print(f"Errore esecuzione azione: {e}")
                import traceback
                traceback.print_exc()
                results.append({
                    'action': service,
                    'success': False,
                    'error': str(e)
                })
                all_success = False
        
        return jsonify({
            'success': all_success,
            'results': results,
            'total_actions': len(results)
        })
        
    except yaml.YAMLError as e:
        return jsonify({
            'success': False,
            'error': f'YAML non valido: {str(e)}'
        }), 400
    except Exception as e:
        print(f"Errore execute: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Errore esecuzione: {str(e)}'
        }), 500

@app.route('/api/debug_automations', methods=['GET'])
@api_login_required
def api_debug_automations():
    """Debug endpoint per verificare dove sono le automazioni"""
    try:
        debug_info = {
            'paths_checked': [],
            'files_found': [],
            'file_content': None,
            'ha_config': None
        }
        
        # 1. Controlla vari percorsi possibili
        possible_paths = [
            '/homeassistant/automations.yaml',
            '/config/automations.yaml',
            '/data/automations.yaml',
            '/usr/share/hassio/homeassistant/automations.yaml'
        ]
        
        for path in possible_paths:
            debug_info['paths_checked'].append({
                'path': path,
                'exists': os.path.exists(path),
                'is_file': os.path.isfile(path) if os.path.exists(path) else False,
                'size': os.path.getsize(path) if os.path.exists(path) else 0
            })
            
            if os.path.exists(path):
                debug_info['files_found'].append(path)
        
        # 2. Leggi il file che esiste
        for path in debug_info['files_found']:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    debug_info['file_content'] = {
                        'path': path,
                        'size': len(content),
                        'lines': len(content.split('\n')),
                        'preview': content[:500] if len(content) > 500 else content,
                        'automations_count': len(yaml.safe_load(content)) if content.strip() else 0
                    }
                    break
            except Exception as e:
                debug_info['file_content'] = {
                    'path': path,
                    'error': str(e)
                }
        
        # 3. Controlla configuration.yaml
        config_paths = [
            '/homeassistant/configuration.yaml',
            '/config/configuration.yaml'
        ]
        
        for config_path in config_paths:
            if os.path.exists(config_path):
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config_content = f.read()
                        debug_info['ha_config'] = {
                            'path': config_path,
                            'has_automation_include': 'automation:' in config_content or 'automations.yaml' in config_content,
                            'preview': config_content[:500]
                        }
                        break
                except Exception as e:
                    debug_info['ha_config'] = {
                        'path': config_path,
                        'error': str(e)
                    }
        
        # 4. Controlla automazioni via API HA
        headers = {
            "Authorization": f"Bearer {SUPERVISOR_TOKEN}",
            "Content-Type": "application/json",
        }
        
        try:
            states_response = requests.get(
                f"{HA_URL}/states",
                headers=headers,
                timeout=10
            )
            
            if states_response.status_code == 200:
                states = states_response.json()
                automations = [s for s in states if s.get('entity_id', '').startswith('automation.')]
                debug_info['ha_automations'] = {
                    'count': len(automations),
                    'list': [a.get('attributes', {}).get('friendly_name', a.get('entity_id')) for a in automations[:10]]
                }
        except Exception as e:
            debug_info['ha_automations'] = {
                'error': str(e)
            }
        
        return jsonify(debug_info)
        
    except Exception as e:
        import traceback
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

@app.route('/api/install', methods=['POST'])
@api_login_required
def api_install():
    """Endpoint per installare automazione usando l'API di Home Assistant"""
    data = request.json
    yaml_text = data.get('automation', '')
    
    if not yaml_text:
        return jsonify({'error': 'YAML mancante'}), 400
    
    try:
        # 1. Parse YAML per validazione
        automation = yaml.safe_load(yaml_text)
        
        # 2. Controlla che abbia alias (obbligatorio per identificazione)
        if 'alias' not in automation:
            return jsonify({
                'success': False,
                'error': 'Automazione senza alias. Aggiungi un nome univoco.'
            }), 400
        
        # 3. Assicurati che abbia un ID univoco
        if 'id' not in automation:
            import time
            automation['id'] = f"ai_generated_{int(time.time())}"
            print(f"Aggiunto ID automazione: {automation['id']}")
        
        alias = automation.get('alias', '')
        automation_id = automation.get('id', '')
        
        print(f"Installazione automazione: {alias} (ID: {automation_id})")
        
        # 4. USA L'API DI HOME ASSISTANT per creare l'automazione
        headers = {
            "Authorization": f"Bearer {SUPERVISOR_TOKEN}",
            "Content-Type": "application/json",
        }
        
        # Converti automation in formato API
        # Rimuovi 'id' e 'alias' perché l'API li gestisce diversamente
        automation_config = dict(automation)
        
        # L'API vuole il formato corretto
        api_automation = {
            "alias": alias,
            "description": automation_config.get('description', ''),
            "trigger": automation_config.get('trigger', []),
            "condition": automation_config.get('condition', []),
            "action": automation_config.get('action', []),
            "mode": automation_config.get('mode', 'single')
        }
        
        # Aggiungi campi opzionali se presenti
        if 'variables' in automation_config:
            api_automation['variables'] = automation_config['variables']
        if 'max' in automation_config:
            api_automation['max'] = automation_config['max']
        if 'max_exceeded' in automation_config:
            api_automation['max_exceeded'] = automation_config['max_exceeded']
        
        print(f"Chiamata API per creare automazione...")
        
        # Crea l'automazione via API
        try:
            # Endpoint per creare automazione
            create_response = requests.post(
                f"{HA_URL}/services/automation/reload",
                headers=headers,
                json={},
                timeout=10
            )
            
            print(f"Reload response: {create_response.status_code}")
            
            # METODO ALTERNATIVO: Scrivi via servizio config
            # Proviamo a usare il servizio di configurazione
            config_response = requests.post(
                f"{HA_URL}/config/automation/config/{automation_id}",
                headers=headers,
                json=api_automation,
                timeout=15
            )
            
            print(f"Config API response: {config_response.status_code}")
            print(f"Config API response text: {config_response.text[:200]}")
            
            if config_response.status_code in [200, 201]:
                # Successo!
                return jsonify({
                    'success': True,
                    'message': f'Automazione "{alias}" creata con successo!',
                    'alias': alias,
                    'id': automation_id,
                    'method': 'api',
                    'note': 'Creata tramite API Home Assistant. Vai in Settings → Automations per vederla.'
                })
            else:
                # Prova metodo POST diretto
                print("Tentativo metodo POST automation config...")
                post_response = requests.post(
                    f"{HA_URL}/config/automation/config",
                    headers=headers,
                    json=api_automation,
                    timeout=15
                )
                
                print(f"POST response: {post_response.status_code}")
                
                if post_response.status_code in [200, 201]:
                    return jsonify({
                        'success': True,
                        'message': f'Automazione "{alias}" creata!',
                        'alias': alias,
                        'id': automation_id,
                        'method': 'api_post',
                        'note': 'Vai in Settings → Automations per vederla.'
                    })
                else:
                    return jsonify({
                        'success': False,
                        'error': f'API Home Assistant non disponibile o non autorizzata. Status: {config_response.status_code}',
                        'detail': config_response.text[:200],
                        'workaround': 'Copia il YAML e incollalo manualmente in Home Assistant.'
                    }), 500
                
        except Exception as api_error:
            print(f"Errore API: {api_error}")
            import traceback
            traceback.print_exc()
            
            return jsonify({
                'success': False,
                'error': f'Impossibile creare automazione via API: {str(api_error)}',
                'workaround': 'SOLUZIONE: Copia il YAML e incollalo manualmente in Settings → Automations → Add Automation → Skip → ... → YAML'
            }), 500
        
    except yaml.YAMLError as e:
        print(f"Errore YAML: {e}")
        return jsonify({
            'success': False,
            'error': f'YAML non valido: {str(e)}'
        }), 400
    except Exception as e:
        print(f"Errore install: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Errore installazione: {str(e)}',
            'workaround': 'Copia il YAML manualmente in Home Assistant'
        }), 500

@app.route('/api/visualize', methods=['POST'])
@api_login_required
def api_visualize():
    """Endpoint per generare visualizzazione grafo automazione"""
    data = request.json
    yaml_text = data.get('automation', '')
    
    if not yaml_text:
        return jsonify({'error': 'YAML mancante'}), 400
    
    # Genera grafo
    graph = parse_automation_to_graph(yaml_text)
    
    # Analisi AI
    ai_analysis = explain_automation_with_ai(yaml_text)
    
    return jsonify({
        'graph': graph,
        'analysis': ai_analysis
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8099)
