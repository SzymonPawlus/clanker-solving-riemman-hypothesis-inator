#!/usr/bin/env python3
"""Generate exact regular-triangular-grid partition certificates."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction


def rational_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def point(u: Fraction, v: Fraction) -> list[str]:
    return [rational_text(u), rational_text(v)]


def grid_certificate(m: int, side: Fraction) -> dict[str, object]:
    """Partition a side-`side` triangle into `m^2` triangles of side `side/m`."""
    if isinstance(m, bool) or not isinstance(m, int) or m < 1:
        raise ValueError("m must be a positive integer")
    if side <= 0:
        raise ValueError("side must be positive")
    step = side / m
    cells: list[list[list[str]]] = []

    # Upward small triangles.
    for i in range(m):
        for j in range(m - i):
            cells.append(
                [
                    point(i * step, j * step),
                    point((i + 1) * step, j * step),
                    point(i * step, (j + 1) * step),
                ]
            )

    # Downward small triangles.
    for i in range(m - 1):
        for j in range(m - 1 - i):
            cells.append(
                [
                    point((i + 1) * step, j * step),
                    point((i + 1) * step, (j + 1) * step),
                    point(i * step, (j + 1) * step),
                ]
            )

    assert len(cells) == m * m
    return {
        "certificate_version": 1,
        "claim": "strict-lower-bound",
        "status": "numerical",
        "n": m * m + 1,
        "triangle_side": rational_text(side),
        "coordinate_system": "oblique-euclidean-60deg",
        "cells": cells,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("m", type=int, help="grid frequency; emits m^2 cells for n=m^2+1")
    parser.add_argument(
        "--epsilon",
        default="1/1000",
        help="positive rational gap below side 2m (default: 1/1000)",
    )
    args = parser.parse_args()
    try:
        epsilon = Fraction(args.epsilon)
    except (ValueError, ZeroDivisionError) as error:
        parser.error(f"invalid rational epsilon: {error}")
    if epsilon <= 0 or epsilon >= 2 * args.m:
        parser.error("epsilon must satisfy 0 < epsilon < 2m")
    certificate = grid_certificate(args.m, Fraction(2 * args.m) - epsilon)
    print(json.dumps(certificate, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
