# modules/__init__.py
# Hace que "modules" sea un paquete importable

from .ml_agents import BaseAgent, TrendAgent, MomentumAgent, VolatilityAgent, PatternAgent, ScalpingAgent, NewsAgent
from .coordinator import MasterCoordinator
from .system import ForexMultiAgentSystem
from .alpaca_client import AlpacaRealClient

__all__ = [
    'BaseAgent',
    'TrendAgent',
    'MomentumAgent',
    'VolatilityAgent',
    'PatternAgent',
    'ScalpingAgent',
    'NewsAgent',
    'MasterCoordinator',
    'ForexMultiAgentSystem',
    'AlpacaRealClient'
]
