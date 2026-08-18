from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from verify_witness import verify


ROOT = Path(__file__).parent


def fixture() -> dict[str, object]:
    return json.loads((ROOT / "witness.json").read_text(encoding="utf-8"))


class WitnessTests(unittest.TestCase):
    def test_committed_witness_is_accepted(self) -> None:
        report = verify(fixture())
        self.assertEqual(report["tau"], 3)
        self.assertEqual(report["minimum_dicut_shores"], 1)
        self.assertEqual(report["missing_forward_arcs"], 22)
        self.assertEqual(
            {row["tau_after"] for row in report["saturation_certificate"]}, {4, 5}
        )

    def test_removing_an_arc_breaks_the_claim(self) -> None:
        data = fixture()
        data["arcs"] = copy.deepcopy(data["arcs"][:-1])
        with self.assertRaises(ValueError):
            verify(data)

    def test_false_source_sink_pair_is_rejected(self) -> None:
        data = fixture()
        data["unreachable_source_sink_pair"] = [1, 9]
        with self.assertRaises(ValueError):
            verify(data)


if __name__ == "__main__":
    unittest.main()
