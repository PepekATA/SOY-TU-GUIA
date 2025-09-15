def format_predictions(predictions):
    """
    Convierte la predicción cruda en texto entendible para el usuario
    """
    formatted = []
    for p in predictions:
        formatted.append({
            "symbol": p["symbol"],
            "text": f"{p['symbol']} → {p['direction']} en {p['duration']} (Confianza {p['confidence']}%)",
            "confidence": p["confidence"]
        })
    return formatted
