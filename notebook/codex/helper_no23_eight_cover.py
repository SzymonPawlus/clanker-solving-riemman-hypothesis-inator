"""Independent bounded exact decision search, both periods 2 and 3 absent.

Branches on a least-supported uncovered endpoint. A minimal completing family
must include one of its rows. Siblings remove only earlier candidates for that
same pivot, so each family is retained in its first applicable branch.
"""
import argparse
from hashlib import sha256
from math import gcd
from pathlib import Path
import json
from time import monotonic


def literal_mask(M,w):
    return sum(1<<j for j in range(M)
               if min(w*(15*j+1)%(15*M),(-w*(15*j+1))%(15*M))<M)


def decide(M,slots=8,forbidden=(2,3),seconds=5):
    started=monotonic();full=(1<<M)-1
    # Equal masks are interchangeable for existence; a found set is normalized
    # afterward and independently rechecked. No primitive classification is used.
    bymask={}
    for w in range(1,M):
        if M//gcd(M,w) not in forbidden:
            bymask.setdefault(literal_mask(M,w),w)
    bymask.pop(0,None)
    columns=sorted(((w,b) for b,w in bymask.items()))
    supports=[sum(1<<i for i,(w,b) in enumerate(columns) if b>>j&1) for j in range(M)]
    nodes=0;gain_prunes=0;private_prunes=0;unsupported_prunes=0

    def walk(missing,available,chosen,private):
        nonlocal nodes,gain_prunes,private_prunes,unsupported_prunes
        nodes+=1
        if nodes%256==0 and monotonic()-started>seconds:raise TimeoutError
        if not missing:return chosen
        r=slots-len(chosen)
        if not r:return None
        filtered=available;gains=[]
        bits=available
        while bits:
            bit=bits&-bits;bits-=bit;i=bit.bit_length()-1
            w,b=columns[i];gain=(b&missing).bit_count()
            if not gain or any(old&~b==0 for old in private):
                filtered&=~bit;private_prunes+=1
            else:gains.append(gain)
        if sum(sorted(gains,reverse=True)[:r])<missing.bit_count():
            gain_prunes+=1;return None
        pivot_options=None;pivot_size=len(columns)+1
        bits=missing
        while bits:
            bit=bits&-bits;bits-=bit;j=bit.bit_length()-1
            options=supports[j]&filtered;count=options.bit_count()
            if not count:
                unsupported_prunes+=1;return None
            if count<pivot_size:pivot_size=count;pivot_options=options
        options=[];bits=pivot_options
        while bits:
            bit=bits&-bits;bits-=bit;i=bit.bit_length()-1
            options.append(((columns[i][1]&missing).bit_count(),i))
        # Larger gain first affects time only, not accepted candidates.
        for gain,i in sorted(options,reverse=True):
            bit=1<<i;filtered&=~bit;w,b=columns[i]
            ans=walk(missing&~b,filtered,chosen+(i,),
                     tuple(old&~b for old in private)+(b&missing,))
            if ans is not None:return ans
        return None

    complete=True;answer=None
    try:answer=walk(full,(1<<len(columns))-1,(),())
    except TimeoutError:complete=False
    result={'M':M,'max_rows':slots,'forbidden_reduced_periods':list(forbidden),
            'complete':complete,'elapsed_seconds':monotonic()-started,
            'nodes':nodes,'distinct_nonempty_masks':len(columns),
            'gain_prunes':gain_prunes,'private_prunes':private_prunes,
            'unsupported_prunes':unsupported_prunes,'cover':None}
    if answer is not None:
        speeds=tuple(sorted(columns[i][0] for i in answer))+(M,)
        g=gcd(*speeds);P=tuple(w//g for w in speeds);N=P[-1]
        masks=[literal_mask(N,w) for w in P[:-1]]
        assert gcd(*P)==1 and len(P)<=slots+1
        assert all(N//gcd(N,w) not in forbidden for w in P[:-1])
        assert all(any(b>>j&1 for b in masks) for j in range(N))
        private={}
        for i,w in enumerate(P[:-1]):
            others=0
            for j,b in enumerate(masks):
                if i!=j:others|=b
            residues=[j for j in range(N) if masks[i]>>j&1 and not(others>>j&1)]
            assert residues
            private[w]=residues
        result['cover']={'physical_speeds':speeds,'primitive_speeds':P,
                         'common_gcd':g,'private_residues':private,
                         'reduced_periods':[N//gcd(N,w) for w in P[:-1]]}
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--first',type=int,default=31)
    p.add_argument('--last',type=int,default=120)
    p.add_argument('--seconds',type=float,default=5)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();assert 9<=a.first<=a.last<=1000 and a.seconds>0
    # Small known positive families validate both the coverage and private tests.
    fixtures=[decide(18,7,(),5),decide(20,8,(),5)]
    assert all(d['complete'] and d['cover'] for d in fixtures)
    assert len(fixtures[0]['cover']['primitive_speeds'])==8
    assert len(fixtures[1]['cover']['primitive_speeds'])==9
    result={'status':'numerical; exact bounded decision search only',
            'moving_velocities':14,'total_runners':15,'threshold':'1/15',
            'max_rows':8,'forbidden_reduced_periods':[2,3],
            'range':[a.first,a.last],'seconds_cap_per_anchor':a.seconds,
            'checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
            'positive_fixtures':fixtures,'anchors':[]}
    for M in range(a.first,a.last+1):
        rec=decide(M,8,(2,3),a.seconds)
        result['anchors'].append(rec)
        a.output.write_text(json.dumps(result,indent=2)+'\n')
        print(M,'complete',rec['complete'],'nodes',rec['nodes'],'cover',bool(rec['cover']),flush=True)
        if rec['cover']:break
    result['completed_anchors']=sum(r['complete'] for r in result['anchors'])
    result['incomplete_anchors']=[r['M'] for r in result['anchors'] if not r['complete']]
    result['covers_found']=sum(r['cover'] is not None for r in result['anchors'])
    a.output.write_text(json.dumps(result,indent=2)+'\n')
