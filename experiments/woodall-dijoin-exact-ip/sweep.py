"""Exhaustive counterexample sweep for Woodall's conjecture over small DAGs.

Status: numerical.  A negative result here does NOT prove the conjecture; it
only says where a counterexample cannot live.

ENUMERATION AND WHAT IT COVERS
------------------------------
Every DAG admits a topological order, so after relabelling its adjacency
matrix is strictly upper triangular.  Enumerating ALL strictly upper triangular
0/1 matrices on n labelled vertices therefore meets every isomorphism class of
n-vertex DAG at least once.  The enumeration is redundant, not isomorph-free:
a class with several topological orders is visited several times.  That costs
time and never costs coverage, which is the tradeoff taken here because nauty
is not available in this container.

Restricting to DAGs is justified by condensation: arcs inside a strongly
connected component lie in no dicut, the condensation has the same dicut family
and the same tau, and a dijoin of the condensation lifts to one of the original
digraph.  A DAG on fewer than n vertices appears here padded with isolated
vertices, which forces an empty dicut and tau = 0, so each vertex count must be
and is swept separately.

Simple DAGs only.  Condensations of general digraphs can carry PARALLEL arcs
between two components, and those are not simple.  That gap is real and is
covered separately by sweep_multi.py.

PRUNING
-------
In upper triangular form, once rows 0..k are fixed, every shore U contained in
{0..k} has all of its entering and leaving arcs already determined (all arc
tails are smaller than their heads).  So closedness of such a U and the size of
delta^+(U) are known at level k, and any branch where a closed U already has
|delta^+(U)| < min_tau can be cut.  This is exact: it discards only DAGs whose
tau is below min_tau.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dijoin_exact as dx  # noqa: E402


def sweep(n: int, min_tau: int, out_dir: str, chunk: int = 200000) -> dict:
    """Sweep all n-vertex simple DAGs with tau >= min_tau."""
    pairs = [(u, v) for u in range(n) for v in range(u + 1, n)]
    index_of = {p: i for i, p in enumerate(pairs)}
    row_pairs = [[(u, v) for v in range(u + 1, n)] for u in range(n)]

    counts: dict[int, int] = {}
    counterexamples: list[dict] = []
    visited = 0
    decided = 0
    pruned = 0
    t0 = time.time()
    os.makedirs(out_dir, exist_ok=True)
    chunk_id = 0

    # arcs[i] present flags for the whole matrix
    present = [False] * len(pairs)

    def cut_ok(level: int) -> bool:
        """Check every shore U subset {0..level} containing `level`."""
        nonlocal pruned
        for sub in range(1 << level):
            shore = (sub << 1) | 1 if False else (sub | (1 << level))
            # shore is a subset of {0..level} containing `level`
            out = 0
            for (u, v), pres in zip(pairs, present):
                if not pres:
                    continue
                if u > level:
                    continue
                u_in = (shore >> u) & 1
                v_in = (shore >> v) & 1
                if not u_in and v_in:
                    out = -1
                    break
                if u_in and not v_in:
                    out += 1
            if out >= 0 and out < min_tau:
                pruned += 1
                return False
        return True

    def leaf() -> None:
        nonlocal visited, decided
        visited += 1
        arcs = [p for p, pres in zip(pairs, present) if pres]
        if not arcs:
            return
        res = dx.analyse(n, arcs)
        tau = res["tau"]
        if tau is None or tau < min_tau:
            return
        decided += 1
        counts[tau] = counts.get(tau, 0) + 1
        if not res["holds"]:
            counterexamples.append(res)

    def rec(level: int) -> None:
        if level == n - 1:
            leaf()
            return
        options = row_pairs[level]
        for bits in range(1 << len(options)):
            for j, p in enumerate(options):
                present[index_of[p]] = bool((bits >> j) & 1)
            if cut_ok(level):
                rec(level + 1)
        for p in options:
            present[index_of[p]] = False

    rec(0)
    elapsed = time.time() - t0
    summary = {
        "n": n,
        "min_tau": min_tau,
        "enumeration": "all strictly upper triangular 0/1 matrices on n labelled vertices",
        "total_matrices": 1 << len(pairs),
        "leaves_reached": visited,
        "decided_with_tau_at_least_min_tau": decided,
        "prunes": pruned,
        "counts_by_tau": {str(k): v for k, v in sorted(counts.items())},
        "counterexamples": counterexamples,
        "seconds": round(elapsed, 2),
    }
    path = os.path.join(out_dir, f"sweep-n{n}-mintau{min_tau}.json")
    with open(path, "w") as fh:
        json.dump(summary, fh, indent=2)
    return summary


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--min-tau", type=int, default=0)
    ap.add_argument("--out", default=os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "results"))
    args = ap.parse_args()
    summary = sweep(args.n, args.min_tau, args.out)
    printable = dict(summary)
    printable["counterexamples"] = len(summary["counterexamples"])
    print(json.dumps(printable, indent=2))
    if summary["counterexamples"]:
        print("*** CANDIDATE COUNTEREXAMPLE(S) FOUND — extraordinary-claim protocol ***")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
