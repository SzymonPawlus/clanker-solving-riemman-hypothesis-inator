"""Exact integer geometry of the four-way subdivision of the container triangle.

Container (problem `RULES.md` §2, point formulation, separation 2):

    A = (0,0),  B = (d,0),  C = (d/2, d*sqrt(3)/2),   closed triangle, side d.

Level-L subdivision.  Put h = d/2**L and

    u = (h, 0),      v = (h/2, h*sqrt(3)/2).

Lattice coordinates (i, j) mean the point i*u + j*v.  A level-L cell is
``(L, orient, i, j)``:

    up(i,j)   : vertices (i,j),   (i+1,j),   (i,j+1)
    down(i,j) : vertices (i+1,j), (i,j+1),   (i+1,j+1)

Children (re-derived here from the vertex formulas, not copied):

    up(i,j)  -> up(2i,2j), up(2i+1,2j), up(2i,2j+1), down(2i,2j)
    down(i,j)-> down(2i+1,2j), down(2i,2j+1), down(2i+1,2j+1), up(2i+1,2j+1)

Derivation for ``up``: the parent's vertices in the level-(L+1) lattice are
(2i,2j), (2i+2,2j), (2i,2j+2); the three edge midpoints are (2i+1,2j), (2i,2j+1),
(2i+1,2j+1).  The three corner sub-triangles are the three ``up`` cells listed and
the middle one has vertices (2i+1,2j), (2i,2j+1), (2i+1,2j+1) = down(2i,2j).  The
four are closed and their union is the closed parent, so no configuration can fall
between children.  ``down`` is identical after the point reflection that swaps the
two orientations.

Distances.  |u| = |v| = h and u.v = h**2/2, so for a lattice displacement (a,b)

    |a*u + b*v|**2 = h**2 * (a**2 + a*b + b**2)

which is an integer multiple of h**2 -- the whole pair test is integer arithmetic.

Areas.  det[u v] = h * h*sqrt(3)/2 > 0, so the linear map (i,j) -> i*u + j*v is
orientation preserving and convex hulls may be computed in (i,j) coordinates
directly.  A polygon with lattice-coordinate shoelace area ``A_lat`` has true area
``(sqrt(3)/2) * h**2 * A_lat``.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Iterable

UP = 0
DOWN = 1

# A cell is the 4-tuple (level, orient, i, j).
Cell = tuple[int, int, int, int]


def cell_vertices(cell: Cell) -> tuple[tuple[int, int], tuple[int, int], tuple[int, int]]:
    _, orient, i, j = cell
    if orient == UP:
        return ((i, j), (i + 1, j), (i, j + 1))
    return ((i + 1, j), (i, j + 1), (i + 1, j + 1))


def children(cell: Cell) -> tuple[Cell, Cell, Cell, Cell]:
    L, orient, i, j = cell
    n = L + 1
    if orient == UP:
        return (
            (n, UP, 2 * i, 2 * j),
            (n, UP, 2 * i + 1, 2 * j),
            (n, UP, 2 * i, 2 * j + 1),
            (n, DOWN, 2 * i, 2 * j),
        )
    return (
        (n, DOWN, 2 * i + 1, 2 * j),
        (n, DOWN, 2 * i, 2 * j + 1),
        (n, DOWN, 2 * i + 1, 2 * j + 1),
        (n, UP, 2 * i + 1, 2 * j + 1),
    )


def cells_at_level(L: int) -> list[Cell]:
    """All 4**L closed cells of the level-L subdivision of the container."""
    m = 1 << L
    out: list[Cell] = []
    for i in range(m):
        for j in range(m - i):
            out.append((L, UP, i, j))
    for i in range(m - 1):
        for j in range(m - 1 - i):
            out.append((L, DOWN, i, j))
    return out


def _rescale(cell: Cell, target: int) -> tuple[tuple[int, int], ...]:
    """Vertices of ``cell`` expressed in the level-``target`` lattice (target >= level)."""
    L = cell[0]
    f = 1 << (target - L)
    return tuple((a * f, b * f) for a, b in cell_vertices(cell))


def norm2(a: int, b: int) -> int:
    """|a*u + b*v|**2 / h**2, an integer."""
    return a * a + a * b + b * b


def max_sep_form(c1: Cell, c2: Cell) -> tuple[int, int]:
    """Return (Q, L) with max distance between the closed cells = (d/2**L)*sqrt(Q).

    The maximum of a convex function (squared distance) over a product of polytopes
    is attained at a pair of vertices, so scanning the nine vertex pairs is exact.
    """
    L = max(c1[0], c2[0])
    v1 = _rescale(c1, L)
    v2 = _rescale(c2, L)
    best = 0
    for a1, b1 in v1:
        for a2, b2 in v2:
            q = norm2(a2 - a1, b2 - b1)
            if q > best:
                best = q
    return best, L


def side_fraction(d: Fraction, L: int) -> Fraction:
    """Side length h = d / 2**L of a level-L cell."""
    return d / (1 << L)


def pair_compatible(c1: Cell, c2: Cell, d: Fraction) -> bool:
    """Can two DISTINCT points, one in each closed cell, be at distance >= 2?

    True iff the maximum separation of the two closed cells is >= 2.  Exact integer
    comparison: with d = p/q and h = d/2**L, the test is p**2 * Q >= 4 * q**2 * 4**L.
    """
    Q, L = max_sep_form(c1, c2)
    p, q = d.numerator, d.denominator
    return p * p * Q >= 4 * q * q * (1 << (2 * L))


# ------------------------------------------------------------------ convex hull


def convex_hull(points: Iterable[tuple[int, int]]) -> list[tuple[int, int]]:
    """Andrew monotone chain in lattice coordinates (exact integers)."""
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts

    def cross(o, a, b) -> int:
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower: list[tuple[int, int]] = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper: list[tuple[int, int]] = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def shoelace_twice_area(hull: list[tuple[int, int]]) -> int:
    """Twice the lattice-coordinate area of a hull, as a non-negative integer."""
    n = len(hull)
    if n < 3:
        return 0
    s = 0
    for k in range(n):
        x1, y1 = hull[k]
        x2, y2 = hull[(k + 1) % n]
        s += x1 * y2 - x2 * y1
    return abs(s)


def hull_edge_forms(hull: list[tuple[int, int]]) -> list[int]:
    """The integers Q_e with edge length = h * sqrt(Q_e)."""
    n = len(hull)
    if n < 2:
        return []
    if n == 2:
        (x1, y1), (x2, y2) = hull
        return [norm2(x2 - x1, y2 - y1), norm2(x1 - x2, y1 - y2)]
    out = []
    for k in range(n):
        x1, y1 = hull[k]
        x2, y2 = hull[(k + 1) % n]
        out.append(norm2(x2 - x1, y2 - y1))
    return out
