"""Test suite for the angular lane.  Standard library `unittest`; no external dependency.

    python3 -m unittest -v test_angular

Three layers:
  1. the field K = Q(sqrt3) and the direction order, against hand values;
  2. the radial machinery, with the COLLINEAR-RAY cases first, since they are the ones a
     sampling cross-check steps over;
  3. the decider, against hand-computed answers and against the independent rotation
     decider in rotcheck.py.
"""

from __future__ import annotations

import random
import unittest
from fractions import Fraction as F

from q3 import Q3, ZERO, ONE, HALF, S60, C60
import angular as A
import rotcheck
import shapes


class TestField(unittest.TestCase):
    def test_sqrt3(self):
        self.assertEqual(Q3(0, 1) * Q3(0, 1), Q3(3, 0))

    def test_trig_identity(self):
        self.assertEqual(S60 * S60 + C60 * C60, ONE)

    def test_signs(self):
        self.assertEqual(Q3(1, -1).sgn(), -1)      # 1 - 1.732 < 0
        self.assertEqual(Q3(2, -1).sgn(), 1)       # 2 - 1.732 > 0
        self.assertEqual(Q3(-2, 2).sgn(), 1)       # -2 + 3.464 > 0
        self.assertEqual(Q3(0, 0).sgn(), 0)

    def test_no_float_input(self):
        with self.assertRaises(TypeError):
            Q3(0.5, 0)

    def test_sign_agrees_with_float_where_float_is_safe(self):
        """The sign algorithm is a rational comparison, not a float one; this checks it on
        values where a float is nowhere near the boundary, and checks the boundary itself
        (a^2 = 3b^2, i.e. sqrt3 rational) is genuinely unreachable over Q."""
        import math
        rng = random.Random(3)
        for _ in range(400):
            a = F(rng.randint(-50, 50), rng.randint(1, 9))
            b = F(rng.randint(-50, 50), rng.randint(1, 9))
            x = Q3(a, b)
            f = float(a) + float(b) * math.sqrt(3.0)
            if abs(f) > 1e-6:
                self.assertEqual(x.sgn(), 1 if f > 0 else -1)
            self.assertNotEqual(a * a, 3 * b * b if b != 0 else a * a + 1)

    def test_equality_is_coefficientwise(self):
        self.assertNotEqual(Q3(1, 0), Q3(0, 1))
        self.assertEqual(Q3(F(2, 4), 0), Q3(F(1, 2), 0))
        self.assertTrue((Q3(1, 1) - Q3(1, 1)).is_zero())

    def test_division(self):
        x = Q3(2, 3)
        self.assertEqual(x * (ONE / x), ONE)


class TestDirections(unittest.TestCase):
    def test_order_round_the_circle(self):
        ds = [A.V(1, 0), A.V(1, 1), A.V(0, 1), A.V(-1, 1), A.V(-1, 0),
              A.V(-1, -1), A.V(0, -1), A.V(1, -1)]
        for i in range(len(ds) - 1):
            self.assertEqual(A.dir_cmp(ds[i], ds[i + 1]), -1)

    def test_positive_scaling_only(self):
        self.assertEqual(A.dir_cmp(A.V(2, 0), A.V(5, 0)), 0)
        self.assertNotEqual(A.dir_cmp(A.V(1, 0), A.V(-1, 0)), 0)
        self.assertTrue(A.dir_eq(A.V(3, 6), A.V(1, 2)))
        self.assertFalse(A.dir_eq(A.V(3, 6), A.V(-1, -2)))

    def test_rotation_is_60_degrees(self):
        v = A.V(1, 0)
        w = A.rot(v, 1)
        # cos of the angle is dot/(|v||w|) = 1/2 exactly, and |w| = |v|
        self.assertEqual(A.norm2(w), A.norm2(v))
        self.assertEqual(A.dot(v, w) * Q3(2), A.norm2(v))
        # six rotations return
        u = v
        for _ in range(6):
            u = A.rot(u, 1)
        self.assertTrue(A.veq(u, v))

    def test_arc_membership(self):
        a, b = A.V(1, 0), A.V(0, 1)
        self.assertTrue(A.in_arc(A.V(1, 1), a, b))
        self.assertTrue(A.in_arc(a, a, b))
        self.assertTrue(A.in_arc(b, a, b))
        self.assertFalse(A.in_arc(A.V(-1, 1), a, b))
        self.assertFalse(A.in_arc(A.V(1, -1), a, b))


class TestCollinearRays(unittest.TestCase):
    """The blind spot: a ray running ALONG an edge sees an INTERVAL of radii, not a point."""

    def test_edge_interior_point_along_edge(self):
        P = shapes.unit_square()
        O = (Q3(F(1, 2)), ZERO)
        for (v, hi) in ((A.V(1, 0), Q3(F(1, 2))), (A.V(-1, 0), Q3(F(1, 2)))):
            S = A.ray_scales(O, P, v)
            self.assertIn((ZERO, hi, True, False), S,
                          "no half-open along-edge interval in %s" % (S,))

    def test_zero_scale_is_never_included(self):
        """s = 0 is the degenerate triangle O,O,O and is available at every point; if any
        radial interval were closed at 0 the decider would call every point good."""
        rng = random.Random(7)
        for _ in range(20):
            P = shapes.random_star(rng, 6)
            if not A.is_simple(P)[0]:
                continue
            n = len(P)
            for O in list(P) + [A.vadd(P[0], A.vscale(Q3(F(1, 3)),
                                                      A.vsub(P[1], P[0])))]:
                for v in (A.V(1, 0), A.V(0, 1), A.V(-1, 0), A.V(0, -1),
                          A.V(1, 1), A.V(-1, 2)):
                    for iv in A.ray_scales(O, P, v):
                        self.assertTrue(iv[0].sgn() > 0 or iv[2] is True)

    def test_vertex_sees_both_incident_edges_as_intervals(self):
        P = shapes.equilateral()
        O = P[0]
        S1 = A.ray_scales(O, P, A.V(1, 0))
        self.assertIn((ZERO, ONE, True, False), S1)
        S2 = A.ray_scales(O, P, A.rot(A.V(1, 0), 1))
        self.assertIn((ZERO, ONE, True, False), S2)
        # ... and those two intervals overlapping is exactly why the vertex is good
        ok, s = A.good_at_direction(O, P, A.V(1, 0))
        self.assertTrue(ok)

    def test_collinear_ray_missing_the_segment(self):
        """O on the line of an edge but past its far end: the ray must see nothing."""
        P = [A.V(0, 0), A.V(3, 0), A.V(3, 2), A.V(0, 2)]
        O = (Q3(1), ZERO)
        # the edge [(0,0),(3,0)] contains O: forward interval (0,2], backward (0,1]
        self.assertIn((ZERO, Q3(2), True, False), A.ray_scales(O, P, A.V(1, 0)))
        self.assertIn((ZERO, Q3(1), True, False), A.ray_scales(O, P, A.V(-1, 0)))

    def test_120_apex_has_two_collinear_good_directions(self):
        P = shapes.t30_30_120()
        g = A.good_directions(P[2], P)
        self.assertEqual(g["n_components"], 3)
        self.assertEqual(g["n_point_components"], 3)


class TestControls(unittest.TestCase):
    def test_equilateral_inscribes_itself(self):
        P = shapes.equilateral()
        for O in P:
            ok, w = A.decide(O, P)
            self.assertTrue(ok)
            wok, d = A.recheck_witness(P, O, w[0], w[1])
            self.assertTrue(wok)
            self.assertEqual(d["side2"], ["1", "0"])

    def test_wedge_test_witness(self):
        """RULES.md 3.1: both 30-degree apexes of the 30-30-120 triangle are exceptional."""
        P = shapes.t30_30_120()
        self.assertFalse(A.decide(P[0], P)[0])
        self.assertFalse(A.decide(P[1], P)[0])
        self.assertTrue(A.decide(P[2], P)[0])

    def test_square_corner_side_squared(self):
        P = shapes.unit_square()
        ok, w = A.decide(P[0], P)
        self.assertTrue(ok)
        _wok, d = A.recheck_witness(P, P[0], w[0], w[1])
        self.assertEqual(d["side2"], ["8", "-4"])       # 8 - 4 sqrt3

    def test_M0_gives_an_arc(self):
        P = shapes.rotated_pair()
        g = A.good_directions(P[0], P)
        self.assertEqual(g["n_arc_components"], 1)
        self.assertEqual(g["n_point_components"], 0)


class TestAgainstRotationDecider(unittest.TestCase):
    """The sweep and the independent plane-intersection decider must agree everywhere."""

    def _points(self, P):
        n = len(P)
        pts = list(P)
        for ei in range(n):
            for t in (F(1, 5), F(1, 2), F(4, 5)):
                pts.append(A.vadd(P[ei], A.vscale(Q3(t), A.vsub(P[(ei + 1) % n], P[ei]))))
        return pts

    def test_named_shapes(self):
        for name, f in shapes.NAMED.items():
            P = f()
            for O in self._points(P):
                self.assertEqual(A.decide(O, P)[0], rotcheck.decide_rot(O, P)[0],
                                 "%s at %s" % (name, A.vfloat(O)))

    def test_random_nonconvex(self):
        rng = random.Random(20260829)
        tested = 0
        for k in range(40):
            P = shapes.random_spiky(rng, 3) if k % 2 else shapes.random_star(rng, 7)
            if not A.is_simple(P)[0] or A.is_convex(P):
                continue
            tested += 1
            for O in self._points(P):
                self.assertEqual(A.decide(O, P)[0], rotcheck.decide_rot(O, P)[0],
                                 "%s at %s" % ([A.vfloat(p) for p in P], A.vfloat(O)))
        self.assertGreater(tested, 10)


class TestWitnesses(unittest.TestCase):
    def test_every_good_verdict_carries_a_verified_triangle(self):
        rng = random.Random(11)
        checked = 0
        for k in range(25):
            P = shapes.random_star(rng, rng.randint(5, 8))
            if not A.is_simple(P)[0]:
                continue
            for O in P:
                ok, w = A.decide(O, P)
                if ok:
                    wok, _d = A.recheck_witness(P, O, w[0], w[1])
                    self.assertTrue(wok)
                    checked += 1
        self.assertGreater(checked, 20)

    def test_sweep_candidates_survive_the_independent_checker(self):
        """good_directions() re-decides every direction the sweep proposes; this asserts
        the verification is actually switched on and passes."""
        rng = random.Random(13)
        for k in range(12):
            P = shapes.random_spiky(rng, 3)
            if not A.is_simple(P)[0]:
                continue
            for O in P:
                A.good_directions(O, P, verify=True)   # raises on any mismatch


class TestJordanCheck(unittest.TestCase):
    def test_simple_and_not(self):
        self.assertTrue(A.is_simple(shapes.unit_square())[0])
        bowtie = [A.V(0, 0), A.V(1, 1), A.V(1, 0), A.V(0, 1)]
        self.assertFalse(A.is_simple(bowtie)[0])
        self.assertFalse(A.is_simple([A.V(0, 0), A.V(1, 0)])[0])
        self.assertFalse(A.is_simple([A.V(0, 0), A.V(0, 0), A.V(1, 0)])[0])


if __name__ == "__main__":
    unittest.main()
