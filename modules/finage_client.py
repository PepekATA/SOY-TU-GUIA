import os
import requests

API_KEY = os.getenv("FINAGE_API_KEY")
BASE_URL = "https://api.finage.co.uk/forex/signal"

def get_forex_signal(symbol: str):
    """Obtiene la señal de predicción de un par de divisas"""
    url = f"{BASE_URL}?symbol={symbol}&apikey={API_KEY}"
    response = requests.get(url)
    return response.json()
