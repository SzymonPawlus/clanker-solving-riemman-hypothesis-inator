"""The dyadic subdivision must cover its parent, and the distance form must be exact."""

from __future__ import annotations

import math
import random

from cpbnb.lattice import DOWN, ROOT, UP, max_sq_form, subdivide, vertices

SQRT3_2 = math.sqrt(3) / 2


def to_xy(coord, scale=1.0):
    a, b = coord
    return (scale * (a + b / 2.0), scale * (b * SQRT3_2))


def in_triangle(p, tri, eps=1e-12):
    """Barycentric containment test in Cartesian coordinates."""
    (x1, y1), (x2, y2), (x3, y3) = tri
    det = (y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3)
    l1 = ((y2 - y3) * (p[0] - x3) + (x3 - x2) * (p[1] - y3)) / det
    l2 = ((y3 - y1) * (p[0] - x3) + (x1 - x3) * (p[1] - y3)) / det
    l3 = 1.0 - l1 - l2
    return l1 >= -eps and l2 >= -eps and l3 >= -eps


def test_children_cover_the_parent():
    rng = random.Random(7)
    for cell in [ROOT, (1, UP, 1, 0), (1, DOWN, 0, 0), (3, DOWN, 2, 1)]:
        level = cell[0]
        parent = [to_xy(v, 1.0 / (1 << level)) for v in vertices(cell)]
        kids = subdivide(cell)
        kid_tris = [[to_xy(v, 1.0 / (1 << (level + 1))) for v in vertices(k)] for k in kids]
        for _ in range(4000):
            r1, r2 = rng.random(), rng.random()
            if r1 + r2 > 1:
                r1, r2 = 1 - r1, 1 - r2
            r3 = 1 - r1 - r2
            p = tuple(
                r1 * parent[0][k] + r2 * parent[1][k] + r3 * parent[2][k] for k in range(2)
            )
            assert any(in_triangle(p, t) for t in kid_tris)


def test_children_have_half_the_side_and_the_right_count():
    for cell in [ROOT, (2, DOWN, 1, 1)]:
        kids = subdivide(cell)
        assert len(set(kids)) == 4
        assert all(k[0] == cell[0] + 1 for k in kids)


def test_max_sq_form_agrees_with_a_float_scan():
    rng = random.Random(11)
    cells = [ROOT, (1, UP, 0, 0), (1, DOWN, 0, 0), (2, UP, 3, 0), (3, DOWN, 1, 4)]
    for a in cells:
        for b in cells:
            q, level = max_sq_form(a, b)
            h = 1.0 / (1 << level)
            best = 0.0
            for _ in range(2000):
                pa = _sample(a, rng)
                pb = _sample(b, rng)
                best = max(best, (pa[0] - pb[0]) ** 2 + (pa[1] - pb[1]) ** 2)
            claimed = q * h * h
            assert best <= claimed + 1e-12
            assert best > claimed * 0.5  # the scan should get reasonably close


def _sample(cell, rng):
    level = cell[0]
    tri = [to_xy(v, 1.0 / (1 << level)) for v in vertices(cell)]
    r1, r2 = rng.random(), rng.random()
    if r1 + r2 > 1:
        r1, r2 = 1 - r1, 1 - r2
    r3 = 1 - r1 - r2
    return tuple(r1 * tri[0][k] + r2 * tri[1][k] + r3 * tri[2][k] for k in range(2))


def test_root_diameter_is_the_side():
    q, level = max_sq_form(ROOT, ROOT)
    assert (q, level) == (1, 0)
