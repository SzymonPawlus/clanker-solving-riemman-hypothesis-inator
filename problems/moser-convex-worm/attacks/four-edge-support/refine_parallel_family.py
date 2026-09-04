#!/usr/bin/env python3
"""Local floating-point refinement around the equal-turn boundary point."""

from __future__ import annotations

import math
import random

from search_four_edge import TARGET, floor_for


def unpack(x):
    beta, alpha, gamma, l1, l2 = x
    if not (0.0 < alpha <= beta < math.pi and 0.0 < gamma < math.pi):
        return None
    l4 = (l1 * math.sin(beta) + l2 * math.sin(alpha)) / math.sin(gamma)
    l0 = 1.0 - l1 - l2 - l4
    if min(l1, l2, l0, l4) <= 0:
        return None
    return (-beta, -alpha, 0.0, gamma), (l1, l2, l0, l4)


def value(x, samples=2048):
    candidate = unpack(x)
    if candidate is None:
        return -1.0
    return floor_for(*candidate, samples)[0]


def main():
    rng = random.Random(178_4)
    theta = math.acos(math.sqrt((4.0 - math.sqrt(13.0)) / 8.0))
    global_best = None
    for restart in range(30):
        x = [theta + rng.gauss(0, .03), theta + rng.gauss(0, .03),
             theta + rng.gauss(0, .03), 1/6 + rng.gauss(0, .02),
             1/6 + rng.gauss(0, .02)]
        if x[1] > x[0]:
            x[0], x[1] = x[1], x[0]
        cur = value(x, 512)
        for stage in range(8):
            angular = 0.04 * (0.45 ** stage)
            length = 0.025 * (0.45 ** stage)
            for _ in range(4000):
                y = x.copy()
                j = rng.randrange(5)
                y[j] += rng.gauss(0, angular if j < 3 else length)
                if y[1] > y[0]:
                    y[0], y[1] = y[1], y[0]
                test = value(y, 1024)
                if test > cur:
                    x, cur = y, test
            print(restart, stage, cur, cur - TARGET, x, unpack(x), flush=True)
        fine = value(x, 32768)
        row = (fine, x, unpack(x))
        if global_best is None or row[0] > global_best[0]:
            global_best = row
            print("BEST", global_best, "delta", fine - TARGET, flush=True)


if __name__ == "__main__":
    main()
