"""Fast admissible-support counter (same prune set as support_enum.py, rewritten for speed).

support_enum.py is the readable reference implementation; this file is the one used for
the measurement runs.  test_agreement.py checks that the two agree on every m where the
slow one can be run.
"""

from __future__ import annotations

import itertools
import subprocess
import sys
import time

import networkx as nx

from support_enum import (Quad, GENG, harborth_max_edges, graph_admissible,
                          is_union_of_paths, wall_capacity)

# label 0 = interior; 1,2,3 = on wall 0,1,2; 4,5,6 = corners {0,1},{1,2},{0,2}
LAB_WALLS = [(), (0,), (1,), (2,), (0, 1), (1, 2), (0, 2)]
LAB_SIZE = [len(w) for w in LAB_WALLS]
DEG_MAX = [6, 4, 4, 4, 2, 2, 2]
DEG_MIN = [2, 1, 1, 1, 1, 1, 1]
S3 = list(itertools.permutations([0, 1, 2]))
# action of a wall permutation tau on the 7 labels
LAB_OF = {frozenset(w): i for i, w in enumerate(LAB_WALLS)}
TAU_LAB = [[LAB_OF[frozenset(tau[w] for w in LAB_WALLS[l])] for l in range(7)]
           for tau in S3]


def count_labellings(G, cap, corners_adjacent, auts, want_orbits, first_only=False):
    """Number of admissible wall labellings of G (as orbit classes if want_orbits)."""
    m = G.number_of_nodes()
    adj = [tuple(G[v]) for v in range(m)]
    deg = [len(a) for a in adj]
    edges = tuple(G.edges())
    uop = is_union_of_paths(G)
    need = 2 if (m < 3 or uop) else 3
    allowed = [[l for l in range(7) if DEG_MIN[l] <= deg[v] <= DEG_MAX[l]]
               for v in range(m)]
    if any(not a for a in allowed):
        return 0
    lab = [0] * m
    per_wall = [0, 0, 0]
    corner_used = [False, False, False]
    orbits = set()
    total = 0
    found = [False]

    def leaf_ok():
        nb = 0
        for v in range(m):
            if LAB_SIZE[lab[v]]:
                nb += 1
        if m >= 2 and nb < min(m, need):
            return False
        for v in range(m):
            l = lab[v]
            if l == 0 and deg[v] == 2:
                a, b = adj[v]
                if b in G[a]:
                    return False
                if len(set(adj[a]) & set(adj[b])) > 1:
                    return False
            elif LAB_SIZE[l] == 2 and deg[v] == 2:
                a, b = adj[v]
                k1, k2 = LAB_WALLS[l]
                wa, wb = LAB_WALLS[lab[a]], LAB_WALLS[lab[b]]
                if not ((k1 in wa and k2 in wb) or (k2 in wa and k1 in wb)):
                    return False
            elif LAB_SIZE[l] == 1 and deg[v] == 4:
                k = LAB_WALLS[l][0]
                if sum(1 for u in adj[v] if k in LAB_WALLS[lab[u]]) < 2:
                    return False
        # per-wall induced subgraph must be a linear forest
        for k in range(3):
            vs = [v for v in range(m) if k in LAB_WALLS[lab[v]]]
            if len(vs) <= 2:
                continue
            idx = {v: i for i, v in enumerate(vs)}
            parent = list(range(len(vs)))

            def find(x):
                while parent[x] != x:
                    parent[x] = parent[parent[x]]
                    x = parent[x]
                return x

            dk = [0] * len(vs)
            for a, b in edges:
                if a in idx and b in idx:
                    ia, ib = idx[a], idx[b]
                    dk[ia] += 1
                    dk[ib] += 1
                    if dk[ia] > 2 or dk[ib] > 2:
                        return False
                    ra, rb = find(ia), find(ib)
                    if ra == rb:
                        return False        # cycle
                    parent[ra] = rb
        return True

    def rec(v):
        nonlocal total
        if found[0]:
            return
        if v == m:
            if leaf_ok():
                if want_orbits:
                    best = None
                    for sigma in auts:
                        perm = [0] * m
                        for u in range(m):
                            perm[sigma[u]] = lab[u]
                        for t in TAU_LAB:
                            cand = tuple(t[x] for x in perm)
                            if best is None or cand < best:
                                best = cand
                    orbits.add(best)
                total += 1
                if first_only:
                    found[0] = True
            return
        for l in allowed[v]:
            ws = LAB_WALLS[l]
            if len(ws) == 2:
                ci = l - 4
                if corner_used[ci]:
                    continue
                bad = False
                for u in adj[v]:
                    if u < v and LAB_SIZE[lab[u]] == 2 and not corners_adjacent:
                        bad = True
                        break
                if bad:
                    continue
            ok = True
            for w in ws:
                if per_wall[w] + 1 > cap:
                    ok = False
                    break
            if not ok:
                continue
            lab[v] = l
            for w in ws:
                per_wall[w] += 1
            if len(ws) == 2:
                corner_used[l - 4] = True
            rec(v + 1)
            for w in ws:
                per_wall[w] -= 1
            if len(ws) == 2:
                corner_used[l - 4] = False
        lab[v] = 0

    rec(0)
    return len(orbits) if want_orbits else total


def automorphisms(G):
    gm = nx.algorithms.isomorphism.GraphMatcher(G, G)
    return [tuple(mp[v] for v in range(G.number_of_nodes()))
            for mp in gm.isomorphisms_iter()]


def geng_stream(m):
    ub = harborth_max_edges(m)
    cmd = [GENG, "-q", "-d1", "-D6", "-k", str(m), f"1:{ub}"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True, bufsize=1 << 20)
    for line in p.stdout:
        line = line.strip()
        if line:
            yield nx.from_graph6_bytes(line.encode())
    p.wait()


def run(m, cap, corners_adjacent, mode, deadline=None):
    """mode 'orbits' -> exact support-class count; 'graphs' -> graph-class lower bound."""
    ngraph = nsup = 0
    seen = 0
    t0 = time.time()
    for G in geng_stream(m):
        seen += 1
        if deadline and seen % 20000 == 0 and time.time() - t0 > deadline:
            return ngraph, nsup, seen, False
        if not graph_admissible(G):
            continue
        if mode == "orbits":
            auts = automorphisms(G)
            c = count_labellings(G, cap, corners_adjacent, auts, True)
            if c:
                ngraph += 1
                nsup += c
        else:
            c = count_labellings(G, cap, corners_adjacent, None, False, first_only=True)
            if c:
                ngraph += 1
    return ngraph, nsup, seen, True


if __name__ == "__main__":
    d_a, d_b = int(sys.argv[1]), int(sys.argv[2])      # d = d_a + d_b*sqrt(3)
    mode = sys.argv[3]
    ms = [int(x) for x in sys.argv[4].split(",")]
    deadline = float(sys.argv[5]) if len(sys.argv) > 5 else None
    d = Quad(d_a, d_b)
    cap = wall_capacity(d)
    ca = not (d - Quad(2)).sign() > 0
    print(f"# d = {d}, wall capacity = {cap}, corners can be adjacent = {ca}", flush=True)
    for m in ms:
        t = time.time()
        ng, ns, seen, done = run(m, cap, ca, mode, deadline)
        print(f"m={m} mode={mode} geng={seen} graphs={ng} supports={ns} "
              f"complete={done} secs={time.time()-t:.1f}", flush=True)
