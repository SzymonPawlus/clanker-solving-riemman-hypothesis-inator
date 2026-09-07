from fractions import Fraction as F
import unittest

import verify_four_edge as v


class FourEdgeCertificateTests(unittest.TestCase):
    def test_surd_order_is_exact(self):
        self.assertLess(v.S(0, 1), v.S(2, 0))
        self.assertLess(v.S(-2, 0), v.S(0, -1))
        self.assertFalse(v.S(1, 1) < v.S(2, 0))

    def test_open_worm_and_balanced_boundary(self):
        tangents, loads = v.exact_data()
        self.assertEqual(sum(loads[:4]), 1)
        self.assertEqual(sum(loads[i] * tangents[i][0] for i in range(5)), 0)
        self.assertEqual(sum(loads[i] * tangents[i][1] for i in range(5)), 0)
        self.assertEqual(loads[-1], F(11984563, 25510200))

    def test_all_maximal_three_cycles(self):
        tangents, loads = v.exact_data()
        cycles = v.maximal_three_cycles(tangents, loads)
        self.assertEqual([inds for inds, _ in cycles],
                         [(0, 2, 4), (0, 3, 4), (1, 2, 4), (1, 3, 4)])
        for _, allocation in cycles:
            self.assertEqual(sum(allocation[i] * tangents[i][0] for i in range(5)), 0)
            self.assertEqual(sum(allocation[i] * tangents[i][1] for i in range(5)), 0)
            self.assertTrue(all(0 <= x <= cap for x, cap in zip(allocation, loads)))

    def test_exact_triangle_orientation_floors(self):
        tangents, loads = v.exact_data()
        cycles = v.maximal_three_cycles(tangents, loads)
        got = {inds: v.triangle_floor(tangents, allocation)
               for inds, allocation in cycles}
        cross = v.S(F(231, 414800), F(399091, 19910400))
        self.assertEqual(got[(0, 2, 4)], cross)
        self.assertEqual(got[(1, 3, 4)], cross)
        self.assertEqual(got[(0, 3, 4)], v.S(F(163, 1968), 0))
        self.assertEqual(got[(1, 2, 4)], v.S(0, F(399091, 9955200)))

    def test_complete_exact_angular_cover(self):
        tangents, loads = v.exact_data()
        cycles = v.maximal_three_cycles(tangents, loads)
        _, leaves = v.certify_cover(tangents, loads, cycles)
        self.assertEqual(len(leaves), 70)
        self.assertEqual(leaves[0][0], 0)
        self.assertEqual(leaves[-1][1], 1)


if __name__ == "__main__":
    unittest.main()
