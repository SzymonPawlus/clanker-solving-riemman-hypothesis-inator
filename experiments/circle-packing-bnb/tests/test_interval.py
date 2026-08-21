"""The interval layer must never return an interval that misses the true value."""

from __future__ import annotations

import math
import random
from fractions import Fraction

import pytest

from cpbnb.interval import Interval, isqrt_interval


def test_endpoints_are_widened_outward():
    a = Interval.from_int(1)
    b = Interval.from_int(3)
    s = a + b
    assert s.lo < 4.0 < s.hi  # widened even though 4 is exact


def test_containment_under_arithmetic():
    rng = random.Random(20260818)
    for _ in range(2000):
        x = rng.uniform(-50, 50)
        y = rng.uniform(-50, 50)
        ix = Interval(math.nextafter(x, -math.inf), math.nextafter(x, math.inf))
        iy = Interval(math.nextafter(y, -math.inf), math.nextafter(y, math.inf))
        fx, fy = Fraction(x), Fraction(y)
        for iv, exact in (
            (ix + iy, fx + fy),
            (ix - iy, fx - fy),
            (ix * iy, fx * fy),
        ):
            assert Fraction(iv.lo) <= exact <= Fraction(iv.hi)


def test_sqrt_encloses_the_true_root():
    for k in range(0, 200):
        iv = isqrt_interval(k)
        # lo^2 <= k <= hi^2, decided exactly in Fraction, so the enclosure is proved.
        # (For k = 0 the outward widening pushes lo one ulp below zero, which is still a
        # correct enclosure; squaring it would not be.)
        lo, hi = Fraction(iv.lo), Fraction(iv.hi)
        assert lo <= 0 or lo**2 <= k
        assert hi >= 0 and hi**2 >= k


def test_sqrt3_matches_the_known_decimal():
    iv = isqrt_interval(3)
    assert iv.lo < 1.7320508075688772935 < iv.hi


def test_division_by_zero_straddling_interval_is_refused():
    with pytest.raises(ZeroDivisionError):
        Interval(1.0, 2.0) / Interval(-1.0, 1.0)


def test_sqrt_of_negative_is_refused():
    with pytest.raises(ValueError):
        Interval(-1.0, 4.0).sqrt()


def test_empty_interval_is_refused():
    with pytest.raises(ValueError):
        Interval(1.0, 0.0)


def test_comparisons_are_one_sided():
    iv = Interval(1.9999, 2.0001)
    assert not iv.gt_fraction(Fraction(2))
    assert not iv.lt_fraction(Fraction(2))
    assert iv.gt_fraction(Fraction(19, 10))
    assert iv.lt_fraction(Fraction(21, 10))
