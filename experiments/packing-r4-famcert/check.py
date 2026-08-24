"""Exact feasibility + containment + TIGHTNESS checker, Q(sqrt 3), stdlib only.

CONSTRUCTION (upper bound) checker.  It certifies s(n) <= s for the point set it
is given.  It says NOTHING about optimality.

Conventions are taken from problems/circle-packing-equilateral-triangle/RULES.md §2
and README.md and are re-derived in comments here rather than imported:

  point formulation: n points, pairwise distance >= 2, in the CLOSED equilateral
  triangle A=(0,0), B=(d,0), C=(d/2, d*sqrt(3)/2), and s = d + 2*sqrt(3).
  `side_length` in a certificate is s, never d.  All inequalities non-strict.

  half planes (signs fixed by the centroid (d/2, d*sqrt(3)/6)):
     AB :  y >= 0
     AC :  line through (0,0),(d/2,d sqrt3/2) is y = sqrt(3) x, interior y <= sqrt3 x
     BC :  line through (d,0),(d/2,d sqrt3/2) is y = sqrt(3)(d - x), interior y <= that
  d enters only through BC, and  sqrt3(d-x) - y >= 0  <=>  d >= x + y/sqrt3.
  Hence the exact minimal enclosing side in this FIXED placement is
     d_min = max_i ( x_i + y_i*sqrt(3)/3 ),   provided AB and AC already hold.

Every arithmetic step is exact.  No float is consulted in any accept/reject
decision anywhere in this file.
"""
from fractions import Fraction as F
from qsqrt3 import Q3, q3

R3 = Q3(0, 1)
R3_OVER_3 = Q3(0, F(1, 3))
FOUR = q3(4)


def sq_dist(p, r):
    dx = p[0] - r[0]
    dy = p[1] - r[1]
    return dx * dx + dy * dy


def slacks(pt, d):
    x, y = pt
    return (y, R3 * x - y, R3 * (d - x) - y)


def min_enclosing_d(pts):
    best = q3(0)
    for (x, y) in pts:
        v = x + R3_OVER_3 * y
        if v > best:
            best = v
    return best


def check(n, s, pts):
    """s is the declared SIDE LENGTH (of the circle problem); d = s - 2 sqrt3."""
    d = s - Q3(0, 2)
    rep = {"n": n, "s_declared": s.sexpr(), "d_declared": d.sexpr(),
           "ok": True, "failures": []}
    if len(pts) != n:
        rep["ok"] = False
        rep["failures"].append(("count", len(pts), n))
        return rep

    # distinctness (a repeated point would pass a >= check on 0 pairs only if
    # sq_dist were mis-signed; check it explicitly)
    if len(set((p[0], p[1]) for p in pts)) != n:
        rep["ok"] = False
        rep["failures"].append(("duplicate points",))

    worst = None
    contacts = 0
    npairs = 0
    for i in range(n):
        for k in range(i + 1, n):
            npairs += 1
            s2 = sq_dist(pts[i], pts[k])
            if s2 < FOUR:
                rep["ok"] = False
                rep["failures"].append(("separation", i, k, s2.sexpr()))
            if s2 == FOUR:
                contacts += 1
            if worst is None or s2 < worst[0]:
                worst = (s2, i, k)
    rep["pairs_checked"] = npairs
    rep["min_sq_distance"] = worst[0].sexpr()
    rep["min_sq_distance_is_exactly_4"] = (worst[0] == FOUR)
    rep["contacts_at_distance_exactly_2"] = contacts

    onb = 0
    for i, p in enumerate(pts):
        sl = slacks(p, d)
        for name, v in zip(("AB", "AC", "BC"), sl):
            if v < q3(0):
                rep["ok"] = False
                rep["failures"].append(("containment", i, name, v.sexpr()))
        if any(v == q3(0) for v in sl):
            onb += 1
    rep["points_on_boundary"] = onb

    dmin = min_enclosing_d(pts)
    rep["d_min_exact"] = dmin.sexpr()
    rep["s_min_exact"] = (dmin + Q3(0, 2)).sexpr()
    if dmin > d:
        rep["ok"] = False
        rep["failures"].append(("tightness", "d_min > d", dmin.sexpr()))
    rep["tight"] = rep["ok"] and (dmin == d)
    return rep


if __name__ == "__main__":
    import sys, json
    from parse import load_certificate
    rc = 0
    for path in sys.argv[1:]:
        cert, pts, s, d = load_certificate(path)
        r = check(cert["n"], s, pts)
        print(path)
        print(json.dumps(r, indent=2))
        if not r["ok"]:
            rc = 1
    sys.exit(rc)
