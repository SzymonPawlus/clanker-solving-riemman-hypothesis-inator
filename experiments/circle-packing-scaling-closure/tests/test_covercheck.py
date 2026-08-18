"""Tests for the Q(sqrt 3) cover verifier and the proposal-J scaling step."""

from __future__ import annotations

import copy
import json
import sys
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import covercheck  # noqa: E402
from covercheck import (  # noqa: E402
    CertificateError,
    clip_convex,
    doubled_area,
    parse_point,
    scaled_certificate,
    squared_distance,
    verify,
)
from generate_graham6_exact import CRITICAL_SIDE, graham_six_cell  # noqa: E402
from generate_graham15_exact import graham_fifteen_cell  # noqa: E402
from qsqrt3 import Q3  # noqa: E402

FOUR = Q3(4, 0)


class TestQ3(unittest.TestCase):
    def test_sign_of_mixed_signs(self):
        # 1 - sqrt(3) < 0 while 2 - sqrt(3) > 0; both need the a^2 vs 3b^2 test.
        self.assertEqual(Q3(1, -1).sign(), -1)
        self.assertEqual(Q3(2, -1).sign(), 1)
        self.assertEqual(Q3(-1, 1).sign(), 1)
        self.assertEqual(Q3(-2, 1).sign(), -1)
        self.assertEqual(Q3(0, 0).sign(), 0)

    def test_sign_agrees_with_high_precision_floats(self):
        for a in range(-4, 5):
            for b in range(-4, 5):
                value = float(a) + float(b) * 3.0 ** 0.5
                expected = 0 if a == 0 and b == 0 else (1 if value > 0 else -1)
                self.assertEqual(Q3(a, b).sign(), expected, (a, b))

    def test_inverse_and_division(self):
        x = Q3(2, 3)
        self.assertEqual(x * x.inverse(), Q3(1, 0))
        self.assertEqual((x / x), Q3(1, 0))
        with self.assertRaises(ZeroDivisionError):
            Q3(0, 0).inverse()

    def test_sqrt3_squares_to_three(self):
        self.assertEqual(Q3(0, 1) * Q3(0, 1), Q3(3, 0))

    def test_delta_is_the_algebraic_root(self):
        delta = Q3(1, 1).inverse()  # 1/(1+sqrt 3)
        self.assertEqual(delta, Q3(Fraction(-1, 2), Fraction(1, 2)))
        self.assertEqual(delta * Q3(1, 1), Q3(1, 0))


class TestObliqueForm(unittest.TestCase):
    def test_quadratic_form_matches_euclidean_distance(self):
        """q(du,dv)=du^2+du*dv+dv^2 must equal |dx|^2+|dy|^2 after the shear."""
        for du in range(-3, 4):
            for dv in range(-3, 4):
                dx = Fraction(du) + Fraction(dv, 2)
                euclid_sq = dx * dx + Fraction(3, 4) * dv * dv  # (dv*sqrt3/2)^2
                q = squared_distance((Q3(du, 0), Q3(dv, 0)), (Q3(0, 0), Q3(0, 0)))
                self.assertEqual(q, Q3(euclid_sq, 0), (du, dv))


class TestClipping(unittest.TestCase):
    def _tri(self, pts):
        return [(Q3(x, 0), Q3(y, 0)) for x, y in pts]

    def test_overlapping_triangles_have_positive_intersection(self):
        a = self._tri([(0, 0), (4, 0), (0, 4)])
        b = self._tri([(1, 1), (5, 1), (1, 5)])
        self.assertNotEqual(doubled_area(clip_convex(a, b)), Q3(0, 0))

    def test_edge_sharing_triangles_have_zero_intersection(self):
        a = self._tri([(0, 0), (2, 0), (0, 2)])
        b = self._tri([(2, 0), (2, 2), (0, 2)])
        overlap = clip_convex(a, b)
        self.assertEqual(doubled_area(overlap) if overlap else Q3(0, 0), Q3(0, 0))


class TestGrahamSixCellAtCriticalSide(unittest.TestCase):
    def setUp(self):
        self.cert = graham_six_cell(CRITICAL_SIDE)

    def test_nonstrict_cover_exists_at_the_exact_critical_side(self):
        report = verify(self.cert, "nonstrict")
        self.assertEqual(report.cells, 6)
        self.assertEqual(report.side, Q3(2, 2))
        self.assertEqual(report.max_squared_diameter, FOUR)

    def test_cover_is_exactly_tight_not_slack(self):
        """A slack cover at d* would contradict the cited d(7) = 2 + 2 sqrt(3)."""
        report = verify(self.cert, "nonstrict")
        self.assertFalse(report.max_squared_diameter < FOUR)

    def test_strict_mode_rejects_at_the_critical_side(self):
        with self.assertRaises(CertificateError):
            verify(self.cert, "strict")

    def test_scaling_makes_every_cell_strictly_subcritical(self):
        for lam in ("1/2", "9/10", "999999/1000000"):
            factor = Fraction(lam)
            scaled = scaled_certificate(self.cert, factor)
            report = verify(scaled, "strict")
            self.assertTrue(report.max_squared_diameter < FOUR, lam)
            self.assertEqual(report.side, Q3(2, 2) * Q3(factor, 0))
            # Diameter is homogeneous of degree one, so squared diameter scales
            # by lambda^2 exactly and uniformly across cells.
            self.assertEqual(report.max_squared_diameter, FOUR * Q3(factor * factor, 0))

    def test_slightly_larger_side_breaks_the_nonstrict_bound(self):
        bigger = graham_six_cell(Q3(Fraction(2000001, 1000000), 2))
        with self.assertRaises(CertificateError):
            verify(bigger, "nonstrict")

    def test_removing_a_cell_is_caught_as_a_coverage_gap(self):
        broken = copy.deepcopy(self.cert)
        broken["cells"] = broken["cells"][:-1]
        broken["n"] = 6
        with self.assertRaises(CertificateError):
            verify(broken, "nonstrict")

    def test_shrinking_a_cell_is_caught_as_a_coverage_gap(self):
        broken = copy.deepcopy(self.cert)
        broken["cells"][3][0] = [["1", "0"], ["1", "0"]]
        with self.assertRaises(CertificateError):
            verify(broken, "nonstrict")

    def test_wrong_cell_count_is_rejected(self):
        broken = copy.deepcopy(self.cert)
        broken["n"] = 8
        with self.assertRaises(CertificateError):
            verify(broken, "nonstrict")

    def test_decimal_scalars_are_rejected(self):
        broken = copy.deepcopy(self.cert)
        broken["cells"][0][0] = [["0.5", "0"], ["0", "0"]]
        with self.assertRaises(CertificateError):
            verify(broken, "nonstrict")


class TestGrahamFifteenCellAtCriticalSide(unittest.TestCase):
    def test_fifteen_cell_cover_exists_at_2_plus_4_sqrt3(self):
        # Existence of this cover gives C(16) >= 2 + 4*sqrt(3) only; it is not an
        # upper bound on the ceiling. See README section 6.1.
        cert = graham_fifteen_cell()
        report = verify(cert, "nonstrict")
        self.assertEqual(report.cells, 15)
        self.assertEqual(report.side, Q3(2, 4))
        self.assertEqual(report.max_squared_diameter, FOUR)

    def test_scaled_fifteen_cell_is_strict(self):
        scaled = scaled_certificate(graham_fifteen_cell(), Fraction(9, 10))
        self.assertTrue(verify(scaled, "strict").max_squared_diameter < FOUR)


class TestCommittedCertificates(unittest.TestCase):
    def test_committed_files_match_the_generators(self):
        pairs = [
            ("n007-graham6-critical.json", graham_six_cell(CRITICAL_SIDE)),
            ("n016-graham15-critical.json", graham_fifteen_cell()),
        ]
        for name, generated in pairs:
            stored = json.loads((ROOT / "certificates" / name).read_text())
            self.assertEqual(stored, json.loads(json.dumps(generated)), name)
            verify(stored, "nonstrict")


if __name__ == "__main__":
    unittest.main()
