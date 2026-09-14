"""Independent sharp 13/12 replay, from prose and JSON only.

Uses only the earlier independent checker's generic period arithmetic.
The unrestricted numerator range is independently generated here.
"""
import argparse
from functools import lru_cache
from hashlib import sha256
import importlib.util
import json
from math import gcd
from pathlib import Path


def literal(h, a):
    assert h > 0 and a > 0 and gcd(h, a) == 1
    B = 0
    for j in range(h):
        z = a * (15*j + 1) % (15*h)
        if min(z, 15*h-z) < h:
            B |= 1 << j
    return B


@lru_cache(None)
def allowed(h):
    return tuple((a, literal(h, a)) for a in range(1, (13*h-1)//12 + 1)
                 if gcd(a, h) == 1)


def audit(path, common):
    data = json.loads(path.read_bytes())
    assert data['complete'] is True and data['cover_found'] is None
    assert data['minimum_period_bound'] == 24
    assert data['ratio_bound_strict'] == '13/12'
    assert literal(1, 1) == 0
    assert literal(1, 15) == 1
    assert all(a != 13 for a, _ in allowed(12)), 'strict ratio tie is excluded'
    assert not (literal(16, 1) & (1 << 1)), 'distance tie is safe'
    assert all(6*((2*h+13)//15) < h for h in (25, 26))
    # For h>=27, 6(2h+13)<15h, since 78<3h.
    assert 78 < 3*27

    def state(values):
        return values[0], values[1], values[2], int(values[3], 16)

    graph = {}
    for node in data['states']:
        s = node['minimum_period'], node['remaining'], node['period'], int(node['missing_hex'], 16)
        p, r, L, R = s
        assert 2 <= p <= 24 and 0 <= r <= 5 and L > 0 and 0 < R < 1 << L
        assert common.normalize(L, R) == (L, R)
        assert s not in graph
        graph[s] = [(e['row'][0], e['row'][1], state(e['state'])) for e in node['children']]

    expected_roots = set()
    for p in range(2, 25):
        for a, B in allowed(p):
            L, R = common.normalize(p, ((1 << p)-1) ^ B)
            assert R
            expected_roots.add((p, 5, L, R))
    roots = {state(root['state']) for root in data['roots']}
    assert len(roots) == len(data['roots'])
    assert expected_roots == roots, ('root coverage', expected_roots-roots, roots-expected_roots)
    for root in data['roots']:
        h, a = root['row']
        s = state(root['state'])
        assert h == s[0] and 12*a < 13*h and gcd(a,h) == 1
        L, R = common.normalize(h, ((1 << h)-1)^literal(h,a))
        assert s == (h, 5, L, R)

    total_rows = edge_count = 0
    for s, recorded in graph.items():
        p, r, L, R = s
        expected = set()
        if r:
            for n in common.admissible_growth(r):
                T = L*n
                lifted = common.lift(R, L, T)
                for h in common.divisors(T):
                    if h < p or h//gcd(h,L) != n:
                        continue
                    for a, B in allowed(h):
                        removed = lifted & common.lift(B,h,T)
                        if r*removed.bit_count() >= lifted.bit_count():
                            D, residual = common.normalize(T,lifted^removed)
                            assert residual, ('cover',s,h,a)
                            expected.add((p,r-1,D,residual))
                            total_rows += 1
        actual = {c for _,_,c in recorded}
        assert len(actual) == len(recorded)
        assert expected == actual, ('child coverage',s,expected-actual,actual-expected)
        for h,a,c in recorded:
            assert h >= p and a > 0 and 12*a < 13*h and gcd(h,a) == 1
            T = L*h//gcd(L,h)
            lifted = common.lift(R,L,T)
            removed = lifted & common.lift(literal(h,a),h,T)
            assert r*removed.bit_count() >= lifted.bit_count()
            D,residual = common.normalize(T,lifted^removed)
            assert c == (p,r-1,D,residual) and residual
            if c[1]:
                assert c in graph
            else:
                assert not graph.get(c,[])
        edge_count += len(recorded)
    seen, todo = set(), list(roots)
    while todo:
        s = todo.pop()
        if s in seen:
            continue
        seen.add(s)
        if s[1]:
            assert s in graph
        todo.extend(c for _,_,c in graph.get(s,[]))
    assert not (set(graph)-seen)
    sharp = [4,5,6,7,11,13]
    private = {}
    for w in sharp:
        others = [v for v in sharp if v != w]
        private[w] = [j for j in range(12)
                      if min(w*(15*j+1)%180,180-w*(15*j+1)%180)<12
                      and all(min(v*(15*j+1)%180,180-v*(15*j+1)%180)>=12 for v in others)]
        assert private[w]
    for j in range(12):
        assert any(min(w*(15*j+1)%180,180-w*(15*j+1)%180)<12 for w in sharp)
    return dict(status='PASS; same-family audit, sketch pending Claude/human review',
                graph_sha256=sha256(path.read_bytes()).hexdigest(),
                roots=len(roots),states=len(graph),edges=edge_count,
                qualifying_physical_rows=total_rows,
                maximum_residual_period=max(s[2] for s in graph),
                sharp_example=dict(anchor=12,killers=sharp,private_indices=private))


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--common-checker',type=Path,required=True)
    p.add_argument('--graph',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a = p.parse_args()
    spec=importlib.util.spec_from_file_location('independent_common',a.common_checker)
    common=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(common)
    result = audit(a.graph,common)
    result['checker_sha256']=sha256(Path(__file__).read_bytes()).hexdigest()
    result['common_checker_sha256']=sha256(a.common_checker.read_bytes()).hexdigest()
    a.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
