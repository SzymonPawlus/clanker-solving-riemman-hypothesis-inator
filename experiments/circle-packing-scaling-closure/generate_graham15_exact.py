#!/usr/bin/env python3
"""Graham's 15-cell complex (Figure 21) at its exact critical side, over Q(sqrt 3).

This measures the *pigeonhole ceiling* for n = 16: the best lower bound that any
cover argument with n - 1 = 15 cells can ever give. In the unit triangle Graham's
optimal 15-cell value is `D = 1/(1 + 2*sqrt 3)`, so the critical side is
`2/D = 2 + 4*sqrt(3) ~ 8.9282`.

Topology and parameterisation are Graham's Figure 21 as reconstructed in the
merged `experiments/circle-packing-partitions/generate_graham15.py` (recorded
there as `sketch`); the only change here is that the four parameters take their
exact algebraic values instead of ten-decimal rational stand-ins:

    D  = 1/(1 + 2 sqrt 3),  H = sqrt(3) D,  X = D / sqrt 3,
    P  = 1 - 3H/2 - X/2.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction

from covercheck import point_text, q3_text
from qsqrt3 import Q3

CRITICAL_SIDE = Q3(2, 4)  # 2 + 4*sqrt(3); equals 2/D
D = Q3(1, 2).inverse()
H = Q3(0, 1) * D
X = D * Q3(0, 1).inverse()
P = Q3(1, 0) - Q3(Fraction(3, 2), 0) * H - Q3(Fraction(1, 2), 0) * X

Bary = tuple[Q3, Q3, Q3]


def rotate(b: Bary) -> Bary:
    return (b[2], b[0], b[1])


def reflect(b: Bary) -> Bary:
    return (b[1], b[0], b[2])


def graham_fifteen_cell(side: Q3 = CRITICAL_SIDE) -> dict[str, object]:
    one, zero = Q3(1, 0), Q3(0, 0)
    two = Q3(2, 0)
    third = Q3(Fraction(1, 3), 0)
    if side.sign() <= 0:
        raise ValueError("side must be positive")
    if not (zero < X < D < P < H < Q3(Fraction(1, 2), 0) and P + X < one):
        raise ValueError("parameters are outside the Figure-21 topology")

    def scaled(b: Bary) -> tuple[Q3, Q3]:
        if b[0] + b[1] + b[2] != one:
            raise ValueError("barycentric coordinates must sum to one")
        return (side * b[1], side * b[2])

    vertices: dict[str, tuple[Q3, Q3]] = {
        "left": scaled((one, zero, zero)),
        "right": scaled((zero, one, zero)),
        "top": scaled((zero, zero, one)),
        "left_1": scaled((one - D, zero, D)),
        "left_2": scaled((one - H, zero, H)),
        "left_3": scaled((H, zero, one - H)),
        "left_4": scaled((D, zero, one - D)),
        "right_1": scaled((zero, one - D, D)),
        "right_2": scaled((zero, one - H, H)),
        "right_3": scaled((zero, H, one - H)),
        "right_4": scaled((zero, D, one - D)),
        "base_1": scaled((one - D, D, zero)),
        "base_2": scaled((one - H, H, zero)),
        "base_3": scaled((H, one - H, zero)),
        "base_4": scaled((D, one - D, zero)),
        "centroid": scaled((third, third, third)),
    }

    def add_orbit(names: tuple[str, str, str], start: Bary) -> None:
        value = start
        for name in names:
            vertices[name] = scaled(value)
            value = rotate(value)

    add_orbit(("top_junction", "left_junction", "right_junction"), (X, X, one - two * X))
    add_orbit(("top_inner", "left_inner", "right_inner"), (D, D, one - two * D))
    add_orbit(
        ("bottom_center", "upper_right_inner", "upper_left_inner"), (H, H, one - two * H)
    )
    scalene: Bary = (P, X, one - P - X)
    add_orbit(("upper_left", "lower_left", "middle_right"), scalene)
    add_orbit(("upper_right", "middle_left", "lower_right"), reflect(scalene))

    topology = [
        ("top", "left_4", "top_junction", "right_4"),
        ("left_4", "left_3", "upper_left", "top_inner", "top_junction"),
        ("right_4", "top_junction", "top_inner", "upper_right", "right_3"),
        ("left_3", "left_2", "middle_left", "upper_left_inner", "upper_left"),
        ("upper_left", "upper_left_inner", "centroid", "upper_right_inner",
         "upper_right", "top_inner"),
        ("right_3", "upper_right", "upper_right_inner", "middle_right", "right_2"),
        ("left_2", "left_1", "left_junction", "left_inner", "middle_left"),
        ("middle_left", "left_inner", "lower_left", "bottom_center", "centroid",
         "upper_left_inner"),
        ("centroid", "bottom_center", "lower_right", "right_inner", "middle_right",
         "upper_right_inner"),
        ("right_2", "middle_right", "right_inner", "right_junction", "right_1"),
        ("left", "base_1", "left_junction", "left_1"),
        ("base_1", "base_2", "lower_left", "left_inner", "left_junction"),
        ("base_2", "base_3", "lower_right", "bottom_center", "lower_left"),
        ("base_3", "base_4", "right_junction", "right_inner", "lower_right"),
        ("base_4", "right", "right_1", "right_junction"),
    ]

    return {
        "certificate_version": 1,
        "claim": "non-strict-cover" if side == CRITICAL_SIDE else "cover",
        "status": "numerical",
        "n": 16,
        "name": "graham15-exact",
        "triangle_side": q3_text(side),
        "coordinate_system": "oblique-euclidean-60deg",
        "parameters": {"D": q3_text(D), "H": q3_text(H), "X": q3_text(X), "P": q3_text(P)},
        "cells": [[point_text(vertices[name]) for name in cell] for cell in topology],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--side", default="2+4", help="'a+b' meaning a + b*sqrt(3)")
    args = parser.parse_args()
    a, _, b = args.side.partition("+")
    print(json.dumps(graham_fifteen_cell(Q3(Fraction(a), Fraction(b) if b else 0)), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
