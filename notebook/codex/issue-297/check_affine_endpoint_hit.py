#!/usr/bin/env python3
"""Direct rational fixtures for the independent endpoint-hit criterion."""
from fractions import Fraction
from math import gcd
from pathlib import Path
import hashlib
import json
import time


def main():
    start = time.monotonic()
    tests = 0
    general_grids = 0
    endpoints = [Fraction(u, v) for v in range(1, 76)
                 for u in range(v) if gcd(u, v) == 1]
    for M in range(1, 51):
        for q in range(1, M + 1):
            if gcd(q, M) != 1:
                continue
            grid = {Fraction((q * (15 * j + 1)) % (15 * M), 15 * M)
                    for j in range(M)}
            assert len(grid) == M
            general_grids += 1
            for x in endpoints:
                u, v = x.numerator, x.denominator
                prediction = (15 * M) % v == 0 and ((15 * M // v) * u - q) % 15 == 0
                assert prediction == (x in grid), (M, q, x)
                tests += 1
    composite_grids = 0
    composite_comparisons = 0
    for p in (7, 11, 17, 31):
        M = 15 * p
        # Any affine endpoint denominator divides 15|a|. Testing every reduced
        # fraction with such a denominator is stronger than any fixed phases.
        denominators = {v for a in range(1, p) if a % 15
                        for v in range(1, 15 * a + 1) if (15 * a) % v == 0}
        all_endpoints = {Fraction(u, v) for v in denominators
                         for u in range(v) if gcd(u, v) == 1}
        for q in range(1, M):
            if gcd(q, M) != 1:
                continue
            grid = {Fraction((q * (15 * j + 1)) % (15 * M), 15 * M)
                    for j in range(M)}
            assert not grid.intersection(all_endpoints), (p, q)
            composite_grids += 1
            composite_comparisons += len(all_endpoints)
    # A slope divisible by 15 destroys the universal avoidance assertion.
    M, q = 255, 1
    x = Fraction(8, 225)  # An actual boundary for slope a=15, shift b/15=8/15.
    assert Fraction(15) * x + Fraction(8, 15) == Fraction(16, 15)
    grid = {Fraction((q * (15 * j + 1)) % (15 * M), 15 * M)
            for j in range(M)}
    assert x in grid
    M, q = 165, 11
    # q shares a factor with M; the coprimality hypothesis cannot be discarded.
    bad_grid = {Fraction((q * (15 * j + 1)) % (15 * M), 15 * M)
                for j in range(M)}
    assert len(bad_grid) < M
    power_grids = 0
    power_comparisons = 0
    for K, M in ((5, 9), (12, 27), (30, 81), (60, 81)):
        denominators = {v for a in range(1, K + 1)
                        for v in range(1, 15 * a + 1) if (15 * a) % v == 0}
        all_endpoints = {Fraction(u, v) for v in denominators
                         for u in range(v) if gcd(u, v) == 1}
        for q in range(1, M):
            if q % 3 == 0:
                continue
            grid = {Fraction((q * (15 * j + 1)) % (15 * M), 15 * M)
                    for j in range(M)}
            assert not grid.intersection(all_endpoints), (K, M, q)
            power_grids += 1
            power_comparisons += len(all_endpoints)
    out = {
        'status': 'passed exact arithmetic fixtures; theorem remains sketch',
        'general_grids': general_grids,
        'literal_membership_comparisons': tests,
        'composite_grids': composite_grids,
        'composite_endpoint_comparisons': composite_comparisons,
        'power_of_three_grids': power_grids,
        'power_of_three_endpoint_comparisons': power_comparisons,
        'code_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'seconds': time.monotonic() - start,
    }
    path = Path(__file__).with_name('affine-endpoint-hit-checks.json')
    path.write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps(out, sort_keys=True))


if __name__ == '__main__':
    main()
