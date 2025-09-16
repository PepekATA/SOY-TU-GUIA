# modules/alpaca_client.py
import alpaca_trade_api as tradeapi
from datetime import datetime, timedelta
import pandas as pd
import os

class AlpacaRealClient:
    def __init__(self, api_key=None, secret_key=None):
        self.api_key = api_key or os.environ.get("ALPACA_API_KEY")
        self.secret_key = secret_key or os.environ.get("ALPACA_SECRET_KEY")
        self.api = tradeapi.REST(
            self.api_key,
            self.secret_key,
            'https://paper-api.alpaca.markets',
            api_version='v2'
        )
        print("✅ Conectado a Alpaca Markets (Paper Trading)")
        try:
            account = self.api.get_account()
            print(f"💰 Balance: ${float(account.cash):,.2f}")
        except Exception as e:
            print(f"⚠️ Error al obtener cuenta: {e}")
    
    def get_all_forex_pairs(self):
        try:
            assets = self.api.list_assets(status='active', asset_class='forex')
            pairs = [asset.symbol.replace("/", "") for asset in assets if asset.tradable]
            print(f"📊 {len(pairs)} pares de forex disponibles")
            return pairs
        except Exception as e:
            print(f"Error obteniendo pares: {e}")
            return [
                "EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD", "USDCHF",
                "NZDUSD", "EURGBP", "EURJPY", "GBPJPY", "AUDJPY", "AUDNZD"
            ]
    
    def get_historical_data(self, pair, timeframe="1Hour", days=30):
        try:
            symbol = f"{pair[:3]}/{pair[3:]}" if len(pair) == 6 else pair
            end = datetime.now()
            start = end - timedelta(days=days)
            tf_map = {
                "M1": "1Min", "M5": "5Min", "M15": "15Min",
                "M30": "30Min", "H1": "1Hour", "H4": "4Hour", "D1": "1Day"
            }
            bars = self.api.get_bars(
                symbol,
                tf_map.get(timeframe, "1Hour"),
                start=start.isoformat(),
                end=end.isoformat()
            ).df
            
            if not bars.empty:
                history = []
                for index, row in bars.iterrows():
                    history.append({
                        "timestamp": index.isoformat(),
                        "o": float(row["open"]),
                        "h": float(row["high"]),
                        "l": float(row["low"]),
                        "c": float(row["close"]),
                        "v": int(row["volume"]) if "volume" in row else 0,
                        "t": index.timestamp() * 1000
                    })
                return history
        except Exception as e:
            print(f"Error obteniendo datos de {pair}: {e}")
        return []
    
    def get_current_prices(self, pairs):
        prices = {}
        for pair in pairs:
            try:
                symbol = f"{pair[:3]}/{pair[3:]}" if len(pair) == 6 else pair
                bar = self.api.get_latest_bar(symbol)
                if bar:
                    prices[pair] = float(bar.c)
            except Exception as e:
                print(f"Error obteniendo precio de {pair}: {e}")
                prices[pair] = 0
        return prices
