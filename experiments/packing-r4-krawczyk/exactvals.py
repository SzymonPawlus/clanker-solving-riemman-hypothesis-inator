"""Known exact values and published records used ONLY as calibration targets.

Nothing here is derived in this directory; every entry carries its source.  These are
*upper-bound* reference values (constructions); the proven/best-known distinction is
Friedman's and is not re-litigated here.
"""

from __future__ import annotations

from fractions import Fraction

# d(n) = s(n) - 2*sqrt(3), written as a + b*sqrt(c) with a, b rational and c a positive int.
# Source: experiments/circle-packing-search/reference.py EXACT_S (Friedman, Packing Center),
# converted by d = s - 2*sqrt(3); the triangular rows d = 2*(k-1) are the k-row lattice.
EXACT_D: dict[int, tuple[Fraction, Fraction, int]] = {
    3: (Fraction(2), Fraction(0), 1),
    6: (Fraction(4), Fraction(0), 1),
    8: (Fraction(2), Fraction(2, 3), 33),
    10: (Fraction(6), Fraction(0), 1),
    12: (Fraction(4), Fraction(2), 3),
    15: (Fraction(8), Fraction(0), 1),
    21: (Fraction(10), Fraction(0), 1),
}

# Graham-Lubachevsky 1995 (EJC 2 #A1) printed d(n), 15 s.f., as tabulated in
# experiments/circle-packing-search/reference.py.  Their d(n) is the min pairwise distance of
# n points in a UNIT triangle, so our D = 2 / d_GL.
GL_D_STR: dict[int, str] = {
    8: "0.343070330817254",
    16: "0.216227269309782",
    17: "0.211324865405187",
    18: "0.203465240539124",
    19: "0.200321458983439",
    20: "0.2",
    21: "0.2",
    22: "0.179396908611866",
    23: "0.175153309170525",
    24: "0.174457630187010",
    25: "0.169065874417891",
    26: "0.166738399395271",
    27: "0.166666666666667",
    28: "0.166666666666667",
    29: "0.152189614060732",
    30: "0.150761500215428",
    31: "0.148543145110506",
    32: "0.145102169183849",
    33: "0.143447408371201",
    34: "0.142869646754496",
}


def gl_D(n: int) -> Fraction | None:
    """Published D = 2 / d_GL(n) as an exact rational built from the printed 15 s.f."""
    s = GL_D_STR.get(n)
    if s is None:
        return None
    return Fraction(2) / Fraction(s)


def cmp_rat_alg(q: Fraction, a: Fraction, b: Fraction, c: int) -> int:
    """Sign of q - (a + b*sqrt(c)), computed exactly.  Returns -1, 0 or +1."""
    t = q - a
    if b == 0:
        return (t > 0) - (t < 0)
    # compare t with b*sqrt(c)
    if b > 0:
        if t <= 0:
            return -1
        return (t * t > b * b * c) - (t * t < b * b * c)
    if t >= 0:
        return 1
    return (t * t < b * b * c) - (t * t > b * b * c)


def gl_D_band(n: int) -> tuple[Fraction, Fraction] | None:
    """Exact rational interval for D = 2 / d_GL(n) implied by the PRINTED digits.

    The paper prints d(n) rounded to the digits shown, so the true value lies within half a
    unit in the last printed place.  Anything inside the returned band is a match, not an
    improvement (problem RULES.md §4: an improvement must exceed the error bars).
    """
    s = GL_D_STR.get(n)
    if s is None:
        return None
    q = Fraction(s)
    ndec = len(s.split(".")[1]) if "." in s else 0
    h = Fraction(5, 10 ** (ndec + 1))
    return Fraction(2) / (q + h), Fraction(2) / (q - h)
