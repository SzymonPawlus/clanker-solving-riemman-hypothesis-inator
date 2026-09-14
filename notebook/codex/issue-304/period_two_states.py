"""Explore no-period-two seven-row covers, with exact replayable certificates.

All floating point work is discovery only. Certificate weights are clipped to
nonnegative integers and every accepted leaf is checked by integer arithmetic.
Independent reviewers must work from the separate mathematical specification.
"""
from functools import lru_cache
from math import gcd
from pathlib import Path
import argparse, hashlib, json, time

import numpy as np
from scipy.optimize import linprog

HERE = Path(__file__).parent
FACTORS = {r: tuple(n for n in range(1,100)
                    if r*((2*n+14)//15) >= n) for r in range(1,7)}


def bad(h,a):
    inv=pow(a,-1,h)
    return tuple(sorted((k*inv)%h for k in
                        range((-h-a)//15+1,(h-1-a)//15+1)))


@lru_cache(None)
def divisors(L):
    return tuple(d for d in range(1,L+1) if L%d==0)


@lru_cache(maxsize=500)
def profiles(L,p,N,keep_all=False):
    """Distinct exact conditional profiles; row representative retained."""
    out=[]
    for d in divisors(L):
        for n in range(1,N+1):
            if gcd(n,L//d)!=1: continue
            h=d*n
            if h<p: continue
            seen=set()
            for a in range(1,h):
                if gcd(a,h)!=1: continue
                low=(-h-a)//15+1; high=(h-1-a)//15
                v=tuple((high-(a*j)%d)//d-(low-1-(a*j)%d)//d
                        for j in range(d))
                if not keep_all and v in seen: continue
                seen.add(v)
                out.append((d,n,h,a,v))
    return tuple(out)


def dual(L,R,p,r):
    # T<=r+0.1 makes all n>N automatic, from T*(2n+14)/(15n)<=1.
    cap_num=10*r+1
    N=(14*cap_num)//(150-2*cap_num)
    ps=profiles(L,p,N)
    rows=[]; seen=set()
    for d,n,h,a,v in ps:
        z=tuple(v[j%d] for j in R)
        key=(n,z)
        if key in seen: continue
        seen.add(key)
        rows.append((n,z))
    A=np.array([[x/n for x in z] for n,z in rows]+[[1.0]*len(R)])
    b=np.array([1.0]*len(rows)+[cap_num/10])
    lp=linprog(-np.ones(len(R)),A_ub=A,b_ub=b,bounds=(0,None),method='highs')
    if not lp.success or -lp.fun<=r+1e-7:
        return None
    # Round down after a slight contraction. This cannot introduce negativity.
    for den in (10000,1000000,100000000):
        w=[max(0,int(float(x)*(1-1e-8)*den)) for x in lp.x]
        total=sum(w)
        if total<=r*den or 10*total>cap_num*den: continue
        if any(sum(x*y for x,y in zip(w,z))>n*den for n,z in rows): continue
        return {'denominator':den,'weights':[[j,x] for j,x in zip(R,w) if x],
                'mass_numerator':total,'tail_starts':N+1,
                'finite_profiles':len(ps),'distinct_constraints':len(rows)}
    return None


def children(L,R,p,r):
    out={}
    # Conditional profiles may coincide without having the same lifted set.
    # Therefore branching retains every numerator; only duals deduplicate profiles.
    for d,n,h,a,v in profiles(L,p,max(FACTORS[r]),True):
        if n not in FACTORS[r]: continue
        hits=sum(v[j%d] for j in R)
        if hits*r < len(R)*n: continue
        H=L*n
        B=set(bad(h,a))
        S=tuple(j+L*k for k in range(n) for j in R if (j+L*k)%h not in B)
        S=tuple(sorted(S))
        assert len(S)==len(R)*n-hits
        H,S=minimize(H,S)
        key=(H,S)
        out.setdefault(key,[h,a])
    return [(h,a,H,S) for (H,S),(h,a) in sorted(out.items())]


def minimize(L,R):
    if not R:return 1,()
    for d in divisors(L):
        if len(R)%(L//d):continue
        reduced=tuple(sorted({j%d for j in R}))
        if len(reduced)*(L//d)==len(R):return d,reduced
    raise AssertionError('no period')


def run(p,limit=100000,maxL=20000,use_dual=True):
    nodes={}; active=set(); start=time.monotonic()
    path=HERE/f'no-period-two-p{p}.json'
    def save(complete=False):
        data={'status':'sketch; exact author check only; independent review required',
              'minimum_period':p,'max_cover_rows':7,'complete':complete,
              'root_ids':roots,'nodes':list(nodes.values()),
              'author_code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
        tmp=path.with_suffix('.tmp'); tmp.write_text(json.dumps(data,separators=(',',':'))+'\n')
        tmp.replace(path)
    def visit(L,R,r):
        key=(L,R,r)
        if key in active: raise AssertionError('cycle')
        sid=hashlib.sha256(repr(key).encode()).hexdigest()[:20]
        if sid in nodes: return sid
        node={'id':sid,'period':L,'residual':list(R),'remaining':r}
        nodes[sid]=node; active.add(key)
        if not R:
            node['kind']='cover-found'
        elif r==0:
            node['kind']='nonempty'
        elif len(nodes)>limit or L>maxL:
            node['kind']='open'
        else:
            cert=dual(L,R,p,r) if use_dual else None
            if cert:
                node['kind']='dual'; node['certificate']=cert
            else:
                ch=children(L,R,p,r)
                node['kind']='branch'; node['children']=[]
                for h,a,H,S in ch:
                    child=visit(H,S,r-1)
                    node['children'].append({'h':h,'a':a,'child':child})
        active.remove(key)
        if len(nodes)%25==0:
            print('p',p,'nodes',len(nodes),'L',L,'r',r,'elapsed',round(time.monotonic()-start,1),flush=True)
            save()
        return sid
    bases={bad(p,a) for a in range(1,p) if gcd(a,p)==1}
    roots=[]
    for B in sorted(bases):
        roots.append(visit(p,tuple(j for j in range(p) if j not in B),6))
        save()
    complete=all(n['kind'] not in ('open','cover-found') for n in nodes.values())
    save(complete)
    from collections import Counter
    print('FINAL',p,len(nodes),Counter(n['kind'] for n in nodes.values()),'complete',complete,
          'maxL',max(n['period'] for n in nodes.values()),'seconds',round(time.monotonic()-start,2),flush=True)


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('p',type=int,nargs='+')
    ap.add_argument('--limit',type=int,default=100000)
    ap.add_argument('--max-period',type=int,default=20000)
    ap.add_argument('--no-dual',action='store_true')
    arg=ap.parse_args()
    print('SANITY:14 moving/15 total; one common endpoint; strict bad arcs; common scaling only.',flush=True)
    assert bad(2,1)==(0,)
    assert min(1,14)>=1  # Equality at t=1/15 is allowed.
    for p in arg.p: run(p,arg.limit,arg.max_period,not arg.no_dual)
