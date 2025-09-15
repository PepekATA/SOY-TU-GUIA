import os
import requests

API_KEY = os.getenv("FINAGE_API_KEY")
BASE_URL = "https://api.finage.co.uk"

def get_forex_signal(symbol: str):
    url = f"{BASE_URL}/last/forex/{symbol}"
    params = {"apikey": API_KEY}
    response = requests.get(url, params=params)
    return response.json()

def get_multiple_signals(symbols: list):
    data = []
    for symbol in symbols:
        try:
            signal = get_forex_signal(symbol)
            data.append(signal)
        except:
            continue
    return data
