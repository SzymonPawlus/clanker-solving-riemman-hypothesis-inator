"""Literal Python model of ``lean/Verified/Woodall/Basic.lean`` as it exists on branch
``claude/76-lean-woodall`` @ 561af29 (PR #79, closed unmerged).  This is the pre-existing
source; B1's issue-#150 module is modelled separately in ``lean_model.py`` once it exists.

Every function here transcribes ONE Lean definition, deliberately literally, including
anything that looks wrong.  Comments cite the Lean line.

    structure FinDigraph (V) where arcs : Finset (V × V)          -- SET of pairs: parallel arcs collapse
    out D S  = D.arcs.filter (a.1 ∈ S ∧ a.2 ∉ S)
    inn D S  = D.arcs.filter (a.1 ∉ S ∧ a.2 ∈ S)
    IsDicutSide D S = S ≠ ∅ ∧ S ≠ univ ∧ D.inn S = ∅
    IsDicut D C     = ∃ S, IsDicutSide D S ∧ C = D.out S          -- C may be ∅
    IsDijoin D J    = J ⊆ D.arcs ∧ ∀ C, IsDicut D C → (J ∩ C).Nonempty
    HasPacking D k  = ∃ J : Fin k → Finset (V×V), (∀ i, IsDijoin (J i)) ∧ ∀ i j, i ≠ j → Disjoint (J i) (J j)
    IsMinDicut D C  = IsDicut D C ∧ ∀ C', IsDicut D C' → C.card ≤ C'.card
    WoodallConjecture D = ∀ C, IsMinDicut D C → HasPacking D C.card
    card_le_of_hasPacking : HasPacking D k → IsDicut D C → k ≤ C.card
"""
from __future__ import annotations

from typing import FrozenSet, Optional, Set, Tuple

import prose_model as P

Pair = Tuple[int, int]


def arcs_finset(D: P.Digraph) -> FrozenSet[Pair]:
    """``D.arcs : Finset (V × V)`` — the Lean digraph built from a prose arc list."""
    return frozenset(D[1])


def out(D, S: FrozenSet[int]) -> FrozenSet[Pair]:
    return frozenset(a for a in arcs_finset(D) if a[0] in S and a[1] not in S)


def inn(D, S: FrozenSet[int]) -> FrozenSet[Pair]:
    return frozenset(a for a in arcs_finset(D) if a[0] not in S and a[1] in S)


def is_dicut_side(D, S: FrozenSet[int]) -> bool:
    n = D[0]
    return len(S) != 0 and len(S) != n and not inn(D, S)


def dicuts(D) -> Set[FrozenSet[Pair]]:
    n = D[0]
    return {out(D, S) for S in P.vertex_subsets(n, proper_nonempty=False) if is_dicut_side(D, S)}


def is_dijoin(D, J: FrozenSet[Pair]) -> bool:
    return J <= arcs_finset(D) and all(J & C for C in dicuts(D))


def tau(D) -> Optional[int]:
    """Not a Lean definition; the card of any ``IsMinDicut`` witness, or None if no dicut."""
    cs = dicuts(D)
    return min(len(C) for C in cs) if cs else None


def max_packing(D) -> Optional[int]:
    """Largest k with ``HasPacking D k``.  Unbounded (None) when no dicut exists, because then
    ``J i = ∅`` is a dijoin and the constant-∅ family is pairwise disjoint for every k."""
    cs = dicuts(D)
    if not cs:
        return None
    if frozenset() in cs:
        return 0
    A = sorted(arcs_finset(D))
    m = len(A)
    js = [frozenset(A[i] for i in range(m) if mask >> i & 1)
          for mask in range(1 << m)]
    js = [J for J in js if is_dijoin(D, J)]
    minimal = [S for S in js if not any(T < S for T in js)]
    best = 0

    def grow(k, used, start):
        nonlocal best
        best = max(best, k)
        for i in range(start, len(minimal)):
            if not (minimal[i] & used):
                grow(k + 1, used | minimal[i], i + 1)

    grow(0, frozenset(), 0)
    return best


# --- Bridges from prose objects (arc indices) to Lean objects (pairs) -------------------

def prose_dicuts_as_pairs(D, allow_empty):
    return {frozenset(D[1][i] for i in C) for C in P.dicuts(D, allow_empty)}


COMPARISONS = [
    # name, prose side, lean side.  Prose uses the literal-README reading (allow_empty=True)
    # because the Lean docstring explicitly chooses that convention; the survey reading is
    # reported separately.
    ("dicuts_as_pair_sets(literal)", lambda D: prose_dicuts_as_pairs(D, True), dicuts),
    ("dicuts_as_pair_sets(survey)", lambda D: prose_dicuts_as_pairs(D, False), dicuts),
    ("tau(literal)", lambda D: P.tau(D, True), tau),
    ("tau(survey)", lambda D: P.tau(D, False), tau),
    ("max_disjoint_dijoins(literal)", lambda D: P.max_disjoint_dijoins(D, True), max_packing),
]
