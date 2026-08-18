#!/usr/bin/env python3
"""Deterministic fixed-topology search for Graham's symmetric six-cell partition."""

from __future__ import annotations

import argparse
import json
import math
from itertools import combinations


FloatPoint = tuple[float, float]
FloatPolygon = list[FloatPoint]


def squared_distance(a: FloatPoint, b: FloatPoint) -> float:
    du, dv = a[0] - b[0], a[1] - b[1]
    return du * du + du * dv + dv * dv


def cross(a: FloatPoint, b: FloatPoint, c: FloatPoint) -> float:
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def normalized_cells(delta: float, r: float) -> list[FloatPolygon]:
    """The Figure-7 planar complex in a unit outer triangle."""
    vertices = {
        "left": (0.0, 0.0),
        "right": (1.0, 0.0),
        "top": (0.0, 1.0),
        "upper_left": (0.0, 1.0 - delta),
        "upper_right": (delta, 1.0 - delta),
        "lower_left": (0.0, delta),
        "lower_right": (1.0 - delta, delta),
        "base_left": (delta, 0.0),
        "base_right": (1.0 - delta, 0.0),
        "upper_center": (r, 1.0 - 2.0 * r),
        "center": (1.0 / 3.0, 1.0 / 3.0),
        "inner_left": (r, r),
        "inner_right": (1.0 - 2.0 * r, r),
    }

    def cell(*names: str) -> FloatPolygon:
        return [vertices[name] for name in names]

    return [
        cell("top", "upper_left", "upper_center", "upper_right"),
        cell("upper_left", "lower_left", "inner_left", "center", "upper_center"),
        cell("upper_right", "upper_center", "center", "inner_right", "lower_right"),
        cell("left", "base_left", "inner_left", "lower_left"),
        cell("base_left", "base_right", "inner_right", "center", "inner_left"),
        cell("right", "lower_right", "inner_right", "base_right"),
    ]


def objective(delta: float, r: float) -> float:
    if not (0.0 < r < delta < 0.5):
        return math.inf
    cells = normalized_cells(delta, r)
    if any(
        cross(cell[i - 1], cell[i], cell[(i + 1) % len(cell)]) <= 1e-14
        for cell in cells
        for i in range(len(cell))
    ):
        return math.inf
    return max(
        squared_distance(a, b)
        for cell in cells
        for a, b in combinations(cell, 2)
    )


def pattern_search(
    start_delta: float = 0.35,
    start_r: float = 0.20,
    initial_step: float = 0.05,
    tolerance: float = 1e-12,
) -> tuple[float, float, float, int]:
    """Minimize the maximum squared diameter over this two-parameter topology.

    The objective is nonsmooth where two candidate diameters exchange roles. A
    one-coordinate-at-a-time search can therefore stick on a ridge. At each scale
    we inspect a 9-by-9 stencil, then quarter the mesh.
    """
    delta, r = start_delta, start_r
    value = objective(delta, r)
    if not math.isfinite(value):
        raise ValueError("starting point is outside the valid topology")
    step = initial_step
    evaluations = 1
    while step > tolerance:
        candidates: list[tuple[float, float, float]] = []
        for delta_direction in range(-4, 5):
            for r_direction in range(-4, 5):
                candidate_delta = delta + delta_direction * step
                candidate_r = r + r_direction * step
                candidate_value = objective(candidate_delta, candidate_r)
                evaluations += 1
                candidates.append((candidate_value, candidate_delta, candidate_r))
        value, delta, r = min(candidates)
        step /= 4.0
    return delta, r, value, evaluations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--delta", type=float, default=0.35)
    parser.add_argument("--r", type=float, default=0.20)
    args = parser.parse_args()
    delta, r, value, evaluations = pattern_search(args.delta, args.r)
    ideal_delta = 1.0 / (1.0 + math.sqrt(3.0))
    ideal_r = ideal_delta / math.sqrt(3.0)
    print(
        json.dumps(
            {
                "status": "numerical",
                "topology": "Graham 1967 Figure 7, six cells",
                "delta": delta,
                "r": r,
                "maximum_squared_diameter_unit_triangle": value,
                "implied_scale_limit": 2.0 / math.sqrt(value),
                "evaluations": evaluations,
                "reference": {
                    "delta": ideal_delta,
                    "r": ideal_r,
                    "maximum_squared_diameter": ideal_delta * ideal_delta,
                    "scale_limit": 2.0 * (1.0 + math.sqrt(3.0)),
                },
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
