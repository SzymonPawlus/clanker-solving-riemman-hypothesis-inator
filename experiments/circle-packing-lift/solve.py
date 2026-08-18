"""High-precision Newton lift of a numerically selected contact system.

This is still numerical: the active set and independent rows were selected from
floats, and Decimal Newton is not an interval proof. Its output is a candidate for
the later interval/algebraic certification stage, never a certificate by itself.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, localcontext
from typing import Sequence

from lift import Candidate, ContactGraph, rank_diagnostic


@dataclass(frozen=True)
class SolvedCandidate:
    point_ids: tuple[int, ...]
    points: tuple[tuple[Decimal, Decimal], ...]
    m: Decimal
    equation_labels: tuple[str, ...]
    iterations: int
    selected_residual: Decimal
    all_active_residual: Decimal


def _evaluate(
    label: str,
    values: Sequence[Decimal],
    positions: dict[int, int],
    sqrt3: Decimal,
) -> tuple[Decimal, list[Decimal]]:
    row = [Decimal(0)] * len(values)
    kind, rest = label.split(":", 1)
    if kind == "pair":
        i, j = map(int, rest.split("-"))
        pi, pj = positions[i], positions[j]
        xi, yi = values[2 * pi : 2 * pi + 2]
        xj, yj = values[2 * pj : 2 * pj + 2]
        m = values[-1]
        dx, dy = xi - xj, yi - yj
        row[2 * pi] = 2 * dx
        row[2 * pi + 1] = 2 * dy
        row[2 * pj] = -2 * dx
        row[2 * pj + 1] = -2 * dy
        row[-1] = -2 * m
        return dx * dx + dy * dy - m * m, row

    point_text, wall = rest.split(":")
    point_id = int(point_text)
    position = positions[point_id]
    x, y = values[2 * position : 2 * position + 2]
    if wall == "bottom":
        row[2 * position + 1] = Decimal(1)
        return y, row
    if wall == "left":
        row[2 * position] = sqrt3
        row[2 * position + 1] = Decimal(-1)
        return sqrt3 * x - y, row
    if wall == "right":
        row[2 * position] = -sqrt3
        row[2 * position + 1] = Decimal(-1)
        return sqrt3 * (1 - x) - y, row
    raise ValueError(f"unknown equation label {label!r}")


def _linear_solve(matrix: Sequence[Sequence[Decimal]], rhs: Sequence[Decimal]) -> list[Decimal]:
    """Dense Decimal Gaussian elimination with full row elimination."""
    n = len(rhs)
    if len(matrix) != n or any(len(row) != n for row in matrix):
        raise ValueError("Newton Jacobian must be square")
    augmented = [list(matrix[i]) + [rhs[i]] for i in range(n)]
    for column in range(n):
        pivot_row = max(range(column, n), key=lambda i: abs(augmented[i][column]))
        if augmented[pivot_row][column] == 0:
            raise ArithmeticError(f"singular Newton Jacobian at column {column}")
        augmented[column], augmented[pivot_row] = augmented[pivot_row], augmented[column]
        pivot = augmented[column][column]
        for j in range(column, n + 1):
            augmented[column][j] /= pivot
        for i in range(n):
            if i == column:
                continue
            factor = augmented[i][column]
            if factor == 0:
                continue
            for j in range(column, n + 1):
                augmented[i][j] -= factor * augmented[column][j]
    return [augmented[i][-1] for i in range(n)]


def solve_candidate(
    candidate: Candidate,
    graph: ContactGraph,
    point_ids: Sequence[int],
    *,
    digits: int = 100,
    max_iterations: int = 20,
) -> SolvedCandidate:
    """Newton-solve an independently selected square subsystem near `candidate`."""
    if digits < 40:
        raise ValueError("use at least 40 decimal digits")
    ids = tuple(sorted(point_ids))
    diagnostic = rank_diagnostic(candidate, graph, ids)
    if not diagnostic.full_column_rank:
        raise ValueError(
            f"contact Jacobian has rank {diagnostic.rank} but {diagnostic.columns} columns"
        )
    selected_labels = tuple(diagnostic.row_labels[i] for i in diagnostic.independent_rows)
    positions = {point_id: position for position, point_id in enumerate(ids)}

    with localcontext() as context:
        context.prec = digits
        sqrt3 = Decimal(3).sqrt()
        values: list[Decimal] = []
        for point_id in ids:
            values.extend(Decimal(str(value)) for value in candidate.points[point_id])
        values.append(Decimal(str(candidate.m)))
        target = Decimal(10) ** (-(digits - 20))

        selected_residual = Decimal("Infinity")
        iteration = 0
        for iteration in range(max_iterations + 1):
            evaluated = [_evaluate(label, values, positions, sqrt3) for label in selected_labels]
            residuals = [item[0] for item in evaluated]
            selected_residual = max(map(abs, residuals), default=Decimal(0))
            if selected_residual <= target:
                break
            if iteration == max_iterations:
                raise ArithmeticError(
                    f"Newton did not reach {target} in {max_iterations} iterations; "
                    f"residual is {selected_residual}"
                )
            step = _linear_solve([item[1] for item in evaluated], [-value for value in residuals])
            values = [value + delta for value, delta in zip(values, step, strict=True)]

        all_residuals = [
            abs(_evaluate(label, values, positions, sqrt3)[0])
            for label in diagnostic.row_labels
        ]
        points = tuple(
            (values[2 * position], values[2 * position + 1])
            for position in range(len(ids))
        )
        return SolvedCandidate(
            point_ids=ids,
            points=points,
            m=values[-1],
            equation_labels=selected_labels,
            iterations=iteration,
            selected_residual=selected_residual,
            all_active_residual=max(all_residuals, default=Decimal(0)),
        )
