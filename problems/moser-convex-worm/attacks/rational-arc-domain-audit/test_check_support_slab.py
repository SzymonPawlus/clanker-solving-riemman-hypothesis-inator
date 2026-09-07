import copy
import json
import tempfile
import unittest
from pathlib import Path

import check_support_slab as checker


HERE = Path(__file__).resolve().parent
GOOD = json.loads((HERE / "support_slab.json").read_text())


class SupportSlabTests(unittest.TestCase):
    def check_doc(self, document):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "slab.json"
            path.write_text(json.dumps(document))
            return checker.check(path)

    def test_full_two_angle_slab_has_exact_coverage(self):
        report = self.check_doc(GOOD)
        self.assertEqual(report["worm_cells"], 119)
        self.assertEqual(report["certified_lower"], checker.Q(2323, 10000))
        self.assertEqual(report["covered_fraction"], checker.Q(119, 360))
        self.assertEqual(report["uncovered_fraction"], checker.Q(241, 360))

    def test_omitted_triangle_domain_must_be_complete(self):
        document = copy.deepcopy(GOOD)
        document["triangle_domain"] = ["0", "60"]
        with self.assertRaisesRegex(checker.Reject, "omitted-angle"):
            self.check_doc(document)

    def test_inflated_recorded_lower_is_rejected(self):
        document = copy.deepcopy(GOOD)
        document["recorded_lower"] = "233/1000"
        with self.assertRaisesRegex(checker.Reject, "recorded lower"):
            self.check_doc(document)

    def test_global_scope_is_rejected(self):
        document = copy.deepcopy(GOOD)
        document["claim_scope"] = "global"
        with self.assertRaisesRegex(checker.Reject, "schema or scope"):
            self.check_doc(document)


if __name__ == "__main__":
    unittest.main()
