#!/usr/bin/env python3
"""Rigorous full-triangle/full-square angular slab from one worm primal."""

import json
import sys
from fractions import Fraction as Q
from pathlib import Path

import check_support_bfs as bfs
import check_support_cell as cell
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


def abs_lower(interval):
    if interval.lo >= 0:
        return interval.lo
    if interval.hi <= 0:
        return -interval.hi
    return Q(0)


def rotated_x(normal, degrees):
    cosine = trig.point_trig(degrees, True)
    sine = trig.point_trig(degrees, False)
    return cosine * cell.field_interval(normal[0]) - sine * cell.field_interval(normal[1])


def center_lower(phi):
    normals, _ = bfs.TEMPLATES["worm"]
    segment = (abs_lower(rotated_x(normals[0], phi)) +
               abs_lower(rotated_x(normals[2], phi)) +
               Q(138, 269) * abs_lower(rotated_x(normals[3], phi))) / 12
    # The two triangle normals are antipodal.  Their support sum is a width,
    # whose minimum for the side-1/2 equilateral triangle is sqrt(3)/4.
    triangle_width = cell.SQRT3.lo / 24
    return segment + triangle_width


def check(path):
    data = json.loads(Path(path).read_text(), object_pairs_hook=strict_object)
    fields = {"schema_version", "claim_scope", "target", "recorded_lower", "template",
              "basis", "triangle_domain", "square_domain", "worm_interval",
              "mesh_degrees"}
    if not isinstance(data, dict) or set(data) != fields:
        raise Reject("root fields")
    if data["schema_version"] != "moser-support-slab-v1" or \
       data["claim_scope"] != "single_partial_worm_angle_slab_only":
        raise Reject("schema or scope")
    basis = [0,1,2,3,5,6,7,8,12,13]
    if data["template"] != "worm" or data["basis"] != basis:
        raise Reject("basis")
    _, solutions = bfs.reconstruct("worm")
    if sum(solution["basis"] == basis for solution in solutions) != 1:
        raise Reject("basis is not exact feasible allocation")
    if data["triangle_domain"] != ["0", "120"] or data["square_domain"] != ["0", "90"]:
        raise Reject("omitted-angle domain incomplete")
    interval = data["worm_interval"]
    if not isinstance(interval, list) or len(interval) != 2:
        raise Reject("worm interval")
    lo, hi = rat(interval[0], "worm lo"), rat(interval[1], "worm hi")
    mesh = rat(data["mesh_degrees"], "mesh")
    if (lo, hi, mesh) != (Q(75), Q(269, 2), Q(1, 2)):
        raise Reject("wrong slab geometry")
    target = rat(data["target"], "target")
    recorded = rat(data["recorded_lower"], "recorded lower")
    if recorded != Q(2323, 10000) or recorded < target:
        raise Reject("recorded lower")
    count = (hi - lo) / mesh
    if count.denominator != 1:
        raise Reject("mesh does not tile slab")
    half_width = mesh / 2
    lipschitz = Q(169, 807)
    error = lipschitz * half_width * trig.PI.hi / 180
    minimum = None
    for index in range(count.numerator):
        center = lo + (Q(index) + Q(1, 2)) * mesh
        lower = center_lower(center) - error
        minimum = lower if minimum is None else min(minimum, lower)
        if lower < recorded:
            raise Reject(f"worm mesh cell {index} misses recorded lower")
    root_volume = Q(120 * 90 * 180)
    covered = Q(120 * 90) * (hi - lo)
    return {"worm_cells": count.numerator, "certified_lower": recorded,
            "covered_fraction": covered / root_volume,
            "uncovered_fraction": 1 - covered / root_volume}


def main():
    try:
        report = check(sys.argv[1])
    except (IndexError, OSError, json.JSONDecodeError, Reject) as error:
        print(f"REJECT: {error}", file=sys.stderr)
        return 1
    print(f"PASS rigorous support slab: {report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
