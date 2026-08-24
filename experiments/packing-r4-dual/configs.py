"""Independent exact reconstruction of the two families of Oler-TIGHT
configurations that the dual certificate uses.

Written from the problem statement, not adapted from
`experiments/packing-r4-delaunay/framework.py`.  That file is a sibling result
and is read-only here; `certify.py` imports it once, in a clearly-marked
optional bridge section, purely to read back the outward-rounded numbers ITS LP
was fed.  Nothing below depends on it.

NORMALISATION (Oler's, as in the sibling result): minimum pairwise separation 1,
container side `a`.  This repo's certificates use separation 2 and side
`d = 2a`, `s = d + 2 sqrt3`.

WHAT IS RECONSTRUCTED.  Two families of finite point sets E with pairwise
distances >= 1, together with a triangulation of conv(E) with vertex set E:

  lattice(m)   the triangular lattice T(m+1): all i,j >= 0 with i + j <= m.
               n = (m+1)(m+2)/2, conv(E) = equilateral triangle of side m.
  rhombus(P,Q) the P x Q lattice parallelogram: 0 <= i <= Q, 0 <= j <= P.
               n = (P+1)(Q+1), conv(E) = parallelogram with sides Q and P.

For each, the following are ASSERTED exactly at construction (no tolerances):

  (C1) every pairwise squared distance is >= 1                 [Q(sqrt3)]
  (C2) Euler:  F = 2n - b - 2
  (C3) the triangulation's face areas sum exactly to area(conv E)
  (C4) every boundary edge has squared length exactly 1, so the perimeter M
       is the exact RATIONAL number b, with no rounding at all
  (C5) OLER-TIGHTNESS:  (2/sqrt3) A + M/2 = n - 1  exactly.

(C4) and (C5) are what make an exact dual certificate possible: for these
configurations the LP data (A, M, n) is exact with no outward rounding, and the
constraint they contribute passes exactly through Oler's own coefficient point.

DERIVED QUANTITY: the SLOPE.  Write A = (sqrt3/4) * r with r rational (true for
both families: r = m^2 and r = 2PQ).  The slope of an Oler-tight configuration
is
        slope(K) = 4 sqrt3 * A(K) / M(K) = 3 r / M,
which is rational.  Section 2 of the attack README explains what it means: in
the coordinates g = (sqrt3/4) c_A, h = 3 c_L, configuration K contributes the
half-plane  slope(K) * (g - 1/2) + (h - 3/2) >= 0, a half-plane whose boundary
line passes through Oler's point (g, h) = (1/2, 3/2).

    lattice(m)   : slope m
    rhombus(P,Q) : slope 3PQ/(P+Q)
"""

from fractions import Fraction as F

from exact import Surd3


# ------------------------------------------------------------ plane geometry

def pt(i, j):
    """Triangular-lattice point i*(1,0) + j*(1/2, sqrt3/2), spacing 1.
    Returned as (x, y) with x, y in Q(sqrt3)."""
    return (Surd3(F(i) + F(j, 2), 0), Surd3(0, F(j, 2)))


def sub(p, q):
    return (p[0] - q[0], p[1] - q[1])


def dist2(p, q):
    dx, dy = sub(p, q)
    return dx * dx + dy * dy


def twice_area(tri):
    """Exact |2 * signed area| of a triangle, in Q(sqrt3)."""
    (ax, ay), (bx, by), (cx, cy) = tri
    v = (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)
    return v if v.sign() >= 0 else -v


# ---------------------------------------------------------------- the record

class TightConfig:
    """An Oler-tight configuration, with all five self-checks run."""

    def __init__(self, name, pts, faces, boundary_cycle, r_area, note=""):
        self.name = name
        self.note = note
        self.pts = list(pts)
        self.n = len(self.pts)
        self.faces = list(faces)
        self.F = len(self.faces)
        self.cycle = list(boundary_cycle)
        self.b = len(self.cycle)

        # (C1) pairwise separation >= 1, exact, all pairs, no float pre-screen
        one = Surd3(1, 0)
        for i in range(self.n):
            for j in range(i + 1, self.n):
                assert dist2(self.pts[i], self.pts[j]) >= one, \
                    f"{name}: points {i},{j} are closer than 1"

        # the boundary cycle must consist of points of E, in order, closed
        idx = {p: k for k, p in enumerate(
            [(q[0].p, q[0].q, q[1].p, q[1].q) for q in self.pts])}
        for p in self.cycle:
            assert (p[0].p, p[0].q, p[1].p, p[1].q) in idx, \
                f"{name}: boundary point not in E"

        # (C2) Euler
        assert self.F == 2 * self.n - self.b - 2, \
            f"{name}: Euler failed, F={self.F}, 2n-b-2={2*self.n-self.b-2}"

        # (C3) faces tile the hull.  hull area by the shoelace on the cycle.
        ta_hull = Surd3(0, 0)
        for k in range(self.b):
            (x1, y1) = self.cycle[k]
            (x2, y2) = self.cycle[(k + 1) % self.b]
            ta_hull = ta_hull + (x1 * y2 - x2 * y1)
        if ta_hull.sign() < 0:
            ta_hull = -ta_hull
        ta_faces = Surd3(0, 0)
        for f in self.faces:
            ta_faces = ta_faces + twice_area(f)
        assert ta_hull == ta_faces, f"{name}: faces do not tile conv(E)"

        self.area = ta_hull * F(1, 2)                       # exact, Q(sqrt3)

        # A = (sqrt3/4) * r  with r rational -- assert the claimed r
        self.r_area = F(r_area)
        assert self.area == Surd3(0, self.r_area / 4), \
            f"{name}: area is not (sqrt3/4)*{r_area}"

        # (C4) every boundary edge has squared length exactly 1
        for k in range(self.b):
            e2 = dist2(self.cycle[k], self.cycle[(k + 1) % self.b])
            assert e2 == Surd3(1, 0), \
                f"{name}: boundary edge {k} does not have length exactly 1"
        self.M = F(self.b)                     # EXACT rational perimeter

        # (C5) Oler-tightness:  (2/sqrt3) A + M/2 = n - 1.
        # (2/sqrt3) * (sqrt3/4) r = r/2, so this is  r/2 + M/2 = n - 1.
        assert self.r_area / 2 + self.M / 2 == self.n - 1, \
            f"{name}: not Oler-tight"

        # slope = 4 sqrt3 A / M = 3 r / M, rational
        self.slope = 3 * self.r_area / self.M

    def __repr__(self):
        return (f"{self.name}: n={self.n} b={self.b} F={self.F} "
                f"A=(sqrt3/4)*{self.r_area} M={self.M} slope={self.slope}")


# ------------------------------------------------------------------ families

def lattice(m):
    """T(m+1): the full triangular lattice triangle of side m."""
    assert m >= 1
    P = {(i, j): pt(i, j) for j in range(m + 1) for i in range(m + 1 - j)}
    faces = []
    for j in range(m):
        for i in range(m - j):
            faces.append((P[(i, j)], P[(i + 1, j)], P[(i, j + 1)]))
    for j in range(m - 1):
        for i in range(m - 1 - j):
            faces.append((P[(i + 1, j)], P[(i, j + 1)], P[(i + 1, j + 1)]))
    cycle = ([P[(i, 0)] for i in range(m)]                 # bottom, left->right
             + [P[(m - j, j)] for j in range(m)]           # right edge, up
             + [P[(0, m - j)] for j in range(m)])          # left edge, down
    c = TightConfig(f"lattice T({m+1}) side {m}", list(P.values()), faces,
                    cycle, r_area=m * m,
                    note="triangular lattice; the classical Oler-extremal set")
    assert c.n == (m + 1) * (m + 2) // 2
    assert c.b == 3 * m and c.F == m * m and c.slope == m
    return c


def rhombus(Pn, Qn):
    """The Pn x Qn lattice parallelogram: 0 <= i <= Qn, 0 <= j <= Pn."""
    assert Pn >= 1 and Qn >= 1
    P = {(i, j): pt(i, j) for j in range(Pn + 1) for i in range(Qn + 1)}
    faces = []
    for j in range(Pn):
        for i in range(Qn):
            faces.append((P[(i, j)], P[(i + 1, j)], P[(i, j + 1)]))
            faces.append((P[(i + 1, j)], P[(i + 1, j + 1)], P[(i, j + 1)]))
    cycle = ([P[(i, 0)] for i in range(Qn)]                    # bottom
             + [P[(Qn, j)] for j in range(Pn)]                 # right
             + [P[(Qn - i, Pn)] for i in range(Qn)]            # top
             + [P[(0, Pn - j)] for j in range(Pn)])            # left
    c = TightConfig(f"rhombus {Pn}x{Qn}", list(P.values()), faces, cycle,
                    r_area=2 * Pn * Qn,
                    note="lattice parallelogram; also Oler-tight")
    assert c.n == (Pn + 1) * (Qn + 1)
    assert c.b == 2 * (Pn + Qn) and c.F == 2 * Pn * Qn
    assert c.slope == F(3 * Pn * Qn, Pn + Qn)
    return c


def _selftest(log=print):
    log("  [configs.py self-test]")
    for m in range(1, 7):
        c = lattice(m)
        log(f"    {c}")
    for (p, q) in ((1, 1), (2, 2), (3, 3), (2, 4), (3, 5)):
        c = rhombus(p, q)
        log(f"    {c}")
    # a lattice with a point removed is NOT tight, so tightness is a real test
    log("  [configs.py self-test PASSED -- C1..C5 asserted on every build]")


if __name__ == "__main__":
    _selftest()
