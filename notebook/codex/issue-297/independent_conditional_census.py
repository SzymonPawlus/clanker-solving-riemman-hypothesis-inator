"""Manager's clean-room replay of the conditional 37-maximum classification.

Written from the residual-grid and high-charge mathematical specification,
without reading the helper's enumeration implementation.
"""
from math import gcd, lcm
from itertools import product
from pathlib import Path
import json
import argparse

E={r:tuple(n for n in range(1,29) if r*((2*n+14)//15)>=n) for r in range(1,7)}
REACH={0:{1}}
for r in range(1,6):
    REACH[r]={n*m for n in E[r] for m in REACH[r-1]}
MAXIMA=sorted({m*a*b*c for m,a,b,c in product((12,18,24,30,60),E[4],E[3],E[2])})


def enumerate_maximum(M):
    masks={}
    periods={}
    for w in range(1,M):
        mask=0
        for j in range(M):
            residue=w*(15*j+1)%(15*M)
            if min(residue,15*M-residue)<M:
                mask|=1<<j
        masks[w]=mask
        periods[w]=M//gcd(M,w)
    full=(1<<M)-1
    first=(M//2,M//3)
    start_covered=masks[first[0]]|masks[first[1]]
    results=set()
    visited=set()
    nodes=0
    def recurse(chosen,covered,joint):
        nonlocal nodes
        key=frozenset(chosen)
        if key in visited:return
        visited.add(key)
        nodes+=1
        remaining=7-len(chosen)
        missing=full^covered
        if not remaining:
            if not missing and joint==M:
                # Exact minimality, not merely a seven-element cover.
                if all(masks[w]&~__import__('functools').reduce(int.__or__,
                       (masks[v] for v in chosen if v!=w),0) for w in chosen):
                    base=frozenset(chosen)
                    results.add(tuple(sorted((*base,M))))
                    alternate=(base-{M//3})|{2*M//3}
                    results.add(tuple(sorted((*alternate,M))))
            return
        if not missing or M//joint not in REACH[remaining]:return
        need=missing.bit_count()
        for w,mask in masks.items():
            if w in chosen or w==2*M//3:continue
            nxt=lcm(joint,periods[w])
            multiplier=nxt//joint
            if multiplier not in E[remaining] or M//nxt not in REACH[remaining-1]:continue
            gain=(mask&missing).bit_count()
            if remaining*gain<need:continue
            recurse((*chosen,w),covered|mask,nxt)
    recurse(first,start_covered,6)
    certificates=[]
    for core in sorted(results):
        killers=core[:-1]
        private={}
        for w in killers:
            other=0
            for v in killers:
                if v!=w:other|=masks[v]
            alone=masks[w]&~other
            assert alone
            private[w]=(alone&-alone).bit_length()-1
        assert gcd(*core)==1
        certificates.append({'core':core,'private_indices':private})
    return {'maximum':M,'nodes':nodes,'complete':True,'primitive_cores':certificates}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path(__file__).with_name('independent-conditional-census-replay.json'))
    args=parser.parse_args()
    assert len(MAXIMA)==37
    reports=[]
    for M in MAXIMA:
        report=enumerate_maximum(M)
        reports.append(report)
        print(json.dumps({'M':M,'nodes':report['nodes'],'cores':len(report['primitive_cores'])}),flush=True)
    result={'status':'numerical/conditional sketch; all 37 candidate maxima complete',
            'assumptions':['inclusion-minimal seven-row maximal cover','primitive gcd1',
                           'period2 and period3 rows both present'],
            'maximum_candidates':MAXIMA,'reports':reports,
            'total_primitive_cores':sum(len(r['primitive_cores']) for r in reports),
            'total_nodes':sum(r['nodes'] for r in reports)}
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print('COMPLETE',result['total_primitive_cores'],result['total_nodes'])
