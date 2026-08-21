"""The ceiling of THIS attack's method: how far the corner+edge structure could
ever go, even with a perfectly sharp edge-piece bound f.

f(l) >= f_lo(l) := pi/4 - arcsin(l)/4 + l*sqrt(1-l^2)/4,

the area of the unit-diameter disk centred at (l/2, sqrt(1-l^2)/2) cut by the
line y = 0.  That set has diameter exactly 1, lies in {y >= 0} and has (0,0)
and (l,0) on its boundary circle, so it is admissible for f(l).

The structure lemma's budget for a covering of T_a is therefore AT LEAST
    3*(pi/6) + 12*f_lo((a-2)/4),
so no bound proved from that lemma can contradict a covering of T_a whenever
area(T_a) is below this.  The largest such a is the method's ceiling.
"""
from fractions import Fraction as F

from exactconst import PI_LO, PI_HI, SQRT3_HI, asin_hi, sqrt_lo

CEIL = F(46247636, 10 ** 7)


_CACHE = {}


def f_lo(ell):
    """Certified rational LOWER bound on f(ell) (0 <= ell <= 0.97)."""
    ell = F(ell)
    if ell not in _CACHE:
        _CACHE[ell] = PI_LO / 4 - asin_hi(ell) / 4 + ell * sqrt_lo(1 - ell * ell) / 4
    return _CACHE[ell]


def area_hi(a):
    """Rational UPPER bound for area(T_a)."""
    return SQRT3_HI * a * a / 4


def budget_lo(a, corner=None, cap=None):
    """A configuration the structure lemma cannot exclude: 3 vertex pieces at the
    full sector area and 12 edge pieces each with trace (a-2)/4."""
    c = PI_LO / 6 if corner is None else corner
    e = f_lo((a - 2) / 4)
    if cap is not None:
        c, e = min(c, cap), min(e, cap)
    return 3 * c + 12 * e


def ceiling(corner=None, cap=None, lo=F(4), hi=F(6), steps=40):
    """Largest a for which the lemma's budget still covers area(T_a)."""
    for _ in range(steps):
        mid = (lo + hi) / 2
        if area_hi(mid) <= budget_lo(mid, corner, cap):
            lo = mid
        else:
            hi = mid
    return lo


if __name__ == "__main__":
    A6 = F(674981, 10 ** 6)          # Graham (1975) biggest little hexagon, rounded DOWN
    HS = F(45, 100)                  # max hexagon in the unit 60-degree sector (numerical, >= 0.433)
    rows = [
        ("X1  corner+edge structure, exact f          (rigorous)", ceiling()),
        ("X2  X1 + every piece capped at A_6          (conditional)", ceiling(cap=A6)),
        ("X3  X2 + corner capped at 0.45              (conditional+numerical)",
         ceiling(corner=HS, cap=A6)),
    ]
    print("Ceiling of the method -- no argument of this shape can prove less:\n")
    for name, a in rows:
        print(f"  {name:58s}  A_15 <= {float(a):.6f} is UNREACHABLE"
              f"   ({'still above' if a > CEIL else 'BELOW'} 4.6247636)")
    print(f"\n  f_lo(0.70) = {float(f_lo(F(7,10))):.6f}   f_lo(0.65) = "
          f"{float(f_lo(F(65,100))):.6f}   pi/4 = {float(PI_HI/4):.6f}")
