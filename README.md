"""

with open('/content/soytuguia/README.md', 'w') as f:
    f.write(readme_content)

print("✅ README.md creado")

#%% Celda 5: Definir configuración del sistema
FOREX_PAIRS = [
    "AUDCAD", "AUDCHF", "AUDJPY", "AUDNZD", "AUDUSD",
    "CADCHF", "CADJPY", "CHFJPY", "EURAUD", "EURCAD",
    "EURCHF", "EURGBP", "EURJPY", "EURNZD", "EURUSD",
    "GBPAUD", "GBPCAD", "GBPCHF", "GBPJPY", "GBPNZD",
    "GBPUSD", "NZDCAD", "NZDCHF", "NZDJPY", "NZDUSD",
    "USDCAD", "USDCHF", "USDJPY"
]

TIMEFRAMES = ["M1", "M5", "M15", "M30", "H1", "H4", "D1"]

AGENTS = [
    "TrendAgent", "MomentumAgent", "VolatilityAgent",
    "PatternAgent", "ScalpingAgent", "NewsAgent"
]

print(f"\n📊 Configuración del Sistema:")
print(f"   - {len(FOREX_PAIRS)} pares de divisas")
print(f"   - {len(TIMEFRAMES)} timeframes")
print(f"   - {len(AGENTS)} agentes por par")
print(f"   - Total: {len(FOREX_PAIRS) * len(TIMEFRAMES) * len(AGENTS)} modelos a entrenar")

#%% Celda 6: Resto del código (igual que antes pero con las funciones mejoradas)
# [Incluir el resto del código desde la Celda 5 en adelante del código anterior]
# Cliente Alpaca, FeatureEngineer, MLAgent, ForexTrainingSystem, etc.

import alpaca_trade_api as tradeapi

class AlpacaDataCollector:
    def __init__(self):
        self.api = tradeapi.REST(
            os.environ['ALPACA_API_KEY'],
            os.environ['ALPACA_SECRET_KEY'],
            'https://paper-api.alpaca.markets',
            api_version='v2'
        )
        print("✅ Conectado a Alpaca Markets")
    
    def get_training_data(self, pair, timeframe="1Hour", days=90):
        """Obtiene datos históricos para entrenamiento"""
        try:
            symbol = f"{pair[:3]}/{pair[3:]}"
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
                end=end.isoformat(),
                limit=10000
            ).df
            
            if not bars.empty:
                bars = bars.reset_index()
                bars.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'trade_count', 'vwap']
                return bars
            
        except Exception as e:
            print(f"⚠️ Error obteniendo datos de {pair}: {e}")
        
        return pd.DataFrame()

#%% Celda 7: Función mejorada para subir a GitHub
def upload_to_github_safe(repo, local_path, github_path, commit_message, max_retries=3):
    """Sube archivo a GitHub con reintentos y manejo de errores"""
    for attempt in range(max_retries):
        try:
            with open(local_path, 'rb') as file:
                content = file.read()
            
            try:
                # Intentar obtener el archivo existente
                contents = repo.get_contents(github_path)
                repo.update_file(
                    path=github_path,
                    message=commit_message,
                    content=content,
                    sha=contents.sha
                )
                print(f"✅ Actualizado en GitHub: {github_path}")
                return True
            except:
                # Crear nuevo archivo
                repo.create_file(
                    path=github_path,
                    message=commit_message,
                    content=content
                )
                print(f"✅ Creado en GitHub: {github_path}")
                return True
                
        except Exception as e:
            print(f"⚠️ Intento {attempt + 1}/{max_retries} falló: {e}")
            if attempt < max_retries - 1:
                time.sleep(5)  # Esperar antes de reintentar
            else:
                print(f"❌ Error final subiendo a GitHub: {github_path}")
                return False

# [Continuar con el resto del código original desde FeatureEngineer, MLAgent, etc.]
