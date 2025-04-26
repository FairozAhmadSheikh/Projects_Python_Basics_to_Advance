# pip install requests plotly pandas
import requests
import time
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime

def fetch_price(crypto_id):
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies=usd'
    response = requests.get(url)
    return response.json()[crypto_id]['usd']

def track_crypto(crypto_ids, duration=60, interval=5):
    data = {crypto: [] for crypto in crypto_ids}
    timestamps = []

    print(f"⏳ Tracking prices for: {', '.join(crypto_ids)}")

    for _ in range(duration // interval):
        timestamp = datetime.now().strftime('%H:%M:%S')
        timestamps.append(timestamp)
        for crypto in crypto_ids:
            price = fetch_price(crypto)
            print(f"{timestamp} - {crypto}: ${price}")
            data[crypto].append(price)
        time.sleep(interval)

    return timestamps, data

def plot_data(timestamps, data):
    fig = go.Figure()
    for crypto, prices in data.items():
        fig.add_trace(go.Scatter(x=timestamps, y=prices, mode='lines+markers', name=crypto.capitalize()))
    fig.update_layout(title='📈 Live Crypto Price Tracker',
                      xaxis_title='Time',
                      yaxis_title='Price (USD)',
                      template='plotly_dark')
    fig.show()
# Example
crypto_list = ['bitcoin', 'ethereum', 'dogecoin']
timestamps, price_data = track_crypto(crypto_list, duration=60, interval=5)
plot_data(timestamps, price_data)