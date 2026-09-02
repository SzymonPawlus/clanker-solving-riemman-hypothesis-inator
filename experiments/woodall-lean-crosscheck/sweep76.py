"""Sweep: prose model vs. literal model of the branch-76 Lean (`lean_model_76.py`).

Prints the disagreement table quoted in
``problems/woodalls-conjecture/attacks/lean-foundations-audit/README.md`` and writes
``results/sweep76.json``.  Deterministic, stdlib only.
"""
import collections
import json
import os

import lean_model_76 as L
import prose_model as P

HERE = os.path.dirname(os.path.abspath(__file__))


def main(max_n=4, max_arcs=6, max_mult=2):
    cnt = collections.Counter()
    first = {}
    total = both = 0
    for D in P.all_digraphs(max_n, max_arcs, max_mult):
        total += 1
        kind = "simple" if len(set(D[1])) == len(D[1]) else "multi"
        for name, pf, lf in L.COMPARISONS:
            a, b = pf(D), lf(D)
            if a != b:
                key = f"{name}[{kind}]"
                cnt[key] += 1
                first.setdefault(key, {"n": D[0], "arcs": D[1], "prose": repr(a), "lean": repr(b)})
        if kind == "multi":
            a = P.has_tau_disjoint_dijoins(D, True)
            lt = L.tau(D)
            if a is not None and lt is not None:
                both += 1
                if a != (L.max_packing(D) >= lt):
                    key = "woodall_truth[multi, both tau defined]"
                    cnt[key] += 1
                    first.setdefault(key, {"n": D[0], "arcs": D[1]})
    out = {"space": {"max_n": max_n, "max_arcs": max_arcs, "max_mult": max_mult},
           "scanned": total, "multigraphs_with_tau_both_sides": both,
           "disagreements": {k: {"count": cnt[k], "first": first[k]} for k in sorted(cnt)}}
    os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
    with open(os.path.join(HERE, "results", "sweep76.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
