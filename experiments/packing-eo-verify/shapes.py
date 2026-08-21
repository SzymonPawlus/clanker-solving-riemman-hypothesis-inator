"""Polygon helpers shared by the eo-verification checkers (mine)."""

from fractions import Fraction as F
from surd import Surd, oler_bound, tri, lattice, cross, shoelace, edge_len, perimeter


def clip(poly, A, B, C):
    """Sutherland-Hodgman: the part of a convex polygon with A*u + B*v <= C."""
    out = []
    n = len(poly)
    for i in range(n):
        p, q = poly[i], poly[(i + 1) % n]
        fp = A * p[0] + B * p[1] - C
        fq = A * q[0] + B * q[1] - C
        if fp <= 0:
            out.append(p)
        if (fp < 0 < fq) or (fq < 0 < fp):
            tpar = fp / (fp - fq)
            out.append((p[0] + tpar * (q[0] - p[0]), p[1] + tpar * (q[1] - p[1])))
    ded = []
    for p in out:
        if not ded or p != ded[-1]:
            ded.append(p)
    if len(ded) > 1 and ded[0] == ded[-1]:
        ded.pop()
    return ded


def cells(a, m):
    """The m^2 closed cells of side a/m subdividing T_a, plus the exact total
    internal cut length I = 3 * sum_{j=1}^{m-1} a*(m-j)/m."""
    a = F(a)
    h = a / m
    up, down = [], []
    for i in range(m):
        for j in range(m - i):
            up.append([(i * h, j * h), ((i + 1) * h, j * h), (i * h, (j + 1) * h)])
    for i in range(m - 1):
        for j in range(m - 1 - i):
            down.append([((i + 1) * h, (j + 1) * h), ((i + 1) * h, j * h),
                         (i * h, (j + 1) * h)])
    I = Surd(3 * sum((a * F(m - j, m) for j in range(1, m)), F(0)))
    return up + down, I


def bound_of(poly):
    """B(K) for a possibly degenerate convex polygon in lattice coordinates."""
    if len(poly) == 0:
        return Surd(0)          # K empty: def(K) = B(T), handled separately
    if len(poly) == 1:
        return Surd(1)
    if len(poly) == 2:
        from surd import edge_len
        return edge_len(poly[0], poly[1]) + Surd(1)
    return oler_bound(poly)


def inside(poly, p):
    """p in the closed convex polygon (CCW or CW), exactly."""
    if len(poly) == 0:
        return False
    if len(poly) == 1:
        return p == poly[0]
    if len(poly) == 2:
        a, b = poly
        if cross(a, b, p) != 0:
            return False
        return (min(a[0], b[0]) <= p[0] <= max(a[0], b[0])
                and min(a[1], b[1]) <= p[1] <= max(a[1], b[1]))
    s = shoelace(poly)
    sgn = 1
    # orient CCW
    tot = F(0)
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        tot += x1 * y2 - x2 * y1
    if tot < 0:
        poly = list(reversed(poly))
    for i in range(len(poly)):
        if cross(poly[i], poly[(i + 1) % len(poly)], p) < 0:
            return False
    return True


def gain(K, m, lam):
    """def(K) - |Lambda ∩ (T\\K)|, as a Surd.  Positive would break Theorem 6."""
    d = oler_bound(tri(m)) - bound_of(K)
    outside = sum(1 for p in lam if not inside(K, p))
    return d - Surd(outside), outside
