"""Independent exact checker, written from problems/circle-packing-equilateral-triangle/README.md
and RULES.md sec 2, NOT by reading r3-qsqrt3/check.py or r4-famcert/check.py.

Conventions (RULES.md sec 2, fixed, no search over rigid motions):
  d = s - 2*sqrt(3);  A=(0,0), B=(d,0), C=(d/2, d*sqrt(3)/2)
  closed triangle; pairwise distances >= 2 (squared >= 4)

Wall functionals (>= 0 inside, = 0 on the edge, scaled to true distance):
  w_AB(p) = y
  w_AC(p) = (sqrt(3)*x - y)/2
  w_BC(p) = (sqrt(3)*(d - x) - y)/2
Only w_BC depends on d, and w_BC >= 0  <=>  d >= x + y*sqrt(3)/3.
So the exact minimal enclosing side is  d_min = max_i (x_i + y_i*sqrt(3)/3),
valid iff every point satisfies w_AB >= 0 and w_AC >= 0.
"""
from fractions import Fraction as F
from q3 import Q3, ZERO, R3

HALF = Q3(F(1, 2), 0)
R3_OVER_3 = Q3(0, F(1, 3))


def sqdist(p, q):
    dx = p[0] - q[0]
    dy = p[1] - q[1]
    return dx * dx + dy * dy


def walls(p, d):
    x, y = p
    return {
        "AB": y,
        "AC": (R3 * x - y) * HALF,
        "BC": (R3 * (d - x) - y) * HALF,
    }


def d_min_of(pts):
    """Exact minimal enclosing d for this fixed placement (assumes AB/AC hold)."""
    best = None
    for (x, y) in pts:
        v = x + y * R3_OVER_3
        if best is None or v > best:
            best = v
    return best


def check(pts, s, n_declared=None):
    d = s - Q3(0, 2)          # d = s - 2*sqrt(3)
    n = len(pts)
    rep = {"n": n, "s": s.sexpr(), "d": d.sexpr(), "failures": []}
    if n_declared is not None and n_declared != n:
        rep["failures"].append("n mismatch: declared %d, got %d" % (n_declared, n))

    # --- pairwise ---
    minsq = None
    contacts = []
    for i in range(n):
        for j in range(i + 1, n):
            sq = sqdist(pts[i], pts[j])
            if minsq is None or sq < minsq:
                minsq = sq
            if sq < Q3(4, 0):
                rep["failures"].append("pair (%d,%d) sq dist %s < 4" % (i, j, sq.sexpr()))
            if sq == Q3(4, 0):
                contacts.append((i, j))
    rep["pairs_checked"] = n * (n - 1) // 2
    rep["min_sq_distance"] = minsq.sexpr() if minsq else None
    rep["min_sq_distance_is_exactly_4"] = (minsq == Q3(4, 0))
    rep["contacts"] = contacts
    rep["n_contacts"] = len(contacts)

    # --- containment ---
    boundary = []
    for i, p in enumerate(pts):
        w = walls(p, d)
        on = [k for k, v in w.items() if v.is_zero()]
        for k, v in w.items():
            if v.sign() < 0:
                rep["failures"].append("point %d outside wall %s by %s" % (i, k, v.sexpr()))
        if on:
            boundary.append((i, tuple(sorted(on))))
    rep["boundary"] = boundary
    rep["n_boundary"] = len(boundary)

    # --- tightness ---
    dm = d_min_of(pts)
    rep["d_min"] = dm.sexpr()
    rep["tight"] = (dm == d)
    rep["s_min"] = (dm + Q3(0, 2)).sexpr()

    # --- degree of each point in the contact graph + wall contacts ---
    deg = [0] * n
    for (i, j) in contacts:
        deg[i] += 1
        deg[j] += 1
    rep["contact_degree"] = deg
    rep["ok"] = not rep["failures"]
    return rep


def free_radius_bracket(pts, i, d, tol=F(1, 10 ** 12)):
    """Exact rational bracket [lo, hi] on the largest r such that moving point i
    by any vector of length <= r keeps the packing feasible.
    r feasible  <=>  for all j: sqdist(i,j) >= (2+r)^2  and  for all walls: w >= r.
    All comparisons exact in Q(sqrt 3) with rational r."""
    def ok(r):
        rr = Q3(r, 0)
        two_r = Q3(2, 0) + rr
        for j, q in enumerate(pts):
            if j == i:
                continue
            if sqdist(pts[i], q) < two_r * two_r:
                return False
        for v in walls(pts[i], d).values():
            if v < rr:
                return False
        return True

    if not ok(F(0)):
        return (F(0), F(0))
    lo, hi = F(0), F(1)
    while ok(hi):
        hi *= 2
        if hi > 100:
            break
    while hi - lo > tol:
        mid = (lo + hi) / 2
        if ok(mid):
            lo = mid
        else:
            hi = mid
    return (lo, hi)


def rattlers(pts, s):
    """A point is a rattler iff it has NO contact at distance exactly 2 and is
    strictly interior to all three walls (RULES.md sense: free to move)."""
    d = s - Q3(0, 2)
    n = len(pts)
    out = []
    for i in range(n):
        has_contact = any(sqdist(pts[i], pts[j]) == Q3(4, 0) for j in range(n) if j != i)
        w = walls(pts[i], d)
        strict = all(v.sign() > 0 for v in w.values())
        if (not has_contact) and strict:
            lo, hi = free_radius_bracket(pts, i, d)
            out.append({"index": i, "point": (pts[i][0].sexpr(), pts[i][1].sexpr()),
                        "free_radius_lo": str(lo), "free_radius_hi": str(hi),
                        "min_nbr_sqdist": min(sqdist(pts[i], pts[j])
                                              for j in range(n) if j != i).sexpr(),
                        "min_wall": min(w.values()).sexpr()})
    return out
