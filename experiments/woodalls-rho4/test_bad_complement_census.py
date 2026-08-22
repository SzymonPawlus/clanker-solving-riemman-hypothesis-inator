import unittest

from acz import d27
from bad_complement_census import census, failed_sbo_pair, id1009_graph, maximum_disjoint_subfamily


class BadComplementCensusTests(unittest.TestCase):
    def test_matching_number(self) -> None:
        family = frozenset(
            {
                frozenset({0, 1, 2, 3}),
                frozenset({4, 5, 6, 7}),
                frozenset({0, 4, 8, 9}),
            }
        )
        matching = maximum_disjoint_subfamily(family)
        self.assertEqual(len(matching), 2)
        self.assertFalse(matching[0] & matching[1])

    def test_d27_non_sbo_control(self) -> None:
        result = census(d27())
        self.assertEqual(result["bad_complement_count"], 1)
        self.assertEqual(result["bad_matching_number"], 1)

    def test_id1009_control(self) -> None:
        from pathlib import Path

        directory = Path(__file__).resolve().parent
        result = census(id1009_graph(directory))
        self.assertEqual(result["base_count"], 271)
        self.assertEqual(result["eligible_complement_count"], 222)
        self.assertEqual(result["bad_complement_count"], 3)
        self.assertEqual(result["bad_matching_number"], 1)
        self.assertEqual(
            result["bad_family"],
            [[0, 9, 10, 11], [1, 9, 10, 11], [8, 9, 10, 11]],
        )

    def test_sbo_check_is_two_sided(self) -> None:
        # This rank-2 family has a valid strong ordering for every pair; the
        # explicit call exercises both exchanged bases for every subset.
        bases = frozenset(map(frozenset, ({0, 1}, {0, 2}, {1, 2})))
        self.assertIsNone(failed_sbo_pair(bases, frozenset({0, 1, 2})))


if __name__ == "__main__":
    unittest.main()
