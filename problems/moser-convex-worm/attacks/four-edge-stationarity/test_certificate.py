import unittest
from fractions import Fraction as Q

import certify_rational_improvement as c


class PerturbedCertificateTests(unittest.TestCase):
    def test_full_replay(self):
        c.main()

    def test_unit_and_open_length(self):
        vs, loads = c.geometry()
        self.assertEqual(sum(loads[:4]), 1)
        self.assertTrue(all(c.dot(v, v) == 1 for v in vs))

    def test_all_allocations_balanced(self):
        vs, loads = c.geometry()
        xs = c.allocations(vs, loads)
        self.assertEqual(tuple(xs), ((0,2,4),(0,3,4),(1,2,4),(1,3,4)))

    def test_inflated_target_breaks_tight_endpoint(self):
        vs, loads = c.geometry(); xs = c.allocations(vs, loads)
        x = xs[(1,2,4)]; q = c.tri_floor(x, vs)
        a,b = c.coefficients(x,vs,loads,Q(1,10),Q(0),Q(4487,20000))
        value = c.value(q,a,b,Q(4487,20000))
        self.assertFalse((value-Q(23519,100000)).positive())

    def test_surd_sign_adversaries(self):
        self.assertGreater(c.sign(Q(-265,153),Q(1)),0)
        self.assertLess(c.sign(Q(-1351,780),Q(1)),0)


if __name__ == '__main__': unittest.main()
