#!/usr/bin/env python3
"""Explore maximal balanced three-edge allocations of four-edge arc hulls.

This is a floating-point candidate locator, not a verifier.
"""

from __future__ import annotations

import itertools
import math
import random

from search_full_triangle import TRIANGLE, edges, hull


TARGET = 0.2346746732371


def support_triangle(nx, ny, psi):
    cp, sp = math.cos(psi), math.sin(psi)
    qx, qy = cp * nx + sp * ny, -sp * nx + cp * ny
    return max(x * qx + y * qy for x, y in TRIANGLE)


def cycles(poly, triangle_samples=60):
    data = []
    for ex, ey in edges(poly):
        ll = math.hypot(ex, ey)
        data.append((ll, ex / ll, ey / ll))
    ans = []
    for inds in itertools.combinations(range(len(data)), 3):
        units = [(data[i][1], data[i][2]) for i in inds]
        raw = []
        for j in range(3):
            a = units[(j + 1) % 3]
            b = units[(j + 2) % 3]
            raw.append(a[0] * b[1] - a[1] * b[0])
        if not (all(x > 1e-10 for x in raw) or all(x < -1e-10 for x in raw)):
            continue
        raw = [abs(x) for x in raw]
        scale = min(data[i][0] / x for i, x in zip(inds, raw))
        alloc = [0.0] * len(data)
        for i, x in zip(inds, raw):
            alloc[i] = scale * x
        # Minimize the triangle contribution over its full direct orientation.
        q = 1.0
        for k in range(triangle_samples):
            psi = 2 * math.pi * k / (3 * triangle_samples)
            val = 0.0
            for x, (_, ux, uy) in zip(alloc, data):
                # outward normal is clockwise rotation of the CCW tangent
                val += x * support_triangle(uy, -ux, psi) / 2.0
            q = min(q, val)
        ans.append((alloc, q, inds))
    return data, ans


def score(poly, samples=360, triangle_samples=60):
    data, allocs = cycles(poly, triangle_samples)
    best = 1.0
    arg = None
    for k in range(samples):
        phi = math.pi * k / samples
        absproj = [abs(uy * math.cos(phi) - ux * math.sin(phi))
                   for _, ux, uy in data]
        full = sum(ll * p for (ll, _, _), p in zip(data, absproj)) / 4.0
        value = full
        label = ("segment",)
        for alloc, q, inds in allocs:
            candidate = q + sum((ll - x) * p for (ll, _, _), x, p
                                in zip(data, alloc, absproj)) / 4.0
            if candidate > value:
                value, label = candidate, inds
        if value < best:
            best, arg = value, (phi, label, full)
    return best, arg, allocs


def main():
    rng = random.Random(178_3)
    records = []
    for trial in range(60_000):
        angles = sorted(rng.uniform(-1.55, 1.55) for _ in range(4))
        cuts = sorted([0.0] + [rng.random() for _ in range(3)] + [1.0])
        lens = [cuts[i + 1] - cuts[i] for i in range(4)]
        pts = [(0.0, 0.0)]
        for a, ll in zip(angles, lens):
            pts.append((pts[-1][0] + ll * math.cos(a), pts[-1][1] + ll * math.sin(a)))
        poly = hull(pts)
        if len(poly) != 5:
            continue
        value, arg, allocs = score(poly, 180)
        row = (value, tuple(angles), tuple(lens), arg, tuple(pts))
        if len(records) < 20 or value > records[0][0]:
            records.append(row)
            records.sort()
            records = records[-20:]
        if trial % 10_000 == 0 and records:
            print(trial, records[-1][:-1], "delta", records[-1][0] - TARGET, flush=True)
    print("FINAL")
    for row in reversed(records):
        print(row, "delta", row[0] - TARGET)


if __name__ == "__main__":
    main()
