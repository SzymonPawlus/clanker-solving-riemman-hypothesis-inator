"""Exact bounded residual-graph exploration for an eight-row minimum period.

An open leaf prevents any exclusion claim. Positive covers are reconstructed
as primitive physical tuples and directly checked. Separate from frozen graphs.
"""
from functools import lru_cache
from collections import Counter
from math import gcd,lcm
from pathlib import Path
import argparse,hashlib,json,time

HERE=Path(__file__).parent
E={r:tuple(n for n in range(1,100) if r*((2*n+14)//15)>=n) for r in range(1,8)}

@lru_cache(None)
def divisors(L):return tuple(d for d in range(1,L+1) if L%d==0)

def bad(h,a):
    inv=pow(a,-1,h)
    return tuple(sorted(k*inv%h for k in range((-h-a)//15+1,(h-1-a)//15+1)))

def minimize(L,R):
    if not R:return 1,()
    for d in divisors(L):
        if len(R)%(L//d):continue
        s=tuple(sorted({x%d for x in R}))
        if len(s)*(L//d)==len(R):return d,s

def children(L,R,p,r):
    found={}
    for d in divisors(L):
        counts=Counter(j%d for j in R)
        for n in E[r]:
            if gcd(n,L//d)!=1:continue
            h=d*n
            if h<p:continue
            for a in range(1,h):
                if gcd(a,h)!=1:continue
                lo=(-h-a)//15+1;hi=(h-1-a)//15
                B=None
                if hi-lo+1<len(counts):
                    B=set(bad(h,a));hits=sum(counts[j%d] for j in B)
                else:
                    hits=sum(c*((hi-a*j%d)//d-(lo-1-a*j%d)//d) for j,c in counts.items())
                if r*hits<len(R)*n:continue
                if B is None:B=set(bad(h,a))
                S=tuple(sorted(j+k*L for k in range(n) for j in R if(j+k*L)%h not in B))
                assert len(S)==len(R)*n-hits
                key=minimize(L*n,S)
                found.setdefault(key,(h,a))
    return [(h,a,H,S) for(H,S),(h,a) in sorted(found.items())]

def run(p,max_nodes,max_period,max_seconds,resume=False):
    start=time.monotonic();nodes={};roots=[];cover=None
    path=HERE/f'eight-period-p{p}.json'
    if resume and path.exists():
        old=json.loads(path.read_text());inventory={n['id']:n for n in old['nodes']}
        @lru_cache(None)
        def closed(sid):
            node=inventory[sid]
            return node['kind']=='nonempty' or(node['kind']=='branch' and all(closed(e['child']) for e in node['children']))
        nodes={sid:node for sid,node in inventory.items() if closed(sid)}
        print('REUSED',len(nodes),'closed nodes',flush=True)
    def save():
        data={'status':'bounded exact exploration; no conclusion if open nodes',
              'minimum_period':p,'roots':roots,'nodes':list(nodes.values()),'cover':cover}
        path.write_text(json.dumps(data,separators=(',',':'))+'\n')
    def visit(L,R,r,chosen):
        nonlocal cover
        key=(L,R,r);sid=hashlib.sha256(repr(key).encode()).hexdigest()[:20]
        if sid in nodes:return sid
        node={'id':sid,'period':L,'residual':R,'remaining':r};nodes[sid]=node
        if not R:
            node['kind']='cover';M=lcm(*(h for h,a in chosen));P=sorted({a*(M//h) for h,a in chosen})+[M]
            assert len(P)<=9 and gcd(*P)==1
            masks=[{j for j in range(M) if min(w*(15*j+1)%(15*M),(-w*(15*j+1))%(15*M))<M} for w in P[:-1]]
            assert set.union(*masks)==set(range(M))
            cover={'pattern':P,'rows':chosen,'private':{str(w):sorted(masks[i]-set.union(*(masks[:i]+masks[i+1:])))[:5] for i,w in enumerate(P[:-1])}}
        elif r==0:node['kind']='nonempty'
        elif len(nodes)>max_nodes or L>max_period or time.monotonic()-start>max_seconds:
            node['kind']='open'
        else:
            node['kind']='branch';node['children']=[]
            for h,a,H,S in children(L,R,p,r):
                cid=visit(H,S,r-1,chosen+[(h,a)]);node['children'].append({'h':h,'a':a,'child':cid})
                if cover:break
        if len(nodes)%100==0:
            print(p,'nodes',len(nodes),'L',L,'r',r,'seconds',round(time.monotonic()-start,1),flush=True)
            save()
        return sid
    seen=set()
    for a in range(1,p):
        if gcd(a,p)!=1:continue
        B=bad(p,a)
        if B in seen:continue
        seen.add(B);roots.append(visit(p,tuple(j for j in range(p) if j not in B),7,[(p,a)]))
        if cover:break
    save()
    print('FINAL',p,len(nodes),dict(Counter(n['kind'] for n in nodes.values())),cover,
          'seconds',round(time.monotonic()-start,1),flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('p',type=int,nargs='+')
    ap.add_argument('--max-nodes',type=int,default=50000);ap.add_argument('--max-period',type=int,default=20000)
    ap.add_argument('--seconds',type=float,default=300);ap.add_argument('--resume',action='store_true')
    ar=ap.parse_args()
    for p in ar.p:run(p,ar.max_nodes,ar.max_period,ar.seconds,ar.resume)
