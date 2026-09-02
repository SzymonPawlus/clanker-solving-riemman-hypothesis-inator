#!/usr/bin/env python3
"""Exact certificate for a rational four-edge support-envelope improvement.

Only ``Fraction`` arithmetic is used.  The sole irrationality is sqrt(3),
represented symbolically as ``a + b*sqrt(3)`` and bounded by rationals whose
squares are checked at startup.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F
from itertools import combinations


TARGET = F(47, 200)  # 0.235, strictly above the three-edge optimum
SQRT3_LO = F(1732050807568877293527446341505, 10**30)
SQRT3_HI = F(1732050807568877293527446341506, 10**30)


@dataclass(frozen=True)
class S:
    """An exact element a + b sqrt(3)."""

    a: F = F(0)
    b: F = F(0)

    def __add__(self, other):
        other = lift(other)
        return S(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self):
        return S(-self.a, -self.b)

    def __sub__(self, other):
        return self + (-lift(other))

    def __rsub__(self, other):
        return lift(other) - self

    def __mul__(self, other):
        other = lift(other)
        return S(self.a * other.a + 3 * self.b * other.b,
                 self.a * other.b + self.b * other.a)

    __rmul__ = __mul__

    def __truediv__(self, other):
        if isinstance(other, (int, F)):
            return S(self.a / other, self.b / other)
        raise TypeError("only rational division is needed")

    def sign(self):
        if self.a == 0:
            return (self.b > 0) - (self.b < 0)
        if self.b == 0 or (self.a > 0) == (self.b > 0):
            return (self.a > 0) - (self.a < 0)
        # Opposite signs: compare |a| with |b| sqrt(3), exactly by squaring.
        cmp = self.a * self.a - 3 * self.b * self.b
        if cmp == 0:
            return 0
        return ((self.a > 0) - (self.a < 0)) if cmp > 0 else ((self.b > 0) - (self.b < 0))

    def __lt__(self, other):
        return (self - other).sign() < 0

    def lower(self):
        return self.a + self.b * (SQRT3_LO if self.b >= 0 else SQRT3_HI)


def lift(x):
    return x if isinstance(x, S) else S(F(x), F(0))


def dot(u, v):
    return u[0] * v[0] + u[1] * v[1]


def cross(u, v):
    return u[0] * v[1] - u[1] * v[0]


def unit(t: F, sign=1):
    den = 1 + t * t
    return ((1 - t * t) / den, sign * 2 * t / den)


def exact_data():
    # Four traversed edges: p at +/- beta and q at +/- alpha.
    # tan(beta/2)=4/5, tan(alpha/2)=1/72.
    p, q = F(163, 480), F(77, 480)
    cb, sb = unit(F(4, 5), 1)
    ca, sa = unit(F(1, 72), 1)
    tangents = ((cb, -sb), (ca, -sa), (ca, sa), (cb, sb), (F(-1), F(0)))
    closing = 2 * p * cb + 2 * q * ca
    loads = (p, q, q, p, closing)
    assert sum(loads[:4]) == 1
    assert sum(loads[i] * tangents[i][0] for i in range(5)) == 0
    assert sum(loads[i] * tangents[i][1] for i in range(5)) == 0
    assert all(x > 0 for x in loads)
    # The four traversed directions and the untraversed closing edge are in
    # strict CCW boundary order; hence all five traversal vertices are hull
    # vertices.  The closing edge is not included in the worm length.
    assert all(cross(tangents[i], tangents[(i + 1) % 5]) > 0 for i in range(5))
    return tangents, loads


def maximal_three_cycles(tangents, loads):
    answer = []
    for inds in combinations(range(5), 3):
        us = [tangents[i] for i in inds]
        raw = [cross(us[(j + 1) % 3], us[(j + 2) % 3]) for j in range(3)]
        if not (all(x > 0 for x in raw) or all(x < 0 for x in raw)):
            continue
        raw = [abs(x) for x in raw]
        scale = min(loads[i] / x for i, x in zip(inds, raw))
        allocation = [F(0)] * 5
        for i, x in zip(inds, raw):
            allocation[i] = scale * x
        assert sum(allocation[i] * tangents[i][0] for i in range(5)) == 0
        assert sum(allocation[i] * tangents[i][1] for i in range(5)) == 0
        assert all(0 <= allocation[i] <= loads[i] for i in range(5))
        answer.append((inds, tuple(allocation)))
    assert [x[0] for x in answer] == [(0, 2, 4), (0, 3, 4), (1, 2, 4), (1, 3, 4)]
    return answer


TRIANGLE_VERTICES = ((S(0), S(0)), (S(F(1, 2)), S(0)),
                     (S(F(1, 4)), S(0, F(1, 4))))
TRIANGLE_NORMALS = ((S(0), S(-1)), (S(0, F(1, 2)), S(F(1, 2))),
                    (S(0, F(-1, 2)), S(F(1, 2))))


def support_triangle(n):
    return max(dot(v, n) for v in TRIANGLE_VERTICES)


def triangle_floor(tangents, allocation):
    """Exact min over all direct orientations of the equilateral triangle.

    Between orientations where a loaded normal is perpendicular to a triangle
    edge, the support sum is a positive sinusoid and hence concave.  Therefore
    its minimum occurs at one of the enumerated boundary orientations.
    """
    normals = tuple((S(u[1]), S(-u[0])) for u in tangents)
    candidates = []
    for k, amount in enumerate(allocation):
        if amount == 0:
            continue
        nk = normals[k]
        for m in TRIANGLE_NORMALS:
            # Rotation taking frame normal m to polygon normal nk.
            cp, sp = dot(m, nk), cross(m, nk)
            total = S(0)
            for x, n in zip(allocation, normals):
                # R(-psi)n
                frame_n = (cp * n[0] + sp * n[1], -sp * n[0] + cp * n[1])
                total += x * support_triangle(frame_n) / 2
            candidates.append(total)
    floor = min(candidates)
    assert all(not (x < floor) for x in candidates)
    return floor


def projection_numerator(u, lo, hi):
    """Lower bound for |uy(1-t^2)-2ux*t| on [lo,hi]."""
    ux, uy = u
    # Interval evaluation; all quantities are rational.
    one_minus = (1 - hi * hi, 1 - lo * lo)
    a = (uy * one_minus[0], uy * one_minus[1])
    if a[0] > a[1]:
        a = (a[1], a[0])
    b = (-2 * ux * hi, -2 * ux * lo)
    if b[0] > b[1]:
        b = (b[1], b[0])
    left, right = a[0] + b[0], a[1] + b[1]
    if left <= 0 <= right:
        return F(0)
    return min(abs(left), abs(right))


def bound_on_interval(tangents, loads, allocation, qfloor, lo, hi):
    numerator = F(0)
    for u, load, used in zip(tangents, loads, allocation):
        numerator += (load - used) * projection_numerator(u, lo, hi)
    return qfloor.lower() + numerator / (4 * (1 + hi * hi))


def certify_cover(tangents, loads, allocations):
    bounds = [(tuple(F(0) for _ in loads), S(0), ("segment",))]
    for inds, allocation in allocations:
        bounds.append((allocation, triangle_floor(tangents, allocation), inds))

    # Algebraic phi -> pi-phi invariance: reflection of the *support formula*
    # swaps paired tangent loads and the two cross-cycle allocations.  This is
    # not a reflected placement of the worm.
    mirror = (3, 2, 1, 0, 4)
    lookup = {label: (allocation, qfloor) for allocation, qfloor, label in bounds[1:]}
    for allocation, qfloor, label in bounds[1:]:
        mirrored = tuple(allocation[mirror[i]] for i in range(5))
        matches = [(a, q) for a, q, _ in bounds[1:] if a == mirrored]
        assert len(matches) == 1 and not (matches[0][1] < qfloor) and not (qfloor < matches[0][1])

    leaves = []
    stack = [(F(0), F(1), 0)]  # symmetry reduces phi in [0,pi] to [0,pi/2]
    while stack:
        lo, hi, depth = stack.pop()
        winners = []
        for allocation, qfloor, label in bounds:
            lower = bound_on_interval(tangents, loads, allocation, qfloor, lo, hi)
            if lower >= TARGET:
                winners.append((label, lower))
        if winners:
            leaves.append((lo, hi, max(winners, key=lambda x: x[1])[0]))
            continue
        assert depth < 36, (lo, hi)
        mid = (lo + hi) / 2
        stack.append((mid, hi, depth + 1))
        stack.append((lo, mid, depth + 1))

    leaves.sort()
    assert leaves[0][0] == 0 and leaves[-1][1] == 1
    assert all(a[1] == b[0] for a, b in zip(leaves, leaves[1:]))
    return bounds, leaves


def main():
    assert SQRT3_LO * SQRT3_LO < 3 < SQRT3_HI * SQRT3_HI
    tangents, loads = exact_data()
    allocations = maximal_three_cycles(tangents, loads)
    bounds, leaves = certify_cover(tangents, loads, allocations)
    print("exact four-edge witness: PASS")
    print("directions tan(theta/2): -4/5, -1/72, 1/72, 4/5")
    print("lengths: 163/480, 77/480, 77/480, 163/480 (sum 1)")
    print("closing load:", loads[-1])
    print("triangle floors:")
    for allocation, qfloor, label in bounds[1:]:
        print(" ", label, qfloor)
    print("complete tan(phi/2) cover leaves:", len(leaves))
    print("certified envelope floor >= 47/200 = 0.235")


if __name__ == "__main__":
    main()
