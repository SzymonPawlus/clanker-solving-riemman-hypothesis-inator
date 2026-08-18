"""Soundness of the exhaustion.

Two families of test, and the second is the important one:

* **positive** -- for a side strictly below the cited d(n), the search closes.
* **negative** -- for a side at or above the cited d(n) a packing exists, so the search
  must *not* report ``proved``.  A bug that over-prunes (a wrong distance form, a wrong
  child set, a capacity off-by-one, a symmetry restriction that is not actually a
  symmetry) produces a false ``proved`` here, which is the failure mode that would
  invalidate every bound this experiment emits.

The strongest negative test is :func:`test_known_packings_survive_every_level`, which
takes explicit optimal packings and checks directly that neither prune rule ever fires on
the cells that contain them, at every level.
"""

from __future__ import annotations

import json
import math
import tempfile
from fractions import Fraction

from cpbnb.caps import capacity
from cpbnb.lattice import DOWN, UP
from cpbnb.search import Prover, compositions, load_frontier

SQRT3 = math.sqrt(3)


def run(n, d, level, max_cited=2, symmetry=True, time_limit=120.0):
    return Prover(n, Fraction(d), level, max_cited, symmetry=symmetry).run(
        time_limit=time_limit
    )


# -- positive: strictly below the cited optimum, the exhaustion closes -----------------


def test_proves_n3_below_two():
    assert run(3, "19/10", 4)["status"] == "proved"


def test_proves_n4_below_2sqrt3():
    assert run(4, "17/5", 7)["status"] == "proved"


def test_proves_n6_below_four():
    assert run(6, "39/10", 6)["status"] == "proved"


def test_proves_n7_below_d7():
    assert run(7, "53/10", 7)["status"] == "proved"


# -- negative: at or above the cited optimum a packing exists ---------------------------


def test_does_not_prove_at_the_optimum():
    # These sides admit a packing, so "proved" would be a soundness bug.  A node budget
    # keeps the test quick; "timeout" is a pass here, since the assertion is only that the
    # search never *claims* infeasibility.  The unbounded version of this check is
    # test_known_packings_survive_every_level below.
    for n, d, level, budget in [
        (3, "2", 7, None),
        (4, "3.4642", 7, None),
        (6, "4", 7, None),
        (7, "5.4642", 7, None),
        (10, "6", 6, None),
        (12, "7.4642", 6, 400_000),
        (15, "8", 5, 400_000),
    ]:
        res = Prover(n, Fraction(d), level, 2).run(node_limit=budget, time_limit=60.0)
        assert res["status"] != "proved", (n, d, res["status"])


def test_does_not_prove_above_the_optimum():
    for n, d, level, budget in [(4, "4", 6, None), (12, "9", 5, 400_000),
                                (16, "12", 4, None)]:
        res = Prover(n, Fraction(d), level, 15).run(node_limit=budget, time_limit=60.0)
        assert res["status"] != "proved", (n, d, res["status"])


# -- the direct soundness check on explicit optimal packings ---------------------------


def triangular_lattice(rows):
    """``rows`` rows of the unit triangular lattice scaled to spacing 2."""
    pts = []
    for j in range(rows):
        for i in range(rows - j):
            pts.append((2 * (i + j / 2.0), 2 * (j * SQRT3 / 2.0)))
    return pts


def cell_of(point, d, level):
    """The subdivision cell containing ``point``; ties resolved towards the 'up' cell."""
    h = float(d) / (1 << level)
    b = point[1] / (h * SQRT3 / 2.0)
    a = point[0] / h - b / 2.0
    i, j = math.floor(a + 1e-12), math.floor(b + 1e-12)
    fa, fb = a - i, b - j
    orient = UP if fa + fb <= 1.0 + 1e-9 else DOWN
    return (level, orient, int(i), int(j))


def test_known_packings_survive_every_level():
    """Neither prune rule may fire on a genuinely feasible configuration."""
    cases = [(3, 2, Fraction(2)), (6, 3, Fraction(4)), (10, 4, Fraction(6)),
             (15, 5, Fraction(8))]
    for n, rows, d in cases:
        pts = triangular_lattice(rows)
        assert len(pts) == n
        # sanity: the configuration really is feasible
        for a in range(n):
            for b in range(a + 1, n):
                dist = math.dist(pts[a], pts[b])
                assert dist >= 2 - 1e-9, (n, a, b, dist)
        prover = Prover(n, d, 8, 15)
        for level in range(0, 8):
            cells = {}
            for p in pts:
                c = cell_of(p, d, level)
                cells[c] = cells.get(c, 0) + 1
            for cell, mult in cells.items():
                assert prover.cap_ok(cell, mult), (n, level, cell, mult)
                if mult >= 2:
                    assert prover.compatible(cell, cell), (n, level, cell, mult)
            keys = list(cells)
            for x in range(len(keys)):
                for y in range(x + 1, len(keys)):
                    assert prover.compatible(keys[x], keys[y]), (n, level, keys[x], keys[y])


# -- structural -------------------------------------------------------------------------


def test_symmetry_reduction_does_not_change_the_verdict():
    for n, d, level in [(4, "17/5", 7), (6, "39/10", 6), (3, "2", 6), (7, "53/10", 7)]:
        with_sym = run(n, d, level, symmetry=True)
        without = run(n, d, level, symmetry=False)
        assert with_sym["status"] == without["status"], (n, d)


def test_symmetry_reduction_shrinks_the_tree():
    a = run(7, "53/10", 7, symmetry=True)
    b = run(7, "53/10", 7, symmetry=False)
    assert a["nodes"] < b["nodes"]


def test_compositions_are_complete():
    for k in range(0, 8):
        comps = compositions(k, 4)
        assert len(comps) == math.comb(k + 3, 3)
        assert len(set(comps)) == len(comps)
        assert all(sum(c) == k and all(x >= 0 for x in c) for c in comps)


def test_root_capacity_is_applied():
    # 12 points in a triangle of side 7 -- cited d(11) = 7.2659... > 7, so the root node
    # is discarded before any branching happens.
    res = run(12, "7", 5, max_cited=15)
    assert res["status"] == "proved"
    assert res["nodes"] == 0


def test_more_literature_never_flips_a_verdict_to_unproved():
    for n, d, level in [(6, "39/10", 6), (4, "17/5", 7)]:
        assert run(n, d, level, max_cited=2)["status"] == "proved"
        assert run(n, d, level, max_cited=15)["status"] == "proved"


def test_checkpoint_and_resume_reproduce_the_same_verdict():
    with tempfile.TemporaryDirectory() as tmp:
        path = f"{tmp}/ck.json"
        p = Prover(7, Fraction("53/10"), 7, 2)
        partial = p.run(node_limit=20_000, checkpoint_path=path, checkpoint_every=20_000)
        assert partial["status"] == "timeout"
        frontier = load_frontier(path)
        assert frontier
        p2 = Prover(7, Fraction("53/10"), 7, 2)
        rest = p2.run(initial_stack=frontier)
        assert rest["status"] == "proved"
        with open(path) as fh:
            assert json.load(fh)["n"] == 7


def test_capacity_helper_matches_the_prover_table():
    p = Prover(12, Fraction("13/2"), 4, 15)
    for level in range(5):
        assert p.cap[level] == capacity(Fraction("13/2") / (1 << level), 15)
