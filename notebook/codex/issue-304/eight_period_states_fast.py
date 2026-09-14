"""Integer-vectorized discovery front end for the exact eight-row graph.

Uses only int64 arrays within the explicitly bounded exploration; final graph
certificates still require independent replay of every physical row.
"""
from collections import Counter
from math import gcd
import argparse
import numpy as np
import eight_period_states as base


def children(L,R,p,r):
    found={}
    for d in base.divisors(L):
        counts=Counter(j%d for j in R)
        hist=np.zeros(d,dtype=np.int64)
        for j,c in counts.items():hist[j]=c
        for n in base.E[r]:
            if gcd(n,L//d)!=1:continue
            h=d*n
            if h<p:continue
            A=np.array([a for a in range(1,h) if gcd(a,h)==1],dtype=np.int64)
            if not len(A):continue
            lo=(-h-A)//15+1;hi=(h-1-A)//15
            hits=np.zeros(len(A),dtype=np.int64)
            lengths=hi-lo+1
            if int(lengths.max())<len(counts):
                inv=np.array([pow(int(a),-1,h) for a in A],dtype=np.int64)
                for offset in range(int(lengths.max())):
                    positions=((lo+offset)*inv%h)%d
                    hits+=hist[positions]*(offset<lengths)
            else:
                for j,c in counts.items():
                    residue=A*j%d
                    hits+=c*((hi-residue)//d-(lo-1-residue)//d)
            for a,hit in zip(A[hits*r>=len(R)*n],hits[hits*r>=len(R)*n]):
                a=int(a);B=set(base.bad(h,a))
                S=tuple(sorted(j+k*L for k in range(n) for j in R if(j+k*L)%h not in B))
                assert len(S)==len(R)*n-int(hit)
                key=base.minimize(L*n,S)
                found.setdefault(key,(h,a))
    return [(h,a,H,S) for(H,S),(h,a) in sorted(found.items())]


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('p',type=int,nargs='*')
    ap.add_argument('--check',action='store_true');ap.add_argument('--seconds',type=float,default=300)
    ap.add_argument('--max-nodes',type=int,default=100000);ap.add_argument('--max-period',type=int,default=50000)
    ap.add_argument('--resume',action='store_true');ar=ap.parse_args()
    if ar.check:
        tested=0
        for L in (4,5,6,8,12,18,30,60):
            for r in (1,3,5):
                R=tuple(j for j in range(L) if j%4 and j%3)
                if not R:continue
                assert children(L,R,4,r)==base.children(L,R,4,r),(L,r)
                tested+=1
        print('Exact scalar/vector child comparison passed',tested,'states',flush=True)
    base.children=children
    for p in ar.p:base.run(p,ar.max_nodes,ar.max_period,ar.seconds,ar.resume)
