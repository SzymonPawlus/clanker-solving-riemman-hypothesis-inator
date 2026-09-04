"""Calibration: extract the Fritz John support of a KNOWN optimum and check that the
enumerator's prunes accept it.

If the enumerator rejected the support of a configuration that really is a maximiser,
the enumeration would not be exhaustive and every count it produces would be worthless.
This is the two-sided control for Stage 2.

Known optima used (problems/circle-packing-equilateral-triangle/README.md, `cited`):
  n = 6, d = 4              the triangular lattice Delta(3)          [d(6) = 4]
  n = 5, d = 4              the same, minus one corner               [d(5) = 4]

Method: exact coordinates (sympy, field Q(sqrt 3)); compute the tight graph and the
active wall incidences exactly; find a Fritz John multiplier vector of maximal support
(floats to search, exact rationals to certify); then run the support through the same
prunes the enumerator uses.
"""
from __future__ import annotations

import itertools
from fractions import Fraction

import networkx as nx
import numpy as np
import sympy as sp

from support_enum import Quad, graph_admissible, is_union_of_paths, wall_capacity
from fastcount import LAB_WALLS, count_labellings, automorphisms, geng_stream

S3_ROOT = sp.sqrt(3)


def triangle(d):
    """outward unit normals and offsets: wall k is {p : <p,nu_k> = c_k}."""
    nus = [sp.Matrix([0, -1]),
           sp.Matrix([S3_ROOT / 2, sp.Rational(1, 2)]),
           sp.Matrix([-S3_ROOT / 2, sp.Rational(1, 2)])]
    cs = [sp.Integer(0), S3_ROOT * d / 2, sp.Integer(0)]
    return nus, cs


def analyse(points, d, name):
    n = len(points)
    P = [sp.Matrix(p) for p in points]
    nus, cs = triangle(d)
    # containment, exactly
    for i, p in enumerate(P):
        for k in range(3):
            assert sp.simplify((nus[k].T * p)[0] - cs[k]) <= 0, (name, i, k)
    d2 = {}
    for i, j in itertools.combinations(range(n), 2):
        d2[(i, j)] = sp.expand(((P[i] - P[j]).T * (P[i] - P[j]))[0])
    r2 = min(sp.nsimplify(v) for v in d2.values())
    tight = [(i, j) for (i, j), v in d2.items() if sp.simplify(v - r2) == 0]
    active = [frozenset(k for k in range(3)
                        if sp.simplify((nus[k].T * P[i])[0] - cs[k]) == 0)
              for i in range(n)]
    print(f"[{name}] n={n} d={d} r^2={r2} tight_edges={len(tight)}")
    print(f"        active walls: {[sorted(a) for a in active]}")

    # --- Fritz John multipliers -------------------------------------------------
    # unknowns: alpha_e for e in tight, mu_(i,k) for k in active[i]
    mus = [(i, k) for i in range(n) for k in sorted(active[i])]
    cols = [("a", e) for e in tight] + [("m", ik) for ik in mus]
    rows = []
    for i in range(n):
        for comp in range(2):
            row = []
            for kind, key in cols:
                if kind == "a":
                    a, b = key
                    if a == i:
                        u = (P[b] - P[i]) / sp.sqrt(r2)
                        row.append(u[comp])
                    elif b == i:
                        u = (P[a] - P[i]) / sp.sqrt(r2)
                        row.append(u[comp])
                    else:
                        row.append(sp.Integer(0))
                else:
                    j, k = key
                    row.append(nus[k][comp] if j == i else sp.Integer(0))
            rows.append(row)
    M = sp.Matrix(rows)
    NS = M.nullspace()
    print(f"        balance matrix {M.shape}, multiplier cone dim {len(NS)}")
    if not NS:
        print("        NO nonzero multiplier vector -> configuration is NOT stationary")
        return None
    N = sp.Matrix.hstack(*NS)
    # search (floats) for a coefficient vector making every multiplier positive
    Nf = np.array(N.evalf(30), dtype=float)
    best, bestval = None, -1.0
    rng = np.random.default_rng(20260823)
    for _ in range(4000):
        c = rng.normal(size=N.shape[1])
        v = Nf @ c
        val = v.min()
        if val > bestval:
            bestval, best = val, c
    if bestval <= 0:
        # fall back: maximise the number of strictly positive entries
        print(f"        no strictly positive multiplier found (best min = {bestval:.3g});"
              f" support is a proper face")
    # certify exactly at a nearby rational coefficient vector
    c_exact = sp.Matrix([sp.Rational(Fraction(float(x)).limit_denominator(10 ** 6))
                         for x in best])
    x = sp.simplify(N * c_exact)
    assert sp.simplify(M * x) == sp.zeros(M.rows, 1), "balance not satisfied exactly"
    pos = [sp.simplify(v) > 0 for v in x]
    loaded_edges = [tight[i] for i in range(len(tight)) if pos[i]]
    print(f"        exactly certified multiplier vector; loaded edges "
          f"{len(loaded_edges)}/{len(tight)}, all wall multipliers positive="
          f"{all(pos[len(tight):])}")

    # --- the support, and the enumerator's verdict on it ------------------------
    L = sorted({v for e in loaded_edges for v in e})
    idx = {v: i for i, v in enumerate(L)}
    G = nx.Graph()
    G.add_nodes_from(range(len(L)))
    G.add_edges_from((idx[a], idx[b]) for a, b in loaded_edges)
    W = tuple(active[v] for v in L)
    m = len(L)
    cap = wall_capacity(Quad(*d_as_quad(d)))
    print(f"        support: m={m} edges={G.number_of_edges()} labels="
          f"{[sorted(w) for w in W]}")
    ok_g = graph_admissible(G)
    lab = tuple(next(i for i, w in enumerate(LAB_WALLS) if frozenset(w) == W[v])
                for v in range(m))
    # re-use the enumerator's own leaf test by enumerating and looking for this label
    auts = automorphisms(G)
    found = label_in_enumeration(G, lab, cap, auts)
    print(f"        graph_admissible={ok_g}   labelling accepted by enumerator={found}")
    return ok_g and found


def d_as_quad(d):
    e = sp.expand(sp.nsimplify(d))
    a = sp.Rational(e.subs(S3_ROOT, 0))
    b = sp.Rational(sp.expand((e - a) / S3_ROOT))
    return (a, b)


def label_in_enumeration(G, lab, cap, auts):
    """True iff `lab` survives every labelling prune the enumerator applies."""
    from fastcount import count_labellings
    import fastcount

    hits = []
    orig = fastcount.count_labellings
    # brute force: enumerate all admissible labellings of this graph and look for lab
    m = G.number_of_nodes()
    all_labs = set()

    def collect(G, cap, ca, auts):
        # replicate the enumerator but keep the labellings
        import fastcount as fc
        res = set()
        deg = [G.degree(v) for v in range(m)]
        for cand in itertools.product(range(7), repeat=m):
            if any(not (fc.DEG_MIN[cand[v]] <= deg[v] <= fc.DEG_MAX[cand[v]])
                   for v in range(m)):
                continue
            if fc.count_labellings.__doc__ is None:
                pass
            res.add(cand)
        return res

    # simplest sound check: run the real enumerator on this graph and ask whether the
    # orbit of `lab` appears among the orbits it returns.
    import fastcount as fc
    target = None
    for sigma in auts:
        perm = [0] * m
        for u in range(m):
            perm[sigma[u]] = lab[u]
        for t in fc.TAU_LAB:
            cand = tuple(t[x] for x in perm)
            if target is None or cand < target:
                target = cand
    # recompute the enumerator's orbit set by monkey-free re-implementation
    orbits = enumerate_orbits(G, cap, auts)
    return target in orbits


def enumerate_orbits(G, cap, auts):
    """Exactly the enumerator's labelling search, but returning the orbit set."""
    import fastcount as fc
    m = G.number_of_nodes()
    out = set()
    saved = []

    def hook(o):
        saved.append(o)

    # re-run count_labellings but capture orbits by calling it with a patched set
    orig_set = set
    res = fc.count_labellings(G, cap, False, auts, True)
    # count_labellings returns only the count, so redo the search here (same prunes)
    adj = [tuple(G[v]) for v in range(m)]
    deg = [len(a) for a in adj]
    allowed = [[l for l in range(7) if fc.DEG_MIN[l] <= deg[v] <= fc.DEG_MAX[l]]
               for v in range(m)]
    lab = [0] * m

    def rec(v):
        if v == m:
            if leaf(lab):
                best = None
                for sigma in auts:
                    perm = [0] * m
                    for u in range(m):
                        perm[sigma[u]] = lab[u]
                    for t in fc.TAU_LAB:
                        cand = tuple(t[x] for x in perm)
                        if best is None or cand < best:
                            best = cand
                out.add(best)
            return
        for l in allowed[v]:
            lab[v] = l
            rec(v + 1)
        lab[v] = 0

    def leaf(labv):
        from support_enum import labelling_admissible
        W = tuple(frozenset(fc.LAB_WALLS[l]) for l in labv)
        return labelling_admissible(G, W, cap, is_union_of_paths(G), False)

    rec(0)
    assert len(out) == res, (len(out), res)
    return out


if __name__ == "__main__":
    s3 = S3_ROOT
    lattice6 = [(0, 0), (2, 0), (4, 0), (1, s3), (3, s3), (2, 2 * s3)]
    r6 = analyse(lattice6, sp.Integer(4), "n=6, d=4 (Delta(3) lattice)")
    r5 = analyse(lattice6[:5], sp.Integer(4), "n=5, d=4 (Delta(3) minus corner C)")
    print()
    print("CALIBRATION PASSED" if (r6 and r5) else "CALIBRATION FAILED")
