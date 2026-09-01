import copy
import json
import tempfile
import unittest
from pathlib import Path

import check_domain


HERE = Path(__file__).resolve().parent
BASELINE = json.loads((HERE / "domain.json").read_text(encoding="utf-8"))


class DomainTests(unittest.TestCase):
    def check_doc(self, doc):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "domain.json"
            path.write_text(doc if isinstance(doc, str) else json.dumps(doc), encoding="utf-8")
            check_domain.check(path)

    def test_baseline_passes(self):
        self.check_doc(BASELINE)

    def test_global_scope_rejected(self):
        doc = copy.deepcopy(BASELINE)
        doc["claim_scope"] = "global_area_lower_bound"
        with self.assertRaisesRegex(check_domain.Reject, "must not claim"):
            self.check_doc(doc)

    def test_inward_diameter_rounding_rejected(self):
        doc = copy.deepcopy(BASELINE)
        doc["diameter_upper"] = "53633/50000"
        with self.assertRaisesRegex(check_domain.Reject, "strictly outward"):
            self.check_doc(doc)

    def test_changed_arc_or_extra_closing_vertex_rejected(self):
        doc = copy.deepcopy(BASELINE)
        doc["arc_vertices"][2][0] = "11/25"
        with self.assertRaisesRegex(check_domain.Reject, "wrong rational arc"):
            self.check_doc(doc)
        doc = copy.deepcopy(BASELINE)
        doc["arc_vertices"].append(["0", "0"])
        with self.assertRaisesRegex(check_domain.Reject, "exactly four"):
            self.check_doc(doc)

    def test_reflection_quotient_rejected(self):
        doc = copy.deepcopy(BASELINE)
        doc["motion_convention"] = "rotations_and_reflection_quotient"
        with self.assertRaisesRegex(check_domain.Reject, "Reflection|reflection"):
            self.check_doc(doc)

    def test_missing_degree_of_freedom_rejected(self):
        doc = copy.deepcopy(BASELINE)
        del doc["pose_domain"]["rational_arc"]["ty"]
        with self.assertRaisesRegex(check_domain.Reject, "incomplete pose"):
            self.check_doc(doc)
        doc = copy.deepcopy(BASELINE)
        del doc["pose_domain"]["square"]
        with self.assertRaisesRegex(check_domain.Reject, "exactly three"):
            self.check_doc(doc)

    def test_shortened_angle_domain_rejected(self):
        doc = copy.deepcopy(BASELINE)
        doc["pose_domain"]["rational_arc"]["theta_degrees"] = ["0", "90"]
        with self.assertRaisesRegex(check_domain.Reject, "orientation gauge"):
            self.check_doc(doc)

    def test_translation_box_gap_rejected(self):
        doc = copy.deepcopy(BASELINE)
        doc["pose_domain"]["triangle"]["tx"][0] = "-1"
        with self.assertRaisesRegex(check_domain.Reject, "translation box"):
            self.check_doc(doc)

    def test_duplicate_and_unknown_fields_rejected(self):
        raw = (HERE / "domain.json").read_text(encoding="utf-8")
        raw = raw.replace('"schema_version":', '"schema_version": "shadow",\n  "schema_version":', 1)
        with self.assertRaisesRegex(check_domain.Reject, "duplicate JSON"):
            self.check_doc(raw)
        doc = copy.deepcopy(BASELINE)
        doc["trust_optimizer"] = True
        with self.assertRaisesRegex(check_domain.Reject, "unknown or missing"):
            self.check_doc(doc)


if __name__ == "__main__":
    unittest.main()
