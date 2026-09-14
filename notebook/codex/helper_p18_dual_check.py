"""Independent direct-integer checker for a uniformly lifted P18 dual.

Inputs are only the mathematical specification and a rational weight TSV.
The author's checker has not been read or imported.
"""
import argparse
import csv
from fractions import Fraction as F
from hashlib import sha256
from math import gcd, lcm
from pathlib import Path
import json

P=(1,5,6,7,9,11,13,18)


def killed(u,j,w):
    residue=(w*(15*j+1))%(15*u)
    return residue<u or residue>14*u


def primitive_deficits():
    return [(u,j) for u in P for j in range(u)
            if all(not killed(u,j,w) for w in P if w!=u)]


def grid_count(n,q,u,r):
    modulus=15*u*n
    return sum((residue:=q*(15*u*k+15*r+1)%modulus)<u*n
               or residue>14*u*n for k in range(n))


def read_weights(path):
    result={}
    with open(path) as f:
        for row in csv.DictReader(f,delimiter='\t'):
            key=int(row['anchor']),int(row['index'])
            assert key not in result, ('duplicate',key)
            result[key]=F(row['weight'])
            assert result[key]>=0
    assert sorted(result)==sorted(primitive_deficits()), (
        sorted(result),primitive_deficits())
    return result


def tail_classes(S):
    # For n=15m+r, ceiling(2n/15)=2m+ceil(2r/15).
    # S*ceiling<=n iff (15-2S)m >= S*ceil(2r/15)-r.
    assert S<F(15,2)
    records=[]
    for r in range(15):
        c=(2*r+14)//15
        threshold=(S*c-r)/(15-2*S)
        min_m=max(0,-((-threshold.numerator)//threshold.denominator))
        records.append({'residue':r, 'first_safe_m':min_m,
                        'largest_failing_n':15*(min_m-1)+r
                            if min_m else None})
    failures=[rec['largest_failing_n'] for rec in records
              if rec['largest_failing_n'] is not None]
    return max(failures,default=0)+1,records


def audit(path,H):
    assert not killed(1,0,1), 'equality is successful'
    assert killed(1,0,15), 'zero distance is forbidden'
    weights=read_weights(path)
    denominator=lcm(*(z.denominator for z in weights.values()))
    coefficients=[(u,r,int(z*denominator))
                  for (u,r),z in weights.items()]
    S=sum(weights.values())
    assert F(6)<S<=F(7),S
    max_value=F(0)
    maximizers=[]
    columns=0
    by_n=[]
    for n in range(1,H+1):
        nmax=0
        narg=[]
        ncolumns=0
        for q in range(1,max(P)*n):
            if gcd(n,q)!=1 or (n==1 and q in P):
                continue
            counts=[grid_count(n,q,u,r) for u,r,_ in coefficients]
            value=sum(c*w for c,(_,_,w) in zip(counts,coefficients))
            assert value<=denominator*n, (n,q,value,denominator*n)
            assert all(c<=(2*n+14)//15 for c in counts),(n,q,counts)
            if value>nmax:nmax,narg=value,[q]
            elif value==nmax:narg.append(q)
            exact=F(value,denominator*n)
            if exact>max_value:max_value,maximizers=exact,[(n,q)]
            elif exact==max_value:maximizers.append((n,q))
            columns+=1
            ncolumns+=1
        by_n.append({'n':n,'columns':ncolumns,
                     'maximum':str(F(nmax,denominator*n)),
                     'maximizers':narg})
    # Reconstruct actual c-fold lifts separately, checking every candidate
    # extra speed for c=1,...,30 against the reduced denominator semantics.
    lift_cases=0
    for c in range(1,31):
        for w in range(1,max(P)*c):
            if w in {c*u for u in P}:
                continue
            g=gcd(c,w)
            n,q=c//g,w//g
            lhs=sum(z*sum(killed(c*u,r+u*ell,w) for ell in range(c))/c
                    for (u,r),z in weights.items())
            rhs=sum(z*grid_count(n,q,u,r)/n for (u,r),z in weights.items())
            assert lhs==rhs,(c,w,lhs,rhs)
            assert lhs<=1,(c,w,lhs)
            lift_cases+=1
    cutoff,tail=tail_classes(S)
    assert H>=cutoff-1
    return {'primitive_speeds':P,'primitive_deficits':primitive_deficits(),
            'total_weight':str(S),'weight_denominator':denominator,
            'finite_max_denominator':H,'finite_columns_checked':columns,
            'maximum_column_weight':str(max_value),'maximizers':maximizers,
            'lift_scales_checked':[1,30],'lift_columns_checked':lift_cases,
            'analytic_tail_starts_at':cutoff,'tail_residue_classes':tail,
            'finite_details':by_n,'weight_sha256':sha256(Path(path).read_bytes()).hexdigest(),
            'checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}


def main():
    global P
    p=argparse.ArgumentParser()
    p.add_argument('weights')
    p.add_argument('--H',type=int,default=83)
    p.add_argument('--primitive',default='1,5,6,7,9,11,13,18')
    p.add_argument('--output',required=True)
    a=p.parse_args()
    P=tuple(map(int,a.primitive.split(',')))
    assert P==tuple(sorted(set(P))) and min(P)>0
    out=audit(a.weights,a.H)
    Path(a.output).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items()
                      if k not in ('finite_details','tail_residue_classes',
                                   'primitive_deficits')},indent=2))


if __name__=='__main__':main()
