# Repairing terminal clamping by forced shore closures

**Issue:** #232. **Status:** `sketch`, targeting `verified:review`.

This repairs most of the terminal-clamping obstruction from PR #230.  For a
relevant fixed trace, the two original clamp blocks cannot merge.  Extra
initial components which feed the trace block are forced into every trace
shore, while extra terminal components fed by the complementary block are
forced out.  Clamping these entire closures is safe and yields a strictly
broader automatic trace-packing theorem.

The only remaining obstruction consists of rogue initial components which do
not reach the trace, or rogue terminal components which are not reachable
from its complement.  Each rogue component creates a genuine binary shore
state and must therefore be exported to the separator trace/Hall machinery;
it cannot be erased by another safe clamp.

## Definitions and small checks

For a finite digraph `D=(V,A)`, a **dicut** is a nonempty outgoing boundary
`delta+(U)` with no arc entering `U`.  A **dijoin** meets every dicut.

Fix `S subseteq V` and a proper nonempty `T subset S`.  Let `B_D(T)` be the
nonempty boundaries of all incoming-closed shores `U` with
`U intersection S=T`, and assume this family is nonempty.  Put

```text
mu_D(T)=min{|B|:B in B_D(T)}.
```

A `T`-cover meets every member of `B_D(T)`.  The goal is to construct
`mu_D(T)` pairwise arc-disjoint `T`-covers.

The no-entering condition is essential.  A directed path has prefix dicuts;
a directed cycle has no dicut; and in
`s1->t1, s2->t1, s2->t2`, the singleton sources define dicuts although the
first source cannot reach the second sink.

## Initial clamps and their condensation

Add artificial arcs in both directions connecting all vertices of `T`, and
separately all vertices of `S-T`.  Call the augmented digraph `D0` and its
condensation `Q`.  Let `c` be the strong component containing `T` and `d` the
strong component containing `S-T`.

Every original incoming-closed shore with trace `T` remains incoming-closed
in `D0`, because each artificial arc has both ends on the same side.  Hence:

**Lemma 1 (merger eliminated).**  The components `c` and `d` are distinct.

**Proof.**  If they were equal, every incoming-closed shore, being a union of
strong components, would contain either both clamped sets or neither.  It
could not have trace exactly `T`, contrary to `B_D(T)` being nonempty.  QED

Thus clamp-block merger is not a genuine obstruction for any relevant trace.

## Forced closures

In the DAG `Q`, define

```text
P = {components which can reach c},
F = {components reachable from d}.
```

**Lemma 2 (forced membership).**  Every incoming-closed shore with trace `T`
contains every component in `P` and excludes every component in `F`.
Moreover `P` and `F` are disjoint.

**Proof.**  Such a shore contains `c`.  Predecessor closure along a path to
`c` forces every member of `P` into it.  It excludes `d`; if it contained a
component reachable from `d`, predecessor closure along that path would also
force `d` in, a contradiction.  Hence it excludes `F`.  If a component lay
in both sets, there would be a path from `d` through it to `c`, and containing
`c` would force `d`, contradicting existence of the trace shore.  QED

Now add artificial bidirected arcs making all original vertices represented
by `P` strongly connected, and likewise all vertices represented by `F`.
Call the result `D*`.  This operation is **safe**: Lemma 2 puts both endpoints
of every new arc on the same side of every fixed-trace shore.  Consequently
the nonempty dicut boundaries of `D*`, once the artificial arcs are ignored,
will be exactly `B_D(T)` whenever its source and sink components are the two
new closure blocks.

## Closure-clampability and automatic adequacy

Call `(D,S,T)` **closure-clampable** when

```text
every source component of Q can reach c, and
d can reach every sink component of Q.                    (CC)
```

This strictly weakens the original terminal-clamping condition: `c` itself
need not initially be a source, and `d` need not initially be a sink.

**Theorem 3.**  If `(D,S,T)` is closure-clampable, then `D` has
`mu_D(T)` pairwise arc-disjoint `T`-covers.  In particular, local adequacy at
three colours is automatic.

**Proof.**  Under (CC), `P` contains every source of `Q`.  Every vertex of a
finite DAG is reachable from some source, so after `P` is made one strong
component, that component reaches every component and is the unique source
of the condensation of `D*`.  Symmetrically, `F` contains every sink of `Q`;
every component reaches a sink, so the `F` block is the unique sink.

Every nonempty proper incoming-closed shore of `D*` therefore contains the
`P` block and excludes the `F` block.  Conversely every original shore with
trace `T` remains incoming-closed after both safe clamps.  Thus the dicuts of
`D*` correspond exactly to `B_D(T)`, have no artificial crossing arc, and

```text
tau(D*)=mu_D(T).                                          (1)
```

The condensation of `D*` has a unique source and sink, hence is
source--sink connected.  The cited source--sink-connected packing theorem
gives `mu_D(T)` pairwise arc-disjoint dijoins of `D*`.  Delete all artificial
arcs from them.  Artificial arcs cross no dicut, so deletion preserves the
hitting property and disjointness.  The remaining original arc sets are
`mu_D(T)` disjoint `T`-covers.  QED

Combining Theorem 3 with the sharp one-optional-trace threshold of PR #227
closes every `tau=3` separator instance having one relevant optional trace,
no unhandled forced trace, and closure-clampable local pieces: local covering
counts are at least `min(3,mu_i)`, while a compatible pair of minimum shores
and `tau=3` give `mu_1+mu_2>=3`; the covering counts therefore sum to at least
three and can be paired into three global dijoins.

## Strictness: a repaired non-source--sink-connected piece

Let

```text
S={c,d}, T={c},
A={a1,a2,c,d,b1,b2},
```

and take the arcs

```text
a1->c, a2->c, a1->d, c->b1, d->b1, d->b2.
```

The sources are `a1,a2`, the sinks are `b1,b2`, and `a2` cannot reach `b2`,
so the original piece is not source--sink connected.  The initial trace
component `c` is not a source and `d` is not a sink, so the narrower terminal
clamp of PR #230 does not apply.

Nevertheless both sources reach `c`, and `d` reaches both sinks.  Here
`P={a1,a2,c}` and `F={d,b1,b2}`.  Every trace-`{c}` shore contains `P` and
excludes `F`; the safe closure clamps make these the unique source and sink
blocks.  Theorem 3 applies.  This proves that forced-closure repair genuinely
enlarges the local class beyond both the original source--sink-connected
pieces and the earlier terminal clamp.

## Exact remaining obstruction and decomposition state

If a relevant trace is not closure-clampable, Lemma 1 rules out merger.  In
the condensation after the safe `P,F` clamps, at least one of the following
exists:

1. a **rogue source** component `r` distinct from the `P` block; or
2. a **rogue sink** component `q` distinct from the `F` block.

If the `F` block is itself a source after clamping, successor-closure of `F`
and absence of incoming arcs make it an isolated weak component; it is fixed
out of every trace shore and contributes no trace boundary.  Dually, a `P`
block which is also a sink is an isolated forced-in weak component.  Discard
these irrelevant components.  Every remaining rogue source or sink lies
outside both forced blocks and is a genuine binary trace state rather than an
artifact.

For a remaining rogue source `r`, the predecessor closure `P` is an
incoming-closed trace-`T` realization excluding `r`, while `P union {r}` is
also incoming-closed and has the same separator trace.  (A source component
has no predecessors, and it contains no separator vertex because those lie
in `c` or `d`.)  Thus incoming-closed realizations have both choices `r out`
and `r in`; whether either boundary is empty is retained by the forced/optional
trace formalism.

For a remaining rogue sink `q`, the realization `P` excludes `q`.  The union
of `P` with the full predecessor closure of `q` is incoming-closed, still
excludes `d` because `d` cannot reach `q`, and hence has the same trace while
including `q`.  Again both states occur.  If this union were the whole graph,
it would include `d`, impossible; so it remains proper.

Accordingly, a rogue source or sink cannot be added to either safe clamp:
doing so would cross one of two actually realizable trace shores.  The
correct decomposition is to export one membership bit for each rogue branch.
With no rogue bits, Theorem 3 closes the instance.  With one bit, the two
shore subfamilies are serial alternatives.  With several bits, their local
cover defects feed exactly the isolated-slot and collision-rectangle Hall
states classified in PR #224.  This identifies the remaining mixed regime
without falsely claiming that arbitrary branch packings are automatically
compatible.

## Mandatory filters

1. **Schrijver filter: passed.**  The external packing engine is the known
   source--sink-connected theorem, for which the stronger capacitated form is
   valid.  The downstream Woodall conclusion uses disjoint unit-capacity
   slots.  No general weighted minimum-cut value is converted into a packing
   outside the closure-clampable class.
2. **Lucchesi--Younger filter: passed.**  No cut/dijoin min-max role reversal
   is used.  The fixed-trace dicut correspondence is proved directly, and
   actual packed dijoins from the cited restricted theorem become actual
   trace covers.
3. **Easy-direction filter: passed.**  Theorem 3 constructs the full set of
   `mu_D(T)` covers.  Its `tau=3` consequence then explicitly pairs local
   covers into three global dijoins; it does not infer existence from the
   minimum-cut upper bound.

## Dependency and review targets

The cited engine is Schrijver, “Min-max relations for directed graphs,”
*Annals of Discrete Mathematics* **16** (1982), Theorems 4 and 5 and
Corollary 5a, <https://ir.cwi.nl/pub/10048/10048D.pdf>, as already recorded in
the problem README.  The new closure and obstruction arguments remain
`sketch` pending independent review.

The highest-risk points are safety of clamping all of `P` and `F`, uniqueness
of the resulting source/sink components, and the claim that rogue source and
sink membership states are both realizable without changing the separator
trace.
