"""Independent literal-row replay of the complete sharp ratio table.

Author generators/checkers are not read or imported. Only root's earlier
independent generic integer period arithmetic is imported.
"""
import argparse
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import importlib.util
import json
from math import gcd
from pathlib import Path
import time

CONFIG={2:('two','15-2',Fraction(15,2),2),3:('three','15-4',Fraction(15,4),4),
        4:('four','13-6',Fraction(13,6),7),5:('five','11-6',Fraction(11,6),13),
        6:('six','13-12',Fraction(13,12),24),7:('seven','1-2',Fraction(1,2),91)}


@lru_cache(None)
def literal(h,a):
    assert h>0 and a>0 and gcd(h,a)==1
    bits=0
    for j in range(h):
        z=a*(15*j+1)%(15*h)
        if min(z,15*h-z)<h: bits |= 1<<j
    return bits


def audit(path,q,common):
    _,_,ratio,H=CONFIG[q]
    data=json.loads(path.read_bytes())
    assert data['complete'] is True and data['cover_found'] is None
    assert data['minimum_period_bound']==H and Fraction(data['ratio_bound_strict'])==ratio
    assert data.get('number_rows',6)==q
    assert q<=7 and ratio<=15
    rawH=13*q//(15-2*q)
    if q==6:
        assert H==24 and all(q*((2*h+13)//15)<h for h in (25,26))
    else: assert H==rawH
    # Beyond rawH, q*(2h+13)<15h, so every row density is <1/q.
    assert q*(2*(rawH+1)+13)<15*(rawH+1)

    def rows(h):
        return ((a,literal(h,a)) for a in range(1,(ratio.numerator*h-1)//ratio.denominator+1)
                if gcd(a,h)==1)
    def state(v): return v[0],v[1],v[2],int(v[3],16)
    def child(s,h,a):
        p,r,L,R=s
        assert r>0 and h>=p and a>0 and ratio.denominator*a<ratio.numerator*h and gcd(h,a)==1
        T=L*h//gcd(L,h)
        lifted=common.lift(R,L,T)
        removed=lifted & common.lift(literal(h,a),h,T)
        assert r*removed.bit_count()>=lifted.bit_count()
        D,residual=common.normalize(T,lifted^removed)
        assert residual,('cover found',s,h,a)
        return p,r-1,D,residual
    graph={}
    for node in data['states']:
        s=node['minimum_period'],node['remaining'],node['period'],int(node['missing_hex'],16)
        p,r,L,R=s
        assert 2<=p<=H and 0<=r<q and L>0 and 0<R<1<<L
        assert common.normalize(L,R)==(L,R) and s not in graph
        graph[s]=[(e['row'][0],e['row'][1],state(e['state'])) for e in node['children']]
    expected_roots=set()
    for p in range(2,H+1):
        for a,B in rows(p):
            if not B: continue  # Empty rows cannot belong to a minimal cover.
            L,R=common.normalize(p,((1<<p)-1)^B)
            assert R
            expected_roots.add((p,q-1,L,R))
    roots={state(e['state']) for e in data['roots']}
    assert len(roots)==len(data['roots']) and roots==expected_roots
    for entry in data['roots']:
        h,a=entry['row'];s=state(entry['state'])
        assert h==s[0] and a>0 and gcd(h,a)==1 and ratio.denominator*a<ratio.numerator*h
        B=literal(h,a);assert B
        L,R=common.normalize(h,((1<<h)-1)^B)
        assert s==(h,q-1,L,R)
    total=edges=density_prunes=0
    for s,recorded in graph.items():
        p,r,L,R=s
        expected=set()
        if r:
            for n in common.admissible_growth(r):
                T=L*n;lifted=common.lift(R,L,T)
                for h in common.divisors(T):
                    if h<p or h//gcd(h,L)!=n: continue
                    # Whole-row size bounds its intersection with the residual.
                    # This necessary high-gain test is independent of numerator.
                    if r*((2*h+13)//15)*L<h*R.bit_count():
                        density_prunes+=1
                        continue
                    for a,B in rows(h):
                        removed=lifted & common.lift(B,h,T)
                        if r*removed.bit_count()<lifted.bit_count(): continue
                        D,residual=common.normalize(T,lifted^removed)
                        assert residual,('cover found',s,h,a)
                        expected.add((p,r-1,D,residual));total+=1
        actual={c for _,_,c in recorded}
        assert len(actual)==len(recorded) and expected==actual,('child omission',s,expected-actual,actual-expected)
        for h,a,c in recorded:
            assert c==child(s,h,a)
            if c[1]: assert c in graph
            else: assert not graph.get(c,[])
        edges+=len(recorded)
    seen=set();todo=list(roots)
    while todo:
        s=todo.pop()
        if s in seen: continue
        seen.add(s)
        if s[1]: assert s in graph
        todo.extend(c for _,_,c in graph.get(s,[]))
    assert not set(graph)-seen
    return dict(rows=q,strict_ratio=str(ratio),roots=len(roots),states=len(graph),edges=edges,
                qualifying_physical_rows=total,density_pruned_periods=density_prunes,
                maximum_period=max(s[2] for s in graph),graph_sha256=sha256(path.read_bytes()).hexdigest())


def main():
    p=argparse.ArgumentParser();p.add_argument('--common-checker',type=Path,required=True)
    p.add_argument('--manager-dir',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();spec=importlib.util.spec_from_file_location('root_common',a.common_checker)
    common=importlib.util.module_from_spec(spec);spec.loader.exec_module(common)
    assert literal(1,15)==1 and all(literal(1,k)==0 for k in range(1,15))
    assert not literal(16,1)&(1<<1)
    started=time.monotonic();reports=[]
    for q,(word,label,_,_) in CONFIG.items():
        result=audit(a.manager_dir/f'upper-anchor-{word}-ratio-{label}.graph.json',q,common)
        reports.append(result);print(json.dumps(result),flush=True)
    fixtures=json.loads((a.manager_dir/'sharp-cover-ratio-fixtures.json').read_text())
    assert len(fixtures['examples'])==7
    for ex in fixtures['examples']:
        q,M,ws=ex['rows'],ex['anchor'],ex['killers']
        assert len(ws)==len(set(ws))==q and all(w>0 for w in ws)
        expected=Fraction(15) if q==1 else CONFIG[q][2]
        assert Fraction(max(ws),M)==Fraction(ex['largest_ratio'])==expected
        masks={w:{j for j in range(M) if min(w*(15*j+1)%(15*M),15*M-w*(15*j+1)%(15*M))<M} for w in ws}
        assert set().union(*masks.values())==set(range(M))
        for w in ws:
            private=masks[w]-set().union(*(masks[v] for v in ws if v!=w))
            assert private and ex['private_indices'][str(w)] in private
    report=dict(status='PASS; same-family audit, sketch pending Claude/human review',
                elapsed_seconds=time.monotonic()-started,graphs=reports,sharp_examples=7,
                checker_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                common_checker_sha256=sha256(a.common_checker.read_bytes()).hexdigest())
    a.output.write_text(json.dumps(report,indent=2)+'\n')
    print('All six exclusion DAGs and seven sharp examples passed.',flush=True)


if __name__=='__main__': main()
