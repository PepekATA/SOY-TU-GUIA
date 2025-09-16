# modules/predictor.py
# Puedes extender esto con lógica adicional de post-procesamiento, backtesting, etc.

def analyze_prediction(prediction):
    """Función de ejemplo para análisis adicional"""
    risk_level = "LOW" if prediction['confidence'] < 70 else "HIGH"
    return {
        **prediction,
        "risk_level": risk_level
    }
