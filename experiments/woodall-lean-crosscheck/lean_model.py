"""Literal Python model of B1's Lean (issue #150, branch ``claude/150-lean-foundations`` @
ad78d86: ``lean/Verified/Woodall/Basic.lean`` and ``Instances.lean``).

Each function transcribes ONE Lean definition as literally as possible, with the Lean quoted.
Nothing here is derived from the prose model; the only shared code is the digraph generator
and the index<->pair plumbing.  The Lean is indexed-arc (``tail, head : Fin m → Fin n``) so
arc *indices* are the natural currency on both sides.

    VertexSet n := Fin n → Bool           -- ALL subsets, including ∅ and univ
    deltaOut D U a := U (tail a) && !U (head a)
    deltaIn  D U a := !U (tail a) && U (head a)
    IsDicutShore D U := (∀ a, deltaIn D U a = false) ∧ (∃ a, deltaOut D U a = true)
    Meets S J := ∃ a, S a = true ∧ J a = true
    IsDijoin D J := ∀ U, IsDicutShore D U → Meets (deltaOut D U) J
    ArcDisjoint J K := ∀ a, ¬(J a = true ∧ K a = true)
    card S := (allArcs m).countP S
    IsMinDicutSize D t := (∃ U, IsDicutShore D U ∧ card (deltaOut D U) = t)
                        ∧ (∀ U, IsDicutShore D U → t ≤ card (deltaOut D U))
    dicutShores D := (allVertexSets n).filter (decide ∘ IsDicutShore D)
    dicutSizes D := (dicutShores D).map (card ∘ deltaOut D)
    tau? D := (dicutSizes D).min?
    length_le_card_deltaOut : (∀ J ∈ Js, IsDijoin D J) → Js.Pairwise ArcDisjoint
                              → IsDicutShore D U → Js.length ≤ card (deltaOut D U)
    length_le_tau : IsMinDicutSize D t → (∀ J ∈ Js, IsDijoin D J) → Js.Pairwise ArcDisjoint
                    → Js.length ≤ t
    IsArcPartition Js := ∀ a, (Js.countP fun J => J a) = 1
    WoodallConjecture D := ∀ t, IsMinDicutSize D t →
        ∃ Js, Js.length = t ∧ (∀ J ∈ Js, IsDijoin D J) ∧ IsArcPartition Js
    IsDicutShoreAllowingEmpty D U := (∃ v, U v) ∧ (∃ v, ¬U v) ∧ (∀ a, deltaIn D U a = false)
"""
from __future__ import annotations

from itertools import product
from typing import FrozenSet, List, Optional, Set

import prose_model as P

Digraph = P.Digraph
ArcSet = FrozenSet[int]      # the set {a | J a = true}
VertexSet = FrozenSet[int]   # the set {v | U v = true}


def all_vertex_sets(n: int) -> List[VertexSet]:
    """``allVertexSets n`` — every ``Fin n → Bool``, i.e. every subset incl. ∅ and univ."""
    return [frozenset(i for i in range(n) if bits[i]) for bits in product((False, True), repeat=n)]


def tail(D: Digraph, a: int) -> int:
    return D[1][a][0]


def head(D: Digraph, a: int) -> int:
    return D[1][a][1]


def delta_out(D: Digraph, U: VertexSet) -> ArcSet:
    return frozenset(a for a in range(len(D[1])) if (tail(D, a) in U) and not (head(D, a) in U))


def delta_in(D: Digraph, U: VertexSet) -> ArcSet:
    return frozenset(a for a in range(len(D[1])) if (not (tail(D, a) in U)) and (head(D, a) in U))


def is_dicut_shore(D: Digraph, U: VertexSet) -> bool:
    return all(a not in delta_in(D, U) for a in range(len(D[1]))) and \
        any(a in delta_out(D, U) for a in range(len(D[1])))


def is_dicut_shore_allowing_empty(D: Digraph, U: VertexSet) -> bool:
    n = D[0]
    return any(v in U for v in range(n)) and any(v not in U for v in range(n)) and \
        all(a not in delta_in(D, U) for a in range(len(D[1])))


def meets(S: ArcSet, J: ArcSet) -> bool:
    return any(a in S and a in J for a in S | J)


def is_dijoin(D: Digraph, J: ArcSet) -> bool:
    return all(meets(delta_out(D, U), J) for U in all_vertex_sets(D[0]) if is_dicut_shore(D, U))


def arc_disjoint(J: ArcSet, K: ArcSet) -> bool:
    return not any(a in J and a in K for a in J | K)


def card(S: ArcSet, m: int) -> int:
    return sum(1 for a in range(m) if a in S)


def is_min_dicut_size(D: Digraph, t: int) -> bool:
    m = len(D[1])
    shores = [U for U in all_vertex_sets(D[0]) if is_dicut_shore(D, U)]
    return any(card(delta_out(D, U), m) == t for U in shores) and \
        all(t <= card(delta_out(D, U), m) for U in shores)


def dicut_shores(D: Digraph) -> List[VertexSet]:
    return [U for U in all_vertex_sets(D[0]) if is_dicut_shore(D, U)]


def dicut_sizes(D: Digraph) -> List[int]:
    return [card(delta_out(D, U), len(D[1])) for U in dicut_shores(D)]


def tau_q(D: Digraph) -> Optional[int]:
    s = dicut_sizes(D)
    return min(s) if s else None


def min_dicut_size_witnesses(D: Digraph) -> List[int]:
    """All t in 0..m with IsMinDicutSize D t (should be at most one)."""
    return [t for t in range(len(D[1]) + 1) if is_min_dicut_size(D, t)]


def dicuts(D: Digraph) -> Set[ArcSet]:
    """The dicuts as arc sets: ``deltaOut D U`` over shores.  Not a Lean definition, but the
    object the prose calls a dicut."""
    return {delta_out(D, U) for U in dicut_shores(D)}


def pairwise_arc_disjoint(Js: List[ArcSet]) -> bool:
    """``Js.Pairwise ArcDisjoint`` — positions i < j."""
    return all(arc_disjoint(Js[i], Js[j]) for i in range(len(Js)) for j in range(i + 1, len(Js)))


def all_arc_sets(m: int) -> List[ArcSet]:
    return [frozenset(i for i in range(m) if mask >> i & 1) for mask in range(1 << m)]


def max_packing_length(D: Digraph) -> Optional[int]:
    """Largest ``Js.length`` over lists with every member a dijoin and ``Pairwise ArcDisjoint``.
    None (unbounded) when the empty set is a dijoin, since ``[∅, ∅, ...]`` then qualifies."""
    m = len(D[1])
    if is_dijoin(D, frozenset()):
        return None
    js = [J for J in all_arc_sets(m) if is_dijoin(D, J)]
    minimal = [S for S in js if not any(T < S for T in js)]
    best = 0

    def grow(chosen: List[ArcSet], start: int) -> None:
        nonlocal best
        best = max(best, len(chosen))
        for i in range(start, len(minimal)):
            if pairwise_arc_disjoint(chosen + [minimal[i]]):
                grow(chosen + [minimal[i]], i + 1)

    grow([], 0)
    return best


def is_arc_partition(Js: List[ArcSet], m: int) -> bool:
    return all(sum(1 for J in Js if a in J) == 1 for a in range(m))


def woodall_conjecture(D: Digraph) -> bool:
    """Literal: for every t with IsMinDicutSize D t, some list of t dijoins partitions the arcs.
    Brute force over all assignments of arcs to t blocks."""
    m = len(D[1])
    ok = True
    for t in min_dicut_size_witnesses(D):
        found = False
        for assign in product(range(t), repeat=m):
            Js = [frozenset(a for a in range(m) if assign[a] == b) for b in range(t)]
            if is_arc_partition(Js, m) and all(is_dijoin(D, J) for J in Js):
                found = True
                break
        ok = ok and found
    return ok


def easy_direction(D: Digraph) -> bool:
    """`length_le_tau` as a fact: every disjoint dijoin family has length <= t when
    IsMinDicutSize D t.  Vacuous when no t qualifies."""
    ws = min_dicut_size_witnesses(D)
    if not ws:
        return True
    mp = max_packing_length(D)
    return mp is not None and all(mp <= t for t in ws)


# ---------------------------------------------------------------------------------------
# Comparisons against the prose model.  Prose is run in BOTH readings so that the report
# says which convention the Lean matches.  Everything is in arc indices, so no bridging.

def _prose_tau_survey(D):
    return P.tau(D, allow_empty=False)


def _prose_tau_literal(D):
    return P.tau(D, allow_empty=True)


def _lean_tau_via_IsMinDicutSize(D):
    ws = min_dicut_size_witnesses(D)
    assert len(ws) <= 1, (D, ws)
    return ws[0] if ws else None


COMPARISONS = [
    ("dicuts(survey) vs lean dicuts", lambda D: P.dicuts(D, False), dicuts),
    ("dicuts(literal) vs lean dicuts", lambda D: P.dicuts(D, True), dicuts),
    ("tau(survey) vs lean tau?", _prose_tau_survey, tau_q),
    ("tau(literal) vs lean tau?", _prose_tau_literal, tau_q),
    ("lean tau? vs lean IsMinDicutSize (unbridged pair)", tau_q, _lean_tau_via_IsMinDicutSize),
    ("max_disjoint_dijoins(survey) vs lean max packing length",
     lambda D: P.max_disjoint_dijoins(D, False), max_packing_length),
    ("has_tau_disjoint_dijoins(survey) vs lean WoodallConjecture (partition form)",
     lambda D: (lambda x: True if x is None else x)(P.has_tau_disjoint_dijoins(D, False)),
     woodall_conjecture),
    ("easy_direction(survey) vs lean length_le_tau", lambda D: P.easy_direction_holds(D, False),
     easy_direction),
]
