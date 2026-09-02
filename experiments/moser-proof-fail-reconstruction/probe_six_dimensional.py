#!/usr/bin/env python3
"""Numerical clean-room probe of the public Proof.Fail six-variable description.

This is candidate evidence only.  It neither reads nor verifies the unavailable
Proof.Fail checker/certificate and it performs no interval arithmetic.
"""

from __future__ import annotations

import argparse
import json
import math

import numpy as np


SQRT3 = math.sqrt(3.0)
SEGMENT = [(0.0, 0.0), (1.0, 0.0)]
TRIANGLE = [(0.0, SQRT3 / 6.0), (-0.25, -SQRT3 / 12.0),
            (0.25, -SQRT3 / 12.0)]
RECTANGLE = [(-0.25, -0.125), (0.25, -0.125),
             (0.25, 0.125), (-0.25, 0.125)]


def transform(points: list[tuple[float, float]], tx: float, ty: float,
              angle: float) -> list[tuple[float, float]]:
    c, s = math.cos(angle), math.sin(angle)
    return [(tx + c * x - s * y, ty + s * x + c * y)
            for x, y in points]


def hull(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    points = sorted(set(points))

    def cross(o: tuple[float, float], a: tuple[float, float],
              b: tuple[float, float]) -> float:
        return ((a[0] - o[0]) * (b[1] - o[1])
                - (a[1] - o[1]) * (b[0] - o[0]))

    lower: list[tuple[float, float]] = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper: list[tuple[float, float]] = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def area(polygon: list[tuple[float, float]]) -> float:
    return abs(sum(
        polygon[i][0] * polygon[(i + 1) % len(polygon)][1]
        - polygon[i][1] * polygon[(i + 1) % len(polygon)][0]
        for i in range(len(polygon))
    )) / 2.0


def objective(x: np.ndarray, breadth: float) -> tuple[float, float, float]:
    """Return max(actual L/T/R hull area, KPS broadworm-width lower bound).

    Variables are triangle (tx, ty, theta) and rectangle (tx, ty, theta).
    For a rectangle whose long side has angle rho to the pinned unit segment,
    Proposition 3.4's breadth term becomes b/4 + |cos(rho)|/8.
    """
    t = transform(TRIANGLE, x[0], x[1], x[2])
    r = transform(RECTANGLE, x[3], x[4], x[5])
    hull_area = area(hull(SEGMENT + t + r))
    breadth_bound = breadth / 4.0 + abs(math.cos(x[5])) / 8.0
    return max(hull_area, breadth_bound), hull_area, breadth_bound


def run(seed: int, samples: int, restarts: int,
        breadth: float) -> dict[str, object]:
    rng = np.random.default_rng(seed)
    best_value = math.inf
    best_x: np.ndarray | None = None

    # The translation window is only a candidate-search window, not a proved
    # compact domain.  It comfortably contains the basin found in this probe.
    for _ in range(samples):
        x = np.r_[rng.uniform(-0.1, 1.1, 2),
                  rng.uniform(0.0, 2.0 * math.pi),
                  rng.uniform(-0.1, 1.1, 2),
                  rng.uniform(0.0, math.pi)]
        value = objective(x, breadth)[0]
        if value < best_value:
            best_value, best_x = value, x.copy()

    assert best_x is not None
    scales0 = np.array([0.03, 0.03, 0.08, 0.03, 0.03, 0.08])
    for restart in range(restarts):
        x = (best_x.copy() if restart == 0
             else best_x + rng.normal(0.0, scales0))
        x[2] %= 2.0 * math.pi
        x[5] %= math.pi
        value = objective(x, breadth)[0]
        scales = scales0.copy()
        while float(np.max(scales)) > 2.0e-9:
            candidates: list[np.ndarray] = []
            for j in range(6):
                for sign in (-1.0, 1.0):
                    y = x.copy()
                    y[j] += sign * scales[j]
                    y[2] %= 2.0 * math.pi
                    y[5] %= math.pi
                    candidates.append(y)
            for _ in range(16):
                y = x + rng.uniform(-1.0, 1.0, 6) * scales
                y[2] %= 2.0 * math.pi
                y[5] %= math.pi
                candidates.append(y)
            values = [objective(y, breadth)[0] for y in candidates]
            k = int(np.argmin(values))
            if values[k] < value:
                x, value = candidates[k], values[k]
                if value < best_value:
                    best_value, best_x = value, x.copy()
            else:
                scales *= 0.55

    value, hull_area, breadth_bound = objective(best_x, breadth)
    return {
        "status": "numerical",
        "interpretation": "clean-room plausible six-dimensional objective",
        "seed": seed,
        "samples": samples,
        "restarts": restarts,
        "breadth_input": breadth,
        "best_objective": value,
        "hull_area": hull_area,
        "breadth_bound": breadth_bound,
        "variables": {
            "triangle_tx": float(best_x[0]),
            "triangle_ty": float(best_x[1]),
            "triangle_angle_radians": float(best_x[2]),
            "rectangle_tx": float(best_x[3]),
            "rectangle_ty": float(best_x[4]),
            "rectangle_angle_radians": float(best_x[5]),
        },
        "warning": "local floating-point search; not a lower-bound proof",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=5)
    parser.add_argument("--samples", type=int, default=50_000)
    parser.add_argument("--restarts", type=int, default=15)
    parser.add_argument("--breadth", type=float, default=0.4389)
    args = parser.parse_args()
    print(json.dumps(run(args.seed, args.samples, args.restarts,
                         args.breadth), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
