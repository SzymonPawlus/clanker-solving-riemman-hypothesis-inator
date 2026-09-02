#!/usr/bin/env python3
"""Exact audit of the rational witness in equal-turn-envelope-theorem.md.

This checker is intentionally limited to rational identities and comparisons;
it does not implement the producer's angular subdivision or geometric bridge.
"""

from fractions import Fraction as Q


def sqnorm(v: tuple[Q, Q]) -> Q:
    return v[0] * v[0] + v[1] * v[1]


def sub(a: tuple[Q, Q], b: tuple[Q, Q]) -> tuple[Q, Q]:
    return a[0] - b[0], a[1] - b[1]


p, q = 2396, 3003
d = p * p + q * q
c = Q(q * q - p * p, d)
s = Q(2 * p * q, d)

assert c == Q(3277193, 14758825)
assert s == Q(14390376, 14758825)
assert c * c + s * s == 1

vertices = (
    (Q(0), Q(0)),
    (Q(1, 3), Q(0)),
    (Q(6012006, 14758825), Q(4796792, 14758825)),
    (
        Q(69847505896723, 653468746141875),
        Q(102235040019112, 217822915380625),
    ),
)

assert vertices[2] == ((1 + c) / 3, s / 3)
assert vertices[3] == ((c + 2 * c * c) / 3, s * (1 + 2 * c) / 3)
for a, b in zip(vertices, vertices[1:]):
    assert sqnorm(sub(b, a)) == Q(1, 9)

# c < c_* without evaluating sqrt(13): c_*^2=(4-sqrt(13))/8.
radical_upper = 4 - 8 * c * c
assert radical_upper > 0
assert radical_upper * radical_upper > 13

# Therefore this is the left side of the unique optimizer and A_s is active.
assert 64 * c * c * s * s < 3
endpoint = s * (1 + 2 * c) / 6
assert endpoint == Q(51117520009556, 217822915380625)
assert endpoint > Q(2346746664, 10_000_000_000)
assert endpoint > Q(232239, 1_000_000)

print("PASS")
print(f"c={c}")
print(f"s={s}")
print(f"endpoint={endpoint}")
