"""Sweep DAGs WITH PARALLEL ARCS -- the gap left by the simple-DAG sweep.

Status: numerical.

Why this exists.  sweep.py covers simple DAGs.  That is not enough to claim
coverage of all digraphs on n vertices, because the condensation of a general
digraph can have several arcs between the same pair of strong components, and
such a multi-DAG is not simple.  Woodall for all simple DAGs therefore does NOT
formally imply Woodall for all digraphs, and pretending otherwise would be the
kind of quiet coverage inflation these rules exist to prevent.

This sweep enumerates every multiplicity vector m : {(u,v) : u < v} -> {0..M}
on n labelled vertices, expands it into a list of parallel arcs, and decides
the packing exactly.  Multiplicity is capped at M, which is stated in the
output and is a genuine limitation: multiplicities above M are not covered.
"""

from __future__ import annotations

import argparse
import itertools
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dijoin_exact as dx  # noqa: E402


def sweep_multi(n: int, max_mult: int, min_tau: int, out_dir: str) -> dict:
    pairs = [(u, v) for u in range(n) for v in range(u + 1, n)]
    counts: dict[int, int] = {}
    counterexamples: list[dict] = []
    visited = 0
    decided = 0
    t0 = time.time()

    for mults in itertools.product(range(max_mult + 1), repeat=len(pairs)):
        visited += 1
        arcs: list[tuple[int, int]] = []
        for pair, k in zip(pairs, mults):
            arcs.extend([pair] * k)
        if not arcs:
            continue
        cuts = dx.dicut_masks(n, arcs)
        tau = dx.tau_of(cuts)
        if tau is None or tau < min_tau:
            continue
        res = dx.analyse(n, arcs)
        decided += 1
        counts[res["tau"]] = counts.get(res["tau"], 0) + 1
        if not res["holds"]:
            counterexamples.append(res)

    elapsed = time.time() - t0
    summary = {
        "n": n,
        "max_multiplicity": max_mult,
        "min_tau": min_tau,
        "enumeration": (
            "every multiplicity vector on the n(n-1)/2 forward pairs of a fixed "
            "topological order, entries 0..max_multiplicity"
        ),
        "total_vectors": (max_mult + 1) ** len(pairs),
        "visited": visited,
        "decided_with_tau_at_least_min_tau": decided,
        "counts_by_tau": {str(k): v for k, v in sorted(counts.items())},
        "counterexamples": counterexamples,
        "seconds": round(elapsed, 2),
    }
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"multi-n{n}-m{max_mult}-mintau{min_tau}.json")
    with open(path, "w") as fh:
        json.dump(summary, fh, indent=2)
    return summary


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--max-mult", type=int, required=True)
    ap.add_argument("--min-tau", type=int, default=2)
    ap.add_argument("--out", default=os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "results"))
    args = ap.parse_args()
    s = sweep_multi(args.n, args.max_mult, args.min_tau, args.out)
    p = dict(s)
    p["counterexamples"] = len(s["counterexamples"])
    print(json.dumps(p, indent=2))
    if s["counterexamples"]:
        print("*** CANDIDATE COUNTEREXAMPLE(S) — extraordinary-claim protocol ***")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
