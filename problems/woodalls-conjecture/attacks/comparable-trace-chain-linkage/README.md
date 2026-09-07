# Comparable trace chains reduce exactly to capped interval linkages

**Issue:** #254. **Status:** `sketch`, targeting `verified:review`.

The two-adjacent-trace augmentation from PR #253 does not iterate by
preserving one chain-wide flow.  A three-trace serial network with local
minima `(2,1,2)` already defeats that plan: its chain-wide flow has value one,
although two disjoint covers are needed at both endpoint traces.

This attack gives the correct arbitrary-length replacement.  Paths may be
born and die at intermediate separator layers.  Each such path covers a
consecutive interval of traces.  If each piece contains a mutually
arc-disjoint path family whose interval depth at trace `t` is the capped
local minimum `min(3,mu_it)`, then the two pieces always glue at `tau=3`.
There is no additional many-trace profile obstruction: a direct sweep colors
the combined interval family with three colors so that every trace sees all
three colors.

Thus the comparable-chain program separates cleanly into:

```text
local problem: construct a capped-depth interval linkage;
global problem: solved here by polychromatic interval coloring.
```

The local existence statement is the genuine remaining submodular-flow
target.  The explicit `(2,1,2)` example proves why it must permit intermediate
path endpoints rather than repeatedly augment one global source--sink flow.

## Directed setup

For a finite digraph, a **dicut** is a nonempty outgoing boundary
`delta+(X)` with `delta-(X)=empty`.  A **dijoin** meets every dicut.

Let a separator carry a chain of relevant traces

```text
R_0 proper-subset R_1 proper-subset ... proper-subset R_m. (1)
```

Write the separator layers as

```text
Z_0=R_0,
Z_j=R_j-R_(j-1)       (1<=j<=m),
Z_(m+1)=S-R_m.                                          (2)
```

The first and last layers are assumed nonempty.  In piece `D_i`, let
`B_it` be the nonempty boundaries of incoming-closed shores with trace
`R_t`; assume every relevant trace is optional, so no member is empty.  Put

```text
mu_it=min{|B|:B in B_it},
a_it=min(3,mu_it).                                       (3)
```

A directed path beginning in layer `Z_p` and ending in layer `Z_q`, with
`p<=q`, is guaranteed to cover every trace `R_t` with

```text
p <= t < q.                                              (4)
```

Indeed its first vertex lies inside every such trace and its last vertex
outside.  It therefore crosses every incoming-closed shore of that trace on
an original forward arc.  The guaranteed coverage set (4) is a consecutive
interval of trace indices.  A path may cover extra traces accidentally; that
only helps the construction below.

The no-entering condition is essential in this crossing argument.  A path
leaving an arbitrary shore could later re-enter it, whereas no arc of the
digraph enters an incoming-closed shore.

## Capped-depth chain linkages

Call a family `P_i` a **capped-depth chain linkage** in piece `D_i` when:

1. its paths are mutually arc-disjoint;
2. every path has endpoints in two layers `Z_p,Z_q` with `p<q`;
3. at every trace index `t`, exactly `a_it` path intervals (4) contain `t`.

The depth is capped at three, so no point belongs to more than three linkage
intervals in either piece.  Paths with the same endpoints need not be
vertex-disjoint.  Only their original arcs must be disjoint.

This definition is deliberately a local flow condition, not a conclusion
smuggled in from the desired dijoins.  Each path is independently certified
as a cover of every trace in its interval by the endpoint-crossing argument.

## Polychromatic coloring of an interval multicover

**Lemma 1.**  Let `I` be a finite multiset of intervals of the discrete line
`{0,...,m}`.  If every point belongs to at least `k` intervals, then the
intervals can be colored with `k` colors so that every point belongs to an
interval of every color.

**Proof.**  Sweep the points from left to right.  At the current point keep,
for each color, one representative interval of that color which contains the
point.  At point zero, choose any `k` intervals containing it and give them
the distinct colors.

On moving to the next point, retain every representative which still
contains that point.  Suppose `r` representatives remain.  Any previously
colored interval which contains the new point is still its color's
representative: a representative is replaced only after its right endpoint
has passed.  Since at least `k` intervals contain the new point, at least
`k-r` of them are uncolored.  Choose that many as representatives for the
missing colors.  This restores all `k` colors at the new point.  Continue to
the last point, then color unused intervals arbitrarily.  QED

The proof is constructive and allows repeated intervals.  It is stronger
than merely properly coloring an interval graph: intervals of one color may
overlap, but every point is polychromatic.

## Arbitrary-chain gluing theorem at `tau=3`

Let `D=D_1 union D_2` have arc-disjoint pieces and common separator `S`.
Assume its only relevant traces are the chain (1), all are optional in both
pieces, and there are no relevant forced traces.  Local shores of the same
trace unite to a global incoming-closed shore, with boundary the disjoint
union of their local boundaries; every global dicut restricts in this way.

**Theorem 2.**  If `tau(D)=3` and each piece admits a capped-depth chain
linkage, then `D` has three pairwise arc-disjoint dijoins.

**Proof.**  For each trace `t`, unite minimum local shores from the two
pieces.  Their boundary is a global dicut, so

```text
mu_1t+mu_2t >= 3.
```

Capping either summand at three preserves the inequality:

```text
a_1t+a_2t >= 3.                                         (5)
```

Take the disjoint union of the interval multisets belonging to the two local
chain linkages.  Its depth at `t` is exactly the left side of (5).  Apply
Lemma 1 with `k=3`.

For color `c`, let `J_c` be the union of the original arcs on all linkage
paths of color `c`, in both pieces.  At every trace `t`, the coloring supplies
a color-`c` path whose interval contains `t`.  By (4), that path meets every
local boundary of trace `t` in its own piece.  Hence `J_c` covers trace `t`
globally: every global boundary at that trace contains the local boundary
met by the path.

This holds for every relevant trace, so `J_c` is a dijoin.  The three sets
`J_1,J_2,J_3` are pairwise arc-disjoint because the local linkages are
arc-disjoint, the pieces have disjoint arc sets, and each path receives only
one color.  Thus they are three disjoint dijoins.  QED

Unlike a pairwise Hall matching, Lemma 1 coordinates all chain traces at
once.  It shows that once the local interval linkages exist, arbitrary
variation of the rank sequence causes no further global obstruction.

## Exact failure of chain-wide augmentation

Take ordered separator vertices

```text
l, z_1, z_2, o
```

and the serial directed multigraph

```text
l ==(two parallel arcs)==> z_1 --(one arc)--> z_2
  ==(two parallel arcs from z_2)==> o.
```

Equivalently, its arc multiplicities on the three consecutive links are
`(2,1,2)`.  Use the three traces

```text
R_0={l},
R_1={l,z_1},
R_2={l,z_1,z_2}.                                        (6)
```

All vertices lie in the separator, so each trace has one local shore and its
boundary is the corresponding parallel link.  Therefore

```text
(mu_0,mu_1,mu_2)=(2,1,2).                               (7)
```

The network pinned only at `l` and `o`, with both intermediate vertices
free, has maximum flow one because every `l-o` path uses the central arc.
Thus a chain-wide base flow supplies only one path covering all three traces.
Augmenting only its total source--sink value cannot realize the required two
endpoint supports in (7): those require paths which terminate at `z_1` and
new paths which begin at `z_2`.

This is not a packing obstruction.  Pair the two left arcs with the two
right arcs into two arc-disjoint slots and place the central arc in either
slot.  Both slots cover traces 0 and 2, and one covers trace 1, exactly
realizing (7).  In linkage language, use two intervals `{0}`, one interval
`{1}`, and two intervals `{2}`, grouping paths into colored slots only after
the global interval-coloring step.

The example isolates the defect in the proposed induction: adjacent
terminal augmentation can preserve one old terminal class, but over a
longer chain the rank may fall and rise.  A single conserved flow cannot
represent that deficiency accumulation.  Intermediate births and deaths,
encoded by the interval linkage, are necessary.

Parallel arcs can be replaced by internally vertex-disjoint length-two
paths if a simple digraph example is desired; the same serial cut values and
argument remain.

## What remains local

Theorem 2 proves that capped-depth interval linkages are sufficient and that
their coloring always satisfies all global trace demands.  It does not claim
that every directed piece has such a linkage.  Establishing that existence
statement, or finding a directed counterexample to it, is now the exact
local target.

The fixed-trace max-flow theorem supplies `a_it` disjoint covers separately
at every trace, while adjacent augmentation supplies a linkage across one
step.  The missing assertion is a common-capacity exchange theorem across
all steps which permits paths to start and stop at intermediate layers.  The
serial example shows that replacing it by one hull max-flow theorem is
strictly too weak.

## Mandatory filters

1. **Schrijver filter: passed.**  The linkage consists of actual paths using
   pairwise disjoint unit arcs.  Coloring those paths produces unweighted
   arc sets; no weighted cut value is converted into a packing.  Existence
   of the linkage is retained as a substantive hypothesis.
2. **Lucchesi--Younger filter: passed.**  No dicut/dijoin role reversal is
   used.  Each path is checked directly against incoming-closed shores by
   its endpoints, and each colored union is checked trace by trace.
3. **Easy-direction filter: passed.**  Lemma 1 explicitly colors paths and
   Theorem 2 explicitly constructs three disjoint dijoins.  The cut
   inequality (5) is only an input to that construction.

## Status and review targets

The theorem and obstruction are noncomputational and self-contained.  They
remain `sketch` until independently reviewed.  The highest-risk points are
the representative invariant in Lemma 1, the claim that a layer-to-layer
path meets every fixed-trace boundary in its interval, and the passage from
local path coverage to every global dicut.
