"""Independent generic rational-atom signed-score witness extraction."""
from fractions import Fraction as F
from pathlib import Path
from random import Random
from time import perf_counter
from hashlib import sha256
import argparse,json
from helper_witness_extract import floor_sum


def bad_count(x,c,w,L,R):
    N=R-L
    D=c*x.denominator
    a=w*x.denominator
    b=w*(x.denominator*L+x.numerator)
    K=(D+14)//15
    # Exactly residues [0,K) or [D-K+1,D) satisfy15*min(residue,-residue)<D.
    return N+floor_sum(N,a,b-(D-K+1),D)-floor_sum(N,a,b-K,D)


def literal(x,c,w,L,R):
    D=c*x.denominator
    return sum(15*min(v,D-v)<D for j in range(L,R)
               for v in [w*(x.denominator*j+x.numerator)%D])


def score(x,c,extras,L,R):
    return R-L-sum(bad_count(x,c,w,L,R) for w in extras)


def extract(P,atoms,c,extras):
    assert c>0 and len(extras)<=6 and all(0<abs(w)<=max(P)*c for w in extras)
    extras=tuple(abs(w) for w in extras)
    for x in atoms:
        value=score(x,c,extras,0,c)
        if value>0:break
    else:raise AssertionError(('no positive fiber',P,c,extras))
    L,R=0,c
    steps=0
    while R-L>1:
        mid=(L+R)//2
        left=score(x,c,extras,L,mid)
        if left>0:R,value=mid,left
        else:L,value=mid,value-left
        assert value>0
        steps+=1
    assert value==1
    t=(L+x)/c
    margins=[15*min(v*t.numerator%t.denominator,(-v*t.numerator)%t.denominator)-t.denominator
             for v in [c*u for u in P]+list(extras)]
    assert min(margins)>=0
    return {'atom':str(x),'lift_index':L,'time':str(t),'bisections':steps,
            'minimum_scaled_margin':min(margins)}


def fixture_audit():
    rng=Random(301987)
    for x,expected in [(F(1,15),0),(F(14,15),0),(F(1,16),1),(F(15,16),1)]:
        assert bad_count(x,1,1,0,1)==expected
    for _ in range(50000):
        den=rng.randrange(1,300)
        x=F(rng.randrange(den),den)
        c=rng.randrange(1,201)
        w=rng.randrange(-30*c,30*c+1)
        L=rng.randrange(c+1)
        R=rng.randrange(L,c+1)
        assert bad_count(x,c,w,L,R)==literal(x,c,w,L,R),(x,c,w,L,R)
    return 50004


def load(path):
    data=json.loads(Path(path).read_text())
    P=data['pattern']
    if 'atoms' in data:atoms=[F(x) for x,z in data['atoms'] if F(z)>0]
    else:atoms=[F(15*r+1,15*u) for (u,r),z in zip(data['types'],data['weights']) if F(z)>0]
    assert all(literal(x,1,u,0,1)==0 for x in atoms for u in P)
    return P,atoms


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('certificates',nargs='+')
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    out={'direct_fixture_cases':fixture_audit(),'witnesses':[],
         'checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
         'floor_sum_module_sha256':sha256(Path(__file__).with_name('helper_witness_extract.py').read_bytes()).hexdigest()}
    rng=Random(3030301)
    for path in args.certificates:
        P,atoms=load(path)
        for c in (37,10**100+267):
            extras=[rng.randrange(1,max(P)*c+1) for _ in range(6)]
            start=perf_counter()
            record={'source':Path(path).name,'P':P,'c':c,'extras':extras,
                    **extract(P,atoms,c,extras)}
            record['elapsed_seconds']=perf_counter()-start
            out['witnesses'].append(record)
            print(record['source'],'scale_digits',len(str(c)),
                  'bisections',record['bisections'],'seconds',record['elapsed_seconds'],flush=True)
    Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
