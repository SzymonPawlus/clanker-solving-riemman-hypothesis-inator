#!/usr/bin/env python3
"""Exact verifier for convex partition lower-bound certificates.

All geometry is performed in oblique coordinates with Fraction arithmetic.
No floating point or symbolic parser is used on the verification path.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations
from pathlib import Path
from typing import Any, Iterable


MAX_FILE_BYTES = 1_000_000
MAX_SCALAR_CHARS = 128
MAX_INTEGER_BITS = 1024
MAX_CELLS = 1000
MAX_VERTICES_PER_CELL = 1000

RATIONAL_RE = re.compile(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?\Z")

Point = tuple[Fraction, Fraction]
Polygon = list[Point]


class CertificateError(ValueError):
    """Raised when a certificate fails a schema or geometric check."""


@dataclass(frozen=True)
class VerificationReport:
    n: int
    triangle_side: Fraction
    cells: int
    maximum_squared_diameter: Fraction

    def as_json(self) -> dict[str, object]:
        return {
            "accepted": True,
            "n": self.n,
            "triangle_side": str(self.triangle_side),
            "cells": self.cells,
            "maximum_squared_diameter": str(self.maximum_squared_diameter),
            "claim": f"s({self.n}) > {self.triangle_side} + 2*sqrt(3)",
            "status": "numerical",
        }


def parse_rational(value: object, path: str) -> Fraction:
    """Parse the certificate's deliberately small rational grammar."""
    if not isinstance(value, str):
        raise CertificateError(f"{path}: expected a rational string")
    if len(value) > MAX_SCALAR_CHARS or RATIONAL_RE.fullmatch(value) is None:
        raise CertificateError(
            f"{path}: expected an integer or fraction string; decimals/expressions are forbidden"
        )
    result = Fraction(value)
    if (
        abs(result.numerator).bit_length() > MAX_INTEGER_BITS
        or result.denominator.bit_length() > MAX_INTEGER_BITS
    ):
        raise CertificateError(f"{path}: rational exceeds the resource bound")
    return result


def parse_point(value: object, path: str) -> Point:
    if not isinstance(value, list) or len(value) != 2:
        raise CertificateError(f"{path}: point must be a two-element list")
    return (parse_rational(value[0], f"{path}[0]"), parse_rational(value[1], f"{path}[1]"))


def cross(a: Point, b: Point, c: Point) -> Fraction:
    """Oriented coordinate-area determinant (positive for a left turn)."""
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def polygon_area2(polygon: Polygon) -> Fraction:
    if len(polygon) < 3:
        return Fraction(0)
    return sum(
        (a[0] * b[1] - a[1] * b[0])
        for a, b in zip(polygon, polygon[1:] + polygon[:1])
    )


def on_segment(a: Point, b: Point, p: Point) -> bool:
    return (
        cross(a, b, p) == 0
        and min(a[0], b[0]) <= p[0] <= max(a[0], b[0])
        and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])
    )


def segments_intersect(a: Point, b: Point, c: Point, d: Point) -> bool:
    o1, o2, o3, o4 = cross(a, b, c), cross(a, b, d), cross(c, d, a), cross(c, d, b)
    if ((o1 > 0 and o2 < 0) or (o1 < 0 and o2 > 0)) and (
        (o3 > 0 and o4 < 0) or (o3 < 0 and o4 > 0)
    ):
        return True
    return (
        (o1 == 0 and on_segment(a, b, c))
        or (o2 == 0 and on_segment(a, b, d))
        or (o3 == 0 and on_segment(c, d, a))
        or (o4 == 0 and on_segment(c, d, b))
    )


def validate_polygon(polygon: Polygon, side: Fraction, path: str) -> None:
    if len(polygon) < 3:
        raise CertificateError(f"{path}: a cell needs at least three vertices")
    if len(polygon) > MAX_VERTICES_PER_CELL:
        raise CertificateError(f"{path}: too many vertices")
    if len(set(polygon)) != len(polygon):
        raise CertificateError(f"{path}: repeated vertices are forbidden")

    for index, (u, v) in enumerate(polygon):
        if u < 0 or v < 0 or u + v > side:
            raise CertificateError(f"{path}[{index}]: vertex lies outside the triangle")

    count = len(polygon)
    for i in range(count):
        a, b = polygon[i], polygon[(i + 1) % count]
        for j in range(i + 1, count):
            # Adjacent edges share an endpoint by design.
            if j == i + 1 or (i == 0 and j == count - 1):
                continue
            c, d = polygon[j], polygon[(j + 1) % count]
            if segments_intersect(a, b, c, d):
                raise CertificateError(f"{path}: polygon is self-intersecting")

    area2 = polygon_area2(polygon)
    if area2 <= 0:
        raise CertificateError(f"{path}: vertices must be counterclockwise with positive area")
    for i in range(count):
        if cross(polygon[i - 1], polygon[i], polygon[(i + 1) % count]) <= 0:
            raise CertificateError(f"{path}: cell must be strictly convex")


def normalize_polygon(polygon: Iterable[Point]) -> Polygon:
    output: Polygon = []
    for point in polygon:
        if not output or point != output[-1]:
            output.append(point)
    if len(output) > 1 and output[0] == output[-1]:
        output.pop()
    return output


def line_intersection(segment_a: Point, segment_b: Point, line_a: Point, line_b: Point) -> Point:
    value_a = cross(line_a, line_b, segment_a)
    value_b = cross(line_a, line_b, segment_b)
    denominator = value_a - value_b
    if denominator == 0:
        raise CertificateError("internal clipping error: parallel crossing segment")
    parameter = value_a / denominator
    return (
        segment_a[0] + parameter * (segment_b[0] - segment_a[0]),
        segment_a[1] + parameter * (segment_b[1] - segment_a[1]),
    )


def clip_convex(subject: Polygon, clip: Polygon) -> Polygon:
    """Intersect two CCW convex polygons by exact half-plane clipping."""
    output = list(subject)
    for line_a, line_b in zip(clip, clip[1:] + clip[:1]):
        if not output:
            break
        input_polygon = output
        output = []
        previous = input_polygon[-1]
        previous_inside = cross(line_a, line_b, previous) >= 0
        for current in input_polygon:
            current_inside = cross(line_a, line_b, current) >= 0
            if current_inside:
                if not previous_inside:
                    output.append(line_intersection(previous, current, line_a, line_b))
                output.append(current)
            elif previous_inside:
                output.append(line_intersection(previous, current, line_a, line_b))
            previous, previous_inside = current, current_inside
        output = normalize_polygon(output)
    return normalize_polygon(output)


def squared_distance(a: Point, b: Point) -> Fraction:
    du, dv = a[0] - b[0], a[1] - b[1]
    return du * du + du * dv + dv * dv


def maximum_squared_diameter(polygon: Polygon) -> Fraction:
    return max(squared_distance(a, b) for a, b in combinations(polygon, 2))


REQUIRED_KEYS = {
    "certificate_version",
    "claim",
    "status",
    "n",
    "triangle_side",
    "coordinate_system",
    "cells",
}


def verify_certificate(data: object) -> VerificationReport:
    if not isinstance(data, dict):
        raise CertificateError("certificate root must be an object")
    keys = set(data)
    if keys != REQUIRED_KEYS:
        missing, extra = sorted(REQUIRED_KEYS - keys), sorted(keys - REQUIRED_KEYS)
        raise CertificateError(f"schema mismatch: missing={missing}, extra={extra}")
    if data["certificate_version"] != 1:
        raise CertificateError("certificate_version must equal 1")
    if data["claim"] != "strict-lower-bound":
        raise CertificateError("claim must equal 'strict-lower-bound'")
    if data["status"] != "numerical":
        raise CertificateError("working certificates must retain status 'numerical'")
    if data["coordinate_system"] != "oblique-euclidean-60deg":
        raise CertificateError("unsupported coordinate_system")

    n = data["n"]
    if isinstance(n, bool) or not isinstance(n, int) or n < 2:
        raise CertificateError("n must be an integer at least 2")
    side = parse_rational(data["triangle_side"], "triangle_side")
    if side <= 0:
        raise CertificateError("triangle_side must be positive")

    raw_cells = data["cells"]
    if not isinstance(raw_cells, list):
        raise CertificateError("cells must be a list")
    if len(raw_cells) != n - 1:
        raise CertificateError(f"expected exactly n-1={n - 1} cells")
    if len(raw_cells) > MAX_CELLS:
        raise CertificateError("too many cells")

    cells: list[Polygon] = []
    for cell_index, raw_cell in enumerate(raw_cells):
        if not isinstance(raw_cell, list):
            raise CertificateError(f"cells[{cell_index}]: expected a vertex list")
        cell = [parse_point(point, f"cells[{cell_index}][{i}]") for i, point in enumerate(raw_cell)]
        validate_polygon(cell, side, f"cells[{cell_index}]")
        cells.append(cell)

    total_area2 = sum((polygon_area2(cell) for cell in cells), Fraction(0))
    if total_area2 != side * side:
        raise CertificateError(
            f"cell area sum {total_area2} does not equal triangle area {side * side} (doubled coordinates)"
        )

    for (first_index, first), (second_index, second) in combinations(enumerate(cells), 2):
        intersection = clip_convex(first, second)
        intersection_area2 = abs(polygon_area2(intersection))
        if intersection_area2 != 0:
            raise CertificateError(
                f"cells[{first_index}] and cells[{second_index}] overlap with positive area"
            )

    diameters = [maximum_squared_diameter(cell) for cell in cells]
    maximum = max(diameters)
    if maximum >= 4:
        raise CertificateError(f"maximum squared cell diameter is {maximum}, not strictly below 4")

    return VerificationReport(n=n, triangle_side=side, cells=len(cells), maximum_squared_diameter=maximum)


def load_certificate(path: Path) -> object:
    if path.stat().st_size > MAX_FILE_BYTES:
        raise CertificateError("certificate file exceeds the resource bound")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise CertificateError(f"cannot read JSON certificate: {error}") from error


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    try:
        report = verify_certificate(load_certificate(args.certificate))
    except (CertificateError, OSError) as error:
        print(json.dumps({"accepted": False, "error": str(error)}, indent=2))
        return 1
    print(json.dumps(report.as_json(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
