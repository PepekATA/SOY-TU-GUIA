def interpret_signal(data):
    """
    Convierte la señal técnica de Finage en:
    - Dirección (sube / baja)
    - Porcentaje de confianza
    - Tiempo estimado de duración
    """
    signal = data.get("signal", "hold")
    confidence = data.get("confidence", 0.75) * 100
    timeframe = data.get("interval", "5m")

    if signal == "buy":
        direction = "Subirá"
        duration = "20 minutos"
    elif signal == "sell":
        direction = "Bajará"
        duration = "15 minutos"
    else:
        direction = "Se mantendrá"
        duration = "10 minutos"

    return {
        "symbol": data.get("symbol", "EUR/USD"),
        "direction": direction,
        "confidence": round(confidence, 2),
        "timeframe": timeframe,
        "duration": duration
    }
