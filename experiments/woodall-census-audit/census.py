"""Independent census (issue #149): isomorph-free simple DAGs on n vertices,
weakly connected, with tau >= 3; exact Woodall verdict on each.
Checkpointed as JSONL per n in census_out/.  Usage: python3 census.py NMAX
"""
import json, os, sys, time
from woodall_audit import *

NMAX = int(sys.argv[1])
os.makedirs("census_out", exist_ok=True)
t0 = time.time()
prev = [()]  # canonical keys of DAGs on n-1 vertices
summary = {}
for n in range(1, NMAX + 1):
    seen = set()
    for key in prev:
        base = arcs_from_matrix_key(n - 1, key)
        for mask in range(1 << (n - 1)):
            arcs = base + [(u, n - 1) for u in range(n - 1) if (mask >> u) & 1]
            seen.add(canonical_form(n, arcs))
    keys = sorted(seen)
    prev = keys
    n_all = len(keys)
    n_wc = n_deg = n_tau3 = 0
    tau_hist = {}
    with open(f"census_out/dags_n{n}.jsonl", "w") as f:
        for key in keys:
            arcs = arcs_from_matrix_key(n, key)
            if not weakly_connected(n, arcs):
                continue
            n_wc += 1
            src, snk = sources_sinks(n, arcs)
            outdeg = [0]*n; indeg = [0]*n
            for u, v in arcs: outdeg[u] += 1; indeg[v] += 1
            if any(outdeg[s] < 3 for s in src) or any(indeg[t] < 3 for t in snk):
                continue
            n_deg += 1
            t = tau(n, arcs)
            tau_hist[t] = tau_hist.get(t, 0) + 1
            if t < 3:
                continue
            n_tau3 += 1
            P = pack_dijoins(n, arcs, t)
            rec = {"n": n, "arcs": arcs, "canon": list(key), "tau": t,
                   "min_dicut": min_dicut_witness(n, arcs), "verdict": P is not None,
                   "packing": P, "ssc": source_sink_connected_dag(n, arcs)}
            f.write(json.dumps(rec) + "\n")
    summary[n] = {"unlabelled_dags": n_all, "weakly_connected": n_wc,
                  "src_out>=3_and_sink_in>=3": n_deg, "tau_hist_after_degree_filter": tau_hist,
                  "tau>=3": n_tau3, "elapsed_s": round(time.time() - t0, 1)}
    print(n, summary[n], flush=True)
    json.dump(summary, open("census_out/summary.json", "w"), indent=1)
