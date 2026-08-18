#!/usr/bin/env python3
"""Exhaustive fixed-order census for tau-saturated DAGs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import time

from saturation import (
    fixed_order_dags,
    is_tau_saturated,
    minimum_dicut,
    saturation_certificate,
    source_sink_connected,
    tau,
    tau_bitset_oracle,
)


def run(max_n: int, cross_check_through: int):
    started = time.monotonic()
    result = {
        "status": "numerical",
        "scope": {
            "max_n": max_n,
            "fixed_topological_order": True,
            "isomorphism_free": False,
            "cross_check_through": cross_check_through,
            "dicut_requires_nonempty_outgoing_boundary": True,
            "saturation_definition": "every missing forward arc strictly raises tau",
        },
        "by_n": [],
        "first_saturated_not_source_sink_connected": None,
    }
    for n in range(1, max_n + 1):
        counts_by_tau: dict[str, int] = {}
        saturated_by_tau: dict[str, int] = {}
        instances = 0
        for arcs in fixed_order_dags(n):
            instances += 1
            current_tau = tau(n, arcs)
            counts_by_tau[str(current_tau)] = counts_by_tau.get(str(current_tau), 0) + 1
            if n <= cross_check_through:
                oracle_tau = tau_bitset_oracle(n, arcs)
                if current_tau != oracle_tau:
                    raise AssertionError(
                        f"tau checkers disagree for n={n}, arcs={arcs}: "
                        f"{current_tau} != {oracle_tau}"
                    )
            if current_tau < 3 or not is_tau_saturated(n, arcs, minimum_tau=3):
                continue
            saturated_by_tau[str(current_tau)] = saturated_by_tau.get(str(current_tau), 0) + 1
            if source_sink_connected(n, arcs):
                continue
            if result["first_saturated_not_source_sink_connected"] is None:
                witness = minimum_dicut(n, arcs)
                result["first_saturated_not_source_sink_connected"] = {
                    "n": n,
                    "arcs": [list(arc) for arc in arcs],
                    "tau": current_tau,
                    "minimum_dicut": {
                        "shore": list(witness.shore),
                        "arcs": [list(arc) for arc in witness.arcs],
                    },
                    "saturation_certificate": [
                        {"arc": list(arc), "tau_after": after}
                        for arc, after in saturation_certificate(n, arcs)
                    ],
                }
        result["by_n"].append(
            {
                "n": n,
                "instances": instances,
                "counts_by_tau": counts_by_tau,
                "saturated_tau_at_least_3_by_tau": saturated_by_tau,
            }
        )
    result["instances_total"] = sum(row["instances"] for row in result["by_n"])
    result["elapsed_seconds"] = round(time.monotonic() - started, 6)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=6)
    parser.add_argument("--cross-check-through", type=int, default=5)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if not 1 <= args.max_n <= 6:
        parser.error("--max-n must lie in the declared range 1..6")
    if not 0 <= args.cross_check_through <= args.max_n:
        parser.error("--cross-check-through must lie between 0 and --max-n")
    rendered = json.dumps(run(args.max_n, args.cross_check_through), indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(rendered, end="")
    else:
        args.output.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
