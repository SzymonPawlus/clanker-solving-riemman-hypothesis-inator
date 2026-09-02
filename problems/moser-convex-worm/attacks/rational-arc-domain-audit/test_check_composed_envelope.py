import copy
import json
import tempfile
import unittest
from pathlib import Path

import check_composed_envelope as checker


HERE = Path(__file__).resolve().parent
GOOD = json.loads((HERE / "composed_envelope.json").read_text())


class ComposedEnvelopeTests(unittest.TestCase):
    def check_doc(self, document):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "certificate.json"
            path.write_text(json.dumps(document))
            return checker.check(path)

    def test_partial_common_cell_schema_passes_and_reports_uncovered_volume(self):
        report = self.check_doc(GOOD)
        self.assertEqual(report["covered"], checker.Q(1, 100))
        self.assertEqual(report["covered_fraction"], checker.Q(2500000, 103555883601))
        self.assertGreater(report["uncovered"], 0)

    def test_mismatched_outer_partitions_are_rejected(self):
        document = copy.deepcopy(GOOD)
        document["outer_cells"][0]["worm_tree"]["outer_cell"]["square_tx"][0] = "7/10"
        with self.assertRaisesRegex(checker.Reject, "mismatched outer partitions"):
            self.check_doc(document)

    def test_combining_only_global_minima_is_rejected(self):
        document = copy.deepcopy(GOOD)
        document["combination_rule"] = "max_of_two_global_minima"
        with self.assertRaisesRegex(checker.Reject, "global minima"):
            self.check_doc(document)

    def test_missing_inner_pose_cell_is_rejected(self):
        document = copy.deepcopy(GOOD)
        document["outer_cells"][0]["triangle_tree"]["leaves"][0]["box"]["tx"][1] = "0"
        with self.assertRaisesRegex(checker.Reject, "missing inner pose cells"):
            self.check_doc(document)

    def test_nonuniform_inner_bound_is_rejected(self):
        document = copy.deepcopy(GOOD)
        document["outer_cells"][0]["worm_tree"]["leaves"][0]["uniform_over_outer_cell"] = False
        with self.assertRaisesRegex(checker.Reject, "nonuniform bound"):
            self.check_doc(document)

    def test_positive_bound_cannot_be_smuggled_through_nonnegativity(self):
        document = copy.deepcopy(GOOD)
        document["outer_cells"][0]["worm_tree"]["leaves"][0]["lower_bound"] = "1/10"
        with self.assertRaisesRegex(checker.Reject, "proves only"):
            self.check_doc(document)

    def test_wrong_compact_root_is_rejected(self):
        document = copy.deepcopy(GOOD)
        document["outer_root"]["square_theta_deg"][1] = "180"
        with self.assertRaisesRegex(checker.Reject, "outer root"):
            self.check_doc(document)

    def test_global_scope_is_rejected(self):
        document = copy.deepcopy(GOOD)
        document["claim_scope"] = "global"
        with self.assertRaisesRegex(checker.Reject, "scope"):
            self.check_doc(document)


if __name__ == "__main__":
    unittest.main()
