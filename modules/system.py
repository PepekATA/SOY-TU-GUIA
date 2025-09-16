# modules/system.py

from .ml_agents import TrendAgent, MomentumAgent, VolatilityAgent, PatternAgent, ScalpingAgent, NewsAgent
from .coordinator import MasterCoordinator

class ForexMultiAgentSystem:
    def __init__(self):
        self.coordinators = {}
        self.all_pairs = []
        
    def initialize_all_pairs(self, pairs, timeframes):
        print(f"🌍 Inicializando sistema para {len(pairs)} pares de divisas")
        for pair in pairs:
            coordinator = MasterCoordinator(pair)
            for tf in timeframes:
                coordinator.add_agent(TrendAgent(pair, tf), weight=1.5)
                coordinator.add_agent(MomentumAgent(pair, tf), weight=1.3)
                coordinator.add_agent(VolatilityAgent(pair, tf), weight=1.2)
                coordinator.add_agent(PatternAgent(pair, tf), weight=1.0)
                coordinator.add_agent(ScalpingAgent(pair, tf), weight=0.8)
                coordinator.add_agent(NewsAgent(pair, tf), weight=0.7)
            self.coordinators[pair] = coordinator
            print(f"✅ {pair}: {len(coordinator.agents)} agentes creados")
        self.all_pairs = pairs
        total_agents = sum(len(c.agents) for c in self.coordinators.values())
        print(f"✅ Sistema inicializado: {len(self.coordinators)} pares, {total_agents} agentes totales")
    
    def predict_all(self, current_prices, historical_data):
        predictions = {}
        for pair, coordinator in self.coordinators.items():
            if pair in current_prices and pair in historical_data and len(historical_data[pair]) > 0:
                pred = coordinator.get_consensus_prediction(current_prices[pair], historical_data[pair])
                predictions[pair] = pred
        return predictions
