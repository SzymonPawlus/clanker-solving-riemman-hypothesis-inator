"""Construct a {0,1}-weighted Edmonds-Giles counterexample at tau_w = 2 by a shore-lattice search.
Status: numerical (the output is then re-verified by tau2lib, an independent brute-force path).

Idea.  Weight-1 arcs: three out-stars, gadget i = { i: a_i->b_i,  i': a_i->c_i,  i'': a_i->d_i }.
Prescribe nine shores whose weight-1 traces are
    P_i = {i, i'},  Q_i = {i, i''}   (forces colour(i') = colour(i'') != colour(i))
    R_1 = {1'', 2'}, R_2 = {2'', 3'}, R_3 = {3'', 1'}   (odd cycle on the gadget colours)
which is not 2-colourable.  Add *every* weight-0 arc x->y that enters none of the nine shores.
Fact (proved in the attack README, section on this construction): the dicut shores of that DAG are
exactly the nontrivial members of the union/intersection closure of the nine shores.  So we only
need a choice of the "wholesale" memberships of the other gadgets making every closure member
carry >= 2 weight-1 arcs.  Search over those choices (32768 cases)."""
from itertools import product
import json, sys

V = [f"{x}{i}" for i in (1, 2, 3) for x in "abcd"]
idx = {v: k for k, v in enumerate(V)}
def m(*names): return sum(1 << idx[x] for x in names)
G = {i: m(f"a{i}", f"b{i}", f"c{i}", f"d{i}") for i in (1, 2, 3)}
W1 = []   # weight-1 arcs (tail, head, label)
for i in (1, 2, 3):
    W1 += [(f"a{i}", f"b{i}", f"{i}"), (f"a{i}", f"c{i}", f"{i}'"), (f"a{i}", f"d{i}", f"{i}''")]
FULL = (1 << 12) - 1

def trace(U):
    return [lab for t, h, lab in W1 if (U >> idx[t]) & 1 and not (U >> idx[h]) & 1]

def closure(F):
    S = set(F)
    frontier = list(S)
    while frontier:
        new = []
        for x in frontier:
            for y in list(S):
                for z in (x & y, x | y):
                    if z not in S:
                        S.add(z); new.append(z)
        frontier = new
    return S


def principal(F):
    """S_y = intersection of the shores containing y (FULL if none)."""
    S = []
    for y in range(12):
        s = FULL
        for U in F:
            if (U >> y) & 1:
                s &= U
        S.append(s)
    return S

def all_downsets_ok(F):
    """Every nontrivial down-set of the DAG 'all arcs entering no shore' has >= 2 weight-1 arcs.
    Down-sets are exactly unions of principal sets S_y; BFS them with early exit."""
    S = principal(F)
    seen = {0}
    stack = [0]
    while stack:
        U = stack.pop()
        for y in range(12):
            if not (U >> y) & 1:
                W = U | S[y]
                if W in seen:
                    continue
                seen.add(W)
                if W != FULL and len(trace(W)) < 2:
                    return False
                stack.append(W)
    return True

others = {1: (2, 3), 2: (3, 1), 3: (1, 2)}
sols = []
for bits in product((0, 1), repeat=15):
    F = []
    k = 0
    for i in (1, 2, 3):
        P = m(f"a{i}", f"d{i}"); Q = m(f"a{i}", f"c{i}")
        for j in others[i]:
            if bits[k]: P |= G[j]
            k += 1
        for j in others[i]:
            if bits[k]: Q |= G[j]
            k += 1
        F += [P, Q]
    for (i, j, kk) in ((1, 2, 3), (2, 3, 1), (3, 1, 2)):
        R = m(f"a{i}", f"b{i}", f"c{i}") | m(f"a{j}", f"b{j}", f"d{j}")
        if bits[k]: R |= G[kk]
        k += 1
        F.append(R)
    if all_downsets_ok(F):
        sols.append((bits, F))
print("solutions:", len(sols))
if not sols:
    sys.exit(1)
bits, F = sols[0]
# all weight-0 arcs entering no shore, minus those parallel to a weight-1 arc
arcs = []
w = []
for t, h, lab in W1:
    arcs.append((idx[t], idx[h])); w.append(1)
w1set = {(idx[t], idx[h]) for t, h, _ in W1}
zero = []
for x in V:
    for y in V:
        if x != y and (idx[x], idx[y]) not in w1set and all(not ((S >> idx[y]) & 1 and not (S >> idx[x]) & 1) for S in F):
            zero.append((idx[x], idx[y]))
# transitive reduction of the zero arcs (they are a preorder; keep it readable)
import itertools
reach = {(x, y) for x, y in zero}
red = [(x, y) for x, y in zero if not any((x, z) in reach and (z, y) in reach for z in range(12) if z not in (x, y))]
for x, y in red:
    arcs.append((x, y)); w.append(0)
out = {"vertices": V, "arcs": [(V[t], V[h]) for t, h in arcs], "w": w,
       "shores": [[v for v in V if (S >> idx[v]) & 1] for S in F], "bits": bits}
json.dump(out, open("constructed_counterexample.json", "w"), indent=1)
print(json.dumps(out["arcs"])); print(w)
