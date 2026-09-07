import copy
import json
import tempfile
import unittest
from pathlib import Path

import check_fan_leaf


HERE = Path(__file__).resolve().parent
GOOD = json.loads((HERE / "fan_leaf.json").read_text(encoding="utf-8"))


class FanLeafTests(unittest.TestCase):
    def check_doc(self, doc):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "leaf.json"
            path.write_text(json.dumps(doc), encoding="utf-8")
            check_fan_leaf.check(path)

    def test_nontrivial_translation_box_passes(self):
        self.check_doc(GOOD)

    def test_sign_uncertain_fan_rejected(self):
        doc = copy.deepcopy(GOOD)
        doc["arc_pose"]["ty"] = ["-1", "1/100"]
        with self.assertRaisesRegex(check_fan_leaf.Reject, "orientation"):
            self.check_doc(doc)

    def test_positive_but_insufficient_area_rejected(self):
        doc = copy.deepcopy(GOOD)
        doc["arc_pose"]["ty"] = ["-49/100", "-12/25"]
        with self.assertRaisesRegex(check_fan_leaf.Reject, "does not clear"):
            self.check_doc(doc)

    def test_midpoint_hull_hint_and_global_scope_rejected(self):
        doc = copy.deepcopy(GOOD)
        doc["midpoint_hull_order"] = [0, 1, 2]
        with self.assertRaisesRegex(check_fan_leaf.Reject, "unknown or missing"):
            self.check_doc(doc)
        doc = copy.deepcopy(GOOD)
        doc["claim_scope"] = "global"
        with self.assertRaisesRegex(check_fan_leaf.Reject, "must not claim"):
            self.check_doc(doc)


if __name__ == "__main__":
    unittest.main()
