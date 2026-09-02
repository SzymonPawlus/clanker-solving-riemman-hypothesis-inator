"""Prose model of Woodall's-conjecture basics, written from
``problems/woodalls-conjecture/README.md`` alone (issue #151, step 1).

Written BEFORE reading any Lean from issue #150 and without reading the other Python
checkers in ``experiments/woodall*``, so that it is an independent oracle.

Conventions (restated in my own words, as the problem RULES.md §4 demands):

* A digraph is ``(n, arcs)``: vertices ``0..n-1`` and ``arcs`` a *list* of ordered pairs
  ``(u, v)``.  Arcs are identified by their **index** in the list, so parallel arcs are
  distinct objects and loops are permitted (they never cross any cut).
* For ``U`` a **nonempty proper** subset of ``V``: ``delta_plus(U)`` = indices of arcs with
  tail in ``U`` and head outside; ``delta_minus(U)`` = indices with head in ``U`` and tail
  outside.
* A **dicut** is ``delta_plus(U)`` for some nonempty proper ``U`` with ``delta_minus(U)``
  empty.  README.md does not say whether ``delta_plus(U)`` itself must be nonempty; the
  literal reading admits the empty arc set as a dicut whenever the underlying graph is
  disconnected.  Both readings are exposed (``allow_empty``), and the sweep records where
  they differ.  The literature (Feofiloff's survey) takes dicuts to be nonempty; the README
  text does not.
* A **dijoin** is a set of arc indices meeting every dicut.  (With no dicuts at all, every
  arc set — including the empty one — is a dijoin.)
* ``tau`` is the minimum size of a dicut, ``None`` if there is no dicut.
* Woodall: the arc set can be partitioned into ``tau`` pairwise disjoint dijoins.  Since a
  superset of a dijoin is a dijoin, this is the same as: ``tau`` pairwise arc-disjoint
  dijoins exist.  The easy direction: no family of pairwise arc-disjoint dijoins has more
  than ``tau`` members (when a dicut exists).
"""

from __future__ import annotations

from itertools import combinations
from typing import FrozenSet, Iterable, List, Optional, Set, Tuple

Arc = Tuple[int, int]
Digraph = Tuple[int, List[Arc]]
ArcSet = FrozenSet[int]


def vertex_subsets(n: int, proper_nonempty: bool = True) -> Iterable[FrozenSet[int]]:
    """All subsets of ``range(n)``; by default only the nonempty proper ones."""
    lo, hi = (1, (1 << n) - 1) if proper_nonempty else (0, 1 << n)
    for mask in range(lo, hi):
        yield frozenset(i for i in range(n) if mask >> i & 1)


def delta_plus(arcs: List[Arc], U: FrozenSet[int]) -> ArcSet:
    return frozenset(i for i, (u, v) in enumerate(arcs) if u in U and v not in U)


def delta_minus(arcs: List[Arc], U: FrozenSet[int]) -> ArcSet:
    return frozenset(i for i, (u, v) in enumerate(arcs) if u not in U and v in U)


def dicut_shores(D: Digraph, allow_empty: bool = False) -> List[Tuple[FrozenSet[int], ArcSet]]:
    """All ``(U, delta_plus(U))`` with ``U`` nonempty proper and ``delta_minus(U)`` empty.

    ``allow_empty=False`` additionally requires ``delta_plus(U)`` nonempty (survey reading).
    """
    n, arcs = D
    out = []
    for U in vertex_subsets(n):
        if delta_minus(arcs, U):
            continue
        C = delta_plus(arcs, U)
        if C or allow_empty:
            out.append((U, C))
    return out


def dicuts(D: Digraph, allow_empty: bool = False) -> Set[ArcSet]:
    return {C for _, C in dicut_shores(D, allow_empty)}


def is_dijoin(D: Digraph, S: ArcSet, allow_empty: bool = False) -> bool:
    return all(S & C for C in dicuts(D, allow_empty))


def dijoins(D: Digraph, allow_empty: bool = False) -> Set[ArcSet]:
    n, arcs = D
    m = len(arcs)
    cuts = dicuts(D, allow_empty)
    out = set()
    for mask in range(1 << m):
        S = frozenset(i for i in range(m) if mask >> i & 1)
        if all(S & C for C in cuts):
            out.add(S)
    return out


def tau(D: Digraph, allow_empty: bool = False) -> Optional[int]:
    cuts = dicuts(D, allow_empty)
    return min((len(C) for C in cuts), key=int) if cuts else None


def min_dicut(D: Digraph, allow_empty: bool = False) -> Optional[ArcSet]:
    cuts = dicuts(D, allow_empty)
    return min(cuts, key=lambda C: (len(C), sorted(C))) if cuts else None


def max_disjoint_dijoins(D: Digraph, allow_empty: bool = False) -> Optional[int]:
    """Largest ``k`` for which ``k`` pairwise arc-disjoint dijoins exist.

    ``None`` when there is no dicut: then every arc set is a dijoin and the empty set may
    be repeated, so the maximum is unbounded / meaningless — matching ``tau is None``.
    Exhaustive: enumerates the minimal dijoins and packs them.
    """
    cuts = dicuts(D, allow_empty)
    if not cuts:
        return None
    if frozenset() in cuts:
        return 0  # nothing meets the empty dicut: no dijoin exists at all
    J = dijoins(D, allow_empty)
    minimal = [S for S in J if not any(T < S for T in J)]
    best = 0

    def grow(chosen: List[ArcSet], used: ArcSet, start: int) -> None:
        nonlocal best
        best = max(best, len(chosen))
        for i in range(start, len(minimal)):
            S = minimal[i]
            if not (S & used):
                grow(chosen + [S], used | S, i + 1)

    grow([], frozenset(), 0)
    return best


def has_tau_disjoint_dijoins(D: Digraph, allow_empty: bool = False) -> Optional[bool]:
    t = tau(D, allow_empty)
    if t is None:
        return None
    return max_disjoint_dijoins(D, allow_empty) >= t


def easy_direction_holds(D: Digraph, allow_empty: bool = False) -> bool:
    """Every pairwise-disjoint family of dijoins has size <= tau (vacuous if no dicut)."""
    t = tau(D, allow_empty)
    if t is None:
        return True
    return max_disjoint_dijoins(D, allow_empty) <= t


# ----------------------------------------------------------------------------------
# Exhaustive small-digraph generator.
# ----------------------------------------------------------------------------------

def all_digraphs(max_n: int = 4, max_arcs: int = 6, max_mult: int = 2,
                 loops: bool = False) -> Iterable[Digraph]:
    """Every labelled digraph with ``1 <= n <= max_n`` vertices and at most ``max_arcs``
    arcs, each ordered pair used with multiplicity ``0..max_mult`` (so parallel arcs are
    present), optionally with loops.  Includes the arcless digraphs, disconnected ones, and
    strongly connected ones (which have no dicut).

    The arc list is emitted in a canonical order (sorted pairs, repeats adjacent), so arc
    indices are deterministic.
    """
    for n in range(1, max_n + 1):
        pairs = [(u, v) for u in range(n) for v in range(n) if loops or u != v]
        # Distribute up to max_arcs arcs over the pairs with bounded multiplicity: choose a
        # multiset of pair-indices.
        for m in range(0, max_arcs + 1):
            for combo in combinations(range(len(pairs) * max_mult), m):
                # combo picks "slots"; slot s corresponds to pair s // max_mult, copy s % max_mult.
                # Require copies to be used in order so that each multiset is emitted once.
                ok = True
                used = {}
                for s in combo:
                    p, c = divmod(s, max_mult)
                    if c != used.get(p, 0):
                        ok = False
                        break
                    used[p] = c + 1
                if not ok:
                    continue
                arcs = []
                for p in sorted(used):
                    arcs.extend([pairs[p]] * used[p])
                yield (n, arcs)


FIXTURES = {
    "path3": (3, [(0, 1), (1, 2)]),
    "cycle3": (3, [(0, 1), (1, 2), (2, 0)]),
    "diamond": (4, [(0, 1), (0, 2), (1, 3), (2, 3)]),          # s=0, x=1, y=2, t=3
    "near_miss": (4, [(0, 2), (1, 2), (1, 3)]),                 # s1=0, s2=1, t1=2, t2=3
    "single_arc": (2, [(0, 1)]),
    "parallel_pair": (2, [(0, 1), (0, 1)]),
    "two_isolated": (2, []),
    "one_vertex": (1, []),
    "loop_only": (1, [(0, 0)]),
    "two_components": (4, [(0, 1), (2, 3)]),
}
