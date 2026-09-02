import random
import unittest
from fractions import Fraction as Q

from mixed_area import (area2, bridge_check, convex_hull, qpoint,
                        strict_ccw_convex, twice_mixed_area)


class MixedAreaBridgeTests(unittest.TestCase):
    def setUp(self):
        self.square = [qpoint(0, 0), qpoint(4, 0), qpoint(4, 4), qpoint(0, 4)]

    def test_equality_for_same_polygon_and_factor_one_half(self):
        lhs, rhs, ok = bridge_check(self.square, self.square)
        self.assertTrue(ok)
        self.assertEqual(lhs, rhs)
        self.assertEqual(twice_mixed_area(self.square, self.square), 2 * rhs)
        self.assertGreater(twice_mixed_area(self.square, self.square), rhs)

    def test_segment_uses_both_boundary_sides(self):
        segment = [qpoint(0, 2), qpoint(4, 2)]
        lhs, rhs, ok = bridge_check(segment, self.square)
        self.assertEqual(lhs, Q(8))
        self.assertEqual(rhs, Q(16))
        self.assertTrue(ok)

    def test_translation_invariance_independently(self):
        tri = [qpoint(1, 1), qpoint(3, 1), qpoint(2, 3)]
        base = twice_mixed_area(tri, self.square)
        shift_k = [(x + Q(17, 3), y - Q(11, 7)) for x, y in self.square]
        shift_p = [(x - Q(5, 2), y + Q(13, 9)) for x, y in tri]
        self.assertEqual(base, twice_mixed_area(tri, shift_k))
        self.assertEqual(base, twice_mixed_area(shift_p, self.square))

    def test_rejects_noncontainment(self):
        outside = [qpoint(0, 0), qpoint(5, 0), qpoint(0, 1)]
        with self.assertRaisesRegex(ValueError, "not contained"):
            bridge_check(outside, self.square)

    def test_rejects_clockwise(self):
        with self.assertRaisesRegex(ValueError, "CCW"):
            bridge_check(list(reversed(self.square)), self.square)
        with self.assertRaisesRegex(ValueError, "inner"):
            bridge_check(list(reversed(self.square)), self.square)

    def test_rejects_duplicate_and_collinear_vertices(self):
        duplicate = self.square[:2] + [self.square[1]] + self.square[2:]
        collinear = [qpoint(0, 0), qpoint(2, 0), qpoint(4, 0),
                     qpoint(4, 4), qpoint(0, 4)]
        for bad in (duplicate, collinear):
            self.assertFalse(strict_ccw_convex(bad))
            with self.assertRaises(ValueError):
                bridge_check(bad, self.square)

    def test_wrong_inward_normals_are_detected_by_translation(self):
        tri = [qpoint(1, 1), qpoint(3, 1), qpoint(2, 3)]
        asymmetric = [qpoint(0, 0), qpoint(7, 0), qpoint(0, 5)]
        moved = [(x + 100, y + 100) for x, y in asymmetric]
        correct = twice_mixed_area(tri, moved)
        wrong = twice_mixed_area(tri, moved, inward=True)
        self.assertNotEqual(correct, wrong)
        # Both complete sums are translation invariant; asymmetry, not an
        # origin-dependent heuristic, exposes reversal of the normals.
        self.assertEqual(correct, twice_mixed_area(tri, asymmetric))

    def test_missing_edge_breaks_translation_invariance(self):
        tri = [qpoint(1, 1), qpoint(3, 1), qpoint(2, 3)]
        moved = [(x + 9, y - 7) for x, y in self.square]
        self.assertNotEqual(twice_mixed_area(tri, self.square, omit_last=True),
                            twice_mixed_area(tri, moved, omit_last=True))

    def test_random_exact_contained_hulls(self):
        rng = random.Random(174)
        checked = 0
        for _ in range(1000):
            outer = convex_hull([qpoint(rng.randrange(-20, 21),
                                       rng.randrange(-20, 21)) for _ in range(12)])
            if len(outer) < 3:
                continue
            # Homothety about the first vertex guarantees exact containment.
            anchor = outer[0]
            scale = Q(rng.randrange(1, 10), 10)
            inner = [(anchor[0] + scale * (x - anchor[0]),
                      anchor[1] + scale * (y - anchor[1])) for x, y in outer]
            lhs, rhs, ok = bridge_check(inner, outer)
            self.assertTrue(ok)
            self.assertLessEqual(lhs, rhs)
            checked += 1
        self.assertGreaterEqual(checked, 990)

    def test_random_exact_nonhomothetic_hulls_and_minkowski_identity(self):
        rng = random.Random(1174)
        checked = 0
        for _ in range(1000):
            outer = convex_hull([qpoint(rng.randrange(-12, 13),
                                       rng.randrange(-12, 13)) for _ in range(10)])
            if len(outer) < 3:
                continue
            samples = []
            for _ in range(10):
                a, b = rng.sample(outer, 2)
                lam = Q(rng.randrange(1, 10), 10)
                samples.append((lam * a[0] + (1 - lam) * b[0],
                                lam * a[1] + (1 - lam) * b[1]))
            inner = convex_hull(samples)
            if len(inner) < 3:
                continue
            lhs, rhs, ok = bridge_check(inner, outer)
            self.assertTrue(ok)
            self.assertLessEqual(lhs, rhs)

            # Independent shoelace check of (1) at an exact rational t.
            t = Q(rng.randrange(1, 8), rng.randrange(2, 9))
            minkowski = convex_hull([
                (x[0] + t * y[0], x[1] + t * y[1])
                for x in outer for y in inner
            ])
            actual = area2(minkowski) / 2
            predicted = (area2(outer) / 2
                         + t * twice_mixed_area(inner, outer)
                         + t * t * area2(inner) / 2)
            self.assertEqual(actual, predicted)
            checked += 1
        self.assertGreaterEqual(checked, 990)


if __name__ == "__main__":
    unittest.main()
