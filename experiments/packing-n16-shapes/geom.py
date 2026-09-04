"""Exact rational geometry for 15-piece coverings of T_a.  EXACT ONLY.

Triangular basis: a point (u, v) means u*e1 + v*e2 with e1 = (1,0), e2 = (1/2, sqrt3/2).
Then  |(du,dv)|^2 = du^2 + du*dv + dv^2  is RATIONAL, and

    T_a = { (u,v) : u >= 0, v >= 0, u + v <= a }.

Euclidean area = (sqrt3/2) * (shoelace area in uv), so all area comparisons are rational too.
Nothing in this file uses floats.
"""
from fractions import Fraction as F


# ---------------------------------------------------------------- basics

def sq(p, q):
    """Squared Euclidean distance between uv-points p and q (exact rational)."""
    du = p[0] - q[0]
    dv = p[1] - q[1]
    return du * du + du * dv + dv * dv


def shoelace2(poly):
    """Twice the signed uv-shoelace area (positive for ccw)."""
    s = F(0)
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        s += x1 * y2 - x2 * y1
    return s


def area_uv(poly):
    """|uv-shoelace area|.  Euclidean area = (sqrt3/2) * this."""
    return abs(shoelace2(poly)) / 2


def diam2(poly):
    """Max squared distance between vertices.  For a polygon (convex or not) the
    diameter is attained at a pair of vertices, so this IS the diameter^2."""
    m = F(0)
    n = len(poly)
    for i in range(n):
        for j in range(i + 1, n):
            d = sq(poly[i], poly[j])
            if d > m:
                m = d
    return m


def ccw(poly):
    return poly if shoelace2(poly) > 0 else poly[::-1]


def is_convex_ccw(poly):
    """True if poly is a simple ccw convex polygon with no repeated/collinear-degenerate
    vertices (cross products all strictly positive)."""
    n = len(poly)
    if n < 3:
        return False
    for i in range(n):
        ax, ay = poly[i]
        bx, by = poly[(i + 1) % n]
        cx, cy = poly[(i + 2) % n]
        cr = (bx - ax) * (cy - by) - (by - ay) * (cx - bx)
        if cr <= 0:
            return False
    return True


# ---------------------------------------------------------------- clipping

def clip_halfplane(poly, a, b, c):
    """Sutherland-Hodgman clip of convex/simple `poly` to { a*u + b*v <= c }."""
    if not poly:
        return []
    out = []
    n = len(poly)
    for i in range(n):
        p = poly[i]
        q = poly[(i + 1) % n]
        fp = a * p[0] + b * p[1] - c
        fq = a * q[0] + b * q[1] - c
        if fp <= 0:
            out.append(p)
        if (fp < 0 < fq) or (fq < 0 < fp):
            t = fp / (fp - fq)
            out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    # drop consecutive duplicates
    res = []
    for p in out:
        if not res or res[-1] != p:
            res.append(p)
    if len(res) > 1 and res[0] == res[-1]:
        res.pop()
    return res if len(res) >= 3 else []


def edges_halfplanes(poly):
    """For a ccw convex polygon, the list of (a,b,c) with a*u+b*v <= c on the inside."""
    hs = []
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        # inward normal for ccw edge (x1,y1)->(x2,y2): (-(y2-y1), (x2-x1)) points inward,
        # so the inside is  (y2-y1)*u - (x2-x1)*v <= (y2-y1)*x1 - (x2-x1)*y1
        a = y2 - y1
        b = -(x2 - x1)
        c = a * x1 + b * y1
        hs.append((a, b, c))
    return hs


def convex_minus_convex(A, B):
    """A \\ B as a finite list of convex polygons (closed over-approximation of the
    set difference; their union contains A\\B and is contained in A).  A, B ccw convex."""
    out = []
    cur = A
    for (a, b, c) in edges_halfplanes(B):
        # part of `cur` on the far side of this edge is outside B
        far = clip_halfplane(cur, -a, -b, -c)
        if far and area_uv(far) > 0:
            out.append(far)
        cur = clip_halfplane(cur, a, b, c)
        if not cur:
            break
    return out


def cover_remainder(region, pieces, verbose=False):
    """Exact: subtract each convex piece from `region` (a ccw convex polygon).
    Returns the list of positive-area convex leftovers.  Empty list <=> the pieces
    cover `region` (up to a null set, which for closed sets means genuinely)."""
    todo = [region]
    for k, P in enumerate(pieces):
        nxt = []
        for A in todo:
            for piece in convex_minus_convex(A, P):
                if area_uv(piece) > 0:
                    nxt.append(piece)
        todo = nxt
        if verbose:
            print("  after piece %d: %d leftover polys, area %s"
                  % (k, len(todo), sum(area_uv(t) for t in todo)))
        if not todo:
            break
    return todo


def hull(points):
    """Exact convex hull (monotone chain), returns ccw vertex list without collinear pts."""
    pts = sorted(set(points))
    if len(pts) <= 2:
        return list(pts)
    def half(seq):
        st = []
        for p in seq:
            while len(st) >= 2:
                ax, ay = st[-2]; bx, by = st[-1]
                cr = (bx - ax) * (p[1] - by) - (by - ay) * (p[0] - bx)
                if cr <= 0:
                    st.pop()
                else:
                    break
            st.append(p)
        return st
    lo = half(pts)
    up = half(pts[::-1])
    return lo[:-1] + up[:-1]


def tri(a):
    """T_a as a ccw convex polygon in uv."""
    return [(F(0), F(0)), (F(a), F(0)), (F(0), F(a))]
