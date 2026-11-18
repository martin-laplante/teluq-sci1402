# teluq-sci1402
Projet de fin de certificat "4865 Science des données" de l'université TÉLUQ

## Démarrage
- Prérequis
  - La plus récente version de Python 3.
  - NumPy
  - Pandas
  - SciKitLearn (sklearn)
  - fastapi (with uvicorn and jinja2)
  - PIL (Pillow)
  - **Optionnel** &mdash; pour les exemples du livre `(Segaran, 2007)`
    - feedparser
    - feedgen
    - beatifulsoup4
    - requests
- Dans le répertoire ./src:
  - Sous **Windows** : `runme.bat` pour une démo de bout en bout (exclut le dashboard)
  - Pour le dashboard, dans une invite de commande :
    - `python -m uvicorn main_web_app:app --reload`
    - Attendre que le message `Application startup complete.` apparaisse.
    - Avec un navigateur web, atteindre <http://127.0.0.1:8000>
<!--- Sous **Linux**: `runme.sh`-->

## Structure

  
  | Dossier        | Description / Contenu         |
  |:---------------|:------------------------------|
  | **./src/**     | Le code source du projet      |
  | **./img/**     | Images ressources             |
  | **./planif/**  | Charte Gantt                  |
  | **./sortie/**  | Travaux notés déjà déposés    |
  | **./doc/**     | Documentation (Ex. : TN1, 2, etc) |
  | **./proto/**   | Sélection de prototypes utilisés pour les travaux notés.  |
  | **./sortie/**  | Copies déposées et rétroaction |
  | **./data/APOD/NASA APOD 1995-2026/** | Contient le fichier obtenu sur Kaggle |
  