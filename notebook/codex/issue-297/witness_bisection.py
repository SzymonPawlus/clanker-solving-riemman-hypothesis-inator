"""Exact constructive exploration for the frozen issue-304 scaling candidate.

This is not a verifier for that certificate. It constructs and directly checks
one common witness for a specified scaled core and at most six extra speeds.
The mathematical guarantee is conditional on the separate dual certificate.
"""
from __future__ import annotations

from fractions import Fraction
from math import gcd
from typing import Iterable

CORE = (1, 5, 6, 7, 9, 11, 13, 18)


def floor_sum(n: int, m: int, a: int, b: int) -> int:
    """Return sum floor((a*j+b)/m), 0<=j<n, by Euclidean descent."""
    if n < 0 or m <= 0:
        raise ValueError("require n>=0 and m>0")
    total = 0
    while True:
        qa, a = divmod(a, m)
        qb, b = divmod(b, m)
        total += qa * n * (n - 1) // 2 + qb * n
        top = a * n + b
        if top < m:
            return total
        n, b = divmod(top, m)
        m, a = a, m


def bad_count(c: int, u: int, r: int, w: int, lo: int, hi: int) -> int:
    """Count STRICT bad incidences on an arbitrary interval of lift indices."""
    h = u * c
    modulus = 15 * h
    a = 15 * u * w
    b = w * (15 * r + 1) + a * lo
    n = hi - lo
    # Residues h and 14h are safe; h-1 and 14h+1 are bad.
    return n + floor_sum(n, modulus, a, b + h - 1) - floor_sum(
        n, modulus, a, b + 14 * h
    )


def deficit_types(core: Iterable[int] = CORE) -> tuple[tuple[int, int], ...]:
    core = tuple(core)
    return tuple(
        (u, r)
        for u in core
        for r in range(u)
        if all(
            min(v * (15 * r + 1) % (15 * u), -v * (15 * r + 1) % (15 * u)) >= u
            for v in core
        )
    )


def exact_witness(
    scale: int, extra_speeds: Iterable[int], core: Iterable[int] = CORE
) -> dict:
    """Find a witness using O(log^2(scale)) exact arithmetic operations.

    The guarantee requires a nonnegative uniform-fiber dual of mass >len(extras)
    for this core. Such a candidate is frozen separately for the default core.
    Every returned witness is checked directly, regardless of that guarantee.
    """
    if isinstance(scale, bool) or not isinstance(scale, int) or scale <= 0:
        raise ValueError("scale must be a positive integer")
    core = tuple(sorted(set(core)))
    supplied = tuple(extra_speeds)
    if any(isinstance(w, bool) or not isinstance(w, int) or not w for w in supplied):
        raise ValueError("extra speeds must be nonzero integers")
    if len(supplied) > 6:
        raise ValueError("at most six additional coordinates are supported")
    fixed = {scale * u for u in core}
    extras = tuple(sorted({abs(w) for w in supplied} - fixed))
    if any(w >= scale * max(core) for w in extras):
        raise ValueError("all additional absolute speeds must lie below the core maximum")
    calls = 0

    def score(u: int, r: int, lo: int, hi: int) -> int:
        nonlocal calls
        calls += len(extras)
        return hi - lo - sum(bad_count(scale, u, r, w, lo, hi) for w in extras)

    for u, r in deficit_types(core):
        initial = score(u, r, 0, scale)
        if initial > 0:
            break
    else:
        raise ValueError("no primitive fiber has positive signed score")
    lo, hi = 0, scale
    current = initial
    splits = 0
    while hi - lo > 1:
        mid = (lo + hi) // 2
        left = score(u, r, lo, mid)
        if left > 0:
            hi, current = mid, left
        else:
            lo, current = mid, current - left
        assert current > 0
        splits += 1
    assert current == 1
    witness = Fraction(15 * u * lo + 15 * r + 1, 15 * u * scale)
    num, den = witness.numerator, witness.denominator
    all_speeds = tuple(sorted(fixed | set(extras)))
    distances = tuple(min(w * num % den, -w * num % den) for w in all_speeds)
    assert all(15 * distance >= den for distance in distances)
    return {
        "scale": scale,
        "core": core,
        "extras": extras,
        "fiber": (u, r),
        "lift_index": lo,
        "initial_signed_score": initial,
        "time": str(witness),
        "minimum_distance": str(Fraction(min(distances), den)),
        "splits": splits,
        "modular_interval_counts": calls,
    }

