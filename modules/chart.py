# modules/chart.py
import matplotlib.pyplot as plt

def plot_prediction(pair, history, prediction):
    prices = [h['c'] for h in history[-50:]]
    plt.figure(figsize=(12,5))
    plt.plot(prices, label="Precio histórico")
    plt.axhline(prediction['current_price'], color='blue', linestyle='--', label="Actual")
    plt.axhline(prediction['target_price'], color='green', linestyle='--', label="Target")
    plt.axhline(prediction['stop_loss'], color='red', linestyle='--', label="Stop Loss")
    plt.title(f"{pair} - {prediction['direction']}")
    plt.legend()
    plt.grid(True)
    plt.show()
