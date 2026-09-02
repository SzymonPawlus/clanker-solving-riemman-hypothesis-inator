"""Differential test of A1's census against my independent census (issue #149).
Usage: python3 diff_a1.py <a1 file(s)>   -- each file JSON or JSONL; records must expose an
arc list (auto-detected keys) and optionally n, tau, verdict.  Every A1 instance is
canonicalised with MY canonical form and joined to my census_out/dags_n*.jsonl (simple) or
multidags_M*_n*.jsonl (multi); tau and verdict are recomputed by my tool regardless.
"""
import glob, json, sys
from woodall_audit import *

def load(path):
    txt = open(path).read()
    try:
        d = json.loads(txt)
        if isinstance(d, dict):
            for k in ("instances", "records", "results", "graphs", "items"):
                if k in d and isinstance(d[k], list):
                    return d[k]
            return [d]
        return d
    except json.JSONDecodeError:
        return [json.loads(l) for l in txt.splitlines() if l.strip()]

def arcs_of(r):
    for k in ("arcs", "edges", "arc_list", "A"):
        if k in r:
            return [tuple(a) for a in r[k]]
    raise KeyError(f"no arc list in record keys {list(r)}")

mine = {}
for f in glob.glob("census_out/dags_n*.jsonl"):
    for l in open(f):
        r = json.loads(l); mine[tuple(r["canon"])] = r

n_seen = n_dup = n_tau_dis = n_verdict_dis = n_missing = 0
seen = set()
by_n = {}
for path in sys.argv[1:]:
    for r in load(path):
        arcs = arcs_of(r)
        n = r.get("n") or (max(max(a) for a in arcs) + 1)
        key = canonical_form(n, arcs)
        n_seen += 1
        if (n, key) in seen:
            n_dup += 1; print("DUPLICATE (isomorphic to an earlier A1 instance):", n, arcs)
        seen.add((n, key))
        by_n[n] = by_n.get(n, 0) + 1
        t, v = woodall_verdict(n, arcs)
        for tk in ("tau", "min_dicut_size", "min_dicut"):
            if tk in r and isinstance(r[tk], int) and r[tk] != t:
                n_tau_dis += 1; print("TAU DISAGREES:", n, arcs, "A1", r[tk], "mine", t)
        for vk in ("verdict", "packs", "holds", "woodall", "result"):
            if vk in r and isinstance(r[vk], bool) and r[vk] != v:
                n_verdict_dis += 1; print("VERDICT DISAGREES:", n, arcs, "A1", r[vk], "mine", v)
        if len(set(arcs)) == len(arcs) and t is not None and t >= 3 and weakly_connected(n, arcs):
            if key not in mine:
                n_missing += 1; print("A1 instance NOT in my simple census:", n, arcs)
print(f"A1 instances: {n_seen}, by n: {by_n}, duplicates-up-to-iso: {n_dup}, tau disagreements: {n_tau_dis}, "
      f"verdict disagreements: {n_verdict_dis}, A1 simple tau>=3 instances missing from my census: {n_missing}")
# reverse direction: my classes missing from A1, per n, for the n values A1 covered
for n in sorted(by_n):
    mine_n = {k for (nn, k) in ((r["n"], tuple(r["canon"])) for r in mine.values()) if nn == n}
    a1_n = {k for (nn, k) in seen if nn == n}
    print(f"n={n}: my simple tau>=3 classes {len(mine_n)}, A1 classes {len(a1_n)}, mine-not-in-A1 {len(mine_n - a1_n)}, A1-not-in-mine {len(a1_n - mine_n)}")
