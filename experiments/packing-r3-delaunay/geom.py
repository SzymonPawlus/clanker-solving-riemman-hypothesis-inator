"""Exact configuration library for the Euler-localised-scoring LP.

Everything here is exact.  A point is a pair of Q(sqrt 3) coordinates; a
Q(sqrt 3) element is a pair of ``Fraction``s ``(u, v)`` meaning ``u + v*sqrt(3)``.

Oler normalisation throughout: minimum pairwise separation is **1** and the
container side is ``a``.  This repo's certificates use separation 2 and side
``d = 2a``.

For every configuration we record exactly the data the LP consumes:

    n     number of points
    b     number of points on the boundary of conv(E)   (hull vertices *and*
          points lying inside a hull edge)
    F     number of faces of a triangulation of conv(E) with vertex set E
    Ahat  (4/sqrt 3) * area(conv E)      -- so a unit equilateral triangle has Ahat = 1
    Mhat  perimeter(conv E) / 3          -- so a unit equilateral triangle has Mhat = 1

Ahat and Mhat are returned as *rational upper bounds* (outward rounded).  That
direction is deliberate: the LP is a relaxation of the family (see README), so
weakening a constraint keeps the conclusion valid.
"""

from fractions import Fraction as Fr
from math import isqrt

# ---------------------------------------------------------------- Q(sqrt 3)

def q(u=0, v=0):
    return (Fr(u), Fr(v))

def qadd(x, y):
    return (x[0] + y[0], x[1] + y[1])

def qsub(x, y):
    return (x[0] - y[0], x[1] - y[1])

def qmul(x, y):
    return (x[0] * y[0] + 3 * x[1] * y[1], x[0] * y[1] + x[1] * y[0])

def qsign(x):
    """Exact sign of u + v*sqrt(3)."""
    u, v = x
    if u == 0:
        return (v > 0) - (v < 0)
    if v == 0:
        return (u > 0) - (u < 0)
    if u > 0 and v > 0:
        return 1
    if u < 0 and v < 0:
        return -1
    # opposite signs: compare u^2 with 3 v^2, sign follows the dominant term
    if u > 0:                      # u > 0 > v : positive iff u^2 > 3 v^2
        return 1 if u * u > 3 * v * v else (-1 if u * u < 3 * v * v else 0)
    return -1 if u * u > 3 * v * v else (1 if u * u < 3 * v * v else 0)

# rational upper/lower bounds for sqrt(3), tightened as needed
_S3_LO = Fr(97, 56)      # 1.732142... no: 97/56 = 1.732142857 > sqrt3
_S3_LO = Fr(1351, 780)   # < sqrt3  (classic Archimedes bound)
_S3_HI = Fr(265, 153)    # > sqrt3

def qbounds(x):
    """Rational (lo, hi) enclosing u + v*sqrt(3)."""
    u, v = x
    if v >= 0:
        return (u + v * _S3_LO, u + v * _S3_HI)
    return (u + v * _S3_HI, u + v * _S3_LO)

def rat_sqrt_up(x, denom=10 ** 25):
    """Rational upper bound for sqrt(x), x a non-negative Fraction."""
    assert x >= 0
    # scale so that we take an integer square root of x * denom^2
    num = x.numerator * denom * denom
    den = x.denominator
    r = isqrt(num // den) + 1          # >= sqrt(num/den)
    return Fr(r, denom)

def qsqrt_up(x, denom=10 ** 25):
    """Rational upper bound for sqrt(u + v*sqrt 3)."""
    _, hi = qbounds(x)
    return rat_sqrt_up(hi, denom)

# ---------------------------------------------------------------- geometry

def d2(p, r):
    """Exact squared distance, an element of Q(sqrt 3)."""
    dx = qsub(p[0], r[0])
    dy = qsub(p[1], r[1])
    return qadd(qmul(dx, dx), qmul(dy, dy))

def cross(o, p, r):
    return qsub(qmul(qsub(p[0], o[0]), qsub(r[1], o[1])),
                qmul(qsub(p[1], o[1]), qsub(r[0], o[0])))

def twice_area(poly):
    """Exact |shoelace| of a simple polygon, element of Q(sqrt 3), >= 0."""
    s = q(0, 0)
    k = len(poly)
    for i in range(k):
        a, bb = poly[i], poly[(i + 1) % k]
        s = qadd(s, qsub(qmul(a[0], bb[1]), qmul(bb[0], a[1])))
    return s if qsign(s) >= 0 else (-s[0], -s[1])

def hull_cycle(pts):
    """Boundary cycle of conv(pts) *including* points interior to hull edges,
    in ccw order.  Monotone chain with exact predicates, keeping collinear
    points on the hull."""
    P = sorted(set(pts), key=lambda p: (qbounds(p[0]), qbounds(p[1])))
    # sort exactly: bucket by exact comparison
    def less(p, r):
        c = qsign(qsub(p[0], r[0]))
        if c != 0:
            return c < 0
        return qsign(qsub(p[1], r[1])) < 0
    def fkey(p):
        return (float(p[0][0]) + 1.7320508075688772 * float(p[0][1]),
                float(p[1][0]) + 1.7320508075688772 * float(p[1][1]))
    P = sorted(set(pts), key=fkey)      # float pre-sort, then exact fix-up
    for i in range(1, len(P)):          # insertion sort, exact, nearly sorted
        j = i
        while j > 0 and less(P[j], P[j - 1]):
            P[j], P[j - 1] = P[j - 1], P[j]
            j -= 1

    def build(seq):
        out = []
        for p in seq:
            while len(out) >= 2 and qsign(cross(out[-2], out[-1], p)) < 0:
                out.pop()
            out.append(p)
        return out

    lower = build(P)
    upper = build(list(reversed(P)))
    cyc = lower[:-1] + upper[:-1]
    # `build` with the strict `< 0` test keeps collinear points.
    return cyc

# ---------------------------------------------------------------- config record

class Config:
    def __init__(self, name, pts, faces, a=None, note=""):
        self.name = name
        self.pts = pts
        self.faces = faces            # list of triples of points
        self.a = a                    # container side, if the config sits in one
        self.note = note
        self.n = len(pts)

        # minimum separation must be >= 1.  Float pre-screen (generous), then
        # every candidate pair is re-checked in exact Q(sqrt 3).
        fl = [(float(x[0]) + 1.7320508075688772 * float(x[1]),
               float(y[0]) + 1.7320508075688772 * float(y[1])) for x, y in pts]
        self.minsep2_lo = None
        for i in range(self.n):
            xi, yi = fl[i]
            for j in range(i + 1, self.n):
                xj, yj = fl[j]
                if (xi - xj) ** 2 + (yi - yj) ** 2 < 1.25:
                    lo = qbounds(d2(pts[i], pts[j]))[0]
                    assert lo >= 1, (name, i, j, float(lo))
                    if self.minsep2_lo is None or lo < self.minsep2_lo:
                        self.minsep2_lo = lo
        if self.minsep2_lo is None:
            self.minsep2_lo = Fr(5, 4)

        cyc = hull_cycle(pts)
        self.b = len(cyc)
        self.F = len(faces)
        assert self.F == 2 * self.n - self.b - 2, \
            f"{name}: Euler F={self.F} != 2n-b-2={2*self.n-self.b-2}"

        # areas: sum of face areas must equal hull area, exactly
        ta_hull = twice_area(cyc)
        ta_faces = q(0, 0)
        for f in faces:
            ta_faces = qadd(ta_faces, twice_area(list(f)))
        assert ta_hull == ta_faces, f"{name}: face areas do not tile the hull"

        # Ahat = (4/sqrt3) * area = (4/sqrt3) * ta/2 = (2/sqrt3) * ta
        #      = (2/3) * sqrt3 * ta
        ahat = qmul(q(0, Fr(2, 3)), ta_hull)
        self.Ahat_up = qbounds(ahat)[1]

        # Mhat = perimeter/3
        per = Fr(0)
        self.edge_len_up = []
        for i in range(self.b):
            e2 = d2(cyc[i], cyc[(i + 1) % self.b])
            L = qsqrt_up(e2)
            self.edge_len_up.append(L)
            per += L
        self.Mhat_up = per / 3
        self.cycle = cyc

        # face shape key (sorted exact squared side lengths) and area upper bound
        self.face_shapes = []
        for f in faces:
            s2 = sorted([d2(f[0], f[1]), d2(f[1], f[2]), d2(f[0], f[2])],
                        key=lambda z: qbounds(z))
            ta = twice_area(list(f))
            area_up = qbounds(qmul(q(Fr(1, 2)), ta))[1]
            self.face_shapes.append((tuple(s2), area_up))

# ---------------------------------------------------------------- families

def lattice_pts(m):
    """Triangular lattice T(m+1): all i*u + j*v with i+j <= m, u=(1,0),
    v=(1/2, sqrt3/2).  n = (m+1)(m+2)/2, container side a = m."""
    P = {}
    for j in range(m + 1):
        for i in range(m + 1 - j):
            P[(i, j)] = (q(Fr(i) + Fr(j, 2), 0), q(0, Fr(j, 2)))
    return P

def lattice_faces(P, m, skip=()):
    faces = []
    for j in range(m):
        for i in range(m - j):
            t = ((i, j), (i + 1, j), (i, j + 1))
            if all(k in P for k in t):
                faces.append(tuple(P[k] for k in t))
    for j in range(m - 1):
        for i in range(m - 1 - j):
            t = ((i + 1, j), (i, j + 1), (i + 1, j + 1))
            if all(k in P for k in t):
                faces.append(tuple(P[k] for k in t))
    return faces

def cfg_lattice(m):
    P = lattice_pts(m)
    return Config(f"T({m+1}) lattice", list(P.values()), lattice_faces(P, m),
                  a=Fr(m), note="triangular lattice, exactly tight for Oler")

def cfg_lattice_minus_apex(m):
    P = lattice_pts(m)
    del P[(0, m)]
    return Config(f"T({m+1}) minus apex", list(P.values()), lattice_faces(P, m),
                  a=Fr(m), note="Erdos-Oler witness")

def cfg_flat_arc(m):
    """p_j = (j, j(m-j)/m^3), j = 0..m.  Strictly concave, so all points are
    hull vertices; consecutive gaps are >= 1; area stays O(1) while n grows."""
    pts = [(q(Fr(j)), q(Fr(j * (m - j), m ** 3))) for j in range(m + 1)]
    faces = [(pts[0], pts[j], pts[j + 1]) for j in range(1, m)]
    return Config(f"flat arc m={m}", pts, faces,
                  note="thin convex arc: forces the boundary-length coefficient")

def cfg_corners_centroid():
    """Equilateral triangle of side sqrt(3) plus its centroid; separation 1."""
    A = (q(0), q(0))
    B = (q(0, 1), q(0))
    C = (q(0, Fr(1, 2)), q(Fr(3, 2)))
    G = (q(0, Fr(1, 2)), q(Fr(1, 2)))
    pts = [A, B, C, G]
    faces = [(A, B, G), (B, C, G), (C, A, G)]
    return Config("corners+centroid (n=4)", pts, faces, a=None,
                  note="hull = container, all slack is stage 1")

def library(max_lattice=12, arcs=(3, 4, 6, 8, 12, 16, 24)):
    cfgs = [cfg_corners_centroid()]
    for m in range(1, max_lattice + 1):
        cfgs.append(cfg_lattice(m))
        if m >= 2:
            cfgs.append(cfg_lattice_minus_apex(m))
    for m in arcs:
        cfgs.append(cfg_flat_arc(m))
    return cfgs
