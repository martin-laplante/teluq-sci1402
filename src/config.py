import re #                                                                    TODO: Bannieres, Copyrights, etc

#                                                                              TODO: Tansform to relative
apod_csv_path = r'C:\Users\Martin\Desktop\teluq-sci1402\data\APOD\NASA APOD 1995-2026\nasa_apod_complete.csv'




class KISS_logger(object):                                                    # YAGNI ?
    def D(self,*args):
        print(*args)
    def E(self,*args):
        import sys
        print(*(('** ERROR **',)+args), file=sys.stderr)

log = KISS_logger()


re_findall = re.compile(r'[-\w]+') # Stratégie de base : exporter avec les strategies

debug_add_word_stream = False












# Envoe besoin ?


line_sep = re.compile( r'\r?\n(?=199[56789]-\d\d-\d\d|20[012]\d-\d\d-\d\d)' )
### Le line parser ici est très utile, car en plus d'accepter selon la syntaxe d'une ligne, les éléments acceptés sont capturés dans un match object qui contient un dictionnaire dont les clés sont aligné avec l'entete du csv.
##
line_parser = re.compile(r'(?P<date>(199[5-9]|20[0-2]\d)-[01]\d-[0-3]\d),'+\
                            r'(?P<explanation>.*?),'+\
                            r'(?P<hdurl>https?:.*?(\?rel=0|\.(wmv|tiff?|png|mpe?g|mp4|mov|jpe?g|gif) ?)|),'+\
                            r'(?P<media_type>image|other|video),'+\
                            r'(?P<service_version>v\d),'+\
                            r'(?P<title>.*?),'+\
                            r'(?P<url>https?:.*?|//player\.vimeo.*?|//www\.youtube.*?|),'+\
                            r'(?P<copyright>.*?)',re.DOTALL|re.I)


sw_step = 1
sw_l_a_ = 25
n = 10