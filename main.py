from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from modules.finage_client import get_forex_signal, get_forex_history
from modules.predictor import interpret_signal
from modules.chart import generate_live_chart

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
    "EURGBP","EURJPY","GBPJPY","AUDJPY","AUDNZD","EURAUD","EURCAD",
    "CHFJPY","CADJPY","GBPCHF","AUDCHF","NZDJPY","EURCHF"
]

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "forex_pairs": FOREX_PAIRS
    })

@app.get("/api/live/{symbol}")
async def get_live_data(symbol: str):
    try:
        current = get_forex_signal(symbol)
        history = get_forex_history(symbol)
        prediction = interpret_signal(current, symbol)
        
        return JSONResponse({
            "symbol": symbol,
            "current_price": current.get("price", 0),
            "bid": current.get("bid", 0),
            "ask": current.get("ask", 0),
            "timestamp": current.get("timestamp", 0),
            "prediction": prediction,
            "history": history
        })
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/api/chart/{symbol}")
async def get_chart(symbol: str):
    try:
        current = get_forex_signal(symbol)
        history = get_forex_history(symbol)
        prediction = interpret_signal(current, symbol)
        chart_html = generate_live_chart(symbol, history, prediction)
        
        return JSONResponse({"chart": chart_html})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
