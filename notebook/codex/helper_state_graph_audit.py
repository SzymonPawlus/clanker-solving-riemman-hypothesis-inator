#!/usr/bin/env python3
"""Independent complete replay from the two mathematical specifications.

No author generator or checker is imported or read. Python integers implement
literal strict residues; graph labels and author candidate counts are untrusted.
"""
import argparse
from functools import lru_cache
from hashlib import sha256
import json
from math import gcd, isqrt
from pathlib import Path
import time


@lru_cache(None)
def divisors(n):
    ds = set()
    for d in range(1, isqrt(n) + 1):
        if n % d == 0:
            ds.update((d, n // d))
    return tuple(sorted(ds))


def literal_row(h, a):
    assert 0 < a < h and gcd(h, a) == 1
    out = 0
    for j in range(h):
        s = (a * (15 * j + 1)) % (15 * h)
        if min(s, 15 * h - s) < h:
            out |= 1 << j
    return out


@lru_cache(None)
def rows(h):
    # Retain all physical unit numerators, including those divisible by 3 or 5.
    return tuple((a, literal_row(h, a)) for a in range(1, h) if gcd(a, h) == 1)


def lift(mask, period, target):
    assert target % period == 0
    return mask * (((1 << target) - 1) // ((1 << period) - 1))


def normalize(period, mask):
    assert 0 <= mask < 1 << period
    if not mask:
        return (1, 0)
    count = mask.bit_count()
    for d in divisors(period):
        if count % (period // d):
            continue
        low = mask & ((1 << d) - 1)
        if lift(low, d, period) == mask:
            return (d, low)
    raise AssertionError('period itself must work')


def admissible_growth(r):
    assert 1 <= r <= 6
    limit = 14 * r // (15 - 2 * r)
    return tuple(n for n in range(1, limit + 1) if r * ((2*n + 14)//15) >= n)


def candidates(state, minimum, forbidden):
    r, L, mask = state
    if r == 0:
        return set(), 0
    targets = set()
    qualifying = 0
    for n in admissible_growth(r):
        T = L * n
        R = lift(mask, L, T)
        size = R.bit_count()
        for h in divisors(T):
            if h < minimum or h in forbidden or h // gcd(h, L) != n:
                continue
            for a, B in rows(h):
                covered = R & lift(B, h, T)
                if r * covered.bit_count() >= size:
                    qualifying += 1
                    D, rest = normalize(T, R ^ covered)
                    assert rest, ('cover found', state, h, a)
                    targets.add((r-1, D, rest))
    return targets, qualifying


def represented_child(state, h, a, minimum, forbidden):
    assert h >= minimum and h not in forbidden
    B = literal_row(h, a)
    r, L, mask = state
    assert r > 0
    T = L * h // gcd(L, h)
    R = lift(mask, L, T)
    covered = R & lift(B, h, T)
    assert r * covered.bit_count() >= R.bit_count()
    D, rest = normalize(T, R ^ covered)
    assert rest
    return r-1, D, rest


def validate_state(state):
    r, L, mask = state
    assert type(r) is int and 0 <= r <= 6
    assert type(L) is int and L > 0
    assert type(mask) is int and 0 < mask < 1 << L


def audit(path, mode):
    raw = path.read_bytes()
    data = json.loads(raw)
    graph = {}
    if mode in ('no3', 'six'):
        minimum, forbidden = 2, ({3} if mode == 'no3' else set())
        for node in data['states']:
            s = node['remaining'], node['period'], int(node['missing_hex'], 16)
            assert s not in graph
            if mode == 'no3':
                graph[s] = [(e['period'], e['numerator'],
                             (e['next'][0], e['next'][1], int(e['next'][2], 16)))
                            for e in node['edges']]
            else:
                graph[s] = [(e['row'][0], e['row'][1],
                             (e['state'][0], e['state'][1], int(e['state'][2], 16)))
                            for e in node['children']]
        root = data['root']
        roots = {(root[0], root[1], int(root[2], 16))}
        assert roots == ({(6, 2, 2)} if mode == 'no3' else {(4, 6, 34)})
    else:
        minimum, forbidden = data['minimum_period'], set()
        assert 3 <= minimum <= 16
        assert data['complete'] is True and data['max_cover_rows'] == 7
        byid = {}
        for node in data['nodes']:
            assert node['id'] not in byid
            residues = node['residual']
            assert residues == sorted(set(residues))
            assert all(type(j) is int and 0 <= j < node['period'] for j in residues)
            s = node['remaining'], node['period'], sum(1 << j for j in residues)
            assert node['kind'] in ('branch', 'nonempty')
            if node['kind'] == 'nonempty':
                assert s[0] == 0
            byid[node['id']] = s
        for node in data['nodes']:
            s = byid[node['id']]
            assert s not in graph
            graph[s] = [(e['h'], e['a'], byid[e['child']]) for e in node.get('children', [])]
        roots = {byid[i] for i in data['root_ids']}
        expected = {(6, minimum, ((1 << minimum)-1) ^ B) for _, B in rows(minimum)}
        assert roots == expected, ('root omission', roots ^ expected)
    edges = total_rows = 0
    for s, recorded in graph.items():
        validate_state(s)
        expected, count = candidates(s, minimum, forbidden)
        actual = {child for _, _, child in recorded}
        assert len(actual) == len(recorded), ('duplicate edge', s)
        assert expected == actual, ('incomplete child set', s, expected-actual, actual-expected)
        for h, a, child in recorded:
            validate_state(child)
            assert represented_child(s, h, a, minimum, forbidden) == child
            assert child[0] == s[0]-1
            if child[0]:
                assert child in graph, ('missing descendant', child)
            else:
                assert not graph.get(child, [])
        edges += len(recorded)
        total_rows += count
    seen, todo = set(), list(roots)
    while todo:
        s = todo.pop()
        if s in seen:
            continue
        seen.add(s)
        if s[0]:
            assert s in graph
        todo.extend(child for _, _, child in graph.get(s, []))
    assert not (set(graph) - seen), 'unreachable graph nodes'
    return dict(file=str(path), sha256=sha256(raw).hexdigest(), mode=mode,
                minimum_period=minimum, nodes=len(graph), edges=edges,
                all_qualifying_physical_rows=total_rows,
                maximum_period=max(s[1] for s in graph), roots=len(roots), complete=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--manager-dir', type=Path, required=True)
    parser.add_argument('--prover-dir', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    assert literal_row(2, 1) == 1
    assert not (literal_row(16, 1) & (1 << 1)), 'equality at 1/15 is safe'
    assert admissible_growth(6) == (1,2,3,4,5,6,8,9,10,11,12,16,17,18,23,24)
    started = time.monotonic()
    results = []
    tasks = [(args.manager_dir/'no-period3-complete.graph.json', 'no3')]
    tasks += [(args.manager_dir/'six-with-two-three-excluded.json', 'six')]
    tasks += [(args.prover_dir/f'no-period-two-p{p}.json', 'no2') for p in range(3,17)]
    for path, mode in tasks:
        result = audit(path, mode)
        results.append(result)
        print(json.dumps(result), flush=True)
        args.output.write_text(json.dumps(dict(status='in progress', audits=results), indent=2)+'\n')
    report = dict(status='PASS; same-family independent replay, not verified:review',
                  elapsed_seconds=time.monotonic()-started,
                  checker_sha256=sha256(Path(__file__).read_bytes()).hexdigest(), audits=results)
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', elapsed_seconds=report['elapsed_seconds'])), flush=True)


if __name__ == '__main__':
    main()
