"""Independent Woodall toolkit for the census audit (issue #149).

Written from problems/woodalls-conjecture/README.md ALONE, before reading any
code of the A1 census (issue #148).  Pure Python 3, no third-party imports.

Definitions used (restated in my own words, per problem RULES.md section 4):

* A digraph is (n, arcs) with vertices 0..n-1 and `arcs` a LIST of (u, v)
  pairs.  The list index is the arc's identity, so parallel arcs are distinct
  arcs and are never collapsed.  Loops are allowed and lie in no dicut.
* For a nonempty proper vertex subset U:  delta_out(U) = arcs u->v with u in U,
  v not in U;  delta_in(U) = arcs with u not in U, v in U.
* A DICUT is delta_out(U) for a U with delta_in(U) EMPTY.  We insist on
  delta_in(U) = empty; delta_out(U) may itself be empty (that happens exactly
  when the digraph is weakly disconnected, and then no dijoin exists).
* A DIJOIN is an arc set that meets every dicut in at least one arc.
  Equivalently the contraction of the set is strongly connected; both are
  implemented and cross-checked.
* tau = min |dicut| over all dicuts.  tau is None (undefined / +infinity)
  when there is no dicut at all, i.e. the digraph is strongly connected.
* The conjecture's existence direction for an instance with tau = t >= 1:
  do t pairwise arc-disjoint dijoins exist?  Because any superset of a dijoin
  is a dijoin, this is the same as: can the arc set be partitioned into t
  dijoins.  We decide it exactly by exhaustive backtracking over arc colourings.
"""
from __future__ import annotations

import itertools
import random
import sys
from typing import Dict, FrozenSet, Iterable, List, Optional, Sequence, Tuple

Arc = Tuple[int, int]


# ----------------------------------------------------------------------------
# Dicuts
# ----------------------------------------------------------------------------

def all_dicuts(n: int, arcs: Sequence[Arc]) -> List[Tuple[int, FrozenSet[int]]]:
    """Every dicut as (U as bitmask, frozenset of arc indices in delta_out(U)).

    U ranges over all nonempty proper subsets of the vertex set (2^n - 2 masks).
    A subset U is reported iff no arc enters U.  Duplicated arc sets from
    different shores U are all reported (callers dedupe if they want).
    """
    out: List[Tuple[int, FrozenSet[int]]] = []
    full = (1 << n) - 1
    for U in range(1, full):
        entering = False
        leaving: List[int] = []
        for idx, (u, v) in enumerate(arcs):
            uin = (U >> u) & 1
            vin = (U >> v) & 1
            if vin and not uin:
                entering = True
                break
            if uin and not vin:
                leaving.append(idx)
        if not entering:
            out.append((U, frozenset(leaving)))
    return out


def distinct_dicut_sets(n: int, arcs: Sequence[Arc]) -> List[FrozenSet[int]]:
    return sorted({c for _, c in all_dicuts(n, arcs)}, key=lambda c: (len(c), sorted(c)))


def minimal_dicut_sets(n: int, arcs: Sequence[Arc]) -> List[FrozenSet[int]]:
    """Inclusion-minimal dicut arc sets.  Meeting all of these == meeting all dicuts."""
    sets = distinct_dicut_sets(n, arcs)
    minimal: List[FrozenSet[int]] = []
    for c in sets:  # sorted by size, so any strict subset was seen earlier
        if not any(m < c for m in minimal):
            minimal.append(c)
    return minimal


def tau(n: int, arcs: Sequence[Arc]) -> Optional[int]:
    """Minimum dicut size; None if there is no dicut (strongly connected)."""
    dc = all_dicuts(n, arcs)
    if not dc:
        return None
    return min(len(c) for _, c in dc)


def min_dicut_witness(n: int, arcs: Sequence[Arc]) -> Optional[Tuple[List[int], List[int]]]:
    dc = all_dicuts(n, arcs)
    if not dc:
        return None
    U, c = min(dc, key=lambda p: (len(p[1]), p[0]))
    return ([v for v in range(n) if (U >> v) & 1], sorted(c))


# ----------------------------------------------------------------------------
# Dijoin recognition, two ways
# ----------------------------------------------------------------------------

def is_dijoin_by_dicuts(n: int, arcs: Sequence[Arc], S: Iterable[int]) -> bool:
    S = set(S)
    return all(c & S for _, c in all_dicuts(n, arcs))


def _strongly_connected(n: int, arcs: Sequence[Arc]) -> bool:
    if n <= 1:
        return True
    fwd = [[] for _ in range(n)]
    bwd = [[] for _ in range(n)]
    for u, v in arcs:
        fwd[u].append(v)
        bwd[v].append(u)

    def reach(adj):
        seen = [False] * n
        seen[0] = True
        stack = [0]
        while stack:
            x = stack.pop()
            for y in adj[x]:
                if not seen[y]:
                    seen[y] = True
                    stack.append(y)
        return all(seen)

    return reach(fwd) and reach(bwd)


def is_dijoin_by_contraction(n: int, arcs: Sequence[Arc], S: Iterable[int]) -> bool:
    """Contract the arcs of S (union-find) and test strong connectivity."""
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for i in S:
        u, v = arcs[i]
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv
    roots = sorted({find(v) for v in range(n)})
    relabel = {r: i for i, r in enumerate(roots)}
    carcs = [(relabel[find(u)], relabel[find(v)]) for u, v in arcs]
    return _strongly_connected(len(roots), carcs)


def is_dijoin(n: int, arcs: Sequence[Arc], S: Iterable[int]) -> bool:
    S = list(S)
    a = is_dijoin_by_dicuts(n, arcs, S)
    b = is_dijoin_by_contraction(n, arcs, S)
    if a != b:
        raise AssertionError(f"dijoin definitions disagree on {S}: dicuts={a} contraction={b}")
    return a


# ----------------------------------------------------------------------------
# Exact decision: do k pairwise arc-disjoint dijoins exist?
# ----------------------------------------------------------------------------

def pack_dijoins(n: int, arcs: Sequence[Arc], k: int) -> Optional[List[List[int]]]:
    """Return k pairwise disjoint dijoins (as lists of arc indices) or None.

    Exhaustive: colours every arc with one of k colours (a partition; WLOG
    since supersets of dijoins are dijoins) such that every inclusion-minimal
    dicut contains every colour.  Backtracking with symmetry breaking
    (colour c+1 may only be introduced after colour c) and the pruning rule
    "missing colours in a dicut <= unassigned arcs in that dicut".
    """
    m = len(arcs)
    if k <= 0:
        return []
    cuts = minimal_dicut_sets(n, arcs)
    if any(len(c) < k for c in cuts):
        return None  # a dicut with < k arcs cannot contain k colours
    if not cuts:
        # strongly connected: every arc set (even the empty one) is a dijoin
        return [[] for _ in range(k)]
    # arc -> list of cuts containing it
    cut_lists = [sorted(c) for c in cuts]
    arc_cuts: List[List[int]] = [[] for _ in range(m)]
    for ci, c in enumerate(cut_lists):
        for a in c:
            arc_cuts[a].append(ci)
    # order arcs: arcs in the smallest cuts first, then by cut membership count
    order: List[int] = []
    seen = set()
    for c in sorted(cut_lists, key=len):
        for a in c:
            if a not in seen:
                seen.add(a)
                order.append(a)
    for a in range(m):
        if a not in seen:
            order.append(a)  # arcs in no dicut: colour freely
    colour = [-1] * m
    present = [[0] * k for _ in cuts]   # present[ci][col] = #arcs of cut ci with colour col
    ncol = [0] * len(cuts)               # number of distinct colours present in cut ci
    unassigned = [len(c) for c in cut_lists]

    sys.setrecursionlimit(10000)

    def feasible_cut(ci: int) -> bool:
        return (k - ncol[ci]) <= unassigned[ci]

    def rec(pos: int, maxcol: int) -> bool:
        if pos == m:
            return all(ncol[ci] == k for ci in range(len(cuts)))
        a = order[pos]
        top = min(k - 1, maxcol + 1)
        for col in range(top + 1):
            colour[a] = col
            ok = True
            for ci in arc_cuts[a]:
                unassigned[ci] -= 1
                if present[ci][col] == 0:
                    ncol[ci] += 1
                present[ci][col] += 1
            for ci in arc_cuts[a]:
                if not feasible_cut(ci):
                    ok = False
                    break
            if ok and rec(pos + 1, max(maxcol, col)):
                return True
            for ci in arc_cuts[a]:
                unassigned[ci] += 1
                present[ci][col] -= 1
                if present[ci][col] == 0:
                    ncol[ci] -= 1
            colour[a] = -1
        return False

    if rec(0, -1):
        classes = [[a for a in range(m) if colour[a] == c] for c in range(k)]
        return classes
    return None


def pack_dijoins_bruteforce(n: int, arcs: Sequence[Arc], k: int) -> bool:
    """Independent slow decision: try every colouring of the arcs with k colours
    and test each class with the (double-checked) dijoin test.  Only for tiny m."""
    m = len(arcs)
    if k <= 0:
        return True
    dc = [c for _, c in all_dicuts(n, arcs)]
    if not dc:
        return True
    for col in itertools.product(range(k), repeat=m):
        classes = [{a for a in range(m) if col[a] == c} for c in range(k)]
        if all(all(c & cl for c in dc) for cl in classes):
            # confirm via contraction as well
            assert all(is_dijoin_by_contraction(n, arcs, cl) for cl in classes)
            return True
    return False


def woodall_verdict(n: int, arcs: Sequence[Arc]) -> Tuple[Optional[int], Optional[bool]]:
    """(tau, verdict).  verdict True = tau disjoint dijoins exist.
    tau None (strongly connected) -> verdict None (vacuous).
    tau 0 (weakly disconnected) -> verdict True (zero dijoins trivially)."""
    t = tau(n, arcs)
    if t is None:
        return None, None
    if t == 0:
        return 0, True
    return t, pack_dijoins(n, arcs, t) is not None


# ----------------------------------------------------------------------------
# Condensation
# ----------------------------------------------------------------------------

def condensation(n: int, arcs: Sequence[Arc]) -> Tuple[int, List[Arc]]:
    """Contract strong components; keep every inter-component arc (parallel
    arcs are kept as distinct arcs, intra-component arcs dropped)."""
    fwd = [[] for _ in range(n)]
    for u, v in arcs:
        fwd[u].append(v)
    # reachability matrix (n small)
    reach = []
    for s in range(n):
        seen = [False] * n
        seen[s] = True
        st = [s]
        while st:
            x = st.pop()
            for y in fwd[x]:
                if not seen[y]:
                    seen[y] = True
                    st.append(y)
        reach.append(seen)
    comp = [-1] * n
    k = 0
    for v in range(n):
        if comp[v] == -1:
            for w in range(n):
                if reach[v][w] and reach[w][v]:
                    comp[w] = k
            k += 1
    carcs = [(comp[u], comp[v]) for u, v in arcs if comp[u] != comp[v]]
    return k, carcs


# ----------------------------------------------------------------------------
# Canonical forms and isomorph-free DAG enumeration
# ----------------------------------------------------------------------------

def _mult_matrix(n: int, arcs: Sequence[Arc]) -> List[List[int]]:
    M = [[0] * n for _ in range(n)]
    for u, v in arcs:
        M[u][v] += 1
    return M


def canonical_form(n: int, arcs: Sequence[Arc]) -> Tuple[int, ...]:
    """Canonical labelling of a multidigraph: colour refinement, then the
    lexicographically smallest multiplicity matrix over all relabellings that
    respect the refined ordered partition.  Two digraphs are isomorphic iff
    their canonical forms are equal (the refinement is isomorphism-invariant,
    so the set of candidate permutations is invariant and the minimum is a
    complete invariant)."""
    M = _mult_matrix(n, arcs)
    col = [(sum(M[v]), sum(M[u][v] for u in range(n)), M[v][v]) for v in range(n)]
    # iterate refinement
    while True:
        sig = []
        for v in range(n):
            outs = sorted((col[w], M[v][w]) for w in range(n) if M[v][w] and w != v)
            ins = sorted((col[u], M[u][v]) for u in range(n) if M[u][v] and u != v)
            sig.append((col[v], tuple(outs), tuple(ins)))
        keys = sorted(set(sig))
        newcol = [keys.index(s) for s in sig]
        if len(set(newcol)) == len(set(col)):
            col = newcol
            break
        col = newcol
    cells: Dict[int, List[int]] = {}
    for v in range(n):
        cells.setdefault(col[v], []).append(v)
    ordered_cells = [cells[c] for c in sorted(cells)]
    best = None
    for perms in itertools.product(*[itertools.permutations(c) for c in ordered_cells]):
        old_of_new = [v for p in perms for v in p]
        key = tuple(M[old_of_new[i]][old_of_new[j]] for i in range(n) for j in range(n))
        if best is None or key < best:
            best = key
    return best  # type: ignore[return-value]


def arcs_from_matrix_key(n: int, key: Sequence[int]) -> List[Arc]:
    arcs = []
    for i in range(n):
        for j in range(n):
            arcs.extend([(i, j)] * key[i * n + j])
    return arcs


def all_simple_dags_upto_iso(nmax: int) -> Dict[int, List[Tuple[int, ...]]]:
    """Isomorph-free simple DAGs on 0..nmax vertices by sink extension:
    every DAG on n>=1 vertices is a DAG on n-1 vertices plus one new sink
    joined from an arbitrary subset of the old vertices.  Canonical forms
    dedupe.  Returns {n: [canonical keys]}."""
    result: Dict[int, List[Tuple[int, ...]]] = {0: [()]}
    for n in range(1, nmax + 1):
        seen = set()
        for key in result[n - 1]:
            base = arcs_from_matrix_key(n - 1, key)
            for mask in range(1 << (n - 1)):
                arcs = base + [(u, n - 1) for u in range(n - 1) if (mask >> u) & 1]
                seen.add(canonical_form(n, arcs))
        result[n] = sorted(seen)
    return result


# ----------------------------------------------------------------------------
# Small helpers
# ----------------------------------------------------------------------------

def sources_sinks(n: int, arcs: Sequence[Arc]):
    indeg = [0] * n
    outdeg = [0] * n
    for u, v in arcs:
        outdeg[u] += 1
        indeg[v] += 1
    return [v for v in range(n) if indeg[v] == 0], [v for v in range(n) if outdeg[v] == 0]


def is_acyclic(n: int, arcs: Sequence[Arc]) -> bool:
    k, _ = condensation(n, arcs)
    return k == n and all(u != v for u, v in arcs)


def source_sink_connected_dag(n: int, arcs: Sequence[Arc]) -> bool:
    fwd = [[] for _ in range(n)]
    for u, v in arcs:
        fwd[u].append(v)
    src, snk = sources_sinks(n, arcs)
    for s in src:
        seen = [False] * n
        seen[s] = True
        st = [s]
        while st:
            x = st.pop()
            for y in fwd[x]:
                if not seen[y]:
                    seen[y] = True
                    st.append(y)
        if not all(seen[t] for t in snk):
            return False
    return True


def weakly_connected(n: int, arcs: Sequence[Arc]) -> bool:
    if n == 0:
        return True
    adj = [[] for _ in range(n)]
    for u, v in arcs:
        adj[u].append(v)
        adj[v].append(u)
    seen = [False] * n
    seen[0] = True
    st = [0]
    while st:
        x = st.pop()
        for y in adj[x]:
            if not seen[y]:
                seen[y] = True
                st.append(y)
    return all(seen)


def parse_arcs(s: str) -> List[Arc]:
    """'0-1,1-2' or '0>1 1>2'."""
    out = []
    for tok in s.replace(",", " ").split():
        tok = tok.replace(">", "-")
        a, b = tok.split("-")
        out.append((int(a), int(b)))
    return out


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        n = int(sys.argv[1])
        arcs = parse_arcs(sys.argv[2])
        t, verdict = woodall_verdict(n, arcs)
        print("tau", t, "verdict", verdict, "min dicut", min_dicut_witness(n, arcs))
        if t:
            print("packing", pack_dijoins(n, arcs, t))
