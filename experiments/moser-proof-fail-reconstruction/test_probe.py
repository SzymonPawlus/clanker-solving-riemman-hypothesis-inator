#!/usr/bin/env python3
"""Small independent sanity checks for the clean-room geometry probe."""

import math
import unittest

import numpy as np

import probe_six_dimensional as probe


class GeometryTests(unittest.TestCase):
    def test_polygon_area(self) -> None:
        self.assertEqual(probe.area([(0, 0), (1, 0), (1, 1), (0, 1)]), 1.0)

    def test_hull_discards_interior_points(self) -> None:
        points = [(0, 0), (1, 0), (1, 1), (0, 1), (0.5, 0.5)]
        self.assertEqual(set(probe.hull(points)), set(points[:4]))

    def test_witness_areas(self) -> None:
        self.assertAlmostEqual(probe.area(probe.hull(probe.TRIANGLE)),
                               math.sqrt(3.0) / 16.0)
        self.assertAlmostEqual(probe.area(probe.hull(probe.RECTANGLE)), 1.0 / 8.0)

    def test_transform_preserves_area(self) -> None:
        moved = probe.transform(probe.RECTANGLE, 0.3, -0.7, 1.234)
        self.assertAlmostEqual(probe.area(probe.hull(moved)), 1.0 / 8.0)

    def test_breadth_term_at_right_angle(self) -> None:
        x = np.array([0.5, 0.0, 0.0, 0.5, 0.0, math.pi / 2.0])
        _, _, breadth_bound = probe.objective(x, 0.4389)
        self.assertAlmostEqual(breadth_bound, 0.4389 / 4.0)


if __name__ == "__main__":
    unittest.main()
