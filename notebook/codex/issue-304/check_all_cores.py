"""Exact author audit of the universal measures in all-twenty-cores.json.

No optimization package or earlier claim is used. This is author verification;
independent reviewers should implement the mathematical specification afresh.
"""
from fractions import Fraction as F
from math import gcd
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).parent


def hit_count(x,n,q):
    a=q*x.numerator % x.denominator
    den=15*x.denominator
    b=15*a
    return -((b-n*x.denominator)//den)-((-n*x.denominator-b)//den)-1


def check(case):
    p=case['pattern']
    atoms=[(F(x),F(z)) for x,z in case['atoms']]
    assert len(p)==8 and len(set(p))==8 and all(isinstance(v,int) and v>0 for v in p)
    assert len(set(x for x,_ in atoms))==len(atoms)
    for x,z in atoms:
        assert 0<=x<1 and z>0
        assert all(15*min(x*v%1,-x*v%1)>=1 for v in p),(case['tag'],x,'unsafe')
    mass=sum(z for _,z in atoms)
    assert mass==F(case['total']) and 6<mass<=F(61,10)
    maxima=[]
    columns=0
    for n in range(1,31):
        worst=(F(-1),0)
        for q in range(1,max(p)*n):
            if gcd(n,q)>1 or(n==1 and q in p):continue
            load=sum(z*hit_count(x,n,q) for x,z in atoms)/n
            assert load<=1,(case['tag'],n,q,load)
            worst=max(worst,(load,q));columns+=1
        maxima.append({'n':n,'load':str(worst[0]),'q':worst[1]})
    return {'tag':case['tag'],'mass':str(mass),'atoms':len(atoms),'columns':columns,
            'maximum_load':str(max(F(x['load']) for x in maxima)),
            'per_denominator':maxima}


if __name__=='__main__':
    print('SANITY: k14/fifteen total; one common time; strict arcs; arbitrary extra speeds.',flush=True)
    # Both boundary points are allowed; the center is forbidden.
    assert hit_count(F(1,15),1,1)==0
    assert hit_count(F(14,15),1,1)==0
    assert hit_count(F(0),1,1)==1
    # This tail covers every integer denominator n>=31 uniformly.
    assert 61*(2*31+14)<=150*31
    path=ROOT/'all-twenty-cores.json'
    manifest=json.loads(path.read_text())
    results=[]
    for case in manifest['cases']:
        result=check(case);results.append(result)
        print(result['tag'],'mass',result['mass'],'max',result['maximum_load'],
              'atoms',result['atoms'],'columns',result['columns'],flush=True)
    report={'manifest_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'status':'author exact audit passed; independent review required','cases':results}
    (ROOT/'all-twenty-author-audits.json').write_text(json.dumps(report,indent=2)+'\n')
