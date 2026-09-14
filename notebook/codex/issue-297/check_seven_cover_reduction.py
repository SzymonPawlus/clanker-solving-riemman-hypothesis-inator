"""Tiny exact audit of the finite table and row semantics in the proof note."""
from collections import Counter
from pathlib import Path
from math import gcd, prod
import json
import sys

EXPECTED = {
    6: [1,2,3,4,5,6,8,9,10,11,12,16,17,18,23,24],
    5: [1,2,3,4,5,8,9,10],
    4: [1,2,3,4,8],
    3: [1,2,3],
    2: [1,2],
    1: [1],
}


if __name__=='__main__':
    sets={}
    for p, expected in EXPECTED.items():
        cutoff=14*p//(15-2*p)
        got=[n for n in range(1,cutoff+1) if p*((2*n+14)//15)>=n]
        assert got==expected
        sets[p]=got
    product=91*prod(max(row) for row in sets.values())
    assert product==1048320
    first_periods=[h for h in range(2,92) if 7*((2*h+13)//15)>=h]
    candidates=set(first_periods)
    for p in (6,5,4,3,2,1):
        candidates={m*n for m in candidates for n in sets[p]}
    assert len(first_periods)==48 and len(candidates)==4324
    candidates={m for m in candidates if m>=8}
    assert len(candidates)==4318
    outside=[m for m in sorted(candidates) if all(m%d for d in (18,24,30))]
    assert len(outside)==1746
    if len(sys.argv)==2:
        Path(sys.argv[1]).write_text(json.dumps({
            'status':'sketch; necessary finite domain, not a completed search',
            'first_periods':first_periods,'remaining_multiplier_sets':sets,
            'candidate_maxima':sorted(candidates),
            'outside_18_24_30_divisibility':outside},indent=2)+'\n')
    diagnostic_rows=diagnostic_classes=0
    boundary_safe=noncoprime15_rows=0
    for h in range(2,181):
        divisors=[d for d in range(1,h+1) if h%d==0]
        for a in range(1,h):
            if gcd(a,h)!=1:continue
            bad=[]
            for j in range(h):
                residue=a*(15*j+1)%(15*h)
                distance=min(residue,15*h-residue)
                if distance<h:bad.append(j)
                if distance==h:
                    assert j not in bad
                    boundary_safe+=1
            assert len(bad)<=(2*h+13)//15
            for d in divisors:
                counts=Counter(j%d for j in bad)
                n=h//d
                assert max(counts.values(),default=0)<=(2*n+14)//15
                diagnostic_classes+=d
            diagnostic_rows+=1
            noncoprime15_rows+=gcd(a,15)>1
    print(json.dumps({'multiplier_sets':sets,'primitive_maximum_bound':product,
                      'candidate_maxima_after_distinctness':len(candidates),
                      'candidates_outside_18_24_30':len(outside),
                      'diagnostic_row_period_bound':180,'rows':diagnostic_rows,
                      'residue_classes':diagnostic_classes,
                      'safe_threshold_endpoints':boundary_safe,
                      'numerators_not_coprime_to15':noncoprime15_rows},indent=2))
