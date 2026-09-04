"""Exact independence-number decision procedure (Tomita-style branch and bound).

``decide(adj, target, ...)`` answers, *exhaustively*, whether the graph has an
independent set of size >= target.  The only pruning used is the greedy
clique-partition bound: a partition of the candidate set into k cliques of G
certifies that at most k of its vertices lie in any independent set, so a
branch is cut only when it provably cannot reach ``target``.  Nothing else is
discarded, hence an exhausted search is a complete refutation.

Outcomes:
    ("SAT", witness)   an independent set of size `target` (exact, re-checkable)
    ("UNSAT", nodes)   search exhausted -> alpha(G) < target
    ("UNKNOWN", nodes) node/time budget exhausted -> proves nothing
"""

import time

__all__ = ["decide", "verify_independent"]


def decide(adj, target, node_budget=None, time_budget=None):
    n = len(adj)
    if target <= 0:
        return ("SAT", [])
    if n < target:
        return ("UNSAT", 0)

    full = (1 << n) - 1
    closed = [adj[v] | (1 << v) for v in range(n)]
    t0 = time.time()
    nodes = 0
    stop = False
    witness = []
    popcount = int.bit_count if hasattr(int, "bit_count") else (lambda x: bin(x).count("1"))

    def expand(cand, chosen):
        nonlocal nodes, stop
        nodes += 1
        if stop:
            return False
        if node_budget is not None and nodes >= node_budget:
            stop = True
            return False
        if time_budget is not None and (nodes & 255) == 0 and time.time() - t0 > time_budget:
            stop = True
            return False

        need = target - len(chosen)
        if need == 0:
            witness.extend(chosen)
            return True
        if popcount(cand) < need:
            return False

        # greedy clique partition of `cand` (greedy colouring of the complement)
        order, colour = [], []
        P = cand
        c = 0
        while P:
            c += 1
            Q = P
            while Q:
                b = Q & -Q
                v = b.bit_length() - 1
                order.append(v)
                colour.append(c)
                P &= ~b
                Q &= adj[v]
        if c < need:
            return False

        prefix = 0
        prefixes = []
        for v in order:
            prefixes.append(prefix)
            prefix |= 1 << v

        for i in range(len(order) - 1, -1, -1):
            if colour[i] < need:
                return False
            v = order[i]
            chosen.append(v)
            if expand(cand & prefixes[i] & ~closed[v], chosen):
                return True
            chosen.pop()
            if stop:
                return False
        return False

    found = expand(full, [])
    if found:
        return ("SAT", sorted(witness))
    if stop:
        return ("UNKNOWN", nodes)
    return ("UNSAT", nodes)


def verify_independent(adj, vs):
    vs = list(vs)
    if len(set(vs)) != len(vs):
        return False
    for i, u in enumerate(vs):
        for v in vs[i + 1:]:
            if adj[u] >> v & 1:
                return False
    return True
