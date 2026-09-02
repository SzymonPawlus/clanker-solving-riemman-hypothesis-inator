"""Independent reimplementation of dicut / dijoin / tau machinery for Woodall's
conjecture red-team (issue #153).

Conventions (restated from the problem RULES.md, deliberately re-derived here
rather than copied from any existing script in the repo):

  D = (V, A), A a MULTISET of ordered pairs (arcs), given as a list; arcs are
  identified by their INDEX in that list, so parallel arcs are distinct.

  For U a subset of V:
     delta_plus(U)  = arcs with tail in U, head not in U
     delta_minus(U) = arcs with tail not in U, head in U
  U is a *dicut shore* iff  U is nonempty, U != V, delta_minus(U) is empty,
  and delta_plus(U) is nonempty.  The dicut is then delta_plus(U).

  A dijoin is an arc set meeting every dicut.
  tau(D) = min size of a dicut (infinity if there are no dicuts).

  Weighted (Edmonds-Giles, 0/1 form): S subset of A are the weight-one arcs.
  tau_w = min over dicuts C of |C cap S|.  A w-packing of k dijoins is k
  pairwise DISJOINT dijoins each contained in S.
"""
from itertools import combinations, product


def delta_plus(n, arcs, U):
    return [i for i, (u, v) in enumerate(arcs) if (u in U) and (v not in U)]


def delta_minus(n, arcs, U):
    return [i for i, (u, v) in enumerate(arcs) if (u not in U) and (v in U)]


def dicuts(n, arcs, allow_empty=False):
    """All dicuts, as frozensets of arc indices.  Enumerates every U."""
    out = []
    for mask in range(1, (1 << n) - 1):          # nonempty proper subsets
        U = {i for i in range(n) if mask >> i & 1}
        if delta_minus(n, arcs, U):
            continue
        C = delta_plus(n, arcs, U)
        if C or allow_empty:
            out.append(frozenset(C))
    return out


def dicut_shores(n, arcs):
    out = []
    for mask in range(1, (1 << n) - 1):
        U = {i for i in range(n) if mask >> i & 1}
        if delta_minus(n, arcs, U):
            continue
        C = delta_plus(n, arcs, U)
        if C:
            out.append((frozenset(U), frozenset(C)))
    return out


def tau(n, arcs):
    cs = dicuts(n, arcs)
    return min((len(c) for c in cs), default=float('inf'))


def tau_w(n, arcs, S):
    """Minimum weighted dicut value for 0/1 weights with support S."""
    cs = dicuts(n, arcs)
    return min((len(c & S) for c in cs), default=float('inf'))


def is_dijoin(n, arcs, J, cs=None):
    if cs is None:
        cs = dicuts(n, arcs)
    J = set(J)
    return all(J & set(c) for c in cs)


def two_disjoint_dijoins(n, arcs, S=None):
    """EXACT decision, by brute force over all 2-colourings of S.

    Returns (J1, J2) with J1, J2 disjoint dijoins contained in S, or None.
    Since a superset of a dijoin is a dijoin, we may WLOG look only at
    partitions of S into two parts (any two disjoint dijoins inside S can be
    grown to a partition of S)."""
    if S is None:
        S = set(range(len(arcs)))
    S = sorted(S)
    cs = [set(c) for c in dicuts(n, arcs)]
    if not cs:
        return (set(S), set())          # no dicuts: everything is a dijoin
    m = len(S)
    for mask in range(1 << m):
        J1 = {S[i] for i in range(m) if mask >> i & 1}
        J2 = set(S) - J1
        if all(c & J1 for c in cs) and all(c & J2 for c in cs):
            return (J1, J2)
    return None


def k_disjoint_dijoins(n, arcs, k, S=None):
    """Exact decision for k pairwise disjoint dijoins inside S, brute force
    over all assignments of S to {0..k-1} (one colour class per dijoin)."""
    if S is None:
        S = set(range(len(arcs)))
    S = sorted(S)
    cs = [set(c) for c in dicuts(n, arcs)]
    if not cs:
        return [set(S)] + [set() for _ in range(k - 1)]
    for assign in product(range(k), repeat=len(S)):
        parts = [set() for _ in range(k)]
        for a, col in zip(S, assign):
            parts[col].add(a)
        if all(all(c & p for c in cs) for p in parts):
            return parts
    return None
