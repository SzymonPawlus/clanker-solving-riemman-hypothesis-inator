"""Exact comparisons against the algebraic constants d(k) = s(k) - 2*sqrt(3).

Everything here decides a *conclusion*, so nothing is allowed to be a float.  A
constant is carried as a finite rational combination

    q0 + q1*sqrt(3) + q2*sqrt(6) + q3*sqrt(33)

and compared against a rational by refining rational enclosures of the surds until
the sign of the difference is decided.  1, sqrt(3), sqrt(6), sqrt(33) are linearly
independent over Q, so a non-zero combination is bounded away from zero and the
refinement terminates; the loop is nevertheless bounded and *fails closed* (returns
``None`` = "undecided"), which loses pruning but never soundness.
"""

from __future__ import annotations

from fractions import Fraction
from math import isqrt

# --------------------------------------------------------------------------- surds


def sqrt_lo_hi(m: int, denom: int) -> tuple[Fraction, Fraction]:
    """Rational enclosure of sqrt(m) with width <= 1/denom.

    ``isqrt`` is exact integer arithmetic, so ``r = isqrt(m*denom**2)`` satisfies
    ``r <= denom*sqrt(m) < r+1`` exactly.  No floating point anywhere.
    """
    r = isqrt(m * denom * denom)
    return Fraction(r, denom), Fraction(r + 1, denom)


def sqrt_upper(m: int, denom: int = 10**30) -> Fraction:
    """A rational UPPER bound for sqrt(m).  Used where over-estimating is the safe side."""
    return sqrt_lo_hi(m, denom)[1]


# ------------------------------------------------------- the cited d(k), k = 1..15
#
# d(k) = s(k) - 2*sqrt(3) with s(k) taken from
# problems/circle-packing-equilateral-triangle/README.md (status `cited`).
# Stored as (rational, coeff of sqrt3, coeff of sqrt6, coeff of sqrt33).

_F = Fraction

CITED_D: dict[int, tuple[Fraction, Fraction, Fraction, Fraction]] = {
    1: (_F(0), _F(0), _F(0), _F(0)),
    2: (_F(2), _F(0), _F(0), _F(0)),
    3: (_F(2), _F(0), _F(0), _F(0)),
    4: (_F(0), _F(2), _F(0), _F(0)),  # 4*sqrt3 - 2*sqrt3 = 2*sqrt3
    5: (_F(4), _F(0), _F(0), _F(0)),
    6: (_F(4), _F(0), _F(0), _F(0)),
    7: (_F(2), _F(2), _F(0), _F(0)),  # 2 + 4sqrt3 - 2sqrt3
    8: (_F(2), _F(0), _F(0), _F(2, 3)),  # 2 + 2*sqrt33/3
    9: (_F(6), _F(0), _F(0), _F(0)),
    10: (_F(6), _F(0), _F(0), _F(0)),
    11: (_F(4), _F(0), _F(4, 3), _F(0)),  # 4 + 4*sqrt6/3
    12: (_F(4), _F(2), _F(0), _F(0)),  # 4 + 4sqrt3 - 2sqrt3
    13: (_F(4), _F(4, 3), _F(2, 3), _F(0)),  # 4 + 2sqrt6/3 + 10sqrt3/3 - 2sqrt3
    14: (_F(8), _F(0), _F(0), _F(0)),
    15: (_F(8), _F(0), _F(0), _F(0)),
}

MAX_CITED = 15


def cited_d_bounds(k: int, denom: int) -> tuple[Fraction, Fraction]:
    """Rational enclosure [lo, hi] of the cited d(k)."""
    q0, q3, q6, q33 = CITED_D[k]
    lo = hi = q0
    for coeff, m in ((q3, 3), (q6, 6), (q33, 33)):
        if coeff == 0:
            continue
        a, b = sqrt_lo_hi(m, denom)
        assert coeff > 0
        lo += coeff * a
        hi += coeff * b
    return lo, hi


def strictly_less_than_cited_d(side: Fraction, k: int) -> bool | None:
    """Is the rational ``side`` strictly below the cited d(k)?

    Returns True / False, or None if undecided within the refinement budget.
    """
    denom = 10**20
    for _ in range(6):
        lo, hi = cited_d_bounds(k, denom)
        if side < lo:
            return True
        if side >= hi:
            return False
        denom *= denom
    return None
