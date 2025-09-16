# modules/ml_agents.py
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.neural_network import MLPRegressor
import xgboost as xgb
import lightgbm as lgb
import os
import joblib
import warnings
warnings.filterwarnings('ignore')

class BaseAgent:
    """Clase base para todos los agentes"""
    def __init__(self, name, pair, timeframe):
        self.name = name
        self.pair = pair
        self.timeframe = timeframe
        self.model = None
        self.scaler = StandardScaler()
        self.performance = {"wins": 0, "losses": 0, "accuracy": 0}
        self.model_path = f"/content/repo/models/{pair}/{name}_{timeframe}.joblib"
        
    def prepare_features(self, history):
        if len(history) < 50:
            return None
        df = pd.DataFrame(history)
        df['returns'] = df['c'].pct_change()
        df['log_returns'] = np.log(df['c'] / df['c'].shift(1))
        df['sma_5'] = df['c'].rolling(5).mean()
        df['sma_10'] = df['c'].rolling(10).mean()
        df['sma_20'] = df['c'].rolling(20).mean()
        df['ema_9'] = df['c'].ewm(span=9).mean()
        df['ema_21'] = df['c'].ewm(span=21).mean()
        
        delta = df['c'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        
        df['macd'] = df['c'].ewm(span=12).mean() - df['c'].ewm(span=26).mean()
        df['macd_signal'] = df['macd'].ewm(span=9).mean()
        df['macd_diff'] = df['macd'] - df['macd_signal']
        
        df['bb_middle'] = df['c'].rolling(20).mean()
        bb_std = df['c'].rolling(20).std()
        df['bb_upper'] = df['bb_middle'] + (bb_std * 2)
        df['bb_lower'] = df['bb_middle'] - (bb_std * 2)
        df['bb_width'] = df['bb_upper'] - df['bb_lower']
        df['bb_position'] = (df['c'] - df['bb_lower']) / df['bb_width']
        
        df['volatility'] = df['returns'].rolling(20).std()
        df['atr'] = self.calculate_atr(df)
        
        if 'v' in df.columns:
            df['volume_ratio'] = df['v'] / df['v'].rolling(20).mean()
            df['volume_trend'] = df['v'].rolling(5).mean() / df['v'].rolling(20).mean()
        
        df['high_low_ratio'] = df['h'] / df['l']
        df['close_open_ratio'] = df['c'] / df['o']
        df['momentum_3'] = df['c'] / df['c'].shift(3) - 1
        df['momentum_5'] = df['c'] / df['c'].shift(5) - 1
        df['momentum_10'] = df['c'] / df['c'].shift(10) - 1
        
        df = df.dropna()
        if len(df) == 0:
            return None
            
        feature_cols = [
            'returns', 'log_returns', 'sma_5', 'sma_10', 'sma_20',
            'ema_9', 'ema_21', 'rsi', 'macd', 'macd_signal', 'macd_diff',
            'bb_position', 'bb_width', 'volatility', 'atr',
            'high_low_ratio', 'close_open_ratio',
            'momentum_3', 'momentum_5', 'momentum_10'
        ]
        if 'volume_ratio' in df.columns:
            feature_cols.extend(['volume_ratio', 'volume_trend'])
        
        return df[feature_cols].iloc[-1:].values
    
    def calculate_atr(self, df, period=14):
        high_low = df['h'] - df['l']
        high_close = np.abs(df['h'] - df['c'].shift())
        low_close = np.abs(df['l'] - df['c'].shift())
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = np.max(ranges, axis=1)
        return true_range.rolling(period).mean()
    
    def save(self):
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler,
            'performance': self.performance,
            'name': self.name,
            'pair': self.pair,
            'timeframe': self.timeframe
        }, self.model_path)
    
    def load(self):
        if os.path.exists(self.model_path):
            data = joblib.load(self.model_path)
            self.model = data['model']
            self.scaler = data['scaler']
            self.performance = data['performance']
            return True
        return False

class TrendAgent(BaseAgent):
    def __init__(self, pair, timeframe):
        super().__init__("TrendAgent", pair, timeframe)
        self.model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
    
    def predict(self, current_price, history):
        features = self.prepare_features(history)
        if features is None:
            return {"agent": self.name, "direction": "NEUTRAL", "confidence": 0}
        try:
            features_scaled = self.scaler.transform(features)
            prediction = self.model.predict(features_scaled)[0]
            if prediction > current_price * 1.001:
                direction = "BUY"
                confidence = min(95, abs(prediction - current_price) / current_price * 10000)
            elif prediction < current_price * 0.999:
                direction = "SELL"
                confidence = min(95, abs(current_price - prediction) / current_price * 10000)
            else:
                direction = "HOLD"
                confidence = 50
            return {
                "agent": self.name,
                "direction": direction,
                "confidence": confidence,
                "predicted_price": prediction
            }
        except Exception:
            return {"agent": self.name, "direction": "NEUTRAL", "confidence": 0}

class MomentumAgent(BaseAgent):
    def __init__(self, pair, timeframe):
        super().__init__("MomentumAgent", pair, timeframe)
        self.model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=5)
    
    def predict(self, current_price, history):
        features = self.prepare_features(history)
        if features is None:
            return {"agent": self.name, "direction": "NEUTRAL", "confidence": 0}
        try:
            df = pd.DataFrame(history)
            momentum = df['c'].pct_change(5).iloc[-1]
            rsi = self.calculate_rsi(df['c'])
            features_scaled = self.scaler.transform(features)
            prediction = self.model.predict(features_scaled)[0]
            if momentum > 0.002 and rsi < 70:
                direction = "BUY"
                confidence = min(90, momentum * 10000)
            elif momentum < -0.002 and rsi > 30:
                direction = "SELL"
                confidence = min(90, abs(momentum) * 10000)
            else:
                direction = "HOLD"
                confidence = 40
            return {
                "agent": self.name,
                "direction": direction,
                "confidence": confidence,
                "momentum": momentum,
                "rsi": rsi
            }
        except Exception:
            return {"agent": self.name, "direction": "NEUTRAL", "confidence": 0}
    
    def calculate_rsi(self, prices, period=14):
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs)).iloc[-1]

class VolatilityAgent(BaseAgent):
    def __init__(self, pair, timeframe):
        super().__init__("VolatilityAgent", pair, timeframe)
        self.model = xgb.XGBRegressor(n_estimators=100, max_depth=6, learning_rate=0.01)
    
    def predict(self, current_price, history):
        features = self.prepare_features(history)
        if features is None:
            return {"agent": self.name, "direction": "NEUTRAL", "confidence": 0}
        try:
            df = pd.DataFrame(history)
            volatility = df['c'].pct_change().std()
            atr = self.calculate_atr(df).iloc[-1]
            sma = df['c'].rolling(20).mean().iloc[-1]
            std = df['c'].rolling(20).std().iloc[-1]
            upper_band = sma + (2 * std)
            lower_band = sma - (2 * std)
            if current_price <= lower_band and volatility < 0.01:
                direction = "BUY"
                confidence = 85
            elif current_price >= upper_band and volatility < 0.01:
                direction = "SELL"
                confidence = 85
            else:
                direction = "HOLD"
                confidence = 60
            return {
                "agent": self.name,
                "direction": direction,
                "confidence": confidence,
                "volatility": volatility,
                "atr": atr
            }
        except Exception:
            return {"agent": self.name, "direction": "NEUTRAL", "confidence": 0}

class PatternAgent(BaseAgent):
    def __init__(self, pair, timeframe):
        super().__init__("PatternAgent", pair, timeframe)
        self.model = MLPRegressor(hidden_layer_sizes=(100, 50), max_iter=1000)
    
    def detect_patterns(self, df):
        patterns = []
        if abs(df['c'].iloc[-1] - df['o'].iloc[-1]) < (df['h'].iloc[-1] - df['l'].iloc[-1]) * 0.1:
            patterns.append("DOJI")
        body = abs(df['c'].iloc[-1] - df['o'].iloc[-1])
        lower_shadow = min(df['c'].iloc[-1], df['o'].iloc[-1]) - df['l'].iloc[-1]
        if lower_shadow > body * 2:
            patterns.append("HAMMER")
        if len(df) > 1:
            prev_body = abs(df['c'].iloc[-2] - df['o'].iloc[-2])
            curr_body = abs(df['c'].iloc[-1] - df['o'].iloc[-1])
            if curr_body > prev_body * 1.5:
                if df['c'].iloc[-1] > df['o'].iloc[-1] and df['c'].iloc[-2] < df['o'].iloc[-2]:
                    patterns.append("BULLISH_ENGULFING")
                elif df['c'].iloc[-1] < df['o'].iloc[-1] and df['c'].iloc[-2] > df['o'].iloc[-2]:
                    patterns.append("BEARISH_ENGULFING")
        return patterns
    
    def predict(self, current_price, history):
        if len(history) < 20:
            return {"agent": self.name, "direction": "NEUTRAL", "confidence": 0}
        try:
            df = pd.DataFrame(history)
            patterns = self.detect_patterns(df)
            if "BULLISH_ENGULFING" in patterns or "HAMMER" in patterns:
                direction = "BUY"
                confidence = 80
            elif "BEARISH_ENGULFING" in patterns:
                direction = "SELL"
                confidence = 80
            elif "DOJI" in patterns:
                direction = "HOLD"
                confidence = 70
            else:
                direction = "NEUTRAL"
                confidence = 50
            return {
                "agent": self.name,
                "direction": direction,
                "confidence": confidence,
                "patterns": patterns
            }
        except Exception:
            return {"agent": self.name, "direction": "NEUTRAL", "confidence": 0}

class ScalpingAgent(BaseAgent):
    def __init__(self, pair, timeframe):
        super().__init__("ScalpingAgent", pair, timeframe)
        self.model = lgb.LGBMRegressor(n_estimators=100, num_leaves=31, learning_rate=0.05)
    
    def predict(self, current_price, history):
        if len(history) < 10:
            return {"agent": self.name, "direction": "NEUTRAL", "confidence": 0}
        try:
            recent_prices = [h['c'] for h in history[-10:]]
            avg_price = np.mean(recent_prices)
            price_std = np.std(recent_prices)
            micro_trend = (recent_prices[-1] - recent_prices[-5]) / recent_prices[-5]
            if micro_trend > 0.0005 and current_price < avg_price:
                direction = "BUY"
                confidence = 75
            elif micro_trend < -0.0005 and current_price > avg_price:
                direction = "SELL"
                confidence = 75
            else:
                direction = "HOLD"
                confidence = 55
            return {
                "agent": self.name,
                "direction": direction,
                "confidence": confidence,
                "micro_trend": micro_trend
            }
        except Exception:
            return {"agent": self.name, "direction": "NEUTRAL", "confidence": 0}

class NewsAgent(BaseAgent):
    def __init__(self, pair, timeframe):
        super().__init__("NewsAgent", pair, timeframe)
    
    def predict(self, current_price, history):
        try:
            df = pd.DataFrame(history)
            recent_volatility = df['c'].pct_change().tail(10).std()
            if recent_volatility > 0.005:
                direction = "BUY" if df['c'].iloc[-1] > df['c'].iloc[-5] else "SELL"
                confidence = 70
            else:
                direction = "HOLD"
                confidence = 60
            return {
                "agent": self.name,
                "direction": direction,
                "confidence": confidence,
                "volatility_signal": recent_volatility
            }
        except Exception:
            return {"agent": self.name, "direction": "NEUTRAL", "confidence": 0}
