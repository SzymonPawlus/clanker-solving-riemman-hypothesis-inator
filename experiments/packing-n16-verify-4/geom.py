"""Exact convex-polygon geometry in the triangular chart, worker V4.

Chart (fixed by attacks/n16-covering-2/README.md, which is what the table of
pieces is written in):  e1 = (1,0), e2 = (1/2, sqrt3/2); a point (u,v) means
u*e1 + v*e2.  Then

    |(du,dv)|^2 = du^2 + du*dv + dv^2                       (metric)
    T_a = { u >= 0, v >= 0, u + v <= a }                    (the triangle)
    dist to side {v=0}    = v*sqrt3/2
    dist to side {u=0}    = u*sqrt3/2
    dist to side {u+v=a}  = (a-u-v)*sqrt3/2                 (Viviani)
    Euclidean area = (sqrt3/2) * (area in the (u,v) chart)

The map (u,v) -> (u+v/2, v*sqrt3/2) has determinant sqrt3/2 > 0, so chart cross
products carry Euclidean orientation.  Written from the geometry, not from any
other lane's code.
"""
from q3 import Q3, R3, ZERO, ONE, floor_q3
from fractions import Fraction as F


def d2(P, Q):
    du = P[0] - Q[0]
    dv = P[1] - Q[1]
    return du * du + du * dv + dv * dv


def cross(O, A, B):
    return (A[0] - O[0]) * (B[1] - O[1]) - (A[1] - O[1]) * (B[0] - O[0])


def signed_area2(poly):
    """2 * signed chart area."""
    s = ZERO
    n = len(poly)
    for i in range(n):
        x0, y0 = poly[i]
        x1, y1 = poly[(i + 1) % n]
        s = s + (x0 * y1 - x1 * y0)
    return s


def ccw(poly):
    return poly if signed_area2(poly).sign() > 0 else poly[::-1]


def is_convex_ccw(poly):
    n = len(poly)
    for i in range(n):
        if cross(poly[i], poly[(i + 1) % n], poly[(i + 2) % n]).sign() <= 0:
            return False
    return True


def clip(poly, f):
    """Sutherland-Hodgman clip of a convex polygon to the closed half-plane
    {X : f(X) >= 0}, f affine.  Returns [] if the result is empty."""
    if not poly:
        return []
    out = []
    n = len(poly)
    vals = [f(P) for P in poly]
    for i in range(n):
        A, B = poly[i], poly[(i + 1) % n]
        fa, fb = vals[i], vals[(i + 1) % n]
        sa, sb = fa.sign(), fb.sign()
        if sa >= 0:
            out.append(A)
        if (sa > 0 and sb < 0) or (sa < 0 and sb > 0):
            t = fa / (fa - fb)
            out.append((A[0] + t * (B[0] - A[0]), A[1] + t * (B[1] - A[1])))
    # drop consecutive duplicates
    ded = []
    for P in out:
        if not ded or (ded[-1][0] != P[0] or ded[-1][1] != P[1]):
            ded.append(P)
    if len(ded) > 1 and ded[0][0] == ded[-1][0] and ded[0][1] == ded[-1][1]:
        ded.pop()
    return ded


def halfplanes(poly):
    """Inward closed half-planes of a ccw convex polygon, as affine functions."""
    hs = []
    n = len(poly)
    for i in range(n):
        A, B = poly[i], poly[(i + 1) % n]
        def f(P, A=A, B=B):
            return cross(A, B, P)      # >= 0 <=> P left of A->B <=> inside
        hs.append(f)
    return hs


def subtract(Q, P):
    """Q \\ interior(P) as a list of convex chart polygons, exact.
    Q, P convex ccw.  Uses only half-plane clipping -- no area identity,
    no disjointness assumption."""
    parts = []
    running = Q
    for f in halfplanes(P):
        outside = clip(running, lambda X, f=f: -f(X))   # {f <= 0}
        if len(outside) >= 3 and signed_area2(outside).sign() != 0:
            parts.append(ccw(outside))
        running = clip(running, f)
        if len(running) < 3 or signed_area2(running).sign() == 0:
            running = []
            break
    return parts


def covered(Q, pieces):
    """True iff the convex region Q is covered by the convex pieces, up to a
    set of zero area (which for closed pieces means covered outright)."""
    residue = [ccw(Q)]
    for P in pieces:
        nxt = []
        for Rg in residue:
            nxt.extend(subtract(Rg, ccw(P)))
        residue = nxt
        if not residue:
            return True, 0
    return (len(residue) == 0), len(residue)
