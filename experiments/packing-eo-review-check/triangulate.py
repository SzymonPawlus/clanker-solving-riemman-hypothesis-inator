"""Build an explicit triangulation of conv(E) with vertex set exactly E.

Used to test the attack's identity by construction rather than by trusting the
face-count formula.  Exact arithmetic throughout; no floating point decides
anything.

Method (deliberately naive, so that it is easy to audit):
  1. order the b boundary points around the hull,
  2. ear-clip that convex polygon at strict corners  -> b - 2 triangles,
  3. insert each of the i interior points, splitting whichever triangle(s)
     contain it -> +2 triangles per insertion.
Step 3 makes F = (b - 2) + 2i = 2n - b - 2 a *consequence* of the construction
rather than an assumption.
"""

from fractions import Fraction as F

from field import Alg


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def boundary_cycle(pts):
    """CCW list of every index lying on the hull boundary, in order."""
    import functools

    def cmp(i, j):
        d = (pts[i][0] - pts[j][0]).sign()
        return d if d else (pts[i][1] - pts[j][1]).sign()

    order = sorted(range(len(pts)), key=functools.cmp_to_key(cmp))

    def build(idxs):
        st = []
        for i in idxs:
            while len(st) >= 2 and cross(pts[st[-2]], pts[st[-1]], pts[i]).sign() <= 0:
                st.pop()
            st.append(i)
        return st

    verts = build(order)[:-1] + build(order[::-1])[:-1]

    cyc = []
    for k in range(len(verts)):
        u, w = verts[k], verts[(k + 1) % len(verts)]
        cyc.append(u)
        mids = []
        dx, dy = pts[w][0] - pts[u][0], pts[w][1] - pts[u][1]
        len2 = dx * dx + dy * dy
        for i in range(len(pts)):
            if i in (u, w):
                continue
            if cross(pts[u], pts[w], pts[i]).sign() != 0:
                continue
            t = (pts[i][0] - pts[u][0]) * dx + (pts[i][1] - pts[u][1]) * dy
            if t.sign() > 0 and (len2 - t).sign() > 0:
                mids.append((t, i))
        mids.sort(key=functools.cmp_to_key(lambda p, q: (p[0] - q[0]).sign()))
        cyc.extend(i for _, i in mids)
    return cyc


def _ccw(pts, t):
    a, b, c = t
    return t if cross(pts[a], pts[b], pts[c]).sign() > 0 else (a, c, b)


def _usable(pts, poly):
    """A polygon we can keep clipping: a strict triangle, or has a strict corner."""
    n = len(poly)
    if n < 3:
        return False
    return any(cross(pts[poly[k - 1]], pts[poly[k]],
                     pts[poly[(k + 1) % n]]).sign() > 0 for k in range(n))


def ear_clip(pts, cyc):
    """Triangulate a convex cycle that may contain collinear vertices.

    Clipping the *first* strict corner is not enough: it can strand a run of
    collinear boundary points as the final triple (this really happens on the
    T(4) lattice).  So a candidate ear is accepted only if what remains is
    still clippable.
    """
    poly = list(cyc)
    tris = []
    while len(poly) > 3:
        for k in range(len(poly)):
            a, b, c = poly[k - 1], poly[k], poly[(k + 1) % len(poly)]
            if cross(pts[a], pts[b], pts[c]).sign() <= 0:
                continue
            rest = poly[:k] + poly[k + 1:]
            if not _usable(pts, rest):
                continue
            tris.append((a, b, c))
            poly = rest
            break
        else:
            raise RuntimeError("no clippable strict corner")
    a, b, c = poly
    assert cross(pts[a], pts[b], pts[c]).sign() > 0, "final triangle degenerate"
    tris.append((a, b, c))
    return tris


def locate(pts, tris, p):
    """Indices of triangles whose closed region contains p, with edge info."""
    hits = []
    for ti, (a, b, c) in enumerate(tris):
        s = [cross(pts[a], pts[b], p).sign(),
             cross(pts[b], pts[c], p).sign(),
             cross(pts[c], pts[a], p).sign()]
        if all(x >= 0 for x in s):
            hits.append((ti, s))
    return hits


def triangulate(pts):
    cyc = boundary_cycle(pts)
    onb = set(cyc)
    tris = [_ccw(pts, t) for t in ear_clip(pts, cyc)]
    interior = [i for i in range(len(pts)) if i not in onb]

    for i in interior:
        p = pts[i]
        hits = locate(pts, tris, p)
        assert hits, f"interior point {i} lies in no triangle"
        zeros = [s.count(0) for _, s in hits]
        assert max(zeros) < 2, f"point {i} coincides with a vertex"
        new = []
        drop = set()
        before = len(tris)
        for ti, s in hits:
            a, b, c = tris[ti]
            drop.add(ti)
            if 0 not in s:                       # strictly inside
                new += [(a, b, i), (b, c, i), (c, a, i)]
            else:                                # on one edge of this triangle
                e = s.index(0)
                u, v, w = [(a, b, c), (b, c, a), (c, a, b)][e]
                new += [(u, i, w), (i, v, w)]
        tris = [t for k, t in enumerate(tris) if k not in drop] + \
               [_ccw(pts, t) for t in new]
        assert len(tris) == before + 2, \
            f"insertion of {i} changed the count by {len(tris) - before}, not 2"
    return tris
