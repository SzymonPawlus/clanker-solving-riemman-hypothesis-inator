"""Exact arithmetic in Q(sqrt3), in the triangular-lattice basis.

PROVENANCE: copied verbatim from experiments/packing-eo-covering/exact.py
(author: claude / W1 "Constructor", 2026-08-21, attack eo-covering-construct),
then MODIFIED here by claude / N1, 2026-08-22:

  * verify() now demands  diam^2 < 1  STRICTLY  (was <= 1).  The problem's
    RULES.md §2 fixes separation as NON-strict, so a closed set of diameter
    exactly 1 may legitimately contain two separated points and the pigeonhole
    step fails.  Every piece of every certificate here has squared diameter
    exactly checked to be < 1.
  * added verify_strict / a_max_exact helpers.

Basis:  e1 = (1,0),  e2 = (1/2, sqrt3/2).  A point is (u,v) = u*e1 + v*e2.
Then  |u*e1 + v*e2|^2 = u^2 + u*v + v^2  -- a RATIONAL quadratic form, so no
square roots enter distance computations at all.  T_a = {u>=0, v>=0, u+v<=a}
has corners (0,0), (a,0), (a/2, a*sqrt3/2) in the plane, which is exactly the
convention fixed by problems/circle-packing-equilateral-triangle/RULES.md.

Coordinates themselves are allowed to live in Q(sqrt3) because the good
hexagonal schemes use spacing sqrt3/2.  NO FLOATS ANYWHERE IN THIS FILE.
"""
from fractions import Fraction as F

class Q3:
    """a + b*sqrt(3), a,b rational.  Exact field arithmetic + exact sign."""
    __slots__ = ("a", "b")
    def __init__(self, a=0, b=0):
        self.a = F(a); self.b = F(b)
    def __add__(s, o):
        o = q3(o); return Q3(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __neg__(s): return Q3(-s.a, -s.b)
    def __sub__(s, o): return s + (-q3(o))
    def __rsub__(s, o): return q3(o) + (-s)
    def __mul__(s, o):
        o = q3(o); return Q3(s.a*o.a + 3*s.b*o.b, s.a*o.b + s.b*o.a)
    __rmul__ = __mul__
    def inv(s):
        d = s.a*s.a - 3*s.b*s.b
        if d == 0: raise ZeroDivisionError
        return Q3(s.a/d, -s.b/d)
    def __truediv__(s, o): return s * q3(o).inv()
    def __rtruediv__(s, o): return q3(o) * s.inv()
    def sign(s):
        a, b = s.a, s.b
        if a == 0: return (0 if b == 0 else (1 if b > 0 else -1))
        if b == 0: return 1 if a > 0 else -1
        if a > 0 and b > 0: return 1
        if a < 0 and b < 0: return -1
        # opposite signs: compare a^2 with 3 b^2
        c = a*a - 3*b*b
        if c == 0: return 0
        return (1 if a > 0 else -1) if c > 0 else (-1 if a > 0 else 1)
    def __eq__(s, o): return (s - q3(o)).sign() == 0
    def __lt__(s, o): return (s - q3(o)).sign() < 0
    def __le__(s, o): return (s - q3(o)).sign() <= 0
    def __gt__(s, o): return (s - q3(o)).sign() > 0
    def __ge__(s, o): return (s - q3(o)).sign() >= 0
    def __hash__(s): return hash((s.a, s.b))
    def __repr__(s):
        if s.b == 0: return str(s.a)
        return "%s%+s*sqrt3" % (s.a, s.b)
    def approx(s): return float(s.a) + float(s.b) * 1.7320508075688772

def q3(x):
    if isinstance(x, Q3): return x
    return Q3(x, 0)

SQ3 = Q3(0, 1)
HALF_SQ3 = Q3(0, F(1, 2))

# ---------- geometry in the (u,v) basis ----------

def qform(du, dv):
    """squared euclidean length of du*e1 + dv*e2"""
    return du*du + du*dv + dv*dv

def dist2(p, q):
    return qform(p[0]-q[0], p[1]-q[1])

def bilin(p, q):
    """<p,q> in the e1,e2 basis: u1u2 + (u1v2+v1u2)/2 + v1v2"""
    return p[0]*q[0] + (p[0]*q[1] + p[1]*q[0]) * F(1, 2) + p[1]*q[1]

def cross(o, a, b):
    """2*signed area of (o,a,b) in (u,v) coords (same sign as in the plane)"""
    return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])

def shoelace2(poly):
    s = q3(0)
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]; x2, y2 = poly[(i+1) % n]
        s = s + (x1*y2 - x2*y1)
    return s          # = 2 * (uv-area); true area = (sqrt3/4) * s

def clip_halfplane(poly, n0, n1, c):
    """keep {(u,v): n0*u + n1*v <= c}; poly convex, ccw, exact"""
    out = []
    m = len(poly)
    for i in range(m):
        p = poly[i]; q = poly[(i+1) % m]
        dp = n0*p[0] + n1*p[1] - c
        dq = n0*q[0] + n1*q[1] - c
        sp = dp.sign(); sq = dq.sign()
        if sp <= 0: out.append(p)
        if (sp > 0) != (sq > 0):
            t = dp / (dp - dq)
            out.append((p[0] + t*(q[0]-p[0]), p[1] + t*(q[1]-p[1])))
    # drop duplicate consecutive vertices
    res = []
    for p in out:
        if not res or not (res[-1][0] == p[0] and res[-1][1] == p[1]):
            res.append(p)
    if len(res) > 1 and res[0][0] == res[-1][0] and res[0][1] == res[-1][1]:
        res.pop()
    return res

def triangle(a):
    a = q3(a)
    return [(q3(0), q3(0)), (a, q3(0)), (q3(0), a)]

def diam2(poly):
    d = q3(0)
    for i in range(len(poly)):
        for j in range(i+1, len(poly)):
            v = dist2(poly[i], poly[j])
            if v > d: d = v
    return d

def bisector_halfplane(p, q):
    """{x : |x-p|^2 <= |x-q|^2} as (n0, n1, c) with n0*u + n1*v <= c"""
    # |x|^2 - 2<x,p> + |p|^2 <= |x|^2 - 2<x,q> + |q|^2
    # 2<x, q-p> <= |q|^2 - |p|^2
    d = (q[0]-p[0], q[1]-p[1])
    n0 = 2*bilin((q3(1), q3(0)), d)
    n1 = 2*bilin((q3(0), q3(1)), d)
    c = qform(q[0], q[1]) - qform(p[0], p[1])
    return n0, n1, c

def voronoi_cells(sites, a):
    tri = triangle(a)
    cells = []
    for i, p in enumerate(sites):
        poly = tri
        for j, q in enumerate(sites):
            if i == j: continue
            n0, n1, c = bisector_halfplane(p, q)
            poly = clip_halfplane(poly, n0, n1, c)
            if len(poly) < 3: break
        cells.append(poly if len(poly) >= 3 else [])
    return cells

def separated(A, B):
    """exact separating-axis test for two convex polygons: interiors disjoint?"""
    for P, Q in ((A, B), (B, A)):
        m = len(P)
        for i in range(m):
            p = P[i]; q = P[(i+1) % m]
            # outward normal test: all of Q on the far side of edge pq
            ok = True
            for r in Q:
                if cross(p, q, r).sign() > 0:
                    ok = False; break
            if ok:
                return True
    return False

def _rep(report, msg):
    if report: print(msg)

def verify(cells, a, verbose=True, check_disjoint=True, report=True):
    """Full exact check that `cells` is a partition of T_a into diameter<=1 sets."""
    a = q3(a)
    ok = True
    tri = triangle(a)
    # 1. containment + convexity + orientation
    for k, P in enumerate(cells):
        if len(P) < 3:
            _rep(report, "FAIL cell %d degenerate" % k); ok = False; continue
        for (u, v) in P:
            if u.sign() < 0 or v.sign() < 0 or (u+v) > a:
                _rep(report, "FAIL cell %d vertex outside T_a" % k); ok = False
        m = len(P)
        for i in range(m):
            if cross(P[i], P[(i+1) % m], P[(i+2) % m]).sign() < 0:
                _rep(report, "FAIL cell %d not convex/ccw at %d" % (k, i)); ok = False
    # 2. diameters
    worst = q3(0); wk = -1
    for k, P in enumerate(cells):
        d = diam2(P)
        if d > worst: worst, wk = d, k
        if d >= q3(1):
            _rep(report, "FAIL cell %d has diam^2 = %s >= 1 (STRICT test)" % (k, d)); ok = False
    # 3. areas
    tot = q3(0)
    for P in cells:
        s = shoelace2(P)
        if s.sign() < 0: s = -s
        tot = tot + s
    target = shoelace2(tri)
    if not (tot == target):
        _rep(report, "FAIL area sum %s != %s" % (tot, target)); ok = False
    # 4. pairwise disjoint interiors
    if check_disjoint:
        for i in range(len(cells)):
            for j in range(i+1, len(cells)):
                if not separated(cells[i], cells[j]):
                    _rep(report, "FAIL cells %d,%d overlap" % (i, j)); ok = False
    if verbose:
        print("cells                : %d" % len(cells))
        print("max squared diameter : %s  (~%.12f)  cell %d" % (worst, worst.approx(), wk))
        print("max diameter         : ~%.12f" % (worst.approx() ** 0.5))
        print("area sum == area T_a : %s" % (tot == target))
        print("all diam^2  < 1      : %s" % all(diam2(P) < q3(1) for P in cells))
        print("VERDICT              : %s" % ("PASS" if ok else "FAIL"))
    return ok, worst

def power_halfplane(p, wp, q, wq):
    """{x : |x-p|^2 - wp <= |x-q|^2 - wq}  ->  (n0,n1,c) with n0*u+n1*v <= c"""
    d = (q[0]-p[0], q[1]-p[1])
    n0 = 2*bilin((q3(1), q3(0)), d)
    n1 = 2*bilin((q3(0), q3(1)), d)
    c = qform(q[0], q[1]) - qform(p[0], p[1]) - q3(wq) + q3(wp)
    return n0, n1, c

def power_cells_exact(sites, weights, a):
    tri = triangle(a)
    cells = []
    for i, p in enumerate(sites):
        poly = tri
        for j, r in enumerate(sites):
            if i == j: continue
            n0, n1, c = power_halfplane(p, weights[i], r, weights[j])
            poly = clip_halfplane(poly, n0, n1, c)
            if len(poly) < 3: break
        cells.append(poly if len(poly) >= 3 else [])
    return cells
