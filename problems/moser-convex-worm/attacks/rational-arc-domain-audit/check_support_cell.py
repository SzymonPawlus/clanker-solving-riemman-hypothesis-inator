#!/usr/bin/env python3
"""Rigorous center-minus-Lipschitz checker for one support-portfolio cell."""

import json
import sys
from fractions import Fraction as Q
from pathlib import Path

import check_support_bfs as bfs
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


def sqrt3_interval():
    high = Q(2)
    for _ in range(10):
        high = (high + 3 / high) / 2
    low = 3 / high
    if not low * low <= 3 <= high * high:
        raise AssertionError("sqrt(3) enclosure")
    return trig.I(low, high)


SQRT3 = sqrt3_interval()


def field_interval(value):
    return trig.I(value.a) + value.b * SQRT3


def rotate_normal(normal, degrees):
    cosine = trig.point_trig(abs(degrees), True)
    sine = trig.point_trig(abs(degrees), False)
    if degrees < 0:
        sine = -sine
    x, y = field_interval(normal[0]), field_interval(normal[1])
    return cosine * x - sine * y, sine * x + cosine * y


SEGMENT = ((bfs.K(Q(-1, 2)), bfs.K(0)), (bfs.K(Q(1, 2)), bfs.K(0)))
TRIANGLE = ((bfs.K(Q(-1, 4)), bfs.K(0, Q(-1, 12))),
            (bfs.K(Q(1, 4)), bfs.K(0, Q(-1, 12))),
            (bfs.K(0), bfs.K(0, Q(1, 6))))


def support_lower(points, normal):
    candidates = []
    for x, y in points:
        value = field_interval(x) * normal[0] + field_interval(y) * normal[1]
        candidates.append(value.lo)
    return max(candidates)


def center_lower(beta, phi):
    normals, _ = bfs.TEMPLATES["worm"]
    segment_supports = [support_lower(SEGMENT, rotate_normal(normals[index], phi))
                        for index in (0, 2, 3)]
    triangle_supports = [support_lower(TRIANGLE, rotate_normal(normals[index], phi - beta))
                         for index in (1, 3)]
    return (segment_supports[0] + segment_supports[1] +
            Q(138, 269) * segment_supports[2] +
            triangle_supports[0] + triangle_supports[1]) / 6


def rigorous_lower(beta, phi, radius):
    center = center_lower(beta, phi)
    triangle_radius_upper = Q(289, 1000)
    if 12 * triangle_radius_upper * triangle_radius_upper <= 1:
        raise AssertionError("triangle radius upper bound")
    l_beta = triangle_radius_upper / 3
    l_phi = Q(169, 807) + triangle_radius_upper / 3
    angular_radius = radius * trig.PI.hi / 180
    return center - (l_beta + l_phi) * angular_radius, l_beta, l_phi


def check(path):
    data = json.loads(Path(path).read_text(), object_pairs_hook=strict_object)
    fields = {"schema_version", "claim_scope", "target", "template", "basis",
              "center_degrees", "half_width_degrees", "periodic_triangle_cell"}
    if not isinstance(data, dict) or set(data) != fields:
        raise Reject("root fields")
    if data["schema_version"] != "moser-support-cell-v1":
        raise Reject("schema")
    if data["claim_scope"] != "single_periodic_angular_cell_only":
        raise Reject("scope escalation")
    if data["template"] != "worm" or data["basis"] != [0,1,2,3,5,6,7,8,12,13]:
        raise Reject("untrusted primal basis")
    _, solutions = bfs.reconstruct("worm")
    matching = [item for item in solutions if item["basis"] == data["basis"]]
    if len(matching) != 1:
        raise Reject("basis is not an exact feasible allocation")
    expected_coordinates = [["1","0"],["0","0"],["0","0"],["0","0"],
                            ["0","0"],["1","0"],["0","0"],["0","0"],
                            ["1","0"],["0","0"],["0","0"],["0","0"],
                            ["138/407","0"],["269/407","0"],["0","0"],["0","0"]]
    if matching[0]["coordinates"] != expected_coordinates:
        raise Reject("unexpected exact primal coordinates")
    centers = data["center_degrees"]
    if not isinstance(centers, dict) or set(centers) != {"triangle", "square", "worm"}:
        raise Reject("center dimensions")
    beta = rat(centers["triangle"], "triangle center")
    alpha = rat(centers["square"], "square center")
    phi = rat(centers["worm"], "worm center")
    radius = rat(data["half_width_degrees"], "half width")
    if (beta, alpha, phi, radius) != (Q(120), Q(0), Q(100), Q(1, 4)):
        raise Reject("wrong prototype cell")
    if data["periodic_triangle_cell"] != [["0", "1/4"], ["479/4", "120"]]:
        raise Reject("triangle quotient boundary not covered periodically")
    target = rat(data["target"], "target")
    lower, l_beta, l_phi = rigorous_lower(beta, phi, radius)
    if lower < target:
        raise Reject("rigorous lower endpoint does not clear target")
    certified = Q(237, 1000)
    if lower < certified:
        raise Reject("raw lower endpoint does not establish recorded rational")
    return {"certified_lower": certified, "l_beta": l_beta, "l_phi": l_phi}


def main():
    try:
        report = check(sys.argv[1])
    except (IndexError, OSError, json.JSONDecodeError, Reject) as error:
        print(f"REJECT: {error}", file=sys.stderr)
        return 1
    print("PASS rigorous support cell; " + "; ".join(f"{key}={value}" for key, value in report.items()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
