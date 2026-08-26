"""Driver: run the active-region B&B on a list of (n, p, q, L) cases, checkpointing
each verdict to out/<tag>.json as soon as it is produced."""
import json
import os
import sys
import time
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from arbb import search


def run(tag, cases, node_budget=None, time_budget=300):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", tag + ".json")
    rows = []
    if os.path.exists(path):
        rows = json.load(open(path))
    done = {(r["n"], r["p"], r["q"], r["L"]) for r in rows}
    for (n, p, q, L) in cases:
        if (n, p, q, L) in done:
            continue
        t0 = time.time()
        inst = search.Instance(n, p, q, L)
        build = time.time() - t0
        t0 = time.time()
        r = inst.solve(node_budget=node_budget, time_budget=time_budget)
        row = dict(n=n, p=p, q=q, L=L, d=float(Fraction(p, q)), verdict=r,
                   nodes=inst.nodes, forced=inst.forced, props=inst.props,
                   killed=inst.killed, bound_prunes=inst.bound_prunes,
                   count_prunes=inst.count_prunes, prop_rounds=inst.prop_rounds,
                   build_s=round(build, 2), solve_s=round(time.time() - t0, 2))
        if r == "sat":
            row["witness"] = inst.witness
        rows.append(row)
        json.dump(rows, open(path, "w"), indent=1)
        print(f"n={n} d={p}/{q}={float(Fraction(p,q)):.4f} L={L} -> {r} "
              f"nodes={inst.nodes} {row['solve_s']}s (build {row['build_s']}s)", flush=True)
    return rows


if __name__ == "__main__":
    tag = sys.argv[1]
    cases = json.loads(sys.argv[2])
    nb = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    tb = float(sys.argv[4]) if len(sys.argv) > 4 else 300
    run(tag, [tuple(c) for c in cases], node_budget=(nb or None), time_budget=tb)
