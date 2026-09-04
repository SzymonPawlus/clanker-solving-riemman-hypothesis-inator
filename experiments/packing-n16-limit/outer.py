"""Upper bound on A_15 = sup{a : T_a is coverable by 15 sets of diameter < 1}.

Every decision below is an exact rational comparison.  pi and sqrt(3) enter only
as certified enclosures, rounded in the direction that WEAKENS the conclusion:
the area of T_a is bounded BELOW (SQRT3_LO) and the covering budget ABOVE
(PI_HI).  See the attack README for the proofs of the structure lemma.

Usage:  python3 outer.py [N_slabs] [grid_denominator]
"""
import json
import os
import sys
from fractions import Fraction as F

from exactconst import PI_HI, PI_LO, SQRT3_LO, SQRT3_HI
from fbound import f_upper

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "out", "f_grid.json")


# --------------------------------------------------------------- f grid + hull
def f_grid(N=128, D=24):
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    key = f"N{N}_D{D}"
    data = {}
    if os.path.exists(CACHE):
        data = json.load(open(CACHE))
    if key not in data:
        vals = []
        for i in range(D + 1):
            b = f_upper(F(i, D), N)
            vals.append([b.numerator, b.denominator])
            print(f"    f({i}/{D}) <= {float(b):.7f}", flush=True)
        data[key] = vals
        json.dump(data, open(CACHE, "w"))
    return [F(n, d) for n, d in data[key]]


def hull_points(vals, D):
    """Points whose upper concave hull majorises f on [0,1].

    f is non-increasing (convexity of a piece: it contains a sub-segment of any
    shorter length), so on [g_i, g_{i+1}] we have f <= vals[i].  Taking the
    closed interval is an over-estimate, hence safe.
    """
    pts = []
    for i in range(D):
        pts.append((F(i, D), vals[i]))
        pts.append((F(i + 1, D), vals[i]))
    pts.append((F(1), vals[D]))
    return pts


def upper_hull(pts):
    """Upper concave hull of a point set, as a list of vertices left to right."""
    pts = sorted(set(pts))
    h = []
    for p in pts:
        while len(h) >= 2:
            (x1, y1), (x2, y2) = h[-2], h[-1]
            # drop h[-1] if it is on or below the segment h[-2] -> p
            if (y2 - y1) * (p[0] - x1) <= (p[1] - y1) * (x2 - x1):
                h.pop()
            else:
                break
        h.append(p)
    return h


def hull_eval(h, x):
    """Value of the piecewise-linear upper hull at x (exact)."""
    assert h[0][0] <= x <= h[-1][0]
    for (x1, y1), (x2, y2) in zip(h, h[1:]):
        if x1 <= x <= x2:
            if x2 == x1:
                return max(y1, y2)
            return y1 + (y2 - y1) * (x - x1) / (x2 - x1)
    raise ValueError


# ------------------------------------------------------------------- the bound
def area_lo(a):
    """Rational lower bound for area(T_a) = sqrt(3) a^2 / 4."""
    return SQRT3_LO * a * a / 4


def budget_hi(a, h, cap=None):
    """Rational upper bound for sum_i area(S_i cap T_a) over any 15-piece
    covering of T_a by sets of diameter < 1, from the structure lemma.

    3 vertex pieces (<= pi/6 each) + M_e pieces on each edge (k_e >= 3 of them,
    traces summing to >= a-2, each contributing <= f(trace)) + the rest (<= pi/4,
    or <= cap if a per-piece cap is assumed).
    """
    L = a - 2
    quarter = PI_HI / 4 if cap is None else min(PI_HI / 4, cap)
    sixth = PI_HI / 6 if cap is None else min(PI_HI / 6, cap)

    def fh(x):
        v = hull_eval(h, x)
        return v if cap is None else min(v, cap)

    best = None
    for k1 in range(3, 13):
        for k2 in range(3, 13 - k1 + 1):
            for k3 in range(3, 13 - k1 - k2 + 1):
                ks = (k1, k2, k3)
                if sum(ks) > 12:
                    continue
                tot = 3 * sixth + (12 - sum(ks)) * quarter
                ok = True
                for k in ks:
                    if L / k > 1:          # a trace cannot exceed the diameter
                        ok = False
                        break
                    tot += k * fh(L / k)
                if ok and (best is None or tot > best):
                    best = tot
    return best


def largest_a(fn, lo=F(4), hi=F(6), steps=60):
    """Largest a (to within 2^-steps) with area_lo(a) <= budget; above it the
    covering is impossible."""
    assert area_lo(lo) <= fn(lo), "lower bracket already contradictory"
    if area_lo(hi) <= fn(hi):
        return None
    for _ in range(steps):
        mid = (lo + hi) / 2
        if area_lo(mid) <= fn(mid):
            lo = mid
        else:
            hi = mid
    return hi


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 128
    D = int(sys.argv[2]) if len(sys.argv) > 2 else 24
    print(f"pi   in [{float(PI_LO):.12f}, {float(PI_HI):.12f}]")
    print(f"sq3  in [{float(SQRT3_LO):.12f}, {float(SQRT3_HI):.12f}]")
    print(f"\ncertified upper bounds for f(l), N={N} slabs, grid 1/{D}:")
    vals = f_grid(N, D)
    h = upper_hull(hull_points(vals, D))
    print(f"  concave hull vertices: {[(float(x), float(y)) for x, y in h]}")

    CEIL = F(46247636, 10 ** 7)      # Melissen-Schuur 16-point packing
    REC = F(446335, 10 ** 5)         # repo's certified 15-piece covering

    rows = []
    # U0 trivial isodiametric
    rows.append(("U0  15 * pi/4 (isodiametric only)",
                 largest_a(lambda a: 15 * PI_HI / 4)))
    # U1 corner-refined
    rows.append(("U1  3 * pi/6 + 12 * pi/4 (corners)",
                 largest_a(lambda a: 3 * PI_HI / 6 + 12 * PI_HI / 4)))
    # U2 main: corners + edge traces
    rows.append(("U2  corners + edge traces (THIS ATTACK)",
                 largest_a(lambda a: budget_hi(a, h))))
    # conditional variants
    A6 = F(6749815, 10 ** 7)         # Graham (1975) biggest little hexagon, rounded UP
    rows.append(("C1  [conditional] all pieces capped at A_6 = 0.6749815",
                 largest_a(lambda a: 15 * A6)))
    rows.append(("C2  [conditional] U2 with every piece also capped at A_6",
                 largest_a(lambda a: budget_hi(a, h, cap=A6))))

    print()
    for name, a in rows:
        if a is None:
            print(f"  {name:52s}  no contradiction anywhere in [4,6]")
        else:
            print(f"  {name:52s}  A_15 <= {float(a):.6f}"
                  f"   {'CLOSES' if a < CEIL else 'above ceiling'}")
    print(f"\n  ceiling to beat (16-point packing)                     {float(CEIL):.7f}")
    print(f"  repo's certified covering (lower bound on A_15)        {float(REC):.7f}")

    # K3 tripwire: no bound may fall below the certified covering
    for name, a in rows:
        if a is not None:
            assert a > REC, f"K3 TRIPWIRE: {name} contradicts the certified covering"
    print("\n  K3 tripwire: every bound is > 4.46335 (consistent with the "
          "certified 15-piece covering).")


if __name__ == "__main__":
    main()
