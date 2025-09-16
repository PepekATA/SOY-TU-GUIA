import numpy as np
import json
import os
import random

class ForexAgent:
    def __init__(self, symbol, timeframe="H1"):
        self.symbol = symbol
        self.timeframe = timeframe
        self.model_path = f"models/{symbol}_{timeframe}.json"
        self.history = []
        self.patterns = self.load_or_create_model()
        
    def load_or_create_model(self):
        os.makedirs("models", exist_ok=True)
        if os.path.exists(self.model_path):
            with open(self.model_path, 'r') as f:
                return json.load(f)
        return self.create_base_patterns()
    
    def create_base_patterns(self):
        return {
            "trend": random.choice(["bullish", "bearish", "neutral"]),
            "volatility": random.uniform(0.001, 0.01),
            "support": 0,
            "resistance": 0,
            "momentum": random.uniform(-1, 1),
            "rsi": random.uniform(30, 70),
            "macd": random.uniform(-0.005, 0.005)
        }
    
    def analyze_price_action(self, current_price, history):
        if len(history) < 10:
            return self.patterns
        
        prices = [h.get("c", current_price) for h in history[-20:]]
        avg_10 = np.mean(prices[-10:])
        avg_20 = np.mean(prices)
        
        self.patterns["momentum"] = (avg_10 - avg_20) / avg_20 * 100
        self.patterns["rsi"] = self.calculate_rsi(prices)
        self.patterns["volatility"] = np.std(prices)
        
        if avg_10 > avg_20:
            self.patterns["trend"] = "bullish"
        elif avg_10 < avg_20:
            self.patterns["trend"] = "bearish"
        else:
            self.patterns["trend"] = "neutral"
            
        return self.patterns
    
    def calculate_rsi(self, prices, period=14):
        if len(prices) < period:
            return 50
        
        deltas = np.diff(prices)
        seed = deltas[:period+1]
        up = seed[seed >= 0].sum() / period
        down = -seed[seed < 0].sum() / period
        
        if down == 0:
            return 100
        rs = up / down
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def predict(self, current_price, history):
        patterns = self.analyze_price_action(current_price, history)
        
        prediction = {
            "symbol": self.symbol,
            "timeframe": self.timeframe,
            "direction": "NEUTRAL",
            "confidence": 50,
            "entry_price": current_price,
            "duration": "5 minutos",
            "target_price": current_price,
            "stop_loss": current_price,
            "reason": []
        }
        
        bull_signals = 0
        bear_signals = 0
        
        # Señales básicas
        if patterns["trend"] == "bullish":
            bull_signals += 2
            prediction["reason"].append("Tendencia alcista")
        elif patterns["trend"] == "bearish":
            bear_signals += 2
            prediction["reason"].append("Tendencia bajista")
        
        if patterns["rsi"] < 30:
            bull_signals += 3
            prediction["reason"].append("RSI sobreventa")
        elif patterns["rsi"] > 70:
            bear_signals += 3
            prediction["reason"].append("RSI sobrecompra")
        
        if patterns["momentum"] > 0.5:
            bull_signals += 2
            prediction["reason"].append("Momentum positivo")
        elif patterns["momentum"] < -0.5:
            bear_signals += 2
            prediction["reason"].append("Momentum negativo")
        
        # Decisión final
        total_signals = bull_signals + bear_signals
        if total_signals > 0:
            if bull_signals > bear_signals:
                prediction["direction"] = "📈 SUBIRÁ"
                prediction["confidence"] = min(95, 50 + (bull_signals * 10))
                change_percent = random.uniform(0.1, 0.5) * (patterns["volatility"] * 100)
                prediction["target_price"] = current_price * (1 + change_percent/100)
                prediction["stop_loss"] = current_price * 0.998
            elif bear_signals > bull_signals:
                prediction["direction"] = "📉 BAJARÁ"
                prediction["confidence"] = min(95, 50 + (bear_signals * 10))
                change_percent = random.uniform(0.1, 0.5) * (patterns["volatility"] * 100)
                prediction["target_price"] = current_price * (1 - change_percent/100)
                prediction["stop_loss"] = current_price * 1.002
        else:
            prediction["direction"] = "📊 LATERAL"
            prediction["confidence"] = 60
            prediction["duration"] = "30 minutos"
            prediction["reason"].append("Sin señales claras")
        
        return prediction
    
    def save_model(self):
        with open(self.model_path, 'w') as f:
            json.dump(self.patterns, f)


class ForexPredictor:
    def __init__(self):
        self.agents = {}
        
    def get_agent(self, symbol, timeframe="H1"):
        key = f"{symbol}_{timeframe}"
        if key not in self.agents:
            self.agents[key] = ForexAgent(symbol, timeframe)
        return self.agents[key]
    
    def predict(self, symbol, price, history, timeframe="H1"):
        agent = self.get_agent(symbol, timeframe)
        return agent.predict(price, history)
