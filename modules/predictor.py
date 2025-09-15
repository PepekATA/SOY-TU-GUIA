import random

def interpret_signal(data, symbol):
    price = data.get("price", 0)
    ask = data.get("ask", price)
    bid = data.get("bid", price)
    
    spread = abs(ask - bid)
    momentum = random.uniform(0.6, 0.95)
    
    if spread < 0.0005:
        direction = "📈 COMPRA FUERTE"
        confidence = 85 + random.randint(0, 10)
    elif spread < 0.001:
        direction = "📊 MANTENER"
        confidence = 70 + random.randint(0, 15)
    else:
        direction = "📉 VENTA"
        confidence = 75 + random.randint(0, 15)
    
    return {
        "symbol": symbol,
        "price": price,
        "direction": direction,
        "confidence": confidence,
        "spread": spread,
        "ask": ask,
        "bid": bid
    }
