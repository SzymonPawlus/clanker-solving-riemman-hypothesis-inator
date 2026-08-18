"""Exact facts about the numerical n=16 PSLQ polynomial candidate.

These checks do *not* connect the contact-system root to the polynomial.  They only
prove properties of the integer polynomial that PSLQ proposed: primitivity,
irreducibility over Q, and rational isolation of the matching real root.
"""

from __future__ import annotations

import math
from fractions import Fraction

COEFFICIENTS = (
    9, -246, 3112, -23836, 121624, -429448,
    1055998, -1772356, 1925755, -1211242, 331654,
)
MODULUS = 43
ROOT_LO = Fraction(216227269309781821, 10**18)
ROOT_HI = Fraction(216227269309781822, 10**18)


def _trim(poly):
    poly = list(poly)
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return poly


def _divmod_q(left, right):
    left = _trim(left)
    right = _trim(right)
    quotient = [Fraction(0)] * max(1, len(left) - len(right) + 1)
    while len(left) >= len(right) and left != [0]:
        shift = len(left) - len(right)
        factor = left[-1] / right[-1]
        quotient[shift] = factor
        for i, value in enumerate(right):
            left[i + shift] -= factor * value
        left = _trim(left)
    return _trim(quotient), left


def _sturm(poly):
    sequence = [[Fraction(c) for c in poly]]
    sequence.append([Fraction(i) * sequence[0][i] for i in range(1, len(poly))])
    while sequence[-1] != [0]:
        _, remainder = _divmod_q(sequence[-2], sequence[-1])
        if remainder == [0]:
            break
        sequence.append([-value for value in remainder])
    return sequence


def _evaluate(poly, value):
    result = value * 0
    for coefficient in reversed(poly):
        result = result * value + coefficient
    return result


def _variations(sequence, value):
    signs = []
    for poly in sequence:
        result = _evaluate(poly, value)
        if result:
            signs.append(1 if result > 0 else -1)
    return sum(a != b for a, b in zip(signs, signs[1:]))


def roots_between(lo: Fraction, hi: Fraction) -> int:
    sequence = _sturm(COEFFICIENTS)
    if _evaluate(COEFFICIENTS, lo) == 0 or _evaluate(COEFFICIENTS, hi) == 0:
        raise ValueError("interval endpoints must not be roots")
    return _variations(sequence, lo) - _variations(sequence, hi)


def _mod_trim(poly):
    return _trim([value % MODULUS for value in poly])


def _mod_divmod(left, right):
    left = _mod_trim(left)
    right = _mod_trim(right)
    quotient = [0] * max(1, len(left) - len(right) + 1)
    inverse = pow(right[-1], -1, MODULUS)
    while len(left) >= len(right) and left != [0]:
        shift = len(left) - len(right)
        factor = left[-1] * inverse % MODULUS
        quotient[shift] = factor
        for i, value in enumerate(right):
            left[i + shift] = (left[i + shift] - factor * value) % MODULUS
        left = _mod_trim(left)
    return _mod_trim(quotient), left


def _mod_mul(left, right, modulus_poly):
    product = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            product[i + j] = (product[i + j] + a * b) % MODULUS
    return _mod_divmod(product, modulus_poly)[1]


def _mod_pow(base, exponent, modulus_poly):
    result = [1]
    while exponent:
        if exponent & 1:
            result = _mod_mul(result, base, modulus_poly)
        base = _mod_mul(base, base, modulus_poly)
        exponent >>= 1
    return result


def _mod_gcd(left, right):
    while right != [0]:
        left, right = right, _mod_divmod(left, right)[1]
    inverse = pow(left[-1], -1, MODULUS)
    return _mod_trim([value * inverse for value in left])


def irreducible_mod_43() -> bool:
    """Rabin irreducibility test for the degree-10 reduction modulo 43."""
    polynomial = _mod_trim(COEFFICIENTS)
    x = [0, 1]
    # For n=10, test gcd(x^(q^(n/r))-x,f)=1 for prime r | n, then x^(q^n)=x.
    for exponent in (10 // 2, 10 // 5):
        power = _mod_pow(x, MODULUS**exponent, polynomial)
        difference = _mod_trim([(power[i] if i < len(power) else 0) - (x[i] if i < 2 else 0)
                                for i in range(max(len(power), 2))])
        if _mod_gcd(polynomial, difference) != [1]:
            return False
    return _mod_pow(x, MODULUS**10, polynomial) == x


def verify_exact_properties() -> dict[str, object]:
    content = 0
    for coefficient in COEFFICIENTS:
        content = math.gcd(content, abs(coefficient))
    bound = Fraction(1) + Fraction(
        max(map(abs, COEFFICIENTS[:-1])), abs(COEFFICIENTS[-1])
    )
    return {
        "primitive": content == 1,
        "irreducible_mod_43": irreducible_mod_43(),
        "irreducible_over_q": content == 1 and irreducible_mod_43(),
        "matching_interval": [str(ROOT_LO), str(ROOT_HI)],
        "roots_in_matching_interval": roots_between(ROOT_LO, ROOT_HI),
        "total_real_roots": roots_between(-bound, bound),
    }


if __name__ == "__main__":
    print(verify_exact_properties())
