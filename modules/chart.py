import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

def generate_live_chart(symbol, history, prediction):
    # Crear figura con subplots
    fig = make_subplots(
        rows=2, cols=2,
        row_heights=[0.7, 0.3],
        column_widths=[0.7, 0.3],
        specs=[
            [{"type": "candlestick"}, {"type": "indicator"}],
            [{"type": "bar"}, {"type": "table"}]
        ],
        subplot_titles=(
            f"📊 {symbol} - Gráfico en Tiempo Real",
            "🎯 Predicción AI",
            "📈 Volumen",
            "📋 Detalles"
        )
    )
    
    # Preparar datos
    if history and len(history) > 0:
        times = [datetime.fromtimestamp(h.get("t", 0)/1000) for h in history]
        
        # Gráfico de velas
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
        
        # Añadir líneas de entrada, target y stop loss
        last_time = times[-1]
        future_times = [last_time + timedelta(minutes=i*5) for i in range(1, 13)]
        
        # Línea de precio actual
        fig.add_trace(
            go.Scatter(
                x=[times[-1], future_times[-1]],
                y=[prediction["price"], prediction["price"]],
                mode='lines',
                name='Precio Actual',
                line=dict(color='yellow', width=2, dash='dash')
            ),
            row=1, col=1
        )
        
        # Línea de target
        fig.add_trace(
            go.Scatter(
                x=[times[-1], future_times[-1]],
                y=[prediction["price"], prediction["target_price"]],
                mode='lines+markers',
                name='Target',
                line=dict(color='#00ff00', width=3),
                marker=dict(size=10, symbol='star')
            ),
            row=1, col=1
        )
        
        # Línea de stop loss
        fig.add_trace(
            go.Scatter(
                x=[times[-1], future_times[-1]],
                y=[prediction["price"], prediction["stop_loss"]],
                mode='lines+markers',
                name='Stop Loss',
                line=dict(color='#ff0000', width=2, dash='dot'),
                marker=dict(size=8, symbol='x')
            ),
            row=1, col=1
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
    
    # Indicador de predicción
    color = "#00ff00" if "SUBIRÁ" in prediction["main_direction"] else "#ff0000" if "BAJARÁ" in prediction["main_direction"] else "#ffff00"
    
    fig.add_trace(
        go.Indicator(
            mode="gauge+number+delta",
            value=prediction["main_confidence"],
            title={'text': f"<b>{prediction['main_direction']}</b><br>Duración: {prediction['main_duration']}"},
            delta={'reference': 75, 'position': "bottom"},
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
    
    # Tabla de detalles
    reasons_text = "<br>".join(prediction.get("reasons", ["Análisis en proceso"]))
    
    fig.add_trace(
        go.Table(
            header=dict(
                values=['Parámetro', 'Valor'],
                fill_color='darkblue',
                align='left',
                font=dict(color='white', size=12)
            ),
            cells=dict(
                values=[
                    ['Precio Entrada', 'Target', 'Stop Loss', 'Spread', 'Razones'],
                    [
                        f'{prediction["entry_price"]:.5f}',
                        f'{prediction["target_price"]:.5f}',
                        f'{prediction["stop_loss"]:.5f}',
                        f'{prediction["spread"]:.5f}',
                        reasons_text
                    ]
                ],
                fill_color='rgba(0,0,0,0.5)',
                align='left',
                font=dict(color='white', size=11),
                height=30
            )
        ),
        row=2, col=2
    )
    
    # Layout
    fig.update_layout(
        template="plotly_dark",
        height=800,
        showlegend=True,
        title={
            'text': f"<b>🤖 PREDICCIÓN AI - {symbol}</b>",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 24, 'color': 'white'}
        },
        paper_bgcolor='rgba(0,0,0,0.95)',
        plot_bgcolor='rgba(0,0,0,0.9)',
        font=dict(color='white', size=11),
        xaxis_rangeslider_visible=False,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig.to_html(full_html=False, include_plotlyjs='cdn', config={'responsive': True})
