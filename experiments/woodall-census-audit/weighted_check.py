"""Cross-check isomorph-freeness and tau against the prior labelled sweep (#73):
sum over my classes G with tau>=3 of  e(G)/|Aut(G)|  (e = #linear extensions) must equal
the number of strictly upper-triangular 0/1 matrices with that tau, i.e. the counts_by_tau
in experiments/woodall-dijoin-exact-ip/results/sweep-n{n}-*.json.  Usage: python3 weighted_check.py n
"""
import itertools, json, sys
from woodall_audit import _mult_matrix

n = int(sys.argv[1])

def linext(n, arcs):
    pred = [0]*n
    for u, v in arcs: pred[v] |= 1 << u
    f = [0]*(1 << n); f[0] = 1
    for S in range(1 << n):
        if not f[S]: continue
        for v in range(n):
            if not (S >> v) & 1 and pred[v] & ~S == 0:
                f[S | 1 << v] += f[S]
    return f[(1 << n) - 1]

def aut(n, arcs):
    M = _mult_matrix(n, arcs)
    indeg = [sum(M[u][v] for u in range(n)) for v in range(n)]
    outdeg = [sum(M[v]) for v in range(n)]
    cnt = 0
    for p in itertools.permutations(range(n)):
        if any(indeg[p[v]] != indeg[v] or outdeg[p[v]] != outdeg[v] for v in range(n)): continue
        if all(M[p[u]][p[v]] == M[u][v] for u in range(n) for v in range(n)): cnt += 1
    return cnt

from fractions import Fraction
tot = {}
seen = set()
for line in open(f"census_out/dags_n{n}.jsonl"):
    r = json.loads(line)
    key = tuple(r["canon"]); assert key not in seen; seen.add(key)
    arcs = [tuple(a) for a in r["arcs"]]
    w = Fraction(linext(n, arcs), aut(n, arcs))
    assert w.denominator == 1
    tot[r["tau"]] = tot.get(r["tau"], 0) + int(w)
print("n", n, "weighted counts by tau (mine):", dict(sorted(tot.items())))
import glob
for f in glob.glob(f"../woodall-dijoin-exact-ip/results/sweep-n{n}-*.json"):
    d = json.load(open(f)); c = {int(k): v for k, v in d["counts_by_tau"].items() if int(k) >= 3}
    print("prior sweep", f.split('/')[-1], c, "MATCH" if c == tot else "MISMATCH")
