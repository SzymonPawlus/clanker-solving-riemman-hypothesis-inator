import copy
import json
import tempfile
import unittest
from pathlib import Path

import check_support_complement as checker


HERE = Path(__file__).resolve().parent
GOOD = json.loads((HERE / "support_complement.json").read_text())


class SupportComplementTests(unittest.TestCase):
    def check_doc(self, document):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "complement.json"
            path.write_text(json.dumps(document))
            return checker.check(path)

    def test_exact_complementary_intervals_pass(self):
        report = self.check_doc(GOOD)
        self.assertEqual(report["worm_cells"], 261)
        self.assertEqual(report["covered_fraction"], checker.Q(29, 40))

    def test_interval_gap_is_rejected(self):
        document = copy.deepcopy(GOOD)
        document["worm_intervals"][0][1] = "79"
        with self.assertRaisesRegex(checker.Reject, "wrong complementary"):
            self.check_doc(document)

    def test_global_scope_is_rejected(self):
        document = copy.deepcopy(GOOD)
        document["claim_scope"] = "global"
        with self.assertRaisesRegex(checker.Reject, "schema or scope"):
            self.check_doc(document)


if __name__ == "__main__":
    unittest.main()
