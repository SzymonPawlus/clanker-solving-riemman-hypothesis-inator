"""Is T(3) coverable by 8 sets of diameter <= 1?

By De Bruijn-Erdos this is equivalent to: EVERY finite P subset T(3) admits a
partition into 8 classes of diameter <= 1, i.e. is 8-colourable in the graph
G(P) with edges {p,q} whenever dist(p,q) > 1.

  * UNSAT for some finite P   ==>  NO 8-cover exists (exact finite refutation).
  * SAT                        ==>  nothing.  P was too weak.  (This is the trap
                                    the previous attempt fell into.)

All distances are compared EXACTLY: lattice points have x in Q and y in Q*sqrt3,
so squared distances are rational.
"""
import sys, os, time, json, itertools
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def tri_lattice(a, m):
    """Triangular lattice of spacing a/m inside T(a) (a rational).
    Returns list of (xq, yq) with real point (xq, yq*sqrt3)."""
    h = F(a) / m
    pts = []
    for j in range(m + 1):
        for i in range(m + 1 - j):
            x = h * i + h * j / 2
            y = h * j / 2          # true y = y*sqrt3
            pts.append((x, y))
    return pts


def sqdist(p, q):
    dx = p[0] - q[0]
    dy = p[1] - q[1]
    return dx * dx + 3 * dy * dy


def build_edges(pts, thresh=1):
    E = []
    n = len(pts)
    for i in range(n):
        for j in range(i + 1, n):
            if sqdist(pts[i], pts[j]) > thresh:
                E.append((i, j))
    return E


def greedy_clique(pts, E, n):
    adj = [set() for _ in range(n)]
    for i, j in E:
        adj[i].add(j); adj[j].add(i)
    best = []
    order = sorted(range(n), key=lambda v: -len(adj[v]))
    for start in order[:60]:
        cl = [start]
        cand = set(adj[start])
        while cand:
            v = max(cand, key=lambda u: len(adj[u] & cand))
            cl.append(v)
            cand &= adj[v]
        if len(cl) > len(best):
            best = cl
    return best


def colourable(pts, k, verbose=True, want_model=True):
    from pysat.solvers import Cadical195
    from pysat.formula import IDPool
    n = len(pts)
    E = build_edges(pts)
    pool = IDPool()
    v = lambda p, c: pool.id(("x", p, c))
    s = Cadical195()
    for p in range(n):
        s.add_clause([v(p, c) for c in range(k)])
    for (i, j) in E:
        for c in range(k):
            s.add_clause([-v(i, c), -v(j, c)])
    cl = greedy_clique(pts, E, n)
    for idx, p in enumerate(cl[:k]):
        s.add_clause([v(p, idx)])
    t0 = time.time()
    sat = s.solve()
    dt = time.time() - t0
    if verbose:
        print(f"  n={n} edges={len(E)} clique>={len(cl)} k={k} -> "
              f"{'SAT' if sat else 'UNSAT'}  ({dt:.2f}s)")
    model = None
    if sat and want_model:
        mset = set(x for x in s.get_model() if x > 0)
        model = []
        for p in range(n):
            for c in range(k):
                if v(p, c) in mset:
                    model.append(c); break
    s.delete()
    return sat, model, len(cl), len(E), dt


if __name__ == "__main__":
    a = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    k = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    ms = [int(x) for x in sys.argv[3].split(",")] if len(sys.argv) > 3 else [3, 6, 9, 12]
    out = []
    for m in ms:
        pts = tri_lattice(a, m)
        print(f"T({a}) lattice spacing {a}/{m}:")
        sat, model, cl, ne, dt = colourable(pts, k)
        out.append({"a": a, "k": k, "m": m, "n": len(pts), "edges": ne,
                    "clique": cl, "sat": sat, "sec": dt})
        if not sat:
            print("  *** UNSAT: no k-cover of T(a) exists ***")
            break
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"sat_a{a}_k{k}.json")
    json.dump(out, open(p, "w"), indent=2)
    print("wrote", p)
