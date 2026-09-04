"""Wider search of the '6-ring of weight-0 arcs + three solid paths' family (independent path
orientations, path lengths 2..4, all endpoint matchings) for a {0,1}-weighted Edmonds-Giles
counterexample with tau_w = 2.  Status: numerical.  Fast down-set enumeration via ancestor
closures (down-sets of a digraph are exactly the unions of ancestor sets); any hit is
re-verified by the slow brute-force path in tau2lib."""
import itertools, json, time, sys
from tau2lib import dicuts, two_packing_within, two_colourable_traces, tau

def ancestors(n, arcs):
    pred = [[] for _ in range(n)]
    for t, h in arcs:
        pred[h].append(t)
    anc = []
    for y in range(n):
        seen = 1 << y
        stack = [y]
        while stack:
            v = stack.pop()
            for u in pred[v]:
                if not (seen >> u) & 1:
                    seen |= 1 << u
                    stack.append(u)
        anc.append(seen)
    return anc

def downsets(n, arcs):
    anc = ancestors(n, arcs)
    full = (1 << n) - 1
    seen = {0}
    stack = [0]
    while stack:
        U = stack.pop()
        for y in range(n):
            if not (U >> y) & 1:
                W = U | anc[y]
                if W not in seen:
                    seen.add(W)
                    stack.append(W)
    seen.discard(0); seen.discard(full)
    return seen

def fast_check(n, arcs, w):
    """True iff tau_w == 2 and no 2-packing inside weight-1 arcs."""
    ones = [i for i in range(len(arcs)) if w[i]]
    idx = {a: k for k, a in enumerate(ones)}
    traces = []
    tw = None
    for U in downsets(n, arcs):
        t = 0
        for i in ones:
            a, b = arcs[i]
            if (U >> a) & 1 and not (U >> b) & 1:
                t |= 1 << idx[i]
        c = bin(t).count("1")
        tw = c if tw is None or c < tw else tw
        if tw < 2:
            return False
        traces.append(t)
    if tw != 2:
        return False
    return two_colourable_traces(list(set(traces)), len(ones)) is None

def instance(ring_or, ends, path_or, L):
    arcs, w = [], []
    for k in range(6):
        u, v = k, (k + 1) % 6
        arcs.append((u, v) if ring_or[k] else (v, u)); w.append(0)
    nxt = 6
    for i in range(3):
        x, y = ends[i]
        inner = list(range(nxt, nxt + L - 1)); nxt += L - 1
        chain = list(zip([x] + inner, inner + [y]))
        for j, (u, v) in enumerate(chain):
            arcs.append((u, v) if path_or[i][j] else (v, u)); w.append(1)
    return nxt, arcs, w

matchings = [[(0, 3), (1, 4), (2, 5)], [(0, 1), (2, 3), (4, 5)], [(0, 1), (2, 5), (3, 4)],
             [(0, 3), (1, 2), (4, 5)], [(0, 5), (1, 2), (3, 4)], [(0, 5), (1, 4), (2, 3)]]
deadline = time.time() + float(sys.argv[1]) if len(sys.argv) > 1 else 1e18
hits, count = [], 0
for L in (2, 3, 4):
    for ends in matchings:
        for ring_or in itertools.product((0, 1), repeat=6):
            if ring_or[0] == 0:
                continue                      # global reversal symmetry
            for por in itertools.product(itertools.product((0, 1), repeat=L), repeat=3):
                n, arcs, w = instance(ring_or, ends, por, L)
                count += 1
                if fast_check(n, arcs, w):
                    assert tau(n, arcs, w) == 2 and two_packing_within(n, arcs, w) is None
                    hits.append({"L": L, "ends": ends, "ring_or": ring_or, "path_or": por,
                                 "n": n, "arcs": arcs, "w": w})
                    print("HIT", L, ends, ring_or, por, flush=True)
                    json.dump(hits, open("ring2_hits.json", "w"), indent=1)
                if time.time() > deadline:
                    print(f"deadline: {count} instances, {len(hits)} hits (L={L})"); sys.exit()
    print(f"L={L} done, {count} instances so far, {len(hits)} hits", flush=True)
print(f"complete: {count} instances, {len(hits)} hits")
