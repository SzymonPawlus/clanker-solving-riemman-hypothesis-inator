"""Bounded discovery only for eight-row covers without periods two or three."""
from pathlib import Path
from math import gcd
import argparse,json,time
import numpy as np
from scipy.optimize import Bounds,LinearConstraint,milp

HERE=Path(__file__).parent

def search(M,seconds):
    rows=[w for w in range(1,M) if M//gcd(w,M)>=4]
    masks=np.array([[min(w*(15*j+1)%(15*M),(-w*(15*j+1))%(15*M))<M
                     for j in range(M)] for w in rows],dtype=np.int8)
    sizes=sorted(map(int,masks.sum(axis=1)),reverse=True)
    if 1+sum(s-1 for s in sizes[:8])<M:
        return {'M':M,'status':'excluded by exact shared-zero cardinality bound'}
    t=time.monotonic()
    lp=milp(np.ones(len(rows)),integrality=np.ones(len(rows)),bounds=Bounds(0,1),
       constraints=LinearConstraint(masks.T,np.ones(M),np.full(M,np.inf)),
       options={'time_limit':seconds,'mip_rel_gap':0})
    result={'M':M,'status':'no candidate; solver output not an exact exclusion',
            'solver_status':int(lp.status),'elapsed':round(time.monotonic()-t,3),
            'solver_objective':float(lp.fun) if lp.fun is not None else None,
            'solver_lower_bound':float(lp.mip_dual_bound) if getattr(lp,'mip_dual_bound',None) is not None else None}
    if lp.x is None:return result
    selected=[rows[i] for i,x in enumerate(lp.x) if x>.5]
    if len(selected)>8:return result
    # Exact direct verification and redundant-row deletion.
    B={w:{j for j in range(M) if min(w*(15*j+1)%(15*M),(-w*(15*j+1))%(15*M))<M}
       for w in selected}
    assert set.union(*B.values())==set(range(M))
    for w in selected[:]:
        if set.union(*(B[v] for v in selected if v!=w))==set(range(M)):selected.remove(w)
    assert len(selected)<=8 and all(M//gcd(w,M)>=4 for w in selected)
    c=gcd(M,*selected);P=[w//c for w in selected]+[M//c]
    result.update(status='exact counterexample to eight-row minimum-period-at-most-three proposal',
                  pattern=P,minimum_period=min(M//gcd(w,M) for w in selected),
                  private_residues={w:sorted(B[w]-set.union(*(B[v] for v in selected if v!=w))) for w in selected})
    return result

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--first',type=int,default=31)
    ap.add_argument('--last',type=int,default=300);ap.add_argument('--seconds',type=float,default=.5)
    ap.add_argument('--output',default='eight-minperiod-discovery.json');ar=ap.parse_args()
    reports=[]
    for M in range(ar.first,ar.last+1):
        r=search(M,ar.seconds);reports.append(r)
        print(M,r['status'],r.get('solver_objective'),r.get('pattern'),flush=True)
        (HERE/ar.output).write_text(json.dumps({'status':'bounded exploratory search; no unbounded exclusion',
              'reports':reports},indent=2)+'\n')
        if 'pattern' in r:break
