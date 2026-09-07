#!/usr/bin/env python3
"""Exact algebraic replay for the calliper's three support sectors."""

from fractions import Fraction


def polynomial_margin(d: Fraction) -> Fraction:
    """Numerator proving r(gamma_D) >= 1 after clearing 8(1+d^2/4)."""
    expanded = 12 * d - d**3 - 2 * d**2 - 8
    factored = (2 - d) * (d**2 + 4 * d - 4)
    assert expanded == factored
    return factored


def verify_range(lo: Fraction, hi: Fraction) -> None:
    # A rational enclosure of the calliper root may be substituted here.  The
    # proof only needs the broader source range 1 < d < 2/sqrt(3), encoded
    # without irrational arithmetic as d^2 < 4/3.
    assert lo > 1
    assert hi > lo
    assert hi * hi < Fraction(4, 3)
    assert hi < 2

    # gamma_C < pi/6 follows from sqrt(d^2-1) < 1/sqrt(3).
    assert hi * hi - 1 < Fraction(1, 3)

    # 2 atan(1/2) > pi/6 follows from 1/2 > 2-sqrt(3), for which
    # sqrt(3)>3/2 is certified by squaring positive rationals.
    assert Fraction(3, 2) ** 2 < 3

    # Both factors in (1) stay strictly positive on the full enclosure.
    assert 2 - hi > 0
    assert lo * lo + 4 * lo - 4 > 0
    assert polynomial_margin(lo) > 0
    assert polynomial_margin(hi) > 0


def main() -> None:
    # Deliberately wider than the isolating interval used by verify_constant:
    # this checks that the support proof uses only the published source range.
    verify_range(Fraction(100001, 100000), Fraction(11547, 10000))
    print("PASS exact calliper support-sector algebra")


if __name__ == "__main__":
    main()
