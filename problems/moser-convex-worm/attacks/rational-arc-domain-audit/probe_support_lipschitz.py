#!/usr/bin/env python3
"""Numerical center-minus-Lipschitz probe around the coarse worst basin.

The allocation vectors are reconstructed exactly by check_support_bfs.  Trig
and the final center evaluation are floating triage, so this is not a global or
interval certificate.
"""

import json
import math

import check_support_bfs as exact


SHAPES = exact.SHAPES
CENTRED_POINTS = {
    "segment": ((-0.5, 0.0), (0.5, 0.0)),
    "triangle": ((-0.25, -math.sqrt(3) / 12),
                 (0.25, -math.sqrt(3) / 12), (0.0, math.sqrt(3) / 6)),
    "square": ((-1 / 6, -1 / 6), (1 / 6, -1 / 6),
               (1 / 6, 1 / 6), (-1 / 6, 1 / 6)),
    "worm": ((-0.2, -0.25), (1 / 3 - 0.2, -0.25),
             (338 / 807 - 0.2, 260 / 807 - 0.25),
             (9361 / 72361 - 0.2, 105820 / 217083 - 0.25)),
}
RADII = {name: max(math.hypot(x, y) for x, y in points)
         for name, points in CENTRED_POINTS.items()}
ANGLES = {"triangle": 120.0, "square": 0.0, "worm": 100.0}
HALF_WIDTH_DEGREES = 0.25
TARGET = 0.232239


def number(value):
    return float(value.a) + float(value.b) * math.sqrt(3)


def rotate(point, degrees):
    angle = math.radians(degrees)
    cosine, sine = math.cos(angle), math.sin(angle)
    return cosine * point[0] - sine * point[1], sine * point[0] + cosine * point[1]


def support(shape, normal, degrees):
    local_normal = rotate(normal, -degrees)
    return max(x * local_normal[0] + y * local_normal[1]
               for x, y in CENTRED_POINTS[shape])


def evaluate(template, vector):
    normals, lengths = exact.TEMPLATES[template]
    template_angle = 0.0 if template == "segment" else ANGLES[template]
    value = 0.0
    lipschitz = {name: 0.0 for name in ANGLES}
    for edge, normal_exact in enumerate(normals):
        normal = rotate((number(normal_exact[0]), number(normal_exact[1])), template_angle)
        length = number(lengths[edge])
        for shape_index, shape in enumerate(SHAPES):
            allocation = number(vector[edge * len(SHAPES) + shape_index])
            coefficient = 0.5 * length * allocation
            if coefficient == 0:
                continue
            shape_angle = 0.0 if shape == "segment" else ANGLES[shape]
            value += coefficient * support(shape, normal, shape_angle)
            for variable in ANGLES:
                relative_derivative = ((1 if template == variable else 0) -
                                       (1 if shape == variable else 0))
                lipschitz[variable] += coefficient * RADII[shape] * abs(relative_derivative)
    return value, lipschitz


def main():
    candidates = []
    for template in exact.TEMPLATES:
        _, solutions = exact.reconstruct(template)
        for index, solution in enumerate(solutions):
            vector = [exact.K(a, b) for a, b in
                      ((exact.Q(raw[0]), exact.Q(raw[1])) for raw in solution["coordinates"])]
            value, lipschitz = evaluate(template, vector)
            radius_radians = math.radians(HALF_WIDTH_DEGREES)
            lower = value - radius_radians * sum(lipschitz.values())
            candidates.append((lower, value, template, index, solution["basis"], lipschitz))
    lower, value, template, index, basis, lipschitz = max(candidates)
    print(json.dumps({
        "scope": "single_angular_cell_numerical_lipschitz_probe_only",
        "global_claim": False,
        "center_degrees": ANGLES,
        "half_width_degrees_each_axis": HALF_WIDTH_DEGREES,
        "chosen_template": template,
        "chosen_exact_bfs_index": index,
        "chosen_basis": basis,
        "center_value_float": value,
        "lipschitz_per_radian": lipschitz,
        "center_minus_lipschitz_float": lower,
        "target": TARGET,
        "clears_target_numerically": lower >= TARGET,
        "uncovered_common_angle_domain": True,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
