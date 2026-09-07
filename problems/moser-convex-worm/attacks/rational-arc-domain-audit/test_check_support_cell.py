import copy
import json
import tempfile
import unittest
from pathlib import Path

import check_support_cell as checker


HERE = Path(__file__).resolve().parent
GOOD = json.loads((HERE / "support_cell.json").read_text())


class SupportCellTests(unittest.TestCase):
    def check_doc(self, document):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "cell.json"
            path.write_text(json.dumps(document))
            return checker.check(path)

    def test_rigorous_periodic_cell_clears_recorded_rational(self):
        self.assertEqual(self.check_doc(GOOD)["certified_lower"], checker.Q(237, 1000))

    def test_untrusted_basis_is_rejected(self):
        document = copy.deepcopy(GOOD)
        document["basis"][-1] = 14
        with self.assertRaisesRegex(checker.Reject, "untrusted primal"):
            self.check_doc(document)

    def test_missing_periodic_wrap_piece_is_rejected(self):
        document = copy.deepcopy(GOOD)
        document["periodic_triangle_cell"] = [["0", "1/4"]]
        with self.assertRaisesRegex(checker.Reject, "periodically"):
            self.check_doc(document)

    def test_global_scope_is_rejected(self):
        document = copy.deepcopy(GOOD)
        document["claim_scope"] = "global"
        with self.assertRaisesRegex(checker.Reject, "scope"):
            self.check_doc(document)


if __name__ == "__main__":
    unittest.main()
