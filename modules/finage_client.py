import os
import requests
from datetime import datetime, timedelta

API_KEY = os.getenv("FINAGE_API_KEY")
BASE_URL = "https://api.finage.co.uk"

def get_forex_signal(symbol: str):
    url = f"{BASE_URL}/last/forex/{symbol}"
    params = {"apikey": API_KEY}
    response = requests.get(url, params=params)
    return response.json()

def get_forex_history(symbol: str):
    end = datetime.now()
    start = end - timedelta(hours=24)
    
    url = f"{BASE_URL}/agg/forex/{symbol}/1/minute/{start.strftime('%Y-%m-%d')}/{end.strftime('%Y-%m-%d')}"
    params = {"apikey": API_KEY, "limit": 100}
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        return data.get("results", [])
    except:
        return []
