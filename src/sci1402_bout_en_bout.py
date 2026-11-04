import collections
import re
import sys
import time

###############################################################################
## Configuration
###############################################################################
source_apod_csv_path = r'..\data\APOD\NASA APOD 1995-2026\nasa_apod_complete.csv'
source_apod_csv_encoding = 'utf-8-sig'

###############################################################################
## Définitions - "Factory Settings"
###############################################################################
destination_markdown_path = r'.\sci1402_bout_en_bout.Qmd'
destination_markdown_encoding = 'utf-8-sig'
str_re_split_lines = r'\r?\n(?=199[56789]-\d\d-\d\d|20[012]\d-\d\d-\d\d)'
str_re_line_parser = r'(?P<date>(199[5-9]|20[0-2]\d)-[01]\d-[0-3]\d),'+\
                     r'(?P<explanation>.*?),'+\
                     r'(?P<hdurl>https?:.*?(\?rel=0|\.(wmv|tiff?|png|mpe?g|mp4|mov|jpe?g|gif) ?)|),'+\
                     r'(?P<media_type>image|other|video),'+\
                     r'(?P<service_version>v\d),'+\
                     r'(?P<title>.*?),'+\
                     r'(?P<url>https?:.*?|//player\.vimeo.*?|//www\.youtube.*?|),'+\
                     r'(?P<copyright>.*?)'
str_re_finditer_english_term=r'\w[-\w]*'

this_script  = sys.argv[0][-23:]
destination_markdown_content = r'''---
format: html
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
    lines = re.split(str_re_split_lines, text)
    sections["Sommaire"] = {
        "intro":"Voici les résultats de la lecture de `%s`"%(source_apod_csv_path,),
        "content":"\n  * **Nombre de lignes**: %d (incluant l'entête)."%(len(lines),),
    }
    heading = lines[0].split(',')
    sections['Sommaire']['content'] += "\n  * **Nombre de colonnes**: %d:"%(len(heading),)
    sections['Sommaire']['content'] += "\n\n    *" + '*, *'.join([col for col in heading])+'*'


    # Construction d'une liste d'enregistrements
    t0 = time.time()
    records = []
    for each_line in lines[1:]:            
        mo = re.match(str_re_line_parser, each_line, re.DOTALL|re.I)
        # Si le regex a produit un match object (mo), c'est que tous les 
        # éléments sont correctement acceptés et prêt à être placé dans un
        # dictionnaire, un pour chaque enregistrement.
        if mo:
            records.append(mo.groupdict())
        else:
            print("Cette ligne n'a pas fonctionné",repr(each_line))
    
    sections['Sommaire']['content'] += "\n  * **enregistrements trouvés**: %d."%(len(records),)

    # On comptabilise les mots
    count_per_english_term = collections.defaultdict(int)
    count_per_english_term_LC = collections.defaultdict(int)
    count_per_english_word_LC = collections.defaultdict(int)
    for record in records:
        for english_term in re.finditer(str_re_finditer_english_term,
                                        record['explanation']):
            count_per_english_term[english_term.group()]+=1
            count_per_english_term_LC[english_term.group().lower()]+=1
            if re.match(r'^([1-9]\d*|0)$', english_term.group()):
                pass 
            elif re.match(r'^\d+$', english_term.group()):
                pass
            elif re.match(r'^(\D+\d+)+\D*$', english_term.group()):
                pass
            elif re.match(r'^(\d+\D+)+\d*$', english_term.group()):
                pass
            elif re.match(r'^[A-Z]+$', english_term.group()):
                pass
            elif re.match(r'^\w+(-+\w+)+$', english_term.group()):
                pass
            elif re.match(r'^\w+-+$', english_term.group()):
                pass
            elif re.match(r'^[a-z]+$', english_term.group().lower()):
                count_per_english_word_LC[english_term.group().lower()]+=1
            else:
                pass 
    duration = time.time() - t0      
    sections['Sommaire']['content'] += "\n  * **Durée totale**: %9.6f secondes."%(duration,)
    sections['Sommaire']['content'] += "\n  * **termes distincts**: %d."%(len(count_per_english_term),)
    sections['Sommaire']['content'] += "\n  * **mots distincts**: %d (sans casse)."%(len(count_per_english_term_LC),)
    sum_count = sum(count_per_english_term.values())
    sections['Sommaire']['content'] += "\n  * **termes au total**: %d."%(sum_count,)
    sections['Sommaire']['content'] += "\n  * **Durée moyenne par terme**: %11.9f &mu;S."%(1000000*duration/sum_count,)
    sections["Mot simples"] = {}
    sections['Mot simples']['content'] =  "\n  * **Nombre de mots simples trouvés**: %d"%(sum(count_per_english_word_LC.values()),)
    sections['Mot simples']['content'] += "\n  * **Nombre de mots distincts trouvés**: %d"%(len(count_per_english_word_LC),) 

    simple_words = [(v,k) for k,v in count_per_english_word_LC.items()]
    tmp = []
    for v,k in reversed(sorted(simple_words)):
        tmp.append("<b>%s</b>:&nbsp;%d;"%(k,v))
    sections['Mot simples']['content'] += '\n\n\n<span style="font-size:smallest;">' + ' '.join(tmp) + '</span>\n\n\n'

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

    main_content = '\n\n'.join(main_content)

    with open(destination_markdown_path,'w+t', 
              encoding=destination_markdown_encoding) as output_text:
        _=output_text.write(destination_markdown_content%locals())