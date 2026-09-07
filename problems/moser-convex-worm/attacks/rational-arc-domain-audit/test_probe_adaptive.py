import unittest
from collections import Counter

import probe_adaptive as probe


class AdaptiveProbeTests(unittest.TestCase):
    def test_cardinal_trig_values_are_enclosed(self):
        for angle, sine, cosine in ((0, 0, 1), (90, 1, 0), (180, 0, -1)):
            sr = probe.sin_range(probe.I(angle))
            cr = probe.cos_range(probe.I(angle))
            self.assertLessEqual(sr.lo, sine)
            self.assertGreaterEqual(sr.hi, sine)
            self.assertLessEqual(cr.lo, cosine)
            self.assertGreaterEqual(cr.hi, cosine)

    def test_coarse_subtree_exactly_replays_coverage(self):
        stats = Counter()
        ty, theta = probe.I(-probe.D, probe.D), probe.I(0, 180)
        tree = probe.build(ty, theta, 0, 5, stats)
        probe.verify_cover(tree, ty, theta)
        leaves = stats["pruned"]+stats["unresolved"]
        splits = stats["split_ty"]+stats["split_theta"]
        self.assertEqual(leaves, splits+1)
        self.assertEqual(stats["nodes"], 2*leaves-1)

    def test_coverage_verifier_rejects_changed_split(self):
        stats = Counter()
        ty, theta = probe.I(-probe.D, probe.D), probe.I(0, 180)
        tree = probe.build(ty, theta, 0, 2, stats)
        tree["mid"] = "1"
        with self.assertRaises(AssertionError):
            probe.verify_cover(tree, ty, theta)


if __name__ == "__main__":
    unittest.main()
