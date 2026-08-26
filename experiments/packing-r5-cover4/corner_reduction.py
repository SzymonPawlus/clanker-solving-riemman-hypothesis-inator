"""Rigorous reduction, then a much smaller finite refutation problem.

REDUCTION (exact, no computation needed).  Suppose T(3) = S_1 u ... u S_8 with
diam(S_i) <= 1.  The three corners A,B,C are pairwise at distance 3 > 1, so they
lie in three distinct pieces S_A,S_B,S_C.  A piece containing the corner V has
diameter <= 1, hence S_V is contained in the closed sector
        R_V = T(3) n Bbar(V,1)      (a 60-degree sector of radius 1).
Therefore the remaining FIVE pieces must cover
        U = { z in T(3) : |z - V| > 1 for every corner V }.

So:  T(3) has an 8-cover by diameter-<=1 sets  ==>  U has a 5-cover by
diameter-<=1 sets.  Contrapositive: a finite P subset U that is not 5-colourable
in the graph (edge iff dist > 1) REFUTES the 8-cover, hence refutes the whole
covering route to EO(4).

Coordinates: (x,u) means the real point (x, u*sqrt3).  Everything rational:
  in T(a):   u >= 0,  u <= x,  u <= a - x
  |z-A|^2 = x^2 + 3u^2 ;  |z-B|^2 = (x-a)^2 + 3u^2 ;
  |z-C|^2 = (x-a/2)^2 + 3(u-a/2)^2
"""
import sys, os, time, json, random
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from adaptive_sat import inside, sqd, solve, fpt

A3 = 3


def in_U(p, a=3, rmin2=1):
    x, u = p
    if not inside(p, a):
        return False
    if x * x + 3 * u * u <= rmin2:
        return False
    if (x - a) ** 2 + 3 * u * u <= rmin2:
        return False
    if (x - F(a, 2)) ** 2 + 3 * (u - F(a, 2)) ** 2 <= rmin2:
        return False
    return True


def grid_U(a, N):
    pts = []
    for j in range(N + 1):
        for i in range(N + 1 - j):
            p = (F(a) * (2 * i + j) / (2 * N), F(a) * j / (2 * N))
            if in_U(p, a):
                pts.append(p)
    return pts


def rand_U(a, n, seed):
    rng = random.Random(seed)
    D = 2000
    out = []
    while len(out) < n:
        x = F(rng.randrange(0, D * a + 1), D)
        u = F(rng.randrange(0, D * a // 2 + 1), D)
        if in_U((x, u), a):
            out.append((x, u))
    return out


if __name__ == "__main__":
    a = 3
    k = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    Ns = [int(v) for v in (sys.argv[2].split(",") if len(sys.argv) > 2
                           else "6,9,12,15,18,24,30,36".split(","))]
    res = []
    for N in Ns:
        P = grid_U(a, N)
        if len(P) < 3:
            continue
        sat, col, ne, cq, dt = solve(P, k)
        print(f"U grid N={N}: |P|={len(P)} edges={ne} clique>={cq} k={k} -> "
              f"{'SAT' if sat else 'UNSAT'}  ({dt:.2f}s)", flush=True)
        res.append({"N": N, "n": len(P), "edges": ne, "clique": cq,
                    "sat": bool(sat), "sec": dt})
        if not sat:
            print("*** UNSAT ***"); break
    # random supplements
    for n in (150, 300, 600):
        P = grid_U(a, 12) + rand_U(a, n, 7)
        sat, col, ne, cq, dt = solve(P, k)
        print(f"U grid12+rand{n}: |P|={len(P)} edges={ne} clique>={cq} -> "
              f"{'SAT' if sat else 'UNSAT'} ({dt:.2f}s)", flush=True)
        res.append({"rand": n, "n": len(P), "edges": ne, "clique": cq,
                    "sat": bool(sat), "sec": dt})
        if not sat:
            print("*** UNSAT ***"); break
    d = os.path.dirname(os.path.abspath(__file__))
    json.dump(res, open(os.path.join(d, f"corner_reduction_k{k}.json"), "w"), indent=2)
