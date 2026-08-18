"""Exact, dependency-free primitives for small Woodall-conjecture instances.

Vertices are hashable objects.  Arcs are stored in a sequence and identified by
their integer position, so parallel arcs are not accidentally collapsed.
The algorithms are exponential and intended as a trustworthy small-instance
reference implementation, not as a large search engine.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Hashable, Iterable, Iterator, Sequence

Vertex = Hashable
Arc = tuple[Vertex, Vertex]
ArcSet = frozenset[int]


@dataclass(frozen=True)
class Digraph:
    vertices: tuple[Vertex, ...]
    arcs: tuple[Arc, ...]

    def __init__(self, vertices: Iterable[Vertex], arcs: Iterable[Arc]):
        vertex_tuple = tuple(vertices)
        if len(set(vertex_tuple)) != len(vertex_tuple):
            raise ValueError("vertices must be distinct")
        arc_tuple = tuple(arcs)
        vertex_set = set(vertex_tuple)
        if any(u not in vertex_set or v not in vertex_set for u, v in arc_tuple):
            raise ValueError("every arc endpoint must be a vertex")
        object.__setattr__(self, "vertices", vertex_tuple)
        object.__setattr__(self, "arcs", arc_tuple)


def dicuts(graph: Digraph) -> tuple[ArcSet, ...]:
    """Enumerate distinct dicuts exactly.

    For every nonempty proper U, delta+(U) is included only when delta-(U)
    is empty.  Different vertex sets producing the same arc set are deduplicated.
    In particular, an empty dicut is retained when it genuinely occurs.
    """

    vertices = graph.vertices
    found: set[ArcSet] = set()
    for size in range(1, len(vertices)):
        for chosen in combinations(vertices, size):
            inside = set(chosen)
            outgoing: set[int] = set()
            has_incoming = False
            for index, (tail, head) in enumerate(graph.arcs):
                if tail not in inside and head in inside:
                    has_incoming = True
                    break
                if tail in inside and head not in inside:
                    outgoing.add(index)
            if not has_incoming:
                found.add(frozenset(outgoing))
    return tuple(sorted(found, key=lambda cut: (len(cut), tuple(sorted(cut)))))


def tau(graph: Digraph) -> int | None:
    """Return the minimum dicut size, or None when the graph has no dicuts."""

    cuts = dicuts(graph)
    return min(map(len, cuts)) if cuts else None


def is_dijoin(graph: Digraph, arc_indices: Iterable[int]) -> bool:
    """Whether the selected arcs meet every dicut."""

    selected = frozenset(arc_indices)
    if any(index < 0 or index >= len(graph.arcs) for index in selected):
        raise ValueError("arc index out of range")
    return all(selected & cut for cut in dicuts(graph))


def _reachable(vertices: Sequence[Vertex], arcs: Iterable[Arc], start: Vertex) -> set[Vertex]:
    adjacency = {vertex: [] for vertex in vertices}
    for tail, head in arcs:
        adjacency[tail].append(head)
    reached = {start}
    stack = [start]
    while stack:
        for head in adjacency[stack.pop()]:
            if head not in reached:
                reached.add(head)
                stack.append(head)
    return reached


def is_strongly_connected(graph: Digraph) -> bool:
    if not graph.vertices:
        return True
    start = graph.vertices[0]
    if len(_reachable(graph.vertices, graph.arcs, start)) != len(graph.vertices):
        return False
    reversed_arcs = ((head, tail) for tail, head in graph.arcs)
    return len(_reachable(graph.vertices, reversed_arcs, start)) == len(graph.vertices)


def is_dijoin_by_reverse_augmentation(graph: Digraph, arc_indices: Iterable[int]) -> bool:
    """Independent dijoin test via strong-connectivity augmentation.

    The standard equivalence retains every original arc and adds the reverse of
    each selected arc.  Replacing selected arcs by their reversals is not
    equivalent (a directed path is an immediate counterexample).
    """

    selected = frozenset(arc_indices)
    if any(index < 0 or index >= len(graph.arcs) for index in selected):
        raise ValueError("arc index out of range")
    augmented = list(graph.arcs)
    augmented.extend((graph.arcs[index][1], graph.arcs[index][0]) for index in selected)
    return is_strongly_connected(Digraph(graph.vertices, augmented))


def strongly_connected_components(graph: Digraph) -> tuple[frozenset[Vertex], ...]:
    """Compute SCCs with Kosaraju's algorithm in deterministic order."""

    adjacency = {vertex: [] for vertex in graph.vertices}
    reverse = {vertex: [] for vertex in graph.vertices}
    for tail, head in graph.arcs:
        adjacency[tail].append(head)
        reverse[head].append(tail)

    seen: set[Vertex] = set()
    order: list[Vertex] = []

    def finish(vertex: Vertex) -> None:
        seen.add(vertex)
        for head in adjacency[vertex]:
            if head not in seen:
                finish(head)
        order.append(vertex)

    for vertex in graph.vertices:
        if vertex not in seen:
            finish(vertex)

    components: list[frozenset[Vertex]] = []
    seen.clear()

    def collect(vertex: Vertex, component: set[Vertex]) -> None:
        seen.add(vertex)
        component.add(vertex)
        for tail in reverse[vertex]:
            if tail not in seen:
                collect(tail, component)

    for vertex in reversed(order):
        if vertex not in seen:
            component: set[Vertex] = set()
            collect(vertex, component)
            components.append(frozenset(component))
    return tuple(components)


def condensation(graph: Digraph) -> Digraph:
    """Contract SCCs; retain multiplicity of arcs between components."""

    components = strongly_connected_components(graph)
    component_of = {
        vertex: component_index
        for component_index, component in enumerate(components)
        for vertex in component
    }
    arcs = (
        (component_of[tail], component_of[head])
        for tail, head in graph.arcs
        if component_of[tail] != component_of[head]
    )
    return Digraph(range(len(components)), arcs)


def dijoins(graph: Digraph) -> Iterator[ArcSet]:
    """Enumerate all dijoins in nondecreasing cardinality."""

    indices = range(len(graph.arcs))
    for size in range(len(graph.arcs) + 1):
        for chosen in combinations(indices, size):
            if is_dijoin(graph, chosen):
                yield frozenset(chosen)


def find_disjoint_dijoins(graph: Digraph, count: int) -> tuple[ArcSet, ...] | None:
    """Find ``count`` pairwise disjoint dijoins by exhaustive backtracking."""

    if count < 0:
        raise ValueError("count must be nonnegative")
    if count == 0:
        return ()
    candidates = tuple(dijoins(graph))

    def search(start: int, chosen: tuple[ArcSet, ...], used: ArcSet):
        if len(chosen) == count:
            return chosen
        for position in range(start, len(candidates)):
            candidate = candidates[position]
            if not candidate & used:
                result = search(position + 1, chosen + (candidate,), used | candidate)
                if result is not None:
                    return result
        return None

    return search(0, (), frozenset())
