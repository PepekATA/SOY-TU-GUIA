# modules/coordinator.py

class MasterCoordinator:
    """Coordina todos los agentes y toma la decisión final"""
    def __init__(self, pair):
        self.pair = pair
        self.agents = {}
        self.weights = {}
        
    def add_agent(self, agent, weight=1.0):
        key = f"{agent.name}_{agent.timeframe}"
        self.agents[key] = agent
        self.weights[key] = weight
    
    def get_consensus_prediction(self, current_price, history):
        predictions = []
        total_weight = 0
        for key, agent in self.agents.items():
            try:
                pred = agent.predict(current_price, history)
                pred['weight'] = self.weights[key]
                predictions.append(pred)
                total_weight += self.weights[key]
            except Exception:
                continue
        if not predictions:
            return {"pair": self.pair, "direction": "HOLD", "confidence": 0, "agents_count": 0}
        
        buy_score = sum(p['confidence'] * p['weight'] for p in predictions if p['direction'] == 'BUY')
        sell_score = sum(p['confidence'] * p['weight'] for p in predictions if p['direction'] == 'SELL')
        hold_score = sum(p['confidence'] * p['weight'] for p in predictions if p['direction'] == 'HOLD')
        
        total_score = buy_score + sell_score + hold_score
        if total_score > 0:
            buy_score /= total_score
            sell_score /= total_score
            hold_score /= total_score
        
        if buy_score > 0.6:
            final_direction = "📈 COMPRAR"
            final_confidence = buy_score * 100
        elif sell_score > 0.6:
            final_direction = "📉 VENDER"
            final_confidence = sell_score * 100
        else:
            final_direction = "⏸️ MANTENER"
            final_confidence = hold_score * 100
        
        if final_direction == "📈 COMPRAR":
            target_price = current_price * 1.005
            stop_loss = current_price * 0.997
        elif final_direction == "📉 VENDER":
            target_price = current_price * 0.995
            stop_loss = current_price * 1.003
        else:
            target_price = current_price
            stop_loss = current_price
        
        return {
            "pair": self.pair,
            "direction": final_direction,
            "confidence": min(95, final_confidence),
            "current_price": current_price,
            "target_price": target_price,
            "stop_loss": stop_loss,
            "agents_count": len(predictions),
            "individual_predictions": predictions,
            "scores": {"buy": buy_score * 100, "sell": sell_score * 100, "hold": hold_score * 100}
        }
