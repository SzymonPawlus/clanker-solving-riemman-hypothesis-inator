#!/usr/bin/env python3
"""Exact-rational replay for the t=10/13 support decomposition."""

from fractions import Fraction as F


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def scale(q, a):
    return (q * a[0], q * a[1])


def sqnorm(a):
    return a[0] ** 2 + a[1] ** 2


def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def support(points, normal):
    return max(dot(point, normal) for point in points)


def main():
    c, s = F(69, 269), F(260, 269)
    assert c * c + s * s == 1

    p = [
        (F(0), F(0)),
        (F(1, 3), F(0)),
        (F(338, 807), F(260, 807)),
        (F(9361, 72361), F(105820, 217083)),
    ]
    edges = [
        (p[(i + 1) % 4][0] - p[i][0], p[(i + 1) % 4][1] - p[i][1])
        for i in range(4)
    ]
    assert all(sqnorm(e) == F(1, 9) for e in edges[:3])
    assert all(cross(edges[i], edges[(i + 1) % 4]) > 0 for i in range(4))

    # Three successive unit directions 1, z, z^2.
    assert edges[0] == (F(1, 3), F(0))
    assert edges[1] == (c / 3, s / 3)
    assert edges[2] == ((c * c - s * s) / 3, 2 * c * s / 3)

    chord_length = F(1, 3) * (1 + 2 * c)
    assert chord_length == F(407, 807)
    assert sqnorm(edges[3]) == chord_length * chord_length

    twice_area = sum(cross(p[i], p[(i + 1) % 4]) for i in range(4))
    assert twice_area > 0
    assert twice_area / 2 == F(87880, 651249)

    # Intrinsic outward unit normals in edge order.
    n0 = (F(0), F(-1))
    n1 = (s, -c)
    n2 = (2 * s * c, s * s - c * c)
    n3 = (-s, c)
    assert all(sqnorm(n) == 1 for n in (n0, n1, n2, n3))

    # The template support-area functional reproduces its own area exactly.
    lengths = (F(1, 3), F(1, 3), F(1, 3), chord_length)
    normals = (n0, n1, n2, n3)
    support_area = sum(
        length * support(p, normal)
        for length, normal in zip(lengths, normals)
    ) / 2
    assert support_area == twice_area / 2

    # Exact balanced decomposition of the trapezoid surface measure.
    assert add(add(n0, n2), scale(2 * c, n3)) == (0, 0)
    assert add(n1, n3) == (0, 0)

    # Exact primal edge capacities at the diagnostic maximizer:
    # C assigned to the segment and D assigned to the square.
    segment_lambda = (F(1), F(0), F(1), F(138, 407))
    square_lambda = (F(0), F(1), F(0), F(269, 407))
    assert all(a + b == 1 for a, b in zip(segment_lambda, square_lambda))
    segment_load = (F(0), F(0))
    square_load = (F(0), F(0))
    for length, normal, a, b in zip(
        lengths, normals, segment_lambda, square_lambda
    ):
        segment_load = add(segment_load, scale(length * a, normal))
        square_load = add(square_load, scale(length * b, normal))
    assert segment_load == (0, 0)
    assert square_load == (0, 0)

    # Recombining the two pieces reproduces the four edge lengths.
    assert F(2) * c / 3 + F(1, 3) == chord_length
    total = add(add(scale(F(1, 3), n0), scale(F(1, 3), n1)),
                add(scale(F(1, 3), n2), scale(chord_length, n3)))
    assert total == (0, 0)

    print("PASS exact t=10/13 witness and balanced support split")


if __name__ == "__main__":
    main()
