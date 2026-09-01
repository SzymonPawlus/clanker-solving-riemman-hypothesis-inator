import unittest
from collections import Counter

import probe_portfolio as probe


class PortfolioTests(unittest.TestCase):
    def test_coarse_portfolio_tree_replays(self):
        stats = Counter()
        tree = probe.build(dict(probe.ROOTS), 0, 5, stats)
        probe.verify(tree, dict(probe.ROOTS))
        leaves = stats["unresolved"] + sum(
            value for key, value in stats.items() if key.startswith("pruned_"))
        splits = sum(value for key, value in stats.items() if key.startswith("split_"))
        self.assertEqual(leaves, splits+1)

    def test_unproved_predicate_selection_is_rejected(self):
        stats = Counter()
        tree = probe.build(dict(probe.ROOTS), 0, 6, stats)

        def find_prune(node):
            if node["kind"] == "prune":
                return node
            if node["kind"] == "split":
                return find_prune(node["children"][0]) or find_prune(node["children"][1])
            return None

        leaf = find_prune(tree)
        self.assertIsNotNone(leaf)
        leaf["predicate"] = "midpoint_hull"
        with self.assertRaises((AssertionError, KeyError)):
            probe.verify(tree, dict(probe.ROOTS))


if __name__ == "__main__":
    unittest.main()
