"""Exact feasibility + tightness checker for a Q(sqrt 3) packing certificate.

CONSTRUCTION (upper bound) checker.  It certifies s(n) <= s for the given
configuration.  It says nothing whatever about optimality.

Every arithmetic step is exact in Q(sqrt 3) (see qsqrt3.py); no float is
consulted in any accept/reject decision.

Checks performed, per problems/circle-packing-equilateral-triangle/RULES.md §2:
  1. all C(n,2) squared pairwise distances >= 4      (non-strict)
  2. all n points in the CLOSED triangle A=(0,0), B=(d,0), C=(d/2, d*sqrt3/2)
  3. TIGHTNESS: the exact minimal enclosing side d_min for this point set in
     this fixed placement, and whether d_min == d.
"""
from qsqrt3 import Q3, q3


def sq_dist(p, q):
    dx = p[0] - q[0]
    dy = p[1] - q[1]
    return dx * dx + dy * dy


def containment_slacks(pt, d):
    """Exact slacks for the three closed half-planes; all must be >= 0.

    AB : y >= 0
    AC : the line through (0,0) and (d/2, d*sqrt3/2) is y = sqrt(3) x,
         interior is y <= sqrt(3) x, so slack = sqrt(3)*x - y
    BC : the line through (d,0) and (d/2, d*sqrt3/2) is y = sqrt(3)(d - x),
         interior is y <= sqrt(3)(d - x), so slack = sqrt(3)*(d - x) - y
    """
    x, y = pt
    r = Q3(0, 1)
    return (y, r * x - y, r * (d - x) - y)


def min_enclosing_d(pts):
    """Exact least d such that every point lies in the closed triangle
    A=(0,0), B=(d,0), C=(d/2, d*sqrt3/2), in THIS fixed placement.

    y >= 0 and sqrt(3)x - y >= 0 do not involve d, so they are pass/fail.
    sqrt(3)(d - x) - y >= 0  <=>  d >= x + y/sqrt(3) = x + y*sqrt(3)/3.
    Hence d_min = max_i (x_i + y_i*sqrt(3)/3), also >= 0.
    """
    r3over3 = Q3(0, q3(1).a / 3)   # sqrt(3)/3
    best = Q3(0, 0)
    for (x, y) in pts:
        v = x + r3over3 * y
        if v > best:
            best = v
    return best


def check(n, d, pts, verbose=True):
    report = {"n": n, "ok": True, "failures": []}
    assert len(pts) == n, "expected %d points, got %d" % (n, len(pts))

    # 1. separations
    worst = None
    for i in range(n):
        for j in range(i + 1, n):
            s2 = sq_dist(pts[i], pts[j])
            if s2 < q3(4):
                report["ok"] = False
                report["failures"].append(("separation", i, j, s2.sexpr()))
            if worst is None or s2 < worst[0]:
                worst = (s2, i, j)
    report["min_sq_distance"] = worst[0].sexpr()
    report["min_sq_distance_pair"] = (worst[1], worst[2])
    report["min_sq_distance_is_exactly_4"] = (worst[0] == q3(4))
    report["n_contacts"] = sum(
        1 for i in range(n) for j in range(i + 1, n) if sq_dist(pts[i], pts[j]) == q3(4)
    )

    # 2. containment
    for i, p in enumerate(pts):
        for name, sl in zip(("AB", "AC", "BC"), containment_slacks(p, d)):
            if sl < q3(0):
                report["ok"] = False
                report["failures"].append(("containment", i, name, sl.sexpr()))
    report["n_on_boundary"] = sum(
        1 for p in pts if any(sl == q3(0) for sl in containment_slacks(p, d))
    )

    # 3. tightness
    dmin = min_enclosing_d(pts)
    report["d_min_exact"] = dmin.sexpr()
    report["d_declared"] = d.sexpr()
    report["tight"] = (dmin == d) and report["ok"]
    if dmin > d:
        report["ok"] = False
        report["failures"].append(("tightness", "d_min > d", dmin.sexpr()))

    report["s_exact"] = (d + Q3(0, 2)).sexpr()

    if verbose:
        import json
        print(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    import sys, json
    import configs
    ns = [int(a) for a in sys.argv[1:]] or [17, 24, 31]
    rc = 0
    for n in ns:
        pts = getattr(configs, "P%d" % n)
        d = getattr(configs, "D%d" % n)
        if pts is None:
            print("n = %d: no configuration on file, skipped" % n)
            continue
        print("=" * 60)
        r = check(n, d, pts)
        if not r["ok"]:
            rc = 1
    sys.exit(rc)
