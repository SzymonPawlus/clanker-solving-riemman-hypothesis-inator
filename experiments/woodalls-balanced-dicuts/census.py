#!/usr/bin/env python3
"""Run the deterministic fixed-topological-order DAG census."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import time

from balanced_dicuts import (
    OddBergeCycle,
    brute_force_unbalanced_submatrix,
    dibonds,
    find_odd_berge_cycle,
    fixed_order_dags,
    source_sink_reachability_is_forest,
    validate_odd_berge_cycle,
)


def serialise_witness(arcs, edges, witness: OddBergeCycle):
    return {
        "order": witness.order,
        "arc_vertices": [list(arcs[index]) for index in witness.vertices],
        "dibonds": [
            [list(arcs[arc_index]) for arc_index in sorted(edges[edge_index])]
            for edge_index in witness.hyperedge_indices
        ],
    }


def run(max_n: int, cross_check_through: int):
    started = time.monotonic()
    output = {
        "status": "numerical",
        "scope": {
            "max_n": max_n,
            "fixed_topological_order": True,
            "isomorphism_free": False,
            "cross_check_through": cross_check_through,
        },
        "by_n": [],
        "first_unbalanced": None,
        "first_forest_reachability_unbalanced": None,
    }

    for n in range(1, max_n + 1):
        stats = {
            "n": n,
            "instances": 0,
            "instances_with_dicuts": 0,
            "unbalanced_dibond_hypergraphs": 0,
            "forest_reachability_instances": 0,
            "forest_reachability_unbalanced": 0,
        }
        for arcs in fixed_order_dags(n):
            stats["instances"] += 1
            edges = dibonds(n, arcs)
            if edges:
                stats["instances_with_dicuts"] += 1
            witness = find_odd_berge_cycle(range(len(arcs)), edges)
            unbalanced = witness is not None

            if n <= cross_check_through:
                brute_result = brute_force_unbalanced_submatrix(range(len(arcs)), edges)
                if unbalanced != brute_result:
                    raise AssertionError(
                        f"balancedness checkers disagree for n={n}, arcs={arcs}"
                    )
            if witness is not None and not validate_odd_berge_cycle(
                range(len(arcs)), edges, witness
            ):
                raise AssertionError(f"invalid emitted witness for n={n}, arcs={arcs}")

            if unbalanced:
                stats["unbalanced_dibond_hypergraphs"] += 1
                if output["first_unbalanced"] is None:
                    output["first_unbalanced"] = {
                        "n": n,
                        "arcs": [list(arc) for arc in arcs],
                        "witness": serialise_witness(arcs, edges, witness),
                    }

            forest = source_sink_reachability_is_forest(n, arcs)
            if forest:
                stats["forest_reachability_instances"] += 1
                if unbalanced:
                    stats["forest_reachability_unbalanced"] += 1
                    if output["first_forest_reachability_unbalanced"] is None:
                        output["first_forest_reachability_unbalanced"] = {
                            "n": n,
                            "arcs": [list(arc) for arc in arcs],
                            "witness": serialise_witness(arcs, edges, witness),
                        }
        output["by_n"].append(stats)

    output["instances_total"] = sum(row["instances"] for row in output["by_n"])
    output["elapsed_seconds"] = round(time.monotonic() - started, 6)
    return output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=6)
    parser.add_argument("--cross-check-through", type=int, default=5)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.max_n < 1 or args.max_n > 6:
        parser.error("--max-n must lie between 1 and the declared scope limit 6")
    if not 0 <= args.cross_check_through <= args.max_n:
        parser.error("--cross-check-through must lie between 0 and --max-n")

    result = run(args.max_n, args.cross_check_through)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(rendered, end="")
    else:
        args.output.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
