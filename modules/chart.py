import plotly.graph_objects as go

def generate_chart(prediction):
    fig = go.Figure()

    # Marcamos la predicción como texto
    fig.add_trace(go.Indicator(
        mode="number+gauge+delta",
        value=prediction["confidence"],
        title={'text': f"{prediction['symbol']} - {prediction['direction']}"},
        delta={'reference': 50},
        gauge={'axis': {'range': [0, 100]}}
    ))

    fig.update_layout(
        title="Soy tu guía - Predicciones AI",
        template="plotly_dark"
    )
    return fig.to_html(full_html=False)
