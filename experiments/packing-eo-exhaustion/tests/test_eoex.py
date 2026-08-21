"""Validation.  The negative controls matter more than the positive ones: a bug that
over-prunes produces a *false* `proved` at a side length where a packing exists, and that
is the failure that would invalidate every bound in this directory."""

from __future__ import annotations

import random
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from eoex.lattice import (  # noqa: E402
    DOWN,
    UP,
    cell_vertices,
    cells_at_level,
    children,
    convex_hull,
    max_sep_form,
    pair_compatible,
    shoelace_twice_area,
)
from eoex.oler import node_bound, oler_bound_count, oler_excludes  # noqa: E402
from eoex.caps import capacity  # noqa: E402
from eoex.search import Prover  # noqa: E402


# ------------------------------------------------------------------ geometry


def _in_cell(cell, a: Fraction, b: Fraction) -> bool:
    _, orient, i, j = cell
    if orient == UP:
        return a >= i and b >= j and a + b <= i + j + 1
    return a <= i + 1 and b <= j + 1 and a + b >= i + j + 1


def test_children_cover_and_are_contained():
    rng = random.Random(20260821)
    for cell in [(0, UP, 0, 0), (2, UP, 1, 0), (3, DOWN, 2, 1), (1, DOWN, 0, 0)]:
        kids = children(cell)
        assert len({k for k in kids}) == 4
        for _ in range(4000):
            # uniform-ish sample of the parent in barycentric lattice coordinates
            x, y = rng.random(), rng.random()
            if x + y > 1:
                x, y = 1 - x, 1 - y
            v = cell_vertices(cell)
            a = Fraction(v[0][0]) + Fraction(x).limit_denominator(10**6) * (v[1][0] - v[0][0]) \
                + Fraction(y).limit_denominator(10**6) * (v[2][0] - v[0][0])
            b = Fraction(v[0][1]) + Fraction(x).limit_denominator(10**6) * (v[1][1] - v[0][1]) \
                + Fraction(y).limit_denominator(10**6) * (v[2][1] - v[0][1])
            f = 2  # children live one level down
            assert any(_in_cell(k, a * f, b * f) for k in kids), (cell, a, b)
        # containment: every child vertex lies in the parent
        for k in kids:
            for (a, b) in cell_vertices(k):
                assert _in_cell(cell, Fraction(a, 2), Fraction(b, 2))


def test_cell_counts():
    for L in range(5):
        assert len(cells_at_level(L)) == 4**L


def test_max_sep_of_a_cell_pair():
    # up(0,0) and up(1,0) at level 1 hold the container corners A=(0,0) and B=(d,0);
    # the farthest vertex pair is (0,0) to (2,0), displacement (2,0), norm2 = 4, so the
    # maximum separation is h*2 = d exactly.
    q, L = max_sep_form((1, UP, 0, 0), (1, UP, 1, 0))
    assert (q, L) == (4, 1)
    assert not pair_compatible((1, UP, 0, 0), (1, UP, 1, 0), Fraction(199, 100))
    assert pair_compatible((1, UP, 0, 0), (1, UP, 1, 0), Fraction(2))
    # the two level-1 cells up(0,0) and down(0,0) are farthest at (0,0)-(1,1):
    # displacement (1,1), norm2 = 3, so max separation = (d/2)*sqrt(3) >= 2 iff
    # d >= 4/sqrt(3) = 2.309401...
    q, L = max_sep_form((1, UP, 0, 0), (1, DOWN, 0, 0))
    assert (q, L) == (3, 1)
    assert not pair_compatible((1, UP, 0, 0), (1, DOWN, 0, 0), Fraction(2309, 1000))
    assert pair_compatible((1, UP, 0, 0), (1, DOWN, 0, 0), Fraction(2310, 1000))


def test_hull_and_area():
    hull = convex_hull([(0, 0), (4, 0), (0, 4), (1, 1), (2, 1)])
    assert set(hull) == {(0, 0), (4, 0), (0, 4)}
    assert shoelace_twice_area(hull) == 16


# ---------------------------------------------------------------------- Oler


def test_oler_matches_the_closed_form_at_the_root():
    for d in [Fraction(4), Fraction(6), Fraction(157, 20)]:
        assert node_bound([(0, UP, 0, 0)], d) == oler_bound_count(d)


def test_oler_is_exactly_tight_on_triangular_numbers():
    for k in range(2, 9):
        n = k * (k + 1) // 2
        d = Fraction(2 * (k - 1))
        assert oler_bound_count(d) == n
        assert not oler_excludes(n, d)
        assert oler_excludes(n, d - Fraction(1, 1000))


def test_oler_closed_form_reproduces_the_known_lower_bounds():
    # d(16) > sqrt(129) - 3 = 8.35781...; the reference value in the repo's
    # attacks/oler-lower-bound write-up is s(16) >= 11.821918 = that + 2*sqrt(3).
    assert oler_excludes(16, Fraction(8357, 1000))
    assert not oler_excludes(16, Fraction(8358, 1000))


# ------------------------------------------------------------------ capacity


def test_capacity_is_never_below_the_truth():
    known_d = {1: 0, 2: 2, 3: 2, 5: 4, 6: 4, 9: 6, 10: 6, 14: 8, 15: 8}
    for k, dk in known_d.items():
        if dk == 0:
            continue
        # a triangle of side exactly d(k) holds k points, so cap must be >= k
        assert capacity(Fraction(dk), 40) >= k, (k, dk)


# ------------------------------------------------- negative controls: real packings


def _lattice_packing(k: int) -> list[tuple[Fraction, Fraction]]:
    """The k-row triangular lattice: Delta(k) points at separation exactly 2 in T(2(k-1))."""
    pts = []
    for j in range(k):
        for i in range(k - j):
            pts.append((Fraction(2 * i + j), Fraction(2 * j)))  # (alpha, beta) at level 0 * ?
    return pts


def _assign_cells(k: int, L: int) -> list:
    """Cell of the level-L subdivision containing each lattice point, exactly.

    Point (i,j) of the packing sits at i*(2,0) + j*(1,sqrt3); the level-L basis is
    u=(h,0), v=(h/2,h*sqrt3/2) with h = d/2**L and d = 2(k-1).  Solving gives lattice
    coordinates (2i/h, 2j/h) = (i*2**L/(k-1), j*2**L/(k-1)).
    """
    d = Fraction(2 * (k - 1))
    h = d / (1 << L)
    out = []
    for j in range(k):
        for i in range(k - j):
            a = Fraction(2 * i) / h
            b = Fraction(2 * j) / h
            i0, j0 = int(a // 1), int(b // 1)
            if (a - i0) + (b - j0) <= 1:
                cell = (L, UP, i0, j0)
            else:
                cell = (L, DOWN, i0, j0)
            assert _in_cell(cell, a, b), (k, L, i, j, a, b)
            out.append(cell)
    return out


def test_known_packings_survive_every_rule_at_every_level():
    """No prune may fire on the cells of an actual optimal packing."""
    for k in range(2, 7):
        n = k * (k + 1) // 2
        d = Fraction(2 * (k - 1))
        for L in range(0, 7):
            cells = _assign_cells(k, L)
            mult: dict = {}
            for c in cells:
                mult[c] = mult.get(c, 0) + 1
            for c, m in mult.items():
                assert m <= capacity(d / (1 << L), n), (k, L, c, m)
            keys = list(mult)
            for x in range(len(keys)):
                for y in range(x + 1, len(keys)):
                    assert pair_compatible(keys[x], keys[y], d), (k, L, keys[x], keys[y])
            assert node_bound(keys, d) >= n, (k, L, float(node_bound(keys, d)), n)


def test_search_never_proves_a_feasible_case():
    """d(Delta(k)) = 2(k-1) exactly, so the search must not close at d = 2(k-1)."""
    for k in (2, 3, 4):
        n = k * (k + 1) // 2
        d = Fraction(2 * (k - 1))
        for hull in (True, False):
            p = Prover(n, d, max_level=5, use_oler_hull=hull and (d < 2 * (n - 1)))
            res = p.run(node_limit=400_000)
            assert res.status != "proved", (k, hull, res.status)


def test_search_proves_just_below_the_optimum():
    for k, ml in ((2, 4), (3, 5), (4, 6)):
        n = k * (k + 1) // 2
        d = Fraction(2 * (k - 1)) - Fraction(1, 100)
        p = Prover(n, d, max_level=ml)
        res = p.run(node_limit=2_000_000)
        assert res.status == "proved", (k, res.status, res.nodes)


def test_symmetry_does_not_change_verdicts():
    cases = [(5, Fraction(7, 2), 5), (6, Fraction(39, 10), 5), (9, Fraction(5), 5)]
    for n, d, ml in cases:
        a = Prover(n, d, ml, symmetry=True).run(node_limit=1_000_000)
        b = Prover(n, d, ml, symmetry=False).run(node_limit=1_000_000)
        assert a.status == b.status, (n, d, a.status, b.status)


def test_frontier_nodes_are_revalidated():
    p = Prover(5, Fraction(7, 2), 4)
    try:
        p.run(initial_stack=[(((0, UP, 0, 0), 4),)])
    except ValueError:
        pass
    else:  # pragma: no cover
        raise AssertionError("a node with the wrong point count was accepted")


if __name__ == "__main__":
    import traceback

    fails = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"PASS {name}")
            except Exception:
                fails += 1
                print(f"FAIL {name}")
                traceback.print_exc()
    print("all good" if not fails else f"{fails} FAILURES")
    raise SystemExit(1 if fails else 0)
