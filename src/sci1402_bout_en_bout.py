import collections
import hashlib
import math
import re
import sys
import time

# Tierce partie
import numpy as np
from sklearn.decomposition import NMF


###############################################################################
## Configuration
###############################################################################
source_apod_csv_path = r'..\data\APOD\NASA APOD 1995-2026\nasa_apod_complete.csv'
source_apod_csv_encoding = 'utf-8'

###############################################################################
## Définitions - "Factory Settings"
###############################################################################
destination_markdown_path = r'.\sci1402_bout_en_bout.Qmd'
destination_markdown_encoding = 'utf-8'
str_re_split_lines = r'\r?\n(?=199[56789]-\d\d-\d\d|20[012]\d-\d\d-\d\d)'
str_re_line_parser = r'(?P<date>(199[5-9]|20[0-2]\d)-[01]\d-[0-3]\d),'+\
                     r'(?P<explanation>.*?),'+\
                     r'(?P<hdurl>https?:.*?(\?rel=0|\.(wmv|tiff?|png|mpe?g|mp4|mov|jpe?g|gif) ?)|),'+\
                     r'(?P<media_type>image|other|video),'+\
                     r'(?P<service_version>v\d),'+\
                     r'(?P<title>.*?),'+\
                     r'(?P<url>https?:.*?|//player\.vimeo.*?|//www\.youtube.*?|),'+\
                     r'(?P<copyright>.*?)'

str_re_finditer_english_term=r'[-\w]+'

this_script  = sys.argv[0][-23:]
destination_markdown_content = r'''---
format: 
  html:
    toc: true
lang: fr-CA
language:
  title-block-author-single: "Par"
  title-block-published: "Génération le"
title: Rapport d'expérience bout en bout
subtitle: Généré automatiquement par ''' + this_script + r'''
date: today
date-format: "YYYY-MM-DD"
author: Martin Laplante (24121010)
---

%(main_content)s
'''

## Point d'entrée
#
if __name__=="__main__":
    
    sections = {}

    # 1. Lecture du fichier CSV.
    with open(source_apod_csv_path, 
              encoding=source_apod_csv_encoding) as input_text:
        text = input_text.read()
    print('Fichier lu.')
    
    # 2. Traitement des lignes.
    lines = re.split(str_re_split_lines, text)
    sections["Sommaire"] = {
        "intro":"Voici les résultats de la lecture de `%s`"%(source_apod_csv_path,),
        "content":"\n  * **Nombre de lignes**: %d (incluant l'entête)."%(len(lines),),
    }
    heading = lines[0].split(',')
    sections['Sommaire']['content'] += "\n  * **Nombre de colonnes**: %d:"%(len(heading),)
    sections['Sommaire']['content'] += "\n\n    *" + '*, *'.join([col for col in heading])+'*'
    print(len(lines),"lignes")

    # 3. Construction d'une liste d'enregistrements (début du chronomètre)    
    t0 = time.time()
    records = []
    for position_, each_line in enumerate(lines[1:]):            
        mo = re.match(str_re_line_parser, each_line, re.DOTALL|re.I)
        # Si le regex a produit un match object (mo), c'est que tous les 
        # éléments sont correctement acceptés et prêt à être placé dans un
        # dictionnaire, un pour chaque enregistrement.
        if mo:
            records.append(mo.groupdict())
            records[-1]['position']=position_
        else:
            print("Cette ligne n'a pas fonctionné",repr(each_line))
    sections['Sommaire']['content'] += "\n  * **Enregistrements trouvés**: %d."%(len(records),)
    print(len(records),"enregistrements. position du dernier:",records[-1]['position'])    

    # 4. On comptabilise les mots
    #    a) par termes
    count_per_english_term = collections.defaultdict(int)

    #    b) par termes, sans la casse
    count_per_english_term_LC = collections.defaultdict(int)
    
    #    c) selon un classement (entiers, acronymes, etc)
    english_term_repo = collections.defaultdict(lambda:collections.defaultdict(int))

    #    d) Par terme, sans la casse, par article
    list_english_term_LC_per_article_position = collections.defaultdict(list)

    #    e) Nombre de termes par article, sans la casse
    count_english_term_LC_per_article_position = collections.defaultdict(lambda:collections.defaultdict(int))

    # On cherche aussi les doublons
    article_title_by_md5 = collections.defaultdict(list)

    # C'est ici aussi qu'on fait le calcul du tf-idf
    tf_per_article_position_per_term_LC = collections.defaultdict(dict) # TF(d,t)
    idf_per_term_LC = collections.defaultdict(float)                    # IDF(t)
    set_article_positions_by_term_LC = collections.defaultdict(set)
    td_idf_per_art_pos_per_term_LC = collections.defaultdict(dict)
    

    for i,record in enumerate(records):
        if i%1000==0:
            print("%6.3f%%"%(100*i/len(records),))
        position_of_article = record['position']
        for english_term in re.finditer(str_re_finditer_english_term,
                                        record['explanation']):
            term = english_term.group()
            term_LC = term.lower()
            count_per_english_term[term]+=1
            count_per_english_term_LC[term_LC]+=1
            list_english_term_LC_per_article_position[position_of_article].append(term_LC)
            count_english_term_LC_per_article_position[position_of_article][term_LC]+=1
            set_article_positions_by_term_LC[term_LC].add(position_of_article)

            # Classement selon des expressions simples (entiers, acronymes, etc)
            if re.match(r'^([1-9]\d*|0)$', term):
                english_term_repo['Entiers'][term]+=1
            elif re.match(r'^\d+$', term):
                english_term_repo['Séries de chiffres'][term]+=1
            elif re.match(r'^\d+(-\d+)+$',term):
                english_term_repo['Nombres unis par un "-"'][term]+=1
            elif re.match(r'^(\D+\d+)+\D*$', term):
                english_term_repo['Identificateurs 1'][term]+=1
            elif re.match(r'^(\d+\D+)+\d*$', term):
                english_term_repo['Identificateurs 2'][term]+=1
            elif re.match(r'^[A-Z]+(-[A-Z]+)*$', term):
                english_term_repo['Acronymes'][term]+=1
            elif re.match(r'^[A-Z][a-z]\w*(-[A-Z][a-z]\w*)*$', term):
                english_term_repo['Nom propres et début de phrases'][term]+=1
            elif re.match(r'^\w+(-+\w+)+$', term):
                english_term_repo['Mots composés, unis par un `-`'][term_LC]+=1
            elif re.match(r'^\w+-+$', term):
                english_term_repo['Se terminant avec un `-`'][term_LC]+=1
            elif re.match(r'^[a-z]+$', term_LC):
                english_term_repo['Mots simples'][term_LC]+=1
            else:
                english_term_repo['Autres'][term_LC]+=1
        # NB:Les collections sous `english_term_repo` se recoupent, et c'est normal.

        # On forme une clée en calculant le hash des mots mis bout en bout.
        # Si deux listes identiques s'y trouvent, elles vont engendrer le meme hash.
        md5 = hashlib.md5(''.join(list_english_term_LC_per_article_position[position_of_article]).encode()).hexdigest()
        record['md5_article'] = md5
        article_title_by_md5[md5].append("%(date)s: %(title)s"%record)

        # Calcul de du tf pour chaque terme de l'article courant.
        total_word_in_article = sum(count_english_term_LC_per_article_position[position_of_article].values())
        if total_word_in_article!=0:
            for word in count_english_term_LC_per_article_position[position_of_article]:
                tf_per_article_position_per_term_LC[position_of_article][word] = count_english_term_LC_per_article_position[position_of_article][word] / total_word_in_article
        if position_of_article==0:
            print(repr(tf_per_article_position_per_term_LC[position_of_article]))
    print("Tous les mots sont comptés.",len(count_english_term_LC_per_article_position),"positions.")

    # Articles dupliqués
    nb_articles_en_trop = sum(len(v)-1 for v in article_title_by_md5.values() if len(v)>1)
    sections['Articles en multiple copies'] = {'content':'\nIl y a %d articles recopiés.\n\n'%(nb_articles_en_trop,)}
    for md5, art in article_title_by_md5.items():
        if len(art)>1:
            sections['Articles en multiple copies']['content'] += '\n  * **%s**: %d articles'%(md5, len(art))
            #print(md5,len(art),"articles:")
            for a in art:
                sections['Articles en multiple copies']['content'] += '\n    * %s'%(repr(a),)
    print("il y a ", nb_articles_en_trop, "articles qui sont dupliqués")

    # IDF 
    for term_LC, count in count_per_english_term_LC.items():
        idf_per_term_LC[term_LC] = math.log(len(records)/len(set_article_positions_by_term_LC[term_LC]))

    # TF-IDF pour tous les articles et les termes:
    for art_pos, terms_LC in tf_per_article_position_per_term_LC.items():
        for term_LC in terms_LC:
            td_idf_per_art_pos_per_term_LC[art_pos][term_LC] = tf_per_article_position_per_term_LC[art_pos][term_LC] * \
                                                               idf_per_term_LC[term_LC]
    
    duration = time.time() - t0      

    sections['Sommaire']['content'] += "\n  * **Durée totale**: %9.6f secondes."%(duration,)
    sections['Sommaire']['content'] += "\n  * **Termes distincts**: %d."%(len(count_per_english_term),)
    sections['Sommaire']['content'] += "\n  * **Mots distincts**: %d (sans casse)."%(len(count_per_english_term_LC),)
    sum_count = sum(count_per_english_term.values())
    sections['Sommaire']['content'] += "\n  * **Termes au total**: %d."%(sum_count,)
    sections['Sommaire']['content'] += "\n  * **Durée moyenne par terme**: %11.9f &mu;S."%(1000000*duration/sum_count,)
    
    for k,v in    english_term_repo.items():
        sections[k] = {}
        sections[k]['content'] =  "\n  * **Nombre de termes trouvés**: %d"%(sum(v.values()),)
        sections[k]['content'] += "\n  * **Nombre de termes distincts trouvés**: %d"%(len(v),) 
        
        simple_words = [(_v,_k) for _k,_v in v.items()]
        tmp = []
        for _v,_k in reversed(sorted(simple_words)):
            tmp.append("<b>%s</b>:&nbsp;%d;"%(_k,_v))
        sections[k]['content'] += '\n\n\n<span style="font-size:xx-small">' + ' '.join(tmp) + '</span>\n\n\n'

    # Construction de M.  C'est ici que la fenetre glissante intervient
    word_at_column = []  # liste de mots ordonés par ordre de détection.
    
    for i in range(1,29):
        for word in list_english_term_LC_per_article_position[i]:
            if word in {'nemiroff','bonnell','jerry', 'robert', 'astronomy','see', 'day',
                        'we', 'page', 'press', 'picture', 'copyrighted'}: continue
            if word not in word_at_column:
                word_at_column.append(word)
    print(word_at_column[:100])
    M = []
    for i in range(1,29):
        m = [0.0]*len(word_at_column)
        for j,w in enumerate(word_at_column):
            tf_idf = td_idf_per_art_pos_per_term_LC[i].get(w)
            if tf_idf != None:
                m[j]=tf_idf
        M.append(m)


    mat = np.matrix(M)
    model = NMF(n_components=10, init='random', random_state=42)  
    W = model.fit_transform(np.array(mat))
    H = model.components_

    print(np.shape(W),"<== W")
    print(np.shape(H),"<== H")
    
    catego_headline = collections.defaultdict(list)
    for r in range(np.shape(H)[0]):
        for c,item in enumerate(H[r]):
            catego_headline[r].append((item,c))
        temp = list(reversed(sorted(catego_headline[r])))
        print( *temp[:5], sep=';')
        print('/'.join([word_at_column[itm[1]] for itm in temp[:5] if itm[0]]))
        articles = []
        for ap in range(np.shape(W)[0]):
            articles.append((W[ap][r],ap+1))
        t2 = list(reversed(sorted(articles)))
        print(*t2[:2],sep='\n\t')
        print()
    


    # Serialisation pour le rapport final
    main_content = []

    for title, each_section in sections.items():
        main_content.append("# %(title)s"%locals())
        if each_section.get('intro'):
            main_content.append("%(intro)s"%each_section)
        if type(each_section.get('content'))==str:
            main_content.append(each_section['content'])
            continue
        for subtitle, each_subsection in each_section.get('content',{}).items():
            main_content.append("## %(subtitle)s"%locals())
            if each_subsection.get('intro'):
                main_content.append("%(intro)s"%each_subsection)
            main_content.append(each_subsection.get("content",''))
    print("Serialisation complétée.")

    main_content = '\n\n'.join(main_content)

    with open(destination_markdown_path,'w+t', 
              encoding=destination_markdown_encoding) as output_text:
        _=output_text.write(destination_markdown_content%locals())
    print("Sortie complétée.")