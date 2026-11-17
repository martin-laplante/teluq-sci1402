##
## SCI 1402 - apodapp 
## ==================           
##
## Coeur de l'application `Dashboard`. 
##
## (C)opyright, 2026 by Martin Laplante

# Python
import time
import math

# Tiers
import numpy as np
from sklearn.decomposition import NMF

# Local
from apodcsv2json import apodcsv2json
from apodcsv2json import get_pos_from_date
from strategies import strategies

# Config
import config

# Lorsque l'option `minuscules` est applicable et choisie, on abaisse la casse sur la chaine d'entrée.
# De cette maniere tous les mots comme les mots vides on la meme valeur interne et seront plus facile à cibler.
# Ce n'est pas toujours le cas.  Par exemple, la cassse est nécessaire pour isoler des noms propres.
case_sens = {
    False: lambda x: x,
    True: lambda x: x.lower(),
}

                                                                                                                                                              # TODO: Placer dans un fichier `strategies.py`


                                                                               # TODO: Placer dans un fichier de traitement
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
    """Point d'entrée.  Le serveur s'assure d'instancier et fait appel à `query` lorsqu'une requete est recue."""

    def __init__(self):
        """Constructeur."""
        pass

    def initialize(self):
        """"""
        pass

    def query(self, start_date, duration_days, nb_catego, flag_lowercase, flag_tf_idf, strategy):
        """Fonction principale.  Appelée lorsqu'une requete est recue par le serveur."""

        ## Obtenir la position des enregistrements selon la date demandée.
        #
        pos = get_pos_from_date(start_date)

        ## Une date hors champs va engendrer une réponse d'erreur.
        #
        if pos<0:
            return {
                "*** ERREUR ***" : [
                    "Start date: %s"%(repr(start_date),),
                    "La date doit se situer entre 1995-06-16 et 2026-02-02 inclusivement."]
            }

        ## Certaines stratégies on besoin de presever la casse, on force la valeur a `False` dans ces cas.
        #
        if strategy in {'noms_propres', 'acronymes'}:
            flag_lowercase = False
        
        strategie_finale = lambda x: strategies[strategy](case_sens.get(flag_lowercase, lambda x:x)(x))

        ## Démarrage du chronomètre pour les résultats de performance.
        t0 = time.time()

        apod_json_data = apodcsv2json(config.apod_csv_path,pos,duration_days,strategie_finale)

        ## Certaines stratégies sont assez restrictive pour permettre de continuer.
        #
        if not apod_json_data:
            return {
                "*** ERREUR ***" : [
                    "Les choix des paramètres n'ont pas trouvé d'article à répartir"]
            }

        ## Construction des entrées
        # 
        M = []
        tags = []
        titles = []
        catego = {
        }

        ## Construction de la liste d'étiquettes (tags)
        #
        for row in apod_json_data.values():
            titles.append(row.get('label','YYYY-MM-DD'))
            for w,count in row.get('words',{}).items():
                if w not in tags:
                    tags.append(w)

        ## Construction de la matrice M
        #
        for row in apod_json_data.values():
            m = [0]*len(tags)
            words = row.get('words',{})
            for i,word in enumerate(tags):
                c = words.get(word,0)
                m[i]=c
            M.append(m)
        
        ## Largeur et Hauteur
        #
        Mw=len(m)
        Mh=len(M)

        # tf-idf...
        if flag_tf_idf:
            M = self.get_td_idf_M(M, tags)

        model = NMF(n_components=nb_catego, init='random', random_state=42)
        W = model.fit_transform(M)
        H = model.components_
        W_ = np.matrix(W).transpose()

        for i,h in enumerate(H):
            arti = CreateTagListFromScores(ScoreSort(ValuesToScores(W_.tolist()[i])),titles,0.5,50)
            catego['/'.join(CreateTagListFromScores(ScoreSort(ValuesToScores(h)),tags,0.5,50))]=arti

        duration = time.time()-t0
        duration_per_elements = duration/(Mh*Mw)
                                                                               # TODO: Revoir pertinence
        result = {
            "Sommaire de l'opération" : [
                "Date de départ demandée %s"%(start_date,),
                "Date de départ obtenue  %s"%(list(apod_json_data.values())[0]['date_ymd'],),
                "Position %d"%(pos,),
                "Date d'arrivée %s"%(list(apod_json_data.values())[-1]['date_ymd'],),
                "Stratégie utilisée: %s"%(strategy,),
                "Longueur du 'apod_json_data': "+str(len(apod_json_data)),
                "minuscules:     %s"%(flag_lowercase,),
                "TF-IDF:    %s"%(flag_tf_idf,),
                "M:  %d X %d (%d elements)"%(Mh, Mw, Mh * Mw,),
                "Durée totale %0.6f seconds"%(duration,),
                "Durée par element: %0.3f μS"%(1000000*duration_per_elements,)
            ]
        }
        result.update(catego)
        return result

    def get_td_idf_M(self, M, tags):
        """Calcul du TF-IDF selon la demande."""
               
        sum_for_each_row = [sum(row) for row in M]
        count_for_each_term = [0 for _ in range(len(tags))]
        for row in M:
            for col,value in enumerate(row):
                if value!=0:
                    count_for_each_term[col]+=1
        
        M_tf_if = []

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

        return M_tf_if

## On démarre la patente
#
apodapp = APOD_App()