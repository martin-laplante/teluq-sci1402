from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import date
from typing import Optional

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Route pour afficher la page d'accueil
@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})
##  return templates.TemplateResponse("index.html", {"request": request})

# Route API en GET qui reçoit les paramètres dans l'URL
@app.get("/api/process")
async def process_data(
    start_date: date = Query(...),
    duration_days: int = Query(...),
    quantity: int = Query(...),
    enum_option: str = Query(...),
    flag_feat1: bool = Query(False),
    flag_feat2: bool = Query(False)
):
    # --- Intégrez votre noyau Python ici ---
    # Exemple de traitement bidon basé sur vos paramètres
    result_data = {
        "Statistiques globales": [
            f"Date de début prise en compte : {start_date}",
            f"Calcul sur une durée de {duration_days} jours.",
            f"Quantité cible : {quantity} unités."
        ],
        "Configuration appliquée": [
            f"Mode d'énumération sélectionné : {enum_option}",
            f"Option Option A active : {flag_feat1}",
            f"Option Option B active : {flag_feat2}"
        ],
        "Métriques générées par le noyau": [
            f"Résultat simulé X : {quantity * duration_days}",
            "Statut du traitement : Succès"
        ]
    }
    
    # Renvoie la réponse proprement en JSON
    return result_data
