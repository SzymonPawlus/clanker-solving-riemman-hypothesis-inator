#!/usr/bin/env python3
"""Exact checks for the analytic three-ray triangle-floor formula."""
from dataclasses import dataclass
from fractions import Fraction as Q


@dataclass(frozen=True)
class R3:
    a: Q = Q(0)
    b: Q = Q(0)

    def __add__(self, other):
        other = lift(other)
        return R3(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self):
        return R3(-self.a, -self.b)

    def __sub__(self, other):
        return self + -lift(other)

    def __rsub__(self, other):
        return lift(other) - self

    def __mul__(self, other):
        other = lift(other)
        return R3(self.a * other.a + 3 * self.b * other.b,
                  self.a * other.b + self.b * other.a)

    __rmul__ = __mul__

    def __truediv__(self, q):
        return R3(self.a / q, self.b / q)

    def sign(self):
        if self.a == 0:
            return (self.b > 0) - (self.b < 0)
        if self.b == 0 or (self.a > 0) == (self.b > 0):
            return (self.a > 0) - (self.a < 0)
        d = self.a * self.a - 3 * self.b * self.b
        if d == 0:
            return 0
        source = self.a if d > 0 else self.b
        return (source > 0) - (source < 0)

    def __lt__(self, other):
        return (self - other).sign() < 0


def lift(x):
    return x if isinstance(x, R3) else R3(Q(x))


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


TRIANGLE = ((R3(0), R3(0)), (R3(Q(1, 2)), R3(0)),
            (R3(Q(1, 4)), R3(0, Q(1, 4))))


def support(n):
    return max(dot(v, n) for v in TRIANGLE)


def unit(t):
    return (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)


def enumerated_floor(t):
    c, s = unit(t)
    tangents = ((c, -s), (c, s), (Q(-1), Q(0)))
    normals = tuple((R3(u[1]), R3(-u[0])) for u in tangents)
    loads = (Q(1), Q(1), 2 * c)
    values = []
    # Align the downward triangle fan wall (0,-1) with each loaded normal.
    for ni in normals:
        cp, sp = -ni[1], ni[0]
        total = R3()
        for amount, n in zip(loads, normals):
            frame = (cp * n[0] + sp * n[1],
                     -sp * n[0] + cp * n[1])
            total += amount * support(frame) / 2
        values.append(total)
    return min(values), tuple(values)


def stated_branch(t):
    c, s = unit(t)
    y = t * t
    cubic = y ** 3 - 33 * y ** 2 + 27 * y - 3
    if y <= Q(1, 3):
        return R3(0, c / 4)
    if cubic >= 0:  # between 1/3 and the isolated middle root rho
        return R3(s / 4, 0)
    return R3(s * c / 4, (s * s - c * c) / 8)


def main():
    h = lambda y: y ** 3 - 33 * y ** 2 + 27 * y - 3
    assert h(Q(7, 10)) == Q(73, 1000) > 0
    assert h(Q(71, 100)) == Q(-107389, 1000000) < 0
    # h' = 3(y^2-22y+9) is negative throughout the isolating interval.
    assert Q(71, 100) ** 2 - 22 * Q(7, 10) + 9 < 0
    samples = (Q(1, 10), Q(1, 2), Q(7, 12), Q(2, 3),
               Q(4, 5), Q(9, 10), Q(19, 20), Q(1))
    for t in samples:
        floor, candidates = enumerated_floor(t)
        expected = stated_branch(t)
        assert floor == expected, (t, floor, expected, candidates)
        print("t=", t, "floor=", floor, "fan candidates=", candidates)
    # Exact half-angle reduction behind the general equioscillation theorem.
    for a, b, constant, u in ((Q(2, 7), Q(-3, 5), Q(11, 13), Q(4, 9)),
                              (Q(-5, 8), Q(7, 12), Q(-2, 3), Q(13, 17))):
        sine, cosine = 2 * u / (1 + u * u), (1 - u * u) / (1 + u * u)
        lhs = a * sine + b * cosine + constant
        polynomial = ((constant - b) * u * u + 2 * a * u
                      + b + constant)
        assert lhs * (1 + u * u) == polynomial
    # One asymmetric positive-circuit identity from formula (2).
    ta, tb = Q(2, 5), Q(3, 4)
    ca, sa = unit(ta)
    cb, sb = unit(tb)
    # Directions -alpha, +beta, pi; sin(alpha+beta) is exact rational.
    sab = sa * cb + ca * sb
    vectors = ((ca, -sa), (cb, sb), (Q(-1), Q(0)))
    loads = (sb, sa, sab)
    assert sum(load * vector[0] for load, vector in zip(loads, vectors)) == 0
    assert sum(load * vector[1] for load, vector in zip(loads, vectors)) == 0
    print("PASS exact Q(sqrt(3)) circuit-floor branch checks")


if __name__ == "__main__":
    main()
