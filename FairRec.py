import gzip,pickle
import numpy as np
import random,math,sys


def greedy_round_robin(m,n,R,l,T,V,U,F): 
    # greedy round robin allocation based on a specific ordering of customers (assuming the ordering is done in the relevance scoring matrix before passing it here)
    
    # creating empty allocations
    B={}
    for u in U:
        B[u]=[]
    
    # available number of copies of each producer
    Z={} # total availability
    P=range(n) # set of producers
    for p in P:
        Z[p]=l
    
    # allocating the producers to customers
    for t in range(1,R+1):
        print("GRR round number==============================",t)
        for i in range(m):
            if T==0:
                return B,F
            u=U[i]
            # choosing the p_ which is available and also in feasible set for the user
            possible=[(Z[p]>0)*(p in F[u])*V[u,p] for p in range(n)] 
            p_=np.argmax(possible) 
            
            if (Z[p_]>0) and (p_ in F[u]) and len(F[u])>0:
                B[u].append(p_)
                F[u].remove(p_)
                Z[p_]=Z[p_]-1
                T=T-1
            else:
                return B,F
    # returning the allocation
    return B,F;


def FairRec(U,P,k,V,alpha):
    # Allocation set for each customer, initially it is set to empty set
    A={}
    for u in U:
        A[u]=[]

    # feasible set for each customer, initially it is set to P
    F={}
    for u in U:
        F[u]=P[:]
    #print(sum([len(F[u]) for u in U]))
   
    # number of copies of each producer
    l=int(alpha*m*k/(n+0.0))

    # R= number of rounds of allocation to be done in first GRR
    R=int(math.ceil((l*n)/(m+0.0)))  

    
    # total number of copies to be allocated
    T= l*n
       
    # first greedy round-robin allocation
    [B,F1]=greedy_round_robin(m,n,R,l,T,V,U[:],F.copy())
    F={}
    F=F1.copy()
    print("GRR done")
    # adding the allocation
    for u in U:        
        A[u]=A[u][:]+B[u][:]
    
    # second phase
    u_less=[] # customers allocated with <k products till now
    for u in A:
        if len(A[u])<k:
            u_less.append(u)

    # allocating every customer till k products
    for u in u_less:
        scores=V[u,:]
        new=scores.argsort()[-(k+k):][::-1]
        for p in new:
            if p not in A[u]:
                A[u].append(p)
            if len(A[u])==k:
                break

    return A;


if __name__== "__main__":
    # dataset
    dataset=sys.argv[1]
    # relevance scoring data
    V=np.loadtxt(dataset,delimiter=',')
    print("relevance scoring data loaded")

    m=V.shape[0] # number of customers
    n=V.shape[1] # number of producers
    
    U=range(m) # list of customers
    P=range(n) # list of producers
 

    # size of recommendation
    reco_size=int(sys.argv[2])

    # fraction of MMS to be guaranteed to every producer
    alpha=float(sys.argv[3])

    # calling FairRec
    A=FairRec(U,P,reco_size,V,alpha)

    # saving the results in pickle format (dictionary format { <customer> : <recommended_products_list> })
    f_out=gzip.open(dataset[:-4]+"_"+str(alpha)+"_k_"+str(reco_size)+".pkl.gz","wb")
    pickle.dump(A,f_out,-1)
    f_out.close()

