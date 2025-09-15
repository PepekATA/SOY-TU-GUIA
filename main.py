from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from modules.finage_client import get_forex_signal, get_multiple_signals
from modules.predictor import interpret_signal
from modules.chart import generate_chart

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

FOREX_PAIRS = [
    "EURUSD","GBPUSD","USDJPY","AUDUSD","USDCAD","USDCHF","NZDUSD",
    "EURGBP","EURJPY","GBPJPY","AUDJPY","AUDNZD","EURAUD","EURCAD"
]

@app.get("/")
async def home(request: Request):
    predictions = []
    for symbol in FOREX_PAIRS[:10]:
        try:
            raw = get_forex_signal(symbol)
            pred = interpret_signal(raw, symbol)
            predictions.append(pred)
        except:
            continue
    
    chart_html = generate_chart(predictions)
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "chart": chart_html
    })

@app.get("/api/chart")
async def get_chart():
    predictions = []
    for symbol in FOREX_PAIRS[:10]:
        try:
            raw = get_forex_signal(symbol)
            pred = interpret_signal(raw, symbol)
            predictions.append(pred)
        except:
            continue
    
    chart_html = generate_chart(predictions)
    return JSONResponse({"chart": chart_html})
