"""Exact small-instance tools for the balanced-dicut-hypergraph attack.

This module uses only the Python standard library.  Vertices are numbered
``0, ..., n-1`` and arcs are ordered pairs.  Census DAGs use only arcs
``u -> v`` with ``u < v``, so their strongly connected components are already
contracted.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Hashable, Iterable, Iterator, Sequence


Arc = tuple[int, int]


@dataclass(frozen=True)
class OddBergeCycle:
    """A proper odd Berge cycle, represented in cyclic incidence order."""

    vertices: tuple[Hashable, ...]
    hyperedge_indices: tuple[int, ...]

    @property
    def order(self) -> int:
        return len(self.vertices)


def validate_odd_berge_cycle(
    vertices: Iterable[Hashable],
    hyperedges: Iterable[Iterable[Hashable]],
    witness: OddBergeCycle,
) -> bool:
    """Check a proper odd Berge-cycle witness from its raw incidence data."""

    vertex_tuple, edge_tuple = _normalise_hypergraph(vertices, hyperedges)
    vertex_set = set(vertex_tuple)
    order = witness.order
    if order < 3 or order % 2 == 0:
        return False
    if len(set(witness.vertices)) != order or not set(witness.vertices) <= vertex_set:
        return False
    if len(witness.hyperedge_indices) != order:
        return False
    if len(set(witness.hyperedge_indices)) != order:
        return False
    if any(not (0 <= index < len(edge_tuple)) for index in witness.hyperedge_indices):
        return False

    selected_vertices = set(witness.vertices)
    for position, edge_index in enumerate(witness.hyperedge_indices):
        expected = {
            witness.vertices[position],
            witness.vertices[(position + 1) % order],
        }
        if edge_tuple[edge_index] & selected_vertices != expected:
            return False
    return True


def dicuts(n: int, arcs: Sequence[Arc]) -> tuple[frozenset[int], ...]:
    """Return the distinct nonempty dicuts as sets of arc indices.

    For a vertex set U, delta+(U) is a dicut exactly when delta-(U) is
    empty and delta+(U) is nonempty.
    """

    if n < 0:
        raise ValueError("n must be nonnegative")
    for u, v in arcs:
        if not (0 <= u < n and 0 <= v < n):
            raise ValueError(f"arc {(u, v)} has an endpoint outside 0..{n - 1}")

    cuts: set[frozenset[int]] = set()
    for mask in range(1, (1 << n) - 1):
        outgoing: set[int] = set()
        has_entering = False
        for index, (u, v) in enumerate(arcs):
            u_in = bool(mask & (1 << u))
            v_in = bool(mask & (1 << v))
            if not u_in and v_in:
                has_entering = True
                break
            if u_in and not v_in:
                outgoing.add(index)
        if not has_entering and outgoing:
            cuts.add(frozenset(outgoing))
    return tuple(sorted(cuts, key=lambda edge: (len(edge), tuple(sorted(edge)))))


def inclusion_minimal(hyperedges: Iterable[frozenset[int]]) -> tuple[frozenset[int], ...]:
    """Discard every hyperedge that properly contains another hyperedge."""

    ordered = sorted(set(hyperedges), key=lambda edge: (len(edge), tuple(sorted(edge))))
    minimal: list[frozenset[int]] = []
    for edge in ordered:
        if not any(previous < edge for previous in minimal):
            minimal.append(edge)
    return tuple(minimal)


def dibonds(n: int, arcs: Sequence[Arc]) -> tuple[frozenset[int], ...]:
    """Return the inclusion-minimal nonempty dicuts."""

    return inclusion_minimal(dicuts(n, arcs))


def _normalise_hypergraph(
    vertices: Iterable[Hashable], hyperedges: Iterable[Iterable[Hashable]]
) -> tuple[tuple[Hashable, ...], tuple[frozenset[Hashable], ...]]:
    vertex_tuple = tuple(vertices)
    if len(set(vertex_tuple)) != len(vertex_tuple):
        raise ValueError("vertices must be distinct")
    vertex_set = set(vertex_tuple)
    edge_tuple = tuple(frozenset(edge) for edge in hyperedges)
    if any(not edge <= vertex_set for edge in edge_tuple):
        raise ValueError("a hyperedge contains a vertex outside the declared vertex set")
    if len(set(edge_tuple)) != len(edge_tuple):
        raise ValueError("hyperedges must be distinct")
    return vertex_tuple, edge_tuple


def find_odd_berge_cycle(
    vertices: Iterable[Hashable], hyperedges: Iterable[Iterable[Hashable]]
) -> OddBergeCycle | None:
    """Return a shortest proper odd Berge cycle, or ``None``.

    A hypergraph is balanced exactly when its incidence bipartite graph has no
    induced cycle of length 2 mod 4.  We inspect possible lengths in increasing
    order and enumerate chordless paths, so the first witness is shortest.
    """

    vertex_tuple, edge_tuple = _normalise_hypergraph(vertices, hyperedges)
    row_count = len(vertex_tuple)
    edge_count = len(edge_tuple)
    node_count = row_count + edge_count
    adjacency: list[set[int]] = [set() for _ in range(node_count)]
    for edge_index, edge in enumerate(edge_tuple):
        edge_node = row_count + edge_index
        for row_index, vertex in enumerate(vertex_tuple):
            if vertex in edge:
                adjacency[row_index].add(edge_node)
                adjacency[edge_node].add(row_index)

    def search_length(target_length: int) -> tuple[int, ...] | None:
        def extend(start: int, path: list[int]) -> tuple[int, ...] | None:
            if len(path) == target_length:
                if start in adjacency[path[-1]]:
                    return tuple(path)
                return None

            last = path[-1]
            for candidate in sorted(adjacency[last]):
                if candidate == start or candidate in path or candidate < start:
                    continue

                earlier_neighbors = [
                    node for node in path[:-1] if candidate in adjacency[node]
                ]
                at_final_node = len(path) + 1 == target_length
                if at_final_node:
                    if earlier_neighbors != [start]:
                        continue
                elif earlier_neighbors:
                    continue

                witness = extend(start, [*path, candidate])
                if witness is not None:
                    return witness
            return None

        for start in range(node_count):
            witness = extend(start, [start])
            if witness is not None:
                return witness
        return None

    for cycle_length in range(6, 2 * min(row_count, edge_count) + 1, 4):
        nodes = search_length(cycle_length)
        if nodes is None:
            continue

        # Rotate to start with a row node, then orient so each reported edge i
        # contains vertices i and i+1.
        row_position = next(i for i, node in enumerate(nodes) if node < row_count)
        nodes = nodes[row_position:] + nodes[:row_position]
        if nodes[1] < row_count:
            nodes = (nodes[0],) + tuple(reversed(nodes[1:]))
        cycle_vertices = tuple(vertex_tuple[nodes[2 * i]] for i in range(cycle_length // 2))
        cycle_edges = tuple(nodes[2 * i + 1] - row_count for i in range(cycle_length // 2))
        return OddBergeCycle(cycle_vertices, cycle_edges)
    return None


def brute_force_unbalanced_submatrix(
    vertices: Iterable[Hashable], hyperedges: Iterable[Iterable[Hashable]]
) -> bool:
    """Independent definition-level balancedness check for tiny fixtures.

    It searches for an odd square incidence submatrix with exactly two ones in
    every row and column.  This is intentionally slow and is used only to
    cross-check the cycle detector.
    """

    vertex_tuple, edge_tuple = _normalise_hypergraph(vertices, hyperedges)
    for order in range(3, min(len(vertex_tuple), len(edge_tuple)) + 1, 2):
        for selected_vertices in combinations(vertex_tuple, order):
            selected_set = set(selected_vertices)
            for selected_edges in combinations(edge_tuple, order):
                if any(len(edge & selected_set) != 2 for edge in selected_edges):
                    continue
                if all(sum(vertex in edge for edge in selected_edges) == 2 for vertex in selected_vertices):
                    return True
    return False


def source_sink_reachability_is_forest(n: int, arcs: Sequence[Arc]) -> bool:
    """Test whether the bipartite source-to-sink reachability graph is a forest."""

    outgoing: list[list[int]] = [[] for _ in range(n)]
    indegree = [0] * n
    for u, v in arcs:
        outgoing[u].append(v)
        indegree[v] += 1
    sources = [vertex for vertex in range(n) if indegree[vertex] == 0]
    sinks = [vertex for vertex in range(n) if not outgoing[vertex]]
    sink_positions = {sink: i for i, sink in enumerate(sinks)}

    parent = list(range(len(sources) + len(sinks)))

    def find(item: int) -> int:
        while parent[item] != item:
            parent[item] = parent[parent[item]]
            item = parent[item]
        return item

    def union(left: int, right: int) -> bool:
        left_root = find(left)
        right_root = find(right)
        if left_root == right_root:
            return False
        parent[right_root] = left_root
        return True

    for source_position, source in enumerate(sources):
        seen = {source}
        stack = [source]
        while stack:
            current = stack.pop()
            for successor in outgoing[current]:
                if successor not in seen:
                    seen.add(successor)
                    stack.append(successor)
        for sink in sinks:
            if sink == source or sink not in seen:
                continue
            sink_node = len(sources) + sink_positions[sink]
            if not union(source_position, sink_node):
                return False
    return True


def fixed_order_dags(n: int) -> Iterator[tuple[Arc, ...]]:
    """Enumerate every subset of forward arcs ``u -> v`` with ``u < v``."""

    possible_arcs = tuple((u, v) for u in range(n) for v in range(u + 1, n))
    for mask in range(1 << len(possible_arcs)):
        yield tuple(arc for index, arc in enumerate(possible_arcs) if mask & (1 << index))
