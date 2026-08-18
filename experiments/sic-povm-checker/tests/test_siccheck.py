from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from siccheck import CertificateError, K, load, parse_rational, verify  # noqa: E402


def scalar(*values):
    values = list(values) + [0] * (8 - len(values))
    return [str(Fraction(value)) for value in values]


ZERO = scalar(0)
ONE = scalar(1)
S2_OVER_2 = scalar(0, Fraction(1, 2))
S3_OVER_3 = scalar(0, 0, Fraction(1, 3))
S6_OVER_3 = scalar(0, 0, 0, Fraction(1, 3))
OMEGA = scalar(Fraction(-1, 2), 0, 0, 0, 0, 0, Fraction(1, 2))
OMEGA2 = scalar(Fraction(-1, 2), 0, 0, 0, 0, 0, Fraction(-1, 2))


def base(d, vectors, weights=None):
    data = {"certificate_version": 1, "claim": "sic-family", "status": "numerical",
            "dimension": d, "field": "Q(sqrt2,sqrt3,i)-basis-v1", "vectors": vectors}
    if weights is not None:
        data["povm_weights"] = weights
    return data


def d2_certificate():
    # Tetrahedral SIC: (1,0), then (1/sqrt3, sqrt(2/3)*omega^k), k=0,1,2.
    vectors = [[ONE, ZERO], [S3_OVER_3, S6_OVER_3]]
    for phase in (OMEGA, OMEGA2):
        # Multiplication by omega is expanded directly in the fixed basis.
        sign = 1 if phase == OMEGA else -1
        vectors.append([S3_OVER_3, scalar(0, 0, 0, Fraction(-1, 6), 0, Fraction(sign, 2))])
    return base(2, vectors, [scalar(Fraction(1, 2))] * 4)


def d3_certificate():
    # Hesse SIC: all cyclic shifts of (0,1,-omega^k)/sqrt2, k=0,1,2.
    # Values of -omega^k/sqrt(2), expanded independently of checker arithmetic.
    phases = (
        scalar(0, Fraction(-1, 2)),
        scalar(0, Fraction(1, 4), 0, 0, 0, 0, 0, Fraction(-1, 4)),
        scalar(0, Fraction(1, 4), 0, 0, 0, 0, 0, Fraction(1, 4)),
    )
    vectors = []
    for phase in phases:
        for zero_index in range(3):
            vector = []
            for index in range(3):
                if index == zero_index:
                    vector.append(ZERO)
                elif index == (zero_index + 1) % 3:
                    vector.append(S2_OVER_2)
                else:
                    vector.append(phase)
            vectors.append(vector)
    return base(3, vectors, [scalar(Fraction(1, 3))] * 9)


class PositiveTests(unittest.TestCase):
    def test_fixed_basis_relations_and_conjugation(self):
        basis = [K(tuple(Fraction(index == j) for index in range(8))) for j in range(8)]
        self.assertEqual(basis[1] * basis[1], K.rational(2))
        self.assertEqual(basis[2] * basis[2], K.rational(3))
        self.assertEqual(basis[4] * basis[4], K.rational(-1))
        self.assertEqual(basis[1] * basis[2], basis[3])
        self.assertEqual(basis[4].conjugate(), -basis[4])

    def test_dimension_one(self):
        report = verify(base(1, [[ONE]], [ONE]))
        self.assertEqual(report["checked_pairs"], 0)
        self.assertTrue(report["povm_completeness_checked"])

    def test_tetrahedral_dimension_two(self):
        report = verify(d2_certificate())
        self.assertEqual(report["checked_pairs"], 6)
        self.assertTrue(report["povm_completeness_checked"])

    def test_povm_completeness_is_optional(self):
        certificate = d2_certificate()
        del certificate["povm_weights"]
        self.assertFalse(verify(certificate)["povm_completeness_checked"])

    def test_hesse_dimension_three(self):
        report = verify(d3_certificate())
        self.assertEqual(report["checked_pairs"], 36)
        self.assertTrue(report["povm_completeness_checked"])


class NegativeTests(unittest.TestCase):
    def setUp(self):
        self.good = d2_certificate()

    def rejects(self, mutate):
        bad = copy.deepcopy(self.good)
        mutate(bad)
        with self.assertRaises(CertificateError):
            verify(bad)

    def test_wrong_vector_count(self): self.rejects(lambda x: x["vectors"].pop())
    def test_wrong_vector_dimension(self): self.rejects(lambda x: x["vectors"][0].pop())
    def test_zero_vector(self): self.rejects(lambda x: x["vectors"].__setitem__(0, [ZERO, ZERO]))
    def test_perturbed_overlap(self): self.rejects(lambda x: x["vectors"][1].__setitem__(0, scalar(Fraction(1, 2))))
    def test_wrong_dimension(self): self.rejects(lambda x: x.__setitem__("dimension", 4))
    def test_bool_dimension(self): self.rejects(lambda x: x.__setitem__("dimension", True))
    def test_decimal_injection(self): self.rejects(lambda x: x["vectors"][0][0].__setitem__(0, "1.0"))
    def test_unknown_field(self): self.rejects(lambda x: x.__setitem__("surprise", 1))
    def test_wrong_status(self): self.rejects(lambda x: x.__setitem__("status", "verified:review"))
    def test_wrong_weights(self): self.rejects(lambda x: x["povm_weights"].__setitem__(0, scalar(1)))
    def test_negative_povm_weight(self): self.rejects(lambda x: x["povm_weights"].__setitem__(0, scalar(-1)))
    def test_nonrational_povm_weight(self): self.rejects(lambda x: x["povm_weights"].__setitem__(0, S2_OVER_2))
    def test_wrong_claim(self): self.rejects(lambda x: x.__setitem__("claim", "construction"))
    def test_wrong_field(self): self.rejects(lambda x: x.__setitem__("field", "expressions"))
    def test_oversized_integer(self): self.rejects(lambda x: x["vectors"][0][0].__setitem__(0, str(1 << 1025)))
    def test_malformed_rational(self): self.rejects(lambda x: x["vectors"][0][0].__setitem__(0, "01"))

    def test_duplicate_json_key(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            path.write_text('{"dimension":2,"dimension":3}')
            with self.assertRaises(CertificateError):
                load(path)

    def test_file_size_bound(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "large.json"
            path.write_text(" " * 1_000_001)
            with self.assertRaises(CertificateError):
                load(path)

    def test_rational_grammar_boundaries(self):
        for accepted in ("0", "-1", "2/3"):
            parse_rational(accepted, "test")
        for rejected in ("", "+1", "-0", "01", "1.0", "1e2", "1/0", "1/-2", " 1", "1 "):
            with self.subTest(rejected=rejected), self.assertRaises(CertificateError):
                parse_rational(rejected, "test")


if __name__ == "__main__":
    unittest.main()
