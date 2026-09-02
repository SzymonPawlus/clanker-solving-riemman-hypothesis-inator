#!/usr/bin/env python3
"""Exact-rational enclosure of the Adhikari--Pitman calliper constant."""

from fractions import Fraction as Q
from math import isqrt


def add(x, y):
    return x[0] + y[0], x[1] + y[1]


def scale(c, x):
    return (c * x[0], c * x[1]) if c >= 0 else (c * x[1], c * x[0])


def atan_interval(x, terms=20):
    """Alternating-series enclosure for atan on a positive rational interval."""
    assert Q(0) <= x[0] <= x[1] < Q(1)

    def partial(last):
        lo = hi = Q(0)
        for k in range(last + 1):
            coefficient = Q((-1) ** k, 2 * k + 1)
            term = x[0] ** (2 * k + 1), x[1] ** (2 * k + 1)
            if coefficient > 0:
                lo, hi = lo + coefficient * term[0], hi + coefficient * term[1]
            else:
                lo, hi = lo + coefficient * term[1], hi + coefficient * term[0]
        return lo, hi

    a, b = partial(terms), partial(terms + 1)
    return min(a[0], b[0]), max(a[1], b[1])


def sqrt_interval(x, digits=50):
    scale10 = 10**digits
    floor_scaled = isqrt(x.numerator * x.denominator * scale10**2) // x.denominator
    while Q(floor_scaled + 1, scale10) ** 2 <= x:
        floor_scaled += 1
    while Q(floor_scaled, scale10) ** 2 > x:
        floor_scaled -= 1
    out = Q(floor_scaled, scale10), Q(floor_scaled + 1, scale10)
    assert out[0] ** 2 <= x < out[1] ** 2
    return out


def atan_point(x, terms=80):
    values = [sum(Q((-1) ** k, 2 * k + 1) * x ** (2 * k + 1) for k in range(n + 1))
              for n in (terms, terms + 1)]
    return min(values), max(values)


PI = add(scale(16, atan_point(Q(1, 5))), scale(-4, atan_point(Q(1, 239), 30)))


def polynomial_z(z):
    return 3 * z**3 + 36 * z**2 + 16 * z - 64


def main():
    if not __debug__:
        raise RuntimeError("replay requires assertions; do not run Python with -O")

    d = Q(104359010959, 10**11), Q(52179505481, 5 * 10**10)
    assert d[0] < d[1]
    assert polynomial_z(d[0] ** 2) < 0 < polynomial_z(d[1] ** 2)
    # P'(z)=9z^2+72z+16 is positive for z>0, so this isolates the root.

    s_lo = sqrt_interval(d[0] ** 2 - 1)
    s_hi = sqrt_interval(d[1] ** 2 - 1)
    s = s_lo[0], s_hi[1]
    arcsec_d = atan_interval(s)
    atan_half_d = atan_interval((d[0] / 2, d[1] / 2))
    length = add(
        add(scale(2, s), d),
        add(PI, add(scale(-2, arcsec_d), scale(-4, atan_half_d))),
    )
    breadth = Q(1, 1) / length[1], Q(1, 1) / length[0]
    lower = Q(17557, 40000)

    assert breadth[0] > lower
    print(f"d: [{float(d[0]):.15g}, {float(d[1]):.15g}]")
    print(f"length: [{float(length[0]):.15g}, {float(length[1]):.15g}]")
    print(f"breadth: [{float(breadth[0]):.15g}, {float(breadth[1]):.15g}]")
    print(f"breadth lower margin over 0.438925: {float(breadth[0] - lower):.15g}")
    print("PASS: b0 > 0.438925")


if __name__ == "__main__":
    main()
