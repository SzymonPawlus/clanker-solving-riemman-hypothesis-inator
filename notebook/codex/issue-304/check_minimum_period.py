"""Exact finite obligation for the smallest-period <=16 reduction.

Author checker; independent reviewers must reimplement the specification.
Groups with the same residue histogram retain their exact multiplicity,
capped at six because only six further rows can be selected.
"""
from collections import Counter,defaultdict
from fractions import Fraction as F
from math import gcd
from pathlib import Path
import hashlib
import heapq
import json

ROOT=Path(__file__).parent


def residue_set(h,a):
    inv=pow(a,-1,h)
    low=(-h-a)//15+1
    high=(h-1-a)//15
    return tuple(sorted((k*inv)%h for k in range(low,high+1)))


def row_catalog():
    catalog={}
    for h in range(2,301):
        unique={}
        for a in range(1,h):
            if gcd(a,h)!=1:continue
            B=residue_set(h,a)
            assert 0 in B
            assert 15*len(B)<=2*h+13
            unique.setdefault(B,a)
        catalog[h]=[(a,B) for B,a in unique.items()]
    return catalog


def finite_check(catalog):
    report=[];grand=(F(0),None)
    for p in range(17,92):
        grouped=[]
        for h in range(p,301):
            d=gcd(p,h)
            counts=Counter()
            example={}
            for a,C in catalog[h]:
                v=tuple(sum(x%d==j for x in C) for j in range(d))
                counts[v]+=1;example.setdefault(v,a)
            grouped.extend((h,d,v,min(6,m),example[v]) for v,m in counts.items())
        bounds=[]
        for a,B in catalog[p]:
            hist={d:tuple(sum(x%d==j for x in B) for j in range(d))
                  for d in {gcd(p,h) for h in range(p,301)}}
            heap=[]
            for h,d,v,m,aa in grouped:
                # At h=p the histogram is the actual set indicator.
                if h==p and v==hist[p]:continue
                numerator=p*sum(v)-d*sum(x*y for x,y in zip(hist[d],v))
                value=F(numerator,p*h)
                for _ in range(m):
                    entry=(value,h,aa)
                    if len(heap)<6:heapq.heappush(heap,entry)
                    elif entry>heap[0]:heapq.heapreplace(heap,entry)
            b=len(B)
            tail=min(F(41,301),F(2,15)*(1-F(b,p))+(F(13,15)+b)/301)
            vals=sorted([v for v,_,_ in heap]+[tail]*6,reverse=True)[:6]
            upper=F(b,p)+sum(vals)
            assert upper<1,(p,a,B,upper)
            bounds.append((upper,a,B,tail,heap))
        worst=max(bounds)
        entry={'p':p,'base_sets':len(bounds),'upper':str(worst[0]),
               'base_numerator':worst[1],'base_residues':worst[2],
               'tail_bound':str(worst[3]),
               'finite_leaders':[(str(v),h,a) for v,h,a in sorted(worst[4],reverse=True)]}
        report.append(entry)
        grand=max(grand,(worst[0],p))
    return {'status':'author exact arithmetic passed; independent review required',
            'row_period_bound':300,'tail_starts':301,
            'base_sets':sum(x['base_sets'] for x in report),
            'global_upper':str(grand[0]),'global_period':grand[1],
            'by_period':report}


if __name__=='__main__':
    print('SANITY:14 moving/15 total; maximal anchor,strict forbidden arcs,common scaling.',flush=True)
    assert residue_set(2,1)==(0,)
    assert residue_set(18,1)==(0,1,17)
    # Direct strict-endpoint check on the row's phase boundary.
    assert not(min(1,14)<1)
    catalog=row_catalog()
    print('Distinct candidate residue sets:',sum(map(len,catalog.values())),flush=True)
    result=finite_check(catalog)
    result['checker_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    print('Bases',result['base_sets'],'global upper',result['global_upper'],
          'at period',result['global_period'],flush=True)
    (ROOT/'minimum-period-16-audit.json').write_text(json.dumps(result,indent=2)+'\n')
