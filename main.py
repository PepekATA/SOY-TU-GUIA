from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from modules.finage_client import get_forex_signal
from modules.predictor import interpret_signal
from modules.chart import generate_chart
from modules.formatter import format_predictions

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Lista completa de pares de Forex
FOREX_PAIRS = [
    "EURUSD","GBPUSD","USDJPY","AUDUSD","USDCAD","USDCHF","NZDUSD",
    "EURGBP","EURJPY","GBPJPY","AUDJPY","AUDNZD","EURAUD","EURCAD",
    "CHFJPY","CADJPY","GBPCHF","AUDCHF","NZDJPY","EURCHF"
]

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, symbols: str = None):
    """
    symbols: string con pares separados por coma. Si es None, devuelve todos.
    """
    selected = symbols.split(",") if symbols else FOREX_PAIRS
    predictions = []

    for symbol in selected:
        raw = get_forex_signal(symbol)
        pred = interpret_signal(raw)
        predictions.append(pred)

    chart_html = generate_chart(predictions)
    formatted = format_predictions(predictions)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "predictions": formatted,
        "chart": chart_html,
        "forex_pairs": FOREX_PAIRS
    })
