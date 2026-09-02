"""Independent census over MULTI-DAGs (parallel arcs allowed, multiplicity <= M),
isomorph-free, weakly connected, tau >= 3.  Usage: python3 multicensus.py NMAX M
Checkpointed to census_out/multidags_M{M}_n{n}.jsonl
"""
import itertools, json, os, sys, time
from woodall_audit import *

NMAX, M = int(sys.argv[1]), int(sys.argv[2])
os.makedirs("census_out", exist_ok=True)
t0 = time.time()
prev = [()]
summary = {}
for n in range(1, NMAX + 1):
    seen = set()
    for key in prev:
        base = arcs_from_matrix_key(n - 1, key)
        for mults in itertools.product(range(M + 1), repeat=n - 1):
            arcs = base + [(u, n - 1) for u in range(n - 1) for _ in range(mults[u])]
            seen.add(canonical_form(n, arcs))
    keys = sorted(seen)
    prev = keys
    n_wc = n_tau3 = 0
    tau_hist = {}
    verdicts = {}
    with open(f"census_out/multidags_M{M}_n{n}.jsonl", "w") as f:
        for key in keys:
            arcs = arcs_from_matrix_key(n, key)
            if not weakly_connected(n, arcs):
                continue
            n_wc += 1
            t = tau(n, arcs)
            tau_hist[t] = tau_hist.get(t, 0) + 1
            if t is None or t < 3:
                continue
            n_tau3 += 1
            P = pack_dijoins(n, arcs, t)
            verdicts[P is not None] = verdicts.get(P is not None, 0) + 1
            simple = len(set(arcs)) == len(arcs)
            rec = {"n": n, "arcs": arcs, "tau": t, "verdict": P is not None, "packing": P, "simple": simple,
                   "ssc": source_sink_connected_dag(n, arcs)}
            f.write(json.dumps(rec) + "\n")
    summary[n] = {"unlabelled_multidags": len(keys), "weakly_connected": n_wc, "tau_hist": tau_hist,
                  "tau>=3": n_tau3, "verdicts": verdicts, "elapsed_s": round(time.time() - t0, 1)}
    print(n, summary[n], flush=True)
    json.dump(summary, open(f"census_out/multisummary_M{M}.json", "w"), indent=1)
