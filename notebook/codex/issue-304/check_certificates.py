"""Exact author certificate audit. Uses only the Python standard library.

This is not an independent implementation of universal_dual.py. Cross-party
review must write a checker from the mathematical specification instead.
"""
import csv
import hashlib
import json
from fractions import Fraction
from math import gcd
from pathlib import Path

ROOT = Path(__file__).parent
CASES = [
    ('p18', (1,5,6,7,9,11,13,18)),
    ('p18-6-14', (1,5,6,9,11,13,14,18)),
    ('p18-12-7', (1,5,7,9,11,12,13,18)),
    ('p18-12-14', (1,5,9,11,12,13,14,18)),
]


def allowed(x, speed):
    a = (x.numerator*speed) % x.denominator
    return 15*min(a, x.denominator-a) >= x.denominator


def translate_count(x, n, q):
    a = q*x.numerator % x.denominator
    N = 15*x.denominator
    b = 15*a
    return -((b-n*x.denominator)//N) - ((-n*x.denominator-b)//N)-1


def audit(tag, pattern):
    path = ROOT/f'{tag}-weights.tsv'
    with path.open() as f:
        records = list(csv.DictReader(f, delimiter='\t'))
    atoms = []
    keys = []
    for row in records:
        u,r = int(row['anchor']),int(row['index'])
        z = Fraction(row['weight'])
        assert u in pattern and 0<=r<u and z>=0
        x = Fraction(15*r+1,15*u)
        assert all(allowed(x,v) for v in pattern), (u,r,'not a fixed deficit')
        keys.append((u,r))
        atoms.append((x,z))
    assert len(keys)==len(set(keys))
    total = sum(z for _,z in atoms)
    assert 6<total<=Fraction(61,10),total
    maxima=[]
    columns=0
    for n in range(1,31):
        worst=(Fraction(-1),0)
        for q in range(1,max(pattern)*n):
            if gcd(n,q)>1 or (n==1 and q in pattern):continue
            load=sum(z*translate_count(x,n,q) for x,z in atoms)/n
            assert load<=1,(tag,n,q,load)
            worst=max(worst,(load,q))
            columns+=1
        maxima.append({'n':n,'maximum':str(worst[0]),'q':worst[1]})
    # For n>=31: (61/10)(2n+14)/(15n)<=1, as 854<=28n.
    assert 854<=28*31
    return {'tag':tag,'pattern':pattern,'atoms':len(atoms),'total':str(total),
            'columns':columns,'finite_maximum':str(max(Fraction(x['maximum']) for x in maxima)),
            'finite_bound':30,'analytic_tail_starts':31,'per_denominator':maxima,
            'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}


if __name__=='__main__':
    print('Sanity: 14 moving / 15 total; one common rational time; common scaling only.')
    # Equality, including both boundaries, must not count as forbidden.
    assert translate_count(Fraction(1,15),1,1)==0
    assert translate_count(Fraction(14,15),1,1)==0
    assert translate_count(Fraction(0),1,1)==1
    # A reported witness fixture lies exactly on several forbidden-arc boundaries.
    fixture=Fraction(1,15)
    assert all(allowed(fixture,v) for v in range(1,15))
    assert min(min((fixture*v)%1,(-fixture*v)%1) for v in range(1,15))==Fraction(1,15)
    results=[audit(tag,p) for tag,p in CASES]
    for result in results:
        print(result['tag'],'mass',result['total'],'max',result['finite_maximum'],
              'columns',result['columns'],'sha256',result['sha256'])
    (ROOT/'p18-author-audits.json').write_text(json.dumps(results,indent=2)+'\n')
