##
## SCI 1402 - apodapp 
## ==================           
##
## Coeur de l'application `Dashboard`. 
##
## (C)opyright, 2026 by Martin Laplante

# Python
from datetime import date                                                      # TODO: Bannieres, Copyrights, etc
import hashlib
import json
import re
import time

# Tiers
import pandas as pd

# Local
from date2pos import date2pos  # BD de conversion

def get_pos_from_date(_date):
    """Permet de choisir la bonne position de départ selon une date fournie."""
    if isinstance(_date, date):
        _date = _date.strftime("%Y-%m-%d")
    result = date2pos.get(_date)
    if result == None:
        return -1
    return result

def build_word_stream(in_txt):
    """On crée une chaine de mots simple basé sur le contenu de `in_txt`."""
    if not isinstance(in_txt,str):
        return ''
    return ''.join(mo.group() for mo in re.finditer(r"[-\w]+",in_txt.lower()))


# le start ici ----------+      est la position dans le CSV
#                        |      donc 0 est le premier 
#                        v      
def apodcsv2json(path, start, nb, chop, **args):
    """Convertis le CSV en dictionnaire Python et forme une sortie au fomat JSON."""

    dataframe = pd.read_csv(path)
    records = dataframe.to_dict(orient='records')

    result = {}
    nbskip=0
    for position, record in enumerate(records[start:]):        
        word_stream = build_word_stream(record['explanation'])
        row = {
            'position':start+position,  # LA POSITION DANS LA LISTE PANDA
            'date_ymd':record['date'],
            'date_secs':time.mktime(time.strptime(record['date'], "%Y-%m-%d")),
            'title':record['title'],
            # Compatibilité avec l'entrée du factorisateur
            'label': "%(date)s -- %(title)s" % record,
            'words': {},
        }
        try:
            if record['explanation'] == '':
                nbskip+=1
                continue
            for itm in chop(record['explanation']): #                          TODO:  chop must be callable 
                if itm not in row['words']:
                    row['words'][itm]=0
                row['words'][itm]+=1
            if len(row['words'])==0:
                nbskip+=1
                continue  # On ne sort pas de liste resultante vide.
        except TypeError as errType: #                                         TODO:  Err Management/Logg 
            nbskip +=1
            continue                 # ICI on va avoir un saut du champs `Position`` dans la sortie
        except Exception as err:#                                              TODO:  Err Management/Logg 
            print(repr(err)+':',type(err))
            print(row['position'])
            print(record['date'])
            print(record['explanation'])
            print()
            nbskip+=1
            continue                 # ICI aussi `Position` va skip.
        if args.get('show_ws'): #                                              TODO:  Document optional parameter
            row['word_stream'] = word_stream
        md5 = hashlib.md5(word_stream.encode()).hexdigest()
        if args.get('want_uid'): #                                             TODO:  Document optional parameter
            row['md5_uid'] = md5
        key = md5
        if key in result:
            nbskip+=1
            continue #   ICI AUSSI ON AURA UN SKIP                             TODO: Log an error ?
        result[key]=row #                                                      TODO: X-ref avec rapport 1/2 parcours que les duplic sont pas permis
        nb-=1
        if nb<=0:break
    return result #                                                            TODO: A list or a dictionary ?

# Quelques tests ...
if __name__=="__main__":                                                     # TODO: Est-ce que ca marche toujours ?
    from strategies import strategies
    
    import config

    log = 'log' in dir(config) and config.log or False

    path = config.apod_csv_path
    start,nb=(0,11186)
#   regex = config.re_findall
#   chop = lambda x: config.re_findall.findall(x)
#   chop = lambda x: (mo.groupdict()['minn'] for mo in re.finditer(r'(?<=\W)(?P<minn>[a-z]+)(?=\W)',x))
#   chop = lambda x: (mo.groupdict()['ttl']  for mo in re.finditer(r'(?<=\W)(?P<ttl>[A-Z][a-z]+)(?=\W)',x))
    chop = strategies['acronymes']
    result = apodcsv2json(path, start, nb, chop, show_ws = config.debug_add_word_stream)

    with open(config.apod_csv_path+'.JSON','w+t',encoding='utf-8') as outf:
        json.dump(result, outf, indent=None, ensure_ascii=False)
    with open(config.apod_csv_path+'.JSON',encoding='utf-8') as inptxt:
        data = re.sub(r'}}, "(?=[0-9a-f]{32})', r'}},\n "',inptxt.read())
    with open(config.apod_csv_path+'.JSON','w+t',encoding='utf-8') as outf:
        outf.write(data)
        
    
