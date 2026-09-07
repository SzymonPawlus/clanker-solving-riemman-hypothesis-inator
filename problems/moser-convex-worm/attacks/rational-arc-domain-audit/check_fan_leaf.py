#!/usr/bin/env python3
"""Exact interval fan-area leaf checker, independent of hull combinatorics."""

import json
import sys
from fractions import Fraction as Q
from pathlib import Path


class Reject(ValueError):
    pass


class I:
    def __init__(self, lo, hi=None):
        self.lo, self.hi = Q(lo), Q(lo if hi is None else hi)
        if self.lo > self.hi:
            raise Reject("reversed interval")

    def __add__(self, other):
        other = other if isinstance(other, I) else I(other)
        return I(self.lo+other.lo, self.hi+other.hi)

    def __neg__(self):
        return I(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + -other

    def __mul__(self, other):
        other = other if isinstance(other, I) else I(other)
        values = (self.lo*other.lo, self.lo*other.hi,
                  self.hi*other.lo, self.hi*other.hi)
        return I(min(values), max(values))


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


def box(raw, label):
    if not isinstance(raw, list) or len(raw) != 2:
        raise Reject(f"{label} must be an interval")
    return I(rational(raw[0], label), rational(raw[1], label))


def cross(a, b):
    return a[0]*b[1] - a[1]*b[0]


def check(path):
    doc = json.loads(Path(path).read_text(encoding="utf-8"),
                     object_pairs_hook=strict_object)
    fields = {"schema_version", "claim_scope", "target_rational",
              "arc_pose", "fan_triangles"}
    if not isinstance(doc, dict) or set(doc) != fields:
        raise Reject("unknown or missing top-level field")
    if doc["schema_version"] != "moser-rational-arc-fan-leaf-v1":
        raise Reject("unsupported schema")
    if doc["claim_scope"] != "single_leaf_area_prune_only":
        raise Reject("fan leaf must not claim domain coverage")
    target = rational(doc["target_rational"], "target_rational")

    pose = doc["arc_pose"]
    if not isinstance(pose, dict) or set(pose) != {"tx", "ty", "theta_degrees"}:
        raise Reject("incomplete arc pose")
    tx, ty = box(pose["tx"], "arc_pose.tx"), box(pose["ty"], "arc_pose.ty")
    if pose["theta_degrees"] != ["0", "0"]:
        raise Reject("demo predicate supports only its exact zero-angle slice")

    # Recompute selected point boxes from fixed witness data. No certificate
    # supplied coordinate or midpoint hull order is trusted.
    points = {
        "segment.E": (I(0), I(0)),
        "segment.F": (I(1), I(0)),
        "rational_arc.P3": (tx+Q(91, 625), ty+Q(312, 625)),
    }
    fans = doc["fan_triangles"]
    if fans != [["segment.E", "segment.F", "rational_arc.P3"]]:
        raise Reject("unknown, missing, or overlapping fan triangle")
    total_lower = Q(0)
    for names in fans:
        a, b, c = (points[name] for name in names)
        determinant = cross((b[0]-a[0], b[1]-a[1]),
                            (c[0]-a[0], c[1]-a[1]))
        if determinant.lo <= 0:
            raise Reject("fan orientation is not strictly certified")
        total_lower += determinant.lo/2
    if total_lower < target:
        raise Reject("fan area lower endpoint does not clear target")


def main():
    if len(sys.argv) != 2:
        return 2
    try:
        check(sys.argv[1])
    except (OSError, json.JSONDecodeError, Reject) as exc:
        print(f"REJECT: {exc}", file=sys.stderr)
        return 1
    print("PASS exact contained-fan area leaf")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
