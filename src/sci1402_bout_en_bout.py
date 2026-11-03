
import sys
this_script  = sys.argv[0][-23:]
destination_markdown_path = './sci1402_bout_en_bout.Qmd'
destination_markdown_encoding = 'utf-8-sig'
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
# &nbsp;

'''

if __name__=="__main__":
    with open(destination_markdown_path,'w+t', encoding=destination_markdown_encoding) as output_text:
        _=output_text.write(destination_markdown_content)