import unittest

import probe_adaptive as base
import probe_mixed as probe


class MixedPredicateTests(unittest.TestCase):
    def test_nontrivial_mixed_box_clears_target(self):
        box = dict(probe.ROOTS)
        box["alpha"] = base.I(88, 90)
        box["theta"] = base.I(130, 140)
        box["ty"] = base.I(base.D-probe.Q(1, 100), base.D)
        box["square_ty"] = base.I(base.D-probe.Q(1, 100), base.D)
        self.assertGreater(probe.mixed_margin(box), 0)

    def test_sign_uncertain_mixed_box_cannot_prune(self):
        self.assertLess(probe.mixed_margin(dict(probe.ROOTS)), 0)


if __name__ == "__main__":
    unittest.main()
