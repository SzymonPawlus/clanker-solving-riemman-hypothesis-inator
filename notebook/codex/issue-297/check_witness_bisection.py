"""Reproducible exact checks for the manager's constructive exploration."""
from fractions import Fraction
from itertools import combinations
import json
from random import Random
from time import perf_counter
import argparse

from witness_bisection import CORE, bad_count, exact_witness, floor_sum


def main(benchmark=False):
    rng = Random(304297)
    for _ in range(10000):
        n = rng.randrange(101)
        m = rng.randrange(1, 101)
        a = rng.randrange(-200, 201)
        b = rng.randrange(-200, 201)
        assert floor_sum(n, m, a, b) == sum((a*j+b)//m for j in range(n))

    for _ in range(20000):
        c = rng.randrange(1, 100)
        u = rng.randrange(1, 40)
        r = rng.randrange(u)
        w = rng.randrange(1, 18*c)
        lo = rng.randrange(c+1)
        hi = rng.randrange(lo, c+1)
        m = 15*u*c
        direct = sum(
            min(w*(15*u*j+15*r+1) % m, -w*(15*u*j+15*r+1) % m) < u*c
            for j in range(lo, hi)
        )
        assert bad_count(c, u, r, w, lo, hi) == direct

    # The primitive finite box is every six-element subset of the ten unused
    # speeds below 18. No symmetry quotient or sieve is used.
    choices = sorted(set(range(1, 18)) - set(CORE))
    primitive_count = 0
    for extras in combinations(choices, 6):
        result = exact_witness(1, extras)
        assert Fraction(result['minimum_distance']) >= Fraction(1, 15)
        primitive_count += 1
    assert primitive_count == 210

    boundary = exact_witness(1, (3, 4, 8, 10, 14, 15))
    assert boundary['time'] == '31/75'
    assert boundary['minimum_distance'] == '1/15'
    assert exact_witness(1, (-3, -4, -8, -10, -14, -15))['time'] == '31/75'
    assert exact_witness(1, (3, 3, 4, -4, 5, -5))['minimum_distance'] == '1/15'

    benchmarks = []
    campaign = ((6, 100), (30, 100), (100, 100), (300, 30), (1000, 3)) if benchmark else ((6, 5), (30, 5), (100, 2))
    for digits, trials in campaign:
        c = 10**digits + 239
        start = perf_counter()
        max_counts = max_splits = 0
        for _ in range(trials):
            extras = []
            while len(extras) < 6:
                w = rng.randrange(1, 18*c)
                if w % c or w // c not in CORE:
                    extras.append(w)
            result = exact_witness(c, extras)
            max_counts = max(max_counts, result['modular_interval_counts'])
            max_splits = max(max_splits, result['splits'])
        benchmarks.append({'scale_decimal_digits':digits+1,'trials':trials,
                           'elapsed_seconds':round(perf_counter()-start,6),
                           'max_modular_interval_counts':max_counts,
                           'max_splits':max_splits})
        print(json.dumps(benchmarks[-1]), flush=True)
    print(json.dumps({'floor_sum_fixtures':10000,'interval_fixtures':20000,
                      'primitive_completions':primitive_count,
                      'endpoint_fixture':boundary,'benchmarks':benchmarks}, indent=2))


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--benchmark',action='store_true',help='include the slower thousand-digit performance campaign')
    main(parser.parse_args().benchmark)
