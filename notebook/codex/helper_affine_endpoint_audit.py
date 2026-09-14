"""Independent exact endpoint-hit and three-power valuation fixtures.

These test the conditional lift algebra, not the existence of a template
whose strict bad sets cover all open cells. No author code is imported.
"""
import argparse
from fractions import Fraction as F
from hashlib import sha256
from math import gcd
from pathlib import Path
import json


def v3(n):
    assert n
    n=abs(n);e=0
    while n%3==0:e+=1;n//=3
    return e


def grid(M,q):
    return {F(q*(15*j+1),15*M)%1 for j in range(M)}


def main():
    p=argparse.ArgumentParser();p.add_argument('--proof',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    rationals={F(u,v) for v in range(1,41) for u in range(v)}
    hit_comparisons=grids=0
    for M in range(1,61):
        for q in range(1,M+1):
            if gcd(q,M)!=1:continue
            sample=grid(M,q);assert len(sample)==M;grids+=1
            for z in rationals:
                u,v=z.numerator,z.denominator
                predicted=(15*M)%v==0 and ((15*M//v)*u-q)%15==0
                assert (z in sample)==predicted
                hit_comparisons+=1
    fixtures=[]
    for slopes in [list(range(1,41))+list(range(-40,0)),[9*k for k in range(1,9)]]:
        s=max(map(v3,slopes));e=min(map(v3,slopes))
        for n in range(4,9):
            M=3**n
            assert n>s and M>max(map(abs,slopes))
            for j in (1,2,3):
                q=M*j//7
                if q%3==0:q+=1
                pairs=[(a,-(a*q//M)) for a in slopes]
                speeds=[a*q+b*M for a,b in pairs]
                assert all(0<w<M for w in speeds) and len(set(speeds))==len(speeds)
                sample=grid(M,q);assert len(sample)==M
                assert all(v3(z.denominator)==n+1 for z in sample)
                endpoints={F(15*k-b+sign,15*a)%1 for a,b in pairs
                           for k in range(abs(a)) for sign in (-1,1)}
                assert all(v3(z.denominator)<=s+1 for z in endpoints)
                assert not sample&endpoints
                g=gcd(M,*speeds)
                assert g==gcd(M,*slopes)==3**e
                assert all(M//gcd(M,w)==3**(n-v3(a)) for w,a in zip(speeds,slopes))
                # Direct coordinate identity and normalization equality on
                # representative original and reduced anchor indices.
                checks=0
                for k in sorted({0,1,M//g-1}):
                    z=F(q*(15*k+1),15*M)%1
                    for w,(a,b) in zip(speeds,pairs):
                        actual=F(w*(15*k+1),15*M)%1
                        assert actual==(a*z+F(b,15))%1
                        assert actual==F((w//g)*(15*k+1),15*(M//g))%1
                        checks+=1
                fixtures.append(dict(M=M,q=q,slopes=slopes,common_gcd=g,
                                     endpoint_count=len(endpoints),sample_count=len(sample),
                                     minimum_row_period=min(M//gcd(M,w) for w in speeds),
                                     coordinate_checks=checks))
    report=dict(status='sketch support only; no covering template asserted',
                checker_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                proof_sha256=sha256(args.proof.read_bytes()).hexdigest(),
                exact_endpoint_grid_count=grids,endpoint_hit_comparisons=hit_comparisons,
                power_three_fixtures=fixtures,power_three_fixture_count=len(fixtures),
                boundary_disjointness_tests=sum(r['endpoint_count'] for r in fixtures),
                sample_valuation_checks=sum(r['sample_count'] for r in fixtures),
                coordinate_checks=sum(r['coordinate_checks'] for r in fixtures))
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print('PASS',grids,'general grids;',hit_comparisons,'endpoint decisions;',len(fixtures),'three-power fixtures')


if __name__=='__main__':main()
