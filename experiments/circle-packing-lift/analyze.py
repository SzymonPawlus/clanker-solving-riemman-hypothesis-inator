#!/usr/bin/env python3
"""Print contact and Jacobian diagnostics for search candidates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from lift import (
    constraint_degrees,
    load_candidate,
    obvious_rattlers,
    rank_diagnostic,
    signatures_stable,
    tolerance_sweep,
)
from solve import solve_candidate

DEFAULT_TOLERANCES = (1e-6, 1e-8, 1e-10)


def analyse(path: Path, tolerances=DEFAULT_TOLERANCES) -> dict:
    candidate = load_candidate(path)
    graphs = tolerance_sweep(candidate, tolerances)
    graph = graphs[-1]
    rattlers = obvious_rattlers(candidate, graph)
    core_ids = tuple(i for i in range(candidate.n) if i not in rattlers)
    full = rank_diagnostic(candidate, graph)
    core = rank_diagnostic(candidate, graph, core_ids)
    solved = None
    if signatures_stable(graphs) and core.full_column_rank:
        lifted = solve_candidate(candidate, graph, core_ids)
        solved = {
            "digits": 100,
            "iterations": lifted.iterations,
            "m": str(lifted.m),
            "selected_residual": str(lifted.selected_residual),
            "all_active_residual": str(lifted.all_active_residual),
            "status": "numerical high-precision candidate; not a certificate",
        }
    return {
        "source": str(path),
        "n": candidate.n,
        "m": candidate.m,
        "tolerances": list(tolerances),
        "signature_stable": signatures_stable(graphs),
        "pair_contacts": len(graph.pairs),
        "wall_contacts": len(graph.walls),
        "constraint_degrees": list(constraint_degrees(candidate, graph)),
        "obvious_rattlers": list(rattlers),
        "minimum_pair_gap": graph.min_pair_gap,
        "minimum_wall_slack": graph.min_wall_slack,
        "full_jacobian": {
            "rows": len(full.row_labels),
            "columns": full.columns,
            "rank": full.rank,
            "independent_equations": [full.row_labels[i] for i in full.independent_rows],
        },
        "core_jacobian": {
            "point_ids": list(core.point_ids),
            "rows": len(core.row_labels),
            "columns": core.columns,
            "rank": core.rank,
            "full_column_rank": core.full_column_rank,
            "independent_equations": [core.row_labels[i] for i in core.independent_rows],
        },
        "decimal_newton": solved,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidates", nargs="+", type=Path)
    args = parser.parse_args()
    print(json.dumps([analyse(path) for path in args.candidates], indent=2))


if __name__ == "__main__":
    main()
