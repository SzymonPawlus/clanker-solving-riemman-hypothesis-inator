from __future__ import annotations

import copy
import json
import sys
import unittest
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from generate_grid import grid_certificate  # noqa: E402
from generate_graham6 import graham_six_cell_certificate  # noqa: E402
from generate_open_baselines import open_baseline  # noqa: E402
from partitioncheck import CertificateError, verify_certificate  # noqa: E402
from search_graham6 import pattern_search  # noqa: E402


FIXTURE = ROOT / "certificates" / "n003-d1999-over-1000.json"
N4_FIXTURE = ROOT / "certificates" / "n004-d433-over-125.json"
N5_FIXTURE = ROOT / "certificates" / "n005-d3999-over-1000.json"
N6_FIXTURE = ROOT / "certificates" / "n006-d3999-over-1000.json"
N7_FIXTURE = ROOT / "certificates" / "n007-graham6-rationalized.json"


def fixture() -> dict[str, object]:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def n4_fixture() -> dict[str, object]:
    return json.loads(N4_FIXTURE.read_text(encoding="utf-8"))


class PartitionCertificateTests(unittest.TestCase):
    def test_known_valid_median_partition(self) -> None:
        report = verify_certificate(fixture())
        self.assertEqual(report.n, 3)
        self.assertEqual(str(report.triangle_side), "1999/1000")
        self.assertLess(report.maximum_squared_diameter, 4)

    def test_shared_boundary_is_allowed(self) -> None:
        self.assertEqual(verify_certificate(fixture()).cells, 2)

    def test_graham_three_cell_calibration(self) -> None:
        report = verify_certificate(n4_fixture())
        self.assertEqual(report.n, 4)
        self.assertEqual(report.cells, 3)
        self.assertEqual(str(report.maximum_squared_diameter), "187489/46875")

    def test_graham_four_and_five_cell_calibrations(self) -> None:
        for path, expected_n in ((N5_FIXTURE, 5), (N6_FIXTURE, 6)):
            with self.subTest(n=expected_n):
                data = json.loads(path.read_text(encoding="utf-8"))
                report = verify_certificate(data)
                self.assertEqual(report.n, expected_n)
                self.assertEqual(report.cells, expected_n - 1)
                self.assertEqual(str(report.maximum_squared_diameter), "15992001/4000000")

    def test_regular_grid_generator_frequencies_one_through_six(self) -> None:
        for m in range(1, 7):
            with self.subTest(m=m):
                data = grid_certificate(m, Fraction(2 * m) - Fraction(1, 1000))
                report = verify_certificate(data)
                self.assertEqual(report.n, m * m + 1)
                self.assertEqual(report.cells, m * m)
                self.assertLess(report.maximum_squared_diameter, 4)

    def test_rationalized_graham_six_cell_calibration(self) -> None:
        generated = graham_six_cell_certificate()
        committed = json.loads(N7_FIXTURE.read_text(encoding="utf-8"))
        self.assertEqual(committed, generated)
        report = verify_certificate(committed)
        self.assertEqual(report.n, 7)
        self.assertEqual(report.cells, 6)
        self.assertEqual(
            str(report.maximum_squared_diameter),
            "6249769587629311467/1562500000000000000",
        )

    def test_fixed_topology_search_rediscovers_graham_parameters(self) -> None:
        delta, r, value, evaluations = pattern_search(tolerance=1e-9)
        self.assertAlmostEqual(delta, 1 / (1 + 3**0.5), places=6)
        self.assertAlmostEqual(r, delta / 3**0.5, places=6)
        self.assertAlmostEqual(value, delta * delta, places=6)
        self.assertGreater(evaluations, 1)

    def test_first_open_case_grid_baselines_are_exactly_valid(self) -> None:
        for n in range(16, 20):
            with self.subTest(n=n):
                report = verify_certificate(open_baseline(n))
                self.assertEqual(report.n, n)
                self.assertEqual(report.cells, n - 1)
                self.assertLess(report.maximum_squared_diameter, 4)

    def test_overlap_compensating_for_a_hole_is_rejected(self) -> None:
        data = fixture()
        data["cells"][1] = copy.deepcopy(data["cells"][0])
        with self.assertRaisesRegex(CertificateError, "overlap with positive area"):
            verify_certificate(data)

    def test_area_gap_is_rejected(self) -> None:
        data = fixture()
        data["cells"][1][2] = ["0", "999/1000"]
        with self.assertRaisesRegex(CertificateError, "area sum"):
            verify_certificate(data)

    def test_vertex_outside_triangle_is_rejected(self) -> None:
        data = fixture()
        data["cells"][0][1] = ["2", "0"]
        with self.assertRaisesRegex(CertificateError, "outside"):
            verify_certificate(data)

    def test_clockwise_cell_is_rejected(self) -> None:
        data = fixture()
        data["cells"][0] = list(reversed(data["cells"][0]))
        with self.assertRaisesRegex(CertificateError, "counterclockwise"):
            verify_certificate(data)

    def test_repeated_vertex_is_rejected(self) -> None:
        data = fixture()
        data["cells"][0][2] = copy.deepcopy(data["cells"][0][1])
        with self.assertRaisesRegex(CertificateError, "repeated"):
            verify_certificate(data)

    def test_cell_count_is_exactly_n_minus_one(self) -> None:
        data = fixture()
        data["cells"].pop()
        with self.assertRaisesRegex(CertificateError, "n-1"):
            verify_certificate(data)

    def test_diameter_must_be_strictly_less_than_two(self) -> None:
        data = fixture()
        data["triangle_side"] = "2"
        data["cells"] = [
            [["0", "0"], ["2", "0"], ["1", "1"]],
            [["0", "0"], ["1", "1"], ["0", "2"]],
        ]
        with self.assertRaisesRegex(CertificateError, "strictly below 4"):
            verify_certificate(data)

    def test_decimal_scalar_is_rejected(self) -> None:
        data = fixture()
        data["triangle_side"] = "1.999"
        with self.assertRaisesRegex(CertificateError, "decimals"):
            verify_certificate(data)

    def test_unexpected_field_is_rejected(self) -> None:
        data = fixture()
        data["optimal"] = True
        with self.assertRaisesRegex(CertificateError, "schema mismatch"):
            verify_certificate(data)

    def test_status_cannot_promote_itself(self) -> None:
        data = fixture()
        data["status"] = "verified:review"
        with self.assertRaisesRegex(CertificateError, "retain status"):
            verify_certificate(data)

    def test_boolean_n_is_rejected(self) -> None:
        data = fixture()
        data["n"] = True
        with self.assertRaisesRegex(CertificateError, "integer"):
            verify_certificate(data)


if __name__ == "__main__":
    unittest.main()
