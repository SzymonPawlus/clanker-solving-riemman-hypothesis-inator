"""Validation gate for the exact polychromatic dijoin packer.

Nothing in the sweep is allowed to run until this passes.  The central test is
an agreement check against experiments/woodalls-dicuts/woodall.py, which is an
INDEPENDENT implementation (subset enumeration over all arc sets) written for a
different issue.  Agreement of two differently-shaped exhaustive procedures is
the strongest cheap evidence available that the primitives are right.
"""

from __future__ import annotations

import itertools
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "experiments", "woodalls-dicuts"))

import dijoin_exact as dx           # noqa: E402
import woodall as ref               # noqa: E402  (independent reference)


class TestDefinitionFixtures(unittest.TestCase):
    """Problem RULES section 4: sanity-check the definitions themselves."""

    def test_directed_cycle_has_no_dicut(self):
        arcs = [(0, 1), (1, 2), (2, 0)]
        self.assertEqual(dx.dicut_masks(3, arcs), [])
        self.assertIsNone(dx.tau_of(dx.dicut_masks(3, arcs)))
        self.assertTrue(dx.analyse(3, arcs)["holds"])

    def test_directed_path_has_tau_one(self):
        arcs = [(0, 1), (1, 2)]
        res = dx.analyse(3, arcs)
        self.assertEqual(res["tau"], 1)
        self.assertTrue(res["holds"])
        # tau = 1 is trivially true: the whole arc set is a dijoin.
        self.assertEqual(len(res["packing"]), 1)

    def test_dicut_needs_empty_in_cut_not_merely_nonempty_out_cut(self):
        # arcs 0: 0->1, 1: 1->2, 2: 0->2.  The shore {1} has a nonempty
        # delta^+ = {1->2} but delta^-({1}) = {0->1} is nonempty, so {1->2} is
        # NOT a dicut.  Accepting it would be the classic fatal misreading.
        arcs = [(0, 1), (1, 2), (0, 2)]
        cuts = dx.dicut_masks(3, arcs)
        self.assertNotIn(1 << 1, cuts)          # {1->2} alone is not a dicut
        self.assertEqual(cuts, [0b101, 0b110])  # only shores {0} and {0,1}

    def test_tau_two_diamond(self):
        arcs = [(0, 1), (0, 2), (1, 3), (2, 3)]
        res = dx.analyse(4, arcs)
        self.assertEqual(res["tau"], 2)
        self.assertTrue(res["holds"])
        self.assertEqual(len(res["packing"]), 2)
        flat = sorted(i for part in res["packing"] for i in part)
        self.assertEqual(flat, [0, 1, 2, 3])    # disjoint

    def test_tau_three_source_sink_connected(self):
        # three internally disjoint 0 -> 4 paths; tau = 3, holds.
        arcs = [(0, 1), (0, 2), (0, 3), (1, 4), (2, 4), (3, 4)]
        res = dx.analyse(5, arcs)
        self.assertEqual(res["tau"], 3)
        self.assertTrue(res["holds"])
        self.assertEqual(len(res["packing"]), 3)

    def test_easy_direction_never_exceeded(self):
        # RULES section 1 filter 3: we test existence of tau dijoins, and can
        # never find more than tau disjoint ones.
        arcs = [(0, 1), (0, 2), (1, 3), (2, 3)]
        cuts = dx.dicut_masks(4, arcs)
        self.assertIsNone(dx.pack_dijoins(4, cuts, 3))   # tau + 1 is infeasible


class TestAgreementWithReference(unittest.TestCase):
    """Cross-check tau and packing existence against woodall.py."""

    def _agree(self, n, arcs):
        graph = ref.Digraph(range(n), arcs)
        ref_cuts = set(
            frozenset(sorted(c)) for c in ref.dicuts(graph)
        )
        mine = dx.dicut_masks(n, arcs)
        mine_sets = set(
            frozenset(i for i in range(len(arcs)) if (m >> i) & 1) for m in mine
        )
        self.assertEqual(mine_sets, ref_cuts, f"dicut families differ on {arcs}")

        ref_tau = ref.tau(graph)
        self.assertEqual(dx.tau_of(mine), ref_tau, f"tau differs on {arcs}")

        ref_pack = ref.find_disjoint_dijoins(graph, ref_tau)
        res = dx.analyse(n, arcs)
        self.assertEqual(
            res["holds"], ref_pack is not None,
            f"packing existence differs on {arcs}",
        )
        if res.get("packing"):
            for part in res["packing"]:
                self.assertTrue(
                    ref.is_dijoin(graph, part),
                    f"reference rejects my dijoin {part} on {arcs}",
                )
                self.assertTrue(
                    ref.is_dijoin_by_reverse_augmentation(graph, part),
                    f"reverse-augmentation test rejects {part} on {arcs}",
                )

    def test_all_loopless_labeled_digraphs_on_three_vertices(self):
        pairs = [(u, v) for u in range(3) for v in range(3) if u != v]
        for bits in range(1 << len(pairs)):
            arcs = [p for i, p in enumerate(pairs) if (bits >> i) & 1]
            self._agree(3, arcs)

    def test_all_loopless_labeled_digraphs_on_four_vertices_sample(self):
        # full 2^12 = 4096 sweep on four vertices
        pairs = [(u, v) for u in range(4) for v in range(4) if u != v]
        for bits in range(1 << len(pairs)):
            arcs = [p for i, p in enumerate(pairs) if (bits >> i) & 1]
            self._agree(4, arcs)

    def test_all_dags_on_five_vertices(self):
        pairs = [(u, v) for u in range(5) for v in range(u + 1, 5)]
        for bits in range(1 << len(pairs)):
            arcs = [p for i, p in enumerate(pairs) if (bits >> i) & 1]
            self._agree(5, arcs)

    def test_parallel_arcs_and_loops(self):
        for arcs in [
            [(0, 1), (0, 1), (1, 2), (1, 2)],
            [(0, 1), (0, 1), (0, 1)],
            [(0, 0), (0, 1), (0, 1)],
            [(0, 1), (0, 2), (0, 2), (1, 3), (2, 3), (2, 3)],
        ]:
            n = 1 + max(max(u, v) for u, v in arcs)
            self._agree(n, arcs)


class TestCondensation(unittest.TestCase):
    def test_condensation_preserves_tau_and_answer(self):
        # a 2-cycle glued in front of a diamond: SCC {0,1} contracts away.
        arcs = [(0, 1), (1, 0), (1, 2), (1, 3), (2, 4), (3, 4)]
        graph = ref.Digraph(range(5), arcs)
        cond = ref.condensation(graph)
        full = dx.analyse(5, arcs)
        small = dx.analyse(len(cond.vertices), list(cond.arcs))
        self.assertEqual(full["tau"], small["tau"])
        self.assertEqual(full["holds"], small["holds"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
