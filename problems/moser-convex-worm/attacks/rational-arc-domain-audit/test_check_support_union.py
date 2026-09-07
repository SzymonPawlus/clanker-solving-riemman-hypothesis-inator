import copy
import json
import tempfile
import unittest
from pathlib import Path

import check_support_union as checker


HERE = Path(__file__).resolve().parent
GOOD = json.loads((HERE / "support_union.json").read_text())


class SupportUnionTests(unittest.TestCase):
    def check_doc(self, document):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "union.json"
            path.write_text(json.dumps(document))
            (Path(directory) / "support_complement.json").write_text(
                (HERE / "support_complement.json").read_text())
            (Path(directory) / "support_slab.json").write_text(
                (HERE / "support_slab.json").read_text())
            return checker.check(path)

    def test_full_angular_union_is_recorded_with_scope_withheld(self):
        report = self.check_doc(GOOD)
        self.assertEqual(report["certified_lower"], checker.Q(2323, 10000))
        self.assertEqual(report["worm_domain_covered"], (checker.Q(0), checker.Q(180)))
        self.assertFalse(report["global_claim"])

    def test_missing_interval_is_rejected(self):
        document = copy.deepcopy(GOOD)
        document["slabs"][0]["worm_intervals"].pop()
        with self.assertRaisesRegex(checker.Reject, "union schema"):
            self.check_doc(document)

    def test_global_claim_is_rejected(self):
        document = copy.deepcopy(GOOD)
        document["global_claim"] = True
        with self.assertRaisesRegex(checker.Reject, "withheld scope"):
            self.check_doc(document)


if __name__ == "__main__":
    unittest.main()
