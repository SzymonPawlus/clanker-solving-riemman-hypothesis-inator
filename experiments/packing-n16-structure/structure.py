#!/usr/bin/env python3
"""The n=16 covering STRUCTURE THEOREM, and its exact check against the record.

Independent transcription of the 15-piece certificate from the TABLE PRINTED IN
problems/circle-packing-equilateral-triangle/attacks/n16-covering-2/README.md
(not from that lane's code), at a = 1 + 2*sqrt3.

CIRCULARITY GUARD.  No value of a_16, d(16), s(16), and no property of any
16-point packing, is an input to anything below.  The only quantity imported is
the record side a0 = 1 + 2*sqrt3, and it is used ONLY as the side at which to
test the structure theorem -- the theorem itself is proved for all a and is
stated in the write-up without reference to it.
"""
from fractions import Fraction as F
from q3 import Q3, q3, R, ZERO, ONE
from geom import ccw, covered, sqdiam, area2, sqdist

def P(pu, qu, pv, qv):        # (pu + qu*r,  pv + qv*r)
    return (Q3(pu, qu), Q3(pv, qv))

th = F(1, 3)                  # r/3 coefficient
A0 = Q3(1, 2)                 # a = 1 + 2 sqrt3

PIECES = [
    [P(0,0,0,0), P(1,0,0,0), P(0,th,0,th), P(0,0,1,0)],                                    # 0
    [P(0,th,1,th), P(0,0,0,1), P(0,0,1,0), P(0,th,0,th), P(1,0,1,0)],                      # 1
    [P(0,th,0,F(4,3)), P(0,0,1,1), P(0,0,0,1), P(0,th,1,th), P(1,0,0,1)],                  # 2
    [P(0,th,1,F(4,3)), P(0,0,0,2), P(0,0,1,1), P(0,th,0,F(4,3)), P(1,0,F(5,2),0)],         # 3
    [P(1,0,0,2), P(0,0,1,2), P(0,0,0,2), P(0,th,1,F(4,3))],                                # 4
    [P(1,0,0,0), P(0,1,0,0), P(1,th,0,th), P(1,0,1,0), P(0,th,0,th)],                      # 5
    [P(F(3,2),0,F(3,2),0), P(1,0,0,1), P(0,th,1,th), P(1,0,1,0), P(1,th,0,th), P(0,1,1,0)],# 6
    [P(1,th,0,F(4,3)), P(1,0,F(5,2),0), P(0,th,0,F(4,3)), P(1,0,0,1), P(F(3,2),0,F(3,2),0), P(0,1,0,1)], # 7
    [P(0,1,1,1), P(1,0,0,2), P(0,th,1,F(4,3)), P(1,0,F(5,2),0), P(1,th,0,F(4,3))],         # 8
    [P(0,1,0,0), P(1,1,0,0), P(0,F(4,3),0,th), P(0,1,1,0), P(1,th,0,th)],                  # 9
    [P(0,F(4,3),1,th), P(0,1,0,1), P(F(3,2),0,F(3,2),0), P(0,1,1,0), P(0,F(4,3),0,th), P(F(5,2),0,1,0)], # 10
    [P(1,1,0,1), P(0,1,1,1), P(1,th,0,F(4,3)), P(0,1,0,1), P(0,F(4,3),1,th)],              # 11
    [P(1,1,0,0), P(0,2,0,0), P(1,F(4,3),0,th), P(F(5,2),0,1,0), P(0,F(4,3),0,th)],         # 12
    [P(0,2,1,0), P(1,1,0,1), P(0,F(4,3),1,th), P(F(5,2),0,1,0), P(1,F(4,3),0,th)],         # 13
    [P(0,2,0,0), P(1,2,0,0), P(0,2,1,0), P(1,F(4,3),0,th)],                                # 14
]

# ---- the three sides of T_a in the chart: v = 0, u = 0, u + v = a -------------
def meets(poly, side, a):
    if side == "v=0":   return any(p[1] == 0 for p in poly)
    if side == "u=0":   return any(p[0] == 0 for p in poly)
    if side == "u+v=a": return any((p[0] + p[1]) == a for p in poly)
    raise ValueError(side)

def contained(poly, a):
    return all(p[0] >= 0 and p[1] >= 0 and (p[0] + p[1]) <= a for p in poly)

def report(a, pieces):
    print(f"a = {a}  ~ {a.approx():.12f}")
    sides = ["v=0", "u=0", "u+v=a"]
    cls = {0: [], 1: [], 2: [], 3: []}
    per_side = {s: 0 for s in sides}
    ok_contain, maxd = True, ZERO
    for i, poly in enumerate(pieces):
        ok_contain &= contained(poly, a)
        d = sqdiam(poly)
        if d > maxd: maxd = d
        met = [s for s in sides if meets(poly, s, a)]
        for s in met: per_side[s] += 1
        cls[len(met)].append(i)
    print(f"  all 15 pieces inside T_a: {ok_contain}")
    print(f"  max squared diameter over all pieces: {maxd}  (== 1: {maxd == 1})")
    print(f"  pieces meeting 2 sides (corner):   {len(cls[2])}  {cls[2]}")
    print(f"  pieces meeting 1 side  (edge):     {len(cls[1])}  {cls[1]}")
    print(f"  pieces meeting 0 sides (deep):     {len(cls[0])}  {cls[0]}")
    print(f"  pieces meeting 3 sides:            {len(cls[3])}")
    for s in sides:
        print(f"  pieces meeting side {s:8s}: {per_side[s]}")

    # --- the deep triangle D: distance >= 1 from all three sides ---------------
    # distance to v=0 is v*sqrt3/2, so v*sqrt3/2 >= 1  <=>  v >= 2/sqrt3 = 2r/3.
    h = Q3(0, F(2, 3))                       # 2/sqrt3 = 2r/3
    delta = a - 2 * R                        # side of D
    Dtri = [(h, h), (h + delta, h), (h, h + delta)]
    print(f"  deep triangle D has side delta = a - 2*sqrt3 = {delta} ~ {delta.approx():.12f}")
    print(f"    delta >= 1 ? {delta >= 1}   -> D's three corners are pairwise >= 1 apart")
    for (x, y) in [(0,1),(0,2),(1,2)]:
        assert sqdist(Dtri[x], Dtri[y]) == delta * delta
    deep = [pieces[i] for i in cls[0]]
    ok, res = covered(Dtri, deep)
    print(f"    D covered by the {len(deep)} deep pieces alone: {ok}"
          + ("" if ok else f"  (residue parts: {len(res)})"))
    # control: does any SINGLE deep piece cover D?  (must be False for delta>=1)
    singles = [covered(Dtri, [p])[0] for p in deep]
    print(f"    covered by any single deep piece: {any(singles)}  (must be False)")

    # --- corner reach: two-side pieces have both footpoints < 2/sqrt3 from the apex
    print("  two-side piece footpoint distances from their apex (must be < 2/sqrt3 = "
          f"{Q3(0,F(2,3)).approx():.9f}):")
    for i in cls[2]:
        poly = pieces[i]
        for (name, sel) in (("v=0", lambda p: p[1] == 0 and p[0] <= a),
                            ("u=0", lambda p: p[0] == 0),
                            ("u+v=a", lambda p: (p[0] + p[1]) == a)):
            pts = [p for p in poly if sel(p)]
            if len(pts) >= 2:
                dd = max(sqdist(x, y) for x in pts for y in pts)
                print(f"    piece {i:2d} trace on {name:6s}: squared length {dd}"
                      f" ~ {dd.approx():.9f}  (< 4/3: {dd < F(4,3)})")

if __name__ == "__main__":
    report(A0, [ccw(p) for p in PIECES])


# ---------------------------------------------------------------------------
# The theorem's arithmetic, as a function of a.  Exact throughout.
#
#   two-side pieces  >= 3            (the three apexes lie in distinct pieces)
#   one-side pieces  >= 3 * ceil(a - 4/sqrt3)   (the three side middles)
#   zero-side pieces >= 3            as soon as delta = a - 2 sqrt3 >= 1
#
# and the three classes are disjoint, so these add.
# ---------------------------------------------------------------------------
def floor_q3(x):
    """Greatest integer <= x, decided exactly."""
    n = int(x.approx()) - 2
    while Q3(n + 1) <= x:
        n += 1
    return n


def min_intervals(L):
    """Fewest intervals of length STRICTLY < 1 needed to cover a closed segment
    of length L.  Their lengths sum to > L, so the count is floor(L) + 1 --
    note this is floor+1, not ceil: at integer L, ceil would be one too few."""
    return floor_q3(L) + 1


def forced_counts(a):
    corner = 3
    L = a - Q3(0, F(4, 3))                 # 4/sqrt3 = 4r/3 ; middle length per side
    per_side = min_intervals(L) if L > 0 else 0
    edge = 3 * per_side
    delta = a - 2 * R
    deep = 3 if delta >= 1 else (1 if delta > 0 else 0)
    # D's three corners together with its centroid are 4 points at pairwise
    # distance >= min(delta, delta/sqrt3) = delta/sqrt3, so delta >= sqrt3
    # forces a 4th deep piece.  (Only the LOWER bound is used; nothing here
    # depends on delta/sqrt3 being the optimal 3-partition of T_delta.)
    if delta >= R:
        deep = 4
    return corner, edge, deep, corner + edge + deep, delta


def thresholds():
    print("\nforced piece counts as a function of a  (exact; corner / edge / deep / total)")
    print(f"{'a':>28} {'~':>10} {'corner':>7}{'edge':>6}{'deep':>6}{'total':>7}   delta = a-2sqrt3")
    cases = [
        ("2sqrt3",              2 * R),
        ("4.30",                Q3(F(43, 10))),
        ("3+4/sqrt3-1 (4.309)", Q3(3) + Q3(0, F(4, 3)) - 1),
        ("1+2sqrt3 - 1/100",    Q3(F(-1, 100), 0) + Q3(1, 2)),
        ("1+2sqrt3  (RECORD)",  Q3(1, 2)),
        ("1+2sqrt3 + 1/100",    Q3(F(1, 100), 0) + Q3(1, 2)),
        ("4.62 (near best pack)", Q3(F(462, 100))),
        ("5",                   Q3(5)),
        ("3sqrt3 (5.196)",      3 * R),
        ("3+4/sqrt3 (5.309)",   Q3(3) + Q3(0, F(4, 3))),
        ("5.4",                 Q3(F(27, 5))),
    ]
    for name, a in cases:
        c, e, d, t, delta = forced_counts(a)
        star = "   <-- 15 first forced here" if name.endswith("(RECORD)") else ""
        print(f"{name:>28} {a.approx():10.6f} {c:7d}{e:6d}{d:6d}{t:7d}   {delta.approx():+.6f}{star}")


if __name__ == "__main__":
    thresholds()


# ---------------------------------------------------------------------------
# Does feeding Theorem N's FORCED class counts into an area budget sharpen the
# ceiling on A_15?  Answer: no -- it reproduces n16-covering-limit's U1 exactly.
# Floats here are a DIAGNOSTIC ONLY: this routine decides nothing, it reports a
# comparison against another lane's published figures (see README 5.1).
# ---------------------------------------------------------------------------
def area_budget():
    import math
    r3 = math.sqrt(3)
    def area(a):
        return r3 / 4 * a * a

    def slice_bound(l):
        return math.pi / 2 - math.asin(l / 2) - (l / 2) * math.sqrt(1 - l * l / 4)

    def budget(a, use_slice):
        l = (a - 4 / r3) / 3               # Theorem N's middle over 3 forced edge pieces
        fe = min(math.pi / 4, slice_bound(l)) if use_slice else math.pi / 4
        return 3 * (math.pi / 6) + 9 * fe + 3 * (math.pi / 4)

    print("\narea budget on Theorem N's forced 3/9/3 classes (diagnostic, floats):")
    for label, use_slice in (("isodiametric only", False), ("+ slice bound on edges", True)):
        lo, hi = 4.0, 7.0
        for _ in range(200):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if area(mid) <= budget(mid, use_slice) else (lo, mid)
        print(f"  {label:24s}: A_15 <= {lo:.6f}")
    print("  n16-covering-limit published U1 = 5.039166, U2 = 4.914308")
    print("  -> row 1 reproduces U1 to 6 dp: the forced counts were already assumed there.")


if __name__ == "__main__":
    area_budget()
