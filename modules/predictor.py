import random
from datetime import datetime, timedelta

TIMEFRAMES = [
    "30 segundos", "1 minuto", "5 minutos", "10 minutos", 
    "15 minutos", "20 minutos", "30 minutos", "1 hora",
    "3 horas", "4 horas", "5 horas", "6 horas", 
    "10 horas", "24 horas", "2 días"
]

def interpret_signal(data, symbol):
    price = data.get("price", 0)
    ask = data.get("ask", price)
    bid = data.get("bid", price)
    
    spread = abs(ask - bid)
    volatility = random.uniform(0.0001, 0.005)
    
    # Análisis técnico simulado
    rsi = random.uniform(20, 80)
    macd = random.uniform(-0.002, 0.002)
    bollinger = random.choice(["upper", "middle", "lower"])
    
    # Predicción principal
    if rsi < 30 and macd > 0:
        main_direction = "📈 SUBIRÁ"
        main_confidence = 85 + random.randint(0, 10)
        main_duration = random.choice(TIMEFRAMES[3:8])
        after_action = "luego se estabilizará"
    elif rsi > 70 and macd < 0:
        main_direction = "📉 BAJARÁ"
        main_confidence = 80 + random.randint(0, 15)
        main_duration = random.choice(TIMEFRAMES[2:7])
        after_action = "luego rebotará"
    else:
        main_direction = "📊 LATERAL"
        main_confidence = 70 + random.randint(0, 15)
        main_duration = random.choice(TIMEFRAMES[1:5])
        after_action = "esperando breakout"
    
    # Predicciones secundarias
    secondary_predictions = []
    for i in range(3):
        timeframe = TIMEFRAMES[random.randint(0, len(TIMEFRAMES)-1)]
        if random.random() > 0.5:
            direction = "Subirá"
            change = f"+{random.uniform(0.0001, 0.01):.4f}"
        else:
            direction = "Bajará"
            change = f"-{random.uniform(0.0001, 0.01):.4f}"
        
        secondary_predictions.append({
            "timeframe": timeframe,
            "direction": direction,
            "change": change,
            "confidence": random.randint(60, 95)
        })
    
    return {
        "symbol": symbol,
        "price": price,
        "main_direction": main_direction,
        "main_confidence": main_confidence,
        "main_duration": main_duration,
        "after_action": after_action,
        "spread": spread,
        "ask": ask,
        "bid": bid,
        "rsi": rsi,
        "macd": macd,
        "bollinger": bollinger,
        "secondary_predictions": secondary_predictions,
        "timestamp": datetime.now().isoformat()
    }
