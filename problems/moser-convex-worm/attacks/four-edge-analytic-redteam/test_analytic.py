import unittest
from fractions import Fraction as Q

import check_analytic as a


class AnalyticRedTeamTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.q, cls.coeff, cls.old, cls.sharp, cls.bottleneck = a.analytic()

    def test_claimed_floor_and_stronger_floor(self):
        self.assertTrue(all(m.sign() > 0 for _, _, m in self.old))
        self.assertTrue(all(m.sign() > 0 for _, _, m in self.sharp))

    def test_exact_bottleneck_isolation(self):
        _, (lo, hi) = self.bottleneck
        self.assertGreater(lo, Q(235068284611, 10**12))
        self.assertLess(hi, Q(235068284612, 10**12))
        self.assertLess(hi - lo, Q(1, 10**30))

    def test_target_above_bottleneck_is_refuted(self):
        _, (_, hi) = self.bottleneck
        self.assertLess(hi, Q(235068285, 10**9))

    def test_allocation_capacity_mutation(self):
        vs, loads = a.hull()
        xs = a.allocations(vs, loads)
        bad = list(xs[(0, 2, 4)])
        bad[2] += Q(1, 10**12)
        self.assertGreater(bad[2], loads[2])

    def test_direct_motion_termwise_symmetry(self):
        vs, _ = a.hull()
        mirror = (3, 2, 1, 0, 4)
        for u in (Q(0), Q(1, 72), Q(157, 697), Q(1, 3), Q(3, 4), Q(1)):
            sn, cs = 2*u/(1+u*u), (1-u*u)/(1+u*u)
            for i, v in enumerate(vs):
                left = abs(v[0]*sn + v[1]*cs)  # phi -> pi-phi
                vm = vs[mirror[i]]
                right = abs(vm[0]*sn - vm[1]*cs)
                self.assertEqual(left, right)

    def test_surd_comparison_adversaries(self):
        self.assertEqual(a.sgn(Q(-265, 153), Q(1)), 1)
        self.assertEqual(a.sgn(Q(-1351, 780), Q(1)), -1)
        self.assertEqual(a.sgn(Q(265, 153), Q(-1)), -1)
        self.assertEqual(a.sgn(Q(1351, 780), Q(-1)), 1)


if __name__ == '__main__':
    unittest.main()
