import os
import requests
import random
from datetime import datetime, timedelta

API_KEY = os.getenv("FINAGE_API_KEY", "demo")
BASE_URL = "https://api.finage.co.uk"

def get_forex_signal(symbol: str):
    # Simular datos si no hay API key o falla
    try:
        if API_KEY and API_KEY != "demo":
            url = f"{BASE_URL}/last/forex/{symbol}"
            params = {"apikey": API_KEY}
            response = requests.get(url, params=params, timeout=2)
            if response.status_code == 200:
                return response.json()
    except:
        pass
    
    # Datos simulados
    base_prices = {
        "EURUSD": 1.0856, "GBPUSD": 1.2734, "USDJPY": 149.32,
        "AUDUSD": 0.6521, "USDCAD": 1.3612, "USDCHF": 0.8654,
        "NZDUSD": 0.5932, "EURGBP": 0.8523, "EURJPY": 162.03
    }
    
    base = base_prices.get(symbol, 1.0000)
    spread = random.uniform(0.0001, 0.0005)
    
    return {
        "symbol": symbol,
        "price": base + random.uniform(-0.005, 0.005),
        "bid": base - spread,
        "ask": base + spread,
        "timestamp": datetime.now().timestamp()
    }

def get_forex_history(symbol: str):
    history = []
    base = get_forex_signal(symbol)["price"]
    
    for i in range(50):
        change = random.uniform(-0.002, 0.002)
        history.append({
            "c": base + change,
            "h": base + change + random.uniform(0, 0.001),
            "l": base + change - random.uniform(0, 0.001),
            "o": base + change + random.uniform(-0.0005, 0.0005),
            "v": random.randint(10000, 100000),
            "t": (datetime.now() - timedelta(minutes=50-i)).timestamp() * 1000
        })
    
    return history
