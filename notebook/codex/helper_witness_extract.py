"""Independent signed-score witness extraction, from integer definitions.

No manager/prover implementation was read. The floor sum is derived by
counting lattice points under a line, not translated from another checker.
"""
from fractions import Fraction as F
from random import Random
from math import gcd
from pathlib import Path
from hashlib import sha256
from time import perf_counter
import json

P=(1,5,6,7,9,11,13,18)


def floor_sum(N,a,b,m):
    """Sum floor((a*j+b)/m), 0<=j<N, for signed a,b and m>0."""
    assert N>=0 and m>0
    result,sign=0,1
    while N:
        qa,a=divmod(a,m)
        qb,b=divmod(b,m)
        result+=sign*(qa*N*(N-1)//2+qb*N)
        if not a:return result
        J=(a*(N-1)+b)//m
        # For each 1<=y<=J, exactly N-ceil((m*y-b)/a) points.
        result+=sign*N*J
        N,a,b,m,sign=J,m,m-b+a-1,a,-sign
    return result


def forbidden_count(u,r,c,w,L,R):
    assert 0<=L<=R<=c
    N=R-L
    m=15*u*c
    a=15*u*w
    b=w*(15*u*L+15*r+1)
    h=u*c
    # Count residues [0,h) and [14h+1,15h); equality h,14h survives.
    return N+floor_sum(N,a,b-(14*h+1),m)-floor_sum(N,a,b-h,m)


def literal_count(u,r,c,w,L,R):
    m=15*u*c
    h=u*c
    return sum((v:=w*(15*u*j+15*r+1)%m)<h or v>14*h
               for j in range(L,R))


def deficits():
    return [(u,r) for u in P for r in range(u)
            if all(literal_count(u,r,1,w,0,1)==0 for w in P)]


def score(u,r,c,extras,L,R):
    return R-L-sum(forbidden_count(u,r,c,w,L,R) for w in extras)


def extract(c,extras):
    assert c>=1 and len(extras)<=6
    assert all(0<abs(w)<=18*c for w in extras)
    extras=tuple(abs(w) for w in extras)
    for u,r in deficits():
        value=score(u,r,c,extras,0,c)
        if value>0:break
    else:raise AssertionError(('no positive fiber',c,extras))
    L,R=0,c
    steps=0
    while R-L>1:
        mid=(L+R)//2
        left=score(u,r,c,extras,L,mid)
        if left>0:R,value=mid,left
        else:L,value=mid,value-left
        assert value>0
        steps+=1
    assert value==1
    t=F(15*u*L+15*r+1,15*u*c)
    all_speeds=[c*v for v in P]+list(extras)
    margins=[min((v*t.numerator)%t.denominator,
                 (-v*t.numerator)%t.denominator)*15-t.denominator
             for v in all_speeds]
    assert min(margins)>=0,(t,all_speeds,margins)
    return {'u':u,'r':r,'lift_index':L,'time':str(t),
            'bisections':steps,'minimum_scaled_margin':min(margins)}


def audit():
    rng=Random(30120260914)
    floor_cases=0
    for N in range(10):
        for m in range(1,14):
            for a in range(-15,16):
                for b in range(-15,16):
                    got=floor_sum(N,a,b,m)
                    expected=sum((a*j+b)//m for j in range(N))
                    assert got==expected,(N,a,b,m,got,expected)
                    floor_cases+=1
    interval_cases=0
    for _ in range(20000):
        u=rng.choice(P)
        r=rng.randrange(u)
        c=rng.randrange(1,200)
        w=rng.randrange(1,18*c+1)
        L=rng.randrange(c+1)
        R=rng.randrange(L,c+1)
        got=forbidden_count(u,r,c,w,L,R)
        expected=literal_count(u,r,c,w,L,R)
        assert got==expected,(u,r,c,w,L,R,got,expected)
        interval_cases+=1
    witnesses=[]
    for c in range(1,101):
        allowed=[w for w in range(1,18*c) if w not in {c*v for v in P}]
        extras=rng.sample(allowed,6)
        witnesses.append({'c':c,'extras':extras,**extract(c,extras)})
    huge=[]
    for c in (10**30+57,10**100+267):
        extras=[rng.randrange(1,18*c) for _ in range(6)]
        start=perf_counter()
        result=extract(c,extras)
        huge.append({'c':c,'extras':extras,'elapsed_seconds':perf_counter()-start,
                     **result})
    return {'floor_sum_cases':floor_cases,'literal_interval_cases':interval_cases,
            'small_scale_witnesses':witnesses,'huge_scale_witnesses':huge,
            'checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}


if __name__=='__main__':
    out=audit()
    Path(__file__).with_name('helper-witness-extract-audit.json').write_text(
        json.dumps(out,indent=2)+'\n')
    print('floor',out['floor_sum_cases'],'interval',out['literal_interval_cases'],
          'witnesses',len(out['small_scale_witnesses']))
    for item in out['huge_scale_witnesses']:
        print('c_digits',len(str(item['c'])),'bisections',item['bisections'],
              'seconds',item['elapsed_seconds'],
              'min_scaled_margin',item['minimum_scaled_margin'])
