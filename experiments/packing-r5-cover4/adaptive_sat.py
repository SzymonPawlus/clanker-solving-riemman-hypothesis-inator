"""Adaptive finite refutation attempt for the k=4 covering question.

Points are stored as (x, u) with the real point (x, u*sqrt3); x,u rational.
Containment in T(a) is then RATIONAL:  u >= 0, u <= x, u <= a - x.
Squared distance is RATIONAL:  (dx)^2 + 3 (du)^2.   No floats in any decision.

Loop:
  1. SAT: can P be 8-coloured so that every class has diameter <= 1?
     (edges = pairs at squared distance > 1)
  2. UNSAT -> NO 8-cover of T(a) exists.  Done, exact finite certificate.
  3. SAT   -> classes C_i.  A point x can join class i only if
     max_{p in C_i} |x-p| <= 1.  Points that can join NO class are cuts:
     they force the next colouring to differ.  Add the best ones and repeat.
"""
import sys, os, time, json, random
from fractions import Fraction as F
S3 = 1.7320508075688772


def inside(p, a):
    x, u = p
    return u >= 0 and u <= x and u <= a - x


def sqd(p, q):
    dx = p[0] - q[0]; du = p[1] - q[1]
    return dx * dx + 3 * du * du


def fpt(p):
    return (float(p[0]), float(p[1]) * S3)


def build_edges(P):
    E = []
    n = len(P)
    for i in range(n):
        for j in range(i + 1, n):
            if sqd(P[i], P[j]) > 1:
                E.append((i, j))
    return E


def greedy_clique(P, E):
    n = len(P)
    adj = [set() for _ in range(n)]
    for i, j in E:
        adj[i].add(j); adj[j].add(i)
    best = []
    for start in sorted(range(n), key=lambda v: -len(adj[v]))[:40]:
        cl = [start]; cand = set(adj[start])
        while cand:
            v = max(cand, key=lambda u: len(adj[u] & cand))
            cl.append(v); cand &= adj[v]
        if len(cl) > len(best):
            best = cl
    return best


def solve(P, k, timeout_conf=0):
    from pysat.solvers import Cadical195
    n = len(P)
    E = build_edges(P)
    var = lambda p, c: p * k + c + 1
    s = Cadical195()
    for p in range(n):
        s.add_clause([var(p, c) for c in range(k)])
    for (i, j) in E:
        for c in range(k):
            s.add_clause([-var(i, c), -var(j, c)])
    cl = greedy_clique(P, E)
    for idx, p in enumerate(cl[:k]):
        s.add_clause([var(p, idx)])
    t0 = time.time()
    sat = s.solve()
    dt = time.time() - t0
    col = None
    if sat:
        m = set(x for x in s.get_model() if x > 0)
        col = [next(c for c in range(k) if var(p, c) in m) for p in range(n)]
    s.delete()
    return sat, col, len(E), len(cl), dt


def candidates(a, N, rng):
    """rational candidate points: fine triangular grid + random."""
    out = []
    for j in range(N + 1):
        for i in range(N + 1 - j):
            out.append((F(a) * (2 * i + j) / (2 * N), F(a) * j / (2 * N)))
    for _ in range(4000):
        x = F(rng.randrange(0, 1000 * a + 1), 1000)
        u = F(rng.randrange(0, 500 * a + 1), 1000)
        if inside((x, u), a):
            out.append((x, u))
    return out


def run(a=3, k=8, rounds=40, seed=0, add=12, N=45, log=None):
    rng = random.Random(seed)
    # seed set: corners + midpoints + a coarse lattice
    P = []
    for j in range(4):
        for i in range(4 - j):
            P.append((F(a) * (2 * i + j) / 6, F(a) * j / 6))
    P = list(dict.fromkeys(P))
    cands = candidates(a, N, rng)
    hist = []
    for r in range(rounds):
        sat, col, ne, cq, dt = solve(P, k)
        print(f"round {r}: |P|={len(P)} edges={ne} clique>={cq} -> "
              f"{'SAT' if sat else 'UNSAT'} ({dt:.2f}s)", flush=True)
        hist.append({"round": r, "n": len(P), "edges": ne, "clique": cq,
                     "sat": bool(sat), "sec": dt})
        if log:
            json.dump(hist, open(log, "w"), indent=2)
        if not sat:
            return P, hist, True
        # --- cut generation (float search, exact re-check on the chosen points)
        cls = [[] for _ in range(k)]
        for idx, c in enumerate(col):
            cls[c].append(fpt(P[idx]))
        best = []
        for q in cands:
            fq = fpt(q)
            score = 1e9
            for C in cls:
                if not C:
                    score = -1e9; break
                v = max((fq[0] - p[0]) ** 2 + (fq[1] - p[1]) ** 2 for p in C) - 1.0
                if v < score:
                    score = v
                if score <= 0:
                    break
            if score > 0:
                best.append((score, q))
        if not best:
            print("  no cut point found from candidate pool")
            return P, hist, False
        best.sort(key=lambda t: -t[0])
        chosen = []
        for sc, q in best:
            if all(sqd(q, o) > F(1, 100) for o in chosen) and q not in P:
                chosen.append(q)
            if len(chosen) >= add:
                break
        print(f"  adding {len(chosen)} cut points, best score {best[0][0]:.4f}")
        P.extend(chosen)
    return P, hist, False


if __name__ == "__main__":
    a = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    k = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    rounds = int(sys.argv[3]) if len(sys.argv) > 3 else 40
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    d = os.path.dirname(os.path.abspath(__file__))
    log = os.path.join(d, f"adaptive_a{a}_k{k}_s{seed}.json")
    P, hist, unsat = run(a, k, rounds, seed, log=log)
    print("UNSAT reached" if unsat else "still SAT")
    json.dump({"unsat": unsat, "hist": hist,
               "P": [[str(p[0]), str(p[1])] for p in P]},
              open(log, "w"), indent=2)
