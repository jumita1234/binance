from flask import Flask, render_template
from binance.client import Client

app = Flask(__name__)

API_KEY = '8Laqqio8vD7ZIX8MwEQPninU3X4lZrKIKjgUatY2sfpBrTY92ld6dlFCQpv6LbOp'
API_SECRET = 'aVE4lDtcEf0ejYVI5vV9qQ10qz78cPlaQvp9GxZzc6VSc7Q5U3tkfvDfrxdWTxpV'

client = Client(API_KEY, API_SECRET)

@app.route('/')
def balance():
    info = client.get_account()
    balances = [
        {
            'asset': b['asset'],
            'free': float(b['free']),
            'locked': float(b['locked'])
        }
        for b in info['balances'] if float(b['free']) > 0 or float(b['locked']) > 0
    ]
    return render_template('balance.html', balances=balances)

if __name__ == '__main__':
    app.run()

import os
API_KEY = os.environ.get('API_KEY')
API_SECRET = os.environ.get('API_SECRET')
