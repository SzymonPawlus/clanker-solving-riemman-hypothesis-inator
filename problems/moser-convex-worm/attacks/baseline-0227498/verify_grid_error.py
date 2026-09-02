#!/usr/bin/env python3
"""Exact-rational countercheck of the non-load-bearing grid error estimate."""

from fractions import Fraction as Q
from math import comb, isqrt

from verify_trig import PI, trig_alt


def sqrt_interval(x, digits=80):
    """Decimal rational enclosure of sqrt(x), verified by integer squaring."""
    scale10 = 10**digits
    floor_scaled = isqrt(x.numerator * x.denominator * scale10**2) // x.denominator
    while Q(floor_scaled + 1, scale10) ** 2 <= x:
        floor_scaled += 1
    while Q(floor_scaled, scale10) ** 2 > x:
        floor_scaled -= 1
    out = Q(floor_scaled, scale10), Q(floor_scaled + 1, scale10)
    assert out[0] ** 2 <= x < out[1] ** 2
    return out


def asin_interval(x, terms=100):
    """Enclose asin(x) for 0 <= x < 1 by its positive power series."""
    assert Q(0) <= x < Q(1)
    partial = Q(0)
    for k in range(terms + 1):
        partial += Q(comb(2 * k, k), 4**k * (2 * k + 1)) * x ** (2 * k + 1)
    k = terms + 1
    next_term = Q(comb(2 * k, k), 4**k * (2 * k + 1)) * x ** (2 * k + 1)
    # Successive coefficient ratios are < 1, hence each later term ratio is
    # < x^2 and the remaining positive tail is geometrically bounded.
    return partial, partial + next_term / (1 - x**2)


def main():
    if not __debug__:
        raise RuntimeError("replay requires assertions; do not run Python with -O")

    y = Q(46, 100)
    root = sqrt_interval(1 - y**2)
    angle = asin_interval(y)
    perimeter = (
        2 * (2 * root[0] - 1) + 4 * angle[0],
        2 * (2 * root[1] - 1) + 4 * angle[1],
    )
    assert perimeter[0] > Q(346364, 100000)

    sqrt2 = sqrt_interval(Q(2))
    sqrt3 = sqrt_interval(Q(3))
    coefficient_d1_lower = perimeter[0] / sqrt2[1]
    coefficient_d2_lower = perimeter[0] / (4 * sqrt3[1])
    assert coefficient_d1_lower > Q(244916, 100000)
    assert coefficient_d2_lower > Q(49993, 100000)

    d1 = d2 = Q(1, 100)
    sin_quarter = trig_alt((d2 / 4, d2 / 4), 1)
    delta_lower = d1 / sqrt2[1] + sin_quarter[0] / sqrt3[1]
    error_lower = delta_lower * perimeter[0] + PI[0] * delta_lower**2
    printed_bound = Q(244916, 100000) * d1 + Q(49993, 100000) * d2
    assert error_lower > printed_bound

    print(f"perimeter lower: {float(perimeter[0]):.15g}")
    print(f"d1 coefficient lower: {float(coefficient_d1_lower):.15g}")
    print(f"d2 coefficient lower: {float(coefficient_d2_lower):.15g}")
    print(f"error lower at d1=d2=0.01: {float(error_lower):.15g}")
    print(f"printed bound at d1=d2=0.01: {float(printed_bound):.15g}")
    print("PASS: Proposition 8's printed upper estimate is not justified")


if __name__ == "__main__":
    main()
