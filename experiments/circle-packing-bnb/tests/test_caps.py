"""The cited d(k) enclosures must match the problem README, and cap() must be one-sided."""

from __future__ import annotations

import math
from fractions import Fraction

from cpbnb.caps import D_ENCLOSURE, MAX_CITED, capacity

SQRT3 = math.sqrt(3)

# d(k) = s(k) - 2*sqrt(3), with s(k) from
# problems/circle-packing-equilateral-triangle/README.md.  Written out as d directly:
# subtracting 2*sqrt(3) in binary64 would introduce its own rounding and make the test
# about float cancellation rather than about the enclosures.
EXPECTED = {
    2: 2.0,
    3: 2.0,
    4: 2 * SQRT3,
    5: 4.0,
    6: 4.0,
    7: 2 + 2 * SQRT3,
    8: 2 + 2 * math.sqrt(33) / 3,
    9: 6.0,
    10: 6.0,
    11: 4 + 4 * math.sqrt(6) / 3,
    12: 4 + 2 * SQRT3,
    13: 4 + 2 * math.sqrt(6) / 3 + 4 * SQRT3 / 3,
    14: 8.0,
    15: 8.0,
}


def test_enclosures_bracket_the_readme_values():
    assert set(D_ENCLOSURE) == set(EXPECTED)
    for k, v in EXPECTED.items():
        iv = D_ENCLOSURE[k]
        assert iv.lo <= v <= iv.hi, k
        assert iv.width() < 1e-13, k


def test_d_is_non_decreasing():
    ks = sorted(D_ENCLOSURE)
    for a, b in zip(ks, ks[1:]):
        assert D_ENCLOSURE[a].lo <= D_ENCLOSURE[b].hi


def test_capacity_is_a_correct_upper_bound():
    # cap(side) = k-1 requires side < d(k); check that against the float values.
    for num in range(1, 200):
        side = Fraction(num, 20)
        c = capacity(side, MAX_CITED)
        if c is None:
            assert float(side) >= EXPECTED[MAX_CITED] - 1e-9
        else:
            assert float(side) < EXPECTED[c + 1] + 1e-9
            # ... and the bound must not be tighter than the truth allows:
            if c >= 2:
                assert float(side) >= EXPECTED[c] - 1e-9


def test_max_cited_limits_the_literature_used():
    side = Fraction(7)
    assert capacity(side, 2) is None            # only d(2)=2 available, 7 > 2
    assert capacity(Fraction(19, 10), 2) == 1   # side < 2 -> at most one point
    assert capacity(side, 15) == 10             # 7 < d(11) = 7.2659... -> at most 10


def test_capacity_never_bounds_below_one():
    assert capacity(Fraction(1, 100), 15) == 1
