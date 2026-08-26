"""Two independent cross-checks of the headline n = 12 refutation.

(A) ADJACENCY.  The search decides conflicts with the integer identity
    |a*u+b*v|^2 = h^2 (a^2+ab+b^2).  Here the same decision is recomputed from the
    Cartesian vertex coordinates in Q(sqrt 3) with `fractions.Fraction` pairs
    (x = r + s*sqrt3 is stored as (r,s)); no float, no shared code path.

(B) SEARCH.  The verdict "no independent set of size n" is re-decided by a SAT
    solver (glucose4 through pysat) on a CNF built directly from the adjacency
    bitsets.  Two independent search procedures; agreement is a cross-check, not a
    proof.
"""
import random
import sys
from fractions import Fraction

sys.path.insert(0, ".")
from arbb import geom


def sq_dist_exact(v1, v2, h):
    """Squared distance between two lattice vertices, computed in Q(sqrt3) from the
    Cartesian coordinates x = h*(a + b/2), y = h*b*sqrt(3)/2."""
    (a1, b1), (a2, b2) = v1, v2
    dx = h * (Fraction(a1 - a2) + Fraction(b1 - b2, 2))          # rational
    dy_over_sqrt3 = h * Fraction(b1 - b2, 2)                     # dy = that * sqrt3
    return dx * dx + 3 * dy_over_sqrt3 * dy_over_sqrt3           # rational


def check_adjacency(L, p, q, samples=4000, seed=20260826):
    rng = random.Random(seed)
    adj, cells, verts = geom.conflict_bitsets(L, p, q)
    h = Fraction(p, q) / (1 << L)
    M = len(adj)
    bad = 0
    for _ in range(samples):
        e = rng.randrange(M)
        f = rng.randrange(M)
        if e == f:
            continue
        mx = max(sq_dist_exact(tuple(verts[i]), tuple(verts[j]), h)
                 for i in cells[e] for j in cells[f])
        want = mx < 4
        got = bool((adj[e] >> f) & 1)
        if want != got:
            bad += 1
    return bad, M


def check_sat(n, p, q, L, timeout_note=""):
    from pysat.card import CardEnc, EncType
    from pysat.formula import IDPool
    from pysat.solvers import Solver
    adj, cells, verts = geom.conflict_bitsets(L, p, q)
    M = len(adj)
    pool = IDPool(start_from=M + 1)
    cnf = []
    for e in range(M):
        it = adj[e] >> (e + 1)
        base = e + 1
        while it:
            b = it & -it
            f = e + 1 + b.bit_length() - 1
            cnf.append([-(e + 1), -(f + 1)])
            it ^= b
    card = CardEnc.atleast(lits=list(range(1, M + 1)), bound=n, vpool=pool,
                           encoding=EncType.seqcounter)
    with Solver(name="glucose4", bootstrap_with=cnf + card.clauses) as s:
        res = s.solve()
    return ("sat" if res else "unsat"), M, len(cnf) + len(card.clauses)


if __name__ == "__main__":
    print("(A) adjacency recomputed in Q(sqrt3) from Cartesian coordinates")
    for (L, p, q) in [(4, 7, 1), (5, 71, 10), (5, 7, 1), (5, 15, 2)]:
        bad, M = check_adjacency(L, p, q)
        print(f"    L={L} d={p}/{q}: {M} cells, disagreements on 4000 random pairs = {bad}")
    print("(B) verdict re-decided by glucose4 on the same graph")
    for (n, p, q, L) in [(12, 72, 10, 5), (12, 15, 2, 5), (12, 4, 1, 4), (12, 55, 10, 4),
                         (12, 6, 1, 4), (12, 65, 10, 5), (12, 71, 10, 5)]:
        r, M, nc = check_sat(n, p, q, L)
        print(f"    n={n} d={p}/{q} L={L}: glucose4 says {r}  ({M} vars, {nc} clauses)",
              flush=True)
