"""Cross-check harness: prose model vs. a literal model of B1's Lean (issue #151, step 4).

Usage: ``python3 crosscheck.py [--max-n 4] [--max-arcs 6] [--max-mult 2]``
Writes a checkpoint every 2000 digraphs to ``results/checkpoint.json`` and the final
disagreement list to ``results/disagreements.json``.
"""
from __future__ import annotations

import argparse
import json
import os
import time

import prose_model as P

try:
    import lean_model as L  # written only after reading B1's sources
except ImportError:  # pragma: no cover
    L = None

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results")


def compare(D):
    """Return a dict of field -> (prose, lean) for every field on which they disagree."""
    diffs = {}
    for name, pf, lf in L.COMPARISONS:
        a, b = pf(D), lf(D)
        if a != b:
            diffs[name] = (repr(a), repr(b))
    return diffs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-n", type=int, default=4)
    ap.add_argument("--max-arcs", type=int, default=6)
    ap.add_argument("--max-mult", type=int, default=2)
    ap.add_argument("--loops", action="store_true")
    args = ap.parse_args()
    if L is None:
        raise SystemExit("lean_model.py missing: nothing to cross-check yet")
    os.makedirs(RESULTS, exist_ok=True)
    disagreements, count, t0 = [], 0, time.time()
    for D in P.all_digraphs(args.max_n, args.max_arcs, args.max_mult, loops=args.loops):
        count += 1
        d = compare(D)
        if d:
            disagreements.append({"n": D[0], "arcs": D[1], "diffs": d})
        if count % 2000 == 0:
            with open(os.path.join(RESULTS, "checkpoint.json"), "w") as fh:
                json.dump({"scanned": count, "disagreements": disagreements}, fh)
    summary = {"space": vars(args), "scanned": count, "seconds": round(time.time() - t0, 1),
               "n_disagreements": len(disagreements), "disagreements": disagreements}
    with open(os.path.join(RESULTS, "disagreements.json"), "w") as fh:
        json.dump(summary, fh, indent=1)
    print(json.dumps({k: v for k, v in summary.items() if k != "disagreements"}))
    by_field = {}
    for rec in disagreements:
        for f in rec["diffs"]:
            by_field.setdefault(f, []).append(rec)
    for f, recs in by_field.items():
        print(f"{f}: {len(recs)} disagreements; first: n={recs[0]['n']} arcs={recs[0]['arcs']} {recs[0]['diffs'][f]}")


if __name__ == "__main__":
    main()
