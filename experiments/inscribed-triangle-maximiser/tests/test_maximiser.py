"""Tests for the exact inscribed-triangle maximiser.

Run:  python3 -m unittest discover -s tests -q      (from this directory)

The three hand-known answers are the point of the file: an equilateral triangle inscribes
itself, the unit square's answer is the classical sec 15 degrees, and the repo's own
30-30-120 wedge witness has max side^2 = 4/9 at its 120 degree apex and NO inscribed
triangle at either 30 degree apex.  Everything else here is either an invariance, an
agreement between two independent implementations, or an external check on the LP chain.
"""
import math
import os
import sys
import unittest
from fractions import Fraction as F

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

from iet.qs3 import Q3, ONE, ZERO, SQRT3                                  # noqa: E402
from iet import maximiser as M                                            # noqa: E402
from iet.maximiser import V, vscale, rot, max_at_point, global_max        # noqa: E402
from iet.pairmax import max_at_point_pairs, feasible_ts                   # noqa: E402

EQ = [V(0, 0), V(1, 0), (Q3(1, 0, 2), Q3(0, 1, 2))]
SQ = [V(0, 0), V(1, 0), V(1, 1), V(0, 1)]
T30 = [V(-1, 0), V(1, 0), (Q3(0), Q3(0, 1, 3))]


class TestQ3(unittest.TestCase):
    def test_sign_and_equality(self):
        self.assertEqual((SQRT3 * SQRT3 - Q3(3)).sgn(), 0)
        self.assertEqual(Q3(0, 1, 1).sgn(), 1)
        self.assertEqual((Q3(7, -4, 1)).sgn(), 1)          # 7 - 4*1.732 = 0.072 > 0
        self.assertEqual((Q3(6, -4, 1)).sgn(), -1)         # 6 - 6.928 < 0
        self.assertEqual(Q3(2, 0, 4), Q3(1, 0, 2))

    def test_refuses_floats(self):
        with self.assertRaises(TypeError):
            Q3.of(0.5)
        with self.assertRaises(TypeError):
            Q3(1.0, 0, 1)

    def test_inverse(self):
        x = Q3(3, 5, 7)
        self.assertEqual(x * x.inv(), ONE)

    def test_pair_roundtrip(self):
        x = Q3(11, -4, 9)
        self.assertEqual(Q3.from_pair(x.pair()), x)


class TestKnownAnswers(unittest.TestCase):
    def test_equilateral_inscribes_itself(self):
        for O in EQ:
            r = max_at_point(O, EQ)
            self.assertTrue(r["good"])
            self.assertEqual(r["side2"], Q3(1))

    def test_unit_square_is_sec_15(self):
        for O in SQ:
            r = max_at_point(O, SQ)
            self.assertTrue(r["good"])
            self.assertEqual(r["side2"], Q3(8, -4, 1))     # 8 - 4 sqrt3
        side = float(Q3(8, -4, 1)) ** 0.5
        self.assertAlmostEqual(side, 1 / math.cos(math.radians(15)), places=12)
        self.assertAlmostEqual(side, math.sqrt(6) - math.sqrt(2), places=12)
        g = global_max(SQ, sample_ts=(F(1, 3), F(1, 2), F(2, 3), F(1, 5)))
        self.assertEqual(g["best"][1]["side2"], Q3(8, -4, 1))
        self.assertIsNone(g["lemma_v_violation"])

    def test_30_30_120(self):
        r0 = max_at_point(T30[0], T30)
        r1 = max_at_point(T30[1], T30)
        r2 = max_at_point(T30[2], T30)
        self.assertFalse(r0["good"])                        # the wedge test: 30 deg apexes
        self.assertFalse(r1["good"])
        self.assertTrue(r2["good"])
        self.assertEqual(r2["side2"], Q3(4, 0, 9))          # 4/9, NOT the 1/3 witness
        # the sibling deciders' witness at the apex has side^2 = 1/3: a valid triangle,
        # merely not the largest one.
        self.assertLess(float(Q3(1, 0, 3)), float(Q3(4, 0, 9)))

    def test_30_30_120_base_midpoint_arc(self):
        # the one arc component in the committed battery (angular lane, section 4):
        # a one-parameter family of inscribed triangles, whose largest member is side^2 = 1/3.
        r = max_at_point(V(0, 0), T30)
        self.assertEqual(r["side2"], Q3(1, 0, 3))
        self.assertEqual(max_at_point_pairs(V(0, 0), T30)["side2"], Q3(1, 0, 3))


class TestInvariance(unittest.TestCase):
    def test_scaling(self):
        base = max_at_point(V(0, 0), SQ)["side2"]
        big = max_at_point(V(0, 0), [vscale(3, p) for p in SQ])["side2"]
        self.assertEqual(big, base * Q3(9))

    def test_rotation_by_60(self):
        base = max_at_point(V(0, 0), SQ)["side2"]
        turned = max_at_point(rot(V(0, 0), 1), [rot(p, 1) for p in SQ])["side2"]
        self.assertEqual(turned, base)

    def test_reflection(self):
        base = max_at_point(V(0, 0), T30)["side2"]
        mirror = [(p[0], -p[1]) for p in T30]
        self.assertEqual(max_at_point(V(0, 0), mirror)["side2"], base)


class TestTwoMaximisersAgree(unittest.TestCase):
    """The direction-space maximiser against the edge-pair maximiser."""

    def _agree(self, poly, pts):
        for O in pts:
            a = max_at_point(O, poly)
            b = max_at_point_pairs(O, poly)
            self.assertEqual(a["good"], b["good"], msg=str(M.vfloat(O)))
            if a["good"]:
                self.assertEqual(a["side2"], b["side2"], msg=str(M.vfloat(O)))

    def test_controls(self):
        for poly in (EQ, SQ, T30):
            pts = list(poly) + [M.vadd(A, M.vscale(Q3.of(F(1, 3)), M.vsub(B, A)))
                                for A, B in M.edges(poly)]
            self._agree(poly, pts)

    def test_fixtures_sample(self):
        from iet import siblings as S
        names = ["ncv-star6", "ncv-dart", "ncv-L", "cvx-12gon", "cvx-sliver-tri",
                 "ncv-cstrip-h1_2", "cvx-60deg-kite", "rand-convex-007"]
        for nm in names:
            poly, _ = S.load_fixture(nm)
            pts = list(poly) + [M.vadd(A, M.vscale(Q3.of(F(2, 5)), M.vsub(B, A)))
                                for A, B in M.edges(poly)]
            self._agree(poly, pts)


class TestSiblingDeciders(unittest.TestCase):
    def test_agreement_and_witness_acceptance(self):
        from iet import siblings as S
        for nm in ("ctl-unit-square", "ctl-tri-30-30-120", "ctl-equilateral",
                   "ncv-star6", "ncv-dart", "cvx-hexagon"):
            poly, _ = S.load_fixture(nm)
            for O in poly:
                r = max_at_point(O, poly)
                pd = S.poly_decide(poly, O)["good"]
                ad = S.ang_decide(poly, O)[0]
                self.assertEqual(bool(pd), r["good"], msg=nm)
                self.assertEqual(bool(ad), r["good"], msg=nm)
                if r["good"]:
                    self.assertTrue(S.poly_verify(poly, O, r["P"], r["Q"])[0], msg=nm)
                    self.assertTrue(S.ang_verify(poly, O, r["P"], r["Q"])[0], msg=nm)
                    self.assertEqual(r["side2"].sgn(), 1)


class TestPairmaxBranches(unittest.TestCase):
    def test_interval_branch(self):
        # O at the base midpoint of the 30-30-120: the rotate of the right edge's LINE is
        # the left edge's line, so a whole interval of t is feasible for that pair.
        E = M.edges(T30)
        (A, B) = E[1]          # right edge
        (C, D) = E[2]          # left edge
        ts = feasible_ts(V(0, 0), A, B, C, D, 1)
        self.assertEqual(len(ts), 2, msg="expected a genuine interval of feasible t")
        self.assertNotEqual(ts[0], ts[1])

    def test_point_branch(self):
        E = M.edges(SQ)
        ts = feasible_ts(SQ[0], E[1][0], E[1][1], E[2][0], E[2][1], 1)
        self.assertLessEqual(len(ts), 1)


class TestLPChainOnKnownBodies(unittest.TestCase):
    """The containment bound must never fall BELOW a known answer."""

    def test_disk(self):
        from iet import cw
        r = cw.run(J=96, D=300, eps=F(0), s_ub=F(12, 5))
        s = r["side_upper_display"]
        self.assertGreater(s, math.sqrt(3))                 # sound
        self.assertLess(s, math.sqrt(3) * 1.05)             # and not absurdly loose

    def test_unit_square(self):
        from iet import cw, lp
        hps = lp.halfplanes_from_convex_polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
        r = cw.run(D=300, s_ub=F(6, 5), hps=hps)
        truth = float(Q3(8, -4, 1)) ** 0.5                  # sec 15 degrees
        self.assertGreater(r["side_upper_display"], truth)
        self.assertLess(r["side_upper_display"], truth * 1.05)
        # ... and the polygon maximiser's exact inscribed answer is below the containment
        # bound, as m(K) <= M(K) demands.
        self.assertLess(float(max_at_point(V(0, 0), SQ)["side2"]),
                        r["side2_upper_display"])

    def test_sqrt3_brackets(self):
        from iet import cw
        cw._check_sqrt3_brackets()


if __name__ == "__main__":
    unittest.main()
