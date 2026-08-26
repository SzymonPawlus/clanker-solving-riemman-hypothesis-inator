"""Exact lattice geometry for dyadic subdivisions of the unit equilateral triangle.

Container (problem RULES.md sec.2 placement, scaled to side 1):
    A=(0,0), B=(1,0), C=(1/2, sqrt3/2), CLOSED.

Everything here is written from the problem statement.  Nothing is imported or
adapted from experiments/packing-eo-exhaustion/ (read for its *results*, not its
code); the four-way subdivision and the integer form a^2+ab+b^2 are forced by the
mathematics, not copied.

LATTICE COORDINATES.  At level L put h = 2^-L, u = (h,0), v = (h/2, h*sqrt3/2).
A lattice point (i,j) means i*u + j*v.  The map (i,j) -> i*u+j*v is linear with
determinant h^2*sqrt3/2 > 0, so it is an orientation-preserving affine bijection:
convex hulls, containment and betweenness may all be computed on integer (i,j).

    up(L,i,j)   = triangle with vertices (i,j), (i+1,j), (i,j+1)
    down(L,i,j) = triangle with vertices (i+1,j), (i,j+1), (i+1,j+1)

The level-L cells of the container are up(L,i,j) for i,j>=0, i+j <= 2^L-1, and
down(L,i,j) for i,j>=0, i+j <= 2^L-2.  Their union is the closed container and
their interiors are disjoint (standard four-way subdivision).

SQUARED DISTANCE.  |a*u + b*v|^2 = h^2 * (a^2 + a*b + b^2).  Integer form.
"""
from fractions import Fraction
from math import isqrt

UP, DOWN = 0, 1


def cell_vertices(cell):
    """Vertices of a cell, in its own level's lattice coordinates."""
    o, i, j = cell[1], cell[2], cell[3]
    if o == UP:
        return ((i, j), (i + 1, j), (i, j + 1))
    return ((i + 1, j), (i, j + 1), (i + 1, j + 1))


def root_cell():
    return (0, UP, 0, 0)


def children(cell):
    """The four level-(L+1) children of a cell.

    Derived, not copied.  Write the parent's vertices in level-(L+1) coordinates
    (double them).  The four children are the three corner triangles cut off by
    the edge midpoints, plus the medial triangle.

    up(L,i,j): vertices double to (2i,2j),(2i+2,2j),(2i,2j+2); midpoints
      (2i+1,2j),(2i,2j+1),(2i+1,2j+1).  Corner children are up(2i,2j),
      up(2i+1,2j), up(2i,2j+1); the medial triangle has vertices
      (2i+1,2j),(2i,2j+1),(2i+1,2j+1) = down(2i,2j).

    down(L,i,j): vertices double to (2i+2,2j),(2i,2j+2),(2i+2,2j+2); midpoints
      (2i+1,2j+1),(2i+2,2j+1),(2i+1,2j+2).  Corner children are down(2i+1,2j),
      down(2i,2j+1), down(2i+1,2j+1); the medial triangle has vertices
      (2i+1,2j+1),(2i+2,2j+1),(2i+1,2j+2) = up(2i+1,2j+1).
    """
    L, o, i, j = cell
    if o == UP:
        return ((L + 1, UP, 2 * i, 2 * j), (L + 1, UP, 2 * i + 1, 2 * j),
                (L + 1, UP, 2 * i, 2 * j + 1), (L + 1, DOWN, 2 * i, 2 * j))
    return ((L + 1, DOWN, 2 * i + 1, 2 * j), (L + 1, DOWN, 2 * i, 2 * j + 1),
            (L + 1, DOWN, 2 * i + 1, 2 * j + 1), (L + 1, UP, 2 * i + 1, 2 * j + 1))


def verts_at(cell, ref_level):
    """Cell vertices expressed in the level-`ref_level` lattice (ref_level >= L)."""
    s = 1 << (ref_level - cell[0])
    return tuple((s * a, s * b) for a, b in cell_vertices(cell))


def qform(p, q):
    a = p[0] - q[0]
    b = p[1] - q[1]
    return a * a + a * b + b * b


def maxq(vx, vy):
    """max over vertex pairs of the integer form; = maxsep^2 / h_ref^2.

    Squared Euclidean distance is a convex function on the product of two
    polytopes, so its maximum over closed triangles X x Y is attained at a
    vertex pair.  Scanning the 9 pairs is therefore exact.
    """
    return max(qform(p, q) for p in vx for q in vy)


def sqrt_upper(q, scale=10 ** 9):
    """Rational upper bound for sqrt(q) (q a non-negative integer), EXACT when q
    is a perfect square.  Exactness matters: the Oler-hull rule is tight to the
    last digit at the configurations that decide these cases, and an overshoot
    of 1e-7 is enough to stop it firing."""
    r0 = isqrt(q)
    if r0 * r0 == q:
        return Fraction(r0)
    r = isqrt(q * scale * scale)
    return Fraction(r + 1, scale)


def convex_hull(points):
    """Andrew monotone chain on integer lattice coordinates."""
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def hull_area2(hull):
    """Twice the shoelace area, in lattice coordinates (an integer)."""
    s = 0
    m = len(hull)
    for k in range(m):
        x1, y1 = hull[k]
        x2, y2 = hull[(k + 1) % m]
        s += x1 * y2 - x2 * y1
    return abs(s)


def hull_perimeter_upper(hull):
    """Rational upper bound for the perimeter, in units of h_ref."""
    if len(hull) < 2:
        return Fraction(0)
    tot = Fraction(0)
    m = len(hull)
    for k in range(m):
        tot += sqrt_upper(qform(hull[k], hull[(k + 1) % m]))
    return tot
