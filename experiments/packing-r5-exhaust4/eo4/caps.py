"""Per-cell capacity from the cited table of a(k) = d(k)/2.

a(k) is the least side of a *unit-separation* equilateral triangle holding k
points at pairwise distance >= 1, i.e. a(k) = d(k)/2 with d from the problem
README's cited table.

CIRCULARITY GUARD.  a(9) = 3 IS the statement being reconstructed and a(10) = 3
is Oler's Delta(4) theorem.  Neither is in the table below: only k <= 8 is used,
so no run can assume any part of its own conclusion.  (a(5) = 2 is EO(3), which
is cited and logically independent of EO(4); it is used.)

Each value is (rational_part, coefficient, radicand) meaning p + c*sqrt(r).
"""
from fractions import Fraction
from math import isqrt

# a(k) for k = 1..8.  a(k) = (s(k) - 2*sqrt3)/2.
_A = {
    1: (Fraction(0), Fraction(0), 1),
    2: (Fraction(1), Fraction(0), 1),
    3: (Fraction(1), Fraction(0), 1),
    4: (Fraction(0), Fraction(1), 3),          # s=4sqrt3 -> d=2sqrt3 -> a=sqrt3
    5: (Fraction(2), Fraction(0), 1),          # s=4+2sqrt3
    6: (Fraction(2), Fraction(0), 1),          # s=4+2sqrt3 (Oler, Delta(3))
    7: (Fraction(1), Fraction(1), 3),          # s=2+4sqrt3 -> a=1+sqrt3
    8: (Fraction(1), Fraction(1, 3), 33),      # s=2+2sqrt3+2sqrt33/3 -> a=1+sqrt33/3
}
MAX_CITED = 8


def _enclose(k, prec=10 ** 40):
    """Rational [lo, hi] enclosure of a(k); exact (lo == hi) when a(k) is rational."""
    p, c, r = _A[k]
    if c == 0 or r == 1:
        return p + c, p + c
    lo = Fraction(isqrt(r * prec * prec), prec)
    hi = lo + Fraction(1, prec)
    return p + c * lo, p + c * hi


def refutes_multiplicity(m, h, t, strict, max_cited=MAX_CITED):
    """True if m points at separation (> t if strict else >= t) cannot lie in a
    closed equilateral triangle of side h.

    Strict case: m such points have separation >= t+eps for some eps > 0, so
    they fit in T(h) only if a(m) <= h/(t+eps) < h/t.  Hence a(m) >= h/t refutes.
    Closed case: they fit only if a(m) <= h/t, so a(m) > h/t refutes.

    Fails closed (returns False) whenever the comparison is not decided.
    """
    if m <= 1:
        return False
    ratio = Fraction(h) / Fraction(t)
    for k in range(min(m, max_cited), 1, -1):
        lo, hi = _enclose(k)
        if strict:
            if lo >= ratio:
                return True
        else:
            if lo > ratio:
                return True
    return False


def capacity(h, t, strict, nmax, max_cited=MAX_CITED):
    """Largest m <= nmax not refuted by the rule above."""
    for m in range(nmax, 0, -1):
        if not refutes_multiplicity(m, h, t, strict, max_cited):
            return m
    return 0
