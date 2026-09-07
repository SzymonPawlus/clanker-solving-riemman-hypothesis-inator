#!/usr/bin/env python3
"""Random search using exact rational unit directions and rational lengths.

Candidate ranking uses binary floating point.  Fractions printed in the final
table retain all exact input data for a later independent exact audit.
"""

from __future__ import annotations

from fractions import Fraction
import math
import random

from search_four_edge import TARGET, floor_for


def direction(t: Fraction):
    den = 1 + t * t
    return (1 - t * t) / den, 2 * t / den


def angle(t: Fraction):
    c, s = direction(t)
    return math.atan2(float(s), float(c))


def main():
    rng = random.Random(178_5)
    ts = sorted({Fraction(p, q) for q in range(5, 81) for p in range(3, 121)
                 if Fraction(1, 2) < Fraction(p, q) < Fraction(6, 5)})
    records = []
    for trial in range(2_000_000):
        tb, ta, tg = rng.choice(ts), rng.choice(ts), rng.choice(ts)
        if ta > tb:
            ta, tb = tb, ta
        # Keep all four edge lengths positive and exactly rational.
        den = rng.choice((60, 72, 84, 96, 120, 144, 180))
        l1 = Fraction(rng.randrange(1, den // 2), den)
        l2 = Fraction(rng.randrange(1, den // 2), den)
        _, sb = direction(tb)
        _, sa = direction(ta)
        _, sg = direction(tg)
        l4 = (l1 * sb + l2 * sa) / sg
        l0 = 1 - l1 - l2 - l4
        if min(l0, l1, l2, l4) <= 0:
            continue
        angles = (-angle(tb), -angle(ta), 0.0, angle(tg))
        lengths = tuple(map(float, (l1, l2, l0, l4)))
        val, arg = floor_for(angles, lengths)
        row = (val, tb, ta, tg, l1, l2, l0, l4, arg)
        if len(records) < 30 or val > records[0][0]:
            records.append(row)
            records.sort()
            records = records[-30:]
        if trial and trial % 250_000 == 0:
            print(trial, records[-1], "delta", records[-1][0] - TARGET, flush=True)
    print("FINAL")
    for row in reversed(records):
        print(row, "delta", row[0] - TARGET)


if __name__ == "__main__":
    main()
