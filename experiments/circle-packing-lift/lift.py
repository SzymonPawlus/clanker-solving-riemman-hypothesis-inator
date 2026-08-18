"""Numerical contact diagnostics for circle-packing search output.

This module deliberately uses only the Python standard library.  It reads floats
and produces numerical diagnostics; it is not an exact verifier.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

SQRT3 = math.sqrt(3.0)
WALL_NAMES = ("bottom", "left", "right")


@dataclass(frozen=True)
class Candidate:
    n: int
    m: float
    points: tuple[tuple[float, float], ...]
    source: str


@dataclass(frozen=True)
class PairContact:
    i: int
    j: int
    gap: float

    @property
    def label(self) -> str:
        return f"pair:{self.i}-{self.j}"


@dataclass(frozen=True)
class WallContact:
    i: int
    wall: str
    slack: float

    @property
    def label(self) -> str:
        return f"wall:{self.i}:{self.wall}"


@dataclass(frozen=True)
class ContactGraph:
    tolerance: float
    pairs: tuple[PairContact, ...]
    walls: tuple[WallContact, ...]
    min_pair_gap: float
    min_wall_slack: float

    @property
    def signature(self) -> tuple[tuple[int, int], tuple[tuple[int, str], ...]]:
        return (
            tuple((edge.i, edge.j) for edge in self.pairs),
            tuple((contact.i, contact.wall) for contact in self.walls),
        )


@dataclass(frozen=True)
class RankDiagnostic:
    point_ids: tuple[int, ...]
    row_labels: tuple[str, ...]
    rank: int
    columns: int
    independent_rows: tuple[int, ...]

    @property
    def full_column_rank(self) -> bool:
        return self.rank == self.columns


def load_candidate(path: str | Path) -> Candidate:
    source = Path(path)
    data = json.loads(source.read_text())
    n = data["n"]
    points = tuple(tuple(map(float, point)) for point in data["unit_triangle_points"])
    m = float(data["m_min_pairwise_distance_unit_triangle"])
    if not isinstance(n, int) or isinstance(n, bool) or n < 2:
        raise ValueError(f"n must be an integer at least 2, got {n!r}")
    if len(points) != n or any(len(point) != 2 for point in points):
        raise ValueError(f"n={n}, but the point array has the wrong shape")
    if not math.isfinite(m) or m <= 0:
        raise ValueError(f"minimum separation must be finite and positive, got {m!r}")
    if any(not math.isfinite(value) for point in points for value in point):
        raise ValueError("all coordinates must be finite")
    return Candidate(n=n, m=m, points=points, source=str(source))


def wall_slacks(point: tuple[float, float]) -> tuple[float, float, float]:
    """Perpendicular signed slacks to bottom, left, and right triangle edges."""
    x, y = point
    return (
        y,
        (SQRT3 * x - y) / 2.0,
        (SQRT3 * (1.0 - x) - y) / 2.0,
    )


def extract_contacts(candidate: Candidate, tolerance: float) -> ContactGraph:
    if not math.isfinite(tolerance) or tolerance <= 0:
        raise ValueError("tolerance must be finite and positive")
    pairs: list[PairContact] = []
    all_pair_gaps: list[float] = []
    for i in range(candidate.n):
        for j in range(i + 1, candidate.n):
            gap = math.dist(candidate.points[i], candidate.points[j]) - candidate.m
            all_pair_gaps.append(gap)
            if abs(gap) <= tolerance:
                pairs.append(PairContact(i, j, gap))

    walls: list[WallContact] = []
    all_wall_slacks: list[float] = []
    for i, point in enumerate(candidate.points):
        for wall, slack in zip(WALL_NAMES, wall_slacks(point), strict=True):
            all_wall_slacks.append(slack)
            if abs(slack) <= tolerance:
                walls.append(WallContact(i, wall, slack))

    return ContactGraph(
        tolerance=tolerance,
        pairs=tuple(pairs),
        walls=tuple(walls),
        min_pair_gap=min(all_pair_gaps),
        min_wall_slack=min(all_wall_slacks),
    )


def tolerance_sweep(
    candidate: Candidate, tolerances: Iterable[float]
) -> tuple[ContactGraph, ...]:
    values = tuple(tolerances)
    if not values:
        raise ValueError("at least one tolerance is required")
    return tuple(extract_contacts(candidate, tolerance) for tolerance in values)


def signatures_stable(graphs: Sequence[ContactGraph]) -> bool:
    return bool(graphs) and all(graph.signature == graphs[0].signature for graph in graphs[1:])


def constraint_degrees(candidate: Candidate, graph: ContactGraph) -> tuple[int, ...]:
    degrees = [0] * candidate.n
    for edge in graph.pairs:
        degrees[edge.i] += 1
        degrees[edge.j] += 1
    for contact in graph.walls:
        degrees[contact.i] += 1
    return tuple(degrees)


def obvious_rattlers(candidate: Candidate, graph: ContactGraph) -> tuple[int, ...]:
    """Points with no active constraint at all.

    This intentionally does not call every degree-1/2 point a rattler; degree is not
    a sound rigidity criterion.  Zero-contact points are the narrow safe diagnostic.
    """
    return tuple(i for i, degree in enumerate(constraint_degrees(candidate, graph)) if degree == 0)


def jacobian(
    candidate: Candidate,
    graph: ContactGraph,
    point_ids: Iterable[int] | None = None,
) -> tuple[tuple[tuple[float, ...], ...], tuple[str, ...], tuple[int, ...]]:
    ids = tuple(sorted(range(candidate.n) if point_ids is None else point_ids))
    if len(set(ids)) != len(ids) or any(i < 0 or i >= candidate.n for i in ids):
        raise ValueError("point_ids must be distinct valid point indices")
    positions = {point_id: position for position, point_id in enumerate(ids)}
    ncols = 2 * len(ids) + 1  # x,y for every retained point, followed by m
    rows: list[tuple[float, ...]] = []
    labels: list[str] = []

    for edge in graph.pairs:
        if edge.i not in positions or edge.j not in positions:
            continue
        xi, yi = candidate.points[edge.i]
        xj, yj = candidate.points[edge.j]
        row = [0.0] * ncols
        ii, jj = positions[edge.i], positions[edge.j]
        row[2 * ii] = 2.0 * (xi - xj)
        row[2 * ii + 1] = 2.0 * (yi - yj)
        row[2 * jj] = -row[2 * ii]
        row[2 * jj + 1] = -row[2 * ii + 1]
        row[-1] = -2.0 * candidate.m
        rows.append(tuple(row))
        labels.append(edge.label)

    wall_gradients = {
        "bottom": (0.0, 1.0),
        "left": (SQRT3, -1.0),
        "right": (-SQRT3, -1.0),
    }
    for contact in graph.walls:
        if contact.i not in positions:
            continue
        row = [0.0] * ncols
        position = positions[contact.i]
        row[2 * position], row[2 * position + 1] = wall_gradients[contact.wall]
        rows.append(tuple(row))
        labels.append(contact.label)

    return tuple(rows), tuple(labels), ids


def matrix_rank(matrix: Sequence[Sequence[float]], relative_tolerance: float = 1e-10) -> int:
    """Numerical rank by scaled Gaussian elimination, for diagnostics only."""
    rows = [list(map(float, row)) for row in matrix]
    if not rows:
        return 0
    ncols = len(rows[0])
    if any(len(row) != ncols for row in rows):
        raise ValueError("matrix rows must have equal length")
    scale = max(abs(value) for row in rows for value in row)
    threshold = relative_tolerance * max(1.0, scale)
    pivot_row = 0
    for column in range(ncols):
        if pivot_row == len(rows):
            break
        best = max(range(pivot_row, len(rows)), key=lambda index: abs(rows[index][column]))
        if abs(rows[best][column]) <= threshold:
            continue
        rows[pivot_row], rows[best] = rows[best], rows[pivot_row]
        pivot = rows[pivot_row][column]
        for j in range(column, ncols):
            rows[pivot_row][j] /= pivot
        for i, row in enumerate(rows):
            if i == pivot_row:
                continue
            factor = row[column]
            if abs(factor) <= threshold:
                continue
            for j in range(column, ncols):
                row[j] -= factor * rows[pivot_row][j]
        pivot_row += 1
    return pivot_row


def independent_row_indices(
    matrix: Sequence[Sequence[float]], relative_tolerance: float = 1e-10
) -> tuple[int, ...]:
    selected: list[int] = []
    selected_rows: list[Sequence[float]] = []
    rank = 0
    for index, row in enumerate(matrix):
        new_rank = matrix_rank((*selected_rows, row), relative_tolerance)
        if new_rank > rank:
            selected.append(index)
            selected_rows.append(row)
            rank = new_rank
    return tuple(selected)


def rank_diagnostic(
    candidate: Candidate,
    graph: ContactGraph,
    point_ids: Iterable[int] | None = None,
    relative_tolerance: float = 1e-10,
) -> RankDiagnostic:
    rows, labels, ids = jacobian(candidate, graph, point_ids)
    independent = independent_row_indices(rows, relative_tolerance)
    columns = 2 * len(ids) + 1
    return RankDiagnostic(
        point_ids=ids,
        row_labels=labels,
        rank=len(independent),
        columns=columns,
        independent_rows=independent,
    )
