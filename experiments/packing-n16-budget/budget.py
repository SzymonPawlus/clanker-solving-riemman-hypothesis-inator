"""The area budget for a 15-piece covering of T_a, with the per-side piece counts
PINNED to (3,3,3) by the class structure of attacks/n16-structure/ Sec.3.1.

Separation 1 throughout; T_a is the closed equilateral triangle of side a; a
"piece" is a set of diameter STRICTLY < 1.  Nothing here reads results/, no value
of s(n)/d(n)/a_n and no covering number is an input (B4).

------------------------------------------------------------------ LEMMA S'
Let a >= 1 + 2 sqrt3 and let T_a = union of 15 pieces.

 1. (structure, `sketch`, attacks/n16-structure Sec.3.1)  Exactly 3 pieces meet
    two sides, 9 meet exactly one, 3 meet none, and each side is met by exactly
    5 pieces.
 2. The three two-side pieces are exactly the pieces containing the three
    vertices: each vertex's piece meets the two sides through it, and the three
    are distinct (vertices are a > 1 apart).  Such a piece P_V contains V and has
    diameter < 1, so P_V is a subset of B(V,1) and
        area(P_V cap T_a) <= area(B(V,1) cap T_a) = pi/6      (the 60-degree unit
    sector, valid for a >= 2).
 3. Let m_e be the "middle" of side e: the points of e at distance > 1 from both
    endpoints, a segment of length a-2.  P_V misses every m_e (it lies within 1
    of V).  A no-side piece misses e.  So the pieces meeting m_e are among the
    3 one-side pieces of e, i.e. k_e := #{i : S_i cap m_e nonempty} <= 3.
 4. The traces S_i cap e, i in M_e, cover m_e and each has 1-dimensional measure
    at most its diameter l_i < 1, so sum_i l_i >= a-2 and k_e > a-2 >= 2, giving
    k_e = 3 exactly -- and a - 2 < 3, i.e. a < 5, or no covering exists at all.
 5. For i in M_e the closure of S_i cap T_a has diameter <= 1, lies in the closed
    half-plane of e, and contains two points of the line of e at distance l_i, so
        area(S_i cap T_a) <= f(l_i) <= fhat(l_i),
    fhat = the concave envelope of f on [0,1].  Jensen plus fhat non-increasing:
        sum_{i in M_e} fhat(l_i) <= 3 fhat( (sum l_i)/3 ) <= 3 fhat( (a-2)/3 ).
 6. The remaining 3 (no-side) pieces get the isodiametric bound pi/4 each.

Subadditivity of outer measure over the 15 traces gives

    sqrt3 a^2 / 4 <= 3*(pi/6) + 9*fhat((a-2)/3) + 3*(pi/4).            (S')

The UNPINNED Lemma S of attacks/n16-covering-limit/ knows only k_e >= 3 with
sum_e k_e <= 12, and must therefore maximise its right-hand side over every
admissible (k_1,k_2,k_3); (S') deletes every branch but (3,3,3).  Both are
computed below from the SAME certified f grid, so the difference is the pinning
and nothing else.

Rounding is always against the conclusion: area(T_a) from below (SQRT3_LO), the
budget from above (PI_HI, certified f upper bounds).

Usage:  python3 budget.py [N_slabs] [grid_denominator]
"""
import json
import os
import sys
from fractions import Fraction as F

from exact import PI_HI, PI_LO, SQRT3_HI, SQRT3_LO
from fupper import f_upper
from flower import f_lo

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "out", "fgrid.json")

# The certified enclosures carry thousand-digit denominators; every quantity is
# therefore re-rounded to 10^-24 IN THE SAFE DIRECTION before it is used, so the
# arithmetic stays fast without ever weakening a guarantee.
RQ = 10 ** 24


def up(x):
    """Smallest multiple of 1/RQ that is >= x."""
    return F(-((-F(x).numerator * RQ) // F(x).denominator), RQ)


def dn(x):
    """Largest multiple of 1/RQ that is <= x."""
    return F(F(x).numerator * RQ // F(x).denominator, RQ)


PI_HI_R, PI_LO_R = up(PI_HI), dn(PI_LO)
SQRT3_HI_R, SQRT3_LO_R = up(SQRT3_HI), dn(SQRT3_LO)

# a >= 1 + 2 sqrt3 is where the class structure applies; it is also the largest a
# for which a 15-piece covering is exactly certified (attacks/n16-covering-2/),
# so ANY bound at or below it is a bug in this argument, never a result (B2).
TRIPWIRE_LO = up(1 + 2 * SQRT3_HI)      # >= 1 + 2 sqrt3
GRAIN = 10 ** 7                         # bisection grid for a
COMPARE = F(46247637, 10 ** 7)          # comparison target only, never an input


# ------------------------------------------------------------------- f grid
def nodes(D, DF, xf):
    """Grid: spacing 1/D on [0, xf], spacing 1/DF on [xf, 1].  The second half is
    where (a-2)/3 lands, and f is steepest there, so the step majorant below
    needs the finer mesh exactly there."""
    xs = [F(i, D) for i in range(int(xf * D) + 1)]
    xs += [F(i, DF) for i in range(int(xf * DF) + 1, DF + 1)]
    assert xs == sorted(set(xs)) and xs[0] == 0 and xs[-1] == 1
    return xs


def f_grid(N, xs):
    """Certified upper bounds f(x) <= v(x) at the nodes, cached per point."""
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    data = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
    vals, fresh = [], False
    for x in xs:
        key = f"N{N}:{x.numerator}/{x.denominator}"
        if key not in data:
            v = up(f_upper(x, N))
            data[key] = [v.numerator, v.denominator]
            fresh = True
            print(f"    f({float(x):.5f}) <= {float(v):.7f}", flush=True)
        vals.append(F(*data[key]))
    if fresh:
        json.dump(data, open(CACHE, "w"))
    return vals


def envelope(xs, vals):
    """Upper concave envelope of the step majorant of f.

    f is non-increasing, so f(x) <= vals[i] for x in [xs[i], xs[i+1]]; the step
    function F with those values majorises f on [0,1], and the concave envelope
    of F majorises the concave envelope of f.  The envelope of a step function is
    the upper concave hull of the points (xs[i], vals[i]), (xs[i+1], vals[i]).
    """
    m = len(xs) - 1
    pts = sorted({(xs[i], vals[i]) for i in range(m)} |
                 {(xs[i + 1], vals[i]) for i in range(m)} | {(xs[m], vals[m])})
    h = []
    for p in pts:
        while len(h) >= 2:
            (x1, y1), (x2, y2) = h[-2], h[-1]
            if (y2 - y1) * (p[0] - x1) <= (p[1] - y1) * (x2 - x1):
                h.pop()
            else:
                break
        h.append(p)
    # the envelope must be non-increasing (f is), else the bisection below is
    # not monotone; check it rather than assume it
    for (x1, y1), (x2, y2) in zip(h, h[1:]):
        assert y2 <= y1, "envelope not non-increasing"
    return h


def ev(h, x):
    """Exact value of the piecewise-linear envelope at x in [0,1]."""
    assert h[0][0] <= x <= h[-1][0], x
    for (x1, y1), (x2, y2) in zip(h, h[1:]):
        if x1 <= x <= x2:
            return y1 if x2 == x1 else y1 + (y2 - y1) * (x - x1) / (x2 - x1)
    raise ValueError(x)


# ------------------------------------------------------------------ budgets
def area_lo(a):
    return SQRT3_LO_R * a * a / 4


def area_hi(a):
    return SQRT3_HI_R * a * a / 4


def pinned_hi(a, h):
    """Upper bound for the right-hand side of (S'), or None if no 15-piece
    covering of T_a exists at all (three traces of length < 1 cannot cover a
    middle of length a-2 >= 3)."""
    ell = (a - 2) / 3
    if ell > 1:
        return None
    return 3 * (PI_HI_R / 6) + 9 * ev(h, ell) + 3 * (PI_HI_R / 4)


def unpinned_hi(a, h):
    """Upper bound for the right-hand side of the UNPINNED Lemma S: k_e >= 3,
    sum_e k_e <= 12, maximised over (k_1,k_2,k_3).  Reimplemented here to make
    the like-for-like comparison at the same f grid."""
    L = a - 2
    best = None
    for k1 in range(3, 7):
        for k2 in range(3, 7):
            for k3 in range(3, 7):
                if k1 + k2 + k3 > 12:
                    continue
                tot = 3 * (PI_HI_R / 6) + (12 - k1 - k2 - k3) * (PI_HI_R / 4)
                ok = True
                for k in (k1, k2, k3):
                    if L / k > 1:
                        ok = False
                        break
                    tot += k * ev(h, L / k)
                if ok and (best is None or tot > best):
                    best = tot
    return best


def pinned_ceiling_lo(a):
    """A budget (S') cannot fall below, whatever the true f: the certified LOWER
    bound f_lo in place of fhat.  Where area(T_a) is under this, (S') holds and
    refutes nothing -- so no bound proved from (S') can go below the largest such
    a.  That is this method's ceiling X1'."""
    ell = (a - 2) / 3
    if ell > 1:
        return None
    return 3 * (PI_LO_R / 6) + 9 * dn(f_lo(ell)) + 3 * (PI_LO_R / 4)


def unpinned_ceiling_lo(a):
    """Same for the unpinned lemma: the (4,4,4) branch, which is what
    attacks/n16-covering-limit/ calls decisive for its U2 (its X1)."""
    ell = (a - 2) / 4
    if ell > 1:
        return None
    return 3 * (PI_LO_R / 6) + 12 * dn(f_lo(ell))


# ---------------------------------------------------------------- bisection
def _bisect(pred, lo_i, hi_i):
    """Largest integer m in [lo_i, hi_i) with pred(m/GRAIN) true, +1.

    pred is anti-monotone: area increases in a and every budget here is
    non-increasing in a (the envelope is non-increasing, checked in envelope()),
    so once it fails it fails for all larger a -- which is what turns the
    bisection into a bound for every a above the answer."""
    assert pred(F(lo_i, GRAIN)), "bracket already refuted -- see B2"
    assert not pred(F(hi_i, GRAIN)), "no refutation at the top of the bracket"
    while hi_i - lo_i > 1:
        mid = (lo_i + hi_i) // 2
        if pred(F(mid, GRAIN)):
            lo_i = mid
        else:
            hi_i = mid
    return F(hi_i, GRAIN)


def largest_a(budget, tag=""):
    """Largest a (to 1e-7) not refuted by the budget: an upper bound on A_15."""
    def pred(a):
        b = budget(a)
        return b is not None and area_lo(a) <= b
    return _bisect(pred, int(TRIPWIRE_LO * GRAIN) + 1, 6 * GRAIN)


def largest_a_ceiling(budget):
    """Largest a at which the lemma provably CANNOT refute: its ceiling."""
    def pred(a):
        b = budget(a)
        return b is not None and area_hi(a) <= b
    return _bisect(pred, int(TRIPWIRE_LO * GRAIN) + 1, 6 * GRAIN) - F(1, GRAIN)


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 128
    D = int(sys.argv[2]) if len(sys.argv) > 2 else 48
    DF = int(sys.argv[3]) if len(sys.argv) > 3 else 192
    xs = nodes(D, DF, F(3, 4))
    print(f"certified f grid: N = {N} slabs, spacing 1/{D} on [0,3/4], "
          f"1/{DF} on [3/4,1]  ({len(xs)} nodes)")
    vals = f_grid(N, xs)
    h = envelope(xs, vals)
    print(f"  envelope vertices: "
          f"{[(round(float(x), 4), round(float(y), 6)) for x, y in h]}")
    print(f"  fhat(0.90) <= {float(ev(h, F(9,10))):.7f}   "
          f"fhat(0.95) <= {float(ev(h, F(95,100))):.7f}   "
          f"fhat(1.00) <= {float(ev(h, F(1))):.7f}")

    B_pin = largest_a(lambda a: pinned_hi(a, h), tag="pinned")
    B_unp = largest_a(lambda a: unpinned_hi(a, h), tag="unpinned")
    X_pin = largest_a_ceiling(pinned_ceiling_lo)
    X_unp = largest_a_ceiling(unpinned_ceiling_lo)

    rows = [
        ("B  pinned (3,3,3) budget, this lane        [NEW]", B_pin),
        ("U2' unpinned Lemma S, same f grid          [repro]", B_unp),
        ("X1' ceiling of the PINNED lemma            [NEW]", X_pin),
        ("X1  ceiling of the unpinned lemma          [repro]", X_unp),
    ]
    print()
    for name, a in rows:
        print(f"  {name:50s} a <= {float(a):.6f}")
    print(f"\n  comparison target (16-point packing, NOT an input) "
          f"{float(COMPARE):.7f}")
    print(f"  1 + 2 sqrt3 (certified 15-piece covering)          "
          f"{float(1 + 2 * SQRT3_LO_R):.7f}")

    # ---- kill-criterion tripwires, asserted rather than eyeballed
    for name, a in rows:
        assert a > TRIPWIRE_LO, f"B2 TRIPWIRE: {name} = {float(a)} <= 1+2sqrt3"
    assert B_pin >= X_pin, "B3 TRIPWIRE: pinned bound below the pinned ceiling"
    assert B_unp >= X_unp, "B3 TRIPWIRE: unpinned bound below the unpinned ceiling"
    assert B_pin <= B_unp, "pinning must not weaken the bound"
    print("\n  B2 tripwire (every bound > 1+2sqrt3): held")
    print("  B3 tripwire (bound >= its own ceiling): held")
    print(f"\n  gain from pinning, same f: {float(B_unp - B_pin):.6f}")
    ell = (B_pin - 2) / 3
    print(f"  operating point: l = (a-2)/3 = {float(ell):.6f}, "
          f"fhat(l) <= {float(ev(h, ell)):.7f}, f(l) >= {float(f_lo(ell)):.7f}")
    print(f"  published U2 = 4.914308;  beats it: "
          f"{'YES' if B_pin < F(4914308, 10**6) else 'NO'}")


if __name__ == "__main__":
    main()
