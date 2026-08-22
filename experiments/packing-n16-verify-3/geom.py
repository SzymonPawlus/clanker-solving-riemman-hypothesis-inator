"""Exact convex-polygon geometry in the triangular chart, worker V3.

Chart: a point is (u, v) meaning u*e1 + v*e2 with e1 = (1,0), e2 = (1/2, sqrt3/2).
Squared distance is the quadratic form  Q(u,v) = u^2 + u v + v^2   (derived from
|u e1 + v e2|^2 = (u+v/2)^2 + 3v^2/4).

The map (u,v) -> Cartesian is linear with determinant sqrt3/2 > 0, so orientation,
convexity and containment tests may be done in (u,v) coordinates unchanged;
only areas differ, by the constant factor sqrt3/2.

T_a = {u >= 0, v >= 0, u + v <= a}: an equilateral triangle of side a with the
vertices (0,0), (a,0), (0,a) of the chart.
"""
from q3f import Q3, q3, ZERO


def sub(P, Q):
    return (P[0] - Q[0], P[1] - Q[1])


def cross(O, A, B):
    """z-component of (A-O) x (B-O) in chart coordinates."""
    return (A[0] - O[0]) * (B[1] - O[1]) - (A[1] - O[1]) * (B[0] - O[0])


def qform(P, Q):
    """Exact squared Euclidean distance between chart points P and Q."""
    du = P[0] - Q[0]
    dv = P[1] - Q[1]
    return du * du + du * dv + dv * dv


def area2(poly):
    """Twice the signed chart area (multiply by sqrt3/2 for true area)."""
    s = ZERO
    n = len(poly)
    for i in range(n):
        A, B = poly[i], poly[(i + 1) % n]
        s = s + (A[0] * B[1] - A[1] * B[0])
    return s


def is_ccw_strictly_convex(poly):
    n = len(poly)
    if n < 3:
        return False
    for i in range(n):
        if cross(poly[i], poly[(i + 1) % n], poly[(i + 2) % n]).sign() <= 0:
            return False
    return True


def clip_halfplane(poly, A, B, keep_left=True):
    """Clip convex polygon by the closed halfplane cross(A,B,X) >= 0 (keep_left)
    or <= 0.  Sutherland-Hodgman, exact."""
    def inside(X):
        s = cross(A, B, X).sign()
        return s >= 0 if keep_left else s <= 0

    def val(X):
        c = cross(A, B, X)
        return c if keep_left else -c

    out = []
    n = len(poly)
    for i in range(n):
        C, D = poly[i], poly[(i + 1) % n]
        ic, idd = inside(C), inside(D)
        if ic:
            out.append(C)
        if ic != idd:
            vc, vd = val(C), val(D)
            t = vc / (vc - vd)
            out.append((C[0] + t * (D[0] - C[0]), C[1] + t * (D[1] - C[1])))
    return dedup(out)


def dedup(poly):
    out = []
    for P in poly:
        if not out or not (out[-1][0] == P[0] and out[-1][1] == P[1]):
            out.append(P)
    if len(out) > 1 and out[0][0] == out[-1][0] and out[0][1] == out[-1][1]:
        out.pop()
    return out


def intersect_convex(A, B):
    """Intersection of two ccw convex polygons."""
    poly = list(A)
    n = len(B)
    for i in range(n):
        poly = clip_halfplane(poly, B[i], B[(i + 1) % n], keep_left=True)
        if len(poly) < 3:
            return []
    return poly


def point_in_convex(P, poly):
    """Closed containment in a ccw convex polygon."""
    n = len(poly)
    for i in range(n):
        if cross(poly[i], poly[(i + 1) % n], P).sign() < 0:
            return False
    return True


def subtract_convex(Q, P):
    """Q \\ int(P) as a list of closed convex polygons whose union is exactly
    that set (the parts may overlap on measure-zero sets; that is harmless for
    an emptiness test).  Both arguments ccw convex.

    Complement of int(P) = union over edges e of P of the closed outer halfplane
    of e, since P is convex.  Intersecting with Q distributes."""
    parts = []
    n = len(P)
    for i in range(n):
        part = clip_halfplane(Q, P[i], P[(i + 1) % n], keep_left=False)
        if len(part) >= 3 and area2(part).sign() != 0:
            parts.append(part)
    return parts


def touches(Q, P):
    """True if Q and P share positive area."""
    I = intersect_convex(Q, P)
    return len(I) >= 3 and area2(I).sign() != 0


def contained_in(part, P):
    """True if every vertex of `part` lies in the closed convex polygon P
    (hence part subset P, both convex)."""
    return all(point_in_convex(V, P) for V in part)
