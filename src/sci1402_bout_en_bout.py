import collections
import re
import sys
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
'''

## Point d'entrée
#
if __name__=="__main__":
    # 1. Lecture du fichier CSV.
    with open(source_apod_csv_path, 
              encoding=source_apod_csv_encoding) as input_text:
        text = input_text.read()
    print('Fichier lu.')
    lines = re.split(str_re_split_lines, text)
    print("%d lignes, incluant l'entête"%(len(lines),))
    heading = lines[0].split(',')
    print("%d colonnes:"%(len(heading),))
    print(" ",*[repr(col) for col in heading])

    # Construction d'une liste d'enregistrements
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
    print("%d enregistrements trouvés"%(len(records),))
    
    # On comptabilise les mots
    count_per_english_term = collections.defaultdict(int)
    for record in records:
        for english_term in re.finditer(str_re_finditer_english_term,
                                        record['explanation']):
            count_per_english_term[english_term.group().lower()]+=1
    print("%d mots distincts."%(len(count_per_english_term),))
    sum_count = sum(count_per_english_term.values())
    print("%d mots au total."%(sum_count,))
    print("100 mots les plus fréquents:")
    L = []
    for k,v in count_per_english_term.items():
        L.append("%7d %-15s (%6.3f%%)"%(v, repr(k), 100*v/sum_count))
    print(*sorted(L)[-100:],sep='\n')
    with open(destination_markdown_path,'w+t', 
              encoding=destination_markdown_encoding) as output_text:
        _=output_text.write(destination_markdown_content)