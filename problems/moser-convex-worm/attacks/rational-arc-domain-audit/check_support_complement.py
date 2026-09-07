#!/usr/bin/env python3
"""Exact complementary worm-angle slabs from the all-segment worm BFS."""

import json
import sys
from fractions import Fraction as Q
from pathlib import Path

import check_support_bfs as bfs
import check_support_cell as cell
import check_support_slab as slab
import probe_adaptive as trig


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


def center_lower(phi):
    normals, _ = bfs.TEMPLATES["worm"]
    x0 = slab.abs_lower(slab.rotated_x(normals[0], phi))
    x1 = slab.abs_lower(slab.rotated_x(normals[1], phi))
    x2 = slab.abs_lower(slab.rotated_x(normals[2], phi))
    return (x0 + x2) / 12 + Q(169, 807) * x1


def check(path):
    data = json.loads(Path(path).read_text(), object_pairs_hook=strict_object)
    fields = {"schema_version", "claim_scope", "target", "recorded_lower", "template",
              "basis", "triangle_domain", "square_domain", "worm_intervals",
              "mesh_degrees"}
    if not isinstance(data, dict) or set(data) != fields:
        raise Reject("root fields")
    if data["schema_version"] != "moser-support-complement-v1" or \
       data["claim_scope"] != "partial_complementary_worm_slabs_only":
        raise Reject("schema or scope")
    basis = [0,1,2,3,4,5,6,7,8,12]
    if data["template"] != "worm" or data["basis"] != basis:
        raise Reject("basis")
    _, solutions = bfs.reconstruct("worm")
    if sum(solution["basis"] == basis for solution in solutions) != 1:
        raise Reject("basis is not exact feasible allocation")
    if data["triangle_domain"] != ["0", "120"] or data["square_domain"] != ["0", "90"]:
        raise Reject("omitted-angle domain incomplete")
    intervals = data["worm_intervals"]
    expected = [["0", "80"], ["259/2", "180"]]
    if intervals != expected:
        raise Reject("wrong complementary intervals")
    mesh = rat(data["mesh_degrees"], "mesh")
    if mesh != Q(1, 2):
        raise Reject("mesh")
    target = rat(data["target"], "target")
    recorded = rat(data["recorded_lower"], "recorded")
    if recorded != Q(93, 400) or recorded < target:
        raise Reject("recorded lower")
    lipschitz = Q(607, 1614)
    error = lipschitz * (mesh / 2) * trig.PI.hi / 180
    total_cells = 0
    covered_length = Q(0)
    for raw_lo, raw_hi in intervals:
        lo, hi = rat(raw_lo, "lo"), rat(raw_hi, "hi")
        count = (hi - lo) / mesh
        if count.denominator != 1:
            raise Reject("mesh does not tile interval")
        for index in range(count.numerator):
            phi = lo + (Q(index) + Q(1, 2)) * mesh
            if center_lower(phi) - error < recorded:
                raise Reject(f"complement mesh cell {total_cells + index} misses bound")
        total_cells += count.numerator
        covered_length += hi - lo
    return {"worm_cells": total_cells, "certified_lower": recorded,
            "covered_fraction": covered_length / 180}


def main():
    try:
        report = check(sys.argv[1])
    except (IndexError, OSError, json.JSONDecodeError, Reject) as error:
        print(f"REJECT: {error}", file=sys.stderr)
        return 1
    print(f"PASS rigorous complementary support slabs: {report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
