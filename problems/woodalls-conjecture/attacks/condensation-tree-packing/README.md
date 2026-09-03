# Condensation tree packings give `k` disjoint dijoins

Status: **sketch**, targeting `verified:review`.

This generalizes the `tau=3` construction of PR #210 to arbitrary `k`, moves
the hypothesis from the original graph to its SCC condensation, and uses the
Nash--Williams--Tutte partition theorem to give an exact undirected
certificate.  It also identifies a mandatory partition obstruction in every
counterexample to Woodall's conjecture.

## Definitions and small checks

For a finite digraph `D=(V,A)` and a nonempty proper set `U`, a **dicut** is
the nonempty set `delta+(U)` of arcs leaving `U` when no arc enters `U`.  A
**dijoin** meets every dicut, and `tau(D)` is the minimum cardinality of a
dicut.  Parallel arcs are retained as distinct elements.

The **condensation** `Q` contracts every strongly connected component of `D`
to one vertex.  It is a DAG and retains parallel arc copies between
components.  Let `G_Q` be its underlying undirected multigraph.  A spanning
forest of `G_Q` means one spanning tree in each nontrivial weak component;
isolated vertices contribute no edges.

The definitions pass the standard checks.  A directed path has singleton
prefix dicuts and its full arc set is its only dijoin.  A directed cycle has
no dicut and contracts to one isolated vertex.  In the two-source DAG
`s1->t1, s2->t1, s2->t2`, the singleton sources give dicuts, while `s1`
cannot reach the sink `t2`.  These use the no-entering condition, not merely
a nonempty outgoing boundary.

## Condensation lemma

**Lemma 1.**  Every dicut shore of `D` is a union of strongly connected
components.  Under contraction, its dicut is exactly the corresponding
nonempty dicut of `Q`, with arc multiplicities preserved.  Conversely every
nonempty dicut of `Q` lifts to one of `D`.

**Proof.**  Suppose a shore `U` splits a strong component, with `x` outside
`U` and `y` inside.  A directed path from `x` to `y` has a first arc entering
`U`, contradicting `delta-(U)=empty`.  Thus `U` is a union of components.
Contraction changes no arc whose ends lie on opposite sides, and internal
arcs cross neither cut, proving both assertions.  QED

In particular, `D` and `Q` have the same dicuts as arc sets and the same
minimum dicut cardinality.  Arc sets in `Q` may be viewed as their original
arc copies in `D`.

## Main theorem

**Theorem 2 (tree-packing criterion).**  Let `k` be a positive integer.  If
every nontrivial weak component of `G_Q` contains `k` pairwise edge-disjoint
spanning trees, then `D` contains `k` pairwise arc-disjoint dijoins.

**Proof.**  In each weak component choose trees
`T_1,...,T_k`.  For each `i`, let `F_i` be the union of the trees named `T_i`
over all weak components, and let `J_i` be the corresponding original arcs
of `D`.  The `J_i` are pairwise disjoint.

Fix a dicut `C=delta+(U)`.  By Lemma 1 it is a dicut of `Q`.  Since `C` is
nonempty, at least one weak component is split by `U`.  In every split
component, each spanning tree has an edge crossing `(U,V-U)`.  No arc enters
`U`, so every such underlying crossing edge corresponds to an outgoing arc
in `C`.  Consequently `C` meets every `J_i`.  Thus all `J_i` are dijoins.
Unused arcs can be distributed among them if a partition of all arcs is
desired.  QED

For `k=tau(D)`, this is Woodall's nontrivial existence direction.  The usual
minimum-dicut argument only shows that no `(k+1)`st disjoint dijoin exists.

Passing to the condensation is a real strengthening of an original-graph
tree condition: arbitrary sparse or low-tree-connectivity structure inside a
strong component is irrelevant to dicuts and is erased before the tree test.

## Exact Nash--Williams--Tutte form

For a partition `P={P_1,...,P_r}` of the vertices of an undirected
multigraph `H`, let `e_H(P)` count edge copies whose ends lie in different
parts.  The classical Nash--Williams--Tutte tree-packing theorem says

```text
H has k pairwise edge-disjoint spanning trees
if and only if
e_H(P) >= k(r-1) for every partition P into r>=2 nonempty parts.
```

Applying this independently in every nontrivial weak component gives the
following immediately checkable version of Theorem 2.

**Corollary 3 (partition criterion).**  If, for every weak component `H` of
`G_Q` and every partition `P` of `V(H)` into `r>=2` parts,

```text
e_H(P) >= k(r-1),
```

then `D` has `k` pairwise arc-disjoint dijoins.  In particular, if
`tau(D)=k`, Woodall's conclusion holds for `D`.

This criterion is materially stronger than checking only undirected
bipartitions.  A graph can have every cut of size at least `k` while a
partition into many parts has fewer than `k(r-1)` cross-edges.  The
many-part inequalities are exactly what permits simultaneous global trees.

## Consequence for every counterexample

**Corollary 4 (partition obstruction).**  If `D` is a counterexample to
Woodall's conjecture with `tau(D)=k`, then some nontrivial weak component `H`
of its condensation has a partition `P` into `r>=2` nonempty parts satisfying

```text
e_H(P) <= k(r-1)-1.
```

This follows by contraposition from Corollary 3 and integrality.  Thus every
hypothetical minimal counterexample has an explicit undirected partition
deficiency after all strong components have been contracted.  The obstruction
is stronger and more informative than a small ordinary cut: `r` may exceed
two.  It also explains why minimum dicut size alone does not trigger the
construction--`tau` controls one-way bipartitions, whereas the obstruction
may be a multidirectional or multipart partition.

No minimality assumption is actually needed.  Consequently any vertex-,
arc-, or SCC-minimal counterexample inherits this obstruction automatically.

The obstruction can always be chosen with every part connected in `H`.
Indeed, if a part has `c>1` connected components, refine it into those
components.  No formerly internal edge becomes a cross-edge, while the
right-hand side increases by `k(c-1)`, so a strict violation remains a strict
violation.  For such a connected-part partition, contract every part.  The
resulting quotient is connected, has `r` vertices, and has at most
`k(r-1)-1` edges.  Its average degree is strictly less than `2k`; hence some
part `P_i` has total undirected interface

```text
|delta_G(P_i)| <= 2k-1.
```

Thus every counterexample has, in some weak condensation component, a
connected vertex set with a sparse interface of at most `2k-1` arc copies.
For `tau=3` the interface has at most five arcs.  If this interface has arcs
in only one direction, it is a dicut and therefore has at least `k` arcs;
interfaces smaller than `k` must be genuinely bidirectional.  This
`[k,2k-1]`/bidirectional dichotomy is a concrete target for a subsequent
directed cut or ear decomposition, not merely a restatement that the desired
dijoins are absent.

## Gluing and attachment consequences

The criterion behaves cleanly under two useful decompositions.

**Vertex-interface gluing.**  Suppose a weak component is the union of
subgraphs `H_1,...,H_m` whose block-intersection graph is a tree, adjacent
subgraphs share exactly one vertex, nonadjacent subgraphs are vertex-disjoint,
and the subgraphs share no edges.  If every `H_j` has `k` edge-disjoint
spanning trees, then so does their union.  For each colour `i`, unite the
`i`th tree in every block.  Successively gluing two trees at one vertex
produces a tree, and edge-disjointness is preserved.  Theorem 2 then supplies
`k` dijoins.  This permits articulation interfaces; global high vertex
connectivity is unnecessary.

**`k`-edge vertex attachments.**  Starting from any certified core, add a new
vertex with at least `k` distinct edge copies to old vertices.  Give one such
edge to each tree.  Each tree gains one leaf and remains a spanning tree.
Repeated attachments therefore preserve the dijoin conclusion.  For `k=3`
this recovers the construction in PR #210; for arbitrary `k` it yields an
infinite family.

Replacing trees by connected spanning subgraphs does not enlarge the class:
each connected spanning subgraph contains a spanning tree, and pairwise
edge-disjoint connected subgraphs therefore contain pairwise edge-disjoint
trees.  Conversely a tree is already connected and spanning.  Hence the
Nash--Williams--Tutte inequalities give the exact limit of this undirected
connected-subgraph route; improvement beyond Corollary 3 must exploit which
cuts are directed, rather than weaken “tree” to “connected.”

## Mandatory filters

1. **Schrijver filter: passed.**  The load-bearing hypothesis consists of
   `k` disjoint sets of ordinary, usable arc copies.  In the weighted problem,
   minimum weighted dicut value `k` does not imply the partition inequalities
   on positive-capacity copies: zero-weight arcs still affect which shores
   are dicuts but cannot be used by packed dijoins.  Nothing here derives the
   tree condition from weighted `tau`, so Schrijver's counterexample is not
   contradicted.  The unit-capacity nature of every selected tree edge is
   exactly where the unweighted setting enters.
2. **Lucchesi--Younger filter: passed.**  Lucchesi--Younger is never invoked.
   The proof directly checks each constructed arc set against every dicut;
   it does not exchange minimum dijoins with packed dicuts.
3. **Easy-direction filter: passed.**  Theorem 2 constructs `k` disjoint
   dijoins.  The inequality that a size-`k` dicut forbids more than `k` is
   mentioned only after existence has been proved.

## Status, limitations, and sources

The new directed consequences are elementary deductions from the cited
tree-packing theorem and remain a `sketch` pending independent review.  They
are not claimed as literature novelty.  The condition is broad but not a
proof of Woodall: a condensation failing a Nash--Williams--Tutte partition
inequality may still have `k` disjoint dijoins because dijoins need hit only
dicuts, not every undirected cut.

Primary sources for the tree-packing theorem:

1. C. St. J. A. Nash-Williams, “Edge-disjoint spanning trees of finite
   graphs,” *Journal of the London Mathematical Society* **36** (1961),
   445--450, <https://doi.org/10.1112/jlms/s1-36.1.445>.
2. W. T. Tutte, “On the problem of decomposing a graph into n connected
   factors,” *Journal of the London Mathematical Society* **36** (1961),
   221--230, <https://doi.org/10.1112/jlms/s1-36.1.221>.

The weakest points for cross-examination are the SCC-shore argument, the
componentwise forest construction when a dicut splits several weak
components, and the claim that vertex-interface gluing preserves a tree for
each colour.
