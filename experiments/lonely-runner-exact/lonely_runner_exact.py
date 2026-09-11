#!/usr/bin/env python3
"""Exact witness-time feasibility for one integer velocity vector.

Only Python's arbitrary-precision integers and Fraction arithmetic are used.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from typing import Iterable, Sequence

Interval = tuple[Fraction, Fraction]


def _merge_closed(intervals: Iterable[Interval]) -> list[Interval]:
    """Return the union of closed intervals, in disjoint sorted form."""
    ordered = sorted(intervals)
    merged: list[Interval] = []
    for left, right in ordered:
        if left > right:
            raise ValueError("interval has left endpoint after right endpoint")
        if merged and left <= merged[-1][1]:
            old_left, old_right = merged[-1]
            merged[-1] = (old_left, max(old_right, right))
        else:
            merged.append((left, right))
    return merged


def _intersect_closed(first: Sequence[Interval], second: Sequence[Interval]) -> list[Interval]:
    """Intersect two sorted lists of disjoint closed intervals exactly."""
    answer: list[Interval] = []
    i = j = 0
    while i < len(first) and j < len(second):
        left = max(first[i][0], second[j][0])
        right = min(first[i][1], second[j][1])
        if left <= right:  # Equality is a valid, closed-endpoint witness.
            answer.append((left, right))
        if first[i][1] < second[j][1]:
            i += 1
        elif second[j][1] < first[i][1]:
            j += 1
        else:
            i += 1
            j += 1
    return _merge_closed(answer)


def allowed_times(velocity: int, separation: Fraction) -> list[Interval]:
    """Times in [0, 1) where distance from ``velocity * t`` to Z is enough."""
    if not isinstance(velocity, int):
        raise TypeError("velocity must be an integer")
    if not 0 < separation <= Fraction(1, 2):
        raise ValueError("separation must lie in (0, 1/2]")
    speed = abs(velocity)
    if speed == 0:
        return []

    # On the j-th period, separation <= speed*t-j <= 1-separation.
    intervals = [
        ((j + separation) / speed, (j + 1 - separation) / speed)
        for j in range(speed)
    ]
    return _merge_closed(intervals)


def feasible_times(velocities: Sequence[int]) -> list[Interval]:
    """Return every witness time for the Lonely Runner bound.

    For k supplied velocities the required separation is 1/(k+1).  The result
    is a sorted union of closed rational intervals contained in [0, 1).
    """
    if not velocities:
        raise ValueError("at least one velocity is required")
    if any(not isinstance(v, int) for v in velocities):
        raise TypeError("all velocities must be integers")

    separation = Fraction(1, len(velocities) + 1)
    feasible: list[Interval] = [(Fraction(0), Fraction(1))]
    # Small speeds create fewer intervals, so processing them first generally
    # keeps intermediate unions small. This does not affect the result.
    for velocity in sorted(velocities, key=abs):
        feasible = _intersect_closed(feasible, allowed_times(velocity, separation))
        if not feasible:
            break
    return feasible


def witness_time(velocities: Sequence[int]) -> Fraction | None:
    """Return an exact witness (the first feasible endpoint), or None."""
    intervals = feasible_times(velocities)
    return intervals[0][0] if intervals else None


def _fraction_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("velocity", type=int, nargs="+", help="integer velocities")
    args = parser.parse_args()
    intervals = feasible_times(args.velocity)
    witness = intervals[0][0] if intervals else None
    print(json.dumps({
        "velocities": args.velocity,
        "separation": _fraction_text(Fraction(1, len(args.velocity) + 1)),
        "feasible": bool(intervals),
        "witness": None if witness is None else _fraction_text(witness),
        "intervals": [[_fraction_text(a), _fraction_text(b)] for a, b in intervals],
    }, indent=2))


if __name__ == "__main__":
    main()
