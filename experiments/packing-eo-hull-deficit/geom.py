"""Exact convex geometry for the hull-deficit attack.

Self-contained apart from `exact.Alg` / `exact.Ival`, which are imported from
`experiments/packing-oler-slack/exact.py` (read-only to this experiment; see the
README for why that import is deliberate).

Everything that decides a *conclusion* is exact: orientation tests, hull, areas,
point-in-halfplane tests, lattice-point counts.  Only quantities containing an
edge *length* (perimeters, and hence def(K)) are rational intervals with outward
rounding.
"""

import os
import sys
from fractions import Fraction as F

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "packing-oler-slack")
)
from exact import Alg, Ival, parse_alg, sqrt_bounds  # noqa: E402

SQRT3 = Alg.sqrt(3)
HALF = Alg(F(1, 2))


def cross(o, a, b):
    """Exact orientation determinant (b-o) x (a-o) sign convention below."""
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def convex_hull(points):
    """Monotone chain.  Returns the hull vertices in CCW order, collinear points dropped."""
    pts = sorted(set((p[0], p[1]) for p in points), key=lambda p: (p[0], p[1]))
    if len(pts) <= 2:
        return list(pts)
    lower = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= Alg(0):
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= Alg(0):
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def polygon_area(poly):
    """Exact shoelace area of a simple polygon given CCW."""
    total = Alg(0)
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        total = total + (x1 * y2 - x2 * y1)
    return total * HALF


def seg_len(p, q):
    """Rigorous rational enclosure of |pq|."""
    d2 = (p[0] - q[0]) * (p[0] - q[0]) + (p[1] - q[1]) * (p[1] - q[1])
    return Ival.of(d2, prec=80).sqrt(prec=80)


def polygon_perimeter(poly):
    total = Ival(F(0))
    for i in range(len(poly)):
        total = total + seg_len(poly[i], poly[(i + 1) % len(poly)])
    return total


def clip_halfplane(poly, nx, ny, c):
    """Sutherland-Hodgman clip of a convex polygon to {n.x >= c}.  Exact."""
    out = []
    m = len(poly)
    for i in range(m):
        cur, nxt = poly[i], poly[(i + 1) % m]
        fcur = nx * cur[0] + ny * cur[1] - c
        fnxt = nx * nxt[0] + ny * nxt[1] - c
        if fcur >= Alg(0):
            out.append(cur)
        if (fcur > Alg(0) and fnxt < Alg(0)) or (fcur < Alg(0) and fnxt > Alg(0)):
            tpar = fcur / (fcur - fnxt)
            out.append(
                (cur[0] + (nxt[0] - cur[0]) * tpar, cur[1] + (nxt[1] - cur[1]) * tpar)
            )
    return out


def triangle(a):
    """The point-triangle of side `a`: A=(0,0), B=(a,0), C=(a/2, a*sqrt3/2), CCW."""
    return [
        (Alg(0), Alg(0)),
        (a, Alg(0)),
        (a * HALF, a * SQRT3 * HALF),
    ]


def bisector_coords(a, p):
    """(h_A, h_B, h_C): distance from each corner along its angle bisector."""
    x, y = p
    hA = SQRT3 * HALF * x + HALF * y
    hB = SQRT3 * HALF * (a - x) + HALF * y
    hC = a * SQRT3 * HALF - y
    return hA, hB, hC


def side_from_h(h):
    """The corner triangle {h_V <= h} has side t = 2h/sqrt3."""
    return h * Alg(F(2, 3)) * SQRT3          # 2/sqrt3 = 2*sqrt3/3


def oler_triangle_bound(a):
    """a^2/2 + 3a/2 + 1 -- Oler's inequality relaxed to the triangle of side a."""
    return a * a * HALF + a * Alg(F(3, 2)) + Alg(1)


def deficit_of_polygon(a, poly):
    """def(K) = (2/sqrt3)(A(T)-A(K)) + (M(T)-M(K))/2, as a rigorous interval."""
    T = triangle(a)
    dA = polygon_area(T) - polygon_area(poly)
    dM = Ival.of(a * Alg(3), prec=80) - polygon_perimeter(poly)
    return Ival.of(dA * Alg(F(2, 3)) * SQRT3, prec=80) + dM * Ival(F(1, 2))


def lattice(k):
    """Triangular lattice T(k): k(k+1)/2 points, separation 1, in the triangle of side k-1."""
    pts = []
    for j in range(k):
        for i in range(k - j):
            pts.append((Alg(F(j, 2)) + Alg(i), Alg(j) * SQRT3 * HALF))
    return pts


# --- radical expressions outside Q(sqrt3, sqrt11): a tiny (rational + sum c_i sqrt r_i) type


class Rad:
    """rational + sum of c*sqrt(r); only ever compared, never multiplied."""

    def __init__(self, q=0, terms=()):
        self.q = F(q)
        self.terms = tuple((F(c), int(r)) for c, r in terms)

    def enclose(self, prec=80):
        lo = hi = self.q
        for c, r in self.terms:
            rlo, rhi = sqrt_bounds(F(r), prec)
            if c >= 0:
                lo += c * rlo
                hi += c * rhi
            else:
                lo += c * rhi
                hi += c * rlo
        return Ival(lo, hi)

    def cmp_rational(self, t):
        """Exact comparison against a rational t: -1, 0 or +1 for self <=> t."""
        t = F(t)
        prec = 40
        while prec <= 4000:
            iv = self.enclose(prec)
            if iv.hi < t:
                return -1
            if iv.lo > t:
                return 1
            if iv.lo == iv.hi == t:
                return 0
            prec *= 2
        raise RuntimeError("comparison did not resolve")


# a(n) = smallest side of an equilateral triangle holding n points at separation >= 1,
# for n <= 15, in Oler normalisation.  These are the `cited` optimal values of this
# problem's README (s(n) = 2*sqrt3 + d(n), a = d/2); n=0,1 are degenerate.
A_OPT = {
    0: Rad(0),
    1: Rad(0),
    2: Rad(1),
    3: Rad(1),
    4: Rad(0, [(1, 3)]),                       # sqrt3
    5: Rad(2),
    6: Rad(2),
    7: Rad(1, [(1, 3)]),                       # 1 + sqrt3
    8: Rad(1, [(F(1, 3), 33)]),                # 1 + sqrt33/3
    9: Rad(3),
    10: Rad(3),
    11: Rad(2, [(F(2, 3), 6)]),                # 2 + 2sqrt6/3
    12: Rad(2, [(1, 3)]),                      # 2 + sqrt3
    13: Rad(2, [(F(1, 3), 6), (F(2, 3), 3)]),  # 2 + sqrt6/3 + 2sqrt3/3
    14: Rad(4),
    15: Rad(4),
}


def max_points_in_triangle(t):
    """N(t) = max unit-separated points in a closed equilateral triangle of side t.

    Exact for rational 0 <= t <= 4: the values above are `cited` optimal, and Oler's
    inequality caps N(4) at 4^2/2 + 3*4/2 + 1 = 15, so no n > 15 can appear.
    """
    t = F(t)
    if t > 4:
        raise ValueError("only certified for t <= 4")
    best = 0
    for n in range(0, 16):
        if A_OPT[n].cmp_rational(t) <= 0:
            best = max(best, n)
    return best
