import gzip,pickle
import numpy as np
import random,math
from itertools import permutations
import sys,datetime
import networkx as nx

def remove_envy_cycle(B,U,V):
    r=0
    while True:
        r+=1
        print("In envy cycle removal:",r)
        # create empty graph
        G=nx.DiGraph()
        # add nodes
        G.add_nodes_from(U)
        # edges
        E=[]
        # find edges
        print("In envy cycle removal: finding edges")
        for u in U:
            for v in U:
                if u!=v:
                    V_u=0
                    V_v=0
                    for p in B[u]:
                        V_u+=V[u,p]
                    for p in B[v]:
                        V_v+=V[u,p]
                    if V_v>V_u:
                        E.append((u,v))
        # add edges to the graph
        G.add_edges_from(E) 
        # find cycle and remove
        print("In envy cycle removal: graph done, finding and removing cycles")        
        try:
            cycle=nx.find_cycle(G,orientation="original")
            temp=B[cycle[0][0]][:]
            for pair in cycle:
                B[pair[0]]=B[pair[1]][:]
            B[cycle[-1][0]]=temp[:]
        except:
            break
    # topological sort
    U=list(nx.topological_sort(G))
    return B.copy(),U[:]

# greedy round robin allocation based on a specific ordering of customers
# This is the modified greedy round robin where we remove envy cycles
def greedy_round_robin(m,n,R,l,T,V,U,F):
    print(m,n,R,l,T,V.shape,len(U))

    # creating empty allocations
    B={}
    for u in U:
        B[u]=[]
    
    # available number of copies of each producer
    Z={} # total availability
    P=range(n) # set of producers
    for p in P:
        Z[p]=l
    
    # number of rounds
    r=0
    while True:
        # number of rounds
        r=r+1
        # allocating the producers to customers
        print("GRR round number==============================",r)
        
        for i in range(m):
            #user
            u=U[i]
            
            # choosing the p_ which is available and also in feasible set for the user
            possible=[(Z[p]>0)*(p in F[u])*V[u,p] for p in range(n)] 
            p_=np.argmax(possible)                             
                
            if (Z[p_]>0) and (p_ in F[u]) and len(F[u])>0:
                B[u].append(p_)
                F[u].remove(p_)
                Z[p_]=Z[p_]-1
                T=T-1
                

            else: #stopping criteria                
                print("now doing envy cycle removal")
                B,U=remove_envy_cycle(B.copy(),U[:],V)
                return B.copy(),F.copy()
            
            if T==0: #stopping criteria                
                print("now doing envy cycle removal")
                B,U=remove_envy_cycle(B.copy(),U[:],V)              
                return B.copy(),F.copy()
        # envy-based manipulations, m, U, V, B.copy()
        print("GRR done")        
      
        # remove envy cycle
        print("now doing envy cycle removal")
        B,U=remove_envy_cycle(B.copy(),U[:],V)
        print(sum([len(B[u]) for u in B]),T,n*l)
    # returning the allocation
    return B.copy(),F.copy();


def FairRecPlus(U,P,k,V,alpha):    
    # Allocation set for each customer, initially it is set to empty set
    A={}
    for u in U:
        A[u]=[]
    
    # feasible set for each customer, initially it is set to P
    F={}
    for u in U:
        F[u]=P[:]
    #print(sum([len(F[u]) for u in U]))
   
    # l= number of copies of each producer, equal to the exposure guarantee for producers
    l=int(alpha*m*k/(n+0.0))

    # R= number of rounds of allocation to be done in first GRR
    R=int(math.ceil((l*n)/(m+0.0)))    

    
    # T= total number of products to be allocated
    T= l*n
       
    # first greedy round-robin allocation
    B={}
    [B,F1]=greedy_round_robin(m,n,R,l,T,V,U[:],F.copy())
    F={}
    F=F1.copy()
    print("GRR done")
    # adding the allocation
    for u in U:
        A[u]=A[u][:]+B[u][:]
        

    # filling the recommendation set upto size k
    u_less=[]
    for u in A:
        if len(A[u])<k:
            u_less.append(u)
    for u in u_less:
        scores=V[u,:]
        new=scores.argsort()[-(k+k):][::-1]
        for p in new:
            if p not in A[u]:
                A[u].append(p)
            if len(A[u])==k:
                break
    end_time=datetime.datetime.now()    
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
    A=FairRecPlus(U,P,reco_size,V,alpha)

    # saving the results in pickle format (dictionary format { <customer> : <recommended_products_list> })
    f_out=gzip.open(dataset[:-4]+"_"+str(alpha)+"_k_"+str(reco_size)+".pkl.gz","wb")
    pickle.dump(A,f_out,-1)
    f_out.close()
