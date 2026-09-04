import copy
import json
import tempfile
import unittest
from pathlib import Path

import check_support_cells as checker


HERE = Path(__file__).resolve().parent
GOOD = json.loads((HERE / "support_cells.json").read_text())


class SupportCellsTests(unittest.TestCase):
    def check_doc(self, document):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "cells.json"
            path.write_text(json.dumps(document))
            return checker.check(path)

    def test_partial_staircase_has_exact_coverage(self):
        report = self.check_doc(GOOD)
        self.assertEqual(report["cells"], 24)
        self.assertEqual(report["covered_fraction"], checker.Q(1, 3600))
        self.assertEqual(report["uncovered_fraction"], checker.Q(3599, 3600))

    def test_overlapping_cell_is_rejected(self):
        document = copy.deepcopy(GOOD)
        document["cells"][1]["worm_center"] = "98"
        with self.assertRaisesRegex(checker.Reject, "overlapping"):
            self.check_doc(document)

    def test_inflated_lower_bound_is_rejected(self):
        document = copy.deepcopy(GOOD)
        document["cells"][0]["certified_lower"] = "6/25"
        with self.assertRaisesRegex(checker.Reject, "lower endpoint"):
            self.check_doc(document)

    def test_global_scope_is_rejected(self):
        document = copy.deepcopy(GOOD)
        document["claim_scope"] = "global"
        with self.assertRaisesRegex(checker.Reject, "schema or scope"):
            self.check_doc(document)


if __name__ == "__main__":
    unittest.main()
