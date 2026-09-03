# A three-spanning-tree class at `tau = 3`

Status: **sketch**, targeting `verified:review`.

This is a non-computational special case.  Its class contains simple DAGs
which are not source--sink connected, so it is not subsumed by the cited
source--sink-connected theorem.

## Definitions and sanity checks

For a finite digraph `D=(V,A)` and a nonempty proper set `U`, write
`delta+(U)` for the arcs with tail in `U` and head outside `U`, and
`delta-(U)` for the arcs entering `U`.  A **dicut** is a nonempty set
`delta+(U)` for which `delta-(U)` is empty.  A **dijoin** meets every dicut.
The number `tau(D)` is the minimum cardinality of a dicut.

The underlying undirected multigraph `G` retains one edge for each arc of
`D`, including parallel copies, and forgets its direction.  Loops may be
discarded because they cross no cut.

These conventions behave as expected.  A directed path has singleton prefix
dicuts, so its only dijoin contains every path arc.  A directed cycle has no
dicut.  In the DAG `s1->t1, s2->t1, s2->t2`, the singleton sources define
dicuts, while `s1` has no directed path to the sink `t2`.  In particular, the
definition requires no arc to enter the shore, not merely some arc to leave.

## The theorem

**Theorem.**  Suppose the underlying multigraph `G` of `D` contains three
pairwise edge-disjoint spanning trees.  Then `D` contains three pairwise
arc-disjoint dijoins.  Consequently Woodall's existence conclusion holds for
every such digraph with `tau(D)=3`.

**Proof.**  Let the spanning trees be `T1,T2,T3`, and let `Ji` consist of the
arcs of `D` corresponding to the edges of `Ti`.  The three sets `Ji` are
pairwise disjoint.

Consider an arbitrary dicut `C=delta+(U)`.  Because no arc enters `U`, every
underlying edge crossing the bipartition `(U,V-U)` corresponds to an arc in
`C`.  Every spanning tree crosses every nontrivial vertex bipartition, so
`Ti` has a crossing edge.  Its corresponding arc lies in `C cap Ji`.
Therefore each `Ji` meets every dicut and is a dijoin.  Thus `J1,J2,J3` are
three pairwise disjoint dijoins.  Any unused arcs may be assigned arbitrarily
if a partition of all of `A` is desired.  QED

Notice that the proof establishes the existence direction.  If additionally
`tau(D)=3`, a minimum dicut prevents a fourth disjoint dijoin, so the packing
has the conjectured optimum size.

## A constructive attachment criterion

The spanning-tree hypothesis has the following useful ear-like sufficient
condition.  Start with a loopless undirected multigraph `H` equipped with
three pairwise edge-disjoint spanning trees.  Repeatedly add a new vertex
`v`, together with at least three new edges from `v` to vertices already
present.  Parallel edges are allowed, but the three chosen edge copies must
be distinct.  Orient all edges arbitrarily afterward.

At each step, choose three distinct attachment edges and add one to each old
tree.  Each augmented subgraph is again a tree: it gains one new vertex and
one incident edge, so it stays connected and acyclic.  The trees remain
edge-disjoint.  Induction and the theorem therefore construct three disjoint
dijoins in every resulting digraph.

Equivalently, one may give the vertices outside `H` an order in which every
vertex has at least three incident edge copies to the core or to earlier
vertices.  The proof is a greedy colouring of three such backward edges with
the three tree colours.  This formulation makes the construction linear once
the core trees and the order are supplied.

## A simple non-source--sink-connected `tau=3` example

Take core vertices `0,1,2,3,4,5`.  Put one arc `i->j` for every `i<j`, so the
underlying core is `K6`.  Add vertices `s,t` and the six arcs

```text
s->3, s->4, s->5, 0->t, 1->t, 2->t.
```

The fifteen core edges split into the following three Hamilton paths:

```text
T1: 0-1-5-2-4-3
T2: 1-2-0-3-5-4
T3: 2-3-1-4-0-5.
```

The displayed edge lists are pairwise disjoint and together contain all
fifteen edges of `K6`.  Extend `T1,T2,T3`, respectively, by

```text
{s-3,0-t},  {s-4,1-t},  {s-5,2-t}.
```

This explicitly gives three edge-disjoint spanning trees and hence three
disjoint dijoins by the theorem.  It also proves every nontrivial undirected
cut has at least three edges, since each tree crosses it.  Therefore every
dicut has size at least three.  The dicut `delta+({s})` is exactly
`{s->3,s->4,s->5}`, so `tau(D)=3`.

The sources are `0` and `s`, while the sinks are `5` and `t`.  Vertex `s`
can only reach core vertices numbered at least `3`, and none of those has an
arc to `t`; hence `s` cannot reach `t`.  The DAG is not source--sink
connected.  This proves that the class above contributes cases outside the
previously cited class, without any computational inference.

## Mandatory filters

1. **Schrijver filter: passed.**  The hypothesis supplies three disjoint
   *unit arc copies* across every undirected cut, through three ordinary
   spanning trees.  In a weighted instance, minimum weighted dicut value
   three does not supply these trees: zero-weight arcs still determine which
   shores are dicuts, while a packed dijoin may not use them.  Thus the proof
   does not infer its structural hypothesis from weighted cut value and does
   not prove the false weighted Edmonds--Giles statement.  The attachment
   criterion likewise selects three distinct capacity-one arc copies; merely
   having total attachment weight three is not substituted for that fact.
2. **Lucchesi--Younger filter: passed.**  No min-dijoin/max-disjoint-dicuts
   equality is invoked.  The proof directly exhibits three arc sets and
   checks each against an arbitrary dicut.
3. **Easy-direction filter: passed.**  The spanning trees explicitly produce
   three disjoint dijoins.  The minimum dicut is used only afterward to note
   optimality, not as a purported existence proof.

## Scope and dependencies

The theorem is elementary and depends on no computational result and no
unverified claim elsewhere in the repository.  It is not asserted to be new
to the literature; "new" here means a previously unrecorded special class in
this campaign.  Its restriction is substantial: many digraphs with
`tau=3` have underlying graphs with no three spanning trees.  It does not
address those instances or the full conjecture.

The load-bearing points for independent review are: (1) for a dicut, all
underlying crossing edges really do correspond to its outgoing arcs; (2) each
spanning tree crosses every proper vertex bipartition; and (3) the three
listed Hamilton paths truly partition `E(K6)` in the separating example.
