"""Generic discovery experiment; no claim is made when optimization fails."""
from fractions import Fraction as F
from math import gcd
from pathlib import Path
import argparse,json
import numpy as np
from scipy.optimize import linprog
from eight_core_phase import atoms,count,safe

HERE=Path(__file__).parent

def solve(P,r,subdivide=4):
    X=atoms(P,subdivide);cap=F(10*r+1,10)
    N=int(14*cap/(15-2*cap))
    pairs=[(n,q) for n in range(1,N+1) for q in range(1,max(P)*n)
           if gcd(n,q)==1 and not(n==1 and q in P)]
    print('atoms',len(X),'columns',len(pairs),'N',N,flush=True)
    C=np.array([[count(x,n,q) for x in X] for n,q in pairs],dtype=np.int64)
    ns=np.array([n for n,q in pairs])
    chosen=[i for i,(n,q) in enumerate(pairs) if n<=10]
    for iteration in range(30):
        A=C[chosen,:]/ns[chosen,None]
        lp=linprog(-np.ones(len(X)),A_ub=np.vstack([A,np.ones(len(X))]),
                   b_ub=np.r_[np.ones(len(chosen)),float(cap)],bounds=(0,None),method='highs')
        if not lp.success:return {'pattern':P,'extra':r,'status':'LP failed','message':lp.message}
        loads=(C@lp.x)/ns
        violation=np.flatnonzero(loads>1+1e-9)
        print('iteration',iteration,'mass',-lp.fun,'maxload',loads.max(),
              'violations',len(violation),flush=True)
        if not len(violation):break
        chosen=sorted(set(chosen)|set(map(int,violation)))
    result={'pattern':P,'extra':r,'candidate_atoms':len(X),'columns':len(pairs),
            'finite_max_n':N,'mass_cap':str(cap),'discovery_optimum':float(-lp.fun)}
    if -lp.fun<=r+1e-7:
        result['status']='failed on this finite atom grid; no nonexistence conclusion'
        return result
    for D in (10000,1000000,100000000):
        W=[max(0,int(float(z)*(1-1e-8)*D)) for z in lp.x]
        T=sum(W)
        if T<=r*D or F(T,D)>cap:continue
        accepted=[(x,z) for x,z in zip(X,W) if z]
        exactloads=[(sum(z*count(x,n,q) for x,z in accepted),n,q) for n,q in pairs]
        if any(z>n*D for z,n,q in exactloads):continue
        worst=max((F(z,n*D),n,q) for z,n,q in exactloads)
        result.update(status='sketch; exact author inequalities pass',total=str(F(T,D)),
          atoms=[[str(x),str(F(z,D))] for x,z in accepted],maximum_load=str(worst[0]),
          maximum_pair=list(worst[1:]))
        return result
    result['status']='rationalization failed';return result

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('speeds',type=int,nargs='+')
    ap.add_argument('--extra',type=int,required=True);ap.add_argument('--subdivide',type=int,default=4)
    ap.add_argument('--output',required=True);ar=ap.parse_args()
    result=solve(ar.speeds,ar.extra,ar.subdivide)
    (HERE/ar.output).write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
