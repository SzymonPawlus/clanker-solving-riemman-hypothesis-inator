from __future__ import annotations

import sys
import unittest
import json
from decimal import Decimal, localcontext
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from lift import (  # noqa: E402
    Candidate,
    extract_contacts,
    load_candidate,
    matrix_rank,
    obvious_rattlers,
    rank_diagnostic,
    signatures_stable,
    tolerance_sweep,
    wall_slacks,
)
from solve import solve_candidate  # noqa: E402
from exact_n8 import verify_n8  # noqa: E402

SEARCH_OUT = ROOT.parent / "circle-packing-search" / "out"


class GeometryTests(unittest.TestCase):
    def test_wall_slacks_at_vertices(self):
        self.assertEqual(wall_slacks((0.0, 0.0))[0], 0.0)
        self.assertEqual(wall_slacks((0.0, 0.0))[1], 0.0)
        self.assertEqual(wall_slacks((1.0, 0.0))[0], 0.0)
        self.assertEqual(wall_slacks((1.0, 0.0))[2], 0.0)

    def test_two_constraints_are_not_automatically_a_rattler(self):
        # The corner has two independent wall constraints.  A degree<3 rule would
        # wrongly call it a rattler; the deliberately narrow zero-contact rule does not.
        candidate = Candidate(n=2, m=1.0, points=((0.0, 0.0), (1.0, 0.0)), source="synthetic")
        graph = extract_contacts(candidate, 1e-12)
        self.assertEqual(obvious_rattlers(candidate, graph), ())

    def test_rank_handles_rectangular_matrices(self):
        self.assertEqual(matrix_rank(((1, 0), (0, 1), (1, 1))), 2)
        self.assertEqual(matrix_rank(((1, 2), (2, 4))), 1)


class CheckedInCandidateTests(unittest.TestCase):
    EXPECTED = {
        8: (9, 9, (), 17, 17),
        11: (11, 11, (6,), 21, 21),
        13: (18, 12, (), 27, 27),
    }

    def test_contact_signatures_and_core_rank_are_stable(self):
        for n, expected in self.EXPECTED.items():
            with self.subTest(n=n):
                candidate = load_candidate(SEARCH_OUT / f"n{n:02d}.json")
                graphs = tolerance_sweep(candidate, (1e-6, 1e-8, 1e-10))
                self.assertTrue(signatures_stable(graphs))
                graph = graphs[-1]
                rattlers = obvious_rattlers(candidate, graph)
                core = tuple(i for i in range(n) if i not in rattlers)
                diagnostic = rank_diagnostic(candidate, graph, core)
                observed = (
                    len(graph.pairs),
                    len(graph.walls),
                    rattlers,
                    diagnostic.rank,
                    diagnostic.columns,
                )
                self.assertEqual(observed, expected)
                self.assertTrue(diagnostic.full_column_rank)

    def test_n8_lift_recovers_the_known_algebraic_minimum(self):
        candidate = load_candidate(SEARCH_OUT / "n08.json")
        graph = extract_contacts(candidate, 1e-10)
        solved = solve_candidate(candidate, graph, tuple(range(8)), digits=100)
        with localcontext() as context:
            context.prec = 100
            exact_m = (Decimal(33).sqrt() - 3) / 8
            self.assertLess(abs(solved.m - exact_m), Decimal("1e-90"))
        self.assertLess(solved.selected_residual, Decimal("1e-80"))
        self.assertLess(solved.all_active_residual, Decimal("1e-80"))

    def test_n8_exact_formula_self_check(self):
        counts = verify_n8()
        self.assertEqual(counts["points"], 8)
        self.assertEqual(counts["pair_constraints"], 28)
        self.assertEqual(counts["pair_equalities"], 9)
        self.assertEqual(counts["wall_equalities"], 9)

    def test_n8_candidate_remains_explicitly_unverified(self):
        candidate = json.loads((ROOT / "candidates" / "n008-lifted.json").read_text())
        self.assertEqual(candidate["claim"], "construction")
        self.assertEqual(candidate["coordinate_type"], "algebraic")
        self.assertEqual(candidate["status"], "numerical")


if __name__ == "__main__":
    unittest.main()
