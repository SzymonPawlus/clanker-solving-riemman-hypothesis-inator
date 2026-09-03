import unittest
import solve_kkt as s

class EquationTests(unittest.TestCase):
    def test_reported_neighborhood(self):
        x=[0.01886026338237,0.80050851849538,0.34141264634836]
        w=s.wells(x)
        self.assertLess(max(w)-min(w),1e-12)
        self.assertTrue(0.23518745714<min(w)<0.23518745716)
    def test_positive_kkt_and_negative_curvature(self):
        x=[0.01886026338237,0.80050851849538,0.34141264634836]
        G=s.gradients(x);lam=s.multipliers(G)
        self.assertTrue(all(z>0 for z in lam))
        _,_,curvature=s.constrained_curvature(x,G)
        self.assertLess(curvature,-0.28)
    def test_outer_angle_independent_of_lengths(self):
        ta,tb=.01886026338237,.80050851849538
        def outer_sine(p):
            ca,sa=s.trig(ta);cb,sb=s.trig(tb)
            return sb*(ca*3**.5-sa)/(4*(sb*ca-cb*sa))
        self.assertEqual(outer_sine(.2),outer_sine(.4))

if __name__=='__main__':unittest.main()
