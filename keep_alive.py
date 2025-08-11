from flask import Flask, render_template
import threading
import time
import logging

# Create Flask app
app = Flask(__name__)

# Disable Flask's default logging to avoid clutter
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.route('/')
def home():
    """Main route that shows bot status"""
    return render_template('index.html')

@app.route('/ping')
def ping():
    """Health check endpoint"""
    return {'status': 'alive', 'timestamp': int(time.time())}

@app.route('/health')
def health():
    """Health check for monitoring services"""
    return {
        'status': 'healthy',
        'service': 'discord-bot',
        'timestamp': int(time.time())
    }

def run():
    """Run the Flask app"""
    try:
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
    except Exception as e:
        logging.error(f"Errore nel server web: {e}")

def keep_alive():
    """Start the web server in a separate thread"""
    try:
        t = threading.Thread(target=run, daemon=True)
        t.start()
        logging.info("🌐 Server web avviato sulla porta 5000")
    except Exception as e:
        logging.error(f"Errore nell'avvio del server web: {e}")
