##
## SCI 1402 - apodapp 
## ==================           
##
## Coeur de l'application `Dashboard`. 
##
## (C)opyright, 2026 by Martin Laplante

# Python
import re

# Local
from stop_words import stop_words

# Stratégie de base : exporter avec les strategies
re_findall = re.compile(r'[-\w]+') 

# Trouver des acronymes.
re_finditer_acronyms = re.compile(r"(?<=\()[-0-9A-Z]+(?=\))|[A-Z]{5,}|[BCDFGHJKLMNPQRSTVWXZ]{2,4}")


def sans_mots_vides(x):
    """Cette stratégie utilise la stratégie de base, mais exclue les mots vides."""
    res = []
    for mot in re_findall.findall(x):
        if mot.lower() in stop_words:
            continue
        res.append(mot)
    return res

def noms_propres(x):
    """Stratégie permettant de repérer les noms propres.  Certaines valeurs sont 'vide': on les retire."""
    res = []
    for mots in list(re.finditer(r'[A-Z][-a-z]+(\s+[A-Z][-a-z]+)+',x)):
        if mots.group().strip() in {'Photo Gallery', 'Jerry Bonnell', 'Robert Nemiroff', 'In July', 'Astronomy Picture', 'Astronomy Pictures'}: continue
        if mots.group().strip().endswith("Explanation"):
            res.append(mots.group().strip().replace("Explanation",'').strip())
            continue    
        if mots.group().strip().endswith("Picture Credit"):
            res.append(mots.group().strip().replace("Picture Credit",'').strip())
            continue   
        res.append(mots.group().strip())
    return res

def acronymes(x):
    """Stratégie permettant de repérer les acronymes."""
    res = []
    for mots in list(re_finditer_acronyms.finditer(x)):
        res.append(mots.group().strip())
    return res

def messier(x):
    """Stratégie permettant de repérer les désignation des objets du catalogue de Messier."""
    res = []
    for mots in list(re.finditer(r"Messier\s*\d+|(?<=\W)m\s*\d+(?=\W)",x,re.I)):
        res.append(mots.group().strip())
    return res

strategies = {
    'tout' : lambda x : re_findall.findall(x),
    'sans_mots_vides': sans_mots_vides,
    'noms_propres': noms_propres,
    'acronymes':acronymes,
    'messier':messier,
}
