from pathlib import Path
import sys
import unittest


sys.path.insert(0, str(Path(__file__).parent))
import saturation  # noqa: E402


class DefinitionTests(unittest.TestCase):
    def test_path_tau_one(self):
        arcs = ((0, 1), (1, 2))
        self.assertEqual(1, saturation.tau(3, arcs))
        self.assertEqual(saturation.tau(3, arcs), saturation.tau_bitset_oracle(3, arcs))

    def test_cycle_has_no_dicut(self):
        arcs = ((0, 1), (1, 2), (2, 0))
        self.assertEqual(0, saturation.tau(3, arcs))

    def test_two_sources(self):
        arcs = ((0, 2), (1, 2))
        witness = saturation.minimum_dicut(3, arcs)
        self.assertIsNotNone(witness)
        self.assertEqual(1, witness.size)

    def test_fixed_order_count(self):
        self.assertEqual(32768, sum(1 for _ in saturation.fixed_order_dags(6)))


class SaturationTests(unittest.TestCase):
    def test_cut_restriction_core_exhaustively_through_four_vertices(self):
        for n in range(1, 5):
            for arcs in saturation.fixed_order_dags(n):
                old_tau = saturation.tau(n, arcs)
                if old_tau < 2:
                    continue
                for new_arc in saturation.missing_forward_arcs(n, arcs):
                    enlarged = (*arcs, new_arc)
                    if saturation.tau(n, enlarged) != old_tau:
                        continue
                    for mask in range(1, (1 << n) - 1):
                        entering_new = any(
                            not mask & (1 << u) and mask & (1 << v)
                            for u, v in enlarged
                        )
                        outgoing_new = {
                            arc
                            for arc in enlarged
                            for u, v in (arc,)
                            if mask & (1 << u) and not mask & (1 << v)
                        }
                        if entering_new or not outgoing_new:
                            continue
                        entering_old = any(
                            not mask & (1 << u) and mask & (1 << v)
                            for u, v in arcs
                        )
                        outgoing_old = {
                            arc
                            for arc in arcs
                            for u, v in (arc,)
                            if mask & (1 << u) and not mask & (1 << v)
                        }
                        self.assertFalse(entering_old)
                        self.assertTrue(outgoing_old)
                        self.assertLessEqual(outgoing_old, outgoing_new)

    def test_complete_dag_is_saturated(self):
        arcs = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
        self.assertEqual(3, saturation.tau(4, arcs))
        self.assertTrue(saturation.is_tau_saturated(4, arcs))

    def test_greedy_tau_preserving_extension(self):
        arcs = ((0, 2), (0, 3), (1, 2), (1, 3))
        self.assertEqual(2, saturation.tau(4, arcs))
        enlarged = saturation.greedy_tau_preserving_extension(4, arcs)
        self.assertEqual(2, saturation.tau(4, enlarged))
        self.assertTrue(saturation.has_no_tau_preserving_forward_arc(4, enlarged))
        self.assertTrue(saturation.is_tau_saturated(4, enlarged))

    def test_no_preserving_arc_is_weaker_than_strict_saturation(self):
        # A transitive triangle plus isolated vertex 3 has tau=2 under the
        # nonempty-dicut convention. Every missing forward arc enters the
        # isolated vertex and lowers tau to 1: none preserves tau, but the
        # graph is not strictly saturated.
        arcs = ((0, 1), (0, 2), (1, 2))
        self.assertEqual(2, saturation.tau(4, arcs))
        certificate = saturation.saturation_certificate(4, arcs)
        self.assertEqual({1}, {after for _, after in certificate})
        self.assertTrue(saturation.has_no_tau_preserving_forward_arc(4, arcs))
        self.assertFalse(saturation.is_tau_saturated(4, arcs))
        self.assertEqual(
            arcs, saturation.greedy_tau_preserving_extension(4, arcs)
        )

    def test_lifting_fixture(self):
        # In K_2,2 oriented from sources to sinks, the two perfect matchings
        # are disjoint dijoins. Adding 0->1 preserves tau=2 and both remain.
        arcs = ((0, 2), (0, 3), (1, 2), (1, 3))
        packing = (((0, 2), (1, 3)), ((0, 3), (1, 2)))
        self.assertTrue(
            saturation.disjoint_dijoin_packing_is_preserved(
                4, arcs, (0, 1), packing
            )
        )

    def test_source_sink_connected(self):
        self.assertTrue(saturation.source_sink_connected(3, ((0, 1), (1, 2))))
        self.assertFalse(
            saturation.source_sink_connected(
                4, ((0, 2), (1, 2), (1, 3))
            )
        )


if __name__ == "__main__":
    unittest.main()
