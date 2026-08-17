import unittest

from acz import (
    BipartiteDigraph,
    acz_route_witness,
    d27,
    m1_bases,
    minimum_dicut,
    restriction_is_strongly_base_orderable,
)
from independent_verify import bases_by_sink_subsets, route_witness_sets
from search import masks_to_sets


class ACZRho4Tests(unittest.TestCase):
    def test_minimum_dicut_matches_direct_vertex_subset_enumeration(self):
        fixtures = (
            BipartiteDigraph(2, 2, ((0, 0), (0, 1), (1, 0), (1, 1))),
            BipartiteDigraph(2, 2, ((0, 0), (0, 0), (1, 1), (1, 1))),
        )
        for graph in fixtures:
            arcs = tuple(
                (source, graph.source_count + sink) for source, sink in graph.arcs
            )
            vertex_count = graph.source_count + graph.sink_count
            direct = None
            for mask in range(1, (1 << vertex_count) - 1):
                outgoing = 0
                incoming = 0
                for tail, head in arcs:
                    if mask & (1 << tail) and not mask & (1 << head):
                        outgoing += 1
                    if not mask & (1 << tail) and mask & (1 << head):
                        incoming += 1
                if incoming == 0:
                    direct = outgoing if direct is None else min(direct, outgoing)
            self.assertEqual(minimum_dicut(graph), direct)

    def test_d27_degree_rho_and_tau(self):
        graph = d27()
        self.assertEqual(graph.source_degrees, (4,) * 9 + (3,) * 3)
        self.assertEqual(graph.sink_degrees, (3,) * 15)
        self.assertEqual(graph.rho, 3)
        self.assertEqual(minimum_dicut(graph), 3)

    def test_d27_reproduces_primary_source_m1_claims(self):
        graph = d27()
        bases = m1_bases(graph)
        base_set = frozenset(bases)
        q1 = sum(1 << i for i in (0, 1, 2))
        q2 = sum(1 << i for i in (3, 4, 5))
        q3 = sum(1 << i for i in (6, 7, 8))
        self.assertTrue({q1, q2, q3} <= base_set)
        self.assertEqual(sum(base & ~(q1 | q2) == 0 for base in bases), 16)
        exchanges = set()
        for left in range(3):
            for right in range(3, 6):
                if (q1 ^ (1 << left) ^ (1 << right)) in base_set and (
                    q2 ^ (1 << left) ^ (1 << right)
                ) in base_set:
                    exchanges.add((right + 1, left + 1))
        self.assertEqual(exchanges, {(4, 1), (4, 2), (4, 3), (5, 3), (6, 3)})
        self.assertFalse(restriction_is_strongly_base_orderable(bases, q1 | q2))
        self.assertIsNotNone(acz_route_witness(bases, ground_size=9))

    def test_independent_d27_basis_and_route_implementations_agree(self):
        graph = d27()
        primary = m1_bases(graph)
        independent = bases_by_sink_subsets(graph)
        self.assertEqual(masks_to_sets(primary), independent)
        self.assertEqual(
            acz_route_witness(primary, ground_size=9) is not None,
            route_witness_sets(independent, frozenset(range(9))) is not None,
        )


if __name__ == "__main__":
    unittest.main()
