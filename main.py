from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from modules.finage_client import get_forex_signal
from modules.predictor import interpret_signal
from modules.chart import generate_chart
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, symbol: str = "EURUSD"):
    raw = get_forex_signal(symbol)
    prediction = interpret_signal(raw)
    chart_html = generate_chart(prediction)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "prediction": prediction,
        "chart": chart_html
    })
