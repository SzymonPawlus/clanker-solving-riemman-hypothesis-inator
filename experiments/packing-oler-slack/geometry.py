"""Exact planar geometry over Q(sqrt3, sqrt11), and the Oler slack decomposition.

Conventions follow `problems/circle-packing-equilateral-triangle/RULES.md` §2 for
certificates, except for one deliberate rescaling stated everywhere it is used:
Oler's inequality is normalised to **minimum separation 1**, while certificates
use minimum separation 2, so certificate coordinates are halved on load.

The decomposition being computed, for a finite non-collinear point set E with
hull P and any triangulation of P whose vertex set is exactly E:

    (2/sqrt3) A(P) + (1/2) M(P) + 1 - |E|
        = sum_faces (2/sqrt3)(A_f - sqrt3/4) + sum_boundary_edges (1/2)(len_e - 1)

The left-hand side is Oler's slack.  The two right-hand sums are the *face
excess* and the *boundary-edge excess*.  Nothing here assumes the separation
condition; the identity is combinatorial.  Oler's theorem is the statement that
the left-hand side is >= 0 when the separation is >= 1.
"""

from fractions import Fraction as F

from exact import Alg, Ival, ZERO

# --- primitives ------------------------------------------------------------


def orient(a, b, c):
    """Sign of the cross product (b-a) x (c-a): +1 left turn, -1 right, 0 collinear."""
    return ((b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])).sign()


def twice_area(poly):
    """Exact 2*area of a simple polygon given as a CCW vertex list."""
    total = ZERO
    for i, p in enumerate(poly):
        q = poly[(i + 1) % len(poly)]
        total = total + (p[0] * q[1] - q[0] * p[1])
    return total


def dist2(p, q):
    dx, dy = p[0] - q[0], p[1] - q[1]
    return dx * dx + dy * dy


def min_separation2(points):
    """Exact minimum squared pairwise distance."""
    best = None
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            d2 = dist2(points[i], points[j])
            if best is None or d2 < best:
                best = d2
    return best


def convex_hull(points):
    """Andrew monotone chain; returns the CCW hull *vertices* (no collinear points)."""
    pts = sorted(set(points), key=lambda p: (p[0], p[1]))
    if len(pts) < 3:
        return pts

    def build(seq):
        chain = []
        for p in seq:
            while len(chain) >= 2 and orient(chain[-2], chain[-1], p) <= 0:
                chain.pop()
            chain.append(p)
        return chain

    lower = build(pts)
    upper = build(reversed(pts))
    return lower[:-1] + upper[:-1]


def on_segment(a, b, p):
    """True if p lies strictly between a and b on the segment ab."""
    if orient(a, b, p) != 0:
        return False
    if p == a or p == b:
        return False
    inner = (p[0] - a[0]) * (b[0] - a[0]) + (p[1] - a[1]) * (b[1] - a[1])
    if inner.sign() <= 0:
        return False
    return inner < dist2(a, b)


def boundary_cycle(points, hull):
    """The boundary points in CCW order, hull edges subdivided by collinear points."""
    cycle = []
    for i, a in enumerate(hull):
        b = hull[(i + 1) % len(hull)]
        cycle.append(a)
        interior = [p for p in points if on_segment(a, b, p)]
        interior.sort(key=lambda p: dist2(a, p))
        cycle.extend(interior)
    return cycle


# --- triangulation ---------------------------------------------------------


def triangulate(points):
    """A triangulation of conv(points) whose vertex set is exactly `points`.

    Fan the strict hull vertices, then insert every remaining point by splitting
    the triangle that contains it (3-way if strictly inside, 2-way per incident
    triangle if it lands on an edge).  Returns a list of CCW vertex triples.
    """
    hull = convex_hull(points)
    if len(hull) < 3:
        raise ValueError("degenerate point set: hull is not a polygon")

    tris = [(hull[0], hull[i], hull[i + 1]) for i in range(1, len(hull) - 1)]
    remaining = [p for p in points if p not in set(hull)]

    for p in remaining:
        inside = None
        on_edge = []
        for t in tris:
            signs = [orient(t[i], t[(i + 1) % 3], p) for i in range(3)]
            if any(s < 0 for s in signs):
                continue
            zeros = [i for i, s in enumerate(signs) if s == 0]
            if not zeros:
                inside = t
                break
            if len(zeros) == 1:
                edge = (t[zeros[0]], t[(zeros[0] + 1) % 3])
                if on_segment(edge[0], edge[1], p):
                    on_edge.append((t, zeros[0]))
        if inside is not None:
            tris.remove(inside)
            a, b, c = inside
            tris += [(a, b, p), (b, c, p), (c, a, p)]
        elif on_edge:
            for t, k in on_edge:
                tris.remove(t)
                a, b, c = t[k], t[(k + 1) % 3], t[(k + 2) % 3]
                tris += [(a, p, c), (p, b, c)]
        else:
            raise RuntimeError(f"point {p} located in no triangle")
    return tris


# --- the decomposition -----------------------------------------------------


class Decomposition:
    """Every quantity in the slack identity, for one point set."""

    def __init__(self, points, label=""):
        self.label = label
        self.points = list(points)
        self.n = len(self.points)
        self.hull = convex_hull(self.points)
        if len(self.hull) < 3:
            raise ValueError("degenerate point set: hull is not a polygon")

        self.cycle = boundary_cycle(self.points, self.hull)
        self.b = len(self.cycle)
        self.interior = self.n - self.b
        self.area = twice_area(self.hull) * F(1, 2)
        self.min_sep2 = min_separation2(self.points)

        self.tris = triangulate(self.points)
        self.faces = len(self.tris)

        # face excess, exactly: sum (2/sqrt3)(A_f - sqrt3/4) = (2 sqrt3/3) A_f - 1/2
        two_over_root3 = Alg(0, F(2, 3), 0, 0)          # 2/sqrt3 = 2 sqrt3 / 3
        self.face_excess = []
        for t in self.tris:
            area_f = twice_area(list(t)) * F(1, 2)
            self.face_excess.append(two_over_root3 * area_f - F(1, 2))
        self.total_face_excess = sum(self.face_excess, ZERO)

        # boundary-edge excess: (1/2)(len_e - 1), lengths enclosed rigorously
        self.edge_len2 = [
            dist2(self.cycle[i], self.cycle[(i + 1) % self.b]) for i in range(self.b)
        ]
        self.edge_len = [Ival.of(l2).sqrt() for l2 in self.edge_len2]
        self.perimeter = sum(self.edge_len[1:], self.edge_len[0])
        self.boundary_excess = sum(
            (F(1, 2) * (l - 1) for l in self.edge_len[1:]),
            F(1, 2) * (self.edge_len[0] - 1),
        )

        # Oler slack, direct from the definition (interval, because M has roots)
        self.slack = (
            Ival.of(two_over_root3 * self.area) + F(1, 2) * self.perimeter + 1 - self.n
        )

    # -- the exact checks
    def check_euler(self):
        """Faces = 2n - b - 2 (the combinatorial half of the identity)."""
        return self.faces == 2 * self.n - self.b - 2

    def check_areas(self):
        """Face areas sum to the hull area (the metric half of the identity)."""
        total = sum(
            (twice_area(list(t)) * F(1, 2) for t in self.tris[1:]),
            twice_area(list(self.tris[0])) * F(1, 2),
        )
        return total == self.area

    def check_sum(self):
        """The two sides of the identity, computed by independent routes, agree.

        The left-hand side comes from A(P), M(P) and n; the right-hand side from
        the triangulation's faces and boundary edges.  Both carry the perimeter,
        so both are enclosures: agreement means the enclosures intersect.
        """
        rhs = Ival.of(self.total_face_excess) + self.boundary_excess
        return not (rhs.hi < self.slack.lo or self.slack.hi < rhs.lo)

    def check_identity(self):
        """All three checks; together they *are* the identity (see module docstring)."""
        return self.check_euler() and self.check_areas() and self.check_sum()

    def summary(self):
        return {
            "label": self.label,
            "n": self.n,
            "boundary_points": self.b,
            "interior_points": self.interior,
            "faces": self.faces,
            "min_separation_sq": str(self.min_sep2),
            "hull_area": str(self.area),
            "identity_faces_ok": self.check_euler(),
            "identity_areas_ok": self.check_areas(),
            "identity_sum_ok": self.check_sum(),
            "total_face_excess_exact": str(self.total_face_excess),
            "total_face_excess": self.total_face_excess.float(),
            "total_face_excess_sign": self.total_face_excess.sign(),
            "boundary_excess": self.boundary_excess.mid(),
            "oler_slack": self.slack.mid(),
            "oler_slack_enclosure_width": self.slack.width(),
            "negative_faces": sum(1 for e in self.face_excess if e.sign() < 0),
            "zero_faces": sum(1 for e in self.face_excess if e.sign() == 0),
            "positive_faces": sum(1 for e in self.face_excess if e.sign() > 0),
        }
