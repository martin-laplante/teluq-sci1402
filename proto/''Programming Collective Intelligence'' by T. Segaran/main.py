from numpy import *
import newsfeatures
import nmf

if __name__=="__main__":
    allw, artw, artt = newsfeatures.getarticlewords(newsfeatures.phys_org_rsses)
    #print(f"Articles : {len(artt)}")
    #print(f"Mots : {len(allw)}")

    wordmatrix, wordvec = newsfeatures.makematrix(allw, artw)
    #print(f"Wordvec : {len(wordvec)}")
    print(artt[1])
    print(wordvec[:10])

    v = matrix(wordmatrix)
    print("v completed.")
    weights, feat = nmf.factorize(v, pc=3, _iter=500)
    print("factorize completed.")

    topp, pn = newsfeatures.showfeatures(weights, feat, artt, wordvec)