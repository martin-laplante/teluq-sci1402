import feedparser
import re

feedlist = [
"https://feeds.bbci.co.uk/news/rss.xml",
"https://feeds.bbci.co.uk/news/technology/rss.xml",
"https://feeds.bbci.co.uk/news/business/rss.xml",
"https://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
"https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
"https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
"https://rss.nytimes.com/services/xml/rss/nyt/Business.xml",
"https://rss.nytimes.com/services/xml/rss/nyt/Science.xml",
#"https://ici.radio-canada.ca/rss/41",
#"https://ici.radio-canada.ca/rss/42",
#"https://ici.radio-canada.ca/rss/51",
#"https://ici.radio-canada.ca/rss/48",
##"https://www.lemonde.fr/international/rss_full.xml",
##"https://www.lemonde.fr/pixels/rss_full.xml",
##"https://www.lemonde.fr/economie/rss_full.xml",
##"https://www.lemonde.fr/sciences/rss_full.xml",
"http://rss.cnn.com/rss/cnn_topstories.rss",
#"https://www.reutersagency.com/feed/?best-topics=world-news&post_type=best",  

#'http://today.reuters.com/rss/topNews',
          #'http://today.reuters.com/rss/domesticNews',
          #'http://today.reuters.com/rss/worldNews',
          #'http://hosted.ap.org/lineups/TOPHEADS-rss_2.0.xml',
          #'http://hosted.ap.org/lineups/USHEADS-rss_2.0.xml',
          #'http://hosted.ap.org/lineups/WORLDHEADS-rss_2.0.xml',
          #'http://hosted.ap.org/lineups/POLITICSHEADS-rss_2.0.xml',
          'http://www.nytimes.com/services/xml/rss/nyt/HomePage.xml',
          #'http://www.nytimes.com/services/xml/rss/nyt/International.xml',
          'http://news.google.com/?output=rss',
          #'http://feeds.salon.com/salon/news',
          #'http://www.foxnews.com/xmlfeed/rss/0,4313,0,00.rss',
          #ttp://www.foxnews.com/xmlfeed/rss/0,4313,80,00.rss',
          #'http://www.foxnews.com/xmlfeed/rss/0,4313,81,00.rss',
           'http://rss.cnn.com/rss/edition.rss',
           'http://rss.cnn.com/rss/edition_world.rss',
           'http://rss.cnn.com/rss/edition_us.rss'
]


phys_org_rsses = [
"https://phys.org/rss-feed/biology-news/",
"https://phys.org/rss-feed/biology-news/agriculture/",
"https://phys.org/rss-feed/biology-news/biology-other/",
"https://phys.org/rss-feed/biology-news/biotechnology/",
"https://phys.org/rss-feed/biology-news/ecology/",
"https://phys.org/rss-feed/biology-news/evolution/",
"https://phys.org/rss-feed/biology-news/microbiology/",
"https://phys.org/rss-feed/biology-news/molecular-computational/",
"https://phys.org/rss-feed/biology-news/paleontology/",
"https://phys.org/rss-feed/biology-news/plants-animals/",
"https://phys.org/rss-feed/biology-news/veterinary-medicine/",
"https://phys.org/rss-feed/breaking/biology-news/",
"https://phys.org/rss-feed/breaking/biology-news/agriculture/",
"https://phys.org/rss-feed/breaking/biology-news/biology-other/",
"https://phys.org/rss-feed/breaking/biology-news/biotechnology/",
"https://phys.org/rss-feed/breaking/biology-news/ecology/",
"https://phys.org/rss-feed/breaking/biology-news/evolution/",
"https://phys.org/rss-feed/breaking/biology-news/microbiology/",
"https://phys.org/rss-feed/breaking/biology-news/molecular-computational/",
"https://phys.org/rss-feed/breaking/biology-news/paleontology/",
"https://phys.org/rss-feed/breaking/biology-news/plants-animals/",
"https://phys.org/rss-feed/breaking/biology-news/veterinary-medicine/",
"https://phys.org/rss-feed/breaking/chemistry-news/",
"https://phys.org/rss-feed/breaking/chemistry-news/analytical-chemistry/",
"https://phys.org/rss-feed/breaking/chemistry-news/biochemistry/",
"https://phys.org/rss-feed/breaking/chemistry-news/chemistry-other/",
"https://phys.org/rss-feed/breaking/chemistry-news/materials-science/",
"https://phys.org/rss-feed/breaking/chemistry-news/polymers/",
"https://phys.org/rss-feed/breaking/earth-news/",
"https://phys.org/rss-feed/breaking/earth-news/earth-sciences/",
"https://phys.org/rss-feed/breaking/earth-news/environment/",
"https://phys.org/rss-feed/breaking/nanotech-news/",
"https://phys.org/rss-feed/breaking/nanotech-news/bio-medicine/",
"https://phys.org/rss-feed/breaking/nanotech-news/nano-materials/",
"https://phys.org/rss-feed/breaking/nanotech-news/nano-physics/",
"https://phys.org/rss-feed/breaking/physics-news/",
"https://phys.org/rss-feed/breaking/physics-news/materials/",
"https://phys.org/rss-feed/breaking/physics-news/optics-photonics/",
"https://phys.org/rss-feed/breaking/physics-news/physics/",
"https://phys.org/rss-feed/breaking/physics-news/plasma/",
"https://phys.org/rss-feed/breaking/physics-news/quantum-physics/",
"https://phys.org/rss-feed/breaking/physics-news/soft-matter/",
"https://phys.org/rss-feed/breaking/physics-news/superconductivity/",
"https://phys.org/rss-feed/breaking/science-news/",
"https://phys.org/rss-feed/breaking/science-news/archaeology-fossils/",
"https://phys.org/rss-feed/breaking/science-news/economics-business/",
"https://phys.org/rss-feed/breaking/science-news/education/",
"https://phys.org/rss-feed/breaking/science-news/mathematics/",
"https://phys.org/rss-feed/breaking/science-news/political-science/",
"https://phys.org/rss-feed/breaking/science-news/sci-other/",
"https://phys.org/rss-feed/breaking/science-news/social-sciences/",
"https://phys.org/rss-feed/breaking/space-news/",
"https://phys.org/rss-feed/breaking/space-news/astrobiology/",
"https://phys.org/rss-feed/breaking/space-news/astronomy/",
"https://phys.org/rss-feed/breaking/space-news/planetary-sciences/",
"https://phys.org/rss-feed/breaking/space-news/space-exploration/",
"https://phys.org/rss-feed/chemistry-news/",
"https://phys.org/rss-feed/chemistry-news/analytical-chemistry/",
"https://phys.org/rss-feed/chemistry-news/biochemistry/",
"https://phys.org/rss-feed/chemistry-news/chemistry-other/",
"https://phys.org/rss-feed/chemistry-news/materials-science/",
"https://phys.org/rss-feed/chemistry-news/polymers/",
"https://phys.org/rss-feed/earth-news/",
"https://phys.org/rss-feed/earth-news/earth-sciences/",
"https://phys.org/rss-feed/earth-news/environment/",
"https://phys.org/rss-feed/nanotech-news/",
"https://phys.org/rss-feed/nanotech-news/bio-medicine/",
"https://phys.org/rss-feed/nanotech-news/nano-materials/",
"https://phys.org/rss-feed/nanotech-news/nano-physics/",
"https://phys.org/rss-feed/physics-news/",
"https://phys.org/rss-feed/physics-news/materials/",
"https://phys.org/rss-feed/physics-news/optics-photonics/",
"https://phys.org/rss-feed/physics-news/physics/",
"https://phys.org/rss-feed/physics-news/plasma/",
"https://phys.org/rss-feed/physics-news/quantum-physics/",
"https://phys.org/rss-feed/physics-news/soft-matter/",
"https://phys.org/rss-feed/physics-news/superconductivity/",
"https://phys.org/rss-feed/science-news/",
"https://phys.org/rss-feed/science-news/archaeology-fossils/",
"https://phys.org/rss-feed/science-news/economics-business/",
"https://phys.org/rss-feed/science-news/education/",
"https://phys.org/rss-feed/science-news/mathematics/",
"https://phys.org/rss-feed/science-news/political-science/",
"https://phys.org/rss-feed/science-news/sci-other/",
"https://phys.org/rss-feed/science-news/social-sciences/",
"https://phys.org/rss-feed/space-news/",
"https://phys.org/rss-feed/space-news/astrobiology/",
"https://phys.org/rss-feed/space-news/astronomy/",
"https://phys.org/rss-feed/space-news/planetary-sciences/",
"https://phys.org/rss-feed/space-news/space-exploration/",
]


def stripHTML(h):
  p=''
  s=0
  for c in h:
    if c=='<': s=1
    elif c=='>':
      s=0
      p+=' '
    elif s==0: p+=c
  return p

other_useless = {
  'about', 'above', 'across', 'after', 'against', 'along', 'although', 'among', 'around', 
  'because', 'been', 'before', 'behind', 'below', 'beneath', 'beside', 'between', 'beyond', 'both', 
  'could', 
  'does', 'during', 
  'each', 'either', 'every', 'except', 
  'from', 
  'have', 
  'into', 
  'less', 'like', 
  'many', 'might', 'mine', 'much', 'must', 'more',
  'near', 'neither', 
  'ours', 'over', 
  'past', 
  'shall', 'should', 'since', 'some', 'such', 
  'than', 'that', 'their', 'them', 'these', 'they', 'this', 'those', 'through', 'toward', 
  'under', 'unless', 'until', 'upon', 
  'were', 'what', 'when', 'whether', 'which', 'who', 'whom', 'whose', 'why' 'will', 'with', 'within', 'without', 'would', 
  'your'
}

def separatewords(text):
  splitter=re.compile(r'\W+')
  return [s.lower() for s in splitter.split(text) if len(s)>3 and s.lower() not in other_useless]

def getarticlewords(feedlist):
  allwords={}
  articlewords=[]
  articletitles=[]
  ec=0
  # Loop over every feed
  for feed in feedlist:
    f=feedparser.parse(feed)
    if len(f.entries)==0:
      print(feed, '->', 'comment')    
    # Loop over every article
    for e in f.entries:
      # Ignore identical articles
      if e.title in articletitles: continue
      
      # Extract the words
      title = e.get('title', '')
      description = e.get('description') or e.get('summary') or ''

      txt = title + ' ' + stripHTML(description)

      words=separatewords(txt)
      articlewords.append({})
      articletitles.append(title)
      
      # Increase the counts for this word in allwords and in articlewords
      for word in words:
        allwords.setdefault(word,0)
        allwords[word]+=1
        articlewords[ec].setdefault(word,0)
        articlewords[ec][word]+=1
      ec+=1

  print(f"Articles : {len(articletitles)}")
  print(f"Mots différents : {len(allwords)}")
  #print(f"Nombre de mots total : {sum(allwords.values())}")

  return allwords,articlewords,articletitles

def makematrix(allw,articlew):
  wordvec=[]
  
  # Only take words that are common but not too common
  for w,c in allw.items():
    if w and c>3 and c<len(articlew)*0.6:
      wordvec.append(w) 
  
  # Create the word matrix
  l1=[[(word in f and f[word] or 0) for word in wordvec] for f in articlew]
  return l1,wordvec

from numpy import *

def showfeatures(w,h,titles,wordvec,out='features.txt'): 
  outfile=open(out, 'w', encoding='utf-8')
  pc,wc=shape(h)
  toppatterns=[[] for i in range(len(titles))]
  patternnames=[]
  
  # Loop over all the features
  for i in range(pc):
    slist=[]
    # Create a list of words and their weights
    for j in range(wc):
      slist.append((h[i,j],wordvec[j]))
    # Reverse sort the word list
    slist.sort()
    slist.reverse()
    
    # Print the first six elements
    n=[s[1] for s in slist[0:6]]
    outfile.write(str(n)+'\n')
    patternnames.append(n)
    
    # Create a list of articles for this feature
    flist=[]
    for j in range(len(titles)):
      # Add the article with its weight
      flist.append((w[j,i],titles[j]))
      toppatterns[j].append((w[j,i],i,titles[j]))
    
    # Reverse sort the list
    flist.sort()
    flist.reverse()
    
    # Show the top 5 articles
    for f in flist[0:5]:
      outfile.write(str(f)+'\n')
    outfile.write('\n')

  outfile.close()
  # Return the pattern names for later use
  return toppatterns,patternnames

def showarticles(titles,toppatterns,patternnames,out='articles.txt'):
  outfile=open(out, 'w', encoding='utf-8')  
  
  # Loop over all the articles
  for j in range(len(titles)):
    outfile.write(titles[j].encode('utf8')+'\n')
    
    # Get the top features for this article and
    # reverse sort them
    toppatterns[j].sort()
    toppatterns[j].reverse()
    
    # Print the top three patterns
    for i in range(3):
      outfile.write(str(toppatterns[j][i][0])+' '+
                    str(patternnames[toppatterns[j][i][1]])+'\n')
    outfile.write('\n')
    
  outfile.close()
