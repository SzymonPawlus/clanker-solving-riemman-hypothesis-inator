#!/usr/bin/env python3
"""Exact angular slab check for the t=75/94 equal-turn candidate.

This checks only the two closed support formulas.  Their geometric mixed-area
interpretation remains capped by the separately reviewed dependency ledger.
"""
from fractions import Fraction as Q
from math import factorial

N = 24
C, S = Q(3211, 14461), Q(14100, 14461)
TARGET = Q(1173, 5000)  # 0.2346


def atan_inverse(n, terms=24):
    """Alternating-series enclosure of atan(1/n)."""
    partial = Q(0)
    for k in range(terms):
        partial += Q(-1 if k % 2 else 1, (2 * k + 1) * n ** (2 * k + 1))
    omitted = Q(1, (2 * terms + 1) * n ** (2 * terms + 1))
    return ((partial, partial + omitted) if terms % 2 == 0
            else (partial - omitted, partial))


def machin_pi():
    a, b = atan_inverse(5)
    c, d = atan_inverse(239)
    return 16 * a - 4 * d, 16 * b - 4 * c


PI = machin_pi()


def add(x, y):
    return x[0] + y[0], x[1] + y[1]


def mul(x, y):
    z = (x[0] * y[0], x[0] * y[1], x[1] * y[0], x[1] * y[1])
    return min(z), max(z)


def scale(a, x):
    return (a * x[0], a * x[1]) if a >= 0 else (a * x[1], a * x[0])


def power(x, k):
    out = (Q(1), Q(1))
    for _ in range(k):
        out = mul(out, x)
    return out


def trig(x, cosine):
    total = (Q(0), Q(0))
    start = 0 if cosine else 1
    for k in range(start, N + 1, 2):
        sign = Q(-1 if ((k - start) // 2) % 2 else 1)
        total = add(total, scale(sign / factorial(k), power(x, k)))
    radius = max(abs(x[0]), abs(x[1]))
    remainder = radius ** (N + 1) / factorial(N + 1)
    return total[0] - remainder, total[1] + remainder


def sincos(degrees):
    angle = scale(Q(degrees, 180), PI)
    return trig(angle, False), trig(angle, True)


def normal_x(degrees):
    sn, cs = sincos(degrees)
    # sin(gamma), sin(gamma+theta), sin(gamma+2 theta).
    return (sn,
            add(scale(S, cs), scale(C, sn)),
            add(scale(2 * S * C, cs), scale(C * C - S * S, sn)))


def fixed_abs(interval, sign):
    return scale(Q(sign), interval)


def abs_range(interval):
    lo, hi = interval
    lower = Q(0) if lo <= 0 <= hi else min(abs(lo), abs(hi))
    return lower, max(abs(lo), abs(hi))


def formula(normals, family):
    a0, a1, a2 = normals
    if family == "width":
        moving = add(add(a0, a2), scale(2 * C, a1))
        # sqrt(3) > 265/153.
        return add(scale(Q(1, 12), moving), (Q(265, 153 * 24), Q(2)))
    return add(scale(Q(1, 12), add(a0, a2)), scale((1 + C) / 6, a1))


def certify_cell(lo, hi, family):
    midpoint = (lo + hi) / 2
    whole = normal_x(midpoint)
    # Each unit-normal coordinate is 1-Lipschitz in radians.
    radius = scale((hi - lo) / 360, PI)[1]
    whole = tuple((v[0] - radius, v[1] + radius) for v in whole)
    signs = tuple(1 if v[0] > 0 else (-1 if v[1] < 0 else 0) for v in whole)
    if 0 in signs:
        value = formula(tuple(map(abs_range, whole)), family)
        if value[0] < TARGET and hi - lo > Q(1, 100000):
            middle = (lo + hi) / 2
            return min(certify_cell(lo, middle, family),
                       certify_cell(middle, hi, family))
        assert value[0] >= TARGET, ("crossing", family, lo, hi, value[0])
        return value[0] - TARGET

    lowers = []
    for endpoint in (lo, hi):
        values = tuple(fixed_abs(v, sign)
                       for v, sign in zip(normal_x(endpoint), signs))
        value = formula(values, family)
        assert value[0] >= TARGET, (family, lo, hi, endpoint, value[0])
        lowers.append(value[0])
    # On a sign-fixed cell the nonconstant formula is A cos+B sin, is positive,
    # and has second derivative equal to its negative.  It is concave, hence
    # its cell minimum is attained at an endpoint.
    return min(lowers) - TARGET


def cells(lo, hi, step=Q(1, 2)):
    x = Q(lo)
    while x < hi:
        y = min(x + step, Q(hi))
        yield x, y
        x = y


def main():
    assert C * C + S * S == 1
    assert Q(265, 153) ** 2 < 3
    chord = (1 + 2 * C) / 3
    allocation = 2 * C / (1 + 2 * C)
    assert chord == Q(6961, 14461)
    assert Q(1, 2) * chord * allocation * Q(1, 2) == (2 * C) / 12
    assert Q(1, 2) * (Q(1, 3) + chord) * Q(1, 2) == (1 + C) / 6
    vertices = ((Q(0), Q(0)), (Q(1, 3), Q(0)),
                ((1 + C) / 3, S / 3),
                ((1 + 2 * C) * C / 3, (1 + 2 * C) * S / 3))
    for p, q in zip(vertices, vertices[1:]):
        assert (q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2 == Q(1, 9)
    # Actual CCW hull surface normals, including the untraversed closing chord.
    normals = ((Q(0), Q(-1)), (S, -C),
               (2 * S * C, -(C * C - S * S)), (-S, C))
    lengths = (Q(1, 3), Q(1, 3), Q(1, 3), chord)
    assert all(x * x + y * y == 1 for x, y in normals)
    assert sum(length * normal[0] for length, normal in zip(lengths, normals)) == 0
    assert sum(length * normal[1] for length, normal in zip(lengths, normals)) == 0
    # The two exact allocation columns used by the slabs.  Entries are
    # (segment, triangle); each surface edge has unit capacity.  The width
    # allocation's only moving-template load cancels between n1 and -n1.
    width_allocation = ((Q(1), Q(0)), (Q(0), Q(1)), (Q(1), Q(0)),
                        (allocation, 1 - allocation))
    complement_allocation = tuple((Q(1), Q(0)) for _ in lengths)
    for table in (width_allocation, complement_allocation):
        assert all(a >= 0 and b >= 0 and a + b == 1 for a, b in table)
    for coordinate in (0, 1):
        assert sum(lengths[k] * width_allocation[k][1] * normals[k][coordinate]
                   for k in range(4)) == 0

    ledger = []
    for family, intervals in (
        ("width", ((Q(771, 10), Q(257, 2)),)),
        ("complement", ((Q(0), Q(386, 5)), (Q(257, 2), Q(180)))),
    ):
        margins = []
        for lo, hi in intervals:
            margins.extend(certify_cell(a, b, family) for a, b in cells(lo, hi))
        ledger.append((family, len(margins), min(margins)))

    # Closed interval union: [0,77.2] U [77.1,128.5] U [128.5,180].
    assert Q(771, 10) <= Q(386, 5)
    assert Q(257, 2) <= Q(257, 2)
    assert TARGET > Q(232239, 1_000_000)
    for family, count, margin in ledger:
        print(f"{family}: {count} cells; minimum margin>{float(margin):.12g}; "
              f"exact numerator/denominator bits={margin.numerator.bit_length()}/"
              f"{margin.denominator.bit_length()}")
    print("PASS exact t=75/94 slabs; endpoint", TARGET)


if __name__ == "__main__":
    main()
