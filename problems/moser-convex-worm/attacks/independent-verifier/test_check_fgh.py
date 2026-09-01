#!/usr/bin/env python3
"""Adversarial tests for the independent conditional f/g/h checker."""

import copy
import json
import tempfile
import unittest
from pathlib import Path

import check_fgh


HERE = Path(__file__).resolve().parent
BASELINE = json.loads((HERE / "baseline-fgh.json").read_text(encoding="utf-8"))


class CertificateTests(unittest.TestCase):
    def check_document(self, document):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "certificate.json"
            if isinstance(document, str):
                path.write_text(document, encoding="utf-8")
            else:
                path.write_text(json.dumps(document), encoding="utf-8")
            check_fgh.check(path)

    def mutation(self, *keys, value):
        document = copy.deepcopy(BASELINE)
        target = document
        for key in keys[:-1]:
            target = target[key]
        target[keys[-1]] = value
        return document

    def test_baseline_passes(self):
        self.check_document(BASELINE)

    def test_stage_one_certificate_cannot_claim_global_theorem(self):
        for scope in ("global", "all_placements", "moser_lower_bound", None):
            with self.subTest(scope=scope), self.assertRaisesRegex(
                    check_fgh.Reject, "must not claim a global"):
                self.check_document(self.mutation("claim_scope", value=scope))

    def test_pi_is_derived_to_more_than_sixty_decimal_places(self):
        self.assertGreater(check_fgh.PI.lo, 3)
        self.assertLess(check_fgh.PI.hi, 4)
        self.assertLess(check_fgh.PI.hi - check_fgh.PI.lo, check_fgh.Q(1, 10**60))

    def test_coarse_tails_clear_point_23(self):
        coarse = check_fgh.Q(23, 100)
        self.assertGreater((check_fgh.sqrt2()*check_fgh.sin_point(78)/6).lo, coarse)
        self.assertGreater((check_fgh.sin_point(83+30)/4).lo, coarse)
        self.assertGreater((check_fgh.sin_point(97-30)/4).lo, coarse)

    def test_printed_inward_alpha_cutoff_is_rejected(self):
        with self.assertRaises(check_fgh.Reject):
            self.check_document(self.mutation("cutoffs", "alpha", value="74.838"))

    def test_printed_inward_beta_cutoffs_are_rejected(self):
        with self.assertRaises(check_fgh.Reject):
            self.check_document(self.mutation("cutoffs", "beta_low", value="84.496"))
        with self.assertRaises(check_fgh.Reject):
            self.check_document(self.mutation("cutoffs", "beta_high", value="95.504"))

    def test_reversed_beta_partition_is_rejected_before_trigonometry(self):
        document = self.mutation("cutoffs", "beta_low", value="96")
        document["cutoffs"]["beta_high"] = "95"
        with self.assertRaisesRegex(check_fgh.Reject, "ordered partition"):
            self.check_document(document)

    def test_cutoff_outside_compact_root_is_rejected(self):
        with self.assertRaisesRegex(check_fgh.Reject, "outside root"):
            self.check_document(self.mutation("cutoffs", "alpha", value="79"))
        with self.assertRaisesRegex(check_fgh.Reject, "ordered partition"):
            self.check_document(self.mutation("cutoffs", "beta_low", value="82"))

    def test_non_string_and_noncanonical_rationals_are_rejected(self):
        for value in (74.83846, True, "07483846/1000000", "2/0", "NaN"):
            with self.subTest(value=value), self.assertRaises(check_fgh.Reject):
                self.check_document(self.mutation("cutoffs", "alpha", value=value))

    def test_duplicate_semantic_field_is_rejected(self):
        raw = (HERE / "baseline-fgh.json").read_text(encoding="utf-8")
        raw = raw.replace('"schema_version":', '"schema_version": "shadow",\n  "schema_version":', 1)
        with self.assertRaisesRegex(check_fgh.Reject, "duplicate JSON field"):
            self.check_document(raw)

    def test_unknown_nested_cutoff_field_is_rejected(self):
        document = copy.deepcopy(BASELINE)
        document["cutoffs"]["unproved_hint"] = "accept"
        with self.assertRaisesRegex(check_fgh.Reject, "wrong cutoff fields"):
            self.check_document(document)

    def test_nonfinite_json_number_is_rejected(self):
        raw = (HERE / "baseline-fgh.json").read_text(encoding="utf-8")
        raw = raw.replace('"alpha": "3741923/50000"', '"alpha": NaN')
        with self.assertRaisesRegex(check_fgh.Reject, "non-finite JSON number"):
            self.check_document(raw)


if __name__ == "__main__":
    unittest.main()
