#!/usr/bin/env python3
"""Exact checker for the rational arc and its compact counterexample box."""

import json
import sys
from fractions import Fraction as Q
from pathlib import Path


class Reject(ValueError):
    pass


def strict_object(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise Reject(f"duplicate JSON field: {key}")
        out[key] = value
    return out


def rational(value, label):
    if not isinstance(value, str):
        raise Reject(f"{label} must be a rational string")
    try:
        result = Q(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise Reject(f"invalid rational in {label}") from exc
    if str(result) != value:
        raise Reject(f"non-canonical rational in {label}")
    return result


def point(raw, label):
    if not isinstance(raw, list) or len(raw) != 2:
        raise Reject(f"{label} must be a two-coordinate point")
    return rational(raw[0], f"{label}.x"), rational(raw[1], f"{label}.y")


def check(path):
    doc = json.loads(Path(path).read_text(encoding="utf-8"),
                     object_pairs_hook=strict_object,
                     parse_constant=lambda value: (_ for _ in ()).throw(
                         Reject(f"non-finite JSON number: {value}")))
    fields = {"schema_version", "claim_scope", "motion_convention",
              "target_rational", "diameter_upper", "pinned_segment",
              "forced_triangle_side", "arc_vertices", "pose_domain"}
    if not isinstance(doc, dict) or set(doc) != fields:
        raise Reject("unknown or missing top-level field")
    if doc["schema_version"] != "moser-rational-arc-domain-v1":
        raise Reject("unsupported schema")
    if doc["claim_scope"] != "witness_and_compact_domain_only":
        raise Reject("domain certificate must not claim an area lower bound")
    if doc["motion_convention"] != "orientation_preserving_no_reflection_quotient":
        raise Reject("reflection or motion convention mismatch")

    target = rational(doc["target_rational"], "target_rational")
    diameter = rational(doc["diameter_upper"], "diameter_upper")
    if target <= 0 or diameter <= 0:
        raise Reject("target and diameter bound must be positive")
    if 3*diameter*diameter <= 64*target*target:
        raise Reject("diameter bound is not strictly outward")

    segment = doc["pinned_segment"]
    if not isinstance(segment, list) or len(segment) != 2:
        raise Reject("pinned segment must have two endpoints")
    if [point(raw, f"pinned_segment[{i}]") for i, raw in enumerate(segment)] != [(Q(0), Q(0)), (Q(1), Q(0))]:
        raise Reject("wrong pinned unit segment")
    if rational(doc["forced_triangle_side"], "forced_triangle_side") != Q(1, 2):
        raise Reject("wrong forced triangle side")

    raw_vertices = doc["arc_vertices"]
    if not isinstance(raw_vertices, list) or len(raw_vertices) != 4:
        raise Reject("arc must have exactly four traversal vertices")
    vertices = [point(raw, f"arc_vertices[{i}]") for i, raw in enumerate(raw_vertices)]
    expected = [(Q(0), Q(0)), (Q(1, 3), Q(0)),
                (Q(32, 75), Q(8, 25)), (Q(91, 625), Q(312, 625))]
    if vertices != expected:
        raise Reject("wrong rational arc")
    for index, (a, b) in enumerate(zip(vertices, vertices[1:])):
        dx, dy = b[0]-a[0], b[1]-a[1]
        if dx*dx + dy*dy != Q(1, 9):
            raise Reject(f"edge {index} does not have length 1/3")

    poses = doc["pose_domain"]
    if not isinstance(poses, dict) or set(poses) != {"triangle", "square", "rational_arc"}:
        raise Reject("pose ledger must contain exactly three unpinned witnesses")
    expected_xy = [str(-diameter), str(diameter)]
    for name, pose in poses.items():
        if not isinstance(pose, dict) or set(pose) != {"tx", "ty", "theta_degrees"}:
            raise Reject(f"incomplete pose variables for {name}")
        if pose["tx"] != expected_xy or pose["ty"] != expected_xy:
            raise Reject(f"translation box mismatch for {name}")
        if pose["theta_degrees"] != ["0", "360"]:
            raise Reject(f"full orientation domain missing for {name}")


def main():
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} DOMAIN.json", file=sys.stderr)
        return 2
    try:
        check(sys.argv[1])
    except (OSError, json.JSONDecodeError, Reject) as exc:
        print(f"REJECT: {exc}", file=sys.stderr)
        return 1
    print("PASS exact rational worm and compact counterexample domain")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
