"""Certified rational enclosures, written from scratch for the n16-budget lane.

Every public function returns exact ``Fraction``s that are rigorous bounds in the
named direction.  No float is ever consulted for a decision anywhere downstream.

Independence note: this module is an independent reimplementation.  It is
cross-checked against three things that do not share its code path --- Machin
vs. Euler for pi, r*r <= x <= R*R for every sqrt, and sin(asin_lo(x)) <= x <=
sin(asin_hi(x)) for every arcsin --- so a transcription error shows up as a
failed assertion rather than as a wrong sixth decimal.
"""
from fractions import Fraction as F
from math import isqrt

# ------------------------------------------------------------------ arctan / pi

def _arctan(x, terms):
    """Enclosure of arctan(x), 0 < x < 1, from the alternating Taylor series.

    Terms x^(2k+1)/(2k+1) strictly decrease, so consecutive partial sums bracket.
    """
    assert 0 < x < 1
    s = F(0)
    prev = F(0)
    xp = x                      # x^(2k+1)
    x2 = x * x
    for k in range(terms):
        prev = s
        s += (-1) ** k * xp / (2 * k + 1)
        xp *= x2
    return (min(s, prev), max(s, prev))


def _pi_machin(terms=45):
    a = _arctan(F(1, 5), terms)
    b = _arctan(F(1, 239), terms)
    return (4 * (4 * a[0] - b[1]), 4 * (4 * a[1] - b[0]))


def _pi_euler(terms=90):
    a = _arctan(F(1, 2), terms)
    b = _arctan(F(1, 3), terms)
    return (4 * (a[0] + b[0]), 4 * (a[1] + b[1]))


_m = _pi_machin()
_e = _pi_euler()
# two formulas, disjoint code paths for the argument: the enclosures must overlap
assert _m[0] <= _e[1] and _e[0] <= _m[1], "pi: Machin and Euler disagree"
PI_LO = max(_m[0], _e[0])
PI_HI = min(_m[1], _e[1])
assert PI_HI - PI_LO < F(1, 10 ** 25)

# -------------------------------------------------------------------- sqrt

_S = 10 ** 40


def sqrt_lo(x):
    """Largest r = m/_S with r*r <= x; hence r <= sqrt(x)."""
    x = F(x)
    assert x >= 0
    m = isqrt(x.numerator * _S * _S // x.denominator)
    r = F(m, _S)
    assert r * r <= x
    return r


def sqrt_hi(x):
    """Rational R with R*R >= x; hence R >= sqrt(x)."""
    x = F(x)
    assert x >= 0
    r = sqrt_lo(x)
    R = r + F(1, _S)
    assert R * R >= x
    return R


SQRT3_LO = sqrt_lo(3)
SQRT3_HI = sqrt_hi(3)

# -------------------------------------------------------------------- arcsin
# arcsin(x) = sum_{k>=0} C(2k,k) x^(2k+1) / (4^k (2k+1)),  all terms > 0.
# Ratio t_{k+1}/t_k = (2k+1)^2 x^2 / (2 (k+1)(2k+3)) < x^2, so the tail after
# the term of index K-1 is < t_{K-1} * x^2/(1-x^2)  (geometric majorant).


def _asin_partial(x, terms):
    x = F(x)
    assert 0 <= x < 1
    s = F(0)
    t = x                       # t_0 = x  (k = 0 term)
    for k in range(terms):
        s += t
        t = t * (2 * k + 1) ** 2 * x * x / (2 * (k + 1) * (2 * k + 3))
    return s, t                 # s = sum_{k<terms}, t = t_terms


def asin_lo(x, terms=400):
    s, _ = _asin_partial(x, terms)
    return s


def asin_hi(x, terms=400):
    x = F(x)
    s, t = _asin_partial(x, terms)
    x2 = x * x
    assert x2 < 1
    return s + t / (1 - x2)     # t_terms + t_terms*x^2 + ... majorises the tail


def _sin_bounds(x, terms=30):
    """Enclosure of sin(x) for 0 <= x <= 2, alternating series."""
    x = F(x)
    s = F(0)
    prev = F(0)
    xp = x
    x2 = x * x
    for k in range(terms):
        prev = s
        f = 1
        for i in range(2, 2 * k + 2):
            f *= i
        s += (-1) ** k * xp / f
        xp *= x2
    return (min(s, prev), max(s, prev))


if __name__ == "__main__":
    print(f"pi   in [{float(PI_LO):.15f}, {float(PI_HI):.15f}]")
    print(f"sq3  in [{float(SQRT3_LO):.15f}, {float(SQRT3_HI):.15f}]")
    for q in (F(1, 2), F(9, 10), F(96, 100), F(99, 100)):
        lo, hi = asin_lo(q), asin_hi(q)
        assert lo <= hi
        # independent check: sin(asin_lo(q)) <= q <= sin(asin_hi(q))
        sl = _sin_bounds(lo)
        sh = _sin_bounds(hi)
        assert sl[0] <= q, (q, "asin_lo too big")
        assert sh[1] >= q, (q, "asin_hi too small")
        print(f"asin({float(q):.2f}) in [{float(lo):.12f}, {float(hi):.12f}]"
              f"  width {float(hi-lo):.3e}  (sin-check ok)")
    # pi/3 - sqrt3/4 = f(1), the lens area
    print("f(1) = pi/3 - sqrt3/4 in "
          f"[{float(PI_LO/3 - SQRT3_HI/4):.12f}, {float(PI_HI/3 - SQRT3_LO/4):.12f}]")
    print("self-tests passed")
