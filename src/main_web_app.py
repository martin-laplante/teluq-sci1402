from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import date
from typing import Optional

from apodapp import apodapp
apodapp.initialize()

app = FastAPI()

# 1. Monter le dossier "static" pour qu'il soit accessible via l'URL "/static"
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Route pour afficher la page d'accueil
@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})

# Route API en GET qui reçoit les paramètres dans l'URL
@app.get("/api/process")
async def process_data(
    start_date: date = Query(...),
    duration_days: int = Query(...),
    nb_catego: int = Query(...),
    strategy: str = Query(...),
    flag_lowercase: bool = Query(False),
    flag_tf_idf: bool = Query(False)
):

    result_data = apodapp.query(start_date, duration_days, nb_catego, flag_lowercase, flag_tf_idf, strategy)

    return result_data
