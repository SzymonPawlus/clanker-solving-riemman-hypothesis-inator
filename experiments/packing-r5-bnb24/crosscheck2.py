"""Independent re-decision of the verdict by a SECOND, deliberately naive search.

`mis_ref` is a textbook maximum-independent-set decision procedure: pick the vertex of
highest degree in the candidate set, branch in/out, bound by a greedy clique partition of
the candidate set.  It shares no code with arbb/search.py beyond the adjacency bitsets
themselves - no tiles, no active-region propagation, no Oler capacity.  Agreement between
two independently written complete searches is a cross-check, not a proof.
"""
import sys
import time

sys.path.insert(0, ".")
from arbb import geom, search


def clique_cover_bound(cand, adj):
    """Partition `cand` into cliques greedily; the number of cliques bounds any
    independent set inside `cand`."""
    rest = cand
    k = 0
    while rest:
        b = rest & -rest
        v = b.bit_length() - 1
        clique = b
        pool = rest & adj[v]          # candidates adjacent to v
        while pool:
            b2 = pool & -pool
            u = b2.bit_length() - 1
            clique |= b2
            pool &= adj[u]
            pool ^= (pool & b2)
        rest &= ~clique
        k += 1
    return k


class Ref:
    def __init__(self, adj):
        self.adj = adj
        self.nodes = 0

    def decide(self, cand, k, deadline):
        self.nodes += 1
        if k == 0:
            return True
        if cand == 0:
            return False
        if (self.nodes & 1023) == 0 and time.time() > deadline:
            raise TimeoutError
        if cand.bit_count() < k or clique_cover_bound(cand, self.adj) < k:
            return False
        # highest-degree vertex in cand
        best, bd = -1, -1
        it = cand
        while it:
            b = it & -it
            v = b.bit_length() - 1
            deg = (cand & self.adj[v]).bit_count()
            if deg > bd:
                best, bd = v, deg
            it ^= b
        v = best
        if self.decide(cand & ~self.adj[v] & ~(1 << v), k - 1, deadline):
            return True
        return self.decide(cand & ~(1 << v), k, deadline)


if __name__ == "__main__":
    for (n, p, q, L, secs) in [(12, 5, 1, 4, 30), (12, 55, 10, 4, 30), (12, 6, 1, 4, 60),
                               (12, 62, 10, 4, 60), (12, 63, 10, 4, 60), (12, 65, 10, 4, 60)]:
        inst = search.Instance(n, p, q, L)
        r1 = inst.solve(node_budget=5_000_000, time_budget=secs)
        ref = Ref(inst.adj)
        try:
            r2 = "sat" if ref.decide((1 << inst.M) - 1, n, time.time() + secs) else "unsat"
        except TimeoutError:
            r2 = "unknown"
        agree = "AGREE" if r1 == r2 else ("(one undecided)" if "unknown" in (r1, r2)
                                          else "*** DISAGREE ***")
        print(f"n={n} d={p}/{q} L={L}: arbb={r1} ({inst.nodes} nodes)  "
              f"reference={r2} ({ref.nodes} nodes)  {agree}", flush=True)
