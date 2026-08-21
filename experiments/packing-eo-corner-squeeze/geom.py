"""Exact geometry of corner-coordinate regions in an equilateral triangle.

Corner coordinates.  T has corners A, B, C and side a.  For p in T let u_V(p) be
normalised so that {u_V <= t} is the closed corner triangle at V of side t.  Then
u_A + u_B + u_C = 2a (Viviani), each u_V in [0, a], and in Euclidean coordinates
with A = (0,0), B = (a,0), C = (a/2, a*sqrt3/2):

    u_A = x + y/sqrt3,   u_B = (a-x) + y/sqrt3,   u_C = a - 2y/sqrt3,
    x   = (a + u_A - u_B)/2,   y = sqrt3 * r  with  r = (u_A + u_B - a)/2.

Because y is sqrt3 times a rational, the shoelace area of a rational polygon is
sqrt3 times a rational, so Oler's area term (2/sqrt3)*A is EXACTLY RATIONAL.
Only edge lengths leave Q; those are rational intervals with outward rounding.

A region is a list of closed half-planes (c1, c2, c0) meaning c1*uA + c2*uB <= c0.
"""

from fractions import Fraction as F
from exactiv import Ival

# ---------------------------------------------------------------- half-planes


def tri_constraints(a):
    """The triangle T itself, in (uA, uB)."""
    return [(F(1), F(0), F(a)), (F(0), F(1), F(a)), (F(-1), F(-1), F(-a))]


def bound_constraints(a, corner, lo, hi):
    """lo <= u_corner <= hi, as half-planes in (uA, uB).  hi=None means no cap."""
    a = F(a)
    out = []
    if corner == 0:      # u_A
        out.append((F(-1), F(0), F(-lo)))
        if hi is not None:
            out.append((F(1), F(0), F(hi)))
    elif corner == 1:    # u_B
        out.append((F(0), F(-1), F(-lo)))
        if hi is not None:
            out.append((F(0), F(1), F(hi)))
    else:                # u_C = 2a - uA - uB
        out.append((F(1), F(1), 2 * a - F(lo)))
        if hi is not None:
            out.append((F(-1), F(-1), -(2 * a - F(hi))))
    return out


# ---------------------------------------------------------------- vertices


def vertices(cons):
    """Exact vertex set of the polyhedron {c1 uA + c2 uB <= c0}, assumed bounded."""
    pts = []
    m = len(cons)
    for i in range(m):
        a1, b1, c1 = cons[i]
        for j in range(i + 1, m):
            a2, b2, c2 = cons[j]
            det = a1 * b2 - a2 * b1
            if det == 0:
                continue
            x = (c1 * b2 - c2 * b1) / det
            y = (a1 * c2 - a2 * c1) / det
            if all(p * x + q * y <= c for (p, q, c) in cons):
                if (x, y) not in pts:
                    pts.append((x, y))
    return pts


def order_ccw(pts):
    if len(pts) <= 2:
        return list(pts)
    cx = sum(p[0] for p in pts) / len(pts)
    cy = sum(p[1] for p in pts) / len(pts)

    def key(p):
        dx, dy = p[0] - cx, p[1] - cy
        # exact angular sort by half-plane + cross product
        half = 0 if (dy > 0 or (dy == 0 and dx > 0)) else 1
        return (half, dx, dy)

    rest = sorted(pts, key=lambda p: (key(p)[0],))
    # full exact angular sort via cross-product comparison
    import functools

    def cmp(p, q):
        hp = 0 if (p[1] - cy > 0 or (p[1] - cy == 0 and p[0] - cx > 0)) else 1
        hq = 0 if (q[1] - cy > 0 or (q[1] - cy == 0 and q[0] - cx > 0)) else 1
        if hp != hq:
            return -1 if hp < hq else 1
        cr = (p[0] - cx) * (q[1] - cy) - (q[0] - cx) * (p[1] - cy)
        if cr > 0:
            return -1
        if cr < 0:
            return 1
        return 0

    return sorted(rest, key=functools.cmp_to_key(cmp))


# ---------------------------------------------------------------- measures


def euclid(a, uA, uB):
    """(x, r) with the true point being (x, sqrt3 * r)."""
    a = F(a)
    return ((a + uA - uB) / 2, (uA + uB - a) / 2)


def sqdist(p, q):
    """Squared Euclidean distance between (x, sqrt3 r) points -- exact rational."""
    dx = p[0] - q[0]
    dr = p[1] - q[1]
    return dx * dx + 3 * dr * dr


def measures(a, cons):
    """(nvert, oler_area_term, perimeter_interval, sqdiam, sqsides) for a region.

    oler_area_term is EXACTLY (2/sqrt3) * Area, a Fraction.
    """
    vs = vertices(cons)
    if not vs:
        return 0, F(0), Ival(0), F(0), []
    vs = order_ccw(vs)
    pts = [euclid(a, u, v) for (u, v) in vs]
    # shoelace in (x, sqrt3 r):  Area = (sqrt3/2)*|sum(x_i r_{i+1} - x_{i+1} r_i)|
    s = F(0)
    n = len(pts)
    for i in range(n):
        x1, r1 = pts[i]
        x2, r2 = pts[(i + 1) % n]
        s += x1 * r2 - x2 * r1
    oler_area = abs(s)          # = (2/sqrt3) * Area
    per = Ival(0)
    sides = []
    if n >= 2:
        rng = range(n) if n >= 3 else [0]
        for i in rng:
            q = sqdist(pts[i], pts[(i + 1) % n])
            sides.append(q)
            per = per + Ival.sqrt_of(q)
        if n == 2:
            per = per * 2       # degenerate: perimeter of a segment is twice its length
    sqdiam = F(0)
    for i in range(n):
        for j in range(i + 1, n):
            sqdiam = max(sqdiam, sqdist(pts[i], pts[j]))
    return n, oler_area, per, sqdiam, sides


# ---------------------------------------------------------------- d(n) table

_SQ = lambda q: Ival.sqrt_of(F(q))


def _d_proven():
    """Lower bounds on d(n) = minimal side (separation 1) holding n points.

    Entries listed here are the PROVEN optimal values from ../../problems/
    circle-packing-equilateral-triangle/README.md (status `cited`), converted by
    d = (s - 2 sqrt3)/2.  Everything else falls back to the Oler root, which is a
    rigorous lower bound for every n.
    """
    t = {}
    t[1] = Ival(0)
    t[2] = Ival(1)
    t[3] = Ival(1)
    t[4] = _SQ(3)                                   # s = 4 sqrt3
    t[5] = Ival(2)
    t[6] = Ival(2)
    t[7] = Ival(1) + _SQ(3)                         # s = 2 + 4 sqrt3
    t[8] = Ival(1) + _SQ(33) * F(1, 3)              # s = 2 + 2 sqrt3 + 2 sqrt33/3
    t[9] = Ival(3)
    t[10] = Ival(3)
    t[11] = Ival(2) + _SQ(6) * F(2, 3)              # s = 4 + 2 sqrt3 + 4 sqrt6/3
    t[12] = Ival(2) + _SQ(3)                        # s = 4 + 4 sqrt3
    t[13] = Ival(2) + _SQ(6) * F(1, 3) + _SQ(3) * F(2, 3)
    t[14] = Ival(4)
    t[15] = Ival(4)
    t[20] = Ival(5)                                 # Payan, qualified in README
    t[21] = Ival(5)
    return t


D_PROVEN = _d_proven()


def oler_root(n):
    """Least a with Oler(a) >= n:  a = (-3 + sqrt(8n+1))/2.  Lower bound on d(n)."""
    return (Ival.sqrt_of(F(8 * n + 1)) - 3) * F(1, 2)


def d_lower(n):
    if n in D_PROVEN:
        return D_PROVEN[n]
    return oler_root(n)


def N_upper_sq(sq_side, nmax=40):
    """Upper bound on N(t) for a CLOSED equilateral triangle whose side squares to sq_side."""
    best = 0
    for n in range(1, nmax + 1):
        dl = d_lower(n)
        # need d_lower(n) <= t, i.e. d_lower(n)^2 <= sq_side, decided on intervals
        lo2 = dl.lo * dl.lo
        if lo2 > sq_side:
            break              # d is non-decreasing, so no larger n qualifies
        best = n
    return best


def N_upper_open(j, nmax=40):
    """Upper bound on the number of unit-separated points with u_V < j (side < j)."""
    best = 0
    for n in range(1, nmax + 1):
        dl = d_lower(n)
        if dl.lo >= j:         # d(n) >= j, so n points do NOT fit in side < j
            break
        best = n
    return best


def capacity(a, cons, nmax=40):
    """Rigorous upper bound on the number of unit-separated points in a closed region."""
    nv, oler_area, per, sqdiam, sides = measures(a, cons)
    if nv == 0:
        return 0
    if sqdiam < 1:
        return 1
    if nv == 1:
        return 1
    if nv == 2:
        L = Ival.sqrt_of(sqdiam)
        import math
        return math.floor(L.hi) + 1
    # Oler on the convex region (valid: conv(points) is contained in it)
    b = Ival(oler_area) + per * F(1, 2) + 1
    cap = b.floor_upper()
    # equilateral triangle?  then the cited table is sharper
    if nv == 3 and sides[0] == sides[1] == sides[2]:
        cap = min(cap, N_upper_sq(sides[0], nmax))
    return cap
