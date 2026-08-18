#!/usr/bin/env python3
"""Generate exact regular-grid baselines for the first open cases n=16..19."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction

from generate_grid import grid_certificate, rational_text


Point = tuple[Fraction, Fraction]
Cell = list[Point]


def decode_cell(cell: list[list[str]]) -> Cell:
    return [(Fraction(point[0]), Fraction(point[1])) for point in cell]


def encode_cell(cell: Cell) -> list[list[str]]:
    return [[rational_text(u), rational_text(v)] for u, v in cell]


def split_triangle(cell: Cell) -> tuple[Cell, Cell]:
    if len(cell) != 3:
        raise ValueError("refinement expects a triangular cell")
    a, b, c = cell
    midpoint = ((b[0] + c[0]) / 2, (b[1] + c[1]) / 2)
    return [a, b, midpoint], [a, midpoint, c]


def open_baseline(n: int) -> dict[str, object]:
    """Return a deliberately simple exact baseline for 16 <= n <= 19."""
    if n not in (16, 17, 18, 19):
        raise ValueError("this bounded baseline supports n=16,17,18,19")

    if n == 16:
        # A 4-by-4 grid has 16 triangles. Merge its corner upward triangle
        # and adjacent downward triangle into one convex rhombus, leaving 15 cells.
        side = Fraction(2309, 500)  # 4.618 < 8/sqrt(3)
        data = grid_certificate(4, side)
        cells = [decode_cell(cell) for cell in data["cells"]]
        step = side / 4
        first_vertices = {(0, 0), (step, 0), (0, step)}
        second_vertices = {(step, 0), (step, step), (0, step)}
        first_index = next(i for i, cell in enumerate(cells) if set(cell) == first_vertices)
        second_index = next(i for i, cell in enumerate(cells) if set(cell) == second_vertices)
        remaining = [cell for i, cell in enumerate(cells) if i not in (first_index, second_index)]
        rhombus = [(0, 0), (step, 0), (step, step), (0, step)]
        cells = [rhombus] + remaining
    else:
        # The 16-cell regular grid already has the right count for n=17.
        # For n=18,19, bisect one or two upward triangles along a median.
        side = Fraction(7999, 1000)
        data = grid_certificate(4, side)
        cells = [decode_cell(cell) for cell in data["cells"]]
        for _ in range(n - 17):
            triangle = cells.pop(0)
            cells.extend(split_triangle(triangle))

    return {
        "certificate_version": 1,
        "claim": "strict-lower-bound",
        "status": "numerical",
        "n": n,
        "triangle_side": rational_text(side),
        "coordinate_system": "oblique-euclidean-60deg",
        "cells": [encode_cell(cell) for cell in cells],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("n", type=int, choices=(16, 17, 18, 19))
    args = parser.parse_args()
    print(json.dumps(open_baseline(args.n), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
