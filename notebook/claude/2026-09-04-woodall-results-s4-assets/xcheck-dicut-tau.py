"""Independent reimplementation of dicut / dijoin / tau, written from
problems/woodalls-conjecture/README.md, NOT from the Lean source.

Conventions (README "Definitions" + "Convention: dicuts are nonempty"):
  U ranges over ALL subsets of V (we let the delta+ != empty condition
  rule out the degenerate U = {} and U = V rather than pre-filtering).
  U is a DICUT SHORE iff  delta^-(U) = {}  and  delta^+(U) != {}.
  A DIJOIN is an arc set meeting every dicut delta^+(U) at least once.
  tau = min |delta^+(U)| over dicut shores; undefined if there is none.
Arcs are an INDEXED family: arcs[i] is arc i, so parallel arcs stay distinct.
"""
from itertools import combinations


def delta_out(arcs, U):
    return frozenset(i for i, (t, h) in enumerate(arcs) if t in U and h not in U)


def delta_in(arcs, U):
    return frozenset(i for i, (t, h) in enumerate(arcs) if t not in U and h in U)


def all_subsets(n):
    for mask in range(1 << n):
        yield frozenset(v for v in range(n) if mask >> v & 1)


def dicut_shores(n, arcs):
    return [U for U in all_subsets(n)
            if not delta_in(arcs, U) and delta_out(arcs, U)]


def permissive_shores(n, arcs):
    """The rejected convention: nonempty proper, delta^- empty, delta^+ MAY be empty."""
    return [U for U in all_subsets(n)
            if U and len(U) < n and not delta_in(arcs, U)]


def tau(n, arcs):
    sizes = [len(delta_out(arcs, U)) for U in dicut_shores(n, arcs)]
    return min(sizes) if sizes else None


def is_dijoin(n, arcs, J):
    return all(delta_out(arcs, U) & J for U in dicut_shores(n, arcs))


INSTANCES = {
    "cycle3":  (3, [(0, 1), (1, 2), (2, 0)]),
    "path3":   (3, [(0, 1), (1, 2)]),
    "diamond": (4, [(0, 1), (0, 2), (1, 3), (2, 3)]),
    "nearMiss": (4, [(0, 1), (2, 1), (2, 3)]),
    "twoArcs": (4, [(0, 1), (2, 3)]),
}

fails = []


def check(label, got, want):
    ok = got == want
    print(f"  {'OK ' if ok else 'FAIL'}  {label}: got {got!r}, want {want!r}")
    if not ok:
        fails.append(label)


for name, (n, arcs) in INSTANCES.items():
    print(f"\n=== {name}  n={n} arcs={arcs} ===")
    shores = sorted(dicut_shores(n, arcs), key=lambda s: (len(s), sorted(s)))
    print(f"  dicut shores: {[sorted(U) for U in shores]}")
    print(f"  tau = {tau(n, arcs)}")

# --- cycle3: no dicut at all (cycle3_no_dicut, cycle3_tau) ---
print("\n--- row checks ---")
n, arcs = INSTANCES["cycle3"]
check("cycle3_no_dicut: no dicut shore", dicut_shores(n, arcs), [])
check("cycle3_tau: tau undefined", tau(n, arcs), None)
# cycle3_empty_isDijoin states ONLY the empty arc set. The prose claims EVERY arc set.
check("cycle3: empty arc set is a dijoin", is_dijoin(n, arcs, frozenset()), True)
check("cycle3: EVERY arc set is a dijoin (the prose claim)",
      all(is_dijoin(n, arcs, frozenset(S))
          for r in range(len(arcs) + 1) for S in combinations(range(len(arcs)), r)), True)
# cycle3_trap: {0} has delta+ nonempty but is NOT a dicut shore
U = frozenset({0})
check("cycle3_trap: delta+({0}) nonempty", bool(delta_out(arcs, U)), True)
check("cycle3_trap: {0} not a dicut shore", U in dicut_shores(n, arcs), False)

# --- path3 ---
n, arcs = INSTANCES["path3"]
check("path3_dicutShores: exactly {0} and {0,1}",
      sorted(sorted(U) for U in dicut_shores(n, arcs)), [[0], [0, 1]])
check("path3_tau = 1", tau(n, arcs), 1)

# --- diamond ---
n, arcs = INSTANCES["diamond"]
check("diamond_tau = 2", tau(n, arcs), 2)
J1, J2 = frozenset({0, 2}), frozenset({1, 3})   # arcSetOf [0,2] and [1,3]
check("diamondJ1 is a dijoin", is_dijoin(n, arcs, J1), True)
check("diamondJ2 is a dijoin", is_dijoin(n, arcs, J2), True)
check("diamond_disjoint", bool(J1 & J2), False)
check("diamond_partition (J1 u J2 = A, exactly one each)",
      J1 | J2 == set(range(len(arcs))) and not (J1 & J2), True)

# --- nearMiss ---
n, arcs = INSTANCES["nearMiss"]
check("nearMiss_tau = 1", tau(n, arcs), 1)
check("nearMiss_shore: {0} is a dicut shore", frozenset({0}) in dicut_shores(n, arcs), True)
check("nearMiss_all_isDijoin", is_dijoin(n, arcs, frozenset(range(len(arcs)))), True)
check("nearMiss_two_sources: 0 and 2 have in-degree 0",
      all(h not in (0, 2) for (_, h) in arcs), True)

# --- twoArcs: the two conventions disagree ---
n, arcs = INSTANCES["twoArcs"]
U = frozenset({0, 1})
check("twoArcs: {0,1} IS a permissive shore", U in permissive_shores(n, arcs), True)
check("twoArcs: {0,1} is NOT a strict dicut shore", U in dicut_shores(n, arcs), False)
check("twoArcs_tau = 1 (strict convention)", tau(n, arcs), 1)

# --- global: tau=0 never occurs under the strict convention, small sweep ---
bad = []
for nn in range(1, 5):
    for mm in range(0, 4):
        for arcs2 in __import__("itertools").product(
                [(a, b) for a in range(nn) for b in range(nn)], repeat=mm):
            t = tau(nn, list(arcs2))
            if t == 0:
                bad.append((nn, arcs2))
check("not_isMinDicutSize_zero: no tau=0 over all digraphs n<=4, m<=3", bad, [])

print("\n" + ("ALL CHECKS PASSED" if not fails else f"FAILURES: {fails}"))
