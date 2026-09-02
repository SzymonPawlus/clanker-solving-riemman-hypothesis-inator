"""Numerically rank rational equal-turn arcs by two reviewed slab formulas.

This is candidate generation, not a global certificate.  Every displayed arc
and coefficient is nevertheless recomputed exactly with Fraction arithmetic;
only the minimization over the rotation angle uses binary64 sampling.
"""
from fractions import Fraction as F
import argparse
import math
import numpy as np


def parameters(t):
    c = (1 - t * t) / (1 + t * t)
    s = 2 * t / (1 + t * t)
    chord = (1 + 2 * c) / 3
    vertices = (
        (F(0), F(0)),
        (F(1, 3), F(0)),
        ((1 + c) / 3, s / 3),
        ((1 + 2 * c) * c / 3, (1 + 2 * c) * s / 3),
    )
    # Coefficients of |n1.x| in the width and all-segment slabs.
    return c, s, chord, vertices, 2 * c, (1 + c) / 6


def exact_checks(t):
    c, s, chord, vertices, width_mid, complement_mid = parameters(t)
    assert c >= 0 and c * c + s * s == 1
    for p, q in zip(vertices, vertices[1:]):
        assert (q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2 == F(1, 9)
    assert ((vertices[-1][0] ** 2 + vertices[-1][1] ** 2)
            == chord * chord)
    # Re-derive coefficients from actual surface lengths and allocations.
    allocation = 2 * c / (1 + 2 * c)
    assert F(1, 2) * chord * allocation * F(1, 2) == width_mid / 12
    assert F(1, 2) * (F(1, 3) + chord) * F(1, 2) == complement_mid
    return c, s, chord, vertices, width_mid, complement_mid


def sampled_minimum(t, samples):
    c, s, *_ = exact_checks(t)
    cf, sf = float(c), float(s)
    theta = math.atan2(sf, cf)
    root3 = math.sqrt(3)
    gamma = np.linspace(0.0, math.pi, samples + 1)
    n0 = np.abs(np.sin(gamma))
    n1 = np.abs(np.sin(gamma + theta))
    n2 = np.abs(np.sin(gamma + 2 * theta))
    width = root3 / 24 + (n0 + n2 + 2 * cf * n1) / 12
    complement = (n0 + n2) / 12 + (1 + cf) * n1 / 6
    value = np.maximum(width, complement)
    k = int(np.argmin(value))
    return float(value[k]), float(gamma[k]), float(width[k]), float(complement[k])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-denominator", type=int, default=100)
    parser.add_argument("--samples", type=int, default=20000)
    parser.add_argument("--top", type=int, default=12)
    args = parser.parse_args()
    ranked = []
    seen = set()
    for q in range(2, args.max_denominator + 1):
        for p in range(1, q + 1):
            t = F(p, q)
            if t in seen or not F(1, 2) <= t <= F(9, 10):
                continue
            seen.add(t)
            value, gamma, width, complement = sampled_minimum(t, args.samples)
            ranked.append((value, t, gamma, width, complement))
    ranked.sort(reverse=True)
    for value, t, gamma, width, complement in ranked[:args.top]:
        c, s, chord, vertices, width_mid, complement_mid = exact_checks(t)
        print({
            "status": "numerical", "t": str(t), "cos": str(c), "sin": str(s),
            "closing_chord": str(chord), "width_mid_coefficient": str(width_mid),
            "complement_mid_coefficient": str(complement_mid),
            "sampled_minimum": value, "gamma_degrees": gamma * 180 / math.pi,
            "active_values": [width, complement],
            "vertices": [[str(x), str(y)] for x, y in vertices],
        })


if __name__ == "__main__":
    main()
