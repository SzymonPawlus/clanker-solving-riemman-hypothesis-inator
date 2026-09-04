"""Fritz John support enumerator for maximin point packings in an equilateral triangle.

Question this answers
---------------------
Proposal V (attacks/r3-approaches, sketch) proposes replacing configuration-space
exhaustion by *support* exhaustion: every maximiser of the maximin problem satisfies
the Fritz John first-order conditions, whose support (which pairs carry a positive
multiplier, which walls carry a positive multiplier) is a finite combinatorial object.
This module enumerates the supports that survive the *provable* combinatorial prunes,
and counts them.  The count is the deliverable: the method is only viable if the count
is small.

Conventions (problems/circle-packing-equilateral-triangle/RULES.md)
------------------------------------------------------------------
A = (0,0), B = (d,0), C = (d/2, d*sqrt(3)/2).  Walls are indexed
    0 = AB  (outward unit normal nu_0 = (0,-1))
    1 = BC  (outward unit normal nu_1 = ( sqrt(3)/2, 1/2))
    2 = CA  (outward unit normal nu_2 = (-sqrt(3)/2, 1/2))

A *support* is a triple (m, G, W):
    m         number of loaded points (the other n-m points are rattlers: they carry
              no multiplier at all, and the FJ conditions say nothing about them),
    G         the loaded contact graph on vertex set {0..m-1},
    W         W[i] subset of {0,1,2}, the walls the point p_i actually lies on (the
              ACTIVE wall constraints, not only the loaded ones: mu_ik >= 0 is allowed
              to vanish).  Taking the active set makes every geometric prune below
              correct, since the degree bounds come from where the point sits, not
              from which multiplier is positive.

Two supports are identified when some graph isomorphism of G composed with some
symmetry of the triangle (S_3 acting on the three wall labels) carries one to the other.

Every prune below is derived and justified in
problems/circle-packing-equilateral-triangle/attacks/r3-stationarity/README.md
(status: sketch).  Nothing here is an assumable claim.
"""

from __future__ import annotations

import itertools
import subprocess
from fractions import Fraction

import networkx as nx

GENG = "/usr/bin/nauty-geng"

# ---------------------------------------------------------------------------
# exact side-length arithmetic:  d = A + B*sqrt(3), A,B rational
# ---------------------------------------------------------------------------


class Quad:
    """A + B*sqrt(3) with exact rational A, B.  Only what is needed here."""

    __slots__ = ("a", "b")

    def __init__(self, a, b=0):
        self.a = Fraction(a)
        self.b = Fraction(b)

    def __repr__(self):
        return f"{self.a} + {self.b}*sqrt(3)"

    def __sub__(self, other):
        if isinstance(other, Quad):
            return Quad(self.a - other.a, self.b - other.b)
        return Quad(self.a - Fraction(other), self.b)

    def sign(self):
        """Exact sign of a + b*sqrt(3)."""
        a, b = self.a, self.b
        if b == 0:
            return (a > 0) - (a < 0)
        if a == 0:
            return (b > 0) - (b < 0)
        if a > 0 and b > 0:
            return 1
        if a < 0 and b < 0:
            return -1
        # opposite signs: compare a^2 with 3 b^2
        s = 1 if a > 0 else -1          # sign of a, opposite to sign of b
        c = a * a - 3 * b * b
        return s if c > 0 else (-s if c < 0 else 0)

    def __ge__(self, other):
        return (self - other).sign() >= 0


def wall_capacity(d: Quad) -> int:
    """Max number of points on one closed side of length d with pairwise gaps >= 2.

    k points on a segment of length d need d >= 2(k-1), so k <= d/2 + 1.
    Computed by exact comparison, no floating point.
    """
    k = 1
    while d >= Quad(2 * k):        # d >= 2k  means k+1 points still fit
        k += 1
    return k


# ---------------------------------------------------------------------------
# wall labels
# ---------------------------------------------------------------------------

LABELS = [
    frozenset(),
    frozenset({0}), frozenset({1}), frozenset({2}),
    frozenset({0, 1}), frozenset({1, 2}), frozenset({0, 2}),
]

# max loaded degree given the wall label:
#   interior  : 6  (contacts all at mutual angle >= 60 deg around a full turn)
#   one wall  : 4  (all contact directions lie in the closed inner half-plane)
#   corner    : 2  (all contact directions lie in the closed 60 deg inner wedge)
DEG_MAX = {0: 6, 1: 4, 2: 2}
# min loaded degree: an interior loaded point needs 0 in the convex hull of its
# contact directions, impossible with fewer than 2; every loaded point needs >= 1.
DEG_MIN = {0: 2, 1: 1, 2: 1}

S3 = list(itertools.permutations([0, 1, 2]))


def harborth_max_edges(m: int) -> int:
    """Penny-graph edge bound  |E| <= floor(3m - sqrt(12m-3))  (Harborth 1974).

    The loaded graph is a spanning subgraph of the graph of all pairs at exactly the
    minimum distance, which is a penny graph, so the bound applies.
    """
    import math

    return int(math.floor(3 * m - math.sqrt(12 * m - 3) + 1e-12))


# ---------------------------------------------------------------------------
# graph-level prunes
# ---------------------------------------------------------------------------


def graph_admissible(G: nx.Graph) -> bool:
    """Prunes that depend on G alone (see README, section 'structural prunes')."""
    m = G.number_of_nodes()
    if m >= 2 and min(dict(G.degree()).values()) < 1:
        return False
    if max(dict(G.degree()).values(), default=0) > 6:
        return False
    if G.number_of_edges() > harborth_max_edges(m):
        return False
    # any two vertices have at most 2 common neighbours: a common neighbour lies on
    # the intersection of two circles of the same radius r about them.
    nodes = list(G.nodes())
    for i in range(m):
        Ni = set(G[nodes[i]])
        for j in range(i + 1, m):
            if len(Ni & set(G[nodes[j]])) > 2:
                return False
    # K4-free: four points pairwise at the same distance do not exist in the plane.
    for clique in nx.find_cliques(G):
        if len(clique) >= 4:
            return False
    if not nx.check_planarity(G, counterexample=False)[0]:
        return False
    return True


def is_union_of_paths(G: nx.Graph) -> bool:
    if max(dict(G.degree()).values(), default=0) > 2:
        return False
    return nx.number_of_edges(G) == G.number_of_nodes() - nx.number_connected_components(G)


# ---------------------------------------------------------------------------
# wall-labelling prunes and enumeration
# ---------------------------------------------------------------------------


def labelling_admissible(G: nx.Graph, W, cap: int, union_of_paths: bool,
                         corners_adjacent: bool) -> bool:
    m = G.number_of_nodes()
    deg = dict(G.degree())
    per_wall = [0, 0, 0]
    corners = set()
    nb = 0
    for v in range(m):
        lab = W[v]
        k = len(lab)
        if not (DEG_MIN[k] <= deg[v] <= DEG_MAX[k]):
            return False
        for w in lab:
            per_wall[w] += 1
        if k == 2:
            if lab in corners:
                return False        # two points at the same triangle vertex
            corners.add(lab)
        if k:
            nb += 1
    if any(c > cap for c in per_wall):
        return False
    # every extreme point of the loaded set carries a wall multiplier, so the loaded
    # set has at least 2 wall-labelled points, and at least 3 unless it is collinear
    # (a collinear loaded set forces G to be a disjoint union of paths).
    need = 2 if (m < 3 or union_of_paths) else 3
    if m >= 2 and nb < min(m, need):
        return False
    # an interior vertex of loaded degree 2 has its two contacts antipodal, so its two
    # neighbours are at distance 2r: they are non-adjacent and share only this vertex.
    for v in range(m):
        if len(W[v]) == 0 and deg[v] == 2:
            a, b = list(G[v])
            if G.has_edge(a, b):
                return False
            if len(set(G[a]) & set(G[b])) > 1:
                return False
    # a corner point of loaded degree 2 has both contact directions inside the closed
    # 60 deg inner wedge and at angle >= 60 deg to each other, so they run exactly along
    # the two sides meeting at that corner: one neighbour on each of the corner's walls.
    for v in range(m):
        if len(W[v]) == 2 and deg[v] == 2:
            a, b = list(G[v])
            k1, k2 = sorted(W[v])
            if not ((k1 in W[a] and k2 in W[b]) or (k2 in W[a] and k1 in W[b])):
                return False
    # a point on exactly one wall with loaded degree 4 has its four directions in a
    # closed half-plane pairwise >= 60 deg apart, hence at 0, 60, 120, 180 deg to the
    # wall: the two extreme neighbours lie on that same wall.
    for v in range(m):
        if len(W[v]) == 1 and deg[v] == 4:
            (k,) = tuple(W[v])
            if sum(1 for u in G[v] if k in W[u]) < 2:
                return False
    # points sharing a wall are collinear at pairwise distance >= r with an edge only
    # when the distance is exactly r, i.e. only between consecutive points: the induced
    # subgraph on each wall is a linear forest.
    for k in range(3):
        vs = [v for v in range(m) if k in W[v]]
        if len(vs) > 2:
            H = G.subgraph(vs)
            if max(dict(H.degree()).values(), default=0) > 2:
                return False
            if H.number_of_edges() > len(vs) - nx.number_connected_components(H):
                return False
    # two distinct corners of the triangle are d apart; when d > r they are not adjacent.
    if not corners_adjacent:
        for a, b in G.edges():
            if len(W[a]) == 2 and len(W[b]) == 2:
                return False
    return True


def enumerate_labellings(G: nx.Graph, cap: int, corners_adjacent: bool = False):
    """All wall labellings of G surviving the labelling prunes (no iso reduction)."""
    m = G.number_of_nodes()
    deg = dict(G.degree())
    uop = is_union_of_paths(G)
    allowed = []
    for v in range(m):
        ok = [lab for lab in LABELS if DEG_MIN[len(lab)] <= deg[v] <= DEG_MAX[len(lab)]]
        if not ok:
            return
        allowed.append(ok)
    out = []
    W = [None] * m
    per_wall = [0, 0, 0]
    corners = set()

    def rec(v):
        if v == m:
            if labelling_admissible(G, tuple(W), cap, uop, corners_adjacent):
                out.append(tuple(W))
            return
        for lab in allowed[v]:
            if len(lab) == 2 and lab in corners:
                continue
            if any(per_wall[w] + 1 > cap for w in lab):
                continue
            W[v] = lab
            for w in lab:
                per_wall[w] += 1
            if len(lab) == 2:
                corners.add(lab)
            rec(v + 1)
            for w in lab:
                per_wall[w] -= 1
            if len(lab) == 2:
                corners.discard(lab)
        W[v] = None

    rec(0)
    return out


def automorphisms(G: nx.Graph):
    gm = nx.algorithms.isomorphism.GraphMatcher(G, G)
    return [tuple(mp[v] for v in range(G.number_of_nodes()))
            for mp in gm.isomorphisms_iter()]


def canonical_labelling(W, auts, m):
    best = None
    for sigma in auts:
        # sigma maps vertex v -> sigma[v]; the relabelled labelling is
        #   W'[sigma[v]] = W[v]
        perm = [None] * m
        for v in range(m):
            perm[sigma[v]] = W[v]
        for tau in S3:
            cand = tuple(tuple(sorted(tau[w] for w in lab)) for lab in perm)
            if best is None or cand < best:
                best = cand
    return best


# ---------------------------------------------------------------------------
# driver
# ---------------------------------------------------------------------------


def geng_graphs(m: int):
    """Isomorphism-free graphs on m vertices with min degree 1, max degree 6, K4-free,
    at most the Harborth number of edges.  These prunes are all sound (README)."""
    if m == 1:
        yield nx.empty_graph(1)
        return
    ub = harborth_max_edges(m)
    cmd = [GENG, "-q", "-d1", "-D6", "-k", str(m), f"1:{ub}"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True)
    for line in p.stdout:
        line = line.strip()
        if line:
            yield nx.from_graph6_bytes(line.encode())
    p.wait()


def count_supports(m: int, cap: int, exact_orbits: bool = True, progress=None):
    """Return (n_graphs_surviving, n_supports) for a given loaded-point count m.

    n_graphs_surviving  graphs passing every graph-level prune AND admitting at least
                        one admissible wall labelling.  This is a rigorous LOWER bound
                        on the number of support classes, because non-isomorphic loaded
                        graphs give non-isomorphic supports.
    n_supports          exact number of support classes when exact_orbits, else None.
    """
    ngraph = 0
    nsup = 0
    seen_total = 0
    for G in geng_graphs(m):
        seen_total += 1
        if progress and seen_total % 200000 == 0:
            progress(seen_total, ngraph, nsup)
        if not graph_admissible(G):
            continue
        labs = enumerate_labellings(G, cap)
        if not labs:
            continue
        ngraph += 1
        if exact_orbits:
            auts = automorphisms(G)
            nsup += len({canonical_labelling(W, auts, m) for W in labs})
    return ngraph, (nsup if exact_orbits else None)
