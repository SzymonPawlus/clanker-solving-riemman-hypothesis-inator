#!/usr/bin/env python3
"""Independent exact checker for the two Moser support slabs.

All arithmetic is Fraction arithmetic.  Trigonometric enclosures use a plain
Taylor polynomial at zero with an absolute Lagrange remainder; this file does
not import any certificate or checker from Issue #140.
"""

from fractions import Fraction as Q
from math import factorial

PI = (Q(333, 106), Q(355, 113))
N = 30


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
    """Taylor interval, valid because |derivative N+1| <= 1."""
    total = (Q(0), Q(0))
    start = 0 if cosine else 1
    for k in range(start, N + 1, 2):
        sign = Q(-1 if ((k - start) // 2) % 2 else 1)
        total = add(total, scale(sign / factorial(k), power(x, k)))
    rem = power((Q(0), max(abs(x[0]), abs(x[1]))), N + 1)[1] / factorial(N + 1)
    return total[0] - rem, total[1] + rem


def angle(deg):
    return scale(Q(deg, 180), PI)


def sincos(deg):
    x = angle(deg)
    return trig(x, False), trig(x, True)


C, S = Q(69, 269), Q(260, 269)


def normal_intervals(deg):
    sn, cs = sincos(deg)
    # x-coordinates of n0,n1,n2 after rotation by gamma.
    n0 = sn
    n1 = add(scale(S, cs), scale(C, sn))
    n2 = add(scale(2 * S * C, cs), scale(-(S * S - C * C), sn))
    return n0, n1, n2


def fixed_abs(interval, sign):
    return scale(Q(sign), interval)


def abs_range(interval):
    lo, hi = interval
    lower = Q(0) if lo <= 0 <= hi else min(abs(lo), abs(hi))
    return lower, max(abs(lo), abs(hi))


def certify_cell(lo, hi, family):
    whole = normal_intervals((lo + hi) / 2)
    # A midpoint enclosure alone is not a cell enclosure.  Bound displacement
    # of every unit-normal coordinate by angular radius (1-Lipschitz).
    radius = scale((hi - lo) / 360, PI)[1]
    whole = tuple((v[0] - radius, v[1] + radius) for v in whole)
    signs = []
    for v in whole:
        signs.append(1 if v[0] > 0 else (-1 if v[1] < 0 else 0))

    target = Q(2323, 10000) if family == "width" else Q(93, 400)
    if 0 in signs:
        a0, a1, a2 = map(abs_range, whole)
        if family == "width":
            worm = add(add(a0, a2), scale(Q(138, 269), a1))
            value = add(scale(Q(1, 12), worm), (Q(265, 153 * 24), Q(2)))
        else:
            value = add(scale(Q(1, 12), add(a0, a2)), scale(Q(169, 807), a1))
        assert value[0] >= target, ("crossing", family, lo, hi, value[0], target)
        return signs, value[0] - target

    endpoint_lowers = []
    for deg in (lo, hi):
        n0, n1, n2 = normal_intervals(deg)
        a0, a1, a2 = (fixed_abs(v, sg) for v, sg in zip((n0, n1, n2), signs))
        if family == "width":
            worm = add(add(a0, a2), scale(Q(138, 269), a1))
            # sqrt(3) > 265/153 (squared comparison is checked below).
            value = add(scale(Q(1, 12), worm), (Q(265, 153 * 24), Q(2)))
        else:
            value = add(scale(Q(1, 12), add(a0, a2)), scale(Q(169, 807), a1))
        assert value[0] >= target, (family, lo, hi, deg, value[0], target)
        endpoint_lowers.append(value[0])

    # On a sign-fixed cell the expression is A cos+B sin plus a constant.
    # Its nonconstant part has second derivative equal to its negative.  The
    # verified positive lower endpoint and concavity therefore put the minimum
    # at an endpoint.  We record the partition and endpoint margin.
    return signs, min(endpoint_lowers) - target


def half_degree_cells(lo, hi):
    x = Q(lo)
    while x < hi:
        y = min(x + Q(1, 2), Q(hi))
        yield x, y
        x = y


def main():
    assert PI[0] * 106 == 333 and PI[1] * 113 == 355
    assert Q(265, 153) ** 2 < 3
    # Re-derive both displayed closed forms from actual edge lengths, the two
    # allocations, and centred unit-segment support h(n)=|n.x|/2.
    chord = Q(407, 807)
    assert Q(1, 2) * Q(1, 3) * Q(1, 2) == Q(1, 12)
    assert Q(1, 2) * chord * Q(138, 407) * Q(1, 2) == Q(138, 269) / 12
    assert Q(1, 2) * (Q(1, 3) + chord) * Q(1, 2) == Q(169, 807)
    # The triangle V has side 1/2, minimum width sqrt(3)/4; its antipodal
    # support pair carries the outer coefficient 1/6.
    assert Q(1, 6) * Q(1, 4) == Q(1, 24)
    ledgers = []
    for family, pieces in (
        ("width", ((Q(75), Q(269, 2)),)),
        ("complement", ((Q(0), Q(80)), (Q(259, 2), Q(180)))),
    ):
        cells = 0
        margin = None
        patterns = set()
        for a, b in pieces:
            for lo, hi in half_degree_cells(a, b):
                signs, m = certify_cell(lo, hi, family)
                patterns.add(tuple(signs))
                margin = m if margin is None else min(margin, m)
                cells += 1
        ledgers.append((family, cells, sorted(patterns), margin))

    # Exact closed endpoint union and conservative target comparison.
    assert Q(75) <= Q(80)
    assert Q(259, 2) <= Q(269, 2)
    assert Q(232239, 1000000) < Q(2323, 10000) < Q(93, 400)
    for family, cells, patterns, margin in ledgers:
        print(f"{family}: {cells} cells; signs={patterns}; minimum margin={margin}")
    print("PASS exact sign/concavity slabs and full closed endpoint union")


if __name__ == "__main__":
    main()
