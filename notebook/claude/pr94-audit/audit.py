#!/usr/bin/env python3
"""Independent audit of PR #94 (exact ID1009 ACZ realization), head 01dbc1c.

Written from the definitions in problems/woodalls-conjecture/RULES.md and
experiments/woodalls-rho4/README.md, not from the author's verify.py.  Uses an
explicit arc multiset with set/dict structures and itertools enumeration; the
author's file uses bitmasks and closed-form counts, so the two agree only if
the mathematics does.  Nothing here imports experiments/woodalls-rho4/.

Run:  python notebook/claude/pr94-audit/audit.py
"""

from itertools import combinations, permutations

# Certificate, retyped by hand from certificate.json.
SUPPORTS = [
    "018", "018", "08B", "08B", "119", "22B", "236", "245",
    "33B", "357", "44A", "467", "559", "66A", "779", "9AA",
]
TARGET = {
    "0234", "1234", "0245", "1245", "0345", "1345", "0236", "1236",
    "0346", "1346", "0256", "1256", "0356", "1356", "0456", "1456",
    "0237", "1237", "0247", "1247", "0347", "1347", "0257", "1257",
    "0357", "1357", "0267", "1267", "0467", "1467", "0567", "1567",
}

DIGITS = "0123456789AB"
SOURCES = range(12)
SINKS = range(16)
show = lambda S: "".join(DIGITS[v] for v in sorted(S))

ARCS = [(DIGITS.index(ch), t) for t, sup in enumerate(SUPPORTS) for ch in sup]
IN = {t: {a for a, b in ARCS if b == t} for t in SINKS}       # sink support

# 1. instance shape
src_deg = [sum(1 for a, _ in ARCS if a == s) for s in SOURCES]
snk_deg = [sum(1 for _, b in ARCS if b == t) for t in SINKS]
assert len(ARCS) == 48 and src_deg == [4] * 12 and snk_deg == [3] * 16
print("48 arcs; source degrees all 4; sink degrees all 3; rho =", 16 - 12)

# 2. tau, at definition level: every U with delta^-(U) empty.  A sink lies in U
# only if its whole support does, and sources have in-degree 0, so U = X + S
# with S a subset of T(X) = {t : IN[t] <= X}; the outgoing count 4|X| - 3|S| is
# minimised at S = T(X), except that U must stay proper.
best, argmin = None, []
for k in range(13):
    for X in combinations(SOURCES, k):
        Xs = set(X)
        T = [t for t in SINKS if IN[t] <= Xs]
        if not (Xs or T) or (len(Xs) == 12 and len(T) == 16):
            continue                                  # nonempty and proper
        out = sum(1 for a, b in ARCS if a in Xs and b not in T)
        if best is None or out < best:
            best, argmin = out, [show(Xs)]
        elif out == best:
            argmin.append(show(Xs))
assert best == 3
print("tau = 3; maximal minimising shores:", argmin)
# The all-source family (X = 12 sources, 15 of 16 sinks) also gives 4*12-3*15 = 3;
# it is excluded above only as the maximal choice, and does not change tau.

# 3. M1 bases.  Q is a basis iff |Q| = 4 and, for every nonempty proper source
# set X, |Q ∩ X| >= 1 + |Y(X)| - |X| where Y(X) = {t : IN[t] <= X}.
Y = {}
for k in range(1, 12):
    for X in combinations(SOURCES, k):
        Xs = frozenset(X)
        Y[Xs] = sum(1 for t in SINKS if IN[t] <= Xs)
assert len(Y) == 4094
assert not [1 for Xs, y in Y.items()                 # necessary bound a >= 3r
            if 1 + y - len(Xs) > 0 and len(Xs) < 3 * (1 + y - len(Xs))]

is_basis = lambda Q: len(Q) == 4 and all(
    len(set(Q) & Xs) >= 1 + y - len(Xs) for Xs, y in Y.items())

full = {frozenset(Q) for Q in combinations(SOURCES, 4) if is_basis(Q)}
B32 = {B for B in full if B <= set(range(8))}
assert {show(B) for B in B32} == TARGET
print("M1 bases: %d on all 12 active sources, %d inside {0..7}, = target_bases"
      % (len(full), len(B32)))

# 4. the restriction is a genuine rank-4 matroid
assert not [1 for A in B32 for C in B32 for x in A - C
            if not any((A - {x}) | {z} in B32 for z in C - A)]
rank = lambda S: max(len(S & B) for B in B32)
subsets = [frozenset(c) for k in range(9) for c in combinations(range(8), k)]
assert rank(frozenset(range(8))) == 4
assert all(rank(A | C) + rank(A & C) <= rank(A) + rank(C)
           for A in subsets for C in subsets)
print("basis exchange holds; rank 4; rank function submodular on all 256 subsets")

# 5. strong base orderability, from the definition
def sbo_pair(B, C, bases):
    common, bs, cs = B & C, sorted(B - C), sorted(C - B)
    for perm in permutations(cs):
        phi = dict(zip(bs, perm)) | {x: x for x in common}
        if all(((B - set(A)) | {phi[a] for a in A}) in bases
               and ((C - {phi[a] for a in A}) | set(A)) in bases
               for k in range(len(bs) + 1) for A in combinations(bs, k)):
            return True
    return False

fails = [(B, C) for B, C in combinations(sorted(B32, key=sorted), 2)
         if not sbo_pair(B, C, B32)]
print("base pairs with no strong ordering: %d of %d -> NOT strongly base orderable"
      % (len(fails), len(B32) * (len(B32) - 1) // 2))

B, C = frozenset({0, 2, 3, 7}), frozenset({0, 4, 5, 6})
edges = [(DIGITS[b], DIGITS[c]) for b in sorted(B - C) for c in sorted(C - B)
         if ((B - {b}) | {c}) in B32 and ((C - {c}) | {b}) in B32]
assert edges == [("2", "4"), ("3", "4"), ("3", "5"), ("3", "6"), ("7", "4")]
assert {c for b, c in edges if b in "27"} == {"4"}
print("ID1009 witness (0237, 0456): exchange edges", edges,
      "; Hall fails at {2,7} with N = {4}")

# 6. the ground is a real two-base restriction, and Question 8.1 still holds
parts = [(A, C_, D) for A, C_, D in combinations(sorted(full, key=sorted), 3)
         if A | C_ | D == set(SOURCES) and not (A & C_ or A & D or C_ & D)]
grounds = {frozenset(p[i] | p[j]) for p in parts for i, j in ((0, 1), (0, 2), (1, 2))}
sbo_ground = {g: all(sbo_pair(X, Z, {B_ for B_ in full if B_ <= g})
                     for X, Z in combinations(
                         sorted((B_ for B_ in full if B_ <= g), key=sorted), 2))
              for g in grounds}
ok = sum(any(sbo_ground[frozenset(p[i] | p[j])] for i, j in ((0, 1), (0, 2), (1, 2)))
         for p in parts)
assert frozenset(range(8)) in grounds and not sbo_ground[frozenset(range(8))]
print("partitions into three M1 bases: %d; distinct two-base grounds: %d (%d SBO)"
      % (len(parts), len(grounds), sum(sbo_ground.values())))
print("partitions satisfying ACZ Question 8.1: %d of %d" % (ok, len(parts)))
print("\nall checks passed")
