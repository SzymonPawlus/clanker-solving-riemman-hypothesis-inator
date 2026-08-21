"""Certified rational enclosures for pi and sqrt(3), plus rational sqrt bounds.

Everything downstream must round in the direction that WEAKENS the conclusion.
Convention here: every function returns an exact ``Fraction`` that is a rigorous
bound in the stated direction.  No float ever reaches a decision.
"""
from fractions import Fraction as F


# ---------------------------------------------------------------- arctan series
def _arctan_bounds(p, q, terms):
    """Enclosure of arctan(p/q) for 0 < p/q < 1 by its alternating Taylor series.

    arctan(x) = sum_{k>=0} (-1)^k x^(2k+1)/(2k+1).  For 0<x<1 the terms decrease
    strictly in absolute value, so consecutive partial sums bracket the value.
    Returns (lo, hi) with lo <= arctan(p/q) <= hi.
    """
    x = F(p, q)
    s = F(0)
    prev = None
    for k in range(terms):
        term = (-1) ** k * x ** (2 * k + 1) / (2 * k + 1)
        prev = s
        s = s + term
    # s and prev are consecutive partial sums; they bracket the limit.
    return (min(s, prev), max(s, prev))


def pi_bounds(terms=40):
    """(lo, hi) with lo <= pi <= hi, via Machin's formula.

    pi/4 = 4*arctan(1/5) - arctan(1/239).
    """
    a_lo, a_hi = _arctan_bounds(1, 5, terms)
    b_lo, b_hi = _arctan_bounds(1, 239, terms)
    lo = 4 * (4 * a_lo - b_hi)
    hi = 4 * (4 * a_hi - b_lo)
    return lo, hi


def pi_bounds_euler(terms=80):
    """Independent cross-check: pi/4 = arctan(1/2) + arctan(1/3)."""
    a_lo, a_hi = _arctan_bounds(1, 2, terms)
    b_lo, b_hi = _arctan_bounds(1, 3, terms)
    return 4 * (a_lo + b_lo), 4 * (a_hi + b_hi)


# ---------------------------------------------------------------- rational sqrt
from math import isqrt

_SCALE = 10 ** 30


def sqrt_lo(x, scale=_SCALE):
    """Rational r with r*r <= x, so r <= sqrt(x).  Exact: r = floor(sqrt(x)*S)/S."""
    x = F(x)
    assert x >= 0
    m = isqrt(x.numerator * scale * scale // x.denominator)
    return F(m, scale)


def sqrt_hi(x, scale=_SCALE):
    """Rational r with r*r >= x, so r >= sqrt(x)."""
    x = F(x)
    assert x >= 0
    m = isqrt(x.numerator * scale * scale // x.denominator) + 1
    r = F(m, scale)
    assert r * r >= x
    return r


def arctan_lo(x, terms=60):
    """Rational lower bound for arctan(x), 0 <= x < 1."""
    return _arctan_bounds(F(x).numerator, F(x).denominator, terms)[0]


def arctan_hi(x, terms=60):
    return _arctan_bounds(F(x).numerator, F(x).denominator, terms)[1]


def asin_lo(x):
    """Rational lower bound for arcsin(x), 0 <= x <= 1/2 (so arctan arg < 1)."""
    x = F(x)
    assert 0 <= x <= F(1, 2)
    if x == 0:
        return F(0)
    t = x / sqrt_hi(1 - x * x)          # <= x/sqrt(1-x^2) = tan(arcsin x)
    return arctan_lo(t)


PI_LO, PI_HI = pi_bounds()
SQRT3_LO, SQRT3_HI = sqrt_lo(3), sqrt_hi(3)


def selftest():
    lo2, hi2 = pi_bounds_euler()
    assert lo2 <= PI_HI and PI_LO <= hi2, "pi enclosures disagree"
    inter_lo, inter_hi = max(PI_LO, lo2), min(PI_HI, hi2)
    assert inter_lo <= inter_hi
    assert SQRT3_LO ** 2 <= 3 <= SQRT3_HI ** 2
    assert PI_HI - PI_LO < F(1, 10 ** 20)
    assert SQRT3_HI - SQRT3_LO < F(1, 10 ** 20)
    # spot values
    assert PI_LO > F(31415926535, 10 ** 10) and PI_HI < F(31415926536, 10 ** 10)
    assert SQRT3_LO > F(17320508075, 10 ** 10) and SQRT3_HI < F(17320508076, 10 ** 10)
    return dict(pi_lo=float(PI_LO), pi_hi=float(PI_HI),
                pi_euler_lo=float(lo2), pi_euler_hi=float(hi2),
                sqrt3_lo=float(SQRT3_LO), sqrt3_hi=float(SQRT3_HI))


if __name__ == "__main__":
    import json
    print(json.dumps(selftest(), indent=2))
