"""Discover and exactly author-check universal measures for nine-speed cores.

New eight-row attack, separate from all frozen seven-row artifacts.
Floating optimization only discovers candidates; the accepted output has exact
positive rational atoms, mass >5, and checked finite column inequalities.
"""
from fractions import Fraction as F
from math import gcd
from pathlib import Path
import argparse, hashlib, json
import numpy as np
from scipy.optimize import linprog

HERE=Path(__file__).parent


def safe(x,P):
    return all(15*min(v*x%1,-v*x%1)>=1 for v in P)


def count(x,n,q):
    a=q*x.numerator%x.denominator
    D=15*x.denominator; b=15*a
    return -((b-n*x.denominator)//D)-((-n*x.denominator-b)//D)-1


def atoms(P,subdivide=4):
    edges=sorted({F(0),F(1)}|{F(15*k+s,15*v)%1 for v in P
                 for k in range(v) for s in (-1,1)})
    candidates={x for x in edges if safe(x,P)}
    for lo,hi in zip(edges,edges[1:]):
        if safe((lo+hi)/2,P):
            candidates.update(lo+(hi-lo)*i/subdivide for i in range(1,subdivide))
    # Reflection leaves all conditional bad counts unchanged.
    return sorted({min(x,1-x) for x in candidates})


def solve(P,subdivide=4):
    P=tuple(sorted(P)); X=atoms(P,subdivide)
    pairs=[(n,q) for n in range(1,15) for q in range(1,max(P)*n)
           if gcd(n,q)==1 and not(n==1 and q in P)]
    C=np.array([[count(x,n,q) for x in X] for n,q in pairs],dtype=np.int64)
    A=C/np.array([n for n,q in pairs])[:,None]
    lp=linprog(-np.ones(len(X)),A_ub=np.vstack([A,np.ones(len(X))]),
               b_ub=np.r_[np.ones(len(pairs)),5.1],bounds=(0,None),method='highs')
    if not lp.success or -lp.fun<=5+1e-7:
        return {'pattern':P,'status':'discovery failed','candidate_atoms':len(X),
                'optimum':float(-lp.fun) if lp.success else None}
    for den in (10000,1000000,100000000):
        w=[max(0,int(float(z)*(1-1e-8)*den)) for z in lp.x]
        total=sum(w)
        if total<=5*den or 10*total>51*den:continue
        accepted=[(x,z) for x,z in zip(X,w) if z]
        assert all(z>0 and safe(x,P) for x,z in accepted)
        loads=[(sum(z*count(x,n,q) for x,z in accepted),n,q) for n,q in pairs]
        if any(z>n*den for z,n,q in loads):continue
        worst=max((F(z,n*den),n,q) for z,n,q in loads)
        return {'pattern':P,'status':'sketch; exact author check passed',
                'total':str(F(total,den)),'atoms':[[str(x),str(F(z,den))] for x,z in accepted],
                'columns':len(pairs),'maximum_load':str(worst[0]),
                'maximum_pair':list(worst[1:]),'candidate_atoms':len(X)}
    return {'pattern':P,'status':'rationalization failed','optimum':float(-lp.fun)}


def initial_census(M):
    # Exact small anchor census, direct bit masks; not a finite reduction.
    from itertools import combinations
    masks=[]
    for w in range(1,M):
        masks.append(sum(1<<j for j in range(M)
                         if min(w*(15*j+1)%(15*M),(-w*(15*j+1))%(15*M))<M))
    full=(1<<M)-1
    result=[]
    for inds in combinations(range(M-1),8):
        if gcd(M,*[i+1 for i in inds])!=1:continue
        union=0
        for i in inds: union|=masks[i]
        if union!=full:continue
        if any((lambda other: other==full)(__import__('functools').reduce(int.__or__,
               (masks[j] for j in inds if j!=i),0)) for i in inds):continue
        result.append(tuple(i+1 for i in inds)+(M,))
    return result


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--max',type=int,default=15)
    ap.add_argument('--input');ap.add_argument('--output',default='eight-core-phase-m15.json')
    ar=ap.parse_args()
    print('SANITY:14 moving/15 total; positive atoms at one common time; strict forbidden arcs; common core scaling.',flush=True)
    assert count(F(1,15),1,1)==0 and count(F(14,15),1,1)==0 and count(F(0),1,1)==1
    assert 51*(2*15+14)<=150*15
    patterns=json.loads(Path(ar.input).read_text()) if ar.input else initial_census(ar.max)
    print('Patterns',len(patterns),flush=True)
    cases=[]
    for i,P in enumerate(patterns):
        result=solve(P);cases.append(result)
        print(i+1,P,result['status'],result.get('total'),result.get('maximum_load'),flush=True)
        (HERE/ar.output).write_text(json.dumps({'status':'sketch; no classification claim',
          'fixed_speeds':9,'extra_speeds':5,'finite_denominators':'1 through 14',
          'tail_starts':15,'mass_cap':'51/10','cases':cases,
          'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n')
