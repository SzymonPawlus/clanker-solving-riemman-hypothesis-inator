# Exact `tau=3` trace obstructions and the limit of recolouring

**Issue:** #222. **Status:** `sketch`, targeting `verified:review`.

This attack addresses the existential gap after the prescribed-slot theorem
of PR #220.  It proves that merely permuting the three local colours can never
repair a Hall obstruction, classifies every irreducible obstruction by at
most a `2 x 2` rectangle of directed trace failures, and gives a local
unique-defect condition that forces compatibility degree at least two.

The classification applies in particular to the connected interfaces of at
most five arcs isolated in PR #215, but does not assume that unreviewed result.

## Definitions and sanity checks

For a finite digraph, a **dicut** is a nonempty outgoing boundary
`delta+(U)` with `delta-(U)=empty`.  A **dijoin** meets every dicut.  Three
disjoint dijoins are equivalently three disjoint arc sets such that every
dicut contains an arc from each set; unused arcs can then be assigned
arbitrarily.

A directed path has singleton prefix dicuts, a directed cycle has no dicut,
and the DAG `s1->t1, s2->t1, s2->t2` has singleton-source dicuts although
`s1` cannot reach `t2`.  Thus every shore below is incoming-closed; a cut
with arcs in both directions is not silently called a dicut.

Let `D=D1 union D2`, with disjoint arc sets, common vertex separator `S`, and
no other overlap.  For `T subseteq S`, let `B_i(T)` contain the local outgoing
boundaries of all incoming-closed shores in `D_i` having trace `T` on `S`.
The empty boundary is retained.  Write `z_i(T)=1` if it occurs.

A local slot `X subseteq A(D_i)` **covers T** if it meets every nonempty
member of `B_i(T)`.  Let `F_i(X)` be the set of traces it does not cover.
Define the optional traces

```text
O = {T : z_1(T)=z_2(T)=0}.
```

A trace is **forced onto piece 1** if `z_2(T)=1`, and forced onto piece 2 if
`z_1(T)=1`.

## Pair compatibility, proved directly

Incoming-closed local shores with the same trace unite to a global
incoming-closed shore, and their boundaries have disjoint union equal to the
global boundary.  Conversely every global dicut restricts this way.

It follows that local slots `X_1,X_2` have dijoin union exactly when:

1. `X_1` covers every trace forced onto piece 1;
2. `X_2` covers every trace forced onto piece 2; and
3. `F_1(X_1) intersection F_2(X_2) intersection O` is empty.

For necessity, an empty realization on one side pairs with any missed
nonempty boundary on the other to form a missed global dicut.  If an optional
trace is missed on both sides, two missed nonempty boundaries unite to a
missed global dicut.  Conversely, for any global dicut, an empty restriction
invokes the forced condition; if both restrictions are nonempty, either a
forced condition applies or the optional failure sets are disjoint.  Hence
one restriction is hit.

This proof records the directed witnesses behind every missing compatibility
edge; it is not an invocation of cut/dijoin duality.

## The compatibility graph at three colours

Let `X_i^1,X_i^2,X_i^3` be pairwise arc-disjoint slots in piece `i`, with
empty slots allowed.  Form the bipartite graph `Gamma` on the two triples of
slots, joining `a` to `b` when `X_1^a union X_2^b` is a dijoin by the criterion
above.  A perfect matching explicitly constructs three disjoint global
dijoins.

Call a slot **forced-bad** if it misses a trace forced onto its own piece.
Such a slot is isolated in `Gamma`.  If neither endpoint is forced-bad, then

```text
a--b is absent exactly when
F_1(X_1^a) intersection F_2(X_2^b) intersection O != empty.       (1)
```

Thus every non-forced missing edge carries an explicit optional trace and a
pair of nonempty local dicuts missed by its endpoints.  Their union is an
explicit missed global dicut.

## Exact obstruction theorem

**Theorem 1.**  The three local slots cannot be bijectively paired into three
global dijoins if and only if at least one of the following occurs (with the
two pieces interchangeable):

1. **isolated-slot obstruction:** some piece-1 slot is incompatible with all
   three piece-2 slots; or
2. **collision rectangle:** there are distinct piece-1 slots `a,a'` and
   distinct piece-2 slots `b,b'` such that all four pairs
   `(a,b),(a,b'),(a',b),(a',b')` are incompatible.

Every incompatibility in these configurations is witnessed either by a
forced-bad endpoint or, through (1), by an optional trace missed on both
sides.  Consequently an obstruction has a directed certificate consisting
of at most three trace witnesses in case 1 and at most four in case 2.

**Proof.**  If a slot is isolated, no perfect matching can cover it.  In a
collision rectangle, the two left slots have neighbors among at most the one
remaining right slot, violating Hall's condition.

Conversely, if `Gamma` has no perfect matching, Hall gives a left slot set
`R` with `|N(R)|<|R|`.  If `|R|=1`, its member is isolated.  If `|R|=2`, at
least two right slots lie outside `N(R)`, and these two together with `R`
form a collision rectangle.  If `|R|=3`, some right slot is isolated, which
is case 1 after interchanging the pieces.  These exhaust the possibilities.
The trace-witness bounds follow by choosing one witness for each absent edge
needed in the obstruction.  QED

This is the exact irreducible finite configuration requested by the mixed
separator attack.  It is “directed” rather than merely graph-theoretic
because every absent edge is backed by compatible-trace local dicuts whose
union is a global dicut missed by that slot pair.

## Recolouring cannot remove an obstruction

**Proposition 2.**  Permuting the three colour names independently in either
piece preserves all compatibility degrees and preserves whether a perfect
matching exists.

**Proof.**  A colour permutation only permutes the corresponding vertices on
one side of `Gamma`; it changes neither the local arc sets nor whether any
pair has dijoin union.  The new compatibility graph is isomorphic to the old
one by row and column permutations.  Degrees and Hall inequalities are
invariant.  QED

Therefore “match the boundary colours differently” cannot by itself resolve
a failed three-colour gluing.  Any successful repair must exchange arcs
between local slots or choose a genuinely different local packing.  This
rules out a tempting but ineffective route, including for a one-way
three-arc dicut whose three boundary arcs are already rainbow.

The reason is the phantom-crossing phenomenon.  Contracting the far piece can
make a boundary arc cross a local shore even when both endpoints lie inside
the corresponding global shore.  That arc may be the only local witness of
its colour.  Relabeling it does not create the missing internal witness; the
forced/optional trace data above detects exactly this failure.

## A sufficient condition eliminating all Hall obstructions

**Theorem 3 (unique optional defect).**  Suppose:

1. no slot is forced-bad;
2. every slot fails to cover at most one optional trace; and
3. for every optional trace `T`, at most one slot in each piece fails to
   cover `T`.

Then every vertex of `Gamma` has degree at least two.  Hence `Gamma` has a
perfect matching, and the slot unions give three disjoint global dijoins.

**Proof.**  Fix a slot in piece 1.  If it covers all optional traces, (1)
makes it compatible with all three opposite slots.  Otherwise it fails one
trace `T`.  By condition 3, at most one piece-2 slot fails `T`; equation (1)
therefore excludes at most one neighbor.  Its degree is at least two.  The
same argument is symmetric.

A balanced `3 by 3` bipartite graph of minimum degree two has a perfect
matching: a one-vertex Hall set has at least two neighbors; a two-vertex Hall
set has at least two; and if all three left vertices had at most two total
neighbors, the omitted right vertex would have degree zero.  QED

This condition is stronger than necessary but local and constructive.  It
identifies the precise exchange goal for a future packing theorem: distribute
optional trace defects so no colour carries two trace defects and no trace
defect is repeated by two colours on the same side.  Under that property the
desired compatibility degree bound follows automatically, including across
interfaces of at most five arcs.

## Sharpness of the local conditions

Each clause of Theorem 3 blocks a genuine obstruction mechanism.

- A forced-bad slot is isolated regardless of the opposite packing.
- If one slot fails two optional traces, it can collide with two different
  opposite slots and become degree one.
- If two slots on each side repeat the same optional defect, they form the
  collision rectangle of Theorem 1.

These are logical sharpness statements about trace profiles, not claims that
every abstract profile is realizable by a digraph.  Realizability, and an arc
exchange lemma forcing the unique-defect property from `tau=3`, remain the
next mathematical bottleneck.

## Mandatory filters

1. **Schrijver filter: passed.**  The conclusion uses three supplied,
   pairwise disjoint slots of ordinary unit-capacity arcs.  Weighted minimum
   dicut value three does not provide such slots; zero-weight arcs can define
   the same trace shores but cannot be used in a packed dijoin.  No weighted
   packing equality is inferred.  The classification itself is a conditional
   finite hitting statement and does not purport to derive its input from
   weighted `tau`.
2. **Lucchesi--Younger filter: passed.**  No min-dijoin/max-dicut theorem is
   used.  Compatibility is proved directly by restricting an arbitrary
   global dicut, and Hall is applied only to the finite slot graph.
3. **Easy-direction filter: passed.**  When the sufficient condition holds,
   a perfect matching explicitly constructs three pairwise disjoint global
   dijoins.  The trivial upper bound from a size-three dicut is not used as
   existence.

## Scope and review targets

Theorems 1 and 3 are noncomputational.  They solve the compatibility and
recolouring questions for prescribed slots and isolate the exact profile an
arc-exchange argument must forbid.  They do **not** prove that arbitrary
`tau=3` local packings can always be exchanged into unique-defect form, so
they do not settle Woodall's conjecture at `tau=3`.

The highest-risk points for review are the empty-boundary/forced-trace logic,
the completeness of the two Hall obstruction types, and the distinction
between colour relabeling (proved useless) and exchanging arcs between slots
(still open).
