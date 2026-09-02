#!/usr/bin/env python3
"""Exact verifier for Q(sqrt 3) convex *cover* certificates of an equilateral triangle.

This is an independent reimplementation, not a port. It differs from the merged
rational verifier in `experiments/circle-packing-partitions/partitioncheck.py` in
two ways that proposal J needs:

  * coordinates live in the real quadratic field `Q(sqrt 3)`, so the *exact*
    algebraic critical side `d* = 2 + 2 sqrt(3)` is representable;
  * the diameter test is parameterised. `--mode nonstrict` accepts squared
    diameter `<= 4`; `--mode strict` demands `< 4`. Only a strict certificate
    supports a pigeonhole lower bound.

Coordinates are oblique: `(u, v) -> u*(1,0) + v*(1/2, sqrt(3)/2)`. In these
coordinates the triangle of side `d` is `T_d = {u >= 0, v >= 0, u + v <= d}` and
squared Euclidean distance is `q(du, dv) = du^2 + du*dv + dv^2`.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations
from pathlib import Path
from typing import Any, Sequence

from qsqrt3 import Q3

MAX_FILE_BYTES = 2_000_000
MAX_SCALAR_CHARS = 128
MAX_INTEGER_BITS = 2048
MAX_CELLS = 2000
MAX_VERTICES_PER_CELL = 2000

RATIONAL_RE = re.compile(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?\Z")

Point = tuple[Q3, Q3]
Polygon = list[Point]


class CertificateError(ValueError):
    """Raised when a certificate fails a schema or geometric check."""


# --------------------------------------------------------------------------
# parsing
# --------------------------------------------------------------------------

def parse_rational(value: object, path: str) -> Fraction:
    if not isinstance(value, str):
        raise CertificateError(f"{path}: expected a rational string")
    if len(value) > MAX_SCALAR_CHARS or RATIONAL_RE.fullmatch(value) is None:
        raise CertificateError(
            f"{path}: expected an integer or fraction string; "
            "decimals and expressions are forbidden"
        )
    result = Fraction(value)
    if (
        abs(result.numerator).bit_length() > MAX_INTEGER_BITS
        or result.denominator.bit_length() > MAX_INTEGER_BITS
    ):
        raise CertificateError(f"{path}: rational exceeds the resource bound")
    return result


def parse_q3(value: object, path: str) -> Q3:
    """`["a", "b"]` denotes `a + b*sqrt(3)` with `a`, `b` exact rationals."""
    if not isinstance(value, list) or len(value) != 2:
        raise CertificateError(f"{path}: a Q(sqrt 3) scalar must be a two-element list")
    return Q3(parse_rational(value[0], f"{path}[0]"), parse_rational(value[1], f"{path}[1]"))


def parse_point(value: object, path: str) -> Point:
    if not isinstance(value, list) or len(value) != 2:
        raise CertificateError(f"{path}: a point must be a two-element list")
    return (parse_q3(value[0], f"{path}[0]"), parse_q3(value[1], f"{path}[1]"))


def q3_text(value: Q3) -> list[str]:
    return [str(value.a), str(value.b)]


def point_text(p: Point) -> list[list[str]]:
    return [q3_text(p[0]), q3_text(p[1])]


# --------------------------------------------------------------------------
# exact geometry over Q(sqrt 3)
# --------------------------------------------------------------------------

def cross(o: Point, a: Point, b: Point) -> Q3:
    """Oblique-coordinate orientation determinant; positive means a left turn.

    The map to Euclidean coordinates has determinant sqrt(3)/2 > 0, so the sign
    of this quantity is the true Euclidean orientation.
    """
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def doubled_area(polygon: Polygon) -> Q3:
    """Twice the signed area in oblique coordinates (the shoelace sum)."""
    total = Q3(0, 0)
    for p, q in zip(polygon, polygon[1:] + polygon[:1]):
        total = total + (p[0] * q[1] - p[1] * q[0])
    return total


def squared_distance(a: Point, b: Point) -> Q3:
    du, dv = a[0] - b[0], a[1] - b[1]
    return du * du + du * dv + dv * dv


def max_squared_diameter(polygon: Polygon) -> Q3:
    """For a convex polygon the diameter is attained at a vertex pair."""
    best = Q3(0, 0)
    for a, b in combinations(polygon, 2):
        d = squared_distance(a, b)
        if d > best:
            best = d
    return best


def line_intersection(p: Point, q: Point, a: Point, b: Point) -> Point:
    """Intersection of segment-line pq with the line through a and b."""
    r = (q[0] - p[0], q[1] - p[1])
    s = (b[0] - a[0], b[1] - a[1])
    denom = r[0] * s[1] - r[1] * s[0]
    if denom == 0:
        raise CertificateError("degenerate clip: parallel lines")
    w = (a[0] - p[0], a[1] - p[1])
    t = (w[0] * s[1] - w[1] * s[0]) / denom
    return (p[0] + r[0] * t, p[1] + r[1] * t)


def clip_convex(subject: Polygon, clip: Polygon) -> Polygon:
    """Sutherland-Hodgman clipping. Both polygons must be convex and CCW."""
    output = list(subject)
    for a, b in zip(clip, clip[1:] + clip[:1]):
        if not output:
            return []
        source, output = output, []
        for current, previous in zip(source, source[-1:] + source[:-1]):
            cur_in = cross(a, b, current) >= 0
            prev_in = cross(a, b, previous) >= 0
            if cur_in:
                if not prev_in:
                    output.append(line_intersection(previous, current, a, b))
                output.append(current)
            elif prev_in:
                output.append(line_intersection(previous, current, a, b))
    return output


def scale_polygon(polygon: Polygon, factor: Q3) -> Polygon:
    """Dilation about the triangle vertex `A = (0, 0)`, which fixes the corner."""
    return [(factor * x, factor * y) for x, y in polygon]


# --------------------------------------------------------------------------
# structural checks
# --------------------------------------------------------------------------

def validate_cell(polygon: Polygon, side: Q3, path: str) -> None:
    if len(polygon) < 3:
        raise CertificateError(f"{path}: a cell needs at least three vertices")
    if len(polygon) > MAX_VERTICES_PER_CELL:
        raise CertificateError(f"{path}: too many vertices")
    seen: list[Point] = []
    for p in polygon:
        if any(p[0] == s[0] and p[1] == s[1] for s in seen):
            raise CertificateError(f"{path}: repeated vertices are forbidden")
        seen.append(p)
    for index, (u, v) in enumerate(polygon):
        if u.sign() < 0 or v.sign() < 0 or (u + v) > side:
            raise CertificateError(f"{path}[{index}]: vertex lies outside the triangle")
    size = len(polygon)
    for i in range(size):
        turn = cross(polygon[i], polygon[(i + 1) % size], polygon[(i + 2) % size])
        if turn.sign() <= 0:
            raise CertificateError(
                f"{path}: vertices must be strictly convex and counterclockwise"
            )


@dataclass(frozen=True)
class Report:
    n: int
    side: Q3
    cells: int
    max_squared_diameter: Q3
    mode: str

    def as_json(self) -> dict[str, object]:
        excess = self.max_squared_diameter - Q3(4, 0)
        return {
            "accepted": True,
            "n": self.n,
            "cells": self.cells,
            "mode": self.mode,
            "triangle_side": str(self.side),
            "triangle_side_approx": self.side.approx(),
            "max_squared_diameter": str(self.max_squared_diameter),
            "max_squared_diameter_minus_4": str(excess),
            "is_covered": True,
            "status": "numerical",
        }


def verify(data: object, mode: str) -> Report:
    if mode not in {"strict", "nonstrict"}:
        raise CertificateError("mode must be 'strict' or 'nonstrict'")
    if not isinstance(data, dict):
        raise CertificateError("certificate must be a JSON object")
    if data.get("certificate_version") != 1:
        raise CertificateError("unsupported certificate_version")
    if data.get("coordinate_system") != "oblique-euclidean-60deg":
        raise CertificateError("unsupported coordinate_system")

    n = data.get("n")
    if not isinstance(n, int) or n < 2:
        raise CertificateError("n must be an integer at least 2")

    side = parse_q3(data.get("triangle_side"), "triangle_side")
    if side.sign() <= 0:
        raise CertificateError("triangle_side must be positive")

    raw_cells = data.get("cells")
    if not isinstance(raw_cells, list) or not raw_cells:
        raise CertificateError("cells must be a non-empty list")
    if len(raw_cells) > MAX_CELLS:
        raise CertificateError("too many cells")
    if len(raw_cells) != n - 1:
        raise CertificateError(
            f"pigeonhole needs exactly n-1 = {n - 1} cells, found {len(raw_cells)}"
        )

    cells: list[Polygon] = []
    for i, raw in enumerate(raw_cells):
        if not isinstance(raw, list):
            raise CertificateError(f"cells[{i}]: expected a list of points")
        cell = [parse_point(p, f"cells[{i}][{j}]") for j, p in enumerate(raw)]
        validate_cell(cell, side, f"cells[{i}]")
        cells.append(cell)

    # Coverage. The cells sit inside T_side, meet only in zero area, and their
    # areas sum to the area of T_side. Hence the open complement inside the
    # triangle has zero area and is therefore empty, so the union contains the
    # interior; being closed it contains the whole closed triangle.
    total = Q3(0, 0)
    for cell in cells:
        total = total + doubled_area(cell)
    triangle_doubled_area = side * side
    if total != triangle_doubled_area:
        raise CertificateError(
            f"cell areas sum to {total} but the triangle has {triangle_doubled_area} "
            "(doubled oblique area)"
        )
    for i, j in combinations(range(len(cells)), 2):
        overlap = clip_convex(cells[i], cells[j])
        if overlap and doubled_area(overlap) != Q3(0, 0):
            raise CertificateError(f"cells[{i}] and cells[{j}] overlap in positive area")

    diameters = [max_squared_diameter(cell) for cell in cells]
    worst = max(diameters)
    four = Q3(4, 0)
    if mode == "strict" and not worst < four:
        raise CertificateError(
            f"max squared cell diameter is {worst}, not strictly below 4"
        )
    if mode == "nonstrict" and worst > four:
        raise CertificateError(f"max squared cell diameter is {worst}, above 4")

    return Report(n=n, side=side, cells=len(cells), max_squared_diameter=worst, mode=mode)


def scaled_certificate(data: dict[str, Any], factor: Fraction) -> dict[str, Any]:
    """Apply the dilation of proposal J's scaling step to a whole certificate."""
    lam = Q3(factor, 0)
    side = parse_q3(data["triangle_side"], "triangle_side")
    cells = [
        [parse_point(p, "p") for p in raw]
        for raw in data["cells"]
    ]
    return {
        "certificate_version": 1,
        "claim": "strict-cover",
        "status": "numerical",
        "n": data["n"],
        "triangle_side": q3_text(lam * side),
        "coordinate_system": "oblique-euclidean-60deg",
        "scaled_from": data.get("name", "unnamed"),
        "scale_factor": str(factor),
        "cells": [[point_text(p) for p in scale_polygon(cell, lam)] for cell in cells],
    }


def load(path: Path) -> Any:
    if path.stat().st_size > MAX_FILE_BYTES:
        raise CertificateError("certificate file is too large")
    return json.loads(path.read_text(encoding="utf-8"))


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--mode", choices=("strict", "nonstrict"), default="strict")
    parser.add_argument(
        "--scale",
        default=None,
        help="rational lambda; verify the dilated certificate in strict mode too",
    )
    args = parser.parse_args(argv)

    data = load(args.certificate)
    try:
        report = verify(data, args.mode)
    except CertificateError as error:
        print(json.dumps({"accepted": False, "error": str(error)}, indent=2))
        return 1
    output: dict[str, object] = {"base": report.as_json()}

    if args.scale is not None:
        factor = Fraction(args.scale)
        if not 0 < factor < 1:
            print(json.dumps({"accepted": False, "error": "scale must lie in (0,1)"}))
            return 1
        try:
            scaled_report = verify(scaled_certificate(data, factor), "strict")
        except CertificateError as error:
            print(json.dumps({"accepted": False, "error": f"scaled: {error}"}, indent=2))
            return 1
        output["scaled"] = scaled_report.as_json()
        output["scaled"]["scale_factor"] = str(factor)
        output["scaled"]["implies"] = (
            f"d({report.n}) > {scaled_report.side} = {scaled_report.side.approx()}"
        )
    print(json.dumps(output, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
