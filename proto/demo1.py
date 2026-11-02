#!pip install feedparser feedgen beautifulsoup4 requests

import feedparser
from feedgen.feed import FeedGenerator
import requests
from bs4 import BeautifulSoup

# 1. Configuration du flux source (Exemple : La Presse Actualités)
URL_RSS_SOURCE = "https://lapresse.ca"
URL_RSS_SOURCE = "http://www.journaldemontreal.com/actualite/faits-divers/rss.xml"
flux_original = feedparser.parse(URL_RSS_SOURCE)

# 2. Création du nouveau flux RSS plein texte
fg = FeedGenerator()
fg.title('Mon Flux La Presse Plein Texte')
fg.link(href='https://lapresse.ca', rel='alternate')
fg.description('Flux RSS converti en texte intégral')

# 3. Boucle pour aller chercher le contenu complet de chaque article
for entry in flux_original.entries[:10]: # Limité aux 10 derniers articles pour tester
    item = fg.add_entry()
    item.title(entry.title)
    item.link(href=entry.link)
    
    try:
        # Requête pour télécharger la page web de l'article complet
        reponse = requests.get(entry.link, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(reponse.text, 'html.parser')
        
        # Extraction du texte (cette classe change selon le site web, exemple générique)
        # Pour La Presse ou Radio-Canada, il faut cibler la balise contenant le texte de l'article
        paragraphes = soup.find_all('p') 
        texte_complet = "".join([str(p) for p in paragraphes])
        
        # On injecte le texte complet dans la description du RSS
        item.description(texte_complet)
    except Exception as e:
        item.description(entry.summary) # En cas d'erreur, on garde le résumé

# 4. Sauvegarde du fichier RSS final
fg.rss_file('flux_complet.xml')
print("Le fichier 'flux_complet.xml' a été généré avec succès !")
