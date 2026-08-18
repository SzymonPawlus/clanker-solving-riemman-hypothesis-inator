#!/usr/bin/env python3
"""Checkpointed deterministic sample of the smallest rho=4 ACZ family."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
from time import monotonic

from acz import acz_route_witness, encode_graph, m1_bases, minimum_dicut, random_rho4
from independent_verify import bases_by_sink_subsets, route_witness_sets


def masks_to_sets(bases: tuple[int, ...]) -> frozenset[frozenset[int]]:
    return frozenset(
        frozenset(position for position in range(12) if base & (1 << position))
        for base in bases
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start-seed", type=int, default=0)
    parser.add_argument("--count", type=int, default=100)
    parser.add_argument("--checkpoint", type=Path, default=Path(__file__).with_name("checkpoint.json"))
    parser.add_argument("--independent-every", type=int, default=10)
    parser.add_argument("--simple", action="store_true")
    parser.add_argument("--source-count", type=int, default=12)
    args = parser.parse_args()

    started = monotonic()
    records = []
    failure = None
    for offset in range(args.count):
        seed = args.start_seed + offset
        graph = random_rho4(seed, source_count=args.source_count, simple=args.simple)
        bases = m1_bases(graph)
        witness = acz_route_witness(bases)
        graph_id = hashlib.sha256(repr(sorted(graph.arcs)).encode()).hexdigest()
        record = {
            "seed": seed,
            "graph_sha256": graph_id,
            "tau": minimum_dicut(graph),
            "base_count": len(bases),
            "route_witness": witness is not None,
        }
        if offset % args.independent_every == 0 or witness is None:
            independent_bases = bases_by_sink_subsets(graph)
            if independent_bases != masks_to_sets(bases):
                raise AssertionError(f"M1 implementations disagree at seed {seed}")
            independent_witness = route_witness_sets(independent_bases, frozenset(range(12)))
            if (independent_witness is not None) != (witness is not None):
                raise AssertionError(f"route implementations disagree at seed {seed}")
            record["independently_verified"] = True
        records.append(record)
        if witness is None:
            failure = encode_graph(graph)
            failure["seed"] = seed
            break
        args.checkpoint.write_text(
            json.dumps(
                {
                    "status": "running",
                    "start_seed": args.start_seed,
                    "requested_count": args.count,
                    "completed_count": len(records),
                    "records": records,
                    "elapsed_seconds": monotonic() - started,
                },
                indent=2,
                sort_keys=True,
            )
            + "\n"
        )

    output = {
        "status": "route-counterexample" if failure is not None else "sample-complete",
        "search_space": {
            "family": (
                f"labelled simple sink-regular rho=4 bipartite graphs with {args.source_count} sources, {args.source_count + 4} sinks, 12 active sources of degree 4, all other vertices degree 3, filtered to minimum dicut at least 3"
                if args.simple
                else f"labelled sink-regular rho=4 bipartite multigraphs with {args.source_count} sources, {args.source_count + 4} sinks, 12 active sources of degree 4, all other vertices degree 3, filtered to minimum dicut at least 3"
            ),
            "generator": "one accepted rejection-sampled graph for each Python random.Random integer seed",
            "start_seed": args.start_seed,
            "requested_count": args.count,
            "isomorphism_reduction": "none",
        },
        "completed_count": len(records),
        "distinct_labelled_graphs": len({record["graph_sha256"] for record in records}),
        "independently_verified_count": sum(record.get("independently_verified", False) for record in records),
        "python_version": sys.version,
        "records": records,
        "route_counterexample": failure,
        "elapsed_seconds": monotonic() - started,
    }
    args.checkpoint.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
