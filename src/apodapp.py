import time
import math

import numpy as np
import pandas as pd
from sklearn.decomposition import NMF


from apodcsv2json import apodcsv2json

import config

case_sens = {
    False: lambda x: x,
    True: lambda x: x.lower(),
}

stop_words = ('incorporating', 'investigating', 'nevertheless', 'even though', 'designated', 'discovered', 'yourselves', 'themselves', 'everywhere', 'whereafter', 'throughout', 'thereafter', 'everything', 'beforehand', 'afterwards', 'meanwhile', 'sometimes', 'therefore', 'including', 'wandering', 'utilizing', 'ourselves', 'yesterday', 'something', 'somewhere', 'elsewhere', 'whereupon', 'thereupon', 'otherwise', 'hereafter', 'launched', 'together', 'studying', 'yourself', 'anything', 'hereupon', 'describe', 'whatever', 'formerly', 'interest', 'everyone', 'whenever', 'although', 'anywhere', 'becoming', 'latterly', 'sometime', 'wherever', 'moreover', 'amoungst', 'through', 'nowhere', 'besides', 'because', 'himself', 'further', 'hundred', 'herself', 'against', 'between', 'tonight', 'towards', 'joining', 'usually', 'instead', 'however', 'without', 'whoever', 'whether', 'becomes', 'wherein', 'whereby', 'whereas', 'several', 'perhaps', 'seeming', 'another', 'amongst', 'neither', 'whither', 'fifteen', 'already', 'serious', 'thereby', 'sincere', 'therein', 'somehow', 'dearest', 'nothing', 'someone', 'couldnt', 'titled', 'latest', 'having', 'during', 'inside', 'before', 'unlike', 'though', 'called', 'within', 'beyond', 'dubbed', 'itself', 'should', 'myself', 'toward', 'across', 'theirs', 'whence', 'bottom', 'beside', 'please', 'rather', 'mostly', 'almost', 'latter', 'namely', 'always', 'indeed', 'amount', 'anyhow', 'anyone', 'anyway', 'thence', 'around', 'nobody', 'others', 'became', 'become', 'eleven', 'either', 'behind', 'former', 'seemed', 'hereby', 'herein', 'detail', 'cannot', 'except', 'system', 'enough', 'twelve', 'twenty', 'unless', 'since', 'below', 'still', 'these', 'today', 'could', 'using', 'every', 'watch', 'maybe', 'named', 'would', 'doing', 'taken', 'there', 'those', 'being', 'again', 'other', 'until', 'where', 'which', 'while', 'yours', 'under', 'about', 'above', 'after', 'their', 'found', 'forty', 'often', 'among', 'third', 'thick', 'along', 'eight', 'alone', 'three', 'first', 'front', 'empty', 'least', 'hasnt', 'fifty', 'never', 'hence', 'noone', 'might', 'whole', 'whose', 'sixty', 'seems', 'once', 'that', 'into', 'left', 'away', 'been', 'each', 'this', 'seen', 'down', 'they', 'same', 'from', 'whom', 'your', 'than', 'like', 'have', 'also', 'over', 'here', 'thus', 'both', 'more', 'were', 'does', 'many', 'some', 'such', 'very', 'next', 'join', 'them', 'last', 'then', 'near', 'only', 'just', 'most', 'what', 'when', 'will', 'with', 'hers', 'ours', 'name', 'nine', 'none', 'onto', 'part', 'seem', 'show', 'side', 'take', 'back', 'thin', 'bill', 'call', 'cant', 'dear', 'done', 'thru', 'else', 'even', 'ever', 'fill', 'find', 'fire', 'upon', 'well', 'five', 'four', 'full', 'give', 'keep', 'less', 'made', 'mill', 'mine', 'miss', 'move', 'much', 'must', 'her', 'has', 'had', 'few', 'did', 'can', 'are', 'any', 'own', 'all', 'you', 'she', 'our', 'who', 'the', 'one', 'off', 'nor', 'why', 'was', 'but', 'for', 'now', 'its', 'and', 'two', 'not', 'new', 'out', 'may', 'how', 'his', 'too', 'him', 'inc', 'etc', 'mrs', 'due', 'sir', 'six', 'cry', 'ltd', 'con', 'yet', 'top', 'let', 'per', 'ten', 'via', 'put', 'see', 'get', 'is', 'on', 'it', 'to', 'my', 'so', 'at', 'as', 'by', 'we', 'no', 'be', 'me', 'in', 'an', 'am', 'if', 'ie', 'of', 'up', 'or', 'mr', 'un', 'do', 'de', 'go', 'eg', 'co', 'us', 'he', 're', 'i', 'a', )
def sans_mots_vides(x):
    res = []
    for mot in config.re_findall.findall(x):
        if mot.lower() in stop_words:continue
        res.append(mot)
    return res
def noms_propres(x):
    import re
    res = []
    for mots in list(re.finditer(r'[A-Z][-a-z]+(\s+[A-Z][-a-z]+)+',x)):
        if mots.group().strip() in {'Photo Gallery',
            'Jerry Bonnell','Robert Nemiroff','In July','Astronomy Picture','Astronomy Pictures',}: continue
        if mots.group().strip().endswith("Explanation"):
            res.append(mots.group().strip().replace("Explanation",'').strip())
            continue    
        if mots.group().strip().endswith("Picture Credit"):
            res.append(mots.group().strip().replace("Picture Credit",'').strip())
            continue   
        res.append(mots.group().strip())
    return res

def acronymes(x):
    import re
    res = []
    for mots in list(re.finditer(r"(?<=\()[-0-9A-Z]+(?=\))|[A-Z]{5,}|[BCDFGHJKLMNPQRSTVWXZ]{2,4}",x)):
        res.append(mots.group().strip())
    return res

def messier(x):
    import re
    res = []
    for mots in list(re.finditer(r"Messier\s*\d+|(?<=\W)m\s*\d+(?=\W)",x,re.I)):
        res.append(mots.group().strip())
    return res

strategies = {
    'tout' : lambda x : config.re_findall.findall(x),
    'sans_mots_vides': sans_mots_vides,
    'noms_propres': noms_propres,
    'acronymes':acronymes,
    'messier':messier,
}

from apodcsv2json import get_pos_from_date


def ValuesToScores(lst):
    """Prends une liste de valeur, en fait la somme et donne une nouvelle liste dont les valeurs deviennent un rapport à cette somme.
       Si la somme est 100 et qu'on a un élément de la liste qui vaut 50 alors la liste résultante aura 0.5 à cette nouvelle position.
       La somme des nouveaux elements doit donner 1.0
       ```Python
       ValuesToScores([1,2,3,4])
       # [0.1, 0.2, 0.3, 0.4]
       ```"""
    result = []
    _sum = sum(lst)
    for itm in lst:
        result.append(itm/_sum)
    return result

def Normalize(lst, S):
    """Prends une liste de valeur, et la normalise selon S.
       La somme ne donnera pas nécessairement 1.0.
       ```Python
       Normalize([1,2,3,4],100)
       # [0.01, 0.02, 0.03, 0.04]
       ```"""
    result = []
    for itm in lst:
        result.append(itm/S)
    return result



def ScoreSort(lst):
    """Prends une liste de valeurs et la trie en ordre décroissant.
       Chaque valeur est couplée de sa position initiale"""
    result = []

    # On construit la liste de sortie, en forman un couple,
    # a partir de chaque valeur et sa position d'origine.
    for i,itm in enumerate(lst):
        result.append( (itm, i) )

    # Tri en ordre décroissant
    return list(reversed(sorted(result)))



def CreateTagListFromScores(scores,tags,limscore,limnb):
    """Permet de créer une liste d'étiquettes selon une cible."""
    result = []
    score_total = 0
    nb=0
    for score,position in scores:
        if score==0:continue
        result.append(tags[position])
        score_total+=score
        # La cible:  soit on atteint un nombre limite d'items: limnb
        #            Soit on dépasse un score minmal
        if score_total>=limscore: break
        nb+=1
        if nb>=limnb:break
    return result



class APOD_App(object):
    """"""
    def __init__(self):
        """"""
        print("init:done.")
    def initialize(self):
        """"""
        print("initialize:done.")

    def query(self, start_date, duration_days, nb_catego, flag_lowercase, flag_tf_idf, strategy):
        pos = get_pos_from_date(start_date)
        if pos<0:
            return {
                "*** ERREUR ***" : [
                    "Start date: %s"%(repr(start_date),),
                    "La date doit se situer entre 1995-06-16 et 2026-02-02 inclusivement."]
            }
        
        strat_finale = lambda x: strategies[strategy](case_sens.get(flag_lowercase, lambda x:x)(x))

        t0 = time.time()

        _ = apodcsv2json(config.apod_csv_path,pos,duration_days,strat_finale)

        M = []
        tags = []
        titles = []
        catego = {
        }

        for row in _.values():
            titles.append(row.get('label','YYYY-MM-DD'))
            for w,count in row.get('words',{}).items():
                if w not in tags:
                    tags.append(w)
        for row in _.values():
            m = [0]*len(tags)
            words = row.get('words',{})
            for i,word in enumerate(tags):
                c = words.get(word,0)
                m[i]=c
            M.append(m)
        Mw=len(m)
        Mh=len(M)
        # tf-idf...
        if flag_tf_idf:
            sum_for_each_row = [sum(row) for row in M]
            count_for_each_term = [0 for _ in range(len(tags))]
            for row in M:
                for col,value in enumerate(row):
                    if value!=0:
                        count_for_each_term[col]+=1
            M_tf_if = []
            #print("???", [tags[i] for i in range(len(tags)) if not count_for_each_term[i]])
            for i,row in enumerate(M):
                m = [0]*len(row)
                for j,itm in enumerate(row):
                    if sum_for_each_row[i]:
                        m[i] = itm/sum_for_each_row[i]
                M_tf_if.append(m)
            IDF_t = [math.log(len(M)/v) for v in count_for_each_term]
            for i,row in enumerate(M):
                for j, value in enumerate(row):
                    M_tf_if[i][j] = value * IDF_t[j]
            M = M_tf_if
        model = NMF(n_components=nb_catego, init='random', random_state=42)
        W = model.fit_transform(M)
        H = model.components_
        W_ = np.matrix(W).transpose()

        for i,h in enumerate(H):
            arti = CreateTagListFromScores(ScoreSort(ValuesToScores(W_.tolist()[i])),titles,0.5,50)
            catego['/'.join(CreateTagListFromScores(ScoreSort(ValuesToScores(h)),tags,0.5,50))]=arti

        duration = time.time()-t0
        duration_per_elements = duration/(Mh*Mw)
        
        result = {
            "Sommaire de l'opération" : [
                "Date de départ demandée %s"%(start_date,),
                "Date de départ obtenue  %s"%(list(_.values())[0]['date_ymd'],),
                "Position %d"%(pos,),
                "Date d'arrivée %s"%(list(_.values())[-1]['date_ymd'],),
                "Stratégie utilisée: %s"%(strategy,),
                "Longueu de '_': "+str(len(_)),
                "minuscules:     %s"%(flag_lowercase,),
                "TF-IDF:    %s"%(flag_tf_idf,),
                "M:  %d X %d (%d elements)"%(Mh, Mw, Mh * Mw,),
                "Durée totale %0.6f seconds"%(duration,),
                "Durée par element: %0.3f μS"%(1000000*duration_per_elements,)
            ]
        }
        result.update(catego)
        return result

apodapp = APOD_App()