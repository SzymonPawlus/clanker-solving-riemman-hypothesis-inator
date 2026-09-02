"""Checker B -- written independently of ``exact_gate.py``, in Cartesian coordinates over Q(sqrt 3).

Problem ``RULES.md`` SS3 asks for a *second, independently written* checker, and the point of it is
that it shares no representation with the first.  Checker A works in oblique coordinates where
sqrt(3) never appears.  Checker B refuses that shortcut: it works in the literal Cartesian
placement of problem ``RULES.md`` SS2,

    A = (0, 0),   B = (L, 0),   C = (L/2, L*sqrt(3)/2),

carries numbers as elements ``p + q*sqrt(3)`` of the field Q(sqrt 3) with a general-purpose exact
sign routine, and evaluates the three half-plane containments and the pairwise squared distances
directly from that geometry.  It does not import ``exact_gate``.

Sign of ``p + q*sqrt(3)`` exactly: if p and q have the same sign the sign is theirs; otherwise
compare ``p^2`` against ``3 q^2`` and attach the sign of whichever term dominates.

Certificate exchange format (``cert.json``)
-------------------------------------------
``{"n", "side": [p, q], "points": [[[p,q],[p,q]], ...], "separation"}`` where every ``[p, q]``
is a pair of exact rational strings denoting ``p + q*sqrt(3)``, ``side`` is the declared side of
the triangle and ``separation`` the required minimum pairwise distance.  The repo certificate
schema (problem ``RULES.md`` SS2) asks for exact algebraic coordinate *expressions*; a bare pair
of rationals over the fixed basis {1, sqrt 3} says the same thing without needing a parser, and a
parser is exactly the kind of soundness-sensitive component SS5 of the repo rules says not to add
casually.  The deviation is deliberate and is recorded in the attack README.
"""

from __future__ import annotations

import json
import math
import sys
from fractions import Fraction
from typing import Sequence

Rat = Fraction
#: an element p + q*sqrt(3)
Alg = tuple[Rat, Rat]

ZERO: Alg = (Fraction(0), Fraction(0))


def add(a: Alg, b: Alg) -> Alg:
    return (a[0] + b[0], a[1] + b[1])


def sub(a: Alg, b: Alg) -> Alg:
    return (a[0] - b[0], a[1] - b[1])


def mul(a: Alg, b: Alg) -> Alg:
    # (p1 + q1 r)(p2 + q2 r) = p1 p2 + 3 q1 q2 + (p1 q2 + q1 p2) r,  r = sqrt(3)
    return (a[0] * b[0] + 3 * a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def scal(c: Rat, a: Alg) -> Alg:
    return (c * a[0], c * a[1])


def sign(a: Alg) -> int:
    """Exact sign of p + q*sqrt(3).  No floating point anywhere in this function."""
    p, q = a
    if p == 0 and q == 0:
        return 0
    if p >= 0 and q >= 0:
        return 1
    if p <= 0 and q <= 0:
        return -1
    # opposite signs: compare magnitudes p^2 vs 3 q^2
    lhs = p * p
    rhs = 3 * q * q
    if lhs == rhs:
        return 0
    dominant_is_p = lhs > rhs
    if dominant_is_p:
        return 1 if p > 0 else -1
    return 1 if q > 0 else -1


def cmp(a: Alg, b: Alg) -> int:
    return sign(sub(a, b))


def to_float(a: Alg) -> float:
    return float(a[0]) + float(a[1]) * math.sqrt(3.0)


# --------------------------------------------------------------------------------------------


def check(points: Sequence[tuple[Alg, Alg]], side: Alg, separation: Rat) -> dict:
    """Full exact check.  Returns a dict of findings; no tolerance is used at any step."""
    n = len(points)
    sep2: Alg = (separation * separation, Fraction(0))

    # --- containment: the three edges of conv{(0,0), (L,0), (L/2, L sqrt3/2)} ----------------
    # bottom  y >= 0
    # left    sqrt(3) x - y >= 0
    # right   sqrt(3) (L - x) - y >= 0
    r: Alg = (Fraction(0), Fraction(1))  # sqrt(3)
    outside: list[tuple[int, str]] = []
    for i, (x, y) in enumerate(points):
        if sign(y) < 0:
            outside.append((i, "bottom"))
        if sign(sub(mul(r, x), y)) < 0:
            outside.append((i, "left"))
        if sign(sub(mul(r, sub(side, x)), y)) < 0:
            outside.append((i, "right"))

    # --- pairwise separations ---------------------------------------------------------------
    worst: Alg | None = None
    worst_pair = (-1, -1)
    violations = 0
    for i in range(n):
        for j in range(i + 1, n):
            dx = sub(points[i][0], points[j][0])
            dy = sub(points[i][1], points[j][1])
            d2 = add(mul(dx, dx), mul(dy, dy))
            if worst is None or cmp(d2, worst) < 0:
                worst, worst_pair = d2, (i, j)
            if cmp(d2, sep2) < 0:
                violations += 1
    assert worst is not None

    # --- tightness: the exact minimal side for this placement --------------------------------
    # A point (x, y) sits in T_L iff L >= x + y/sqrt(3) (from the right edge); the other two
    # constraints do not involve L.  So L_min = max_i (x_i + y_i/sqrt(3)) = max_i (x_i + y_i*sqrt(3)/3).
    third_r: Alg = (Fraction(0), Fraction(1, 3))
    L_min: Alg | None = None
    for x, y in points:
        cand = add(x, mul(third_r, y))
        if L_min is None or cmp(cand, L_min) > 0:
            L_min = cand
    assert L_min is not None

    return {
        "n": n,
        "contained": not outside,
        "outside": outside,
        "separation_ok": violations == 0,
        "violations": violations,
        "min_sq_distance": worst,
        "min_sq_distance_float": to_float(worst),
        "closest_pair": worst_pair,
        "declared_side": side,
        "declared_side_float": to_float(side),
        "minimal_side": L_min,
        "minimal_side_float": to_float(L_min),
        "tight": cmp(L_min, side) == 0,
    }


# --------------------------------------------------------------------------------------------


def _alg(v) -> Alg:
    return (Fraction(v[0]), Fraction(v[1]))


def load(path: str) -> dict:
    with open(path) as fh:
        return json.load(fh)


def check_file(path: str) -> dict:
    cert = load(path)
    pts = [( _alg(p[0]), _alg(p[1]) ) for p in cert["points"]]
    return check(pts, _alg(cert["side"]), Fraction(cert["separation"]))


if __name__ == "__main__":
    for path in sys.argv[1:]:
        res = check_file(path)
        print(f"--- {path}")
        for k in ("n", "contained", "separation_ok", "violations", "tight"):
            print(f"    {k:16s} {res[k]}")
        print(f"    min_sq_distance  {res['min_sq_distance']}  ~ {res['min_sq_distance_float']:.18f}")
        print(f"    declared_side    {res['declared_side']}  ~ {res['declared_side_float']:.15f}")
        print(f"    minimal_side     {res['minimal_side']}  ~ {res['minimal_side_float']:.15f}")
