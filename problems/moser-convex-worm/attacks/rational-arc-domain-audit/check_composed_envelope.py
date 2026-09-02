#!/usr/bin/env python3
"""Exact structural checker for a common-outer-cell envelope certificate.

This checker intentionally knows only the universal area >= 0 leaf.  It proves
the quantifier/coverage plumbing without laundering a local pose witness into a
lower bound on an inner minimum.
"""

import json
import sys
from fractions import Fraction as Q
from pathlib import Path

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
    if not isinstance(raw, str):
        raise Reject(f"{label} must be a string")
    try:
        value = Q(raw)
    except (ValueError, ZeroDivisionError) as error:
        raise Reject(f"bad rational {label}") from error
    if str(value) != raw:
        raise Reject(f"noncanonical rational {label}")
    return value


def box(raw, dimensions, label):
    if not isinstance(raw, dict) or set(raw) != set(dimensions):
        raise Reject(f"{label} has wrong dimensions")
    parsed = {}
    for dimension in dimensions:
        interval = raw[dimension]
        if not isinstance(interval, list) or len(interval) != 2:
            raise Reject(f"{label}.{dimension} is not an interval")
        lo = rat(interval[0], f"{label}.{dimension}.lo")
        hi = rat(interval[1], f"{label}.{dimension}.hi")
        if lo >= hi:
            raise Reject(f"{label}.{dimension} is empty or reversed")
        parsed[dimension] = (lo, hi)
    return parsed


def same_box(left, right):
    return left == right


def contains(outer, inner):
    return all(outer[d][0] <= inner[d][0] and inner[d][1] <= outer[d][1] for d in outer)


def volume(value):
    result = Q(1)
    for lo, hi in value.values():
        result *= hi - lo
    return result


def interiors_overlap(left, right):
    return all(max(left[d][0], right[d][0]) < min(left[d][1], right[d][1]) for d in left)


def cross(left, right):
    return left[0] * right[1] - left[1] * right[0]


def subtract(left, right):
    return left[0] - right[0], left[1] - right[1]


def segment_square_cycle_bound(outer_cell):
    """Uniform area bound from segment P0,P1 and opposite square corners P2,P3."""
    tx = trig.I(*outer_cell["square_tx"])
    ty = trig.I(*outer_cell["square_ty"])
    angle = trig.I(*outer_cell["square_theta_deg"])
    cosine = trig.cos_range(angle)
    sine = trig.sin_range(angle)
    points = [(trig.I(0), trig.I(0)), (trig.I(1), trig.I(0))]
    for x, y in ((Q(1, 3), Q(1, 3)), (Q(0), Q(1, 3))):
        points.append((tx + cosine * x - sine * y, ty + sine * x + cosine * y))
    for index in range(4):
        edge = subtract(points[(index + 1) % 4], points[index])
        for other in range(4):
            if other in (index, (index + 1) % 4):
                continue
            turn = cross(edge, subtract(points[other], points[index]))
            if turn.lo <= 0:
                raise Reject("segment-square cycle is not uniformly convex")
    twice_area = trig.I(0)
    for index in range(4):
        twice_area += cross(points[index], points[(index + 1) % 4])
    if twice_area.lo <= 0:
        raise Reject("segment-square area sign uncertain")
    return twice_area.lo / 2


def union_is_root(root, leaves):
    """Exact recursive-grid coverage check by endpoint atomization."""
    endpoints = {d: {root[d][0], root[d][1]} for d in root}
    for leaf in leaves:
        if not contains(root, leaf):
            return False
        for d, (lo, hi) in leaf.items():
            endpoints[d].update((lo, hi))
    atoms = [[]]
    for d in root:
        spans = sorted(endpoints[d])
        next_atoms = []
        for prefix in atoms:
            for lo, hi in zip(spans, spans[1:]):
                if lo < hi:
                    next_atoms.append(prefix + [(d, (lo, hi))])
        atoms = next_atoms
    for atom_items in atoms:
        atom = dict(atom_items)
        midpoint = {d: (lo + hi) / 2 for d, (lo, hi) in atom.items()}
        if all(root[d][0] < midpoint[d] < root[d][1] for d in root):
            hits = sum(all(lo <= midpoint[d] <= hi for d, (lo, hi) in leaf.items()) for leaf in leaves)
            if hits != 1:
                return False
    return True


def check_inner(raw, expected_kind, outer_cell, compact_root):
    fields = {"kind", "outer_cell", "inner_root", "leaves"}
    if not isinstance(raw, dict) or set(raw) != fields:
        raise Reject(f"{expected_kind} inner tree fields")
    if raw["kind"] != expected_kind:
        raise Reject("inner family kind mismatch")
    attached = box(raw["outer_cell"], outer_cell.keys(), f"{expected_kind}.outer_cell")
    if not same_box(attached, outer_cell):
        raise Reject("mismatched outer partitions")
    root = box(raw["inner_root"], compact_root.keys(), f"{expected_kind}.inner_root")
    if not same_box(root, compact_root):
        raise Reject("missing inner pose cells: wrong compact root")
    if not isinstance(raw["leaves"], list) or not raw["leaves"]:
        raise Reject("missing inner pose cells: no leaves")
    leaf_boxes = []
    bounds = []
    for index, leaf in enumerate(raw["leaves"]):
        leaf_fields = {"box", "proof", "lower_bound", "uniform_over_outer_cell"}
        if not isinstance(leaf, dict) or set(leaf) != leaf_fields:
            raise Reject("inner leaf fields")
        if leaf["uniform_over_outer_cell"] is not True:
            raise Reject("nonuniform bound")
        bound = rat(leaf["lower_bound"], f"{expected_kind}.leaf{index}.lower_bound")
        if leaf["proof"] == "convex_hull_area_nonnegative":
            if bound != 0:
                raise Reject("nonnegativity proves only lower bound zero")
        elif leaf["proof"] == "segment_square_strict_convex_cycle":
            proved = segment_square_cycle_bound(outer_cell)
            if bound > proved:
                raise Reject("declared segment-square bound exceeds interval proof")
        else:
            raise Reject("unsupported inner proof")
        leaf_boxes.append(box(leaf["box"], root.keys(), f"{expected_kind}.leaf{index}.box"))
        bounds.append(bound)
    if not union_is_root(root, leaf_boxes):
        raise Reject("missing inner pose cells or overlapping leaves")
    return min(bounds)


def check(path):
    data = json.loads(Path(path).read_text(), object_pairs_hook=strict_object)
    fields = {"schema_version", "claim_scope", "combination_rule", "target_rational",
              "diameter_bound", "outer_root", "inner_compact_roots", "outer_cells"}
    if not isinstance(data, dict) or set(data) != fields:
        raise Reject("unknown or missing root field")
    if data["schema_version"] != "moser-common-outer-envelope-v1":
        raise Reject("schema")
    if data["claim_scope"] != "partial_outer_coverage_schema_only":
        raise Reject("scope escalation")
    if data["combination_rule"] != "pointwise_max_on_identical_outer_cell":
        raise Reject("combining only global minima is forbidden")
    target = rat(data["target_rational"], "target")
    diameter = rat(data["diameter_bound"], "diameter")
    if target <= 0 or diameter <= 0 or 3 * diameter * diameter <= 64 * target * target:
        raise Reject("unproved root-domain compactification")
    outer_dims = ("square_tx", "square_ty", "square_theta_deg")
    outer_root = box(data["outer_root"], outer_dims, "outer_root")
    if outer_root != {"square_tx": (-diameter, diameter),
                      "square_ty": (-diameter, diameter),
                      "square_theta_deg": (Q(0), Q(90))}:
        raise Reject("outer root does not match compactification and square symmetry")
    roots = data["inner_compact_roots"]
    if not isinstance(roots, dict) or set(roots) != {"triangle", "worm"}:
        raise Reject("inner compact roots")
    triangle_root = box(roots["triangle"], ("tx", "ty", "theta_deg"), "triangle_root")
    worm_root = box(roots["worm"], ("tx", "ty", "theta_deg"), "worm_root")
    expected_triangle = {"tx": (-diameter, diameter), "ty": (-diameter, diameter),
                         "theta_deg": (Q(0), Q(120))}
    expected_worm = {"tx": (-diameter, diameter), "ty": (-diameter, diameter),
                     "theta_deg": (Q(0), Q(180))}
    if triangle_root != expected_triangle or worm_root != expected_worm:
        raise Reject("inner root does not match compactification and angular gauges")
    cells = data["outer_cells"]
    if not isinstance(cells, list) or not cells:
        raise Reject("no outer cells")
    parsed_cells = []
    certified_cells = []
    for index, cell in enumerate(cells):
        if not isinstance(cell, dict) or set(cell) != {"id", "box", "triangle_tree", "worm_tree"}:
            raise Reject("outer cell fields")
        if cell["id"] != f"cell-{index}":
            raise Reject("noncanonical outer cell id")
        outer_cell = box(cell["box"], outer_dims, f"outer_cell{index}")
        if not contains(outer_root, outer_cell):
            raise Reject("outer cell outside root")
        if any(interiors_overlap(outer_cell, previous) for previous in parsed_cells):
            raise Reject("overlapping outer cells")
        parsed_cells.append(outer_cell)
        triangle_bound = check_inner(cell["triangle_tree"], "triangle", outer_cell, triangle_root)
        worm_bound = check_inner(cell["worm_tree"], "worm", outer_cell, worm_root)
        if max(triangle_bound, worm_bound) < target:
            raise Reject("outer cell does not clear target")
        certified_cells.append({"triangle": triangle_bound, "worm": worm_bound,
                                "envelope": max(triangle_bound, worm_bound)})
    covered = sum((volume(cell) for cell in parsed_cells), Q(0))
    root_volume = volume(outer_root)
    if covered >= root_volume:
        raise Reject("partial schema must not claim global outer coverage")
    return {"covered": covered, "root": root_volume, "uncovered": root_volume - covered,
            "covered_fraction": covered / root_volume, "cell_bounds": certified_cells}


def main():
    try:
        report = check(sys.argv[1])
    except (IndexError, OSError, json.JSONDecodeError, Reject) as error:
        print(f"REJECT: {error}", file=sys.stderr)
        return 1
    print("PASS common-cell envelope schema; "
          f"covered_volume={report['covered']}; root_volume={report['root']}; "
          f"covered_fraction={report['covered_fraction']}; uncovered_volume={report['uncovered']}; "
          f"cell_bounds={report['cell_bounds']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
