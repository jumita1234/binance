from flask import Flask, jsonify, render_template
from binance.client import Client
import os
import logging

app = Flask(__name__)

# Configurar logging
logging.basicConfig(level=logging.INFO)

# Cargar claves desde variables de entorno
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

if not API_KEY or not API_SECRET:
    raise Exception("API_KEY o API_SECRET no están definidos en el entorno")

# Inicializar cliente Binance
client = Client(API_KEY, API_SECRET)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/balance')
def get_balance():
    try:
        account_info = client.get_account()
        balances = [
            {
                'asset': b['asset'],
                'free': float(b['free']),
                'locked': float(b['locked'])
            }
            for b in account_info['balances']
            if float(b['free']) > 0 or float(b['locked']) > 0
        ]
        return jsonify(balances)
    except Exception as e:
        logging.exception("Error al obtener el balance")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
