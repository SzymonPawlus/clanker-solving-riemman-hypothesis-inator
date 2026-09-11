import itertools
import random
import unittest
from fractions import Fraction

from lonely_runner_exact import allowed_times, feasible_times, witness_time


def distance_to_integer(x: Fraction) -> Fraction:
    fractional = x - (x.numerator // x.denominator)
    return min(fractional, 1 - fractional)


class ExactLonelyRunnerTests(unittest.TestCase):
    def assert_witness_valid(self, velocities, witness):
        self.assertIsNotNone(witness)
        self.assertGreaterEqual(witness, 0)
        self.assertLess(witness, 1)
        bound = Fraction(1, len(velocities) + 1)
        for velocity in velocities:
            self.assertGreaterEqual(distance_to_integer(witness * velocity), bound)

    def test_one_runner_has_exact_half_time(self):
        self.assertEqual(feasible_times([1]), [(Fraction(1, 2), Fraction(1, 2))])

    def test_hand_derived_two_runner_intersection_is_two_points(self):
        # speed 1 allows [1/3, 2/3]; speed 2 meets it only at its endpoints.
        self.assertEqual(
            feasible_times([1, 2]),
            [(Fraction(1, 3), Fraction(1, 3)), (Fraction(2, 3), Fraction(2, 3))],
        )

    def test_closed_endpoint_touching_is_not_discarded(self):
        self.assertEqual(witness_time([1, 2, 3]), Fraction(1, 4))
        self.assert_witness_valid([1, 2, 3], Fraction(1, 4))
        # An explicit intersection that would be empty for open endpoints.
        first = allowed_times(1, Fraction(1, 3))
        second = allowed_times(2, Fraction(1, 3))
        self.assertIn((Fraction(1, 3), Fraction(1, 3)), feasible_times([1, 2]))
        self.assertEqual(first, [(Fraction(1, 3), Fraction(2, 3))])
        self.assertEqual(second[0][1], first[0][0])

    def test_zero_velocity_is_correctly_infeasible(self):
        self.assertEqual(feasible_times([0]), [])
        self.assertEqual(feasible_times([1, 0, 7]), [])
        self.assertIsNone(witness_time([0, 2]))

    def test_sign_and_permutation_invariance(self):
        velocities = [1, 3, 7, 8]
        expected = feasible_times(velocities)
        for signs in itertools.product((-1, 1), repeat=len(velocities)):
            signed = [s * v for s, v in zip(signs, velocities)]
            self.assertEqual(feasible_times(signed), expected)
        for permutation in itertools.permutations(velocities):
            self.assertEqual(feasible_times(permutation), expected)

    def test_gcd_scaling_preserves_feasibility_and_maps_witness(self):
        examples = ([1], [1, 2], [1, 3, 7], [-2, 5, 11, 13])
        for velocities in examples:
            base_witness = witness_time(velocities)
            self.assert_witness_valid(velocities, base_witness)
            for factor in (2, 3, 11):
                scaled = [factor * velocity for velocity in velocities]
                self.assertEqual(bool(feasible_times(scaled)), bool(feasible_times(velocities)))
                # t/factor has exactly the same phases as t in the base vector.
                self.assert_witness_valid(scaled, base_witness / factor)

    def test_every_returned_endpoint_is_an_actual_witness(self):
        velocities = [2, -5, 9, 14]
        intervals = feasible_times(velocities)
        self.assertTrue(intervals)
        for interval in intervals:
            for endpoint in interval:
                self.assert_witness_valid(velocities, endpoint)

    def test_random_instances_against_independent_cell_sampling(self):
        # Between consecutive rational boundary points every predicate is
        # constant. Check all cells and boundary points without using the
        # production intersection routine.
        rng = random.Random(299)
        for k in range(1, 6):
            bound = Fraction(1, k + 1)
            for _ in range(60):
                velocities = [rng.randint(-10, 10) for _ in range(k)]
                exact = feasible_times(velocities)
                boundaries = {Fraction(0), Fraction(1)}
                # Generate phase-change points from the definition here,
                # independently of allowed_times().
                for v in velocities:
                    speed = abs(v)
                    if speed:
                        for j in range(speed):
                            boundaries.add((j + bound) / speed)
                            boundaries.add((j + 1 - bound) / speed)
                ordered = sorted(boundaries)
                probes = set(ordered[:-1])
                probes.update((a + b) / 2 for a, b in zip(ordered, ordered[1:]))
                brute = any(
                    all(distance_to_integer(t * v) >= bound for v in velocities)
                    for t in probes if t < 1
                )
                self.assertEqual(bool(exact), brute, velocities)

    def test_input_validation(self):
        with self.assertRaises(ValueError):
            feasible_times([])
        with self.assertRaises(TypeError):
            feasible_times([1, Fraction(2, 1)])
        with self.assertRaises(ValueError):
            allowed_times(1, Fraction(0))


if __name__ == "__main__":
    unittest.main()
