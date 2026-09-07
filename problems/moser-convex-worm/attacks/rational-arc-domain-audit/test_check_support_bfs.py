import copy
import json
import tempfile
import unittest
from pathlib import Path

import check_support_bfs as checker


HERE = Path(__file__).resolve().parent
GOOD = json.loads((HERE / "support_bfs.json").read_text())


class SupportBfsTests(unittest.TestCase):
    def check_doc(self, document):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "certificate.json"
            path.write_text(json.dumps(document))
            return checker.check(path)

    def test_all_exact_basic_feasible_allocations_reconstruct(self):
        report = self.check_doc(GOOD)
        self.assertEqual({name: item["bfs_count"] for name, item in report.items()},
                         {"segment": 4, "triangle": 4, "square": 16, "worm": 16})

    def test_changed_basis_is_rejected(self):
        document = copy.deepcopy(GOOD)
        document["templates"]["worm"]["bases"][4][-1] = 14
        with self.assertRaisesRegex(checker.Reject, "worm exact BFS mismatch"):
            self.check_doc(document)

    def test_missing_segment_lemma_is_rejected(self):
        document = copy.deepcopy(GOOD)
        document["segment_template_lemma"] = "mixed_area_asserted_without_degenerate_proof"
        with self.assertRaisesRegex(checker.Reject, "segment-template"):
            self.check_doc(document)

    def test_half_turn_must_be_checked_or_domain_restored_to_360(self):
        document = copy.deepcopy(GOOD)
        document["half_turn_action"]["reflection_used"] = True
        with self.assertRaisesRegex(checker.Reject, "restore worm domain to 360"):
            self.check_doc(document)

    def test_shorter_worm_domain_is_rejected(self):
        document = copy.deepcopy(GOOD)
        document["worm_angle_domain_degrees"] = ["0", "90"]
        with self.assertRaisesRegex(checker.Reject, "full 180-degree quotient"):
            self.check_doc(document)

    def test_global_scope_is_rejected(self):
        document = copy.deepcopy(GOOD)
        document["claim_scope"] = "global"
        with self.assertRaisesRegex(checker.Reject, "scope"):
            self.check_doc(document)


if __name__ == "__main__":
    unittest.main()
