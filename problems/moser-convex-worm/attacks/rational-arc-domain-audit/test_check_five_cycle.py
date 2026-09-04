import copy
import json
import tempfile
import unittest
from pathlib import Path

import check_five_cycle


HERE=Path(__file__).resolve().parent
GOOD=json.loads((HERE/"five_cycle_box.json").read_text())


class FiveCycleTests(unittest.TestCase):
    def check_doc(self,doc):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"box.json";p.write_text(json.dumps(doc))
            return check_five_cycle.check(p)

    def test_independent_lower_matches_reported_box(self):
        self.assertGreater(float(self.check_doc(GOOD)),0.2350064)

    def test_radius_1_over_1700_passes(self):
        d=copy.deepcopy(GOOD);d["box_radius"]="1/1700"
        self.assertGreater(float(self.check_doc(d)),0.2331180)

    def test_radius_1_over_1650_loses_convex_order(self):
        d=copy.deepcopy(GOOD);d["box_radius"]="1/1650"
        with self.assertRaisesRegex(check_five_cycle.Reject,"convex-order"):
            self.check_doc(d)

    def test_cycle_label_without_guards_is_rejected(self):
        d=copy.deepcopy(GOOD);d["selected_cycle"][1]="square.P1"
        with self.assertRaisesRegex(check_five_cycle.Reject,"untrusted cycle"):
            self.check_doc(d)

    def test_global_scope_is_rejected(self):
        d=copy.deepcopy(GOOD);d["claim_scope"]="global"
        with self.assertRaisesRegex(check_five_cycle.Reject,"scope"):
            self.check_doc(d)


if __name__=="__main__": unittest.main()
