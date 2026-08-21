"""The chi-vs-omega tool: the only route to a floor of 27.

For a 1-separated set P in T_a with |P| = m, let Z = { z in T_a : |z-p| >= 1 for all p in P }.
In any covering of T_a by pieces of diameter < 1 the m points of P occupy m distinct pieces, and
no point of Z lies in any of them, so

        N*(a)  >=  m + chi(G_Z)                                                   (*)

where G_Z is the "distance >= 1" graph on ANY finite subset of Z (a finite subgraph only lowers
chi, so (*) stays a valid lower bound).  Note m + alpha(G_Z) is just "a bigger separated set", so
(*) beats the separated-point bound exactly when chi(G_Z) > alpha(G_Z).

Everything here is exact rational arithmetic in triangular coordinates (see exactlib).
"""
import json, os, sys
from fractions import Fraction as F
from collections import deque
from exactlib import d2, in_triangle

HERE = os.path.dirname(os.path.abspath(__file__))

def free_grid(P, a, q):
    """All points of the (1/q)-triangular lattice inside T_a at squared distance >= 1 from every
    point of P.  A finite subset of Z."""
    Z = []
    N = int(a * q)
    for iu in range(N + 1):
        u = F(iu, q)
        for iv in range(N + 1 - iu):
            v = F(iv, q)
            if u + v > a:
                continue
            z = (u, v)
            ok = True
            for p in P:
                if d2(z, p) < 1:
                    ok = False; break
            if ok:
                Z.append(z)
    return Z

def graph(Z):
    n = len(Z)
    adj = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if d2(Z[i], Z[j]) >= 1:
                adj[i].append(j); adj[j].append(i)
    return adj

def bipartite(adj):
    """Return (is_bipartite, odd_cycle_witness_or_None)."""
    n = len(adj); col = [-1] * n; par = [-1] * n
    for s in range(n):
        if col[s] != -1: continue
        col[s] = 0; dq = deque([s])
        while dq:
            x = dq.popleft()
            for y in adj[x]:
                if col[y] == -1:
                    col[y] = 1 - col[x]; par[y] = x; dq.append(y)
                elif col[y] == col[x]:
                    # recover an odd closed walk through x-y
                    px = [x]
                    while par[px[-1]] != -1: px.append(par[px[-1]])
                    py = [y]
                    while par[py[-1]] != -1: py.append(par[py[-1]])
                    return False, (px, py)
    return True, None

def greedy_clique(Z, adj, rounds=200):
    """A lower bound on alpha(G_Z) = the largest 1-separated subset of Z."""
    import random
    rng = random.Random(7)
    n = len(Z); best = []
    order = list(range(n))
    for r in range(rounds):
        rng.shuffle(order)
        cur = []
        adjset = None
        for i in order:
            ok = True
            for j in cur:
                if d2(Z[i], Z[j]) < 1:
                    ok = False; break
            if ok: cur.append(i)
        if len(cur) > len(best): best = list(cur)
    return best

def analyse(P, a, q, label):
    Z = free_grid(P, a, q)
    m = len(P)
    if not Z:
        return {"label": label, "m": m, "|Z_grid|": 0, "chi_lb": 0, "floor": m}
    adj = graph(Z)
    ne = sum(len(x) for x in adj) // 2
    if ne == 0:
        chi_lb = 1; witness = None
    else:
        bip, w = bipartite(adj)
        chi_lb = 2 if bip else 3
        witness = None if bip else "odd cycle"
    cl = greedy_clique(Z, adj)
    alpha_lb = len(cl)
    return {"label": label, "m": m, "|Z_grid|": len(Z), "edges": ne,
            "chi_lb": chi_lb, "alpha_lb": alpha_lb, "witness": witness,
            "floor": m + chi_lb, "separated_total": m + alpha_lb}

if __name__ == '__main__':
    cert = json.load(open(os.path.join(HERE, 'out', 'certificates.json')))
    q = int(sys.argv[1]) if len(sys.argv) > 1 else 16
    which = int(sys.argv[2]) if len(sys.argv) > 2 else 25
    entry = [c for c in cert if c.get('certified') and c['n'] == which]
    if not entry:
        print("no certificate for n =", which); sys.exit(1)
    e = entry[0]
    a = F(e['a']); P = [(F(x), F(y)) for x, y in e['pts']]
    print(f"base certificate: n={e['n']}  a={float(a):.7f}  grid 1/{q}")
    res = [analyse(P, a, q, "full")]
    print(res[0], flush=True)
    n = len(P)
    # delete one point, then two, and look for a chi>alpha gap in the freed region
    for i in range(n):
        Q = [P[j] for j in range(n) if j != i]
        r = analyse(Q, a, q, f"-{i}")
        res.append(r)
        if r['chi_lb'] >= 3 or r['floor'] >= 27:
            print("  !!", r, flush=True)
    best = max(res, key=lambda r: r['floor'])
    print("best floor from (*):", best)
    with open(os.path.join(HERE, 'out', f'gap_n{which}_q{q}.json'), 'w') as f:
        json.dump(res, f, indent=1)
