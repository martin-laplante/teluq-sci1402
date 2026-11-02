quelques_n_grammes = [('black', 'hole'), ('bright', 'star'), ('cassini', 'spacecraft'), ('cluster', 'stars'), ('color', 'image'),
                      ('dust', 'clouds'), ('dust', 'lanes'), ('earth', 's'), ('elliptical', 'orbit'), ('false', 'color'), ('full', 'moon'),
                      ('gamma', 'ray'), ('giant', 'stars'), ('globular', 'star', 'cluster'), ('glowing', 'gas'), ('high', 'energy'),
                      ('hubble', 'space', 'telescope'), ('hydrogen', 'gas'), ('image', 'data'), ('infrared', 'light'),
                      ('international', 'space', 'station'), ('james', 'webb', 'space', 'telescope'), ('light', 'years'), ('lunar', 'eclipse'),
                      ('magellanic', 'cloud'), ('magellanic', 'clouds'), ('magnetic', 'field'), ('massive', 'star'), ('massive', 'stars'),
                      ('meteor', 'shower'), ('milky', 'way'), ('million', 'light', 'years', 'away'), ('molecular', 'cloud'), ('near', 'infrared'),
                      ('night', 'sky'), ('northern', 'hemisphere'), ('orion', 'nebula'), ('parent', 'star'), ('planet', 'earth'), ('planetary', 'nebula'),
                      ('solar', 'eclipse'), ('solar', 'system'), ('space', 'shuttle'), ('space', 'station'), ('space', 'telescope'), ('spiral', 'arms'),
                      ('spiral', 'galaxy'), ('star', 'cluster'), ('star', 'clusters'), ('star', 'formation'), ('star', 'forming', 'regions'),
                      ('supernova', 'remnant'), ('unaided', 'eye'), ('visible', 'light'), ('white', 'dwarf'), ('wide', 'field'), ('x', 'ray'),
                      ('x', 'rays'), ('young', 'stars')]

skipp = '|'.join('''approximately
aproximately
accomplished
anticipated
impressive
additional
measuring
currently
ambitious
annotated
september
estimated
measures
covering
december
november
february
acquired
although
allowing
adopting
actually
achieved
perhaps
january
between
beneath
roughly
exactly
amazing
another
ancient
october
merely
covers
before
within
nearly
browse
during
across
adrift
august
around
almost
until
spans
march
inner
below
early
april
after
since
every
their
added
about
again
above
that
mere
than
year
with
full
last
lies
many
each
some
from
next
span
post
near
this
apod
june
also
only
over
july
past
for
its
the
and
may
oct
are
air
aka
all
age'''.split())


if True:
    import collections
    count_by_split = collections.defaultdict(int)
    import re
    celes = re.compile(r'(?<=\W)([bcdfghjklmnpqrstvwxz]{1,2}|[a-z]{3,}) ?\d+(\+\d+)?(?=\W)', re.I)
    count_oc = collections.defaultdict(int)
    import time
    with open(r'C:\Users\Martin\Desktop\teluq-sci1402\data\APOD\NASA APOD 1995-2026\nasa_apod_complete.csv','rb') as inbin:
        data = inbin.read()
    texte = data.decode()
    lignes = re.split(r'\r?\n(?=199[56789]-\d\d-\d\d|20[012]\d-\d\d-\d\d)',texte)
    hier = -1
    premiers = []
    for i,l in enumerate(lignes[1:],2):
        mo = re.match(r'(?P<date>(199[5-9]|20[0-2]\d)-[01]\d-[0-3]\d),(?P<explanation>.*?),(?P<hdurl>https?:.*?(\?rel=0|\.(wmv|tiff?|png|mpe?g|mp4|mov|jpe?g|gif) ?)|),(?P<media_type>image|other|video),v1,(?P<title>.*?),(?P<url>https?:.*?|//player\.vimeo.*?|//www\.youtube.*?|),(?P<copyright>.*?)',l,re.DOTALL|re.I)
        if mo==None:
            print(i,repr(l))
        else:
            journee = time.strptime(mo.groupdict()['date'], "%Y-%m-%d")
            journee = time.mktime(journee)
            if hier>0 and (journee - hier) not in (90000,86400,86400-3600):
                print(mo.groupdict()['date'],"Ecart",(journee - hier)/86400,journee - hier,'jours', journee, hier)
            hier = journee
            explication = mo.groupdict()['explanation']

            # remove CR/LF + other W/S
            expl_1 = re.sub(r'\r?\n|\r|\t|\xa0',' ',explication,flags=re.I)
#            if expl_1!=explication:
 #               print(repr(explication))
  #              print(repr(expl_1))
   #             print()
            for mo in celes.finditer(expl_1.lower()):
                if re.match(r'^('+skipp+r') \d+$',mo.group()):continue
#                if re.match(r'^(hershel|herschel|falcon|ugc|hcg|hd|gemini|messier|gliese|grb|eso|barnard|voyager|artemis|asteroid|arp|apollo|abell|luna|afgl|aco|ngc|ic) \d+$',mo.group()):continue
 #               if re.match(r'^(hayabusa|canadarm|hfg|hde?|grb|gw|m|g)\d+$',mo.group()):continue
                if re.match(r'^((hersc?hel|canadarm|hayabusa|surveyor|mariner|pioneer|sputnik|falcon|pismis|venera|viking|hde|[bcdfghjklmnpqrstvwxz]{2,}|[gjnrmvx])[- ]?\d+)(\+\d+)?$',mo.group()):continue
                count_oc[mo.group()]+=1
            mots = []
            for split in explication.split():
                split = re.sub(r'\W+',' ',split)
                if split.lower() in {'the', 'of', 'a', 'in',
                                     'and', 'to', 'is', 'from', 'this',
                                     'as', 'on', 'by', 'that', 'are',
                                     'it', 'be', 'for', 'than',
                                     'an', 'its', 'above', 'but',
                                     'so', '--', 'across', 'also', 'away', 'been', 'can', 'has', 'have', 'into', 'just', 'left', 'like', 'many', 'may', 'more', 'most', 'near', 'new', 'not', 'now', 'only', 'or', 'our', 'out', 'over', 'seen', 'some', 'taken', 'these', 'they', 'through', 'toward', 'two', 'were', 'while', 'will', 'you',
                                     'with', 'was', 'at', 'about'}:continue
                for resplit in split.split():
                    if not resplit:continue
                    if re.match(r'^\d+$',resplit):continue
                    count_by_split[resplit.lower()]+=1
                    mots.append(resplit.lower())
            premiers.append(mots)
    print(i)
    L = []
    for split,nombre in count_by_split.items():
        L.append("%6d %s"%(nombre,split))
#    print(*sorted(L),sep="\n")
#  ~ 20k entries ...

    # Impression des mots des 10 premiers articles:
    for mots in premiers[:10]:
        print(mots[:10]) # 10 mots par articles

    #by_bigrams=collections.defaultdict(int)
    #by_trigrams=collections.defaultdict(int)
    by_4grams=collections.defaultdict(int)
    for mots in premiers:
    #    for i in range(len(mots)-1):
    #        by_bigrams [(mots[i],mots[i+1])]+=1
    #    for j in range(len(mots)-2):
    #        by_trigrams[(mots[j],mots[j+1],mots[j+2])]+=1
        for k in range(len(mots)-3):
            by_4grams  [(mots[k],mots[k+1],mots[k+2],mots[k+3])]+=1
    L2 = []
    #for grm,cnt in by_bigrams.items():
     #   if cnt>1:
      #      L2.append("%7d %s"%(cnt,grm))

    #for grm,cnt in by_trigrams.items():
     #   if cnt>1:
      #      L2.append("%7d %s"%(cnt,grm))

    for grm,cnt in by_4grams.items():
        if cnt>1:      
            L2.append("%7d %s"%(cnt,grm))


    #print(*sorted(L2)[-5000:],sep='\n')

    L_celes = []
    for co,count in count_oc.items():
        if count==1:continue
        L_celes.append("%5d %s"%(count,co))
    print(*sorted(L_celes),sep='\n')
