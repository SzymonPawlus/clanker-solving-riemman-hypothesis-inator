"""Exact configuration library for the Euler-localised-scoring measurement.

Status of everything computed here: `numerical` (exact arithmetic, but it is a
computation, not a proof) -- see ../../problems/circle-packing-equilateral-triangle/
attacks/r4-delaunay/README.md.

Written from scratch for issue AB / round 4.  The abandoned r3-delaunay
scaffolding was read but nothing was copied without re-derivation; the Euler
identity, the hull cycle, the families and every self-check below are
re-established here independently.

NORMALISATION.  Oler normalisation throughout: minimum pairwise separation is
**1** and the container side is `a`.  This repo's certificates use separation 2
and side `d = 2a`, so `d = 2a` and `s = d + 2*sqrt(3)`.

WHAT A CONFIGURATION RECORD CONTAINS.  For a finite non-collinear point set E
with pairwise distances >= 1, and a triangulation T of P = conv(E) whose vertex
set is exactly E:

    n     = |E|
    b     = number of points of E on the boundary of P (hull vertices AND
            points lying in the relative interior of a hull edge)
    F     = number of triangles of T
    A     = area of P                     (exact, in Q(sqrt 3))
    M     = perimeter of P                (irrational in general; an exact
                                           rational UPPER bound is stored)
    faces = list of triangles, each with its exact shape key and exact area
    bedges= list of boundary edges, each with an exact rational upper bound on
            its length

Self-checks run on construction (all exact, all assertions):
    (C1) every pairwise distance is >= 1;
    (C2) Euler:  F = 2n - b - 2;
    (C3) the face areas sum exactly to the area of the hull;
    (C4) the boundary edge lengths sum to the hull perimeter (checked via the
         same enclosure used to build both).

DIRECTION OF ROUNDING.  A, M enter the LP through constraints of the form

        c_A * A + c_L * M + 1 >= n,

which are NECESSARY conditions on any member of the score family.  Using an
UPPER bound for A and M weakens the constraint, enlarging the LP's feasible set.
That makes the LP an optimistic relaxation of the family, which is the direction
that makes a negative answer meaningful.  So all rounding here is outward/up.
"""

from fractions import Fraction as Fr
from math import isqrt

# --------------------------------------------------------------------------
# Q(sqrt 3):  an element is a pair (u, v) of Fractions meaning u + v*sqrt(3).
# --------------------------------------------------------------------------

ZERO = (Fr(0), Fr(0))


def K(u=0, v=0):
    return (Fr(u), Fr(v))


def kadd(x, y):
    return (x[0] + y[0], x[1] + y[1])


def ksub(x, y):
    return (x[0] - y[0], x[1] - y[1])


def kmul(x, y):
    return (x[0] * y[0] + 3 * x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def kneg(x):
    return (-x[0], -x[1])


def ksign(x):
    """Exact sign of u + v*sqrt(3).  sqrt(3) is irrational, so u + v*sqrt3 == 0
    iff u == v == 0."""
    u, v = x
    if u == 0 and v == 0:
        return 0
    if u == 0:
        return 1 if v > 0 else -1
    if v == 0:
        return 1 if u > 0 else -1
    if u > 0 and v > 0:
        return 1
    if u < 0 and v < 0:
        return -1
    # opposite signs: compare u^2 against 3 v^2 (never equal, sqrt3 irrational)
    big_u = u * u > 3 * v * v
    if u > 0:                      # u > 0 > v: positive iff |u| > sqrt3 |v|
        return 1 if big_u else -1
    return -1 if big_u else 1      # u < 0 < v


def kcmp(x, y):
    return ksign(ksub(x, y))


# Rational bounds for sqrt(3), certified by the assertion in _selftest_field().
#
# The Archimedes pair 265/153 < sqrt3 < 1351/780 is only good to 4.7e-7, and at
# that width the outward rounding of the lattice areas shifts the LP optimum by
# ~8e-7 in d -- enough to fake a spurious "beats Oler by 1e-6".  That is exactly
# the kind of artifact this repo keeps logging, so the bounds are computed to
# 10^-40 instead.  (The abandoned r3-delaunay scaffolding also has the
# Archimedes pair SWAPPED; do not copy them from there.)
_S3_DEN = 10 ** 40
_S3_LO = Fr(isqrt(3 * _S3_DEN * _S3_DEN), _S3_DEN)
_S3_HI = Fr(isqrt(3 * _S3_DEN * _S3_DEN) + 1, _S3_DEN)


def kbounds(x):
    """Rational (lo, hi) with lo <= u + v*sqrt3 <= hi."""
    u, v = x
    if v >= 0:
        return (u + v * _S3_LO, u + v * _S3_HI)
    return (u + v * _S3_HI, u + v * _S3_LO)


def kfloat(x):
    return float(x[0]) + 1.7320508075688772 * float(x[1])


def rat_sqrt_up(x, denom=10 ** 30):
    """Rational UPPER bound for sqrt(x), x a non-negative Fraction."""
    assert x >= 0
    num = x.numerator * denom * denom
    den = x.denominator
    r = isqrt(num // den) + 1
    out = Fr(r, denom)
    assert out * out >= x
    return out


def ksqrt_up(x, denom=10 ** 30):
    """Rational UPPER bound for sqrt(u + v*sqrt3), the argument being >= 0."""
    lo, hi = kbounds(x)
    assert lo >= 0 or ksign(x) >= 0
    return rat_sqrt_up(max(hi, Fr(0)), denom)


def _selftest_field():
    # sqrt(3) bounds
    assert _S3_LO * _S3_LO < 3 < _S3_HI * _S3_HI
    # sign predicate on a few known elements
    assert ksign(ksub(K(0, 1), K(17, 0))) < 0          # sqrt3 < 17
    assert ksign(ksub(K(0, 1), K(1, 0))) > 0           # sqrt3 > 1
    assert ksign(ksub(K(0, 2), K(7, 0))) < 0           # 2 sqrt3 < 7
    assert ksign(ksub(K(0, 2), K(3, 0))) > 0           # 2 sqrt3 > 3
    assert ksign(K(0, 0)) == 0
    # (1+sqrt3)^2 = 4 + 2 sqrt3
    assert kmul(K(1, 1), K(1, 1)) == K(4, 2)
    assert rat_sqrt_up(Fr(2)) ** 2 >= 2


_selftest_field()


# --------------------------------------------------------------------------
# planar geometry, exact
# --------------------------------------------------------------------------

def d2(p, q):
    """Exact squared distance in Q(sqrt3)."""
    dx = ksub(p[0], q[0])
    dy = ksub(p[1], q[1])
    return kadd(kmul(dx, dx), kmul(dy, dy))


def cross(o, p, q):
    """Exact 2*signed area of triangle (o,p,q)."""
    return ksub(kmul(ksub(p[0], o[0]), ksub(q[1], o[1])),
                kmul(ksub(p[1], o[1]), ksub(q[0], o[0])))


def twice_area(poly):
    """|shoelace| of a simple polygon given in order; exact, >= 0."""
    s = ZERO
    m = len(poly)
    for i in range(m):
        p, q = poly[i], poly[(i + 1) % m]
        s = kadd(s, ksub(kmul(p[0], q[1]), kmul(q[0], p[1])))
    return s if ksign(s) >= 0 else kneg(s)


def _lex_less(p, q):
    c = kcmp(p[0], q[0])
    if c != 0:
        return c < 0
    return kcmp(p[1], q[1]) < 0


def hull_cycle(pts):
    """Boundary cycle of conv(pts) in ccw order, INCLUDING points that lie in
    the relative interior of a hull edge.  Andrew monotone chain with exact
    predicates; collinear points are kept because the turn test is strict."""
    P = list(pts)
    # exact insertion sort (small inputs; correctness over speed)
    for i in range(1, len(P)):
        j = i
        while j > 0 and _lex_less(P[j], P[j - 1]):
            P[j], P[j - 1] = P[j - 1], P[j]
            j -= 1
    # drop exact duplicates
    Q = [P[0]]
    for p in P[1:]:
        if p != Q[-1]:
            Q.append(p)
    P = Q
    assert len(P) >= 3

    def build(seq):
        out = []
        for p in seq:
            while len(out) >= 2 and ksign(cross(out[-2], out[-1], p)) < 0:
                out.pop()
            out.append(p)
        return out

    lower = build(P)
    upper = build(list(reversed(P)))
    cyc = lower[:-1] + upper[:-1]
    assert len(cyc) >= 3
    return cyc


# --------------------------------------------------------------------------
# configuration record
# --------------------------------------------------------------------------

class Config:
    """A point set together with a triangulation of its convex hull."""

    def __init__(self, name, pts, faces, note=""):
        self.name = name
        self.pts = list(pts)
        self.faces = [tuple(f) for f in faces]
        self.note = note
        self.n = len(self.pts)

        # (C1) separation >= 1, exact.  Float pre-screen then exact recheck.
        fl = [(kfloat(p[0]), kfloat(p[1])) for p in self.pts]
        self.minsep2 = None
        for i in range(self.n):
            for j in range(i + 1, self.n):
                dxf = fl[i][0] - fl[j][0]
                dyf = fl[i][1] - fl[j][1]
                if dxf * dxf + dyf * dyf < 4.0:
                    s2 = d2(self.pts[i], self.pts[j])
                    assert ksign(ksub(s2, K(1))) >= 0, \
                        f"{name}: points {i},{j} closer than 1"
                    if self.minsep2 is None or kcmp(s2, self.minsep2) < 0:
                        self.minsep2 = s2
        if self.minsep2 is None:
            self.minsep2 = K(4)

        # hull cycle, b, and (C2) Euler
        self.cycle = hull_cycle(self.pts)
        self.b = len(self.cycle)
        self.F = len(self.faces)
        assert self.F == 2 * self.n - self.b - 2, \
            f"{name}: Euler check failed, F={self.F}, 2n-b-2={2*self.n-self.b-2}"

        # (C3) face areas tile the hull, exactly
        ta_hull = twice_area(self.cycle)
        ta_faces = ZERO
        for f in self.faces:
            ta_faces = kadd(ta_faces, twice_area(list(f)))
        assert ta_hull == ta_faces, f"{name}: faces do not tile conv(E)"
        self.twice_area_hull = ta_hull
        self.area = kmul(K(Fr(1, 2)), ta_hull)          # exact, in Q(sqrt3)
        self.area_up = kbounds(self.area)[1]            # rational upper bound

        # boundary edges: exact squared lengths, rational upper bounds
        self.bedge_len2 = []
        self.bedge_len_up = []
        per_up = Fr(0)
        for i in range(self.b):
            e2 = d2(self.cycle[i], self.cycle[(i + 1) % self.b])
            self.bedge_len2.append(e2)
            L = ksqrt_up(e2)
            self.bedge_len_up.append(L)
            per_up += L
        self.perim_up = per_up

        # per-face shape key (sorted exact squared side lengths) and exact area
        self.face_shapes = []
        for f in self.faces:
            s2 = [d2(f[0], f[1]), d2(f[1], f[2]), d2(f[0], f[2])]
            s2.sort(key=lambda z: (kbounds(z), z))
            fa = kmul(K(Fr(1, 2)), twice_area(list(f)))
            self.face_shapes.append((tuple(s2), fa))

    # -- the Oler linear member, evaluated exactly on this configuration -----
    def oler_terms(self):
        """(face excess, boundary-edge excess) for the Oler score, as rational
        enclosures.  face excess = sum_f ((2/sqrt3) A_f - 1/2)
                                 = (2/sqrt3) A(P) - F/2, exact in Q(sqrt3);
        edge excess = sum_e (l_e - 1)/2, enclosed."""
        # (2/sqrt3) x = (2/3) sqrt3 x
        fe = ksub(kmul(K(0, Fr(2, 3)), self.area), K(Fr(self.F, 2)))
        be_up = (self.perim_up - self.b) / 2
        return fe, be_up

    def summary(self):
        fe, be_up = self.oler_terms()
        return dict(name=self.name, n=self.n, b=self.b, F=self.F,
                    A=float(kfloat(self.area)), M_up=float(self.perim_up),
                    face_excess=float(kfloat(fe)), edge_excess_up=float(be_up),
                    oler_slack_up=float(kfloat(fe)) + float(be_up))


# --------------------------------------------------------------------------
# families
# --------------------------------------------------------------------------

def _lat(i, j):
    """Triangular-lattice point i*(1,0) + j*(1/2, sqrt3/2), spacing 1."""
    return (K(Fr(i) + Fr(j, 2), 0), K(0, Fr(j, 2)))


def cfg_lattice(m):
    """T(m+1): all i,j >= 0 with i + j <= m.  n = (m+1)(m+2)/2, hull is the
    equilateral triangle of side a = m."""
    idx = [(i, j) for j in range(m + 1) for i in range(m + 1 - j)]
    pos = {k: _lat(*k) for k in idx}
    faces = []
    for j in range(m):
        for i in range(m - j):
            faces.append((pos[(i, j)], pos[(i + 1, j)], pos[(i, j + 1)]))
    for j in range(m - 1):
        for i in range(m - 1 - j):
            faces.append((pos[(i + 1, j)], pos[(i, j + 1)], pos[(i + 1, j + 1)]))
    return Config(f"lattice T({m+1})", list(pos.values()), faces,
                  note=f"triangular lattice, a={m}, Oler-tight")


def cfg_lattice_minus_apex(m):
    """T(m+1) with the apex (0,m) deleted -- the Erdos-Oler witness."""
    idx = [(i, j) for j in range(m + 1) for i in range(m + 1 - j)]
    idx.remove((0, m))
    pos = {k: _lat(*k) for k in idx}
    faces = []
    for j in range(m):
        for i in range(m - j):
            t = ((i, j), (i + 1, j), (i, j + 1))
            if all(k in pos for k in t):
                faces.append(tuple(pos[k] for k in t))
    for j in range(m - 1):
        for i in range(m - 1 - j):
            t = ((i + 1, j), (i, j + 1), (i + 1, j + 1))
            if all(k in pos for k in t):
                faces.append(tuple(pos[k] for k in t))
    return Config(f"lattice T({m+1}) - apex", list(pos.values()), faces,
                  note="Erdos-Oler witness, n = T(k)-1")


def cfg_parallelogram(p, q):
    """p rows by q columns of the triangular lattice; hull is a rhombus."""
    assert p >= 2 and q >= 2
    pos = {(i, j): _lat(i, j) for j in range(p) for i in range(q)}
    faces = []
    for j in range(p - 1):
        for i in range(q - 1):
            faces.append((pos[(i, j)], pos[(i + 1, j)], pos[(i, j + 1)]))
            faces.append((pos[(i + 1, j)], pos[(i + 1, j + 1)], pos[(i, j + 1)]))
    return Config(f"rhombus {p}x{q}", list(pos.values()), faces,
                  note="lattice patch; forces the area coefficient")


def cfg_flat_arc(m):
    """p_j = (j, j(m-j)/m^3), j = 0..m.  Strictly concave so every point is a
    hull vertex; consecutive gaps >= 1; hull area is O(1) while n grows.  This
    is the family that forces the boundary-LENGTH coefficient (it is the
    witness family recorded in attacks/oler-slack-analysis)."""
    pts = [(K(Fr(j), 0), K(Fr(j * (m - j), m ** 3), 0)) for j in range(m + 1)]
    faces = [(pts[0], pts[j], pts[j + 1]) for j in range(1, m)]
    return Config(f"flat arc m={m}", pts, faces,
                  note="thin convex arc; forces the perimeter coefficient")


def cfg_corners_centroid():
    """Equilateral triangle of side sqrt(3) plus its centroid; separation 1."""
    A = (K(0, 0), K(0, 0))
    B = (K(0, 1), K(0, 0))
    C = (K(0, Fr(1, 2)), K(Fr(3, 2), 0))
    G = (K(0, Fr(1, 2)), K(Fr(1, 2), 0))
    return Config("corners+centroid n=4", [A, B, C, G],
                  [(A, B, G), (B, C, G), (C, A, G)],
                  note="hull = container; all Oler slack is stage 1")


def library(size=8):
    """The constraint library at refinement level `size`.  Larger `size` = more
    and bigger configurations = MORE constraints = a tighter (less optimistic)
    LP.  `size` is the largest lattice index m, the largest rhombus dimension,
    and the largest arc index m."""
    cfgs = [cfg_corners_centroid()]
    for m in range(1, size + 1):
        cfgs.append(cfg_lattice(m))
        if m >= 2:
            cfgs.append(cfg_lattice_minus_apex(m))
    for p in range(2, min(size, 6) + 1):
        for q in range(2, size + 1):
            if p <= q:
                cfgs.append(cfg_parallelogram(p, q))
    for m in range(3, size + 1):
        cfgs.append(cfg_flat_arc(m))
    return cfgs
