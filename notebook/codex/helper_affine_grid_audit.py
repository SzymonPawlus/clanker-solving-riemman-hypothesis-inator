"""Exact orbit and boundary fixtures for the affine-template grid lemma."""
import argparse
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from math import gcd,lcm
from pathlib import Path
import json
import random


def audit_fixture(M,speeds,triples):
    w0=speeds[0]
    assert len(speeds)==len(triples)==8 and gcd(M,*speeds)==1
    assert all(0<w<M for w in speeds)
    assert triples[0]==(1,1,0)
    assert all(P and Q>0 and Q*w==P*w0+R*M for w,(P,Q,R) in zip(speeds,triples))
    L=lcm(*(Q for P,Q,R in triples))
    b=[L*P//Q for P,Q,R in triples];B=gcd(*map(abs,b))
    Pstar=lcm(*(abs(P) for P,Q,R in triples));H=15*(L//B)*Pstar
    g=gcd(M,L);d=gcd(M,B*w0);q=M//d;d0=gcd(M,w0)
    assert L%B==0 and d==g and L%d0==0
    residues=sorted({0,1%L,L-1})
    orbit_checks=boundary_checks=0
    for r in residues:
        ys=[(F(B*w0*k,M)+F(B*w0*(15*r+1),15*L*M))%1 for k in range(M//g)]
        counts=Counter(ys)
        assert len(counts)==q and set(counts.values())=={1}
        assert {(y-ys[0])%1 for y in ys}=={F(k,q) for k in range(q)}
        for k,y in enumerate(ys):
            j=(L*k+r)%M
            for w,bi,(Pi,Qi,Ri) in zip(speeds,b,triples):
                actual=F(w*(15*j+1),15*M)%1
                template=((bi//B)*y+F(Ri*(15*r+1),15*Qi))%1
                assert actual==template
                orbit_checks+=1
        for bi,(Pi,Qi,Ri) in zip(b,triples):
            A=bi//B;offset=F(Ri*(15*r+1),15*Qi)
            for k in sorted({0,1,abs(A)-1}):
                for sign in(-1,1):
                    y=F(15*Qi*k+sign*Qi-Ri*(15*r+1),15*(L//B)*Pi)%1
                    assert (y*H).denominator==1
                    assert (A*y+offset)%1 in(F(1,15),F(14,15))
                    boundary_checks+=1
    return {'M':M,'speeds':speeds,'triples':triples,'L':L,'B':B,'P':Pstar,'H':H,
            'g':g,'d':d,'q':q,'d0':d0,'sampled_residues':residues,
            'direct_orbit_coordinate_checks':orbit_checks,'boundary_checks':boundary_checks,
            'old_maximum_bound':15*L*L*Pstar,'stronger_maximum_bound':L*H}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--proof',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    fixtures=[]
    speeds=[13,1,2,3,4,5,6,7]
    fixtures.append(audit_fixture(17,speeds,[(1,1,0)]+[((i+2)*w,(i+2)*13,0) for i,w in enumerate(speeds[1:])]))
    speeds=[6,1,2,3,4,5,7,11]
    fixtures.append(audit_fixture(30,speeds,[(1,1,0)]+[(w,6,0) for w in speeds[1:]]))
    rng=random.Random(15092026)
    for M in (17,23,31,43,61,79,101):
        speeds=rng.sample(range(1,M),8);w0=speeds[0];triples=[(1,1,0)]
        for w in speeds[1:]:
            Q=rng.randrange(1,7);P=(Q*w*pow(w0,-1,M))%M
            if P>M//2:P-=M
            R=(Q*w-P*w0)//M;triples.append((P,Q,R))
        fixtures.append(audit_fixture(M,speeds,triples))
    # q>=H and a positive safe interval, so an actual endpoint must survive.
    M=15013;speeds=[1700*k for k in range(1,9)]
    large=audit_fixture(M,speeds,[(k,1,0) for k in range(1,9)])
    assert large['q']>=large['H']
    safe_j=next(j for j in range(M)
                if all(15*min(w*(15*j+1)%(15*M),(-w*(15*j+1))%(15*M))>=15*M for w in speeds))
    large['direct_safe_anchor_index']=safe_j;fixtures.append(large)
    result={'status':'sketch; exact orbit/boundary regressions support separate algebraic audit',
            'proof_sha256':sha256(a.proof.read_bytes()).hexdigest(),
            'checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
            'fixtures':fixtures,'fixture_count':len(fixtures),
            'orbit_coordinate_checks':sum(x['direct_orbit_coordinate_checks'] for x in fixtures),
            'boundary_checks':sum(x['boundary_checks'] for x in fixtures),
            'all_primitive_orbits_unrepeated':True}
    a.output.write_text(json.dumps(result,indent=2)+'\n')
    print('PASS',len(fixtures),'template fixtures,',result['orbit_coordinate_checks'],'direct coordinate identities')
