import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random
from datetime import datetime, timedelta

def generate_live_chart(symbol, history, prediction):
    # Simular datos si no hay historia
    if not history or len(history) < 50:
        history = []
        base_price = prediction["price"]
        for i in range(100):
            history.append({
                "c": base_price + random.uniform(-0.005, 0.005),
                "h": base_price + random.uniform(0, 0.008),
                "l": base_price - random.uniform(0, 0.008),
                "o": base_price + random.uniform(-0.003, 0.003),
                "v": random.randint(1000, 100000),
                "t": (datetime.now() - timedelta(minutes=100-i)).timestamp() * 1000
            })
    
    # Crear subplots
    fig = make_subplots(
        rows=3, cols=2,
        row_heights=[0.5, 0.25, 0.25],
        column_widths=[0.7, 0.3],
        specs=[
            [{"type": "candlestick", "rowspan": 1, "colspan": 1}, {"type": "indicator"}],
            [{"type": "bar", "colspan": 1}, {"type": "indicator"}],
            [{"type": "scatter", "colspan": 2}, None]
        ],
        subplot_titles=(
            f"📊 {symbol} - Precio en Vivo",
            "🎯 Predicción Principal",
            "📈 Volumen",
            "📍 Indicadores Técnicos",
            "⏰ Predicciones Múltiples"
        )
    )
    
    # Gráfico de velas
    times = [datetime.fromtimestamp(h.get("t", 0)/1000) for h in history]
    
    fig.add_trace(
        go.Candlestick(
            x=times,
            open=[h.get("o", 0) for h in history],
            high=[h.get("h", 0) for h in history],
            low=[h.get("l", 0) for h in history],
            close=[h.get("c", 0) for h in history],
            name=symbol,
            increasing_line_color='#00ff00',
            decreasing_line_color='#ff0000'
        ),
        row=1, col=1
    )
    
    # Indicador principal
    color = "#00ff00" if "SUBIRÁ" in prediction["main_direction"] else "#ff0000" if "BAJARÁ" in prediction["main_direction"] else "#ffff00"
    
    fig.add_trace(
        go.Indicator(
            mode="gauge+number+delta",
            value=prediction["main_confidence"],
            title={'text': f"<b>{prediction['main_direction']}</b><br>{prediction['main_duration']}<br><i>{prediction['after_action']}</i>"},
            delta={'reference': 75},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': color},
                'steps': [
                    {'range': [0, 50], 'color': "rgba(255,0,0,0.1)"},
                    {'range': [50, 75], 'color': "rgba(255,255,0,0.1)"},
                    {'range': [75, 100], 'color': "rgba(0,255,0,0.1)"}
                ],
                'threshold': {
                    'line': {'color': "white", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ),
        row=1, col=2
    )
    
    # Volumen
    fig.add_trace(
        go.Bar(
            x=times,
            y=[h.get("v", 0) for h in history],
            name='Volumen',
            marker_color='cyan',
            opacity=0.5
        ),
        row=2, col=1
    )
    
    # Indicadores técnicos
    fig.add_trace(
        go.Indicator(
            mode="number",
            value=prediction["rsi"],
            title={'text': f"RSI: {prediction['rsi']:.1f}<br>MACD: {prediction['macd']:.4f}<br>Bollinger: {prediction['bollinger']}"},
            number={'font': {'size': 20}},
            domain={'x': [0.7, 1], 'y': [0.25, 0.5]}
        ),
        row=2, col=2
    )
    
    # Predicciones secundarias
    pred_times = []
    pred_values = []
    pred_labels = []
    
    current_price = prediction["price"]
    for pred in prediction["secondary_predictions"]:
        pred_times.append(pred["timeframe"])
        change = float(pred["change"].replace("+", "").replace("-", ""))
        if "-" in pred["change"]:
            change = -change
        pred_values.append(current_price + change)
        pred_labels.append(f"{pred['direction']} ({pred['confidence']}%)")
    
    fig.add_trace(
        go.Scatter(
            x=pred_times,
            y=pred_values,
            mode='lines+markers+text',
            name='Predicciones',
            line=dict(color='yellow', width=2),
            marker=dict(size=12, color='orange'),
            text=pred_labels,
            textposition="top center"
        ),
        row=3, col=1
    )
    
    # Layout
    fig.update_layout(
        template="plotly_dark",
        height=900,
        showlegend=False,
        title={
            'text': f"<b>🎯 SOY TU GUÍA - {symbol} EN VIVO</b>",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 28, 'color': 'white'}
        },
        paper_bgcolor='rgba(0,0,0,0.95)',
        plot_bgcolor='rgba(0,0,0,0.9)',
        font=dict(color='white', size=11),
        xaxis_rangeslider_visible=False,
        updatemenus=[{
            'type': 'buttons',
            'showactive': False,
            'x': 0.98,
            'y': 0.98,
            'xanchor': 'right',
            'yanchor': 'top',
            'buttons': [{
                'label': '🔄 Auto-refresh ON',
                'method': 'relayout',
                'args': [{'title': f"<b>🎯 SOY TU GUÍA - {symbol} EN VIVO 🔄</b>"}]
            }]
        }]
    )
    
    return fig.to_html(full_html=False, include_plotlyjs='cdn', config={'responsive': True})
