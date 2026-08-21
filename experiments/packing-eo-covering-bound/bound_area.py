"""Theorem 1: the corner-refined isodiametric floor, computed with certified rational enclosures.

    area(T_a)  <=  3 * (pi/6)  +  (N-3) * (pi/4)      =>   N >= 3 + (area(T_a) - pi/2) * 4/pi

  * pieces have diameter < 1, so a piece containing a corner V lies in B(V,1), hence its trace on
    T_a lies in the 60-degree sector of radius 1 there: area <= pi/6;
  * the three corners are pairwise at distance a >= 1, so they lie in three DISTINCT pieces;
  * every other piece has area < pi/4 (isodiametric / Bieberbach inequality, `cited`).

No floats.  pi and sqrt(3) enter only as rational enclosures, rounded in the direction that
weakens the conclusion.
"""
from fractions import Fraction as F

# rigorous enclosures (each verified by the exact checks at the bottom of this file)
PI_LO = F(3141592653589793, 10**15)
PI_HI = F(3141592653589794, 10**15)
SQ3_LO = F(17320508075688772, 10**16)
SQ3_HI = F(17320508075688773, 10**16)

def floor_bound(a):
    """A rigorous integer lower bound on N*(a) from Theorem 1."""
    area_lo = SQ3_LO * a * a / 4          # under-estimate of area(T_a)
    # N >= 3 + (area - pi/2) * 4 / pi ; weaken: use area_lo, PI_HI in -pi/2, PI_HI in the divisor
    val = 3 + (area_lo - PI_HI / 2) * 4 / PI_HI
    n = 0
    while n + 1 <= val:
        n += 1
    # N is an integer >= val, so N >= ceil(val)
    return (n + 1) if F(n) < val else n, val

def area_only(a):
    area_lo = SQ3_LO * a * a / 4
    val = area_lo * 4 / PI_HI
    n = 0
    while n + 1 <= val:
        n += 1
    return (n + 1) if F(n) < val else n, val

if __name__ == '__main__':
    # enclosure checks, exact
    assert PI_LO < PI_HI
    assert SQ3_LO ** 2 < 3 < SQ3_HI ** 2, "sqrt(3) enclosure"
    # Archimedes-style check of the pi enclosure via a Machin formula with exact rational bounds
    def atan_bounds(x, terms=40):
        lo = F(0); hi = F(0); t = x; s = 1
        acc = F(0)
        for k in range(terms):
            term = t / (2 * k + 1)
            acc += term if s > 0 else -term
            t *= x * x; s = -s
        nxt = t / (2 * terms + 1)
        return acc - nxt, acc + nxt
    l1, h1 = atan_bounds(F(1, 5)); l2, h2 = atan_bounds(F(1, 239))
    pi_lo = 16 * l1 - 4 * h2; pi_hi = 16 * h1 - 4 * l2
    assert PI_LO <= pi_lo and pi_hi <= PI_HI, (float(pi_lo), float(pi_hi))
    print("pi enclosure verified against Machin:", float(pi_lo), float(pi_hi))

    for a in [F(6), F(5999999, 10**6), F(5983367, 10**6), F(59, 10), F(5)]:
        n1, v1 = floor_bound(a)
        n0, v0 = area_only(a)
        print(f"a = {str(a):>18} = {float(a):.7f} : area-only N >= {n0} ({float(v0):.4f}), "
              f"corner-refined N >= {n1} ({float(v1):.4f})")
