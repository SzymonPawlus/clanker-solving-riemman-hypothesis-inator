"""Exact ACZ M1-matroid primitives for sink-regular bipartite digraphs.

The implementation follows Definition 4.7 of Abdi--Cornuejols--Zlatin.
It is deliberately dependency-free and represents parallel arcs separately.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, permutations
from random import Random


@dataclass(frozen=True)
class BipartiteDigraph:
    """All arcs are directed from integer sources to integer sinks."""

    source_count: int
    sink_count: int
    arcs: tuple[tuple[int, int], ...]

    def __post_init__(self) -> None:
        for source, sink in self.arcs:
            if not 0 <= source < self.source_count:
                raise ValueError("source outside range")
            if not 0 <= sink < self.sink_count:
                raise ValueError("sink outside range")

    @property
    def source_degrees(self) -> tuple[int, ...]:
        return tuple(sum(source == s for source, _ in self.arcs) for s in range(self.source_count))

    @property
    def sink_degrees(self) -> tuple[int, ...]:
        return tuple(sum(sink == t for _, sink in self.arcs) for t in range(self.sink_count))

    @property
    def active_sources(self) -> tuple[int, ...]:
        return tuple(source for source, degree in enumerate(self.source_degrees) if degree == 4)

    @property
    def rho(self) -> int:
        return self.sink_count - self.source_count


def d27() -> BipartiteDigraph:
    """The 27-vertex graph in ACZ Figure 11, transcribed from its vector source.

    Sources 0..8 are the labelled active vertices 1..9.  Sources 9..11
    are the three unlabelled inactive sources.  Sinks are ordered by their
    original vector-graphic vertex ids.  Repeated pairs are parallel arcs.
    """

    adjacency = (
        (12, 2, 12, 7),       # active vertex 1
        (10, 3, 5, 5),        # active vertex 2
        (0, 6, 6, 14),        # active vertex 3
        (4, 8, 8, 3),         # active vertex 4
        (1, 9, 1, 13),        # active vertex 5
        (10, 11, 11, 4),      # active vertex 6
        (9, 5, 6, 14),        # active vertex 7
        (2, 13, 8, 1),        # active vertex 8
        (0, 7, 12, 11),       # active vertex 9
        (7, 4, 2),            # inactive source
        (13, 3, 9),           # inactive source
        (10, 0, 14),          # inactive source
    )
    arcs = tuple((source, sink) for source, row in enumerate(adjacency) for sink in row)
    return BipartiteDigraph(12, 15, arcs)


def _sink_neighborhood_masks(graph: BipartiteDigraph) -> tuple[int, ...]:
    masks = [0] * graph.sink_count
    for source, sink in graph.arcs:
        masks[sink] |= 1 << source
    return tuple(masks)


def minimum_dicut(graph: BipartiteDigraph) -> int | None:
    """Minimum dicut cardinality by exact source-margin enumeration.

    For a chosen source subset X, the largest source margin contains every
    sink whose complete neighborhood is in X.  Adding all such sinks minimizes
    the outgoing dicut, so one canonical margin per X suffices.
    """

    neighborhoods = _sink_neighborhood_masks(graph)
    all_sources = (1 << graph.source_count) - 1
    # Margins containing every source must omit at least one sink to remain
    # proper; omitting a minimum-degree sink gives the smallest such dicut.
    best: int | None = min(graph.sink_degrees, default=None)
    for source_mask in range(1, all_sources):
        internal_arcs = sum(
            1
            for source, sink in graph.arcs
            if source_mask & (1 << source)
            and neighborhoods[sink] & ~source_mask == 0
        )
        source_degree_sum = sum(
            degree
            for source, degree in enumerate(graph.source_degrees)
            if source_mask & (1 << source)
        )
        cut_size = source_degree_sum - internal_arcs
        best = cut_size if best is None else min(best, cut_size)
    return best


def m1_bases(graph: BipartiteDigraph) -> tuple[int, ...]:
    """Return all M1 bases as bitmasks on active-source positions.

    For a source subset X, the maximum-discrepancy source margin includes
    every sink whose neighborhood is contained in X.  Definition 4.7 then
    requires |Q intersect X| >= 1 + |Y(X)| - |X|.
    """

    active = graph.active_sources
    rank = graph.rho
    if len(active) != 3 * rank:
        raise ValueError("not a sink-regular (3,4)-bipartite degree sequence")
    active_position = {source: position for position, source in enumerate(active)}
    neighborhoods = _sink_neighborhood_masks(graph)
    all_sources = (1 << graph.source_count) - 1
    constraints: list[tuple[int, int]] = []
    for source_mask in range(1, all_sources):
        contained_sinks = sum(mask & ~source_mask == 0 for mask in neighborhoods)
        rhs = 1 + contained_sinks - source_mask.bit_count()
        if rhs <= 0:
            continue
        active_mask = 0
        for source, position in active_position.items():
            if source_mask & (1 << source):
                active_mask |= 1 << position
        constraints.append((active_mask, rhs))

    bases = []
    for chosen in combinations(range(len(active)), rank):
        base = sum(1 << position for position in chosen)
        if all((base & subset).bit_count() >= rhs for subset, rhs in constraints):
            bases.append(base)
    return tuple(bases)


def _pair_is_strongly_orderable(first: int, second: int, base_set: frozenset[int]) -> bool:
    common = first & second
    left = tuple(i for i in range(12) if first & (1 << i) and not common & (1 << i))
    right = tuple(i for i in range(12) if second & (1 << i) and not common & (1 << i))
    for image in permutations(right):
        exchanges = tuple((1 << left[i], 1 << image[i]) for i in range(len(left)))
        valid = True
        for subset in range(1 << len(exchanges)):
            candidate = first
            for index, (remove, add) in enumerate(exchanges):
                if subset & (1 << index):
                    candidate = candidate ^ remove ^ add
            if candidate not in base_set:
                valid = False
                break
        if valid:
            return True
    return False


def restriction_is_strongly_base_orderable(bases: tuple[int, ...], ground: int) -> bool:
    restricted = tuple(base for base in bases if base & ~ground == 0)
    restricted_set = frozenset(restricted)
    return all(
        _pair_is_strongly_orderable(first, second, restricted_set)
        for first in restricted
        for second in restricted
    )


def acz_route_witness(bases: tuple[int, ...], ground_size: int = 12) -> tuple[int, int, int] | None:
    """Find a Q1,Q2,Q3 partition satisfying ACZ Question 8.1 for tau=3."""

    base_set = frozenset(bases)
    all_ground = (1 << ground_size) - 1
    checked_restrictions: dict[int, bool] = {}
    for q3 in bases:
        pair_ground = all_ground ^ q3
        possible_q1 = next(
            (
                q1
                for q1 in bases
                if q1 & q3 == 0 and (pair_ground ^ q1) in base_set
            ),
            None,
        )
        if possible_q1 is None:
            continue
        if pair_ground not in checked_restrictions:
            checked_restrictions[pair_ground] = restriction_is_strongly_base_orderable(
                bases, pair_ground
            )
        if checked_restrictions[pair_ground]:
            return possible_q1, pair_ground ^ possible_q1, q3
    return None


def random_rho4(
    seed: int,
    *,
    source_count: int = 12,
    simple: bool = False,
    max_attempts: int = 100_000,
) -> BipartiteDigraph:
    """Sample a labelled sink-regular rho=4 degree instance exactly.

    This is rejection sampling on uniformly shuffled sink stubs for a fixed
    ordering of the 48 source stubs.  Parallel arcs are retained unless
    ``simple`` is requested.  The returned distribution is not claimed to be
    uniform over unlabelled graphs.
    """

    rng = Random(seed)
    if source_count < 12:
        raise ValueError("rho=4 requires the 12 active sources")
    sink_count = source_count + 4
    source_stubs = tuple(
        source
        for source in range(source_count)
        for _ in range(4 if source < 12 else 3)
    )
    original_sink_stubs = tuple(sink for sink in range(sink_count) for _ in range(3))
    for _ in range(max_attempts):
        sink_stubs = list(original_sink_stubs)
        rng.shuffle(sink_stubs)
        arcs = tuple(zip(source_stubs, sink_stubs))
        if simple and len(set(arcs)) != len(arcs):
            continue
        graph = BipartiteDigraph(source_count, sink_count, arcs)
        if minimum_dicut(graph) >= 3:
            return graph
    raise RuntimeError(f"no accepted graph after {max_attempts} attempts for seed {seed}")


def random_simple_rho4(seed: int, max_attempts: int = 100_000) -> BipartiteDigraph:
    return random_rho4(seed, simple=True, max_attempts=max_attempts)


def encode_graph(graph: BipartiteDigraph) -> dict[str, object]:
    return {
        "source_count": graph.source_count,
        "sink_count": graph.sink_count,
        "arcs": [list(arc) for arc in graph.arcs],
    }
