"""Independent set-based verifier for ACZ M1 bases and strong orderability."""

from __future__ import annotations

from itertools import combinations, permutations

from acz import BipartiteDigraph


def bases_by_sink_subsets(graph: BipartiteDigraph) -> frozenset[frozenset[int]]:
    """Compute M1 bases by enumerating sink subsets, not source closures.

    For a nonempty proper sink set Y, the smallest source margin containing Y
    uses N(Y).  Definition 4.7 becomes
    |Q intersect N(Y)| >= 1 + |Y| - |N(Y)|.
    """

    active = graph.active_sources
    active_position = {source: position for position, source in enumerate(active)}
    incident_sources = [set() for _ in range(graph.sink_count)]
    for source, sink in graph.arcs:
        incident_sources[sink].add(source)

    constraints: list[tuple[frozenset[int], int]] = []
    all_sinks = (1 << graph.sink_count) - 1
    for sink_mask in range(1, all_sinks):
        neighborhood: set[int] = set()
        sink_count = 0
        for sink, sources in enumerate(incident_sources):
            if sink_mask & (1 << sink):
                sink_count += 1
                neighborhood.update(sources)
        rhs = 1 + sink_count - len(neighborhood)
        if rhs > 0:
            constraints.append(
                (
                    frozenset(active_position[s] for s in neighborhood if s in active_position),
                    rhs,
                )
            )

    found = set()
    for chosen_tuple in combinations(range(len(active)), graph.rho):
        chosen = frozenset(chosen_tuple)
        if all(len(chosen & subset) >= rhs for subset, rhs in constraints):
            found.add(chosen)
    return frozenset(found)


def restriction_is_sbo_sets(
    bases: frozenset[frozenset[int]], ground: frozenset[int]
) -> bool:
    restricted = frozenset(base for base in bases if base <= ground)
    for first in restricted:
        for second in restricted:
            common = first & second
            domain = tuple(sorted(first - common))
            codomain = tuple(sorted(second - common))
            pair_ok = False
            for permuted in permutations(codomain):
                mapping = dict(zip(domain, permuted))
                all_partial_exchanges_are_bases = True
                for size in range(len(domain) + 1):
                    for selected_tuple in combinations(domain, size):
                        selected = frozenset(selected_tuple)
                        image = frozenset(mapping[x] for x in selected)
                        if (first - selected) | image not in restricted:
                            all_partial_exchanges_are_bases = False
                            break
                    if not all_partial_exchanges_are_bases:
                        break
                if all_partial_exchanges_are_bases:
                    pair_ok = True
                    break
            if not pair_ok:
                return False
    return True


def route_witness_sets(
    bases: frozenset[frozenset[int]], ground: frozenset[int]
) -> tuple[frozenset[int], frozenset[int], frozenset[int]] | None:
    for q3 in bases:
        remaining = ground - q3
        for q1 in bases:
            q2 = remaining - q1
            if not q1 <= remaining or q2 not in bases:
                continue
            if restriction_is_sbo_sets(bases, remaining):
                return q1, q2, q3
    return None
