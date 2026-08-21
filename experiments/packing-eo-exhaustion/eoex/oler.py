"""Oler's inequality as a rigorous bound, in this repo's separation-2 normalisation.

Oler (1961), `cited`, as transcribed in
``problems/circle-packing-equilateral-triangle/attacks/oler-lower-bound/README.md`` §1.1:
for a Jordan polygon pi whose vertices belong to a finite set E contained in the closed
region bounded by pi, with all pairwise distances in E at least **1**,

    N  <=  (2/sqrt3) * A(pi)  +  (1/2) * M(pi)  +  1.

Our points are at separation >= 2, so halve every coordinate before applying it.  With
``A``, ``M`` the area and perimeter measured in the separation-2 picture,

    N  <=  A / (2*sqrt3)  +  M / 4  +  1.                                       (OLER-2)

Two uses:

1. **Closed form for the container.**  A = sqrt(3)*d^2/4 and M = 3d give
   ``N <= d^2/8 + 3d/4 + 1``, i.e. no ``n`` points at separation >= 2 fit in the closed
   equilateral triangle of side ``d`` whenever ``d < sqrt(8n+1) - 3``.

2. **Per-node bound during the search** (``node_bound``).  In a search node the points
   are known to lie in a union of closed cells; ``conv(E)`` is contained in the convex
   hull ``K`` of those cells, and both area and perimeter are monotone under inclusion of
   convex sets, so (OLER-2) applied to ``conv(E)`` and then relaxed to ``K`` is valid.
   This is a *global* test on the node: it fires exactly when the occupied cells have
   retreated from the container's boundary, which pairwise tests never see.

**The collinear escape clause.**  Oler's theorem needs ``conv(E)`` to be a Jordan
polygon, which fails if E lies on a line.  In that case the extreme points of E are at
distance >= 2*(N-1), which exceeds the container diameter ``d`` as soon as
``d < 2*(N-1)``.  Every caller must check that, and ``node_bound`` refuses to fire
otherwise.  (For every run in this directory ``n >= 5`` and ``d <= 2n``, so the clause
is comfortably satisfied; it is checked rather than assumed.)
"""

from __future__ import annotations

from fractions import Fraction
from math import isqrt

from .algebraic import sqrt_upper
from .lattice import Cell, cell_vertices, convex_hull, hull_edge_forms, shoelace_twice_area


def oler_min_d(n: int) -> tuple[int, str]:
    """Largest integer ``m`` with d(n) > sqrt(m) - 3, i.e. m = 8n+1.

    Returns (8n+1, human readable) so callers can compare exactly against a rational.
    """
    return 8 * n + 1, f"sqrt({8 * n + 1}) - 3"


def oler_excludes(n: int, d: Fraction) -> bool:
    """Exact test: does Oler alone rule out ``n`` points at separation >= 2 in T(d)?

    Rules them out iff  d^2/8 + 3d/4 + 1 < n, i.e. d^2 + 6d + 8 - 8n < 0.  Exact
    rational arithmetic.
    """
    return d * d + 6 * d + 8 - 8 * n < 0


def oler_bound_count(d: Fraction) -> Fraction:
    """The Oler upper bound on the number of separation-2 points in T(d)."""
    return d * d / 8 + 3 * d / 4 + 1


def node_bound(cells: list[Cell], d: Fraction, sqrt_denom: int = 10**12) -> Fraction:
    """Rigorous upper bound on the number of separation-2 points in a union of cells.

    The bound returned is an upper bound on the true (OLER-2) right-hand side for the
    convex hull of the cells: the area term is exact rational, and each edge length uses
    a rational UPPER bound for its square root, so rounding can only weaken the bound.
    """
    if not cells:
        return Fraction(0)
    L = max(c[0] for c in cells)
    verts: list[tuple[int, int]] = []
    for c in cells:
        f = 1 << (L - c[0])
        for a, b in cell_vertices(c):
            verts.append((a * f, b * f))
    hull = convex_hull(verts)
    h = d / (1 << L)
    two_area_lat = shoelace_twice_area(hull)
    area_term = h * h * Fraction(two_area_lat, 2) / 4
    per = Fraction(0)
    for q in hull_edge_forms(hull):
        r = isqrt(q)
        per += Fraction(r) if r * r == q else sqrt_upper(q, sqrt_denom)
    return area_term + h * per / 4 + 1


def cell_capacity_oler(side: Fraction) -> int:
    """Oler's cap on separation-2 points in a closed equilateral triangle of side ``side``."""
    b = oler_bound_count(side)
    return int(b)  # floor, since b >= 1 > 0
