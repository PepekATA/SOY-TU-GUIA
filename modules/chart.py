import plotly.graph_objects as go
from plotly.subplots import make_subplots

def generate_chart(predictions):
    fig = make_subplots(
        rows=2, cols=2,
        specs=[[{'type': 'indicator'}, {'type': 'indicator'}],
               [{'type': 'bar'}, {'type': 'scatter'}]],
        subplot_titles=("Señales en Tiempo Real", "Confianza AI", 
                       "Fuerza de Señal", "Tendencia")
    )
    
    # Indicadores principales
    for i, pred in enumerate(predictions[:2]):
        color = "green" if "COMPRA" in pred["direction"] else "red" if "VENTA" in pred["direction"] else "yellow"
        fig.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=pred["confidence"],
                title={'text': f"<b>{pred['symbol']}</b><br>{pred['direction']}"},
                delta={'reference': 75},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': color},
                    'steps': [
                        {'range': [0, 50], 'color': "rgba(255,255,255,0.1)"},
                        {'range': [50, 80], 'color': "rgba(255,255,255,0.2)"},
                        {'range': [80, 100], 'color': "rgba(255,255,255,0.3)"}
                    ],
                    'threshold': {
                        'line': {'color': "white", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ),
            row=1, col=i+1
        )
    
    # Barras de confianza
    symbols = [p["symbol"] for p in predictions[:10]]
    confidences = [p["confidence"] for p in predictions[:10]]
    colors = ["green" if c > 80 else "yellow" if c > 60 else "red" for c in confidences]
    
    fig.add_trace(
        go.Bar(
            x=symbols,
            y=confidences,
            marker_color=colors,
            text=confidences,
            textposition='outside'
        ),
        row=2, col=1
    )
    
    # Línea de tendencia
    fig.add_trace(
        go.Scatter(
            x=symbols,
            y=confidences,
            mode='lines+markers',
            line=dict(color='cyan', width=3),
            marker=dict(size=10, color=colors)
        ),
        row=2, col=2
    )
    
    fig.update_layout(
        template="plotly_dark",
        height=800,
        showlegend=False,
        title={
            'text': "<b>🎯 SOY TU GUÍA - PREDICCIONES FOREX AI</b>",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 24, 'color': 'white'}
        },
        paper_bgcolor='rgba(0,0,0,0.9)',
        plot_bgcolor='rgba(0,0,0,0.8)',
        font=dict(color='white', size=12)
    )
    
    return fig.to_html(full_html=False, include_plotlyjs='cdn')
