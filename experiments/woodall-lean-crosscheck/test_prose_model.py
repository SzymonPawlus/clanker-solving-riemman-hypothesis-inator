"""Fixture tests for the prose model.  Must pass before the sweep means anything."""
import unittest

from prose_model import (FIXTURES, dicuts, dijoins, easy_direction_holds,
                         has_tau_disjoint_dijoins, is_dijoin, max_disjoint_dijoins, tau)

F = lambda k=(): frozenset(k)


class ProseFixtures(unittest.TestCase):
    def test_path(self):
        D = FIXTURES["path3"]
        self.assertEqual(dicuts(D), {F({0}), F({1})})
        self.assertEqual(tau(D), 1)
        self.assertTrue(is_dijoin(D, F({0, 1})))
        self.assertFalse(is_dijoin(D, F({0})))
        self.assertEqual(max_disjoint_dijoins(D), 1)
        self.assertTrue(has_tau_disjoint_dijoins(D))

    def test_cycle_has_no_dicut(self):
        D = FIXTURES["cycle3"]
        self.assertEqual(dicuts(D), set())
        self.assertEqual(dicuts(D, allow_empty=True), set())
        self.assertIsNone(tau(D))
        self.assertTrue(is_dijoin(D, F()))  # vacuously everything is a dijoin
        self.assertEqual(len(dijoins(D)), 8)

    def test_diamond(self):
        D = FIXTURES["diamond"]
        self.assertEqual(tau(D), 2)
        # dicuts: {s}->{0,1}, {t}^c -> {2,3}, {s,x}: arcs 1 (s->y), 2 (x->t); {s,y}: 0,3
        self.assertEqual(dicuts(D), {F({0, 1}), F({2, 3}), F({1, 2}), F({0, 3})})
        self.assertTrue(is_dijoin(D, F({0, 2})))  # path s->x->t
        self.assertTrue(is_dijoin(D, F({1, 3})))  # path s->y->t
        self.assertFalse(is_dijoin(D, F({0, 1})))
        self.assertEqual(max_disjoint_dijoins(D), 2)
        self.assertTrue(has_tau_disjoint_dijoins(D))

    def test_near_miss(self):
        D = FIXTURES["near_miss"]
        # arcs: 0 = s1->t1, 1 = s2->t1, 2 = s2->t2
        self.assertEqual(tau(D), 1)  # U={s1}: delta+ = {0}, delta- = {}
        self.assertIn(F({0}), dicuts(D))
        self.assertTrue(has_tau_disjoint_dijoins(D))
        self.assertTrue(easy_direction_holds(D))

    def test_parallel_arcs_survive(self):
        D = FIXTURES["parallel_pair"]
        self.assertEqual(tau(D), 2)
        self.assertEqual(max_disjoint_dijoins(D), 2)

    def test_empty_dicut_reading(self):
        D = FIXTURES["two_components"]
        # U = {0,1} has delta+ = delta- = {} : an empty dicut under the literal reading only.
        self.assertIn(F(), dicuts(D, allow_empty=True))
        self.assertNotIn(F(), dicuts(D, allow_empty=False))
        self.assertEqual(tau(D, allow_empty=True), 0)
        self.assertEqual(tau(D, allow_empty=False), 1)
        self.assertEqual(max_disjoint_dijoins(D, allow_empty=True), 0)
        self.assertEqual(max_disjoint_dijoins(D, allow_empty=False), 1)

    def test_easy_direction_everywhere_small(self):
        from prose_model import all_digraphs
        for D in all_digraphs(max_n=3, max_arcs=4, max_mult=2):
            self.assertTrue(easy_direction_holds(D), D)
            self.assertTrue(easy_direction_holds(D, allow_empty=True), D)


if __name__ == "__main__":
    unittest.main()
