#!/usr/bin/env python3
"""Generate rational certificates from Graham's 15-cell partition (Figure 21)."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction

from generate_grid import point, rational_text


DEFAULT_SIDE = Fraction(1116, 125)  # 8.928 < 2 + 4 sqrt(3)
DEFAULT_D = Fraction(2_240_092_377, 10_000_000_000)
DEFAULT_SQRT3_D = Fraction(3_879_953_811, 10_000_000_000)
DEFAULT_D_OVER_SQRT3 = Fraction(1_293_317_937, 10_000_000_000)
DEFAULT_P = Fraction(3_533_410_314, 10_000_000_000)


BarycentricPoint = tuple[Fraction, Fraction, Fraction]


def rotate(barycentric: BarycentricPoint) -> BarycentricPoint:
    """Rotate 120 degrees, sending the top vertex to the left vertex."""
    a, b, c = barycentric
    return c, a, b


def reflect(barycentric: BarycentricPoint) -> BarycentricPoint:
    """Reflect across the vertical altitude."""
    a, b, c = barycentric
    return b, a, c


def graham_fifteen_cell_certificate(
    n: int = 16,
    side: Fraction = DEFAULT_SIDE,
    d: Fraction = DEFAULT_D,
    sqrt3_d: Fraction = DEFAULT_SQRT3_D,
    d_over_sqrt3: Fraction = DEFAULT_D_OVER_SQRT3,
    p: Fraction = DEFAULT_P,
) -> dict[str, object]:
    """Return Figure 21, with up to three corner cells bisected.

    In the ideal normalized construction, ``d=1/(1+2*sqrt(3))``,
    ``sqrt3_d=sqrt(3)*d``, ``d_over_sqrt3=d/sqrt(3)``, and
    ``p=1-3*sqrt3_d/2-d_over_sqrt3/2``.  Rational approximations are
    deliberately supplied independently; the exact checker is the authority.
    """
    if n not in (16, 17, 18, 19):
        raise ValueError("Figure-21 certificates support n=16,17,18,19")
    if side <= 0:
        raise ValueError("side must be positive")
    if not (
        0 < d_over_sqrt3 < d < p < sqrt3_d < Fraction(1, 2)
        and p + d_over_sqrt3 < 1
    ):
        raise ValueError("parameters are outside the Figure-21 topology")

    def scaled(barycentric: BarycentricPoint) -> list[str]:
        a, b, c = barycentric
        if a + b + c != 1:
            raise ValueError("barycentric coordinates must sum to one")
        return point(side * b, side * c)

    vertices: dict[str, list[str]] = {
        "left": scaled((1, 0, 0)),
        "right": scaled((0, 1, 0)),
        "top": scaled((0, 0, 1)),
        "left_1": scaled((1 - d, 0, d)),
        "left_2": scaled((1 - sqrt3_d, 0, sqrt3_d)),
        "left_3": scaled((sqrt3_d, 0, 1 - sqrt3_d)),
        "left_4": scaled((d, 0, 1 - d)),
        "right_1": scaled((0, 1 - d, d)),
        "right_2": scaled((0, 1 - sqrt3_d, sqrt3_d)),
        "right_3": scaled((0, sqrt3_d, 1 - sqrt3_d)),
        "right_4": scaled((0, d, 1 - d)),
        "base_1": scaled((1 - d, d, 0)),
        "base_2": scaled((1 - sqrt3_d, sqrt3_d, 0)),
        "base_3": scaled((sqrt3_d, 1 - sqrt3_d, 0)),
        "base_4": scaled((d, 1 - d, 0)),
        "centroid": scaled((Fraction(1, 3),) * 3),
    }

    def add_orbit(names: tuple[str, str, str], start: BarycentricPoint) -> None:
        value = start
        for name in names:
            vertices[name] = scaled(value)
            value = rotate(value)

    add_orbit(
        ("top_junction", "left_junction", "right_junction"),
        (d_over_sqrt3, d_over_sqrt3, 1 - 2 * d_over_sqrt3),
    )
    add_orbit(
        ("top_inner", "left_inner", "right_inner"),
        (d, d, 1 - 2 * d),
    )
    add_orbit(
        ("bottom_center", "upper_right_inner", "upper_left_inner"),
        (sqrt3_d, sqrt3_d, 1 - 2 * sqrt3_d),
    )
    scalene = (p, d_over_sqrt3, 1 - p - d_over_sqrt3)
    add_orbit(("upper_left", "lower_left", "middle_right"), scalene)
    add_orbit(
        ("upper_right", "middle_left", "lower_right"), reflect(scalene)
    )

    def cell(*names: str) -> list[list[str]]:
        return [vertices[name] for name in names]

    cells = [
        cell("top", "left_4", "top_junction", "right_4"),
        cell("left_4", "left_3", "upper_left", "top_inner", "top_junction"),
        cell("right_4", "top_junction", "top_inner", "upper_right", "right_3"),
        cell("left_3", "left_2", "middle_left", "upper_left_inner", "upper_left"),
        cell(
            "upper_left",
            "upper_left_inner",
            "centroid",
            "upper_right_inner",
            "upper_right",
            "top_inner",
        ),
        cell("right_3", "upper_right", "upper_right_inner", "middle_right", "right_2"),
        cell("left_2", "left_1", "left_junction", "left_inner", "middle_left"),
        cell(
            "middle_left",
            "left_inner",
            "lower_left",
            "bottom_center",
            "centroid",
            "upper_left_inner",
        ),
        cell(
            "centroid",
            "bottom_center",
            "lower_right",
            "right_inner",
            "middle_right",
            "upper_right_inner",
        ),
        cell("right_2", "middle_right", "right_inner", "right_junction", "right_1"),
        cell("left", "base_1", "left_junction", "left_1"),
        cell("base_1", "base_2", "lower_left", "left_inner", "left_junction"),
        cell("base_2", "base_3", "lower_right", "bottom_center", "lower_left"),
        cell("base_3", "base_4", "right_junction", "right_inner", "lower_right"),
        cell("base_4", "right", "right_1", "right_junction"),
    ]

    # Each diagonal subdivision preserves the parent cell's diameter.  The three
    # corner quadrilaterals form a symmetry orbit and supply 16, 17, or 18 cells.
    for index in sorted((0, 10, 14)[: n - 16], reverse=True):
        quadrilateral = cells.pop(index)
        a, b, c, d_vertex = quadrilateral
        cells.extend(([a, b, c], [a, c, d_vertex]))

    return {
        "certificate_version": 1,
        "claim": "strict-lower-bound",
        "status": "numerical",
        "n": n,
        "triangle_side": rational_text(side),
        "coordinate_system": "oblique-euclidean-60deg",
        "cells": cells,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("n", nargs="?", type=int, choices=(16, 17, 18, 19), default=16)
    parser.add_argument("--side", default=rational_text(DEFAULT_SIDE))
    args = parser.parse_args()
    try:
        certificate = graham_fifteen_cell_certificate(n=args.n, side=Fraction(args.side))
    except (ValueError, ZeroDivisionError) as error:
        parser.error(str(error))
    print(json.dumps(certificate, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
