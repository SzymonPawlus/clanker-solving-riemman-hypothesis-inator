"""Exact standalone author replay of the 160 explicit nine-speed measures."""
from fractions import Fraction as F
from math import gcd,lcm
from pathlib import Path
import hashlib,json

HERE=Path(__file__).parent


def check(case):
    P=case['pattern']; assert len(P)==9 and P==sorted(set(P))
    assert all(type(v)==int and v>0 for v in P)
    assert gcd(*P)==1
    M=max(P)
    masks=[{j for j in range(M) if min(v*(15*j+1)%(15*M),
           (-v*(15*j+1))%(15*M))<M} for v in P[:-1]]
    assert set.union(*masks)==set(range(M))
    assert all(C-set.union(*(masks[:i]+masks[i+1:])) for i,C in enumerate(masks))
    atoms=[(F(x),F(w)) for x,w in case['atoms']]
    assert len(atoms)==len(set(x for x,w in atoms))
    assert all(0<=x<1 and w>0 for x,w in atoms)
    assert all(15*min(v*x.numerator%x.denominator,
                     (-v*x.numerator)%x.denominator)>=x.denominator
               for x,w in atoms for v in P)
    D=lcm(*(w.denominator for x,w in atoms))
    atomints=[(x.numerator,x.denominator,int(w*D)) for x,w in atoms]
    T=sum(w for x,y,w in atomints)
    assert F(T,D)==F(case['total']) and 5*D<T and 10*T<=51*D
    columns=0;worst=(F(0),0,0)
    for n in range(1,15):
        for q in range(1,M*n):
            if gcd(n,q)!=1 or(n==1 and q in P):continue
            hit=0
            for x,y,w in atomints:
                phase=q*x%y
                count=-((15*phase-n*y)//(15*y))-((-n*y-15*phase)//(15*y))-1
                assert 0<=count<=n
                hit+=w*count
            assert hit<=D*n,(P,n,q,hit,D*n)
            worst=max(worst,(F(hit,D*n),n,q));columns+=1
    assert str(worst[0])==case['maximum_load'] and columns==case['columns']
    return {'pattern':P,'total':str(F(T,D)),'atoms':len(atoms),
            'columns':columns,'maximum_load':str(worst[0]),'maximum_pair':list(worst[1:])}


if __name__=='__main__':
    assert 51*(2*15+14)<=150*15
    path=HERE/'eight-core-phase-to30.json'; data=json.loads(path.read_text())
    assert len(data['cases'])==160
    assert len({tuple(c['pattern']) for c in data['cases']})==160
    rows=[check(c) for c in data['cases']]
    out={'status':'sketch; standalone exact author replay passed',
         'manifest_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
         'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'cases':rows,'total_columns':sum(c['columns'] for c in rows),
         'total_atoms':sum(c['atoms'] for c in rows),
         'least_mass':str(min(F(c['total']) for c in rows)),
         'greatest_load':str(max(F(c['maximum_load']) for c in rows))}
    (HERE/'eight-core-phase-to30-author-audit.json').write_text(json.dumps(out,indent=2)+'\n')
    print({k:v for k,v in out.items() if k!='cases'})
