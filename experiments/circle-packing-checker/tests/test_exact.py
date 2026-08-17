"""Unit tests for the exact-arithmetic core.

The properties that matter: roots are exact, enclosures really enclose, signs are
decided rather than guessed, and no float can sneak in.
"""

from __future__ import annotations

from fractions import Fraction

import pytest
import sympy

from packcheck.exact import (
    RatInterval,
    UnsupportedExpression,
    enclose,
    iroot,
    is_exactly_zero,
    is_nonneg,
    sign_of,
)


@pytest.mark.parametrize("n", [1, 2, 3, 5, 7])
@pytest.mark.parametrize("a", [0, 1, 2, 26, 10**30, 10**30 + 1, 2**101 - 1])
def test_iroot_is_exact_floor(a, n):
    r = iroot(a, n)
    assert r**n <= a < (r + 1) ** n


def test_iroot_on_perfect_powers():
    assert iroot(10**30, 3) == 10**10
    assert iroot(3**101, 101) == 3


@pytest.mark.parametrize(
    "expr",
    [sympy.sqrt(3), sympy.sqrt(2), 2 * sympy.sqrt(3), sympy.Rational(7, 3), sympy.cbrt(7),
     4 + 4 * sympy.sqrt(3), sympy.sqrt(33) / 3],
)
@pytest.mark.parametrize("bits", [8, 64, 200])
def test_enclosure_really_encloses(expr, bits):
    iv = enclose(expr, bits)
    assert isinstance(iv.lo, Fraction) and isinstance(iv.hi, Fraction)
    # Cross-check against a high-precision (but independent) evaluation.
    exact_lo = sympy.Rational(iv.lo.numerator, iv.lo.denominator)
    exact_hi = sympy.Rational(iv.hi.numerator, iv.hi.denominator)
    assert sympy.simplify(expr - exact_lo) >= 0
    assert sympy.simplify(exact_hi - expr) >= 0
    assert iv.width() <= Fraction(1, 2 ** (bits - 4))


def test_sign_of_rationals_and_radicals():
    assert sign_of(sympy.Integer(0)) == 0
    assert sign_of(sympy.Rational(-1, 10**40)) == -1
    assert sign_of(sympy.sqrt(3) - sympy.Rational(17320508, 10**7)) == 1
    assert sign_of(sympy.sqrt(3) - sympy.Rational(17320509, 10**7)) == -1


def test_sign_of_an_exactly_zero_algebraic_number():
    """The case that a tolerance-based checker gets wrong: an exact contact."""
    # 1^2 + sqrt(3)^2 - 2^2 == 0 -- adjacent triangular-lattice rows touch exactly.
    expr = 1**2 + sympy.sqrt(3) ** 2 - 4
    assert sign_of(expr) == 0
    assert is_nonneg(expr)


def test_sign_of_a_nested_radical_zero():
    expr = sympy.sqrt(3 + 2 * sympy.sqrt(2)) - (1 + sympy.sqrt(2))
    assert is_exactly_zero(expr)
    assert sign_of(expr) == 0


def test_sign_of_something_astronomically_small_but_nonzero():
    """Nothing here is 'close enough to zero'."""
    expr = sympy.sqrt(3) - sympy.Rational(1, 10**200) - sympy.sqrt(3)
    assert sign_of(expr) == -1
    assert not is_nonneg(expr)


def test_floats_are_refused_not_rounded():
    with pytest.raises(UnsupportedExpression, match="float literal"):
        sign_of(sympy.Float(1.5))
    with pytest.raises(UnsupportedExpression, match="float literal"):
        enclose(sympy.Float(1.5), 64)


def test_transcendental_input_is_refused_not_approximated():
    with pytest.raises(UnsupportedExpression):
        enclose(sympy.pi, 64)


def test_interval_arithmetic_rounds_outward():
    a = RatInterval(Fraction(1, 3), Fraction(1, 2))
    b = RatInterval(Fraction(-1), Fraction(2))
    assert (a + b) == RatInterval(Fraction(-2, 3), Fraction(5, 2))
    assert (a * b).lo == Fraction(-1, 2)
    assert (a * b).hi == Fraction(1)
    assert (a - a).contains_zero()


def test_is_nonneg_on_intervals_is_conservative():
    assert is_nonneg(RatInterval(Fraction(0), Fraction(1)))
    assert not is_nonneg(RatInterval(Fraction(-1, 10**50), Fraction(1)))
