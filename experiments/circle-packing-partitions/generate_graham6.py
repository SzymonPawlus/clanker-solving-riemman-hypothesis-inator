#!/usr/bin/env python3
"""Generate a rationalized version of Graham's six-cell partition (Figure 7)."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction

from generate_grid import point, rational_text


DEFAULT_SIDE = Fraction(683, 125)  # 5.464 < 2 + 2 sqrt(3)
DEFAULT_DELTA = Fraction(1_830_127, 5_000_000)  # 0.3660254 ~ 1/(1+sqrt(3))
DEFAULT_R = Fraction(2_113_249, 10_000_000)  # 0.2113249 ~ delta/sqrt(3)


def graham_six_cell_certificate(
    side: Fraction = DEFAULT_SIDE,
    delta: Fraction = DEFAULT_DELTA,
    r: Fraction = DEFAULT_R,
) -> dict[str, object]:
    """Return the symmetric six-cell topology in rational oblique coordinates.

    `delta` and `r` are normalized to a unit outer triangle. The ideal algebraic
    values are delta=1/(1+sqrt(3)) and r=delta/sqrt(3). This function deliberately
    accepts rational inward approximations and lets partitioncheck.py decide whether
    the resulting certificate is valid.
    """
    if side <= 0:
        raise ValueError("side must be positive")
    if not (0 < r < delta < Fraction(1, 2)):
        raise ValueError("expected 0 < r < delta < 1/2")

    def scaled(u: Fraction, v: Fraction) -> list[str]:
        return point(side * u, side * v)

    vertices = {
        "left": scaled(0, 0),
        "right": scaled(1, 0),
        "top": scaled(0, 1),
        "upper_left": scaled(0, 1 - delta),
        "upper_right": scaled(delta, 1 - delta),
        "lower_left": scaled(0, delta),
        "lower_right": scaled(1 - delta, delta),
        "base_left": scaled(delta, 0),
        "base_right": scaled(1 - delta, 0),
        "upper_center": scaled(r, 1 - 2 * r),
        "center": scaled(Fraction(1, 3), Fraction(1, 3)),
        "inner_left": scaled(r, r),
        "inner_right": scaled(1 - 2 * r, r),
    }

    def cell(*names: str) -> list[list[str]]:
        return [vertices[name] for name in names]

    cells = [
        cell("top", "upper_left", "upper_center", "upper_right"),
        cell("upper_left", "lower_left", "inner_left", "center", "upper_center"),
        cell("upper_right", "upper_center", "center", "inner_right", "lower_right"),
        cell("left", "base_left", "inner_left", "lower_left"),
        cell("base_left", "base_right", "inner_right", "center", "inner_left"),
        cell("right", "lower_right", "inner_right", "base_right"),
    ]
    return {
        "certificate_version": 1,
        "claim": "strict-lower-bound",
        "status": "numerical",
        "n": 7,
        "triangle_side": rational_text(side),
        "coordinate_system": "oblique-euclidean-60deg",
        "cells": cells,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--side", default=rational_text(DEFAULT_SIDE))
    parser.add_argument("--delta", default=rational_text(DEFAULT_DELTA))
    parser.add_argument("--r", default=rational_text(DEFAULT_R))
    args = parser.parse_args()
    try:
        certificate = graham_six_cell_certificate(
            Fraction(args.side), Fraction(args.delta), Fraction(args.r)
        )
    except (ValueError, ZeroDivisionError) as error:
        parser.error(str(error))
    print(json.dumps(certificate, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
