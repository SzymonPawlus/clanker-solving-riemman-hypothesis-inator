#!/usr/bin/env python3
"""Exact replay and coverage accounting for a partial angular-cell staircase."""

import json
import sys
from fractions import Fraction as Q
from pathlib import Path

import check_support_cell as cellcheck
import check_support_bfs as bfscheck


class Reject(ValueError):
    pass


def strict_object(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise Reject(f"duplicate JSON field: {key}")
        out[key] = value
    return out


def rat(raw, label):
    try:
        value = Q(raw)
    except (TypeError, ValueError, ZeroDivisionError) as error:
        raise Reject(f"bad rational {label}") from error
    if not isinstance(raw, str) or str(value) != raw:
        raise Reject(f"noncanonical rational {label}")
    return value


def beta_pieces(center, radius):
    lo, hi = center - radius, center + radius
    if hi <= 120:
        return [(lo, hi)]
    return [(lo, Q(120)), (Q(0), hi - 120)]


def overlap(left, right):
    return max(left[0], right[0]) < min(left[1], right[1])


def check(path):
    data = json.loads(Path(path).read_text(), object_pairs_hook=strict_object)
    if not isinstance(data, dict) or set(data) != {"schema_version", "claim_scope", "target",
                                                  "basis", "half_width_degrees",
                                                  "square_domain_degrees", "cells"}:
        raise Reject("root fields")
    if data["schema_version"] != "moser-support-cells-v1" or \
       data["claim_scope"] != "partial_common_angular_coverage_only":
        raise Reject("schema or scope")
    basis = [0,1,2,3,5,6,7,8,12,13]
    if data["basis"] != basis:
        raise Reject("basis")
    _, exact_solutions = bfscheck.reconstruct("worm")
    if sum(solution["basis"] == basis for solution in exact_solutions) != 1:
        raise Reject("basis is not an exact feasible allocation")
    radius = rat(data["half_width_degrees"], "radius")
    if radius != Q(1, 4) or data["square_domain_degrees"] != ["0", "90"]:
        raise Reject("cell geometry")
    target = rat(data["target"], "target")
    cells = data["cells"]
    if not isinstance(cells, list) or not cells:
        raise Reject("no cells")
    rectangles = []
    for index, item in enumerate(cells):
        if not isinstance(item, dict) or set(item) != {"id", "triangle_center", "worm_center",
                                                "certified_lower"}:
            raise Reject("cell fields")
        if item["id"] != f"cell-{index}":
            raise Reject("cell id")
        beta = rat(item["triangle_center"], "beta")
        phi = rat(item["worm_center"], "phi")
        declared = rat(item["certified_lower"], "lower")
        if not 0 <= beta <= 120 or not radius <= phi <= 180 - radius:
            raise Reject("cell outside angular root")
        lower, _, _ = cellcheck.rigorous_lower(beta, phi, radius)
        if declared != Q(237, 1000) or lower < declared or declared < target:
            raise Reject("cell lower endpoint")
        phi_interval = (phi - radius, phi + radius)
        for beta_interval in beta_pieces(beta, radius):
            rectangle = (beta_interval, phi_interval)
            if any(overlap(rectangle[0], old[0]) and overlap(rectangle[1], old[1])
                   for old in rectangles):
                raise Reject("overlapping angular cells")
            rectangles.append(rectangle)
    covered = Q(90) * sum((hi_b - lo_b) * (hi_p - lo_p)
                          for (lo_b, hi_b), (lo_p, hi_p) in rectangles)
    root = Q(120 * 90 * 180)
    if covered >= root:
        raise Reject("partial certificate claims full coverage")
    return {"cells": len(cells), "covered_volume_degrees3": covered,
            "root_volume_degrees3": root, "covered_fraction": covered / root,
            "uncovered_fraction": 1 - covered / root}


def main():
    try:
        report = check(sys.argv[1])
    except (IndexError, OSError, json.JSONDecodeError, Reject) as error:
        print(f"REJECT: {error}", file=sys.stderr)
        return 1
    print(f"PASS partial support-cell coverage: {report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
