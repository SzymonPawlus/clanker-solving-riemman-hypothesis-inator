"""Exact helpers for strict forward-arc saturation of small DAGs."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Iterator, Sequence


Arc = tuple[int, int]


@dataclass(frozen=True)
class MinimumDicut:
    shore: tuple[int, ...]
    arcs: tuple[Arc, ...]

    @property
    def size(self) -> int:
        return len(self.arcs)


def _validate(n: int, arcs: Sequence[Arc], require_forward: bool = False) -> tuple[Arc, ...]:
    if n < 0:
        raise ValueError("n must be nonnegative")
    normalised = tuple(sorted(arcs))
    if len(set(normalised)) != len(normalised):
        raise ValueError("parallel copies are outside this simple-DAG experiment")
    for u, v in normalised:
        if not (0 <= u < n and 0 <= v < n) or u == v:
            raise ValueError(f"invalid arc {(u, v)} for n={n}")
        if require_forward and u >= v:
            raise ValueError(f"arc {(u, v)} is not forward in the declared order")
    return normalised


def minimum_dicut(n: int, arcs: Sequence[Arc]) -> MinimumDicut | None:
    """Return a minimum nonempty dicut by direct shore enumeration."""

    arcs = _validate(n, arcs)
    best: MinimumDicut | None = None
    for mask in range(1, (1 << n) - 1):
        outgoing: list[Arc] = []
        has_entering = False
        for u, v in arcs:
            u_in = bool(mask & (1 << u))
            v_in = bool(mask & (1 << v))
            if not u_in and v_in:
                has_entering = True
                break
            if u_in and not v_in:
                outgoing.append((u, v))
        if has_entering or not outgoing:
            continue
        candidate = MinimumDicut(
            tuple(vertex for vertex in range(n) if mask & (1 << vertex)),
            tuple(outgoing),
        )
        if best is None or candidate.size < best.size:
            best = candidate
    return best


def tau(n: int, arcs: Sequence[Arc]) -> int:
    """Minimum dicut cardinality, or zero when there is no nonempty dicut."""

    witness = minimum_dicut(n, arcs)
    return 0 if witness is None else witness.size


def tau_bitset_oracle(n: int, arcs: Sequence[Arc]) -> int:
    """Independent definition-level oracle using predecessor bitsets."""

    arcs = _validate(n, arcs)
    predecessor_masks = [0] * n
    arc_bits: list[tuple[int, int]] = []
    for u, v in arcs:
        predecessor_masks[v] |= 1 << u
        arc_bits.append((1 << u, 1 << v))

    best: int | None = None
    for mask in range(1, (1 << n) - 1):
        is_ideal = all(
            not (mask & (1 << vertex))
            or predecessor_masks[vertex] & ~mask == 0
            for vertex in range(n)
        )
        if not is_ideal:
            continue
        size = sum(bool(mask & tail and not mask & head) for tail, head in arc_bits)
        if size and (best is None or size < best):
            best = size
    return 0 if best is None else best


def fixed_order_dags(n: int) -> Iterator[tuple[Arc, ...]]:
    """Enumerate all subsets of arcs u->v with u<v."""

    possible = tuple((u, v) for u in range(n) for v in range(u + 1, n))
    for mask in range(1 << len(possible)):
        yield tuple(arc for index, arc in enumerate(possible) if mask & (1 << index))


def missing_forward_arcs(n: int, arcs: Sequence[Arc]) -> tuple[Arc, ...]:
    arcs = _validate(n, arcs, require_forward=True)
    present = set(arcs)
    return tuple(
        (u, v)
        for u in range(n)
        for v in range(u + 1, n)
        if (u, v) not in present
    )


def saturation_certificate(n: int, arcs: Sequence[Arc]) -> tuple[tuple[Arc, int], ...]:
    """List every missing forward arc and tau after adding it."""

    arcs = _validate(n, arcs, require_forward=True)
    return tuple((arc, tau(n, (*arcs, arc))) for arc in missing_forward_arcs(n, arcs))


def is_tau_saturated(n: int, arcs: Sequence[Arc], minimum_tau: int = 2) -> bool:
    """Whether every missing forward arc strictly raises the current tau."""

    arcs = _validate(n, arcs, require_forward=True)
    current_tau = tau(n, arcs)
    if current_tau < minimum_tau:
        return False
    return all(after > current_tau for _, after in saturation_certificate(n, arcs))


def has_no_tau_preserving_forward_arc(n: int, arcs: Sequence[Arc]) -> bool:
    """Whether no missing forward arc preserves the current tau.

    This is weaker than ``is_tau_saturated``: a missing arc may lower tau.
    """

    arcs = _validate(n, arcs, require_forward=True)
    current_tau = tau(n, arcs)
    return all(after != current_tau for _, after in saturation_certificate(n, arcs))


def greedy_tau_preserving_extension(n: int, arcs: Sequence[Arc]) -> tuple[Arc, ...]:
    """Add lexicographically first tau-preserving arcs until none remain.

    The endpoint need not be strictly tau-saturated because an unadded arc may
    lower tau. This routine is diagnostic only; it gives no counterexample
    reduction.
    """

    current = set(_validate(n, arcs, require_forward=True))
    current_tau = tau(n, tuple(current))
    if current_tau < 2:
        raise ValueError("the lifting lemma and this saturation routine require tau >= 2")
    while True:
        for arc in missing_forward_arcs(n, tuple(current)):
            if tau(n, (*current, arc)) == current_tau:
                current.add(arc)
                break
        else:
            return tuple(sorted(current))


def source_sink_connected(n: int, arcs: Sequence[Arc]) -> bool:
    """Whether every source reaches every distinct sink."""

    arcs = _validate(n, arcs, require_forward=True)
    outgoing: list[list[int]] = [[] for _ in range(n)]
    indegree = [0] * n
    for u, v in arcs:
        outgoing[u].append(v)
        indegree[v] += 1
    sources = [vertex for vertex in range(n) if indegree[vertex] == 0]
    sinks = [vertex for vertex in range(n) if not outgoing[vertex]]
    for source in sources:
        seen = {source}
        stack = [source]
        while stack:
            current = stack.pop()
            for successor in outgoing[current]:
                if successor not in seen:
                    seen.add(successor)
                    stack.append(successor)
        if any(sink != source and sink not in seen for sink in sinks):
            return False
    return True


def disjoint_dijoin_packing_is_preserved(
    n: int,
    arcs: Sequence[Arc],
    new_arc: Arc,
    packing: Sequence[Sequence[Arc]],
) -> bool:
    """Definition-level finite checker for fixtures of the lifting lemma.

    This is not used to prove the prose lemma. It verifies that each supplied
    member is a dijoin before and after adding an arc for which the enlarged
    graph has tau at least two.
    """

    arcs = _validate(n, arcs)
    enlarged = _validate(n, (*arcs, new_arc))
    if tau(n, enlarged) < 2:
        return False
    packed_sets = [set(member) for member in packing]
    if any(packed_sets[i] & packed_sets[j] for i, j in combinations(range(len(packing)), 2)):
        return False

    def is_dijoin(member: set[Arc], graph_arcs: tuple[Arc, ...]) -> bool:
        for mask in range(1, (1 << n) - 1):
            outgoing: set[Arc] = set()
            entering = False
            for u, v in graph_arcs:
                u_in = bool(mask & (1 << u))
                v_in = bool(mask & (1 << v))
                entering |= not u_in and v_in
                if u_in and not v_in:
                    outgoing.add((u, v))
            if not entering and outgoing and not member & outgoing:
                return False
        return True

    return all(is_dijoin(member, arcs) and is_dijoin(member, enlarged) for member in packed_sets)
