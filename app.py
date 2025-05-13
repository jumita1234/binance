from flask import Flask, jsonify, render_template
from binance.client import Client
from dotenv import load_dotenv
import os
import logging

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Configurar logging
logging.basicConfig(level=logging.INFO)

# Obtener claves API desde variables de entorno
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

if not API_KEY or not API_SECRET:
    raise Exception("API_KEY o API_SECRET no están definidos en el entorno")

# Inicializar cliente de Binance
client = Client(API_KEY, API_SECRET)

def get_all_balances():
    balances = {}

    # Saldo Spot
    spot = client.get_account()
    balances['spot'] = [
        {
            'asset': b['asset'],
            'free': float(b['free']),
            'locked': float(b['locked'])
        }
        for b in spot['balances']
        if float(b['free']) > 0 or float(b['locked']) > 0
    ]

    # Saldo Futuros
    try:
        futures = client.futures_account_balance()
        balances['futures'] = [
            {
                'asset': b['asset'],
                'balance': float(b['balance']),
                'availableBalance': float(b['availableBalance'])
            }
            for b in futures
            if float(b['balance']) > 0
        ]
    except Exception as e:
        balances['futures'] = []
        logging.exception("Error al obtener saldo de Futuros")

    # Saldo Margen
    try:
        margin = client.get_margin_account()
        balances['margin'] = [
            {
                'asset': b['asset'],
                'free': float(b['free']),
                'locked': float(b['locked']),
                'borrowed': float(b['borrowed']),
                'interest': float(b['interest'])
            }
            for b in margin['userAssets']
            if float(b['free']) > 0 or float(b['locked']) > 0
        ]
    except Exception as e:
        balances['margin'] = []
        logging.exception("Error al obtener saldo de Margen")

    return balances

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/balances')
def balances():
    try:
        data = get_all_balances()
        return jsonify(data)
    except Exception as e:
        logging.exception("Error al obtener el balance")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
