import plotly.graph_objects as go

def generate_chart(predictions):
    """
    Recibe una lista de predicciones y genera gráficas interactivas
    Cada predicción es un dict con:
    symbol, direction, confidence
    """
    fig = go.Figure()

    for pred in predictions:
        fig.add_trace(go.Indicator(
            mode="number+gauge+delta",
            value=pred["confidence"],
            title={'text': f"{pred['symbol']} - {pred['direction']}"},
            delta={'reference': 50},
            gauge={'axis': {'range': [0, 100]}}
        ))

    fig.update_layout(
        title="Soy tu guía - Predicciones AI",
        template="plotly_dark",
        grid={'rows': len(predictions), 'columns': 1}
    )
    return fig.to_html(full_html=False)
