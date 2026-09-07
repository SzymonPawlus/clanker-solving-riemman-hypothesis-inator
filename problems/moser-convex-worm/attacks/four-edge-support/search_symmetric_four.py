#!/usr/bin/env python3
"""Focused numerical search of symmetric genuine four-direction arcs."""

from __future__ import annotations

import math
import random

from search_cycle_allocations import score
from search_full_triangle import hull


TARGET = 0.2346746732371


def polygon(beta, alpha, p):
    q = 0.5 - p
    angles = (-beta, -alpha, alpha, beta)
    lengths = (p, q, q, p)
    pts = [(0.0, 0.0)]
    for a, ll in zip(angles, lengths):
        pts.append((pts[-1][0] + ll * math.cos(a),
                    pts[-1][1] + ll * math.sin(a)))
    return hull(pts), angles, lengths, pts


def main():
    rng = random.Random(178_6)
    records = []
    for trial in range(300_000):
        beta = rng.uniform(0.8, 1.56)
        alpha = rng.uniform(0.01, beta - 0.001)
        p = rng.uniform(0.005, 0.495)
        poly, angles, lengths, pts = polygon(beta, alpha, p)
        if len(poly) != 5:
            continue
        value, arg, _ = score(poly, 240)
        row = (value, beta, alpha, p, arg, tuple(pts))
        if len(records) < 20 or value > records[0][0]:
            records.append(row)
            records.sort()
            records = records[-20:]
        if trial and trial % 25_000 == 0:
            print(trial, records[-1][:-1], "delta", records[-1][0] - TARGET, flush=True)
    print("FINAL")
    for row in reversed(records):
        print(row, "delta", row[0] - TARGET)


if __name__ == "__main__":
    main()
