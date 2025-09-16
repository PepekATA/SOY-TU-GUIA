from modules.ml_agents import ForexPredictor
from modules.finage_client import get_forex_history

predictor = ForexPredictor()

def interpret_signal(data, symbol, timeframe="H1"):
    """
    Genera señal de trading para un par de divisa y timeframe específico.
    """
    price = data.get("price", 0)
    history = get_forex_history(symbol, timeframe)  # ajustar tu cliente para timeframe
    
    prediction = predictor.predict(symbol, price, history, timeframe)

    return {
        "symbol": symbol,
        "timeframe": timeframe,
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
