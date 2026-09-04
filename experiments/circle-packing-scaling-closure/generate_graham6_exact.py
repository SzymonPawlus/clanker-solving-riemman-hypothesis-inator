#!/usr/bin/env python3
"""Emit Graham's six-cell complex at the *exact* critical side, over Q(sqrt 3).

Proposal J's pilot question for n = 7: at exactly `d* = 2 + 2*sqrt(3)`, does the
Figure-7 six-cell complex have every cell diameter `<= 2`?

The topology (which vertex belongs to which cell) is Graham's; the two-parameter
coordinate reconstruction follows the merged rational generator
`experiments/circle-packing-partitions/generate_graham6.py`, which records it as
`sketch`. What is new here is that `delta` and `r` are their exact algebraic
values rather than ten-decimal rational stand-ins, so the certificate can be
placed at `d*` itself instead of `d* - 1e-4`.

    delta = 1/(1 + sqrt 3) = (sqrt(3) - 1)/2
    r     = delta / sqrt 3 = (3 - sqrt 3)/6

Coordinates are the oblique ones described in `covercheck.py`, scaled by the
side; nothing here is rounded.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction

from covercheck import point_text, q3_text
from qsqrt3 import Q3

CRITICAL_SIDE = Q3(2, 2)  # d* = 2 + 2*sqrt(3), the cited d(7)
DELTA = Q3(1, 1).inverse()  # 1/(1 + sqrt 3)
R = DELTA * Q3(0, 1).inverse()  # delta / sqrt 3


def graham_six_cell(side: Q3, delta: Q3 = DELTA, r: Q3 = R) -> dict[str, object]:
    if side.sign() <= 0:
        raise ValueError("side must be positive")
    if not (Q3(0, 0) < r < delta < Q3(Fraction(1, 2), 0)):
        raise ValueError("expected 0 < r < delta < 1/2 in the unit normalisation")

    one = Q3(1, 0)
    third = Q3(Fraction(1, 3), 0)

    def scaled(u: Q3, v: Q3) -> tuple[Q3, Q3]:
        return (side * u, side * v)

    vertices = {
        "left": scaled(Q3(0, 0), Q3(0, 0)),
        "right": scaled(one, Q3(0, 0)),
        "top": scaled(Q3(0, 0), one),
        "upper_left": scaled(Q3(0, 0), one - delta),
        "upper_right": scaled(delta, one - delta),
        "lower_left": scaled(Q3(0, 0), delta),
        "lower_right": scaled(one - delta, delta),
        "base_left": scaled(delta, Q3(0, 0)),
        "base_right": scaled(one - delta, Q3(0, 0)),
        "upper_center": scaled(r, one - Q3(2, 0) * r),
        "center": scaled(third, third),
        "inner_left": scaled(r, r),
        "inner_right": scaled(one - Q3(2, 0) * r, r),
    }

    topology = [
        ("top", "upper_left", "upper_center", "upper_right"),
        ("upper_left", "lower_left", "inner_left", "center", "upper_center"),
        ("upper_right", "upper_center", "center", "inner_right", "lower_right"),
        ("left", "base_left", "inner_left", "lower_left"),
        ("base_left", "base_right", "inner_right", "center", "inner_left"),
        ("right", "lower_right", "inner_right", "base_right"),
    ]

    return {
        "certificate_version": 1,
        "claim": "non-strict-cover" if side == CRITICAL_SIDE else "cover",
        "status": "numerical",
        "n": 7,
        "name": "graham6-exact",
        "triangle_side": q3_text(side),
        "coordinate_system": "oblique-euclidean-60deg",
        "parameters": {"delta": q3_text(delta), "r": q3_text(r)},
        "cells": [[point_text(vertices[name]) for name in cell] for cell in topology],
    }


def parse_side(text: str) -> Q3:
    a, _, b = text.partition("+")
    return Q3(Fraction(a), Fraction(b) if b else 0)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--side",
        default="2+2",
        help="side as 'a+b' meaning a + b*sqrt(3); default '2+2' is d* = 2 + 2*sqrt(3)",
    )
    args = parser.parse_args()
    print(json.dumps(graham_six_cell(parse_side(args.side)), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
