"""Exact convex-polygon geometry in the triangular chart, over Q(sqrt3).

Chart: a point (u, v) means u*e1 + v*e2 with e1 = (1,0), e2 = (1/2, sqrt3/2).
The chart map is linear with determinant sqrt3/2 > 0, so orientation and
convexity tests may be done directly on (u, v) with no distortion, and
|u e1 + v e2|^2 = u^2 + u v + v^2.
"""
from q3 import Q3, q3, ZERO


def cross(a, b, c):
    """(b-a) x (c-a), exact."""
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def area2(poly):
    """Twice the chart (shoelace) area, signed, exact."""
    s = ZERO
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        s = s + (x1 * y2 - x2 * y1)
    return s


def ccw(poly):
    return poly if area2(poly).sign() > 0 else poly[::-1]


def clip(poly, a, b, keep):
    """Sutherland-Hodgman: keep the part of convex `poly` with
    keep * cross(a, b, P) >= 0.  Exact; returns [] if empty."""
    if not poly:
        return []
    out = []
    n = len(poly)
    for i in range(n):
        P, Q = poly[i], poly[(i + 1) % n]
        sp = (cross(a, b, P) * keep).sign()
        sq = (cross(a, b, Q) * keep).sign()
        if sp >= 0:
            out.append(P)
        if (sp > 0 and sq < 0) or (sp < 0 and sq > 0):
            cp, cq = cross(a, b, P), cross(a, b, Q)
            t = cp / (cp - cq)
            out.append((P[0] + t * (Q[0] - P[0]), P[1] + t * (Q[1] - P[1])))
    # drop repeated vertices
    ded = []
    for p in out:
        if not ded or not (p[0] == ded[-1][0] and p[1] == ded[-1][1]):
            ded.append(p)
    if len(ded) > 1 and ded[0][0] == ded[-1][0] and ded[0][1] == ded[-1][1]:
        ded.pop()
    return ded if len(ded) >= 3 else []


def difference(Q, P):
    """Q \\ P for convex Q and convex P (both ccw): a list of convex parts.

    Decomposes by the standard 'outside edge i, inside edges 1..i-1' split.
    Exact; no area identity is used anywhere."""
    parts, cur = [], Q
    n = len(P)
    for i in range(n):
        if not cur:
            break
        A, B = P[i], P[(i + 1) % n]
        outside = clip(cur, A, B, q3(-1))
        if outside and area2(outside).sign() != 0:
            parts.append(outside)
        cur = clip(cur, A, B, q3(1))
    return parts


def covered(region, pieces):
    """True iff convex `region` is covered by `pieces`.  Direct residue
    subtraction: no area identity, no disjointness assumption, overlaps fine."""
    residue = [ccw(region)]
    for P in pieces:
        P = ccw(P)
        nxt = []
        for Q in residue:
            nxt.extend(difference(Q, P))
        residue = [r for r in nxt if area2(r).sign() != 0]
    return len(residue) == 0, residue


def sqdist(p, q):
    """Squared Euclidean distance between chart points, exact."""
    du, dv = p[0] - q[0], p[1] - q[1]
    return du * du + du * dv + dv * dv


def sqdiam(poly):
    """Max squared distance over vertex pairs = squared diameter of the
    convex hull, hence of the piece."""
    m = ZERO
    for i in range(len(poly)):
        for j in range(i + 1, len(poly)):
            d = sqdist(poly[i], poly[j])
            if d > m:
                m = d
    return m
