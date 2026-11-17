# teluq-sci1402
Projet de fin de certificat "4865 Science des données" de l'université TÉLUQ

## Démarrage
- Prérequis
  - La plus récente version de Python 3.
  - NumPy
  - Pandas
  - SciKitLearn (sklearn)
  - fastapi
  - **Optionnel** &mdash; pour les exemples du livre `(Segaran, 2007)`
    - PIL (Pillow)
    - feedparser
    - feedgen
    - beatifulsoup4
    - requests
- Dans le répertoire ./src:
  - Sous **Windows** : `runme.bat` pour une démo de bout en bout (exclut le dashboard)
  - Pour le dashboard, dans une invite de commande :
    - `python -m uvicorn main_web_app:app --reload`
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
  