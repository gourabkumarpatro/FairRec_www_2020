import numpy as np
import gzip,pickle
import random,math
import operator

# Baselines: random-k and top-k
# INPUTS: fname= csv file with relevance scores, k= recommendation size
def generate_random_n_top_k(fname,k):
    # relevance scores
    V=np.loadtxt(fname,delimiter=',')
    
    m=V.shape[0] #number of customers
    n=V.shape[1] #number of producers

    U=range(m) #Customers
    P=range(n) #Producers
 
    # baseline1 = top-k recommendations
    B1={}
    # baseline2 = random-k recommendations
    B2={}

    for u in U:
        scores=V[u,:]
        B1[u]=scores.argsort()[-k:][::-1]
        B2[u]=random.sample(P,k)
    # Saving the results in pickle format
    f_out=gzip.open(fname[:-4]+"_top_k_"+str(k)+".pkl.gz","wb")
    pickle.dump(B1,f_out,-1)
    f_out.close()
    
    f_out=gzip.open(fname[:-4]+"_random_k_"+str(k)+".pkl.gz","wb")
    pickle.dump(B2,f_out,-1)
    f_out.close()
    
# Baseline: mixedTR-k (mix of top-k/2 and random-k/2)
# INPUTS: fname= csv file with relevance scores, k= recommendation size
def generate_mixedTR_k(fname,k):
    # relevance scores
    V=np.loadtxt(fname,delimiter=',')
    
    m=V.shape[0] #number of customers
    n=V.shape[1] #number of producers

    U=range(m) #Customers
    P=range(n) #Producers

    # mixedTR-k
    B={}

    for u in U:
        scores=V[u,:]
        l=int(math.ceil((k+0.0)/2))
        half=scores.argsort()[-l:][::-1]
        remaining_P=[]
        for p in P:
            if p not in half:
                remaining_P.append(p)
        other_half=random.sample(remaining_P,int(k-l))

        B[u]=[]
        # first half from top-k/2
        for i in half:
            B[u].append(i)
        # second half from random-k/2
        for i in other_half:
            B[u].append(i)        
    # Saving the results in pickle format
    f_out=gzip.open(fname[:-4]+"_mixedTR_k_"+str(k)+".pkl.gz","wb")
    pickle.dump(B,f_out,-1)
    f_out.close()
    
# Baseline: poorest-k
# INPUTS: fname= csv file with relevance scores, k= recommendation size
def generate_poorest_k(fname,k):
    # relevance scores
    V=np.loadtxt(fname,delimiter=',')
    
    m=V.shape[0] #number of customers
    n=V.shape[1] #number of producers

    U=range(m) #Customers
    P=range(n) #Producers

    # Exposures
    E={}
    for p in P:
        E[p]=0.0
        
    # poorest-k
    B={}
    for u in U:
        B[u]=[]
    
    # greedy round robin of producer-centric allocation: poorest-k
    for i in range(k):
        for u in U:
            # producers sorted based on increasing exposures and allocating the first feasible producer
            prod_sorted=sorted(E.items(),key=operator.itemgetter(1))
            for p_tuple in prod_sorted:
                p=p_tuple[0]
                if p not in B[u]:
                    E[p]+=1
                    B[u].append(p)
                    break
    # Saving the results in pickle format
    f_out=gzip.open(fname[:-4]+"_poorest_k_"+str(k)+".pkl.gz","wb")
    pickle.dump(B,f_out,-1)
    f_out.close()
    
    
# Baseline: mixedTP-k (mix of top-k/2 and poorest-k/2)
# INPUTS: fname= csv file with relevance scores, k= recommendation size
def generate_mixedTP_k(fname,k):
    # relevance scores
    V=np.loadtxt(fname,delimiter=',')
    
    m=V.shape[0] #number of customers
    n=V.shape[1] #number of producers

    U=range(m) #Customers
    P=range(n) #Producers
    
    # Recommendations
    B={}
    # Exposures
    E={}
    for p in range(n):
        E[p]=0.0
    for u in U:
        B[u]=[]
        scores=V[u,:]
        #top-k/2
        top_half=scores.argsort()[-int(math.ceil((k+0.0)/2)):][::-1]
        for p in top_half:
            B[u].append(p)
        # producers sorted based on increasing exposures and allocating the first feasible producer
        prod_sorted=sorted(E.items(),key=operator.itemgetter(1))
        prod_index=0
        while len(B[u])<k:
            p=prod_sorted[prod_index][0]
            #print(p)
            if p not in B[u]:
                B[u].append(p)
            prod_index+=1
        for p in B[u]:
            E[p]+=1.0
    # Saving the results in pickle format
    f_out=gzip.open(fname[:-4]+"_mixedTP_k_"+str(k)+".pkl.gz","wb")
    pickle.dump(B,f_out,-1)
    f_out.close()