#!/usr/bin/env python3
"""Numerical landscape for whole-boundary allocations to base witnesses."""

from __future__ import annotations

import math
import random


SQRT3 = math.sqrt(3.0)
TRIANGLE = ((0.0, 0.0), (0.5, 0.0), (0.25, SQRT3 / 4.0))
TARGET = 0.2346746732371


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def hull(points):
    ordered = sorted(set(points))
    lower = []
    for p in ordered:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(ordered):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def edges(poly):
    return [(poly[(i + 1) % len(poly)][0] - p[0],
             poly[(i + 1) % len(poly)][1] - p[1]) for i, p in enumerate(poly)]


def width(poly, phi):
    u = (math.cos(phi), math.sin(phi))
    vals = [x * u[0] + y * u[1] for x, y in poly]
    return max(vals) - min(vals)


def triangle_mixed(poly, psi):
    cp, sp = math.cos(psi), math.sin(psi)
    value = 0.0
    for ex, ey in edges(poly):
        length = math.hypot(ex, ey)
        # CCW polygon: outward normal is the clockwise edge rotation.
        nx, ny = ey / length, -ex / length
        # Rotate normal into the triangle's frame.
        qx, qy = cp * nx + sp * ny, -sp * nx + cp * ny
        support = max(x * qx + y * qy for x, y in TRIANGLE)
        value += length * support / 2.0
    return value


def score(poly, samples=720):
    mw = min(width(poly, math.pi * k / samples) for k in range(samples)) / 2.0
    # A direct-motion equilateral triangle has orientation period 2*pi/3.
    mt = min(triangle_mixed(poly, 2 * math.pi * k / (3 * samples)) for k in range(samples))
    return max(mw, mt), mw, mt


def main():
    rng = random.Random(178_2)
    records = []
    for trial in range(200_000):
        raw = sorted(rng.uniform(-1.55, 1.55) for _ in range(4))
        cuts = sorted([0.0] + [rng.random() for _ in range(3)] + [1.0])
        lens = [cuts[i + 1] - cuts[i] for i in range(4)]
        pts = [(0.0, 0.0)]
        for a, l in zip(raw, lens):
            pts.append((pts[-1][0] + l * math.cos(a), pts[-1][1] + l * math.sin(a)))
        poly = hull(pts)
        if len(poly) != 5:
            continue
        value, mw, mt = score(poly, 180)
        row = (value, mw, mt, tuple(raw), tuple(lens), tuple(pts))
        if len(records) < 20 or value > records[0][0]:
            records.append(row)
            records.sort()
            records = records[-20:]
        if trial % 20_000 == 0 and records:
            print(trial, records[-1][:-1], "delta", records[-1][0] - TARGET, flush=True)
    print("FINAL")
    for row in reversed(records):
        print(row, "delta", row[0] - TARGET)


if __name__ == "__main__":
    main()
