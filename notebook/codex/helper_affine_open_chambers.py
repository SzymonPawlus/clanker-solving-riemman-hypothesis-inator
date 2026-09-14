"""Independent exact cell-cover decisions for bounded affine floor chambers.

Rows are all nonzero integers a with |a|<=K, b=-floor(a*x). The finite
universe has every exact open circle cell. The older eligibility bit is
computed only for diagnostic output and is not required by this decision. No author solver
or checker is imported. Unfinished cases are explicitly incomplete.
"""
import argparse
from fractions import Fraction as F
from hashlib import sha256
from math import gcd,lcm
from pathlib import Path
from time import monotonic
import json


def bad(pair,z):
    a,b=pair;den=15*z.denominator
    r=(15*a*z.numerator+b*z.denominator)%den
    return min(r,den-r)<z.denominator


def circle_problem(pairs):
    ends={F(0),F(1)}
    for a,b in pairs:
        for k in range(abs(a)):
            for s in(-1,1):ends.add(F(15*k-b+s,15*a)%1)
    ends=sorted(ends);cells=[(left+right)/2 for left,right in zip(ends,ends[1:])]
    H=lcm(*(z.denominator for z in ends))
    widths=[int((right-left)*H) for left,right in zip(ends,ends[1:])]
    eligible_bit=1<<len(cells)
    masks=[]
    for pair in pairs:
        mask=sum(1<<j for j,z in enumerate(cells) if bad(pair,z))
        if any(bad(pair,F(ell,15)) for ell in range(15)):mask|=eligible_bit
        masks.append(mask)
    widths.append(0)
    assert sum(widths)==H and all(w>0 for w in widths[:-1])
    for mask in masks:
        assert sum(w for j,w in enumerate(widths) if mask>>j&1)*15==2*H
    return masks,widths,H,ends


def decide(pairs,seconds):
    start=monotonic();masks,widths,H,ends=circle_problem(pairs)
    full=(1<<(len(widths)-1))-1  # Open cells only; ignore the eligibility bit.
    supports=[[i for i,B in enumerate(masks) if B>>j&1] for j in range(len(widths))]
    priority=sorted(range(len(widths)),key=lambda j:len(supports[j]))
    failed=set();nodes=hits=measure_prunes=count_prunes=0

    def walk(R,r):
        nonlocal nodes,hits,measure_prunes,count_prunes
        nodes+=1
        if nodes%128==0 and monotonic()-start>seconds:raise TimeoutError
        if not R:return ()
        if not r:return None
        key=R,r
        if key in failed:hits+=1;return None
        weight=0;bits=R
        while bits:
            bit=bits&-bits;bits-=bit;weight+=widths[bit.bit_length()-1]
        if 15*weight>2*r*H:
            measure_prunes+=1;failed.add(key);return None
        gains=[(B&R).bit_count() for B in masks]
        if sum(sorted(gains,reverse=True)[:r])<R.bit_count():
            count_prunes+=1;failed.add(key);return None
        pivot=next(j for j in priority if R>>j&1)
        for i in sorted(supports[pivot],key=lambda i:gains[i],reverse=True):
            suffix=walk(R&~masks[i],r-1)
            if suffix is not None:return (i,)+suffix
        failed.add(key);return None

    complete=True;answer=None
    try:answer=walk(full,8)
    except TimeoutError:complete=False
    result={'complete':complete,'nodes':nodes,'cache_hits':hits,
            'measure_prunes':measure_prunes,'count_prunes':count_prunes,
            'circle_open_cells':len(widths)-1,'common_width_denominator':H,
            'elapsed_seconds':monotonic()-start,'cover':None}
    if answer is not None:
        chosen=[pairs[i] for i in answer]
        assert len(set(answer))==len(answer)<=8
        assert all(any(bad(pair,(left+right)/2) for pair in chosen) for left,right in zip(ends,ends[1:]))
        fifteenths=[ell for ell in range(15) if any(bad(pair,F(ell,15)) for pair in chosen)]
        assert all(any(bad(pair,(left+right)/2) for pair in chosen) for left,right in zip(ends,ends[1:]))
        isolated_safe=[str(z) for z in ends[:-1] if not any(bad(pair,z) for pair in chosen)]
        result['cover']={'pairs':chosen,'bad_fifteenths':fifteenths,'safe_boundary_points':isolated_safe}
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--K',type=int,default=24)
    p.add_argument('--seconds',type=float,default=3)
    p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    assert 1<=a.K<=40 and a.seconds>0
    # Generic circle-cover positive; no common floor chamber is claimed for it.
    positive=decide([(1,b) for b in range(0,15,2)],3)
    assert positive['complete'] and positive['cover']
    negative=decide([(1,0)]*8,3)
    assert negative['complete'] and not negative['cover']
    cuts=sorted({F(k,n) for n in range(1,a.K+1) for k in range(n+1)})
    result={'status':'numerical; exact bounded affine-template decisions only',
            'K':a.K,'slopes':'all nonzero integers a with |a|<=K',
            'chamber_count':len(cuts)-1,'seconds_cap_per_chamber':a.seconds,
            'condition':'all open circle cells covered; no condition on fifteenth points',
            'checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
            'positive_circle_fixture':positive,'negative_circle_fixture':negative,'chambers':[]}
    for index,(left,right) in enumerate(zip(cuts,cuts[1:]),1):
        x=(left+right)/2
        pairs=[(a,-(a*x.numerator//x.denominator)) for a in range(-a.K,a.K+1) if a]
        assert all(0<s*x+b<1 for s,b in pairs)
        rec=decide(pairs,a.seconds)
        rec.update(index=index,left=str(left),right=str(right),midpoint=str(x))
        result['chambers'].append(rec)
        a.output.write_text(json.dumps(result,indent=2)+'\n')
        print(index,str(left),str(right),rec['complete'],rec['nodes'],bool(rec['cover']),flush=True)
        if rec['cover']:break
    result['incomplete_chambers']=[r['index'] for r in result['chambers'] if not r['complete']]
    result['completed_chambers']=sum(r['complete'] for r in result['chambers'])
    result['covers_found']=sum(r['cover'] is not None for r in result['chambers'])
    a.output.write_text(json.dumps(result,indent=2)+'\n')
