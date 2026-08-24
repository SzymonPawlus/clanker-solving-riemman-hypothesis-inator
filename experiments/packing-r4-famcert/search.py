"""Exact resolution of the seam-depth freedom: independent sets over the
four-grain candidate sites.

The mechanism fixes the four grain OFFSETS but not the grain EXTENTS.  Choosing
extents by eye is exactly what made the round-4 lens's first n = 49 transcription
infeasible.  So instead of transcribing, we solve, for each j:

  (F) FEASIBILITY -- is there a subset of U(d) of size n(j) with all pairwise
      distances >= 2?   A yes is a CONSTRUCTION: s(n(j)) <= 2j + 4 sqrt(3).
  (M) MAXIMALITY   -- is there one of size n(j)+1?   A no says the mechanism is
      saturated at exactly the family value (this is NOT an optimality claim
      about s(n): it only says this candidate LATTICE UNION holds no more).

The conflict graph is built in exact Q(sqrt 3) arithmetic -- an edge is placed
iff the squared distance is EXACTLY < 4, decided by the exact sign rule.  No
float participates.  The independent-set search is combinatorial (SAT), hence
exact by construction; and its output is re-checked from scratch by check.py.

Determinism: the SAT solver is used with a fixed CNF built in a fixed candidate
order, single-threaded, no randomisation.  Reruns reproduce the same witness.
"""
import json
import os
import sys
import time

from qsqrt3 import Q3, q3
from candidates import candidates, d_of

FOUR = q3(4)
HERE = os.path.dirname(os.path.abspath(__file__))
CKPT = os.path.join(HERE, "out")


def conflict_graph(cands):
    n = len(cands)
    pts = [c[3] for c in cands]
    edges = []
    for a in range(n):
        xa, ya = pts[a]
        for b in range(a + 1, n):
            dx = xa - pts[b][0]
            dy = ya - pts[b][1]
            if dx * dx + dy * dy < FOUR:
                edges.append((a, b))
    return edges


def _solve_at_least(nv, edges, k):
    from pysat.formula import IDPool, CNF
    from pysat.card import CardEnc, EncType
    from pysat.solvers import Cadical153
    pool = IDPool(start_from=nv + 1)
    cnf = CNF()
    for (a, b) in edges:
        cnf.append([-(a + 1), -(b + 1)])
    cnf.extend(CardEnc.atleast(lits=list(range(1, nv + 1)), bound=k,
                               vpool=pool, encoding=EncType.seqcounter).clauses)
    with Cadical153(bootstrap_with=cnf) as sol:
        if sol.solve():
            m = sol.get_model()
            return [v - 1 for v in m[:nv] if v > 0]
        return None


def run(j, want, do_maximality=True, verbose=True):
    os.makedirs(CKPT, exist_ok=True)
    t0 = time.time()
    cands = candidates(j)
    edges = conflict_graph(cands)
    nv = len(cands)
    res = {"j": j, "n_target": want, "d": d_of(j).sexpr(),
           "n_candidates": nv, "n_conflict_edges": len(edges)}
    sel = _solve_at_least(nv, edges, want)
    res["feasible_at_n"] = sel is not None
    if sel is not None:
        res["witness"] = [[cands[v][0], cands[v][1], cands[v][2]] for v in sel]
        res["points"] = [[cands[v][3][0].sexpr(), cands[v][3][1].sexpr()] for v in sel]
    res["t_feas"] = round(time.time() - t0, 1)
    if verbose:
        print("j=%d n=%d d=%-16s |U|=%3d |E|=%4d  FEASIBLE=%s  (%.1fs)"
              % (j, want, res["d"], nv, len(edges), res["feasible_at_n"], res["t_feas"]),
              flush=True)
    # checkpoint before the (possibly slow) maximality proof
    with open(os.path.join(CKPT, "j%02d.json" % j), "w") as f:
        json.dump(res, f, indent=1)
    if do_maximality and sel is not None:
        t1 = time.time()
        more = _solve_at_least(nv, edges, want + 1)
        res["feasible_at_n_plus_1"] = more is not None
        res["maximal_in_candidate_union"] = more is None
        res["t_max"] = round(time.time() - t1, 1)
        if verbose:
            print("   n+1 = %d in the candidate union: %s  (%.1fs)"
                  % (want + 1, more is not None, res["t_max"]), flush=True)
        if more is not None:
            res["points_n_plus_1"] = [[cands[v][3][0].sexpr(), cands[v][3][1].sexpr()]
                                      for v in more]
        with open(os.path.join(CKPT, "j%02d.json" % j), "w") as f:
            json.dump(res, f, indent=1)
    return res


if __name__ == "__main__":
    from family_law import law_n
    args = sys.argv[1:]
    do_max = "--nomax" not in args
    js = [int(a) for a in args if not a.startswith("--")] or list(range(0, 8))
    for j in js:
        run(j, law_n(j), do_maximality=do_max)
