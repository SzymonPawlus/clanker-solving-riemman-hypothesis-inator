from pathlib import Path
import sys
import unittest


sys.path.insert(0, str(Path(__file__).parent))
import balanced_dicuts  # noqa: E402


class HypergraphTests(unittest.TestCase):
    def test_triangle_incidence_is_unbalanced(self):
        vertices = ("a", "b", "c")
        edges = ({"a", "b"}, {"b", "c"}, {"c", "a"})
        witness = balanced_dicuts.find_odd_berge_cycle(vertices, edges)
        self.assertIsNotNone(witness)
        self.assertEqual(3, witness.order)
        self.assertTrue(balanced_dicuts.validate_odd_berge_cycle(vertices, edges, witness))
        self.assertTrue(balanced_dicuts.brute_force_unbalanced_submatrix(vertices, edges))

    def test_four_cycle_incidence_is_balanced(self):
        vertices = ("a", "b", "c", "d")
        edges = ({"a", "b"}, {"b", "c"}, {"c", "d"}, {"d", "a"})
        self.assertIsNone(balanced_dicuts.find_odd_berge_cycle(vertices, edges))
        self.assertFalse(balanced_dicuts.brute_force_unbalanced_submatrix(vertices, edges))

    def test_shortest_witness_wins(self):
        vertices = tuple(range(8))
        edges = (
            {0, 1}, {1, 2}, {2, 3}, {3, 4}, {4, 0},
            {5, 6}, {6, 7}, {7, 5},
        )
        witness = balanced_dicuts.find_odd_berge_cycle(vertices, edges)
        self.assertIsNotNone(witness)
        self.assertEqual(3, witness.order)
        self.assertTrue(balanced_dicuts.validate_odd_berge_cycle(vertices, edges, witness))


class DicutTests(unittest.TestCase):
    def test_fixed_order_dag_count(self):
        self.assertEqual(1024, sum(1 for _ in balanced_dicuts.fixed_order_dags(5)))

    def test_directed_path(self):
        arcs = ((0, 1), (1, 2))
        self.assertEqual(
            (frozenset({0}), frozenset({1})),
            balanced_dicuts.dicuts(3, arcs),
        )
        self.assertIsNone(
            balanced_dicuts.find_odd_berge_cycle(range(len(arcs)), balanced_dicuts.dibonds(3, arcs))
        )

    def test_directed_cycle_has_no_dicut(self):
        arcs = ((0, 1), (1, 2), (2, 0))
        self.assertEqual((), balanced_dicuts.dicuts(3, arcs))

    def test_two_sources(self):
        arcs = ((0, 2), (1, 2))
        self.assertEqual(
            (frozenset({0}), frozenset({1})),
            balanced_dicuts.dibonds(3, arcs),
        )

    def test_reachability_forest(self):
        self.assertTrue(
            balanced_dicuts.source_sink_reachability_is_forest(
                4, ((0, 2), (1, 2), (1, 3))
            )
        )
        self.assertFalse(
            balanced_dicuts.source_sink_reachability_is_forest(
                4, ((0, 2), (0, 3), (1, 2), (1, 3))
            )
        )


if __name__ == "__main__":
    unittest.main()
