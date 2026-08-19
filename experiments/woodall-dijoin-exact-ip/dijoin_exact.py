"""Exact dicut / dijoin-packing decision by polychromatic colouring.

Status: numerical tooling.  Nothing here is a proof of Woodall's conjecture.

DEFINITIONS USED (restated per problems/woodalls-conjecture/RULES.md section 4).
Let D = (V, A) be a digraph; A is a *sequence* of ordered pairs, so parallel
arcs stay distinct and are identified by their position.  For a nonempty proper
U subset V:

    delta^-(U) = { arcs (x, y) in A : x not in U, y in U }
    delta^+(U) = { arcs (x, y) in A : x in U, y not in U }

  * a DICUT is delta^+(U) for a nonempty proper U with delta^-(U) EMPTY.
    The emptiness of delta^-(U) is the whole content of the definition; merely
    requiring delta^+(U) nonempty is the standard fatal misreading.
  * a DIJOIN is an arc set meeting every dicut.
  * tau(D) is the minimum cardinality of a dicut.

Woodall's conjecture is that tau pairwise arc-disjoint dijoins always exist.

THE REFORMULATION THIS MODULE IS BUILT ON
-----------------------------------------
A superset of a dijoin is a dijoin, so leftover arcs may always be dumped into
an existing part.  Hence, for tau >= 1:

    tau pairwise disjoint dijoins exist
      <=> the arcs admit a colouring by tau colours in which every dicut
          receives ALL tau colours.

(=>) Given disjoint dijoins J_1..J_tau, colour a by i when a in J_i and by 0
     otherwise; each dicut meets each J_i, so every colour occurs in it.
(<=) Colour class i meets every dicut, so it is a dijoin; the classes are
     disjoint because a colouring assigns one colour per arc.

That is a *polychromatic colouring* of the dicut hypergraph: a CSP on |A|
variables with tau values, decided here by complete backtracking.  The
reference implementation in experiments/woodalls-dicuts instead enumerates all
2^|A| arc subsets to list every dijoin; that is the ceiling this module lifts.

Only inclusion-minimal dicuts need constraining (meeting a subset implies
meeting a superset).  All arithmetic is on Python ints used as bitmasks: exact,
no floating point, no LP relaxation.  An UNSAT answer is a completed exhaustive
search, not a solver's opinion.
"""

from __future__ import annotations

from typing import Iterable, Sequence

Arc = tuple[int, int]

# --------------------------------------------------------------------------
# dicuts
# --------------------------------------------------------------------------


def dicut_masks(n: int, arcs: Sequence[Arc]) -> list[int]:
    """All distinct dicuts of the digraph, as bitmasks over arc positions.

    Returns one mask per distinct arc set; duplicates arising from different
    shores are collapsed.  An empty dicut is reported as the mask 0 when it
    genuinely occurs (a closed U with no leaving arcs).
    """
    found: set[int] = set()
    for shore in range(1, (1 << n) - 1):          # nonempty proper subsets
        out = 0
        entered = False
        for index, (tail, head) in enumerate(arcs):
            tail_in = (shore >> tail) & 1
            head_in = (shore >> head) & 1
            if not tail_in and head_in:
                entered = True
                break
            if tail_in and not head_in:
                out |= 1 << index
        if not entered:
            found.add(out)
    return sorted(found)


def minimal_masks(masks: Iterable[int]) -> list[int]:
    """Keep only the inclusion-minimal members of a family of bitmasks."""
    items = sorted(set(masks), key=lambda m: (bin(m).count("1"), m))
    kept: list[int] = []
    for mask in items:
        if not any(prev & mask == prev for prev in kept):
            kept.append(mask)
    return kept


def tau_of(masks: Sequence[int]) -> int | None:
    """Minimum dicut size, or None when the digraph has no dicut at all."""
    if not masks:
        return None
    return min(bin(m).count("1") for m in masks)


# --------------------------------------------------------------------------
# dijoin test (used by the verifier, not by the search)
# --------------------------------------------------------------------------


def is_dijoin_mask(selected: int, dicuts: Sequence[int]) -> bool:
    """Whether the selected arcs meet every dicut."""
    return all(selected & cut for cut in dicuts)


# --------------------------------------------------------------------------
# exact polychromatic-colouring decision
# --------------------------------------------------------------------------


class Stats:
    __slots__ = ("nodes",)

    def __init__(self) -> None:
        self.nodes = 0


def pack_dijoins(
    n_arcs: int,
    dicuts: Sequence[int],
    tau: int,
    node_limit: int | None = None,
    stats: Stats | None = None,
) -> list[int] | None:
    """Decide whether `tau` pairwise disjoint dijoins exist; return them.

    Returns a list of `tau` arc-index bitmasks (pairwise disjoint, each a
    dijoin), or None when no such family exists.  None is a COMPLETE negative:
    the backtracking search is exhaustive over the tau-colouring space modulo
    the colour-permutation symmetry, which the constraint is invariant under.

    Raises RuntimeError if node_limit is exceeded, so an aborted search can
    never be mistaken for a negative answer.
    """
    if tau <= 0:
        return []
    if any(cut == 0 for cut in dicuts):
        # An empty dicut cannot be met, so no dijoin exists; but then tau = 0
        # and the caller should not have asked for a positive packing.
        return None

    cuts = minimal_masks(dicuts)
    # Arcs that lie in no minimal dicut are unconstrained; they may be dumped
    # into colour 0 afterwards.
    constrained = 0
    for cut in cuts:
        constrained |= cut

    arcs = [i for i in range(n_arcs) if (constrained >> i) & 1]
    if not arcs:
        return None

    cut_arcs = [[i for i in arcs if (cut >> i) & 1] for cut in cuts]
    # A dicut smaller than tau makes the instance infeasible by counting.
    for members in cut_arcs:
        if len(members) < tau:
            return None

    cuts_of_arc: dict[int, list[int]] = {a: [] for a in arcs}
    for ci, members in enumerate(cut_arcs):
        for a in members:
            cuts_of_arc[a].append(ci)

    colour: dict[int, int] = {}
    used_mask = [0] * len(cuts)        # colours already present in each cut
    free_count = [len(m) for m in cut_arcs]   # uncoloured arcs in each cut
    full = (1 << tau) - 1
    st = stats if stats is not None else Stats()

    def feasible() -> bool:
        for ci in range(len(cuts)):
            missing = bin(full & ~used_mask[ci]).count("1")
            if missing > free_count[ci]:
                return False
        return True

    def choose() -> int | None:
        """Most-constrained uncoloured arc: from the cut with least slack."""
        best_ci = -1
        best_slack = None
        for ci in range(len(cuts)):
            missing = bin(full & ~used_mask[ci]).count("1")
            if missing == 0:
                continue
            slack = free_count[ci] - missing
            if best_slack is None or slack < best_slack:
                best_slack = slack
                best_ci = ci
        if best_ci < 0:
            return None
        for a in cut_arcs[best_ci]:
            if a not in colour:
                return a
        return None

    def search(max_used: int) -> bool:
        st.nodes += 1
        if node_limit is not None and st.nodes > node_limit:
            raise RuntimeError("node limit exceeded")
        if not feasible():
            return False
        arc = choose()
        if arc is None:
            return True                      # every cut already polychromatic
        # Colour-permutation symmetry break: colours are fully interchangeable,
        # so only ever open one fresh colour.
        limit = min(tau - 1, max_used + 1)
        for c in range(limit + 1):
            colour[arc] = c
            bit = 1 << c
            touched = cuts_of_arc[arc]
            for ci in touched:
                used_mask[ci] |= bit
                free_count[ci] -= 1
            if search(max(max_used, c)):
                return True
            for ci in touched:
                free_count[ci] += 1
            del colour[arc]
            # recompute used_mask for touched cuts (a colour may no longer occur)
            for ci in touched:
                m = 0
                for b in cut_arcs[ci]:
                    if b in colour:
                        m |= 1 << colour[b]
                used_mask[ci] = m
        return False

    if not search(-1):
        return None

    # The search stops as soon as every cut is polychromatic, which can leave
    # arcs uncoloured; they are free and go to colour 0.
    parts = [0] * tau
    for a in arcs:
        parts[colour.get(a, 0)] |= 1 << a
    # Unconstrained arcs are dumped into colour 0; a superset of a dijoin is a
    # dijoin, so this keeps every part a dijoin and the parts disjoint.
    parts[0] |= ((1 << n_arcs) - 1) & ~constrained
    return parts


# --------------------------------------------------------------------------
# end-to-end analysis + independent re-verification of the witness
# --------------------------------------------------------------------------


def analyse(n: int, arcs: Sequence[Arc], node_limit: int | None = None) -> dict:
    """Compute tau and decide the packing, re-verifying any witness.

    The witness check is deliberately redundant: it re-tests every emitted part
    against the FULL dicut family (not the minimal one used by the search) and
    re-checks pairwise disjointness, so a bug in the minimality reduction or in
    the colouring search cannot produce a silently accepted answer.
    """
    cuts = dicut_masks(n, arcs)
    tau = tau_of(cuts)
    result = {"n": n, "arcs": list(arcs), "tau": tau, "n_dicuts": len(cuts)}
    if tau is None:
        result["holds"] = True
        result["reason"] = "no dicut exists; the statement is vacuous here"
        return result
    if tau == 0:
        result["holds"] = True
        result["reason"] = "empty dicut, tau = 0, zero dijoins required"
        return result

    parts = pack_dijoins(len(arcs), cuts, tau, node_limit=node_limit)
    if parts is None:
        result["holds"] = False
        result["packing"] = None
        return result

    # independent re-verification
    assert len(parts) == tau
    for i in range(tau):
        if not is_dijoin_mask(parts[i], cuts):
            raise AssertionError(f"emitted part {i} is not a dijoin: {arcs}")
        for j in range(i + 1, tau):
            if parts[i] & parts[j]:
                raise AssertionError(f"parts {i},{j} overlap: {arcs}")
    result["holds"] = True
    result["packing"] = [
        [i for i in range(len(arcs)) if (p >> i) & 1] for p in parts
    ]
    return result
