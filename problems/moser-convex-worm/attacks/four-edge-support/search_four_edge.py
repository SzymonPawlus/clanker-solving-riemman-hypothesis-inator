#!/usr/bin/env python3
"""Exploratory search for four-edge arcs with one closure-parallel edge.

Floating point is used only to locate candidates.  Nothing accepted by this
script is a certificate.
"""

from __future__ import annotations

import math
import random


H = math.sqrt(3.0) / 4.0
TARGET = 0.2346746732371


def floor_for(angles: tuple[float, ...], lengths: tuple[float, ...], samples: int = 4096):
    resultant = sum(l * math.cos(a) for a, l in zip(angles, lengths))
    horizontal = lengths[2]
    if resultant < horizontal:
        return -1.0, 0.0
    # On intervals cut out by projection zeros and C=W, the selected envelope
    # is a positive sine combination, hence concave.  Its minimum is at a cut.
    delta = math.asin(H)
    cuts = {0.0, math.pi, delta, math.pi - delta}
    for angle in angles:
        cuts.add(angle % math.pi)
    best = 1.0
    arg = 0.0
    for phi in cuts:
        projections = [l * abs(math.sin(a - phi)) for a, l in zip(angles, lengths)]
        close = resultant * abs(math.sin(phi))
        segment = (sum(projections) + close) / 4.0
        residual = (sum(projections[:2]) + sum(projections[3:])
                    + (resultant - horizontal) * abs(math.sin(phi))) / 4.0
        triangle = horizontal * H / 2.0 + residual
        value = max(segment, triangle)
        if value < best:
            best, arg = value, phi
    return best, arg


def main() -> None:
    rng = random.Random(178)
    records: list[tuple[float, tuple[float, ...], tuple[float, ...], float]] = []
    for trial in range(600_000):
        beta = rng.uniform(0.15, 1.55)
        alpha = rng.uniform(0.01, beta - 0.005)
        gamma = rng.uniform(0.05, 1.55)
        l1 = rng.uniform(0.01, 0.45)
        l2 = rng.uniform(0.01, 0.45)
        l4 = (l1 * math.sin(beta) + l2 * math.sin(alpha)) / math.sin(gamma)
        l0 = 1.0 - l1 - l2 - l4
        if l0 <= 0.005 or l4 <= 0.005:
            continue
        angles = (-beta, -alpha, 0.0, gamma)
        lengths = (l1, l2, l0, l4)
        value, arg = floor_for(angles, lengths, 512)
        if len(records) < 20 or value > records[0][0]:
            records.append((value, angles, lengths, arg))
            records.sort()
            records = records[-20:]
        if trial % 50_000 == 0 and records:
            print(trial, records[-1], "delta", records[-1][0] - TARGET, flush=True)
    print("FINAL")
    for row in reversed(records):
        print(row, "delta", row[0] - TARGET)


if __name__ == "__main__":
    main()
