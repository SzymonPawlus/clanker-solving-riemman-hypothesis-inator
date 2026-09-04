#!/usr/bin/env python3
"""Exact Q(sqrt(3)) replay of the four-interval 0.23518 theorem."""
from fractions import Fraction as Q

from verify_circuit_formula import R3, TRIANGLE, dot, support, unit


TARGET = Q(11759, 50000)  # 0.23518 exactly


def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


def triangle_floor(tangents, allocation):
    normals = tuple((R3(u[1]), R3(-u[0])) for u in tangents)
    values = []
    for amount, ni in zip(allocation, normals):
        if amount == 0:
            continue
        cp, sp = -ni[1], ni[0]
        total = R3()
        for x, n in zip(allocation, normals):
            frame = (cp * n[0] + sp * n[1],
                     -sp * n[0] + cp * n[1])
            total += x * support(frame) / 2
        values.append(total)
    return min(values), tuple(values)


def data():
    tb, ta = Q(19999, 25000), Q(3, 200)
    cb, sb = unit(tb)
    ca, sa = unit(ta)
    p, q = Q(683, 2000), Q(317, 2000)
    tangents = ((cb, -sb), (ca, -sa), (ca, sa), (cb, sb),
                (Q(-1), Q(0)))
    closing = 2 * (p * cb + q * ca)
    loads = (p, q, q, p, closing)
    assert sum(loads[:4]) == 1
    assert sum(l * u[0] for l, u in zip(loads, tangents)) == 0
    assert sum(l * u[1] for l, u in zip(loads, tangents)) == 0
    assert all(cross(tangents[i], tangents[(i + 1) % 5]) > 0
               for i in range(5))

    x0 = q * sa / sb
    cross_a = (x0, Q(0), q, Q(0), x0 * cb + q * ca)
    inner_c = (Q(0), q, q, Q(0), 2 * q * ca)
    outer_b = (p, Q(0), Q(0), p, 2 * p * cb)
    for allocation in (cross_a, inner_c, outer_b):
        assert all(0 <= x <= cap for x, cap in zip(allocation, loads))
        assert sum(x * u[0] for x, u in zip(allocation, tangents)) == 0
        assert sum(x * u[1] for x, u in zip(allocation, tangents)) == 0
    return tangents, loads, cross_a, inner_c, outer_b


def projection(tangent, u):
    sine, cosine = 2 * u / (1 + u * u), (1 - u * u) / (1 + u * u)
    return abs(tangent[0] * sine - tangent[1] * cosine)


def support_bound(tangents, loads, allocation, triangle_constant, u):
    residual = sum((cap - used) * projection(tangent, u)
                   for tangent, cap, used in zip(tangents, loads, allocation))
    return triangle_constant + residual / 4


def main():
    tangents, loads, alloc_a, alloc_c, alloc_b = data()
    zero = (Q(0),) * 5
    q_a, candidates_a = triangle_floor(tangents, alloc_a)
    q_c, candidates_c = triangle_floor(tangents, alloc_c)
    q_b, candidates_b = triangle_floor(tangents, alloc_b)
    # Independent closed-form checks from the three-ray formula (7).
    cb, sb = tangents[3]
    ca, _ = tangents[2]
    p, q = loads[0], loads[1]
    assert q_c == R3(0, q * ca / 4)
    assert q_b == R3(p * sb / 4, 0)

    named = {"C": (alloc_c, q_c), "A": (alloc_a, q_a),
             "S": (zero, R3()), "B": (alloc_b, q_b)}
    intervals = (("C", Q(0), Q(9, 40)),
                 ("A", Q(9, 40), Q(1, 3)),
                 ("S", Q(1, 3), Q(1493, 2000)),
                 ("B", Q(1493, 2000), Q(1)))
    # Projection-wall audit on the half-domain: positive-angle walls have
    # half-angle parameters ta,tb; negative-angle walls have reciprocals.
    ta, tb = Q(3, 200), Q(19999, 25000)
    assert ta < Q(9, 40) < Q(1, 3) < Q(1493, 2000) < tb < 1
    assert 1 / ta > 1 and 1 / tb > 1
    margins = []
    for label, lo, hi in intervals:
        allocation, constant = named[label]
        left = support_bound(tangents, loads, allocation, constant, lo)
        right = support_bound(tangents, loads, allocation, constant, hi)
        assert not (left < TARGET) and not (right < TARGET)
        margins.extend((left - TARGET, right - TARGET))
        print(label, "u in", (lo, hi), "endpoints", left, right)

    # All residual coefficients are nonnegative.  Between the listed edge
    # angles each bound is constant plus a positive sinusoid, hence concave;
    # endpoint checks prove the whole interval.  The four u-intervals cover
    # phi in [0,pi/2].  Paired data give the other half by index reversal.
    mirror = (3, 2, 1, 0, 4)
    mirrored_a = tuple(alloc_a[mirror[i]] for i in range(5))
    q_d, _ = triangle_floor(tangents, mirrored_a)
    assert q_d == q_a
    assert min(margins).sign() > 0
    print("triangle A candidates", candidates_a)
    print("triangle C candidates", candidates_c)
    print("triangle B candidates", candidates_b)
    print("minimum endpoint margin", min(margins))
    print("PASS analytic direct-angle support floor >= 11759/50000 = 0.23518")


if __name__ == "__main__":
    main()
