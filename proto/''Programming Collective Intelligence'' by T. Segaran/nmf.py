from numpy import *

def difcost(a,b):
    dif=0
    # loop over everry row and column on the matrix
    for i in range(shape(a)[0]):
        for j in range(shape(a)[1]):
            # add togheter the differences
            dif += pow(a[i,j]-b[i,j],2)
    return dif
                                        
def factorize(v, pc=10,_iter=50):
    ic = shape(v)[0]
    fc = shape(v)[1]

    # initialize the weight and feature matrices with random values
    w=matrix([[random.random() for j in range(pc)] for i in range(ic)])
    h=matrix([[random.random() for i in range(fc)] for j in range(pc)])

    print("w finite :", isfinite(asarray(w)).all())
    print("h finite :", isfinite(asarray(h)).all())

    # Perform operation a maximum of iter times
    for i in range(_iter):
        wh=w*h

        # Calculate the current difference
        cost = difcost(v, wh)

        if i%10==0: print(cost)

        # Terminate if the matrix has been fully factorized
        if cost==0:break

        # Update Feature Matrix
        hn = (transpose(w)*v)
        hd = (transpose(w)*w*h)
        h =  matrix(array(h)*array(hn)/array(hd))

        # Update weights matrix
        wn=(v*transpose(h))
        wd=(w*h*transpose(h))

        wd_array = asarray(wd)

        print("Nombre de zéros dans wd :", count_nonzero(wd_array == 0))
        print("Nombre de valeurs non finies :", count_nonzero(~isfinite(wd_array)))
        indices = argwhere(wd_array == 0)
        print("Indices des zéros :", indices[:10])


        w = matrix(array(w)*array(wn)/array(wd))
        print("hd min =", min(hd))
        print("hd max =", max(hd))
        print("wd min =", min(wd))
        print("wd max =", max(wd))

    return w,h
        
    
