#!/usr/bin/env python3
"""Exact BFS reconstruction for mixed-area support allocations."""

import itertools
import json
import sys
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path


class Reject(ValueError):
    pass


class K:
    """The ordered quadratic field Q(sqrt(3)), represented as a+b sqrt(3)."""
    def __init__(self, a=0, b=0):
        self.a, self.b = Q(a), Q(b)

    def __add__(self, other):
        other = k(other)
        return K(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self):
        return K(-self.a, -self.b)

    def __sub__(self, other):
        return self + -k(other)

    def __mul__(self, other):
        other = k(other)
        return K(self.a * other.a + 3 * self.b * other.b,
                 self.a * other.b + self.b * other.a)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = k(other)
        denominator = other.a * other.a - 3 * other.b * other.b
        if denominator == 0:
            raise ZeroDivisionError
        return K((self.a * other.a - 3 * self.b * other.b) / denominator,
                 (self.b * other.a - self.a * other.b) / denominator)

    def __eq__(self, other):
        other = k(other)
        return self.a == other.a and self.b == other.b

    def sign(self):
        if self.a == 0:
            return (self.b > 0) - (self.b < 0)
        if self.b == 0 or (self.a > 0) == (self.b > 0):
            return (self.a > 0) - (self.a < 0)
        comparison = self.a * self.a - 3 * self.b * self.b
        return ((self.a > 0) - (self.a < 0)) * ((comparison > 0) - (comparison < 0))

    def __lt__(self, other):
        return (self - other).sign() < 0

    def text(self):
        return [str(self.a), str(self.b)]


def k(value):
    return value if isinstance(value, K) else K(value)


ZERO, ONE = K(0), K(1)
SHAPES = ("segment", "triangle", "square", "worm")


TEMPLATES = {
    "segment": (
        ((K(0), K(1)), (K(0), K(-1))),
        (K(1), K(1)),
    ),
    "triangle": (
        ((K(0), K(-1)), (K(0, Q(1, 2)), K(Q(1, 2))),
         (K(0, Q(-1, 2)), K(Q(1, 2)))),
        (K(Q(1, 2)),) * 3,
    ),
    "square": (
        ((K(0), K(-1)), (K(1), K(0)), (K(0), K(1)), (K(-1), K(0))),
        (K(Q(1, 3)),) * 4,
    ),
    "worm": (
        ((K(0), K(-1)), (K(Q(260, 269)), K(Q(-69, 269))),
         (K(Q(35880, 72361)), K(Q(62839, 72361))),
         (K(Q(-260, 269)), K(Q(69, 269)))),
        (K(Q(1, 3)), K(Q(1, 3)), K(Q(1, 3)), K(Q(407, 807))),
    ),
}


def rank(matrix):
    work = [row[:] for row in matrix]
    row = 0
    for column in range(len(work[0]) if work else 0):
        pivot = next((i for i in range(row, len(work)) if work[i][column] != ZERO), None)
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        scale = work[row][column]
        work[row] = [value / scale for value in work[row]]
        for i in range(len(work)):
            if i != row and work[i][column] != ZERO:
                factor = work[i][column]
                work[i] = [a - factor * b for a, b in zip(work[i], work[row])]
        row += 1
        if row == len(work):
            break
    return row


def independent_rows(matrix, rhs):
    rows, values = [], []
    current_rank = 0
    for row, value in zip(matrix, rhs):
        candidate = rank(rows + [row])
        if candidate > current_rank:
            rows.append(row)
            values.append(value)
            current_rank = candidate
    return rows, values


def solve(matrix, rhs):
    size = len(matrix)
    work = [row[:] + [rhs[i]] for i, row in enumerate(matrix)]
    for column in range(size):
        pivot = next((i for i in range(column, size) if work[i][column] != ZERO), None)
        if pivot is None:
            return None
        work[column], work[pivot] = work[pivot], work[column]
        scale = work[column][column]
        work[column] = [value / scale for value in work[column]]
        for i in range(size):
            if i != column and work[i][column] != ZERO:
                factor = work[i][column]
                work[i] = [a - factor * b for a, b in zip(work[i], work[column])]
    return [work[i][-1] for i in range(size)]


def constraint_system(template):
    normals, lengths = TEMPLATES[template]
    edges = len(normals)
    variables = edges * len(SHAPES)
    matrix, rhs = [], []
    for edge in range(edges):
        row = [ZERO] * variables
        for shape in range(len(SHAPES)):
            row[edge * len(SHAPES) + shape] = ONE
        matrix.append(row)
        rhs.append(ONE)
    # The segment is pinned.  Each of the three moving witnesses must have
    # zero allocated surface-normal load in both coordinates.
    for shape in range(1, len(SHAPES)):
        for coordinate in range(2):
            row = [ZERO] * variables
            for edge in range(edges):
                row[edge * len(SHAPES) + shape] = lengths[edge] * normals[edge][coordinate]
            matrix.append(row)
            rhs.append(ZERO)
    return independent_rows(matrix, rhs), matrix, rhs


@lru_cache(maxsize=None)
def reconstruct(template):
    (reduced, reduced_rhs), full_matrix, full_rhs = constraint_system(template)
    variables = len(full_matrix[0])
    dimension = len(reduced)
    solutions = {}
    for basis in itertools.combinations(range(variables), dimension):
        square = [[row[column] for column in basis] for row in reduced]
        values = solve(square, reduced_rhs)
        if values is None or any(value < ZERO for value in values):
            continue
        vector = [ZERO] * variables
        for column, value in zip(basis, values):
            vector[column] = value
        if any(sum((coefficient * value for coefficient, value in zip(row, vector)), ZERO) != rhs
               for row, rhs in zip(full_matrix, full_rhs)):
            raise Reject("reconstructed BFS violates capacity or load equation")
        key = tuple((value.a, value.b) for value in vector)
        solutions.setdefault(key, {"basis": list(basis),
                                   "coordinates": [value.text() for value in vector]})
    return dimension, sorted(solutions.values(), key=lambda item: item["basis"])


def strict_object(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise Reject(f"duplicate JSON field: {key}")
        out[key] = value
    return out


def check(path):
    data = json.loads(Path(path).read_text(), object_pairs_hook=strict_object)
    fields = {"schema_version", "claim_scope", "segment_template_lemma",
              "worm_angle_domain_degrees", "half_turn_action", "templates"}
    if not isinstance(data, dict) or set(data) != fields:
        raise Reject("root fields")
    if data["schema_version"] != "moser-support-bfs-v1":
        raise Reject("schema")
    if data["claim_scope"] != "exact_allocation_polytope_and_partial_angle_probe_only":
        raise Reject("scope escalation")
    if data["segment_template_lemma"] != "base_segment_two_triangles_width_over_two":
        raise Reject("missing direct segment-template proof")
    if data["worm_angle_domain_degrees"] != ["0", "180"]:
        raise Reject("worm angle domain must be full 180-degree quotient")
    action = data["half_turn_action"]
    expected_action = {"motion": "orientation_preserving_rotation_180_about_segment_midpoint",
                       "segment_image": "same_unlabelled_segment",
                       "worm_angle_shift_degrees": "180",
                       "reflection_used": False,
                       "all_translation_boxes_reanchored_by_diameter": True}
    if action != expected_action:
        raise Reject("half-turn action not checked; restore worm domain to 360 degrees")
    supplied = data["templates"]
    if not isinstance(supplied, dict) or set(supplied) != set(TEMPLATES):
        raise Reject("template list")
    report = {}
    for template in TEMPLATES:
        dimension, solutions = reconstruct(template)
        entry = supplied[template]
        if not isinstance(entry, dict) or set(entry) != {"rank", "bases"}:
            raise Reject("template fields")
        bases = [solution["basis"] for solution in solutions]
        if entry["rank"] != dimension or entry["bases"] != bases:
            raise Reject(f"{template} exact BFS mismatch")
        report[template] = {"rank": dimension, "bfs_count": len(solutions)}
    return report


def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--emit":
        document = {"schema_version": "moser-support-bfs-v1",
                    "claim_scope": "exact_allocation_polytope_and_partial_angle_probe_only",
                    "segment_template_lemma": "base_segment_two_triangles_width_over_two",
                    "worm_angle_domain_degrees": ["0", "180"],
                    "half_turn_action": {
                        "motion": "orientation_preserving_rotation_180_about_segment_midpoint",
                        "segment_image": "same_unlabelled_segment",
                        "worm_angle_shift_degrees": "180",
                        "reflection_used": False,
                        "all_translation_boxes_reanchored_by_diameter": True},
                    "templates": {}}
        for template in TEMPLATES:
            dimension, solutions = reconstruct(template)
            document["templates"][template] = {
                "rank": dimension,
                "bases": [solution["basis"] for solution in solutions],
            }
        print(json.dumps(document, indent=2))
        return 0
    try:
        report = check(sys.argv[1])
    except (IndexError, OSError, json.JSONDecodeError, Reject) as error:
        print(f"REJECT: {error}", file=sys.stderr)
        return 1
    print(f"PASS exact support-allocation BFS: {report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
