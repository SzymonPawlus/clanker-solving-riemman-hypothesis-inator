import importlib.util
from pathlib import Path
import sys
import unittest


MODULE_PATH = Path(__file__).with_name("woodall.py")
SPEC = importlib.util.spec_from_file_location("woodall", MODULE_PATH)
woodall = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = woodall
SPEC.loader.exec_module(woodall)


class WoodallPrimitiveTests(unittest.TestCase):
    def assert_dijoin_tests_agree(self, graph):
        for mask in range(1 << len(graph.arcs)):
            selected = {i for i in range(len(graph.arcs)) if mask & (1 << i)}
            self.assertEqual(
                woodall.is_dijoin(graph, selected),
                woodall.is_dijoin_by_reverse_augmentation(graph, selected),
                (graph, selected),
            )

    def test_directed_cycle_has_no_dicuts(self):
        cycle = woodall.Digraph(range(3), [(0, 1), (1, 2), (2, 0)])
        self.assertEqual(woodall.dicuts(cycle), ())
        self.assertIsNone(woodall.tau(cycle))
        self.assertTrue(woodall.is_dijoin(cycle, set()))
        self.assert_dijoin_tests_agree(cycle)

    def test_directed_path_by_hand(self):
        path = woodall.Digraph(range(3), [(0, 1), (1, 2)])
        self.assertEqual(set(woodall.dicuts(path)), {frozenset({0}), frozenset({1})})
        self.assertEqual(woodall.tau(path), 1)
        self.assertFalse(woodall.is_dijoin(path, {0}))
        self.assertTrue(woodall.is_dijoin(path, {0, 1}))
        self.assert_dijoin_tests_agree(path)

    def test_tau_two_diamond_finds_two_disjoint_dijoins(self):
        diamond = woodall.Digraph(("s", "a", "b", "t"), [("s", "a"), ("s", "b"), ("a", "t"), ("b", "t")])
        self.assertEqual(woodall.tau(diamond), 2)
        packing = woodall.find_disjoint_dijoins(diamond, 2)
        self.assertIsNotNone(packing)
        self.assertTrue(all(woodall.is_dijoin(diamond, part) for part in packing))
        self.assertFalse(packing[0] & packing[1])
        self.assert_dijoin_tests_agree(diamond)

    def test_source_sink_connected_dags(self):
        fixtures = [
            woodall.Digraph(("s", "a", "b", "t"), [("s", "a"), ("s", "b"), ("a", "t"), ("b", "t")]),
            woodall.Digraph(
                ("s", "a", "b", "x", "y", "t"),
                [("s", "a"), ("s", "b"), ("a", "x"), ("a", "y"),
                 ("b", "x"), ("b", "y"), ("x", "t"), ("y", "t")],
            ),
        ]
        for graph in fixtures:
            minimum = woodall.tau(graph)
            self.assertIsNotNone(minimum)
            packing = woodall.find_disjoint_dijoins(graph, minimum)
            self.assertIsNotNone(packing)
            self.assertEqual(len(set().union(*packing)), sum(map(len, packing)))
            self.assert_dijoin_tests_agree(graph)

    def test_condensation_contracts_sccs_and_preserves_parallel_arcs(self):
        graph = woodall.Digraph(
            range(5),
            [(0, 1), (1, 0), (1, 2), (0, 2), (2, 3), (3, 2), (3, 4)],
        )
        reduced = woodall.condensation(graph)
        self.assertEqual(len(reduced.vertices), 3)
        self.assertEqual(len(reduced.arcs), 3)
        self.assertEqual(woodall.tau(reduced), 1)
        self.assertTrue(all(tail != head for tail, head in reduced.arcs))
        counts = {}
        for arc in reduced.arcs:
            counts[arc] = counts.get(arc, 0) + 1
        self.assertIn(2, counts.values())

    def test_empty_dicut_for_disconnected_graph_is_not_dropped(self):
        graph = woodall.Digraph((0, 1), [])
        self.assertEqual(woodall.dicuts(graph), (frozenset(),))
        self.assertEqual(woodall.tau(graph), 0)
        self.assertFalse(woodall.is_dijoin(graph, set()))
        self.assert_dijoin_tests_agree(graph)

    def test_exhaustive_three_vertex_cross_checks(self):
        possible_arcs = [(u, v) for u in range(3) for v in range(3) if u != v]
        for graph_mask in range(1 << len(possible_arcs)):
            arcs = [arc for i, arc in enumerate(possible_arcs) if graph_mask & (1 << i)]
            graph = woodall.Digraph(range(3), arcs)
            self.assert_dijoin_tests_agree(graph)
            reduced = woodall.condensation(graph)
            self.assertEqual(woodall.tau(graph), woodall.tau(reduced))
            self.assertTrue(all(len(component) == 1 for component in woodall.strongly_connected_components(reduced)))


if __name__ == "__main__":
    unittest.main()
