"""Bounded affine-template discovery; exact positive outputs only.

For fixed rational x and integer slopes a, physical ratios are a*x-floor(a*x).
The corresponding continuous bad rows in z are ||a*z-floor(a*x)/15||<1/15.
If eight of these cover the circle, every sufficiently accurate large rational
x=q/M in the same floor chamber gives a large-period endpoint cover.
Absent candidates and solver infeasibility are exploratory only.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse,json,time
import numpy as np
from scipy.optimize import Bounds,LinearConstraint,milp

HERE=Path(__file__).parent

def mask_at(z,rows):
    den=15*z.denominator
    return tuple(int(min((15*a*z.numerator+b*z.denominator)%den,
                    (-15*a*z.numerator-b*z.denominator)%den)<z.denominator)
                 for a,b in rows)

def search(x,K,seconds,allow_isolated=False):
    rows=[(a,-(a*x.numerator//x.denominator)) for a in range(-K,K+1) if a]
    edges=sorted({F(0),F(1)}|{F(15*k-b+s,15*a)%1 for a,b in rows
                           for k in range(abs(a)) for s in (-1,1)})
    midpoints=[F(u+v,2) for u,v in zip(edges,edges[1:])]
    points=midpoints if allow_isolated else edges+midpoints
    masks={mask_at(z,rows) for z in points}
    zero=(0,)*len(rows)
    result={'x':str(x),'K':K,'rows':len(rows),'points':len(points),
            'distinct_constraints':len(masks)}
    if zero in masks:
        witness=next(z for z in points if mask_at(z,rows)==zero)
        return dict(result,status='all available rows fail at an exact circle point',witness=str(witness))
    A=np.array(sorted(masks),dtype=np.float64)
    A=np.vstack([A,np.ones(len(rows))]);lower=np.r_[np.ones(len(masks)),0]
    upper=np.r_[np.full(len(masks),np.inf),8]
    if allow_isolated:
        # At least one fifteenth-grid point must be bad, to choose the sampled
        # grid's compulsory fifteenth-grid point away from isolated witnesses.
        eligible=[int(any(any(mask_at(F(k,15),[row])) for k in range(15))) for row in rows]
        A=np.vstack([A,eligible]);lower=np.r_[lower,1];upper=np.r_[upper,np.inf]
    sol=milp(np.zeros(len(rows)),integrality=np.ones(len(rows)),bounds=Bounds(0,1),
             constraints=LinearConstraint(A,lower,upper),options={'time_limit':seconds})
    result.update(status='no candidate; bounded optimization is not an exact exclusion',
                  solver_status=int(sol.status))
    if sol.x is None:return result
    chosen=[rows[i] for i,v in enumerate(sol.x) if v>.5]
    if len(chosen)>8:return result
    assert all(any(mask_at(z,chosen)) for z in points)
    assert len(chosen)==8  # Seven strict arcs have total measure at most14/15.
    result.update(status='exact eight-row affine cell cover found' if allow_isolated else
                         'exact continuous eight-row affine cover found',chosen=chosen,
      isolated_safe_points=[str(z) for z in edges if not any(mask_at(z,chosen))],
      bad_fifteenths=[k for k in range(15) if any(mask_at(F(k,15),chosen))])
    if allow_isolated:
        result['physical']=materialize(x,chosen,result['bad_fifteenths'])
    return result


def materialize(x,rows,bad_fifteenths):
    from math import isqrt,gcd
    M=100003
    while True:
        while any(M%d==0 for d in range(2,isqrt(M)+1)):M+=1
        for r in bad_fifteenths:
            residue=M*r%15
            q=round(float(x)*M)
            q+=((residue-q+7)%15)-7
            P=[a*q+b*M for a,b in rows]
            if not(0<q<M and all(0<w<M for w in P)):continue
            assert gcd(q,M)==1 and len(set(P))==8
            j=np.arange(M,dtype=np.int64)
            s=np.array(P,dtype=np.int64)[:,None]*(15*j[None,:]+1)%(15*M)
            masks=np.minimum(s,15*M-s)<M
            assert np.all(masks.any(axis=0))
            multiplicity=masks.sum(axis=0)
            private={str(w):int(np.flatnonzero(masks[i]&(multiplicity==1))[0]) for i,w in enumerate(P)}
            return {'M':M,'q':q,'pattern':sorted(P)+[M],'minimum_period':M,
                    'private_endpoint':private,'grid_fifteenth':r}
        M=10*M+1

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--slopes',type=int,default=24)
    ap.add_argument('--seconds',type=float,default=2);ap.add_argument('--limit',type=int,default=0)
    ap.add_argument('--output',default='affine-template-discovery.json')
    ap.add_argument('--allow-isolated',action='store_true');ap.add_argument('--stride',type=int,default=1)
    ar=ap.parse_args()
    cuts=sorted({F(a,b) for b in range(1,ar.slopes+1) for a in range(b+1)})
    xs=[(a+b)/2 for a,b in zip(cuts,cuts[1:])]
    xs=xs[::ar.stride]
    if ar.limit:xs=xs[:ar.limit]
    reports=[]
    for i,x in enumerate(xs):
        r=search(x,ar.slopes,ar.seconds,ar.allow_isolated);reports.append(r)
        print(i+1,'/',len(xs),str(x),r['status'],r.get('chosen'),flush=True)
        (HERE/ar.output).write_text(json.dumps({'status':'bounded structured discovery; no global exclusion',
          'slopes':ar.slopes,'chambers_planned':len(xs),'reports':reports},indent=2)+'\n')
        if 'chosen' in r:break
