# modules/formatter.py

def format_signal(signal):
    return f"[{signal['pair']}] {signal['direction']} @ {signal['current_price']:.5f} (Conf: {signal['confidence']:.1f}%)"
