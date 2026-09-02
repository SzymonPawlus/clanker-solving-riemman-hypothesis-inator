"""Validation of woodall_audit.py against known-true cases (issue #149 step 2).
Run:  python3 validate.py      (exit code 0 == every check passed)
"""
import itertools, random, sys, time
from woodall_audit import *

random.seed(20260902)
failures = []

def check(cond, msg):
    if not cond:
        failures.append(msg)
        print("FAIL:", msg)

# --- README fixtures -------------------------------------------------------
path = (3, [(0, 1), (1, 2)])
cycle = (3, [(0, 1), (1, 2), (2, 0)])
diamond = (4, [(0, 1), (0, 2), (1, 3), (2, 3)])
nearmiss = (4, [(0, 2), (1, 2), (1, 3)])   # s1->t1, s2->t1, s2->t2  (s1=0,s2=1,t1=2,t2=3)

check(tau(*path) == 1, "path tau")
check(len(all_dicuts(*path)) == 2 and sorted(len(c) for _, c in all_dicuts(*path)) == [1, 1], "path dicuts are {01},{12}")
check(all_dicuts(*cycle) == [] and tau(*cycle) is None, "cycle has NO dicuts")
check(tau(*diamond) == 2, "diamond tau=2")
check(woodall_verdict(*diamond) == (2, True), "diamond packs 2")
p = pack_dijoins(*diamond, 2)
check(sorted(map(sorted, p)) == [[0, 2], [1, 3]] or sorted(map(sorted, p)) == [[0, 3], [1, 2]], f"diamond packing is the two s-t paths or the crossed pair: {p}")
check(source_sink_connected_dag(*diamond), "diamond is source-sink connected")
check(not source_sink_connected_dag(*nearmiss), "near-miss is NOT source-sink connected")
check(tau(*nearmiss) == 1, "near-miss tau=1")
check(woodall_verdict(*nearmiss) == (1, True), "near-miss verdict")
# path: whole arc set is a dijoin but its reversal is not strongly connected -> dijoin != strengthening
check(is_dijoin(*path, [0, 1]), "path arcs form a dijoin (contraction), even though reversal is not SC")
check(not is_dijoin(*path, [0]), "single arc of path is not a dijoin")

# --- dijoin definitions agree on random sets ---------------------------------
t0 = time.time()
cnt = 0
for _ in range(3000):
    n = random.randint(1, 6)
    m = random.randint(0, 10)
    arcs = [(random.randrange(n), random.randrange(n)) for _ in range(m)]
    S = [i for i in range(m) if random.random() < 0.5]
    try:
        is_dijoin(n, arcs, S)
    except AssertionError as e:
        check(False, f"dijoin defs disagree: n={n} arcs={arcs} S={S}: {e}")
    cnt += 1
print(f"dijoin-definition cross-check: {cnt} random (digraph, arc set) pairs, {time.time()-t0:.1f}s")

# --- exact packer vs brute force on random small multi-digraphs -------------
t0 = time.time()
cnt = 0
for _ in range(1500):
    n = random.randint(2, 5)
    m = random.randint(1, 9)
    arcs = [(random.randrange(n), random.randrange(n)) for _ in range(m)]
    t = tau(n, arcs)
    if t is None or t == 0:
        continue
    for k in (t, t + 1):
        if k ** m > 30000:
            continue
        a = pack_dijoins(n, arcs, k) is not None
        b = pack_dijoins_bruteforce(n, arcs, k)
        check(a == b, f"packer vs brute force disagree n={n} arcs={arcs} k={k}: fast={a} brute={b}")
        if a:
            classes = pack_dijoins(n, arcs, k)
            used = [x for c in classes for x in c]
            check(len(used) == len(set(used)) and len(classes) == k, "packing classes disjoint")
            check(all(is_dijoin(n, arcs, c) for c in classes), f"each class is a dijoin: {arcs} {classes}")
        cnt += 1
print(f"packer vs brute force: {cnt} decisions, {time.time()-t0:.1f}s")

# --- tau = 2 is known true; tau+1 must always fail (easy direction) ---------
# all labelled simple DAGs on <= 5 vertices with arcs i->j, i<j  (every DAG is iso to one of these)
t0 = time.time()
stats = {}
for n in range(1, 6):
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    for mask in range(1 << len(pairs)):
        arcs = [pairs[i] for i in range(len(pairs)) if (mask >> i) & 1]
        t, v = woodall_verdict(n, arcs)
        stats[(n, t)] = stats.get((n, t), 0) + 1
        if t == 2:
            check(v is True, f"tau=2 instance failed: n={n} arcs={arcs}")
        if t and t >= 1:
            check(pack_dijoins(n, arcs, t + 1) is None, f"tau+1 disjoint dijoins claimed to exist: {arcs}")
        if t and t >= 1 and source_sink_connected_dag(n, arcs):
            check(v is True, f"source-sink-connected DAG failed: n={n} arcs={arcs}")
print("labelled upper-triangular DAGs n<=5 by (n,tau):", sorted(stats.items(), key=lambda kv: (kv[0][0], -1 if kv[0][1] is None else kv[0][1])), f"{time.time()-t0:.1f}s")

# tau=2 and SSC with parallel arcs, random multi-DAGs on <= 6 vertices
t0 = time.time()
c2 = css = 0
for _ in range(2000):
    n = random.randint(2, 6)
    m = random.randint(1, 12)
    arcs = [tuple(sorted((random.randrange(n), random.randrange(n)))) for _ in range(m)]
    arcs = [a for a in arcs if a[0] != a[1]]
    if not arcs:
        continue
    t, v = woodall_verdict(n, arcs)
    if t == 2:
        c2 += 1
        check(v is True, f"tau=2 multi-DAG failed: n={n} arcs={arcs}")
    if t and source_sink_connected_dag(n, arcs):
        css += 1
        check(v is True, f"SSC multi-DAG failed: n={n} arcs={arcs}")
print(f"random multi-DAGs: {c2} tau=2 instances, {css} source-sink-connected instances, {time.time()-t0:.1f}s")

# --- condensation invariance: verdict(D) == verdict(condensation(D)) --------
t0 = time.time()
cnt = 0
for _ in range(1500):
    n = random.randint(2, 6)
    m = random.randint(1, 12)
    arcs = [(random.randrange(n), random.randrange(n)) for _ in range(m)]
    k, carcs = condensation(n, arcs)
    check(woodall_verdict(n, arcs) == woodall_verdict(k, carcs), f"condensation changed verdict: {n} {arcs} -> {k} {carcs}")
    check(sorted(len(c) for c in distinct_dicut_sets(n, arcs)) == sorted(len(c) for c in distinct_dicut_sets(k, carcs)), f"condensation changed dicut sizes: {arcs}")
    cnt += 1
print(f"condensation invariance: {cnt} random digraphs, {time.time()-t0:.1f}s")

# --- canonical form: isomorphic relabellings collide, OEIS A003087 counts ---
t0 = time.time()
for _ in range(500):
    n = random.randint(1, 6)
    m = random.randint(0, 10)
    arcs = [(random.randrange(n), random.randrange(n)) for _ in range(m)]
    perm = list(range(n)); random.shuffle(perm)
    arcs2 = [(perm[u], perm[v]) for u, v in arcs]
    random.shuffle(arcs2)
    check(canonical_form(n, arcs) == canonical_form(n, arcs2), f"canonical form not invariant: {arcs}")
dags = all_simple_dags_upto_iso(6)
counts = [len(dags[n]) for n in range(7)]
print("unlabelled simple DAG counts n=0..6:", counts, f"{time.time()-t0:.1f}s")
check(counts == [1, 1, 2, 6, 31, 302, 5984], "OEIS A003087 counts 1,1,2,6,31,302,5984")

print("FAILURES:", len(failures))
sys.exit(1 if failures else 0)
