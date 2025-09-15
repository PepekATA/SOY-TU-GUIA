from modules.ml_agents import ForexPredictor

predictor = ForexPredictor()

def interpret_signal(data, symbol):
    from modules.finage_client import get_forex_history
    
    price = data.get("price", 0)
    history = get_forex_history(symbol)
    
    # Obtener predicción del agente ML
    prediction = predictor.predict(symbol, price, history)
    
    return {
        "symbol": symbol,
        "price": price,
        "entry_price": prediction["entry_price"],
        "target_price": prediction["target_price"],
        "stop_loss": prediction["stop_loss"],
        "main_direction": prediction["direction"],
        "main_confidence": prediction["confidence"],
        "main_duration": prediction["duration"],
        "reasons": prediction["reason"],
        "spread": abs(data.get("ask", price) - data.get("bid", price)),
        "ask": data.get("ask", price),
        "bid": data.get("bid", price)
    }
