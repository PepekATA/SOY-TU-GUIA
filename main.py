# modules/chart.py
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

def generate_live_chart(pair, history, prediction, timeframe="M1"):
    """Genera gráfico interactivo con predicciones"""
    
    if not history or len(history) < 20:
        return "<div style='color: cyan; text-align: center; padding: 50px;'>Esperando datos...</div>"
    
    # Preparar datos
    df = pd.DataFrame(history)
    
    # Crear subplots
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        subplot_titles=(f'{pair} - {timeframe}', 'RSI', 'Volumen'),
        row_heights=[0.6, 0.2, 0.2]
    )
    
    # Candlestick principal
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df['o'],
            high=df['h'],
            low=df['l'],
            close=df['c'],
            name='Precio',
            increasing_line_color='#00ff00',
            decreasing_line_color='#ff0000'
        ),
        row=1, col=1
    )
    
    # Media móviles
    if len(df) >= 20:
        df['sma20'] = df['c'].rolling(20).mean()
        df['sma50'] = df['c'].rolling(50).mean() if len(df) >= 50 else None
        
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['sma20'],
                name='SMA 20',
                line=dict(color='yellow', width=1)
            ),
            row=1, col=1
        )
    
    # RSI
    if len(df) >= 14:
        delta = df['c'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['rsi'],
                name='RSI',
                line=dict(color='cyan', width=1),
                fill='tozeroy',
                fillcolor='rgba(0,255,255,0.1)'
            ),
            row=2, col=1
        )
        
        # Líneas RSI
        fig.add_hline(y=70, line_color="red", line_width=1, line_dash="dash", row=2, col=1)
        fig.add_hline(y=30, line_color="green", line_width=1, line_dash="dash", row=2, col=1)
    
    # Volumen
    colors = ['green' if df['c'].iloc[i] > df['o'].iloc[i] else 'red' 
              for i in range(len(df))]
    
    fig.add_trace(
        go.Bar(
            x=df.index,
            y=df.get('v', [0]*len(df)),
            name='Volumen',
            marker_color=colors
        ),
        row=3, col=1
    )
    
    # Añadir predicción
    if prediction and 'current_price' in prediction:
        last_price = prediction['current_price']
        target = prediction.get('target_price', last_price)
        stop = prediction.get('stop_loss', last_price)
        
        # Líneas de predicción
        fig.add_hline(y=last_price, line_color="blue", line_width=2, 
                     annotation_text=f"Actual: {last_price:.5f}", row=1, col=1)
        fig.add_hline(y=target, line_color="green", line_width=2, line_dash="dash",
                     annotation_text=f"Target: {target:.5f}", row=1, col=1)
        fig.add_hline(y=stop, line_color="red", line_width=2, line_dash="dash",
                     annotation_text=f"Stop: {stop:.5f}", row=1, col=1)
    
    # Layout
    fig.update_layout(
        template='plotly_dark',
        height=600,
        showlegend=True,
        xaxis_rangeslider_visible=False,
        hovermode='x unified',
        margin=dict(l=0, r=0, t=30, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0.3)',
        font=dict(color='white')
    )
    
    # Configuración de ejes
    fig.update_xaxes(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
    fig.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
    
    return fig.to_html(
        div_id=f"chart-{pair}",
        include_plotlyjs='cdn',
        config={'displayModeBar': False}
    )

def plot_prediction(pair, history, prediction):
    """Versión simplificada para matplotlib si se necesita"""
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('Agg')
    
    prices = [h['c'] for h in history[-100:]]
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), 
                                    gridspec_kw={'height_ratios': [3, 1]})
    
    # Precio
    ax1.plot(prices, label="Precio", color='cyan', linewidth=2)
    ax1.set_facecolor('black')
    ax1.grid(True, alpha=0.3)
    
    if prediction:
        ax1.axhline(prediction['current_price'], color='blue', linestyle='--', label="Actual")
        ax1.axhline(prediction.get('target_price', 0), color='green', linestyle='--', label="Target")
        ax1.axhline(prediction.get('stop_loss', 0), color='red', linestyle='--', label="Stop Loss")
    
    ax1.legend(loc='upper left')
    ax1.set_title(f"{pair} - {prediction.get('direction', 'ANALIZANDO')}", color='white', fontsize=14)
    
    # RSI
    if len(prices) > 14:
        df = pd.DataFrame({'c': prices})
        delta = df['c'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        ax2.plot(rsi, color='yellow', linewidth=1)
        ax2.axhline(70, color='red', linestyle='--', alpha=0.5)
        ax2.axhline(30, color='green', linestyle='--', alpha=0.5)
        ax2.fill_between(range(len(rsi)), 30, 70, alpha=0.1, color='gray')
        ax2.set_ylabel('RSI', color='white')
        ax2.set_ylim(0, 100)
    
    ax2.set_facecolor('black')
    ax2.grid(True, alpha=0.3)
    
    fig.patch.set_facecolor('black')
    plt.tight_layout()
    
    return fig
