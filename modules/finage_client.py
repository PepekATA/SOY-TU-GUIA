import requests
import os

API_KEY = os.getenv("FINAGE_API_KEY")
BASE_URL = "https://api.finage.co.uk/forex/signal"

def get_forex_signal(symbol: str):
    """Llama a la API de Finage para obtener señales de predicción Forex"""
    url = f"{BASE_URL}?symbol={symbol}&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data
