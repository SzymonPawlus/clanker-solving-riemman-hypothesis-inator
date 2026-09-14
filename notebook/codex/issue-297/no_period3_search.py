"""Exploratory exact state search: period 2 present, period 3 absent.

Quantifiers: endpoint-cover obstruction, not an LRC witness theorem.
Boundary: direct strict danger mask; endpoint equality is excluded.
Scaling: only reduced (h,a) data and periodic lifts; no coordinatewise scaling.
Dimension: fourteen moving velocities, fifteen total, threshold 1/15.
Any resource-limited run is incomplete numerical evidence.
"""
from functools import lru_cache
from math import gcd,lcm
from pathlib import Path
import argparse,json,time,hashlib
from fractions import Fraction

E={p:tuple(n for n in range(1,29) if p*((2*n+14)//15)>=n) for p in range(1,7)}
@lru_cache(None)
def divisors(n):
    out=[]
    for d in range(1,__import__('math').isqrt(n)+1):
        if n%d==0:
            out.append(d)
            if d*d!=n:out.append(n//d)
    return tuple(sorted(out))
@lru_cache(2000)
def rows(h):
    out={}
    for a in range(1,h):
        if gcd(a,h)!=1:continue
        lo=-((h-1+a)//15);hi=(h-1-a)//15
        inv=pow(a,-1,h)
        mask=sum(1<<((inv*k)%h) for k in range(lo,hi+1))
        if mask:out.setdefault(mask,a)
    return tuple((a,mask) for mask,a in out.items())
def repeat(mask,h,M):
    return mask*((1<<M)-1)//((1<<h)-1)
def reduce_state(L,R):
    for d in divisors(L):
        low=R&((1<<d)-1)
        if repeat(low,d,L)==R:return d,low
    raise AssertionError

def search(seconds=120,limit=1000000,out=None):
    started=time.monotonic();nodes=0;largest=0;memo={};width={};stop=False;graph={}
    failures={};witness=None
    def recurse(p,L,R,path):
        nonlocal nodes,largest,stop,witness
        if not R:witness=path;return True
        if p==0:return False
        key=(p,L,R)
        if key in memo:return memo[key]
        nodes+=1;largest=max(largest,L);width[p]=width.get(p,0)+1
        if nodes%1000==0:
            print(json.dumps({'nodes':nodes,'largest_period':largest,'width':width,'seconds':round(time.monotonic()-started,2)}),flush=True)
        if nodes>limit or time.monotonic()-started>seconds:stop=True;raise TimeoutError
        need=R.bit_count();candidates=[]
        hs=sorted({h for n in E[p] for h in divisors(L*n) if h>1 and h!=3 and h//gcd(h,L)==n})
        for h in hs:
            n=h//gcd(h,L);M=L*n;liftR=repeat(R,L,M)
            for a,B in rows(h):
                liftB=repeat(B,h,M);gain=(liftR&liftB).bit_count()
                if p*gain<need*n:continue
                nxt=reduce_state(M,liftR&~liftB)
                candidates.append((nxt,(h,a),Fraction(gain,need*n)))
        # Sorting affects discovery order only; every high-gain row is retained.
        candidates.sort(key=lambda v:(-v[2],v[0][0],v[1]))
        seen=set();edges=[]
        graph[key]={'remaining':p,'period':L,'missing_hex':hex(R),'candidate_rows':len(candidates),'edges':edges}
        for (newL,newR),(h,a),gain in candidates:
            nxtkey=(newL,newR)
            if nxtkey in seen:continue
            seen.add(nxtkey)
            edges.append({'period':h,'numerator':a,'next':[p-1,newL,hex(newR)]})
            if recurse(p-1,newL,newR,path+[(h,a)]):memo[key]=True;return True
        memo[key]=False
        return False
    try:answer=recurse(6,2,2,[(2,1)])
    except TimeoutError:answer=None
    result={'scope':'seven-row covers with physical reduced period 2 present and period 3 absent','complete':not stop,'cover_found':answer,'witness':witness,'nodes':nodes,'largest_period':largest,'width':width,'seconds':time.monotonic()-started,'memoized':len(memo)}
    if out:
        report_path=Path(out)
        graph_path=report_path.with_suffix('.graph.json')
        graph_path.write_text(json.dumps({'root':[6,2,'0x2'],'states':list(graph.values())},sort_keys=True,separators=(',',':'))+'\n')
        result['graph_file']=graph_path.name
        result['graph_sha256']=hashlib.sha256(graph_path.read_bytes()).hexdigest()
        result['code_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        result['edges']=sum(len(v['edges']) for v in graph.values())
        report_path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result),flush=True)
    return result
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--seconds',type=int,default=120);ap.add_argument('--limit',type=int,default=1000000);ap.add_argument('--out');ns=ap.parse_args()
    # Boundary fixture: (h,a,j)=(16,1,1) has exact distance 1/15.
    assert min(16,15*16-16)==16
    assert 1 in dict(rows(16)) and not (dict(rows(16))[1]&2)
    # Centered K implementation agrees with direct strict modular semantics.
    for h in range(2,80):
      for a,B in rows(h):
        direct=sum(1<<j for j in range(h) if min(a*(15*j+1)%(15*h),15*h-a*(15*j+1)%(15*h))<h)
        assert B==direct,(h,a)
    search(ns.seconds,ns.limit,ns.out)
