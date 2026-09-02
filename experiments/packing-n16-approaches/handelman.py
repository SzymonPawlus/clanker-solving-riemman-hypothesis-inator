#!/usr/bin/env python3
"""Kill-experiment: Handelman/Krivine LP Positivstellensatz for packing infeasibility.

Proposal (worker I1, issue #97).  Fix a.  The system
    u_i >= 0, v_i >= 0, a-u_i-v_i >= 0            (containment, oblique coords)
    q_ij = du^2+du*dv+dv^2-1 >= 0                 (pairwise Euclid >= 1, rational!)
is infeasible iff n points at pairwise distance >= 1 do not fit T_a, i.e. iff
a < a_n.  A Krivine/Handelman-style certificate of infeasibility is an identity
    sum_alpha  lambda_alpha * (product of generators)  =  -1,   lambda >= 0,
which is verifiable in EXACT rational arithmetic (it is a finite list of
rationals) -- the certificate itself would be a lower-bound proof for a_n.
Finding one at bounded product-degree is a pure LP: no SDP solver needed, which
matters because this environment has scipy only.

CALIBRATION GATE (fixed in advance): run n=4 (a_4 = sqrt3 = 1.7320508, cited).
Bisect the largest a for which a degree-<=4 certificate exists.  If that value
h4 is below 1.6 (relative slack > ~7.6%), the LP hierarchy at affordable degree
is far too slack for n=16 (whose covering record sits 3.5% below the best
packing) => proposal dies.  Floats decide only the SEARCH; any positive claim
would need exact rationalization (not done here -- this is a triage run).
"""
import itertools, numpy as np
from scipy.optimize import linprog
from scipy.sparse import csc_matrix

N = 4          # points
NV = 2 * N     # variables u0,v0,...  (var 2i = u_i, 2i+1 = v_i)
DEG = 4

# ---- sparse polynomial arithmetic: dict{exponent-tuple: float} -----------------

def pmul(p, q):
    r = {}
    for m1, c1 in p.items():
        for m2, c2 in q.items():
            m = tuple(a + b for a, b in zip(m1, m2))
            r[m] = r.get(m, 0.0) + c1 * c2
    return r

def mono(idx, c=1.0):
    e = [0] * NV
    for i in idx: e[i] += 1
    return {tuple(e): c}

def const(c): return {tuple([0]*NV): c}

def padd(p, q):
    r = dict(p)
    for m, c in q.items(): r[m] = r.get(m, 0.0) + c
    return r

def generators(a):
    lins, quads = [], []
    for i in range(N):
        lins.append(mono([2*i]))                       # u_i
        lins.append(mono([2*i+1]))                     # v_i
        s = padd(const(a), {tuple(e): -c for e, c in padd(mono([2*i]), mono([2*i+1])).items()})
        lins.append(s)                                 # a - u_i - v_i
    for i, j in itertools.combinations(range(N), 2):
        du = padd(mono([2*i]), {tuple(e): -c for e, c in mono([2*j]).items()})
        dv = padd(mono([2*i+1]), {tuple(e): -c for e, c in mono([2*j+1]).items()})
        q = padd(padd(pmul(du, du), pmul(du, dv)), pmul(dv, dv))
        q = padd(q, const(-1.0))
        quads.append(q)                                # |pi-pj|^2 - 1
    return lins, quads

def columns(a):
    lins, quads = generators(a)
    cols = [const(1.0)]
    # products of up to DEG linear generators
    for k in range(1, DEG + 1):
        for comb in itertools.combinations_with_replacement(range(len(lins)), k):
            p = const(1.0)
            for t in comb: p = pmul(p, lins[t])
            cols.append(p)
    # q * (up to DEG-2 linears)
    for q in quads:
        cols.append(q)
        for k in range(1, DEG - 1):
            for comb in itertools.combinations_with_replacement(range(len(lins)), k):
                p = q
                for t in comb: p = pmul(p, lins[t])
                cols.append(p)
    # q * q'
    for q1, q2 in itertools.combinations_with_replacement(range(len(quads)), 2):
        cols.append(pmul(quads[q1], quads[q2]))
    return cols

def cert_exists(a):
    cols = columns(a)
    monos = {}
    for p in cols:
        for m in p:
            if m not in monos: monos[m] = len(monos)
    zero = tuple([0]*NV)
    rows, cs, vals = [], [], []
    for j, p in enumerate(cols):
        for m, c in p.items():
            rows.append(monos[m]); cs.append(j); vals.append(c)
    A = csc_matrix((vals, (rows, cs)), shape=(len(monos), len(cols)))
    b = np.zeros(len(monos)); b[monos[zero]] = -1.0
    c = np.ones(len(cols))                       # minimize sum lambda (stability)
    res = linprog(c, A_eq=A, b_eq=b, bounds=[(0, None)] * len(cols),
                  method="highs")
    return res.success

if __name__ == "__main__":
    print(f"n={N}, product-degree <= {DEG}; a_4 = sqrt(3) = 1.7320508")
    lo, hi = 0.5, 1.7320508             # cert must exist a<lo? verify ends first
    for a in (0.5, 0.9, 1.0, 1.2, 1.4, 1.5, 1.6, 1.7):
        ok = cert_exists(a)
        print(f"  a = {a:6.4f}: certificate {'EXISTS' if ok else 'none'}")
    # bisect the frontier
    lo, hi = 0.5, 1.7320508
    if not cert_exists(lo):
        print("  no certificate even at a=0.5 -- LP route completely dead"); raise SystemExit
    for _ in range(18):
        mid = (lo + hi) / 2
        if cert_exists(mid): lo = mid
        else: hi = mid
    print(f"  degree-{DEG} Handelman value for n=4:  h4 in [{lo:.6f}, {hi:.6f}]")
    print(f"  slack vs a_4 = sqrt3: {1.7320508 - lo:.4f}  ({(1.7320508-lo)/1.7320508*100:.1f}%)")
    print("  GATE: h4 < 1.6 kills the proposal for n=16." )
